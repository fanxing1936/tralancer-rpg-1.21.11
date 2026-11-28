# -*- coding: utf-8 -*-
"""主世界地形与群系（策划书：TRALANCER 主世界群系策划书，2026-11-26）。

第一期：10000×10000 的大陆，其余全是海；按纬度分气候（北冷南热）；河网与内海；
平原、森林、原野、雪原、沙漠五个基础群系，加河、滩、海。不保留任何原版结构
（新群系不在原版结构的群系标签里，原版结构自然不生成，要塞也一样）。

做法沿用失乐园的研究（docs/TERRAIN-STUDY.md）：
  * 坐标还原：两到三张噪声在原点附近线性化，解出 x、z，于是能写「离边多远」「离原点多远」；
  * 每个尺度一张噪声，样条节点按噪声分布的分位数放；
  * 洞穴、含水层、矿脉直接引用原版的 minecraft:overworld/* 密度函数（不重写）；
  * 地表规则与群系 JSON 以客户端 jar 里的原版文件为底（mc_env），只改我们要改的。

write(rpg) 写正式文件；write(rpg, sc=16, tag='ow_map') 另写一份缩小 16 倍的「地图维度」，
用来在一千多个区块里看到整块大陆（只用于测试，不进正式包）。
"""
import copy
import io
import json
import os
import zipfile

NS = "rpg"
SEA = 63
MIN_Y, HEIGHT = -64, 1088      # 用户 2026-11-26：高度上限 1024（最高可建到 y=1023），给超高地形留空间
HALF = 5000          # 大陆半宽（格）
UNIT = 1000.0        # 坐标还原的单位：1000 格
EPS = 1e-10

# ------------------------------------------------------------------ 原版文件
_JAR = None


def _vanilla(rel):
    global _JAR
    if _JAR is None:
        import mc_env
        _JAR = zipfile.ZipFile(mc_env.JAR)
    return json.loads(_JAR.read("data/minecraft/" + rel).decode("utf-8"))


# ------------------------------------------------------------------ 节点
def op(t, a, b): return {"type": "minecraft:" + t, "argument1": a, "argument2": b}
def add(*xs):
    r = xs[0]
    for x in xs[1:]: r = op("add", r, x)
    return r
def mul(*xs):
    r = xs[0]
    for x in xs[1:]: r = op("mul", r, x)
    return r
def sub(a, b): return add(a, mul(-1.0, b))
def un(t, a): return {"type": "minecraft:" + t, "argument": a}
def clamp(a, lo, hi): return {"type": "minecraft:clamp", "input": a, "min": lo, "max": hi}
def fc(a): return un("flat_cache", a)
def mn(a, b): return {"type": "minecraft:min", "argument1": a, "argument2": b}
def mx(a, b): return {"type": "minecraft:max", "argument1": a, "argument2": b}
def spline(coord, pts):
    return {"type": "minecraft:spline", "spline": {"coordinate": coord, "points": [
        {"location": float(p[0]), "value": float(p[1]), "derivative": float(p[2] if len(p) > 2 else 0.0)} for p in pts]}}
def lin(coord, pts):
    """折线：中间点的斜率取两侧平均，端点为 0。"""
    out = []
    for i, (x, v) in enumerate(pts):
        s = (pts[i + 1][1] - pts[i - 1][1]) / (pts[i + 1][0] - pts[i - 1][0]) if 0 < i < len(pts) - 1 else 0.0
        out.append((x, v, s))
    return spline(coord, out)


class Gen:
    def __init__(self, data, sc=1.0, tag="overworld"):
        self.data, self.sc, self.tag = data, sc, tag
        self.files = {}

    # ---- 写文件
    def w(self, rel, obj):
        self.files[rel] = obj

    def flush(self):
        for rel, obj in self.files.items():
            p = os.path.join(self.data, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with io.open(p, "w", encoding="utf-8") as fh:
                json.dump(obj, fh, ensure_ascii=False, indent=1)
                fh.write("\n")
        return len(self.files)

    def df(self, name, obj):
        self.w("%s/worldgen/density_function/%s/%s.json" % (NS, self.tag, name), obj)
        return "%s:%s/%s" % (NS, self.tag, name)

    def nz(self, name, first, amps):
        """噪声定义放在共用目录（正式与地图维度同一张噪声，地图才对得上）。"""
        self.w("%s/worldgen/noise/ow/%s.json" % (NS, name), {"firstOctave": first, "amplitudes": amps})
        return "%s:ow/%s" % (NS, name)

    def noise(self, n, xz, y=0.0):
        return {"type": "minecraft:noise", "noise": n, "xz_scale": xz * self.sc, "y_scale": y}

    def warped(self, n, xz, amp, wx, wz):
        """在 (x + amp·wx, z + amp·wz) 取样；amp 单位为格。"""
        s = xz * self.sc
        return {"type": "minecraft:shifted_noise", "noise": n, "xz_scale": s, "y_scale": 0.0,
                "shift_x": mul(amp * xz, wx), "shift_y": 0.0, "shift_z": mul(amp * xz, wz)}
        # 位移加在缩放后的噪声坐标上：要按 xz（不含 sc）乘，地图维度（sc=16）才和真实世界一致。
        # 2026-11-26 之前误乘了 sc，地图里的扭曲被放大 16 倍——用户看图认可的大陆形状是放大后的样子，
        # 所以大陆尺度的三处扭曲（cont_big、fracture、spine）幅度乘了 16 保住那个形状。

    # ---- 坐标还原（失乐园验证过：48 个种子、到两千万格）
    def coords(self):
        names = [self.nz("coord_" + c, 0, [1.0]) for c in "abc"]
        h = EPS * UNIT
        K = 1e5
        Kv = self.sc / h / K                    # 地图维度：解出的坐标放大 sc 倍
        Ks = 1.0 / h / K
        def at(n, dx, dz):
            return {"type": "minecraft:shifted_noise", "noise": n, "xz_scale": 0.0, "y_scale": 0.0, "shift_x": dx, "shift_y": 0.0, "shift_z": dz}
        vals = []
        for n in names:
            o = at(n, 0.0, 0.0)
            k = n.split("/")[1]
            vals.append((self.df(k + "_v", fc(mul(Kv, mul(K, sub({"type": "minecraft:noise", "noise": n, "xz_scale": EPS, "y_scale": 0.0}, o))))),
                         self.df(k + "_x", fc(mul(Ks, mul(K, sub(at(n, h, 0.0), o))))),
                         self.df(k + "_z", fc(mul(Ks, mul(K, sub(at(n, 0.0, h), o)))))))
        def solve(p, r):
            (a, a1, a2), (b, b1, b2) = p, r
            det = sub(mul(a1, b2), mul(a2, b1))
            inv = un("invert", det)
            return det, mul(sub(mul(b2, a), mul(a2, b)), inv), mul(sub(mul(a1, b), mul(b1, a)), inv)
        d_ab, x_ab, z_ab = solve(vals[0], vals[1])
        _, x_ac, z_ac = solve(vals[0], vals[2])
        det = self.df("det_ab", fc(un("abs", d_ab)))
        pick = lambda p, q: {"type": "minecraft:range_choice", "input": det, "min_inclusive": 0.1, "max_exclusive": 1000.0, "when_in_range": p, "when_out_of_range": q}
        x = self.df("x", fc(clamp(pick(x_ab, x_ac), -40000.0, 40000.0)))
        z = self.df("z", fc(clamp(pick(z_ab, z_ac), -40000.0, 40000.0)))
        return x, z


# ------------------------------------------------------------------ 分位数（单张噪声，按幅值查；来自失乐园在 1.21.11 的实测）
# 正态近似：p → z 分数；各幅值组合的标准差实测 0.25～0.31
def q(p, sd=0.28):
    """噪声值的分位数（p 为百分比）。单张多倍频噪声近似正态，标准差实测 0.25～0.31。"""
    from statistics import NormalDist
    return NormalDist().inv_cdf(p / 100.0) * sd


# ------------------------------------------------------------------ 布局常量（单位 1000 格；坐标 z 正 = 南）
VOLCANOES = [(3.0, 1.9, 0.42), (-2.6, 3.6, 0.45), (-4.1, 2.0, 0.36)]   # 中心 x, z, 半径 —— 东南大岛北部、西南大陆两座
VOLC_PEAK, VOLC_FLOOR = 250.0, 160.0                                  # 火山口沿与火山口底（相对海平面，格）
WAR = (2.7, 3.55, 0.8)                                               # 战争前线：东南大岛南部
T_EDGES = (-0.5, -0.2, 0.2)                                         # 寒 | 凉 | 温 | 热
H_EDGES = (-0.12, 0.12)                                               # 干 | 中 | 湿
W_EDGE = 0.05                                                         # 怪异度：变体


def band_lo(v, e, w=0.05): return spline(v, [(e - w, 1.0), (e + w, 0.0)])
def band_hi(v, e, w=0.05): return spline(v, [(e - w, 0.0), (e + w, 1.0)])
def band_mid(v, a, b, w=0.05): return spline(v, [(a - w, 0.0), (a + w, 1.0), (b - w, 1.0), (b + w, 0.0)])


# ------------------------------------------------------------------ 地形
def terrain(g):
    # 注意（2026-11-26 实测）：每建一个 NoiseChunk（每个区块，加上每次结构投影地表高度）游戏都会把整棵路由树
    # 「引用全展开」再哈希一遍；被多处引用的大函数会被重复展开。坐标还原 x/z 每次展开约 190 个节点，
    # 所以：x、z 只在少数几个函数里出现；这几个函数也尽量少被引用。改动前用 dfcost 量一下展开后的节点数。
    x, z = g.coords()
    r2 = g.df("r2", fc(add(un("square", x), un("square", z))))
    N = lambda name, first, amps: g.nz(name, first, amps)
    at0 = lambda n: {"type": "minecraft:shifted_noise", "noise": n, "xz_scale": 0.0, "y_scale": 0.0, "shift_x": 0.0, "shift_y": 0.0, "shift_z": 0.0}

    n_temp, n_hum, n_weird = N("temperature", -11, [1.0, 0.4]), N("humidity", -10, [1.0, 0.4]), N("weird", -10, [1.0, 0.4])
    n_river = N("river", -10, [1.0, 0.45, 0.2])
    n_wx, n_wz = N("warp_x", -9, [1.0, 0.5]), N("warp_z", -9, [1.0, 0.5])
    n_hill, n_det = N("hills", -8, [1.0, 0.55, 0.3]), N("detail", -5, [1.0, 0.5])
    wx, wz = g.df("warp_x", fc(g.noise(n_wx, 1.0))), g.df("warp_z", fc(g.noise(n_wz, 1.0)))

    # ---- 陆地：碎而不散的三块大陆（见策划书）。出生点附近强制为陆地，外圈强制为海（大陆半径约 4.9 千格）
    n_c1, n_c2, n_frac = N("cont_big", -11, [1.0, 0.45, 0.2]), N("cont_mid", -9, [1.0, 0.5, 0.25]), N("fracture", -12, [1.0, 0.3])
    n_cwx, n_cwz = N("cont_warp_x", -11, [1.0, 0.5]), N("cont_warp_z", -11, [1.0, 0.5])
    cwx, cwz = g.df("cont_warp_x", fc(g.noise(n_cwx, 1.14))), g.df("cont_warp_z", fc(g.noise(n_cwz, 1.14)))
    F = lin(r2, [(0.0, 1.6), (0.55 ** 2, 1.6), (1.1 ** 2, 0.6), (2.4 ** 2, 0.6), (3.9 ** 2, 0.25), (4.6 ** 2, -0.3), (5.0 ** 2, -1.2), (5.5 ** 2, -2.0)])
    big = g.warped(n_c1, 0.79, 420.0 * 16, cwx, cwz)
    mid = g.noise(n_c2, 0.73)
    frac = un("abs", g.warped(n_frac, 1.0, 500.0 * 16, cwz, cwx))
    n_gate = N("fracture_gate", -10, [1.0, 0.5])
    gate = lin(g.noise(n_gate, 0.6), [(q(25), 0.0), (q(45), 1.0)])
    fjord = mul(gate, lin(frac, [(0.0, 1.0), (0.03, 0.8), (0.055, 0.2), (0.09, 0.0)]))
    n_s1, n_s2, n_sw = N("strait_a", -11, [1.0, 0.5, 0.25]), N("strait_b", -11, [1.0, 0.5, 0.25]), N("strait_width", -9, [1.0, 0.5])
    zs = g.df("strait_zs", fc(add(z, -1.2, mul(-1.8, g.noise(n_s1, 0.9)))))
    d1 = un("abs", zs)
    d2 = un("abs", add(x, -0.7, mul(-1.8, g.noise(n_s2, 0.9))))
    # 竖向海峡只在横向海峡以南：北边给 d2 加一大截
    north = lin(zs, [(-0.15, 9.0), (0.15, 0.0)])
    wv = lin(g.noise(n_sw, 1.0), [(q(5), 0.06), (q(15), 0.11), (q(50), 0.17), (q(95), 0.24)])
    strait = lin(sub(mn(d1, add(d2, north)), wv), [(-0.06, 2.4), (0.0, 1.6), (0.08, 0.4), (0.16, 0.0)])
    coastal = lin(add(F, mul(1.9, big)), [(-0.7, 0.0), (-0.3, 1.0), (0.4, 1.0), (0.8, 0.4)])
    C = add(F, mul(1.5, big), mul(0.25, coastal, mid), mul(-1.0, add(fjord, strait)), 0.18)
    land = g.df("land", fc(clamp(mul(1.6, C), -1.0, 1.0)))

    # ---- 气候：北冷南热 + 噪声。出生点 1 千格内把噪声在原点的值减掉，让出生点落在「温」带中间
    #      （整张图都减会按种子把气候整体平移，2026-11-26 实测热带被压没）
    spawn_t = spline(r2, [(0.6 ** 2, 1.0), (1.2 ** 2, 0.0)])
    t_raw = add(mul(0.17, z), mul(0.55, sub(g.noise(n_temp, 1.365), mul(spawn_t, at0(n_temp)))))
    temp = g.df("temp", fc(clamp(t_raw, -1.0, 1.0)))
    hum = g.df("hum", fc(g.noise(n_hum, 1.02)))
    weird = g.df("weird", fc(g.noise(n_weird, 1.0)))
    n_j1, n_j2, n_j3 = N("jit_a", -8, [1.0, 0.5]), N("jit_b", -6, [1.0, 0.5]), N("jit_c", -4, [1.0, 0.5])
    n_k1, n_k2, n_k3 = N("jit_d", -8, [1.0, 0.5]), N("jit_e", -6, [1.0, 0.5]), N("jit_f", -4, [1.0, 0.5])
    jt = add(mul(0.32, g.noise(n_j1, 1.28)), mul(0.1, g.noise(n_j2, 1.07)), mul(0.02, g.noise(n_j3, 0.8)))
    jh = add(mul(0.32, g.noise(n_k1, 1.28)), mul(0.1, g.noise(n_k2, 1.07)), mul(0.02, g.noise(n_k3, 0.8)))
    temp_b = g.df("temp_biome", fc(clamp(add(temp, jt), -1.0, 1.0)))
    hum_b = g.df("hum_biome", fc(clamp(add(hum, jh), -1.0, 1.0)))

    # ---- 气候权重（平滑，供地形用）
    Tc, Th = band_lo(temp, T_EDGES[0]), band_hi(temp, T_EDGES[2])
    Tk, Tm = band_mid(temp, T_EDGES[0], T_EDGES[1]), band_mid(temp, T_EDGES[1], T_EDGES[2])
    Hd, Hw = band_lo(hum, H_EDGES[0], 0.06), band_hi(hum, H_EDGES[1], 0.06)
    Hm = band_mid(hum, H_EDGES[0], H_EDGES[1], 0.06)
    Wv = band_hi(weird, W_EDGE, 0.07)
    Tc, Th, Tk, Tm, Hd, Hw, Hm, Wv = [g.df("w_" + n, fc(v)) for n, v in zip(("cold", "hot", "cool", "mild", "dry", "wet", "midh", "weird"), (Tc, Th, Tk, Tm, Hd, Hw, Hm, Wv))]
    one_m = lambda a: add(1.0, mul(-1.0, a))

    # ---- 各群系的地形形状（格，相对内陆基准）
    h0 = g.df("hill", fc(lin(g.noise(n_hill, 0.85), [(q(5), -3.0), (q(50), 2.0), (q(95), 13.0)])))
    n_creek, n_can, n_spr, n_plat, n_dune, n_run = N("creek", -7, [1.0, 0.5]), N("canyon", -8, [1.0, 0.5, 0.25]), N("spring", -6, [1.0, 0.5]), N("plateau", -9, [1.0, 0.45, 0.2]), N("dune", -6, [1.0, 0.4]), N("runoff", -8, [1.0, 0.5, 0.25])
    n_m1, n_m2, n_m3, n_m4 = N("mesa_a", -8, [1.0, 0.5]), N("mesa_b", -8, [1.0, 0.5]), N("mesa_c", -7, [1.0, 0.5]), N("mesa_d", -7, [1.0, 0.5])
    S = {}
    S["plains"] = h0
    S["forest"] = mul(1.3, h0)
    S["wildfield"] = mul(0.6, h0)
    S["golden"] = mul(0.9, h0)
    S["lavender"] = add(mul(1.1, h0), lin(un("abs", g.warped(n_creek, 0.8, 40.0, wx, wz)), [(0.0, -5.0), (0.02, -4.0), (0.05, 0.0)]))
    S["snow"] = mul(0.45, h0)
    S["glacier"] = mul(0.3, h0)
    S["geyser"] = add(20.0, mul(0.8, h0),
                      lin(un("abs", g.warped(n_can, 0.78, 120.0, wx, wz)), [(0.0, -48.0), (0.022, -44.0), (0.04, -12.0), (0.065, 0.0)]),
                      lin(g.noise(n_spr, 1.0), [(q(94), 0.0), (q(96.5), -2.0), (q(99), -3.0)]))
    pl = g.noise(n_plat, 0.98)
    S["warped"] = add(6.0, mul(0.5, h0), lin(pl, [(q(40), 0.0), (q(44.5), 52.0), (q(48), 58.0), (q(80), 66.0), (q(97), 82.0)]))
    dn = g.warped(n_dune, 0.71, 18.0, wx, wz)
    S["desert"] = lin(dn, [(-0.5, 0.0), (-0.12, 4.5), (0.0, 10.0), (0.06, 3.0), (0.3, 0.0)])
    # 侵蚀沙漠：三层逐层侵蚀 + 径流沟（径流噪声 xz=1、不扭曲，地表规则用同一张噪声铺红沙）
    e, m = 1.0, None
    for k, (first, xz, st, c) in enumerate(((-7, 1.28, 8.0, 0.18), (-5, 0.8, 5.0, 0.30), (-4, 1.0, 3.0, 0.40))):
        nm = N("ero%d" % k, first, [1.0, 0.5])
        def sh(a_, b_, nm=nm, xz=xz):
            if not a_ and not b_: return g.noise(nm, xz)
            s_ = xz * g.sc
            return {"type": "minecraft:shifted_noise", "noise": nm, "xz_scale": s_, "y_scale": 0.0, "shift_x": a_ * xz, "shift_y": 0.0, "shift_z": b_ * xz}
        vv = g.df("ero%d_v" % k, fc(sh(0, 0)))
        ab = lambda a_, b_: un("abs", sub(sh(a_, b_), vv))
        t_ = st * 0.7071
        gg = mul(0.5, add(mn(ab(st, 0), ab(0, st)), mn(ab(t_, t_), ab(t_, -t_))))
        e = g.df("ero%d_e" % k, fc(mul(add(c, un("square", vv), mul(3.0, fc(gg))), e)))
        m = e if m is None else add(m, e)
    ero = g.df("ero_m", fc(m))
    S["eroded"] = add(lin(ero, [(0.41, -4.0), (0.63, 12.0), (1.21, 40.0)]),
                      lin(un("abs", g.noise(n_run, 1.0)), [(0.0, -6.0), (0.02, -5.0), (0.045, 0.0)]))
    c2a = g.df("mesa_c2a", fc(add(un("square", g.noise(n_m1, 0.73)), un("square", g.noise(n_m2, 0.73)))))
    c2b = g.df("mesa_c2b", fc(add(un("square", g.noise(n_m3, 0.71)), un("square", g.noise(n_m4, 0.71)))))
    S["mesa"] = add(mul(0.3, h0), mx(lin(c2a, [(0.0, 100.0), (0.012, 95.0), (0.016, 40.0), (0.025, 14.0), (0.045, 0.0)]),
                                     lin(c2b, [(0.0, 48.0), (0.008, 45.0), (0.011, 18.0), (0.018, 6.0), (0.03, 0.0)])))
    S["stone"] = add(-2.0, mul(0.15, h0))
    climate = add(
        mul(Tc, add(mul(Hd, add(mul(one_m(Wv), S["snow"]), mul(Wv, S["glacier"]))), mul(Hm, S["snow"]), mul(Hw, S["geyser"]))),
        mul(Tk, add(mul(Hd, S["warped"]), mul(Hm, S["wildfield"]), mul(Hw, S["lavender"]))),
        mul(Tm, add(mul(Hd, S["plains"]), mul(Hm, S["forest"]), mul(Hw, S["golden"]))),
        mul(Th, add(mul(Hd, add(mul(one_m(Wv), S["desert"]), mul(Wv, S["eroded"]))), mul(Hm, S["mesa"]), mul(Hw, S["stone"]))))
    climate = g.df("climate_h", fc(climate))

    # ---- 高山：脊状多重分形（terrain_styles.alpine_M，照 World Machine 示例 ridgy_mountains 调的，离线对比见 docs/TERRAIN-STUDY.md）
    #      主体峰顶约 y 300，少数孤峰更高（用户 2026-11-26）。坡度按 >20/>50/>70° 分成三个子群系换材质
    import terrain_dsl as TD
    import terrain_styles as TS
    JB = TD.JsonB(g)
    n_sp = N("spine", -11, [1.0, 0.5, 0.25])
    spine = g.warped(n_sp, 0.68, 600.0 * 16, cwx, cwz)
    alp = g.df("alp_w", fc(mul(lin(spine, [(q(80), 0.0), (q(88), 0.55), (q(95), 1.0)]), lin(land, [(0.1, 0.0), (0.3, 1.0)]))))
    alp2 = un("square", alp)
    gully = lin(ero, [(0.41, -10.0), (0.5, -5.0), (0.63, 0.0), (0.8, 5.0), (1.21, 9.0)])
    M = g.df("alp_shape", fc(TS.alpine_M(JB, wx, wz)))
    mtn = g.df("alp_h", fc(mul(alp2, add(M, mul(1.4, gully)))))
    s2 = TS.slope2(JB, lambda sh: TS.alpine_M(JB, wx, wz, shift=sh), alp2)
    T2 = TS.TAN2
    alp_tier = g.df("alp_tier", fc(spline(s2, [(T2[20] * 0.85, 0.0), (T2[20] * 1.15, 0.04), (T2[50] * 0.85, 0.04), (T2[50] * 1.15, 0.08),
                                                (T2[70] * 0.85, 0.08), (T2[70] * 1.15, 0.12)])))

    # ---- 火山场：一个函数同时给出锥体高度和焦木林光环。值 = 2 + 锥高（火山内），1（光环），0（外面）
    #      火山口底 = 海平面上 160，地表规则在这一高度铺岩浆
    n_wob = N("edge_wobble", -7, [1.0, 0.5, 0.25])
    wob = g.df("edge_wobble", fc(g.noise(n_wob, 1.0)))      # 让火山光环、战争前线的边缘碎一点
    vf = None
    for cx, cz, R in VOLCANOES:
        d_ = add(un("square", add(x, -cx)), un("square", add(z, -cz)), mul(0.35 * R * R, wob))
        c_ = lin(d_, [(0.0, 2 + VOLC_FLOOR), ((0.1 * R) ** 2, 2 + VOLC_FLOOR), ((0.15 * R) ** 2, 2 + VOLC_PEAK), ((0.2 * R) ** 2, 2 + VOLC_PEAK - 12),
                      ((0.45 * R) ** 2, 2 + 0.55 * VOLC_PEAK), ((0.8 * R) ** 2, 2 + 0.18 * VOLC_PEAK), (R ** 2, 2.0), ((R + 0.02) ** 2, 1.0),
                      ((R + 0.15) ** 2, 1.0), ((R + 0.22) ** 2, 0.0)])
        vf = c_ if vf is None else mx(vf, c_)
    vf = g.df("volc_field", fc(vf))
    cones = mx(add(vf, -2.0), 0.0)

    # ---- 战争前线场：2 = 核心，1..2 = 过渡，1 = 焦木林光环，0 = 外面。焊平 + 弹坑
    W = WAR[2]
    wf = g.df("war_field", fc(lin(add(un("square", add(x, -WAR[0])), un("square", add(z, -WAR[1])), mul(0.45 * W * W, wob)),
                                  [(0.0, 2.0), ((0.82 * W) ** 2, 2.0), (W ** 2, 1.0), ((W + 0.12) ** 2, 1.0), ((W + 0.2) ** 2, 0.0)])))
    war_m = spline(wf, [(1.0, 0.0), (2.0, 1.0)])
    # 战壕已删（用户 2026-11-26：影响观感），只留焊平的地面和弹坑
    n_cr1, n_cr2 = N("crater_a", -7, [1.0, 0.5]), N("crater_b", -7, [1.0, 0.5])
    crat = add(un("square", g.noise(n_cr1, 1.16)), un("square", g.noise(n_cr2, 1.16)))
    S_war = add(mul(0.25, h0), lin(crat, [(0.0, -7.0), (0.006, -6.0), (0.014, 0.6), (0.02, 0.0)]))

    # ---- 海岸断崖（只在海岸带：land 0.08..0.6）
    n_cl = N("cliff", -10, [1.0, 0.5])
    cl_n = g.df("cliff_n", fc(lin(g.noise(n_cl, 1.46), [(q(55), 0.0), (q(70), 1.0)])))
    cliff_h = mul(cl_n, lin(land, [(0.08, 0.0), (0.13, 24.0), (0.3, 34.0), (0.45, 28.0), (0.6, 0.0)]))

    # ---- 合成
    base = lin(land, [(-1.0, -40), (-0.5, -28), (-0.15, -9), (0.0, -1.5), (0.12, 1.5), (0.4, 4.0), (1.0, 6.0)])
    inland = lin(land, [(0.0, 0.0), (0.35, 1.0)])
    det = lin(g.noise(n_det, 0.8), [(q(5), -1.3), (q(95), 1.3)])
    shape = add(mul(add(1.0, mul(-1.0, war_m)), climate), mul(war_m, S_war))
    h_land = add(base, mul(inland, shape), mtn, cliff_h, det)
    # 河：把地面压到河床，两岸渐变；穿过高山就成峡谷。火山锥在河之后再加（河从火山上过只留一道干沟）
    rv = g.df("river_v", fc(un("abs", g.warped(n_river, 0.85, 80.0, wx, wz))))
    v = lin(rv, [(0.012, 0.0), (0.022, 0.12), (0.036, 0.6), (0.06, 1.0)])
    v = add(1.0, mul(add(1.0, mul(-1.0, v)), lin(land, [(-0.05, 0.0), (0.06, 1.0)]), -1.0))
    bed = -6.0
    height = g.df("height", fc(clamp(add(bed, mul(add(h_land, -bed), v), cones), -60.0, 900.0)))
    dist = add(float(SEA), height, mul(-1.0, "minecraft:y"))
    # 3D：冰尖（巨大冰原）、石柱（石林）、高山挑檐
    n_icol, n_ireg, n_scol, n_sreg, n_rough = N("ice_col", -5, [1.0, 0.5]), N("ice_reg", -8, [1.0, 0.5]), N("stone_col", -4, [1.0, 0.5]), N("stone_reg", -8, [1.0, 0.5]), N("rough", -5, [1.0, 0.6, 0.36])
    ice_m = g.df("ice_mask", fc(mul(Tc, Hd, Wv, lin(g.noise(n_ireg, 1.07), [(q(45), 0.0), (q(65), 1.0)]), lin(g.noise(n_icol, 1.33), [(q(86), 0.0), (q(97), 1.0)]))))
    st_m = g.df("stone_mask", fc(mul(Th, Hw, lin(g.noise(n_sreg, 0.85), [(q(40), 0.0), (q(60), 1.0)]), lin(g.noise(n_scol, 1.33), [(q(84), 0.0), (q(96), 1.0)]))))
    ycol = lambda pts: {"type": "minecraft:spline", "spline": {"coordinate": "minecraft:y", "points": [{"location": float(a), "value": float(b), "derivative": 0.0} for a, b in pts]}}
    sel = lambda msk, val: {"type": "minecraft:range_choice", "input": msk, "min_inclusive": -1.0, "max_exclusive": 0.02, "when_in_range": 0.0, "when_out_of_range": val}
    spires = sel(ice_m, mul(6.5, ice_m, ycol([(60, 1.0), (150, 1.0), (230, 0.0)])))
    pillars = sel(st_m, mul(2.8, st_m, ycol([(58, 1.0), (100, 1.0), (128, 0.0)])))
    rough = sel(alp, mul(0.9, alp, g.noise(n_rough, 1.07, 1.7)))
    sloped = g.df("sloped", add(mul(4.0, un("quarter_negative", mul(0.04, dist))), mul(0.25, "minecraft:overworld/base_3d_noise"), spires, pillars, rough))
    river_ix = g.df("river_ix", fc(lin(rv, [(0.012, 1.0), (0.02, 0.4), (0.03, -1.0)])))
    # ---- 特殊分区编码（群系参数 depth）：海岸断崖 0.15，高山 0.3，焦木林 0.5，火山 0.7，战争前线 0.9
    step = lambda v_, a_: spline(v_, [(a_ - 0.03, 0.0), (a_ + 0.03, 1.0)])
    cliff_code = mul(0.15, step(mul(cl_n, lin(land, [(0.05, 1.0), (0.45, 1.0), (0.6, 0.0)])), 0.5))
    volc_code = lin(vf, [(0.4, 0.0), (0.6, 0.5), (1.4, 0.5), (1.9, 0.7)])
    war_code = lin(wf, [(0.4, 0.0), (0.6, 0.5), (1.4, 0.5), (1.6, 0.9)])
    code = g.df("special", fc(mx(mx(cliff_code, mul(step(alp, 0.45), add(0.3, alp_tier))), mx(volc_code, war_code))))
    return dict(sloped=sloped, land=land, temp=temp_b, hum=hum_b, weird=weird, river=river_ix, special=code)


def noise_settings(g, T):
    ns = _vanilla("worldgen/noise_settings/overworld.json")
    r = ns["noise_router"]
    # 用户 2026-11-26：地形纯装饰——不要洞穴、矿洞、裂缝、矿物。地下实心
    top = MIN_Y + HEIGHT
    fd = mx(T["sloped"], {"type": "minecraft:y_clamped_gradient", "from_y": MIN_Y, "to_y": MIN_Y + 24, "from_value": 1.0, "to_value": -1.0})
    fd = un("interpolated", mul(fd, {"type": "minecraft:y_clamped_gradient", "from_y": top - 16, "to_y": top, "from_value": 1.0, "to_value": 0.0}))
    r["final_density"] = fd
    ns["noise"]["height"] = HEIGHT
    r["preliminary_surface_level"] = float(MIN_Y)      # 含水层已关、没有洞穴：地表规则整列可用，省掉一整棵高度树
    for k in ("barrier", "fluid_level_floodedness", "fluid_level_spread", "lava", "vein_toggle", "vein_ridged", "vein_gap"):
        r[k] = 0.0
    ns["aquifers_enabled"] = False
    ns["ore_veins_enabled"] = False
    r["continents"] = T["land"]
    r["temperature"] = T["temp"]
    r["vegetation"] = T["hum"]
    r["erosion"] = T["river"]
    r["ridges"] = T["weird"]
    r["depth"] = T["special"]
    ns["spawn_target"] = [{"continentalness": [0.2, 1.0], "depth": 0.0, "erosion": [-1.0, 0.3], "humidity": [-1.0, 1.0],
                           "offset": 0.0, "temperature": [-0.3, 0.3], "weirdness": [-1.0, 1.0]}]
    ns["surface_rule"] = surface(ns["surface_rule"])
    return ns


# ------------------------------------------------------------------ 群系
B_ = lambda n: "%s:%s" % (NS, n)
T_BANDS = {"cold": (-1.0, T_EDGES[0]), "cool": (T_EDGES[0], T_EDGES[1]), "mild": (T_EDGES[1], T_EDGES[2]), "hot": (T_EDGES[2], 1.0)}
H_BANDS = {"dry": (-1.0, H_EDGES[0]), "mid": H_EDGES, "wet": (H_EDGES[1], 1.0)}
W_BANDS = {"plain": (-1.0, W_EDGE), "odd": (W_EDGE, 1.0)}
GRID = {("cold", "dry", "plain"): "snowfield", ("cold", "dry", "odd"): "glacier_spires", ("cold", "mid", None): "snowfield", ("cold", "wet", None): "geyser_taiga",
        ("cool", "dry", None): "warped_plateau", ("cool", "mid", None): "wildfield", ("cool", "wet", None): "lavender_forest",
        ("mild", "dry", None): "plains", ("mild", "mid", None): "forest", ("mild", "wet", None): "golden_forest",
        ("hot", "dry", "plain"): "desert", ("hot", "dry", "odd"): "eroded_desert", ("hot", "mid", None): "mesa_valley", ("hot", "wet", None): "stone_forest"}
SPECIAL = {"sea_cliffs": 0.15, "alpine": 0.3, "alpine_slope": 0.34, "alpine_rock": 0.38, "alpine_cliff": 0.42, "ashwood": 0.5, "volcano": 0.7, "war_front": 0.9}


def biome_source():
    out = []
    def e(b, t, h, c, er, w=(-1.0, 1.0), d=0.0):
        out.append({"biome": B_(b), "parameters": {"temperature": list(t), "humidity": list(h), "continentalness": list(c),
                                                   "erosion": list(er), "weirdness": list(w), "depth": d, "offset": 0.0}})
    for (tb, hb, wb), b in GRID.items():
        e(b, T_BANDS[tb], H_BANDS[hb], (0.08, 1.0), (-1.0, 0.5), W_BANDS[wb] if wb else (-1.0, 1.0))
    for b, d in SPECIAL.items():      # 火山、战争前线可以伸进海里；特殊区盖过河
        e(b, (-1.0, 1.0), (-1.0, 1.0), (-1.0, 1.0) if b in ("volcano", "war_front") else (0.08, 1.0), (-1.0, 1.0), d=d)
    for tb in T_BANDS:
        cold = tb == "cold"
        e("frozen_river" if cold else "river", T_BANDS[tb], (-1.0, 1.0), (0.03, 1.0), (0.5, 1.0), d=[0.0, 0.1])
        e("snowy_beach" if cold else "beach", T_BANDS[tb], (-1.0, 1.0), (-0.16, 0.08), (-1.0, 1.0), d=[0.0, 0.6])
        e("frozen_ocean" if cold else "ocean", T_BANDS[tb], (-1.0, 1.0), (-0.55, -0.16), (-1.0, 1.0), d=[0.0, 0.6])
        e("deep_ocean", T_BANDS[tb], (-1.0, 1.0), (-1.0, -0.55), (-1.0, 1.0), d=[0.0, 0.6])
    return {"type": "minecraft:multi_noise", "biomes": out}


# 名: (底子原版群系, 草色, 叶色, 枯叶色, 天色, 雾色, 粒子)
BIOMES = {
    "plains": ("plains", None, None, None, None, None, None),
    "forest": ("forest", None, None, None, None, None, None),
    "wildfield": ("meadow", "#8fc95a", "#7cbf4a", "#b57a3a", None, None, None),
    "snowfield": ("snowy_plains", None, None, None, None, None, None),
    "desert": ("desert", None, None, None, None, None, None),
    "lavender_forest": ("flower_forest", "#a98bd6", "#9271c9", "#8a6fb8", "#a9a4ff", "#c8b8ec", ("minecraft:spore_blossom_air", 0.004)),
    "golden_forest": ("forest", "#d9b13b", "#e0a82e", "#d08a28", None, "#e8d8b0", ("minecraft:falling_spore_blossom", 0.0)),
    "warped_plateau": ("meadow", "#167e86", "#14b485", "#167e86", "#7fb8c8", "#5aa6a8", ("minecraft:warped_spore", 0.012)),
    "geyser_taiga": ("old_growth_pine_taiga", None, None, None, None, "#cfd8dc", ("minecraft:white_ash", 0.003)),
    "glacier_spires": ("ice_spikes", None, None, None, None, None, ("minecraft:snowflake", 0.004)),
    "eroded_desert": ("desert", None, None, None, None, None, None),
    "mesa_valley": ("badlands", None, None, None, None, None, None),
    "stone_forest": ("jungle", "#6fbf55", "#5aaa3a", None, None, None, None),
    "alpine": ("meadow", None, None, None, None, None, None),
    "alpine_slope": ("meadow", None, None, None, None, None, None),     # 坡度 20-50°：青色陶瓦
    "alpine_rock": ("stony_peaks", None, None, None, None, None, None),  # 50-70°：石头+原石
    "alpine_cliff": ("stony_peaks", None, None, None, None, None, None), # >70°：方解石
    "volcano": ("badlands", "#6b5a45", "#5a4a38", "#5a4a38", "#a08070", "#8a6658", ("minecraft:ash", 0.02)),
    "ashwood": ("savanna", "#7a7050", "#6a6040", "#6a5a40", "#a8a090", "#9a9080", ("minecraft:ash", 0.008)),
    "war_front": ("plains", "#8a7a52", "#7a6a48", "#7a6448", "#c85024", "#d87034", ("minecraft:white_ash", 0.02)),
    "sea_cliffs": ("stony_shore", None, None, None, None, None, None),
    "river": ("river",) + (None,) * 6, "frozen_river": ("frozen_river",) + (None,) * 6, "beach": ("beach",) + (None,) * 6,
    "snowy_beach": ("snowy_beach",) + (None,) * 6, "ocean": ("ocean",) + (None,) * 6, "deep_ocean": ("deep_ocean",) + (None,) * 6,
    "frozen_ocean": ("frozen_ocean",) + (None,) * 6,
}
TEMPS = {"alpine": 0.4, "alpine_slope": 0.4, "alpine_rock": 0.4, "alpine_cliff": 0.4, "stone_forest": 0.95, "war_front": 0.9, "volcano": 2.0, "ashwood": 1.2, "glacier_spires": 0.0, "warped_plateau": 0.3, "geyser_taiga": 0.1}
# 植被（各群系；顺序按 VEG_ORDER 统一，避免地物顺序循环）
VEG = {
    "plains": ["patch_tall_grass_2", "patch_bush", "flower_plains", "patch_grass_plain", "patch_pumpkin", "patch_sugar_cane", "patch_firefly_bush_near_water"],
    "forest": ["forest_flowers", "patch_bush", "flower_default", "patch_grass_forest", "brown_mushroom_normal", "red_mushroom_normal", "patch_leaf_litter", "patch_sugar_cane"],
    "wildfield": ["patch_grass_meadow", "flower_meadow", "wildflowers_meadow", "patch_leaf_litter", "wildflowers_birch_forest", "flower_cherry"],
    "snowfield": ["patch_grass_badlands", "patch_sugar_cane"],
    "desert": ["patch_dry_grass_desert", "patch_dead_bush_2", "patch_cactus_desert", "patch_sugar_cane_desert"],
    "eroded_desert": ["patch_dry_grass_desert", "patch_dead_bush_2", "rpg:ow/eroded_cactus"],
    "mesa_valley": ["patch_grass_badlands", "patch_dead_bush_badlands", "patch_cactus_decorated"],
    "lavender_forest": ["rpg:ow/lav_flowers", "patch_grass_forest", "flower_default", "patch_sugar_cane", "patch_firefly_bush_near_water"],
    "golden_forest": ["rpg:ow/gold_wheat", "patch_grass_forest", "patch_berry_bush", "patch_pumpkin", "patch_leaf_litter"],
    "warped_plateau": ["rpg:ow/warped_veg"],          # 缠怨藤去掉（用户 2026-11-27）
    "geyser_taiga": ["patch_large_fern", "rpg:ow/geyser_snag", "patch_grass_taiga", "patch_berry_bush"],
    "glacier_spires": [],
    "stone_forest": ["rpg:ow/stone_bamboo", "patch_grass_forest", "patch_waterlily", "vines"],
    "alpine": ["patch_grass_meadow", "flower_meadow"],
    "alpine_slope": [], "alpine_rock": [], "alpine_cliff": [],
    "volcano": [],          # 岩浆湖放在 feats[1]（湖泊阶段）
    "ashwood": ["rpg:ow/ash_trunk", "patch_dead_bush_2", "patch_grass_badlands"],
    "war_front": ["rpg:ow/war_stump", "rpg:ow/war_web", "rpg:ow/war_skull", "patch_dead_bush_2", "patch_grass_badlands"],
    "sea_cliffs": ["patch_grass_plain"],
    "river": ["patch_sugar_cane", "seagrass_river"], "frozen_river": [], "beach": [], "snowy_beach": [],
    "ocean": ["seagrass_normal", "kelp_cold"], "deep_ocean": ["seagrass_deep", "kelp_cold"], "frozen_ocean": [],
}
VEG_ORDER = ["patch_tall_grass_2", "patch_bush", "flower_plains", "patch_grass_plain", "forest_flowers", "flower_default", "patch_grass_forest", "patch_grass_meadow", "flower_meadow", "wildflowers_meadow",
             "rpg:ow/gold_wheat", "rpg:ow/lav_flowers", "rpg:ow/warped_veg", "patch_large_fern", "rpg:ow/geyser_snag",
             "patch_grass_taiga", "patch_grass_badlands", "patch_dry_grass_desert", "patch_dead_bush_2", "patch_dead_bush_badlands",
             "patch_cactus_desert", "patch_cactus_decorated", "rpg:ow/eroded_cactus", "patch_sugar_cane_desert", "rpg:ow/stone_bamboo",
             "rpg:ow/ash_trunk", "rpg:ow/war_stump", "rpg:ow/war_web", "rpg:ow/war_skull", "patch_berry_bush", "brown_mushroom_normal", "red_mushroom_normal", "patch_pumpkin", "patch_leaf_litter", "wildflowers_birch_forest", "flower_cherry",
             "patch_sugar_cane", "patch_firefly_bush_near_water", "patch_waterlily", "vines", "seagrass_river", "seagrass_normal", "seagrass_deep", "kelp_cold"]
WATERY = ("river", "frozen_river", "beach", "snowy_beach", "ocean", "deep_ocean", "frozen_ocean", "stone_forest")


def _attr(o, key, val):
    o.setdefault("attributes", {})[key] = val


def biomes(g):
    n = 0
    for name, (src, grass, foliage, dry, sky, fog, part) in BIOMES.items():
        o = _vanilla("worldgen/biome/%s.json" % src)
        feats = [[] for _ in range(11)]
        if name in WATERY: feats[6] = ["minecraft:disk_sand", "minecraft:disk_clay", "minecraft:disk_gravel"]
        if name == "glacier_spires": feats[4] = ["minecraft:ice_spike", "minecraft:ice_patch"]
        if name == "volcano": feats[1] = ["rpg:ow/crater_lava"]
        # 不放原版泉水（spring_water / spring_lava）：用户 2026-11-26「除了河流这些，不要出现水源」
        want = set(VEG[name])
        feats[9] = [(f if f.startswith("rpg:") else "minecraft:" + f) for f in VEG_ORDER if f in want]
        feats[10] = ["minecraft:freeze_top_layer"]
        o["features"] = feats
        o["carvers"] = []
        eff = o.setdefault("effects", {})
        if grass: eff["grass_color"] = grass
        if foliage: eff["foliage_color"] = foliage
        if dry: eff["dry_foliage_color"] = dry
        if sky: _attr(o, "minecraft:visual/sky_color", sky)
        if fog: _attr(o, "minecraft:visual/fog_color", fog)
        if part and part[1] > 0: _attr(o, "minecraft:visual/ambient_particles", [{"particle": {"type": part[0]}, "probability": part[1]}])
        if name in TEMPS: o["temperature"] = TEMPS[name]
        if name == "war_front":
            o["spawners"]["creature"] = []
            o["spawners"]["monster"] = [{"type": "minecraft:zombie", "weight": 100, "minCount": 2, "maxCount": 4}, {"type": "minecraft:skeleton", "weight": 100, "minCount": 1, "maxCount": 3},
                                        {"type": "minecraft:husk", "weight": 40, "minCount": 1, "maxCount": 3}, {"type": "minecraft:pillager", "weight": 20, "minCount": 1, "maxCount": 2},
                                        {"type": "minecraft:creeper", "weight": 60, "minCount": 1, "maxCount": 2}, {"type": "minecraft:spider", "weight": 60, "minCount": 1, "maxCount": 2}]
        if name == "stone_forest":
            o["spawners"] = _vanilla("worldgen/biome/plains.json")["spawners"]
        if name == "volcano":
            o["spawners"]["creature"] = []
            o["spawners"]["monster"] = o["spawners"].get("monster", []) + [{"type": "minecraft:magma_cube", "weight": 60, "minCount": 1, "maxCount": 3}]
        g.w("%s/worldgen/biome/%s.json" % (NS, name), o)
        n += 1
    return n


# ------------------------------------------------------------------ 自定义地物
def _place(feature, pl, survive="minecraft:oak_sapling", hm="OCEAN_FLOOR"):
    pre = [{"type": "minecraft:rarity_filter", "chance": pl[1]}] if pl[0] == "rare" else [{"type": "minecraft:count", "count": pl[1]}]
    tail = [{"type": "minecraft:in_square"}, {"type": "minecraft:surface_water_depth_filter", "max_water_depth": 0}, {"type": "minecraft:heightmap", "heightmap": hm}]
    if survive: tail.append({"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:would_survive", "state": {"Name": survive, "Properties": {"stage": "0"}}}})
    return {"feature": feature, "placement": pre + tail + [{"type": "minecraft:biome"}]}


def _patch(states, tries, spread, on=None):
    prov = {"type": "minecraft:weighted_state_provider", "entries": [{"data": s, "weight": w} for s, w in states]}
    preds = [{"type": "minecraft:matching_blocks", "blocks": "minecraft:air"}]
    if on: preds.append({"type": "minecraft:matching_blocks", "offset": [0, -1, 0], "blocks": ["minecraft:" + b for b in on]})
    return {"type": "minecraft:random_patch", "config": {"tries": tries, "xz_spread": spread, "y_spread": 2, "feature": {
        "feature": {"type": "minecraft:simple_block", "config": {"to_place": prov}},
        "placement": [{"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:all_of", "predicates": preds}}]}}}


def _column(state, lo, hi):
    return {"type": "minecraft:block_column", "config": {"direction": "up", "allowed_placement": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
            "prioritize_tip": False, "layers": [{"height": {"type": "minecraft:uniform", "min_inclusive": lo, "max_inclusive": hi},
                                                 "provider": {"type": "minecraft:simple_state_provider", "state": state}}]}}


def features(g):
    S = lambda n, **p: dict({"Name": "minecraft:" + n}, **({"Properties": {k: str(v) for k, v in p.items()}} if p else {}))
    CF, PF = {}, {}
    CF["lav_flowers"] = _patch([(S("allium"), 3), (S("lilac", half="lower"), 2), (S("pink_petals", facing="north", flower_amount=3), 2)], 48, 6, ["grass_block", "dirt", "podzol"])
    CF["eroded_cactus"] = _patch([(S("cactus", age=0), 1)], 6, 4, ["sand", "red_sand"])
    CF["geyser_snag"] = _column(S("stripped_spruce_log", axis="y"), 4, 9)
    CF["ash_trunk"] = _column(S("dark_oak_log", axis="y"), 2, 6)
    CF["war_stump"] = _column(S("dark_oak_log", axis="y"), 1, 2)
    CF["war_web"] = _patch([(S("cobweb"), 1)], 6, 4)
    # 小麦用 block_column 放：simple_block 会查作物存活（要光照），生成阶段光照还没算，全会被跳过
    CF["gold_wheat"] = {"type": "minecraft:random_patch", "config": {"tries": 96, "xz_spread": 7, "y_spread": 1, "feature": {
        "feature": _column(S("wheat", age=7), 1, 1),
        "placement": [{"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:all_of", "predicates": [
            {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
            {"type": "minecraft:matching_blocks", "offset": [0, -1, 0], "blocks": "minecraft:farmland"}]}}]}}}
    # 火山口的岩浆湖：原版湖地物只在四周封闭的凹地里成形（开口就放弃），所以岩浆是静止的池子，不会顺坡流
    CF["crater_lava"] = {"type": "minecraft:lake", "config": {"fluid": {"type": "minecraft:simple_state_provider", "state": S("lava", level=0)},
                                                              "barrier": {"type": "minecraft:simple_state_provider", "state": S("blackstone")}}}
    CF["war_skull"] = _patch([(S("skeleton_skull", rotation=r), 1) for r in (0, 3, 6, 9, 12)], 3, 3)
    PF.update({
        "lav_flowers": {"feature": "rpg:ow/lav_flowers", "placement": [{"type": "minecraft:noise_threshold_count", "noise_level": 0.0, "below_noise": 1, "above_noise": 6},
                        {"type": "minecraft:in_square"}, {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}]},
        "warped_veg": _place("minecraft:warped_forest_vegetation", ("count", 4), survive=None, hm="MOTION_BLOCKING"),
        "twisting": _place("minecraft:twisting_vines", ("rare", 2), survive=None, hm="MOTION_BLOCKING"),
        "geyser_snag": _place("rpg:ow/geyser_snag", ("rare", 3), survive=None),
        "eroded_cactus": {"feature": "rpg:ow/eroded_cactus", "placement": [{"type": "minecraft:rarity_filter", "chance": 6}, {"type": "minecraft:in_square"},
                          {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}]},
        "stone_bamboo": _place("minecraft:bamboo_no_podzol", ("count", 3), survive=None, hm="MOTION_BLOCKING"),
        "ash_trunk": _place("rpg:ow/ash_trunk", ("count", 2), survive=None),
        "war_stump": _place("rpg:ow/war_stump", ("count", 1), survive=None),
        "war_web": {"feature": "rpg:ow/war_web", "placement": [{"type": "minecraft:rarity_filter", "chance": 2}, {"type": "minecraft:in_square"},
                    {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}]},
        "war_skull": {"feature": "rpg:ow/war_skull", "placement": [{"type": "minecraft:rarity_filter", "chance": 3}, {"type": "minecraft:in_square"},
                      {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}]},
        # 只在火山口底那个高度带里找地面（外坡在这一高度是陡坡，湖地物成不了形）
        "gold_wheat": {"feature": "rpg:ow/gold_wheat", "placement": [{"type": "minecraft:count", "count": 16}, {"type": "minecraft:in_square"},
                       {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}]},
        "crater_lava": {"feature": "rpg:ow/crater_lava", "placement": [{"type": "minecraft:count", "count": 6}, {"type": "minecraft:in_square"},
                        {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform", "min_inclusive": {"absolute": SEA + int(VOLC_FLOOR) - 4},
                                                                       "max_inclusive": {"absolute": SEA + int(VOLC_FLOOR) + 10}}},
                        {"type": "minecraft:environment_scan", "direction_of_search": "down", "max_steps": 16,
                         "target_condition": {"type": "minecraft:all_of", "predicates": [{"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
                                                                                         {"type": "minecraft:solid", "offset": [0, -1, 0]}]},
                         "allowed_search_condition": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"}},
                        {"type": "minecraft:biome"}]},
    })
    for k, v in CF.items(): g.w("%s/worldgen/configured_feature/ow/%s.json" % (NS, k), v)
    for k, v in PF.items(): g.w("%s/worldgen/placed_feature/ow/%s.json" % (NS, k), v)


# ------------------------------------------------------------------ 地表
def surface(vanilla_rule):
    def block(n, **p):
        d = {"Name": "minecraft:" + n}
        if p: d["Properties"] = {k: str(v) for k, v in p.items()}
        return {"type": "minecraft:block", "result_state": d}
    def cond(c, t): return {"type": "minecraft:condition", "if_true": c, "then_run": t}
    def seq(*s): return {"type": "minecraft:sequence", "sequence": list(s)}
    def no(c): return {"type": "minecraft:not", "invert": c}
    def nt(n, lo, hi): return {"type": "minecraft:noise_threshold", "noise": n, "min_threshold": lo, "max_threshold": hi}
    def bio(*b): return {"type": "minecraft:biome", "biome_is": [B_(x) for x in b]}
    def depth(add_sd, sec=0, off=0): return {"type": "minecraft:stone_depth", "offset": off, "add_surface_depth": add_sd, "secondary_depth_range": sec, "surface_type": "floor"}
    def yab(y, m=0): return {"type": "minecraft:y_above", "anchor": {"absolute": y}, "surface_depth_multiplier": m, "add_stone_depth": False}
    def water(off=-1, m=0): return {"type": "minecraft:water", "offset": off, "surface_depth_multiplier": m, "add_stone_depth": False}
    steep = {"type": "minecraft:steep"}
    A, Bn, C, M = "rpg:ow/s_a", "rpg:ow/s_b", "rpg:ow/s_c", "rpg:ow/s_m"
    SPR, RUN = "rpg:ow/spring", "rpg:ow/runoff"
    b = block
    grass, moss, dirt, podzol, coarse, rooted = b("grass_block", snowy="false"), b("moss_block"), b("dirt"), b("podzol", snowy="false"), b("coarse_dirt"), b("rooted_dirt")
    mud, roots = b("mud"), b("muddy_mangrove_roots", axis="y")
    sand, red_sand, sandstone, susp = b("sand"), b("red_sand"), b("sandstone"), b("suspicious_sand", dusted=0)
    gravel, clay, stone, andesite, diorite, cobble, tuff = b("gravel"), b("clay"), b("stone"), b("andesite"), b("diorite"), b("cobblestone"), b("tuff")
    snow_block, powder, packed_ice, blue_ice = b("snow_block"), b("powder_snow"), b("packed_ice"), b("blue_ice")
    basalt, blackstone, magma, obsidian, lava = b("basalt", axis="y"), b("blackstone"), b("magma_block"), b("obsidian"), b("lava", level=0)
    nylium, wart = b("warped_nylium"), b("warped_wart_block")
    calcite, yterra, oterra, wterra = b("calcite"), b("yellow_terracotta"), b("orange_terracotta"), b("white_terracotta")
    xor = lambda p, q_: seq(cond(nt(C, 0.0, 9.0), seq(cond(nt(Bn, 0.0, 9.0), p), q_)), seq(cond(nt(Bn, 0.0, 9.0), q_), p))
    def green(moss_t):
        mossy = seq(cond(nt(C, 0.0, 9.0), cond(nt(A, moss_t, 9.0), moss)), cond(nt(C, -9.0, 0.0), cond(nt(Bn, moss_t, 9.0), moss)))
        return seq(cond(no(water()), dirt), mossy, grass)
    muddy = seq(cond(nt(A, 0.30, 9.0), coarse), cond(nt(Bn, 0.42, 9.0), cond(water(), grass)), xor(roots, mud))
    under_water = seq(cond(nt(A, 0.25, 9.0), gravel), cond(nt(Bn, 0.35, 9.0), clay), sand)
    shore = cond(no(yab(SEA + 2, 0)), muddy)
    rocky = seq(cond(nt(A, 0.25, 9.0), andesite), cond(nt(Bn, 0.3, 9.0), gravel), cond(nt(C, 0.35, 9.0), diorite), stone)
    snowcap = seq(cond(nt(A, 0.45, 9.0), powder), snow_block)
    top = seq(
        cond(bio("ocean", "deep_ocean", "frozen_ocean"), under_water),
        cond(bio("beach", "snowy_beach"), seq(cond(nt(A, 0.42, 9.0), gravel), sand)),
        cond(bio("river", "frozen_river"), seq(cond(no(water()), under_water), muddy)),
        # 火山口底不铺岩浆（会顺外坡流下来）：铺岩浆块/黑石，岩浆只来自封闭的岩浆湖地物（rpg:ow/crater_lava）
        cond(bio("volcano"), seq(cond(no(steep), cond(yab(SEA + int(VOLC_FLOOR) - 3), cond(no(yab(SEA + int(VOLC_FLOOR) + 5)), seq(cond(nt(A, -0.1, 9.0), magma), cond(nt(Bn, 0.3, 9.0), obsidian), blackstone)))),
                                 cond(yab(SEA + 200), seq(cond(nt(A, 0.3, 9.0), magma), cond(nt(Bn, 0.2, 9.0), obsidian), blackstone)),
                                 cond(steep, seq(cond(nt(A, 0.1, 9.0), blackstone), basalt)),
                                 cond(nt(A, 0.35, 9.0), magma), cond(nt(Bn, 0.0, 9.0), basalt), cond(nt(C, 0.2, 9.0), tuff), blackstone)),
        cond(no(water()), under_water),
        cond(bio("desert"), seq(cond(steep, sandstone), sand)),
        cond(bio("eroded_desert"), seq(cond(nt(RUN, -0.02, 0.02), red_sand), cond(steep, seq(cond(nt(A, 0.2, 9.0), b("smooth_sandstone")), sandstone)),
                                       cond(nt(A, 0.18, 9.0), susp), cond(nt(Bn, 0.42, 9.0), susp), sand)),
        cond(bio("mesa_valley"), seq(cond(steep, {"type": "minecraft:bandlands"}), cond(yab(SEA + 30), seq(cond(nt(A, 0.3, 9.0), b("red_sandstone")), {"type": "minecraft:bandlands"})),
                                     cond(nt(A, 0.4, 9.0), coarse), red_sand)),
        cond(bio("glacier_spires"), seq(cond(yab(SEA + 12), seq(cond(nt(A, 0.3, 9.0), blue_ice), packed_ice)), cond(nt(M, 0.2, 9.0), snow_block), cond(nt(A, 0.45, 9.0), packed_ice), b("grass_block", snowy="true"))),
        cond(bio("snowfield"), seq(cond(nt(M, 0.25, 9.0), snow_block), cond(nt(A, 0.52, 9.0), powder), b("grass_block", snowy="true"))),
        # 高山坡度子群系（用户 2026-11-26）：>70° 方解石，50-70° 石头+原石，20-50° 青色陶瓦
        cond(bio("alpine_cliff"), calcite),
        cond(bio("alpine_rock"), seq(cond(nt(A, 0.0, 9.0), cobble), stone)),
        cond(bio("alpine_slope"), b("cyan_terracotta")),
        cond(bio("alpine"), seq(cond(yab(SEA + 240, 2), snowcap), cond(yab(SEA + 160, 2), seq(cond(steep, rocky), cond(nt(M, 0.0, 9.0), rocky), cond(nt(A, 0.2, 9.0), gravel), stone)),
                                cond(steep, rocky), green(0.25))),
        cond(bio("geyser_taiga"), seq(cond(nt(SPR, q(99), 9.0), b("water", level=0)), cond(nt(SPR, q(98.2), 9.0), calcite), cond(nt(SPR, q(97.4), 9.0), yterra), cond(nt(SPR, q(96.5), 9.0), oterra),
                                      cond(steep, seq(cond(yab(SEA + 10), cond(nt(A, 0.0, 9.0), wterra)), yterra)),
                                      cond(nt(A, 0.2, 9.0), coarse), cond(nt(Bn, 0.1, 9.0), podzol), grass)),
        # 诡异高原：诡异菌岩 + 诡异疣块 + 少量蓝色草方块（去皮诡异木已去掉，用户 2026-11-26）；
        # 一部分地块是泥巴和红树根泥巴混在一起（用户 2026-11-27）
        cond(bio("warped_plateau"), seq(cond(steep, seq(cond(nt(A, 0.1, 9.0), wart), b("deepslate", axis="y"))),
                                        cond(nt(A, 0.42, 9.0), grass), cond(nt(M, 0.3, 9.0), xor(roots, mud)),
                                        cond(nt(Bn, 0.2, 9.0), wart), nylium)),
        cond(bio("stone_forest"), seq(shore, cond(nt(A, 0.1, 9.0), moss), cond(nt(Bn, 0.15, 9.0), andesite), cond(nt(C, 0.3, 9.0), cobble), stone)),
        cond(bio("war_front"), seq(cond(nt(A, 0.38, 9.0), gravel), cond(nt(Bn, 0.45, 9.0), b("soul_soil")), muddy)),
        cond(bio("ashwood"), seq(cond(nt(A, 0.35, 9.0), coarse), cond(nt(Bn, 0.4, 9.0), b("soul_soil")), cond(nt(M, 0.3, 9.0), gravel), muddy)),
        cond(bio("sea_cliffs"), seq(cond(steep, rocky), green(0.35))),
        cond(steep, seq(cond(nt(A, 0.2, 9.0), gravel), stone)),
        shore,
        cond(bio("forest"), green(0.05)),
        cond(bio("wildfield"), green(0.30)),
        cond(bio("lavender_forest"), seq(cond(nt(A, 0.45, 9.0), rooted), cond(nt(Bn, 0.48, 9.0), podzol), grass)),
        # 丰饶森林：成片的耕地，上面由 rpg:ow/gold_wheat 种满成熟小麦（用户 2026-11-26）
        cond(bio("golden_forest"), seq(cond(no(steep), cond(nt("rpg:ow/field", q(60), 9.0), b("farmland", moisture=7))), cond(nt(A, 0.46, 9.0), coarse), grass)),
        green(0.40))
    under = seq(cond(bio("desert", "beach", "snowy_beach", "eroded_desert"), sand),
                cond(bio("mesa_valley"), red_sand),
                cond(bio("glacier_spires", "snowfield"), seq(cond(nt(A, 0.3, 9.0), packed_ice), snow_block)),
                cond(bio("volcano"), seq(cond(nt(Bn, 0.0, 9.0), basalt), blackstone)),
                cond(bio("warped_plateau"), dirt),
                cond(bio("ocean", "deep_ocean", "frozen_ocean", "river", "frozen_river"), sand),
                cond(bio("alpine_cliff"), calcite), cond(bio("alpine_rock"), seq(cond(nt(A, 0.0, 9.0), cobble), stone)), cond(bio("alpine_slope"), b("cyan_terracotta")),
                cond(bio("stone_forest", "alpine", "sea_cliffs"), stone),
                dirt)
    # 本体：露出的岩壁
    body = cond(yab(SEA - 8), seq(          # 先判高度：地下深处的石头一条群系都不查
        cond(bio("glacier_spires"), cond(yab(SEA + 3), seq(cond(nt(A, 0.35, 9.0), blue_ice), cond(nt(Bn, 0.5, 9.0), snow_block), packed_ice))),
        cond(bio("mesa_valley"), cond(yab(SEA + 1), {"type": "minecraft:bandlands"})),
        cond(bio("volcano"), cond(yab(SEA + 1), seq(cond(nt(A, 0.3, 9.0), blackstone), cond(nt(Bn, 0.35, 9.0), tuff), basalt))),
        cond(bio("warped_plateau"), cond(yab(SEA + 3), seq(cond(nt(Bn, 0.4, 9.0), wart), b("deepslate", axis="y")))),
        cond(bio("geyser_taiga"), cond(yab(SEA + 1), seq(cond(nt(A, 0.1, 9.0), wterra), yterra))),
        cond(bio("eroded_desert", "desert"), cond(yab(SEA - 2), sandstone)),
        cond(bio("alpine_cliff"), calcite), cond(bio("alpine_rock"), seq(cond(nt(A, 0.0, 9.0), cobble), stone)), cond(bio("alpine_slope"), b("cyan_terracotta")),
        cond(bio("stone_forest", "alpine", "sea_cliffs"), cond(yab(SEA - 8), seq(cond(nt(A, 0.3, 9.0), andesite), cond(nt(Bn, 0.45, 9.0), diorite), stone)))))
    bedrock, deepslate = vanilla_rule["sequence"][0], vanilla_rule["sequence"][2]
    return seq(bedrock, cond({"type": "minecraft:above_preliminary_surface"}, seq(cond(depth(False), top), cond(depth(True), under),
                                                                                  cond(bio("desert", "beach", "snowy_beach", "eroded_desert"), cond(depth(True, 6), sandstone)))),
               body, deepslate)


def surface_noises(g):
    g.nz("field", -6, [1.0, 0.5])          # 丰饶森林的麦田
    g.nz("s_a", -3, [0.8, 1.0]); g.nz("s_b", -3, [0.6, 1.0]); g.nz("s_c", -2, [1.0]); g.nz("s_m", -5, [1.0, 0.5])


# ------------------------------------------------------------------ 入口
def write(rpg, sc=1.0, tag="overworld"):
    data = os.path.join(rpg, "data")
    g = Gen(data, sc, tag)
    surface_noises(g)
    T = terrain(g)
    ns = noise_settings(g, T)
    g.w("%s/worldgen/noise_settings/%s.json" % (NS, tag), ns)
    if tag == "overworld":
        dt = _vanilla("dimension_type/overworld.json")
        dt["height"] = HEIGHT; dt["logical_height"] = HEIGHT; dt["min_y"] = MIN_Y
        dt.setdefault("attributes", {})["minecraft:visual/cloud_height"] = 500.0      # 用户 2026-11-26：云高 500
        g.w("minecraft/dimension_type/overworld.json", dt)
        g.w("minecraft/dimension/overworld.json", {"type": "minecraft:overworld", "generator": {
            "type": "minecraft:noise", "settings": "%s:%s" % (NS, tag), "biome_source": biome_source()}})
        biomes(g)
        features(g)
        import overworld_trees
        overworld_trees.write(g)
        p = os.path.join(data, NS, "function", "overworld", "border.mcfunction")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with io.open(p, "w", encoding="utf-8") as fh:
            fh.write("# 主世界的世界边界：大陆 10000×10000，外面留一圈海\n"
                     "execute in minecraft:overworld run worldborder center 0 0\n"
                     "execute in minecraft:overworld run worldborder set 12000\n")
    else:
        g.w("%s/dimension/%s.json" % (NS, tag), {"type": "minecraft:overworld", "generator": {
            "type": "minecraft:noise", "settings": "%s:%s" % (NS, tag), "biome_source": biome_source()}})
    return g.flush()


if __name__ == "__main__":
    import sys
    print(write(sys.argv[1]), "files")
