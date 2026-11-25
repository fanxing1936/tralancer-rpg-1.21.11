# -*- coding: utf-8 -*-
"""失乐园的地形：按离伊甸之门的距离分三区（用户 2026-11-25，说明与实测见 docs/TERRAIN-STUDY.md）。

    由 add_paradise.py 在 paradise_world.write 之后调用：paradise_terrain.write("../rpg")

只用原版 1.21.11 的节点。做法：
  * 坐标还原：三张尺度 1e-10 的噪声近似平面，解二元一次方程得 x、z，于是能按 r² 分区、给门与河庭留平地。
  * 泥沼（36 到 240）平泥滩与水洼；血泽（240 到 560）网状血河、湖与泥岗；灰烬边境（560 起）崎岖高山与盆地，维度高 384。
  * 材料三组：泥 + 沾泥红树根、砂土 + 红草方块、绯红菌岩 + 下界疣块；跟着地形走、不成片；山脊由深灰到白，灰烬低洼是石头、圆石、安山岩。
  * 黑石堡垒只在盆地中心。
噪声的分布先在 1.21.11 里量过（paradise_ref/quant.json），样条节点按分位数放；设计量在 paradise_ref/design.json。
坡度与逐层侵蚀的思路来自 Epic Terrain（MIT，Copyright (c) 2025 wonderfulaichen），代码与数值自写。
"""
import copy
import io
import json
import os
import shutil

REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paradise_ref")
D5 = json.load(io.open(os.path.join(REF, "design.json"), encoding="utf-8"))
QJ = json.load(io.open(os.path.join(REF, "quant.json"), encoding="utf-8"))
HEIGHT = D5["height"]
EPS = 1e-10                              # 坐标还原用的噪声尺度
UNIT = 1000.0                           # 还原出来的坐标以 1000 格为 1
CLOUD = 300.0                           # 云在绝大多数山顶之上（用户 2026-11-25）
D = None


def w(rel, obj):
    p = os.path.join(D, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def rd(rel):
    return json.load(io.open(os.path.join(D, rel), encoding="utf-8"))


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
def noise(n, xz, y=0.0): return {"type": "minecraft:noise", "noise": n, "xz_scale": xz, "y_scale": y}
def at(n, dx, dz):      # 在原点附近的固定一点取样：常数
    return {"type": "minecraft:shifted_noise", "noise": n, "xz_scale": 0.0, "y_scale": 0.0,
            "shift_x": dx, "shift_y": 0.0, "shift_z": dz}
def clamp(a, lo, hi): return {"type": "minecraft:clamp", "input": a, "min": lo, "max": hi}
def spline(coord, pts):
    """pts: (位置, 值[, 斜率])；缺省斜率 0（平台之间平滑过渡）。"""
    return {"type": "minecraft:spline", "spline": {"coordinate": coord, "points": [
        {"location": float(p[0]), "value": float(p[1]), "derivative": float(p[2] if len(p) > 2 else 0.0)} for p in pts]}}
def lin(coord, pts):
    """折线：每一点的斜率取两侧斜率的平均，端点为 0。"""
    out = []
    for i, (x, v) in enumerate(pts):
        if 0 < i < len(pts) - 1:
            s = (pts[i + 1][1] - pts[i - 1][1]) / (pts[i + 1][0] - pts[i - 1][0])
        else:
            s = 0.0
        out.append((x, v, s))
    return spline(coord, out)
def fc(a): return un("flat_cache", a)


NDF = "rpg:paradise_lost/"
def df(name, obj):
    w("rpg/worldgen/density_function/paradise_lost/%s.json" % name, obj)
    return NDF + name


def wnoise(name, first, amps):
    w("rpg/worldgen/noise/paradise_lost/%s.json" % name, {"firstOctave": first, "amplitudes": amps})
    return NDF + name


# ------------------------------------------------------------------ 坐标还原
def coords():
    """独立噪声在原点附近线性化，解二元一次方程得 x、z（单位 1000 格）。
    三张噪声 A、B、C：A-B 的行列式太小（|det|<0.1）时改用 A-C，避免误差被放大。"""
    names = [wnoise("coord_" + c, 0, [1.0]) for c in "abc"]
    h = EPS * UNIT
    K = 1e5                                   # 常数上限 1e6，所以 1/h 拆成两次相乘
    K2 = 1.0 / h / K
    vals = []
    for n in names:
        o = at(n, 0.0, 0.0)
        vals.append((df(n.split("/")[1] + "_v", fc(mul(K2, mul(K, sub(noise(n, EPS), o))))),
                     df(n.split("/")[1] + "_x", fc(mul(K2, mul(K, sub(at(n, h, 0.0), o))))),
                     df(n.split("/")[1] + "_z", fc(mul(K2, mul(K, sub(at(n, 0.0, h), o)))))))
    def solve(p, r):
        (a, a1, a2), (b, b1, b2) = p, r
        det = sub(mul(a1, b2), mul(a2, b1))
        inv = un("invert", det)
        return (det, mul(sub(mul(b2, a), mul(a2, b)), inv), mul(sub(mul(a1, b), mul(b1, a)), inv))
    d_ab, x_ab, z_ab = solve(vals[0], vals[1])
    d_ac, x_ac, z_ac = solve(vals[0], vals[2])
    det = df("det_ab", fc(un("abs", d_ab)))
    pick = lambda p, q: {"type": "minecraft:range_choice", "input": det, "min_inclusive": 0.1, "max_exclusive": 1000.0, "when_in_range": p, "when_out_of_range": q}
    x = df("x", fc(clamp(pick(x_ab, x_ac), -40000.0, 40000.0)))
    z = df("z", fc(clamp(pick(z_ab, z_ac), -40000.0, 40000.0)))
    return x, z


def build():
    x, z = coords()
    warp = wnoise("warp", -6, [1.0, 0.5])          # 分区边界的摆动
    rr = df("r2", fc(add(un("square", x), un("square", z))))                # (r/1000)^2
    # 边界摆动：只在门区之外起作用；r^2 的相对扰动约 ±12%（半径约 ±6%）
    rw = df("r2w", fc(mul(rr, add(1.0, mul(0.14, noise(warp, 1.0))))))
    # 离最近一座河庭中心的距离平方
    ax, az = un("abs", x), un("abs", z)
    c = 0.12
    cd = df("court2", fc({"type": "minecraft:min",
                           "argument1": add(un("square", add(-c, ax)), un("square", z)),
                           "argument2": add(un("square", x), un("square", add(-c, az)))}))

    q = lambda r: (r / UNIT) ** 2
    # 平地遮罩：0 = 完全压平，1 = 地形自由起伏
    open_gate = spline(rr, [(q(44), 0.0), (q(78), 1.0)])
    open_court = spline(cd, [(q(50), 0.0), (q(74), 1.0)])
    free = df("free", fc(mul(open_gate, open_court)))
    # 各区权重（按半径）
    z1 = spline(rw, [(q(195), 1.0), (q(285), 0.0)])
    z2 = spline(rw, [(q(195), 0.0), (q(285), 1.0), (q(490), 1.0), (q(640), 0.0)])
    z3 = spline(rw, [(q(490), 0.0), (q(640), 1.0)])
    z1, z2, z3 = df("w1", fc(z1)), df("w2", fc(z2)), df("w3", fc(z3))

    # ---- 地貌用的噪声（自己的，避免与原版各层相关）
    n_roll = wnoise("roll", -5, [1.0, 1.0, 0.5])      # 小起伏
    n_chan = wnoise("channel", -7, [1.0, 0.6, 0.25])  # 血泽的河道（取绝对值）
    n_lake = wnoise("lake", -7, [1.0, 0.4])
    n_mound = wnoise("mound", -5, [1.0, 0.8])

    B = 1 / 32.0                                       # 一格的高度
    roll = mul(noise(n_roll, 1.0), 1.0)
    # 2 血泽：网状河道 + 湖 + 散落的泥岗；y 69～92
    chan = lin(un("abs", noise(n_chan, 1.0)), [(0.0, -9 * B), (0.04, -8 * B), (0.09, -3.4 * B), (0.15, 0.6 * B), (0.5, 2.6 * B)])
    lake = lin(noise(n_lake, 1.0), [(-0.75, -9 * B), (-0.45, -5 * B), (-0.25, 0.0), (0.3, 0.8 * B)])
    mound = lin(noise(n_mound, 1.0), [(0.18, 0.0), (0.42, 3 * B), (0.62, 10 * B), (0.8, 12 * B)])
    h2 = df("h_marsh", fc(add(chan, lake, mound, mul(1.4 * B, roll))))
    flat = 2.4 * B                                     # 压平处地表 y=82
    # 群系坐标：按半径分段的常数
    n_dith = wnoise("dither", -4, [1.0, 0.8, 0.4])
    zc = df("zone_r", fc(mul(rw, add(1.0, mul(0.11, noise(n_dith, 1.0))))))
    zone = df("zone", fc(spline(zc, [(q(236), -1.0), (q(244), 0.0), (q(555), 0.0), (q(567), 1.0)])))
    build_g(dict(locals()))


# 名: (首倍频, 幅值, xz_scale, 扭曲, 分位数取自哪张已测噪声(同幅值), 用途)
N5 = {
    "bog":    (-6, [1.0, 0.6, 0.36], 1.14, None, "bog"),
    "roll":   (-5, [1.0, 0.6], 1.33, None, "roll"),
    "fine":   (-4, [1.0, 0.6], 1.33, None, "roll"),
    "isle":   (-5, [1.0, 0.6, 0.36], 1.4, None, "mound"),
    "basin":  (-9, [1.0, 0.3], 0.9, None, "lake"),
    "valley": (-8, [1.0, 0.6, 0.3], 0.85, "wxz", "fault"),
    "prov":   (-8, [1.0, 0.55, 0.3], 1.0, None, "prov"),
    "crest":  (-8, [1.0, 0.6, 0.36], 1.1, "wxz", "crest"),
    "crest2": (-7, [1.0, 0.6, 0.36], 1.2, "wzx", "crest"),
    "spire":  (-6, [1.0, 0.6], 0.9, None, "roll"),
    "foot":   (-6, [1.0, 0.6, 0.36], 1.15, None, "foot"),
    "rough":  (-5, [1.0, 0.6, 0.36], 1.07, None, "rough"),
    "pass":   (-7, [1.0, 0.5], 0.7, None, "lake"),
}
ER = ((-7, 1.28, 8.0, 0.18), (-5, 0.8, 5.0, 0.30), (-4, 1.0, 3.0, 0.40))
WARP, EK2 = D5["warp"], 3.0


def wl(n):
    return 2 ** -N5[n][0] / N5[n][2]


def wn(n): return wnoise("g_" + n, N5[n][0], N5[n][1])


def smp(n):
    f, a, xz, warp, _ = N5[n]
    if not warp: return noise(wn(n), xz)
    wx, wz = noise(wnoise("g_wx", -8, [1.0, 0.5]), 1.0), noise(wnoise("g_wz", -8, [1.0, 0.5]), 1.0)
    a1, a2 = (wx, wz) if warp == "wxz" else (wz, wx)
    return {"type": "minecraft:shifted_noise", "noise": wn(n), "xz_scale": xz, "y_scale": 0.0,
            "shift_x": mul(WARP * xz, a1), "shift_y": 0.0, "shift_z": mul(WARP * xz, a2)}


def qt(n, p):
    key = N5[n][4] if n in N5 else n
    xs, ys = QJ[key]["p"], QJ[key]["v"]
    for i in range(len(xs) - 1):
        if xs[i] <= p <= xs[i + 1]: return ys[i] + (ys[i + 1] - ys[i]) * (p - xs[i]) / (xs[i + 1] - xs[i])
    return ys[-1]


def qt_abs(n, p):           # 用 abs_crest / abs_fault
    key = "abs_" + N5[n][4]
    xs, ys = QJ[key]["p"], QJ[key]["v"]
    for i in range(len(xs) - 1):
        if xs[i] <= p <= xs[i + 1]: return ys[i] + (ys[i + 1] - ys[i]) * (p - xs[i]) / (xs[i + 1] - xs[i])
    return ys[-1]


def qs(coord, n, pts, k=1.0, ab=False):
    ss, last = [], -9e9
    for p, v in pts:
        x = (qt_abs if ab else qt)(n, p)
        if x <= last: x = last + 1e-4
        ss.append((x, v * k)); last = x
    return lin(coord, ss)


def build_g(L):
    z1, z2, z3, free, flat, rw, q, B = (L[k] for k in ("z1", "z2", "z3", "free", "flat", "rw", "q", "B"))
    F = {n: df("g_" + n, fc(smp(n))) for n in N5 if n != "rough"}
    # ---- 侵蚀 m
    e, m = 1.0, None
    for k, (first, xz, st, c) in enumerate(ER):
        nm = wnoise("g_er%d" % k, first, [1.0, 0.5])
        def sh(ax, az): return {"type": "minecraft:shifted_noise", "noise": nm, "xz_scale": xz, "y_scale": 0.0, "shift_x": ax * xz, "shift_y": 0.0, "shift_z": az * xz} if (ax or az) else noise(nm, xz)
        vv = df("g_er%d_v" % k, fc(sh(0, 0)))
        ab = lambda ax, az: un("abs", sub(sh(ax, az), vv))
        t = st * 0.7071
        g = mul(0.5, add({"type": "minecraft:min", "argument1": ab(st, 0), "argument2": ab(0, st)}, {"type": "minecraft:min", "argument1": ab(t, t), "argument2": ab(t, -t)}))
        e = df("g_er%d_e" % k, fc(mul(add(c, un("square", vv), mul(EK2, fc(g))), e)))
        m = e if m is None else add(m, e)
    m = df("g_er_m", fc(m))
    H = D5["h"]
    # ---- 泥沼、血泽：沿用第一版，加细部与岛
    det = add(mul(H["roll"] * B / QJ["roll"]["sd"], F["roll"]), mul(H["fine"] * B / QJ["roll"]["sd"], F["fine"]))
    h1 = df("g_h1", fc(add(qs(F["bog"], "bog", D5["bog"], B), det)))
    isl = df("g_isl", fc(qs(F["isle"], "isle", D5["isle"], B)))
    h2b = L["h2"]
    lowmask = spline(h2b, [(-5.5 * B, 1.0), (-3.0 * B, 0.55), (-1.5 * B, 0.0)])     # 只在水里长岛
    h2 = df("g_h2", fc(add(h2b, mul(isl, lowmask), det)))
    # ---- 灰烬：山地
    mb = df("g_mb", fc(spline(F["basin"], [(qt("basin", D5["basin"][0]), 1.0), (qt("basin", D5["basin"][1]), 0.0)])))
    inner = df("g_inner", fc(spline(rw, [(q(D5["inner"][0]), 0.0), (q(D5["inner"][1]), 1.0)])))
    mb = df("g_mb2", fc(add(1.0, mul(inner, add(-1.0, mb)))))
    wall = df("g_wall", fc(spline(rw, [(q(D5["wall"][0]), 0.0), (q(D5["wall"][1]), 1.0)])))
    vf = df("g_vf", fc(qs(un("abs", F["valley"]), "valley", D5["valley"], 1.0, True)))
    prov01 = df("g_prov01", fc(qs(F["prov"], "prov", [[8, 0.0], [92, 1.0]])))
    ridge = df("g_ridge", fc(qs(un("abs", F["crest"]), "crest", D5["ridge"], 1.0, True)))
    branch = df("g_branch", fc(qs(un("abs", F["crest2"]), "crest2", D5["branch"], 1.0, True)))
    gully = qs(m, "er_m", D5["gully"])
    sp = qs(F["spire"], "spire", D5["spire"])
    core = df("g_mtn", fc(add(H["mass0"], mul(H["mass1"], prov01), mul(H["ridge"], ridge, add(0.4, mul(0.6, prov01))),
                              mul(H["branch"], branch, add(0.3, mul(0.7, ridge))), mul(H["gully"], gully), mul(H["spire"], sp, add(0.2, mul(0.8, ridge))))))
    mw = df("g_mw", fc(mul(wall, mul(mb, vf))))
    hm = df("g_hm", fc(add(mul(mw, core), mul(H["foot"], qs(F["foot"], "foot", [[5, -1.0], [50, 0.0], [95, 1.0]]), add(0.5, mul(0.5, mw))))))     # 单位：格
    st = D5["terrace"]
    steps = []
    for k in range(0, 16):
        steps += [((k * st + 0.0), k * st, 0.15), ((k * st + 0.72 * st), k * st + 0.15 * st, 0.15)]
    terr = spline(hm, steps)
    th = df("g_th", fc(add(mul(D5["terrace_w"], terr), mul(1.0 - D5["terrace_w"], hm))))
    cut = spline(hm, [(10.0, 0.0), (26.0, 1.0)])               # 平地不做台阶
    hm2 = df("g_hm2", fc(add(mul(cut, th), mul(add(1.0, mul(-1.0, cut)), hm))))
    h3 = df("g_h3", fc(add(D5["base3"] * B, mul(B, hm2), mul(H["roll3"] * B / QJ["roll"]["sd"], F["roll"]))))
    z3m = z3
    mix = add(mul(z1, h1), mul(z2, h2), mul(z3m, h3))
    height = df("g_height", fc(clamp(add(mul(free, mix), mul(add(1.0, mul(-1.0, free)), flat)), -13 * B, 232 * B)))
    slope_gate = add(0.10, mul(0.9, mw))
    rough = {"type": "minecraft:range_choice", "input": z3, "min_inclusive": -1.0, "max_exclusive": 0.02, "when_in_range": 0.0,
             "when_out_of_range": mul(H["rough"] * B, z3, slope_gate, noise(wn("rough"), 1.07, 1.7))}
    gr = {"type": "minecraft:y_clamped_gradient", "from_y": 0, "to_y": HEIGHT, "from_value": 80.0 / 32, "to_value": -(HEIGHT - 80.0) / 32}
    final = un("interpolated", add(add(gr, height), rough))
    # ---- 群系：分区 × 山地/盆地/堡垒盆心
    eros = df("g_basin_zone", fc(add(-1.0, mul(inner, spline(F["basin"], [(qt("basin", D5["basin"][1] - 4), 0.0), (qt("basin", D5["basin"][1]), 1.0)])),
                                     mul(inner, spline(F["basin"], [(qt("basin", D5["core"][0]), 0.0), (qt("basin", D5["core"][1]), 1.0)]), spline(rw, [(q(D5["core_r"][0]), 0.0), (q(D5["core_r"][1]), 1.0)])))))
    ns = rd("rpg/worldgen/noise_settings/paradise_lost.json")
    ns["noise"]["height"] = HEIGHT
    ns["noise_router"]["final_density"] = final
    ns["noise_router"]["continents"] = L["zone"]
    ns["noise_router"]["erosion"] = eros
    ns["surface_rule"] = surface3()
    w("rpg/worldgen/noise_settings/paradise_lost.json", ns)
    dt = rd("rpg/dimension_type/paradise_lost.json"); dt["height"] = HEIGHT; dt["logical_height"] = HEIGHT
    dt["attributes"]["minecraft:visual/cloud_height"] = CLOUD
    w("rpg/dimension_type/paradise_lost.json", dt)
    def ee(b, c, er):
        p = {k: 0.0 for k in ("temperature", "humidity", "depth", "weirdness", "offset")}
        p["continentalness"] = c; p["erosion"] = er
        return {"biome": b, "parameters": p}
    w("rpg/dimension/paradise_lost.json", {"type": "rpg:paradise_lost", "generator": {"type": "minecraft:noise", "settings": "rpg:paradise_lost",
        "biome_source": {"type": "minecraft:multi_noise", "biomes": [
            ee("rpg:paradise/bog", -1.0, [-1.0, 1.0]), ee("rpg:paradise/marsh", 0.0, [-1.0, 1.0]),
            ee("rpg:paradise/mountain", 1.0, -1.0), ee("rpg:paradise/basin", 1.0, 0.0), ee("rpg:paradise/core", 1.0, 1.0)]}}})
    biomes()
    fortress()


# ------------------------------------------------------------------ 地表
def surface3():
    M = D5["mat"]
    def block(n, **p):
        d = {"Name": "minecraft:" + n}
        if p: d["Properties"] = p
        return {"type": "minecraft:block", "result_state": d}
    def cond(c, t): return {"type": "minecraft:condition", "if_true": c, "then_run": t}
    def seq(*s): return {"type": "minecraft:sequence", "sequence": list(s)}
    def no(c): return {"type": "minecraft:not", "invert": c}
    def nt(n, lo, hi): return {"type": "minecraft:noise_threshold", "noise": NDF + n, "min_threshold": lo, "max_threshold": hi}
    def bio(*b): return {"type": "minecraft:biome", "biome_is": ["rpg:" + x for x in b]}
    def depth(add_sd, sec, off=0): return {"type": "minecraft:stone_depth", "offset": off, "add_surface_depth": add_sd, "secondary_depth_range": sec, "surface_type": "floor"}
    def yab(y, m=0): return {"type": "minecraft:y_above", "anchor": {"absolute": y}, "surface_depth_multiplier": m, "add_stone_depth": False}
    def rnd(p, name):          # 逐格随机：垂直渐变取很宽的范围，概率近似常数 p
        b = int(80 + 2112 * p / (1 - p))
        return {"type": "minecraft:vertical_gradient", "random_name": "rpg:" + name, "true_at_and_below": {"absolute": -2032}, "false_at_and_above": {"absolute": min(b, 2031)}}
    above_water = {"type": "minecraft:water", "offset": 0, "surface_depth_multiplier": 0, "add_stone_depth": False}
    steep = {"type": "minecraft:steep"}
    mud, roots, coarse = block("mud"), block("muddy_mangrove_roots", axis="y"), block("coarse_dirt")
    grass, nyl, wart = block("grass_block", snowy="false"), block("crimson_nylium"), block("nether_wart_block")
    tuff, black = block("tuff"), block("blackstone")
    wnoise("g_sa", -3, [0.8, 1.0]); wnoise("g_sb", -3, [0.6, 1.0]); wnoise("g_sd", -3, [1.0, 0.8]); wnoise("g_se", -3, [0.8, 1.0]); wnoise("g_sm", -5, [1.0, 0.5])
    sA, sB, sD, sE, sM = "g_sa", "g_sb", "g_sd", "g_se", "g_sm"
    wnoise("g_sc", -2, [1.0]); sC = "g_sc"
    xor = seq(cond(nt(sC, 0.0, 9.0), seq(cond(nt(sB, 0.0, 9.0), roots), mud)), seq(cond(nt(sB, 0.0, 9.0), mud), roots))
    g1 = seq(cond(rnd(0.02, "pl_j1"), roots), xor)
    g2 = seq(cond(nt(sD, M["grassD"], 9.0), cond(above_water, grass)), coarse)
    def mix(zone):
        """三组：短波 sA 决定组（中段 = 主体），中波 sM 只改变比例。组内再用 sB / sD / sA 的核心决定方块。"""
        z = M[zone]
        def level(t3, t2):
            g3 = seq(cond(nt(sA, t3 + M["core"], 9.0), wart), nyl)
            return seq(cond(nt(sA, t3, 9.0), g3), cond(nt(sE, t2, 9.0), g2), g1)
        return seq(cond(nt(sM, 0.16, 9.0), level(*z[0])), cond(nt(sM, -0.16, 0.16), level(*z[1])), level(*z[2]))
    def bands(zone):
        """水边色带：先按地表 y（带短波扰动）给窄带，再按 sM 断续。"""
        e = M["band_keep"]
        g3 = seq(cond(nt(sA, M["band_wart"], 9.0), wart), nyl)
        return seq(
            cond(nt(sM, -9.0, e),
                 seq(cond(no(yab(79)), g3),
                     cond(nt(sD, 0.05, 9.0), cond(no(yab(80)), g3)),
                     cond(nt(sE, -9.0, 0.15), cond(no(yab(81)), g2)),
                     cond(nt(sD, -9.0, -0.2), cond(no(yab(82)), g2)))),
            mix(zone))
    under_water = seq(cond(nt(sA, 0.42, 9.0), wart), cond(nt(sB, M["rootB"], 9.0), roots), mud)
    def ground(zone, near_water):
        b = bands(zone) if near_water else mix(zone)
        return seq(cond(no(above_water), under_water), b)
    # 陡面：另一种组合，斑驳；石骨只少量
    cliff = seq(cond(nt(sA, M["cliff_wart"], 9.0), wart), cond(nt(sD, M["cliff_black"], 9.0), black), cond(nt(sE, M["cliff_tuff"], 9.0), tuff),
                cond(nt(sB, 0.05, 9.0), coarse), cond(nt(sB, -9.0, -0.28), nyl), cond(nt(sD, -0.1, 9.0), roots), mud)
    # 山尖与山脊：深灰 → 白（用户 2026-11-25）。每级两到三种石头用短波互掺，级与级的边界按 sE / sD 错开
    st = {n: block(n) for n in ("deepslate", "tuff", "blackstone", "stone", "andesite", "diorite", "calcite", "cobblestone", "cobbled_deepslate", "polished_andesite", "polished_diorite")}
    st["deepslate"] = block("deepslate", axis="y")
    # 地表规则只有 2D 噪声，直接用会在崖壁上拉出竖条；所以每约 9 格换一组噪声，层与层之间逐格抖动过渡
    PV = []
    for k in range(4):
        wnoise("g_pa%d" % k, -3, [1.0, 1.0, 0.6])
        wnoise("g_pb%d" % k, -3, [0.6, 1.0, 1.0])
        PV.append(("g_pa%d" % k, "g_pb%d" % k))

    def above(y0, half, name):
        return no({"type": "minecraft:vertical_gradient", "random_name": "rpg:" + name, "true_at_and_below": {"absolute": y0 - half}, "false_at_and_above": {"absolute": y0 + half}})

    def pair(k, a, b, c, t):
        na, nb = PV[k % 4]
        return seq(cond(nt(na, 0.34, 9.0), st[c]), cond(nt(nb, t, 9.0), st[a]), st[b])

    KIND = [("deepslate", "cobbled_deepslate", "tuff", 0.05), ("stone", "cobbled_deepslate", "andesite", 0.0), ("andesite", "stone", "diorite", 0.0),
            ("diorite", "andesite", "calcite", -0.05), ("calcite", "diorite", "polished_diorite", 0.05)]

    def ladder(shift):
        """从高到低：每级里再按 9 格切片。"""
        ys = [y + shift for y in M["peak"]] + [HEIGHT - 50]
        out = []
        for lv in range(4, -1, -1):
            cuts = list(range(ys[lv], ys[lv + 1], 9))
            inner = [cond(above(y, 3, "pl_s%d" % (y % 97)), pair(y // 9, *KIND[lv])) for y in reversed(cuts[1:])] + [pair(ys[lv] // 9, *KIND[lv])]
            out.append(cond(above(ys[lv], 8, "pl_l%d" % lv), seq(*inner)))
        return seq(*out)
    peaks = seq(cond(nt(sM, 0.0, 9.0), ladder(-6)), ladder(6))
    cobble, stone_, ande, gravel = block("cobblestone"), block("stone"), block("andesite"), block("gravel")
    R = M["rock"]
    rock = seq(cond(nt(sA, R["wart"], 9.0), seq(cond(nt(sA, R["wart"] + 0.16, 9.0), wart), nyl)),        # 绯红点缀
               cond(nt(sE, R["dirt"], 9.0), g2),                                                        # 砂土 + 草
               cond(nt(sE, -9.0, -R["mud"]), seq(cond(nt(sB, 0.0, 9.0), roots), mud)),                 # 泥
               cond(nt(sB, R["cob"], 9.0), seq(cond(nt(sD, 0.30, 9.0), st["tuff"]), cobble)),
               cond(nt(sB, -9.0, -R["and"]), seq(cond(nt(sD, 0.34, 9.0), gravel), ande)),
               cond(nt(sD, -9.0, -0.34), st["tuff"]), cond(nt(sC, 0.28, 9.0), cobble), cond(nt(sC, -9.0, -0.28), ande), stone_)
    tops = seq(
        cond(bio("paradise/mountain"), cond(yab(M["peak"][0] - 16), peaks)),
        cond(bio("paradise/marsh"), ground("marsh", True)),
        cond(bio("paradise/mountain"), seq(cond(steep, cliff), cond(no(yab(M["rock_top"])), rock), ground("mountain", False))),
        cond(bio("paradise/basin", "paradise/core"), seq(cond(steep, cliff), cond(no(above_water), under_water),
             cond(nt(sM, -9.0, M["band_keep"] - 0.15), cond(no(yab(80)), seq(cond(nt(sA, M["band_wart"], 9.0), wart), nyl))),     # 盆地里血池的窄沿仍在
             rock)),
        ground("bog", True))
    under = seq(cond(bio("paradise/mountain"), cond(yab(M["peak"][0] - 16), peaks)), cond(bio("paradise/mountain", "paradise/basin", "paradise/core"), cond(steep, cliff)),
                cond(bio("paradise/mountain", "paradise/basin", "paradise/core"), seq(cond(nt(sB, 0.1, 9.0), cobble), cond(nt(sD, 0.2, 9.0), ande), stone_)),
                cond(nt(sB, 0.1, 9.0), roots), mud)
    body_rule = cond(yab(80), cond(bio("paradise/mountain", "paradise/basin", "paradise/core"), seq(
        cond(yab(M["peak"][0] - 16), peaks),
        cond(nt(sA, 0.30, 9.0), wart), cond(nt(sD, 0.30, 9.0), black), cond(nt(sE, 0.22, 9.0), tuff), cond(nt(sB, 0.12, 9.0), coarse),
        cond(nt(sB, -9.0, -0.35), nyl), cond(nt(sD, -0.25, 9.0), roots), mud)))
    old = rd("rpg/worldgen/noise_settings/paradise_lost.json")["surface_rule"]["sequence"]
    return seq(old[0], cond(depth(True, 6), seq(cond(depth(False, 0), tops), under)), body_rule)


# ------------------------------------------------------------------ 群系与植被
def biomes():
    base = rd("rpg/worldgen/biome/paradise_lost.json")
    V = D5["veg"]
    feats, placed = {}, {}
    def simple(name, states):
        prov = {"type": "minecraft:weighted_state_provider", "entries": [{"data": {"Name": "minecraft:" + s, **({"Properties": p} if p else {})}, "weight": k} for s, p, k in states]}
        return {"type": "minecraft:simple_block", "config": {"to_place": prov}}
    AIR = {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"}
    def on(*blocks): return {"type": "minecraft:matching_blocks", "offset": [0, -1, 0], "blocks": ["minecraft:" + b for b in blocks]}
    def surv(b, props=None): return {"type": "minecraft:would_survive", "state": {"Name": "minecraft:" + b, **({"Properties": props} if props else {})}}
    def patch(name, feat, tries, spread, pred):
        feats[name] = {"type": "minecraft:random_patch", "config": {"tries": tries, "xz_spread": spread, "y_spread": 2,
            "feature": {"feature": feat, "placement": [{"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:all_of", "predicates": [AIR] + pred}}]}}}
    g2 = on("coarse_dirt", "grass_block")
    g3 = on("crimson_nylium", "nether_wart_block")
    g1 = on("mud", "muddy_mangrove_roots")
    patch("grass", simple("g", [("short_grass", None, 3), ("fern", None, 2)]), 10, 3, [g2, surv("short_grass")])
    patch("grass_sparse", simple("g", [("short_grass", None, 3), ("fern", None, 1)]), 4, 4, [g1, surv("short_grass")])
    patch("tall", {"type": "minecraft:simple_block", "config": {"to_place": {"type": "minecraft:weighted_state_provider", "entries": [
        {"data": {"Name": "minecraft:tall_grass", "Properties": {"half": "lower"}}, "weight": 1}, {"data": {"Name": "minecraft:large_fern", "Properties": {"half": "lower"}}, "weight": 1}]}}}, 10, 4, [g2, surv("tall_grass", {"half": "lower"})])
    patch("crimson", simple("c", [("crimson_roots", None, 3), ("crimson_fungus", None, 1)]), 8, 3, [g3, surv("crimson_roots")])
    patch("dead", simple("d", [("dead_bush", None, 1)]), 2, 3, [g2, surv("dead_bush")])
    patch("roots_hang", simple("r", [("hanging_roots", None, 1)]), 1, 2, [surv("hanging_roots")])
    feats["spring"] = {"type": "minecraft:spring_feature", "config": {"state": {"Name": "minecraft:water", "Properties": {"falling": "true"}}, "requires_block_below": False, "rock_count": 4, "hole_count": 1,
                       "valid_blocks": ["minecraft:mud", "minecraft:muddy_mangrove_roots", "minecraft:coarse_dirt", "minecraft:crimson_nylium", "minecraft:nether_wart_block", "minecraft:tuff", "minecraft:blackstone"]}}
    def ore(size, b, targets):
        return {"type": "minecraft:ore", "config": {"size": size, "discard_chance_on_air_exposure": 0.0, "targets": [{"target": {"predicate_type": "minecraft:block_match", "block": "minecraft:" + t}, "state": {"Name": "minecraft:" + b, **({"Properties": {"axis": "y"}} if b == "muddy_mangrove_roots" else {})}} for t in targets]}}
    feats["blob_coarse"] = ore(10, "coarse_dirt", ["mud", "tuff", "blackstone", "muddy_mangrove_roots"])
    feats["blob_mud"] = ore(10, "mud", ["coarse_dirt", "tuff", "nether_wart_block", "muddy_mangrove_roots"])
    feats["blob_wart"] = ore(8, "nether_wart_block", ["mud", "coarse_dirt", "muddy_mangrove_roots", "tuff"])
    feats["blob_tuff"] = ore(9, "tuff", ["mud", "coarse_dirt", "muddy_mangrove_roots"])
    feats["blob_andesite"] = ore(22, "andesite", ["stone", "tuff", "diorite", "deepslate"])
    feats["blob_diorite"] = ore(22, "diorite", ["andesite", "stone", "calcite"])
    feats["blob_deep"] = ore(22, "deepslate", ["stone", "tuff", "andesite"])
    for k, v in feats.items(): w("rpg/worldgen/configured_feature/paradise/%s.json" % k, v)
    SQ, HM, BI = {"type": "minecraft:in_square"}, {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}
    def rate(c, ch=1):
        if isinstance(c, list): return [{"type": "minecraft:noise_threshold_count", "noise_level": 0.0, "below_noise": c[0], "above_noise": c[1]}]
        return [{"type": "minecraft:rarity_filter", "chance": ch}] if ch > 1 else ([{"type": "minecraft:count", "count": c}])
    def pl(name, feature, c, ch=1, hm=True):
        w("rpg/worldgen/placed_feature/paradise/%s.json" % name, {"feature": "rpg:paradise/" + feature, "placement": rate(c, ch) + [SQ] + ([HM] if hm else []) + [BI]})
        return "rpg:paradise/" + name
    def blob(name, feature, c, lo, hi):
        w("rpg/worldgen/placed_feature/paradise/%s.json" % name, {"feature": "rpg:paradise/" + feature, "placement": [{"type": "minecraft:count", "count": c}, SQ,
            {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform", "min_inclusive": {"absolute": lo}, "max_inclusive": {"absolute": hi}}}, BI]})
        return "rpg:paradise/" + name
    w("rpg/worldgen/placed_feature/paradise/spring.json", {"feature": "rpg:paradise/spring", "placement": [{"type": "minecraft:count", "count": V["spring_tries"]}, SQ,
        {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform", "min_inclusive": {"absolute": 82}, "max_inclusive": {"absolute": 110}}}, BI]})
    zones = {"paradise/bog": "bog", "paradise/marsh": "marsh", "paradise/mountain": "mountain", "paradise/basin": "basin", "paradise/core": "basin"}
    for b, z in zones.items():
        o = copy.deepcopy(base)
        v = V[z]
        o["effects"].update({"grass_color": D5["tint"]["grass"], "foliage_color": D5["tint"]["foliage"]})
        o["features"] = [list(x) for x in o["features"]]
        while len(o["features"]) < 11: o["features"].append([])
        if z in ("mountain",):
            o["features"] = [[f for f in st if "blood_puddle" not in f] for st in o["features"]]
        o["features"][9] = [f for f in o["features"][9] if not any(k in f for k in ("dry_grass", "dead_bush"))]
        n = z
        add9 = [pl("%s_grass" % n, "grass", v["grass"]), pl("%s_grass1" % n, "grass_sparse", v["sparse"]), pl("%s_tall" % n, "tall", v["tall"]),
                pl("%s_crimson" % n, "crimson", v["crimson"]), pl("%s_dead" % n, "dead", 1, v["dead_chance"])]
        o["features"][9] += add9
        if z in ("marsh", "basin", "bog"): o["features"][8] = o["features"][8] + ["rpg:paradise/spring"]
        if z in ("mountain", "basin"):
            o["features"][6] = o["features"][6] + [blob("%s_b1" % n, "blob_coarse", v["blob"], 78, 140), blob("%s_b2" % n, "blob_mud", v["blob"], 78, 140),
                                                    blob("%s_b3" % n, "blob_wart", v["blob"] // 2 + 1, 78, 140), blob("%s_b4" % n, "blob_tuff", v["blob"] // 2 + 1, 78, 140)]
        if z == "mountain":
            o["features"][6] += [blob("%s_s1" % n, "blob_andesite", v["blob"] * 3, 130, 300), blob("%s_s2" % n, "blob_diorite", v["blob"] * 3, 150, 320), blob("%s_s3" % n, "blob_deep", v["blob"] * 2, 112, 200)]
        w("rpg/worldgen/biome/paradise/%s.json" % b.split("/")[1], o)


def fortress():
    """堡垒只在盆地中心；露天骸骨的起点抬到山顶以上，从上往下找第一处地面。"""
    f = D5["fort"]
    w("rpg/tags/worldgen/biome/paradise_fortress.json", {"values": ["rpg:paradise/core"]})
    w("rpg/tags/worldgen/biome/in_paradise.json", {"values": ["rpg:paradise/" + k for k in ("bog", "marsh", "mountain", "basin", "core")]})
    p = "rpg/worldgen/structure/paradise/fortress.json"
    if os.path.exists(os.path.join(D, p)):
        o = rd(p)
        o["biomes"] = "#rpg:paradise_fortress"
        w(p, o)
    p = "rpg/worldgen/structure/paradise_lost/remains.json"
    o = rd(p)
    o["biomes"] = "#rpg:in_paradise"
    o["height"].update({"min_inclusive": {"absolute": f["remains"][0]}, "max_inclusive": {"absolute": f["remains"][1]}})
    w(p, o)


def write(rpg):
    global D
    D = os.path.join(rpg, "data")
    for k in ("density_function/paradise_lost", "noise/paradise_lost", "biome/paradise", "configured_feature/paradise", "placed_feature/paradise"):
        shutil.rmtree(os.path.join(D, "rpg", "worldgen", *k.split("/")), ignore_errors=True)
    build()
    # 血洼、焦痕这些老地物也认新材料
    t = rd("rpg/tags/block/paradise_lost_ground.json")
    for b in ("coarse_dirt", "grass_block", "crimson_nylium", "nether_wart_block"):
        if "minecraft:" + b not in t["values"]:
            t["values"].append("minecraft:" + b)
    w("rpg/tags/block/paradise_lost_ground.json", t)
    n = 0
    for k in ("density_function/paradise_lost", "noise/paradise_lost", "biome/paradise", "configured_feature/paradise", "placed_feature/paradise"):
        n += len(os.listdir(os.path.join(D, "rpg", "worldgen", *k.split("/"))))
    return n
