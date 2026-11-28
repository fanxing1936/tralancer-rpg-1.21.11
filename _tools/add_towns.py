# -*- coding: utf-8 -*-
"""城镇：选址、建造、故乡出生、安全区、进镇标题（《开局参与感》策划书第二节，用户 2026-11-27「可以开始开工了」）。

建筑只用用户给的文件（town_ref/SOURCES.md），由 town_build.py 转成 town_ref/struct/*.nbt；这里把它们拼成二十座城镇。
- 主世界地形随世界种子变，所以不预先定坐标：每座镇有一个名义位置（十个国家各占一个扇区，内外两圈），
  第一次需要它时（有人以它为故乡，或有人走近）才在名义位置附近找一块平地，forceload 后建起来。
- 选址（用户 2026-11-28：「预留出完全平坦的地方，小镇只在完全平坦的地方生成，无任何地表覆盖层」）：
  在名义位置附近找一块危险 I–II 群系里的缓地（5×5 取样高差 ≤ 10，不在水上），把 224×224 的「町地」整块削平、填实，
  地皮统一（草；雪原换雪、沙漠换沙），不留任何覆盖层；外圈 12 格 1:1 缓坡接回地形。找不到就不建，不退回到坡地。
- 建造不破坏地表：每栋建筑按自己脚下的最高点放（低处用地基裙边垫到地形，只替换空气、水和花草），
  结构里只有建筑本身和室内空气；脚下和顶上的树、草先清掉（植被可以破坏）。
- 土径：只换地表那一层（不是建筑方块），从各栋门口连到天使像，再引三条小路出镇，越远越窄、越断续。
- 进镇标题、镇内不刷敌对怪（副本进行时例外）、故乡复活点。

python add_towns.py ../rpg
"""
import heapq
import io
import json
import math
import os
import random
import shutil
import sys

import rpg_ui_style as ui
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
HERE = os.path.dirname(os.path.abspath(__file__))
STRUCT = os.path.join(HERE, "town_ref", "struct")
FUNC = os.path.join(DP, "data", "rpg", "function")
P = "rpg:town"
O = "rpg_tw"
OW = "execute in minecraft:overworld "
COUNT = [0]
GAP = 8
CENTER_CLEAR = 16   # 房子离天使像至少这么远：中间是土径广场
NATIONS = ["犹大王国", "以色列北国", "以东公国", "摩押王国", "亚扪联邦", "非利士五城同盟", "亚兰帝国", "推罗海商共和国", "基列边境领", "圣城教廷领"]
# (国家序号, 内圈镇, 外圈镇)：圣经地名
NAMES = [("伯利恒", "Bethlehem", "希伯仑", "Hebron"), ("撒玛利亚", "Samaria", "示剑", "Shechem"), ("波斯拉", "Bozrah", "提幔", "Teman"),
         ("底本", "Dibon", "基珥", "Kir"), ("拉巴", "Rabbah", "雅谢", "Jazer"), ("迦特", "Gath", "亚实基伦", "Ashkelon"),
         ("哈马", "Hamath", "但城", "Dan"), ("西顿", "Sidon", "撒勒法", "Zarephath"), ("拉末", "Ramoth", "雅比", "Jabesh"),
         ("伯大尼", "Bethany", "以马忤斯", "Emmaus")]
KIND = {"wheat": "乡村", "fief": "小城", "ferry": "渡口"}
RING = (1800, 3400)
TYPES_A = ["wheat", "fief", "ferry", "wheat", "fief", "wheat", "ferry", "fief", "wheat", "fief"]
TYPES_B = ["fief", "ferry", "wheat", "ferry", "wheat", "fief", "wheat", "ferry", "fief", "wheat"]
LAYOUTS = {   # (建筑, 角色)：第一栋是镇中心
    "wheat": [("angel_statue", "center"), ("church_white", "church"), ("barn", "granary"), ("rustic_house", "farm"), ("folk_house", "house"),
              ("tutorial_house", "rent"), ("meadow_house", "elder"), ("green_house_big", "house"), ("green_house_medium", "house"),
              ("green_house_small", "house"), ("survival_2", "house"), ("survival_6", "house"), ("cottage_1000", "house")],
    "fief": [("angel_statue", "center"), ("church_glimmerhall", "church"), ("barn", "granary"), ("old_fiefdom", "keep"), ("medieval_street", "street"),
             ("cozy_manor", "priest"), ("serene_manor", "elder"), ("half_timbered", "house"), ("roadside_tavern", "tavern"), ("tutorial_house", "rent"),
             ("survival_9", "house"), ("green_house_small", "house")],
    "ferry": [("angel_statue", "center"), ("church_gothic", "church"), ("barn", "granary"), ("fisherman_house", "elder"), ("roadside_tavern", "tavern"),
              ("tutorial_house", "rent"), ("survival_1", "house"), ("survival_3", "house"), ("survival_5", "house"), ("survival_8", "house"),
              ("survival_10", "house"), ("survival_4", "house")],
}
RESERVED = {"plaza": (15, 15), "grave": (19, 13)}       # 刑台广场、墓地：只是空地，道具（地下城模型）摆在上面
ROT_OF = {"none": 0, "clockwise_90": 1, "180": 2, "counterclockwise_90": 3}
ROTS = ["none", "clockwise_90", "180", "counterclockwise_90"]
DIRS = ["north", "east", "south", "west"]                # 顺时针
STEP = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
WOODISH = ("planks", "_log", "_wood")
OFFS = [(0, 0)] + [(round(r * math.cos(2 * math.pi * k / n + r)), round(r * math.sin(2 * math.pi * k / n + r)))
                   for r, n in ((160, 6), (320, 10), (480, 14), (640, 18), (800, 22), (960, 26)) for k in range(n)]
PROBE = 48         # 候选点四周 forceload 的半宽（7×7 个区块；再大，这片 1024 格高的地形一次生成会吃光内存）
SPREAD = 8         # 候选点 80×80 内的高差上限
WIDE = 16          # 选中后整块町地（±96）的高差上限（削平与外圈缓坡兜得住）
EDGE = 12          # 町地外一圈 1:1 的缓坡
PAD = 112          # 町地半宽（整块 224×224；结构连同地形自适应不能超出中心 128 格）
CAMP_R = (185, 200, 215)   # 林中营地离镇中心（用户 2026-11-28：「林中祭坛要远离，离村庄 200 格左右」）
PAD_H = 40         # 町地上方清空的高度
LIM = PAD + 6      # 不规则町地的外沿不超出镇中心 ±LIM（再加外圈缓坡 EDGE）
PLOT_G = 2         # 町地轮廓的网格（格）：轮廓按 2×2 的小块走（更细的弯），缓坡再把台阶抹圆


def J(c):
    return json.dumps(c, ensure_ascii=False, separators=(",", ":"))


def T(text, colour=ui.BROADCAST_BODY, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def fn(name, lines):
    path = os.path.join(FUNC, "town", name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT[0] += 1


def wj(rel, doc):
    path = os.path.join(DP, "data", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)


# ============================================================================ 城镇表
# 地标按群系挑地方（用户 2026-11-28）：#lmk = 1 孤堡（边地高处）、2 尼古拉城堡（阴暗的林子）、3 湖畔庄园（平地，町地外有水）
LM_BIOMES = {1: ["rpg:stone_forest", "rpg:wildfield", "rpg:snowfield", "rpg:geyser_taiga"],
             2: ["rpg:ashwood", "rpg:lavender_forest", "rpg:geyser_taiga"],
             3: ["rpg:plains", "rpg:forest", "rpg:golden_forest", "rpg:wildfield"]}
LM_KIND = {"lone_fort": 1, "castle_nicolae": 2, "lake_mansion": 3}
LANDMARKS = [  # (编号, 名, 英文, 结构, 半径, 角度, 副标题)
    (21, "孤堡", "Lone Fort", "lone_fort", 2600, 54, "教廷前哨 · 审判官驻地"),
    (22, "孤堡", "Lone Fort", "lone_fort", 2600, 234, "教廷前哨 · 审判官驻地"),
    (23, "尼古拉城堡", "Castle Nicolae", "castle_nicolae", 4300, 126, "无人的古堡"),
    (24, "湖畔庄园", "Lake Mansion", "lake_mansion", 2600, 306, "边缘者的网络藏在这里"),
]


def towns():
    out = []
    for ring, r in enumerate(RING):
        for k in range(10):
            a = math.radians(36 * k + 18)
            zh, en = NAMES[k][ring * 2], NAMES[k][ring * 2 + 1]
            out.append(dict(i=ring * 10 + k + 1, nation=k, ring=ring, zh=zh, en=en, type=(TYPES_A, TYPES_B)[ring][k],
                            x=round(r * math.sin(a)), z=round(-r * math.cos(a))))
    for i, zh, en, key, r, deg, sub in LANDMARKS:
        a = math.radians(deg)
        out.append(dict(i=i, nation=0, ring=2, zh=zh, en=en, type="lm", key=key, sub=sub, lm=True,
                        x=round(r * math.sin(a)), z=round(-r * math.cos(a))))
    return out


# ============================================================================ 布局（离线）
def rot_pt(r, x, z):
    return [(x, z), (-z, x), (-x, -z), (z, -x)][r]


def footprint(meta, rot):
    sx, _sy, sz = meta["size"]
    return (sx, sz) if rot in (0, 2) else (sz, sx)


def pivot(rot, mx, mz, wx, wz):
    """place template 的落点：让旋转后的建筑正好占 [mx, mx+wx-1] × [mz, mz+wz-1]。"""
    return [(mx, mz), (mx + wx - 1, mz), (mx + wx - 1, mz + wz - 1), (mx, mz + wz - 1)][rot]


def overlap(a, b, gap):
    return not (a[0] + a[2] + gap <= b[0] or b[0] + b[2] + gap <= a[0] or a[1] + a[3] + gap <= b[1] or b[1] + b[3] + gap <= a[1])


def layout(town, META, v1=False):
    if town.get("lm"):
        wx, wz = footprint(META[town["key"]], 0)
        c = dict(key=town["key"], role="center", rot=0, rect=(-(wx // 2), -(wz // 2), wx, wz))
        return [c], None, None, [c["rect"]]
    best = None
    for salt in range(40):
        got = _layout(town, META, salt, v1)
        ext = max(max(abs(q[0]), abs(q[0] + q[2]), abs(q[1]), abs(q[1] + q[3])) for q in got[3])
        if best is None or ext < best[0]:
            best = (ext, got)
        if ext <= PAD - 4:
            break
    return best[1]


def _layout(town, META, salt, v1=False):
    rng = random.Random(9177 + town["i"] * 131 + salt * 7919)
    spec = LAYOUTS[town["type"]]
    placed = []      # dict(key, role, rot, rect=(mx, mz, wx, wz))
    rects = []
    m0 = META[spec[0][0]]
    wx, wz = footprint(m0, 0)
    c = dict(key=spec[0][0], role="center", rot=0, rect=(-(wx // 2), -(wz // 2), wx, wz))
    placed.append(c)
    rects.append(c["rect"])
    # 刑台广场在天使像正面（用户 2026-11-28：「断头台是对着天使的正面」）
    a0 = math.atan2(STEP[m0["front"]][1], STEP[m0["front"]][0])
    r0 = rng.random()
    if v1:                              # 2026-11-28 之前的布局：广场随机绕在天使像四周（重修旧存档时要知道旧房子在哪）
        a0 = r0 * 2 * math.pi
    pw, pd = RESERVED["plaza"]
    px, pz = round(math.cos(a0) * (wx // 2 + pw // 2 + 3)), round(math.sin(a0) * (wz // 2 + pd // 2 + 3))
    plaza = (px - pw // 2, pz - pd // 2, pw, pd)
    rects.append(plaza)
    order = sorted(spec[1:], key=lambda kr: -(META[kr[0]]["size"][0] * META[kr[0]]["size"][2]))
    base_a = rng.random() * 2 * math.pi
    for n, (key, role) in enumerate(order):
        meta = META[key]
        ok = None
        r = 14
        while ok is None and r < 260:
            angles = [base_a + 2 * math.pi * (k + rng.random() * 0.5) / 16 for k in range(16)]
            rng.shuffle(angles)
            for a in angles:
                cx, cz = r * math.cos(a), r * math.sin(a)
                want = ("west" if cx > 0 else "east") if abs(cx) > abs(cz) else ("north" if cz > 0 else "south")
                rot = (DIRS.index(want) - DIRS.index(meta["front"])) % 4
                bw, bd = footprint(meta, rot)
                rect = (round(cx - bw / 2), round(cz - bd / 2), bw, bd)
                # 天使像四周留出一片空地当广场（用户 2026-11-28「天使雕塑附近土径的范围大一点，就像一个广场」）；旧布局（v1）不变
                if all(not overlap(rect, q, GAP) for q in rects) and (v1 or not overlap(rect, c["rect"], CENTER_CLEAR)):
                    ok = dict(key=key, role=role, rot=rot, rect=rect)
                    break
            r += 3
        if ok is None:
            raise SystemExit("towns: %s 放不下 %s" % (town["zh"], key))
        placed.append(ok)
        rects.append(ok["rect"])
    ext = max(max(abs(q[0]), abs(q[0] + q[2]), abs(q[1]), abs(q[1] + q[3])) for q in rects)
    gw, gd = RESERVED["grave"]
    grave = None
    for r in range(ext - 6, ext + 60, 3):
        for k in range(24):
            a = a0 + math.pi + 2 * math.pi * k / 24 * (1 if k % 2 else -1) / 2
            rect = (round(r * math.cos(a) - gw / 2), round(r * math.sin(a) - gd / 2), gw, gd)
            if all(not overlap(rect, q, GAP) for q in rects):
                grave = rect
                break
        if grave:
            break
    rects.append(grave)
    return placed, plaza, grave, rects


def door_point(b, META):
    """门外两格（世界偏移，相对镇中心）。"""
    meta = META[b["key"]]
    mx, mz, wx, wz = b["rect"]
    px, pz = pivot(b["rot"], mx, mz, wx, wz)
    front = DIRS[(DIRS.index(meta["front"]) + b["rot"]) % 4]
    sx, sz = STEP[front]
    if meta["doors"]:
        pts = [(px + rot_pt(b["rot"], d[0], d[2])[0], pz + rot_pt(b["rot"], d[0], d[2])[1]) for d in meta["doors"]]
        dx, dz = min(pts, key=lambda q: q[0] * q[0] + q[1] * q[1])
    else:
        dx, dz = mx + wx // 2, mz + wz // 2
        dx, dz = {"north": (dx, mz), "south": (dx, mz + wz - 1), "west": (mx, dz), "east": (mx + wx - 1, dz)}[front]
    # 从门往外走到包围盒外两格
    while mx <= dx < mx + wx and mz <= dz < mz + wz:
        dx, dz = dx + sx, dz + sz
    return dx + sx, dz + sz


def noise(x, z, seed, size):
    def h(i, j):
        n = (i * 374761393 + j * 668265263 + seed * 1274126177) & 0xFFFFFFFF
        n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
        return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0
    fx, fz = x / float(size), z / float(size)
    i, j = math.floor(fx), math.floor(fz)
    u, v = fx - i, fz - j
    u, v = u * u * (3 - 2 * u), v * v * (3 - 2 * v)
    return (h(i, j) * (1 - u) + h(i + 1, j) * u) * (1 - v) + (h(i, j + 1) * (1 - u) + h(i + 1, j + 1) * u) * v


def paths(town, placed, plaza, grave, rects, META):
    """蜿蜒土径：{(x, z): 'P'|'C'|'G'|'M'}（P 土径、C 粗土、G 碎石、M 苔藓）。"""
    seed = town["i"] * 7 + 3
    rng = random.Random(seed)
    span = lambda q: max(abs(q[0]), abs(q[0] + q[2]), abs(q[1]), abs(q[1] + q[3]))
    ext = max(span(q) for q in rects)
    R = ext + 62
    RF = R                                          # 林中营地另外单独 forceload（见 job/camp）
    blocked = set()
    near = set()
    for b in placed:
        mx, mz, wx, wz = b["rect"]
        for x in range(mx - 1, mx + wx + 1):
            for z in range(mz - 1, mz + wz + 1):
                (blocked if mx <= x < mx + wx and mz <= z < mz + wz else near).add((x, z))
    gx, gz, gw, gd = grave
    for x in range(gx, gx + gw):
        for z in range(gz, gz + gd):
            near.add((x, z))
    used = set()

    def route(start, goal_test, goal_pt):
        dist = {start: 0.0}
        pq = [(0.0, start)]
        prev = {}
        while pq:
            d, cur = heapq.heappop(pq)
            if d > dist.get(cur, 1e18):
                continue
            if goal_test(cur):
                out = [cur]
                while cur in prev:
                    cur = prev[cur]
                    out.append(cur)
                return out[::-1]
            x, z = cur
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nb = (x + dx, z + dz)
                if nb in blocked or abs(nb[0]) > R + 4 or abs(nb[1]) > R + 4:
                    continue
                w = 1.0 + 2.6 * noise(nb[0], nb[1], seed, 9) + (5.0 if nb in near else 0.0)
                if nb in used:
                    w *= 0.35
                nd = d + w + 0.15 * (abs(nb[0] - goal_pt[0]) + abs(nb[1] - goal_pt[1]) - abs(x - goal_pt[0]) - abs(z - goal_pt[1]))
                if nd < dist.get(nb, 1e18):
                    dist[nb] = nd
                    prev[nb] = cur
                    heapq.heappush(pq, (nd, nb))
        return []

    c = placed[0]["rect"]
    ring = lambda q: c[0] - 3 <= q[0] <= c[0] + c[2] + 2 and c[1] - 3 <= q[1] <= c[1] + c[3] + 2
    lines = []
    for b in placed[1:]:
        if b["role"] == "camp":
            continue
        dp = door_point(b, META)
        blocked.discard(dp)
        lines.append(route(dp, ring, (0, 0)))
        used.update(lines[-1])
    # 广场、墓地也接上
    for rect in (plaza, grave):
        pt = (rect[0] + rect[2] // 2, rect[1] + rect[3] // 2)
        lines.append(route(pt, ring, (0, 0)))
        used.update(lines[-1])
    # 三条出镇的小路
    a0 = rng.random() * 2 * math.pi
    for k in range(3):
        a = a0 + 2 * math.pi * k / 3 + rng.uniform(-0.3, 0.3)
        goal = (round(R * math.cos(a)), round(R * math.sin(a)))
        lines.append(route((c[0] + c[2] // 2, c[1] - 3), lambda q, g=goal: abs(q[0] - g[0]) + abs(q[1] - g[1]) <= 2, goal))
        used.update(lines[-1])
    cells = {}
    for ln in lines:
        for n, (x, z) in enumerate(ln):
            d = math.hypot(x, z)
            fade = max(0.0, (d - ext) / 62.0)
            if fade > 0 and rng.random() < fade * 0.85:
                continue
            w = 1 if fade > 0.4 else 1 + int(noise(x, z, seed + 11, 7) * 2.999)
            nx, nz = (ln[min(n + 1, len(ln) - 1)][0] - ln[max(n - 1, 0)][0], ln[min(n + 1, len(ln) - 1)][1] - ln[max(n - 1, 0)][1])
            px, pz = (0, 1) if abs(nx) >= abs(nz) else (1, 0)
            pts = [(x, z)] + ([(x + px, z + pz)] if w >= 2 else []) + ([(x - px, z - pz)] if w >= 3 else [])
            for q in pts:
                if q in blocked:
                    continue
                r = rng.random()
                cells[q] = "P" if r < 0.78 - fade * 0.4 else ("C" if r < 0.9 else "G")
    # 天使像四周铺开一片土径，像个广场（用户 2026-11-28「天使雕塑附近土径的范围大一点，就像一个广场」）：
    # 离雕像底座 9–15 格以内（随方向起伏），边上再由下面的毛边打散
    cx0, cz0, cw, cd = c
    for x in range(cx0 - 21, cx0 + cw + 21):
        for z in range(cz0 - 21, cz0 + cd + 21):
            if (x, z) in blocked:
                continue
            gx = max(cx0 - x, 0, x - (cx0 + cw - 1))
            gz = max(cz0 - z, 0, z - (cz0 + cd - 1))
            th = math.atan2(z - (cz0 + cd / 2.0), x - (cx0 + cw / 2.0))
            lim = 12 + 8 * noise(4 * math.cos(th) + 7, 4 * math.sin(th) + 7, seed + 23, 1)
            if math.hypot(gx, gz) <= lim:
                r = rng.random()
                cells[(x, z)] = "P" if r < 0.8 else ("C" if r < 0.93 else "G")
    for (x, z) in list(cells):
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, z + dz)
            if q not in cells and q not in blocked and rng.random() < 0.22:
                cells[q] = rng.choice("CCGM")
    for x in range(plaza[0], plaza[0] + plaza[2]):          # 广场中间留给刑台
        for z in range(plaza[1], plaza[1] + plaza[3]):
            if abs(x - (plaza[0] + plaza[2] // 2)) < 4 and abs(z - (plaza[1] + plaza[3] // 2)) < 4:
                cells.pop((x, z), None)
    return cells, RF


# ============================================================================ 数据包：建筑
def building_fns(META, used):
    for key, rot in sorted(used):
        meta = META[key]
        sx, sy, sz = meta["size"]
        wx, wz = footprint(meta, rot)
        ax, az = [(0, 0), (-(wx - 1), 0), (-(wx - 1), -(wz - 1)), (0, -(wz - 1))][rot]
        out = ["# %s（旋转 %s）：positioned 在落点、y = 结构原点；宏参数 sfx（材质版本）" % (key, ROTS[rot])]
        # 1 清掉脚下与上方的树和花草（不碰地形）
        y0, y1 = -2, sy + 12
        xs = list(range(ax - 2, ax + wx + 2, 32))
        for x in xs:
            for z in range(az - 2, az + wz + 2, 32):
                x2, z2 = min(x + 31, ax + wx + 1), min(z + 31, az + wz + 1)
                h = max(1, 32768 // ((x2 - x + 1) * (z2 - z + 1)))
                for y in range(y0, y1 + 1, h):
                    out.append("fill ~%d ~%d ~%d ~%d ~%d ~%d minecraft:air replace #rpg:town_clear" % (x, y, z, x2, min(y + h - 1, y1), z2))
        # 2 放结构
        out.append("$place template rpg:town/%s$(sfx) ~ ~ ~ %s" % (key, ROTS[rot]))
        # 3 地基裙边：往下垫 10 格，只替换空气、水和花草
        groups = {}
        for x, z, lo, mat in meta["skirt"]:
            if any(t in mat for t in WOODISH):
                mat = "cobblestone"
            rx, rz = rot_pt(rot, x, z)
            groups.setdefault((lo, mat), set()).add((rx, rz))
        for (lo, mat), cells in sorted(groups.items()):
            for x0, z0, x1, z1 in rects_of(cells):
                out.append("fill ~%d ~%d ~%d ~%d ~%d ~%d minecraft:%s replace #rpg:town_soft" % (x0, lo - 1, z0, x1, lo - 10, z1, mat))
        fn("b/%s/%s" % (key, rot_name(rot)), out)


def rot_name(rot):
    return ["none", "cw", "180", "ccw"][rot]


def rects_of(cells):
    """把格子并成长方形（贪心）。"""
    left = set(cells)
    out = []
    for (x, z) in sorted(cells, key=lambda q: (q[1], q[0])):
        if (x, z) not in left:
            continue
        x1 = x
        while (x1 + 1, z) in left:
            x1 += 1
        z1 = z
        while all((xx, z1 + 1) in left for xx in range(x, x1 + 1)):
            z1 += 1
        for xx in range(x, x1 + 1):
            for zz in range(z, z1 + 1):
                left.discard((xx, zz))
        out.append((x, z, x1, z1))
    return out


# ============================================================================ 数据包：每座镇
def town_fns(META):
    used = set()
    info = {}
    for t in towns():
        placed, plaza, grave, rects = layout(t, META)
        if t.get("lm"):
            c = rects[0]
            cells, R = {}, max(max(abs(c[0]), abs(c[1]), c[0] + c[2], c[1] + c[3]) + 8, LIM + EDGE + 4)
        else:
            cells, R = paths(t, placed, plaza, grave, rects, META)
            R = max(R, LIM + EDGE + 4)
        i = t["i"]
        out = ["# %s（%s）：positioned 镇中心 y=0；宏参数 sfx、var" % (t["zh"], t.get("sub") or NATIONS[t["nation"]] + " · " + KIND[t["type"]]),
               "$scoreboard players set #var %s $(var)" % O]
        plot_fns(i, rects)
        out.append("$execute positioned ~ $(h) ~ run function %s/pad/t%d" % (P, i))
        if t.get("lm"):
            out.append('data modify storage rpg:town m.sfx set value ""')      # 地标只有原版材质
        roles = {}
        for n, b in enumerate(placed):
            meta = META[b["key"]]
            mx, mz, wx, wz = b["rect"]
            px, pz = pivot(b["rot"], mx, mz, wx, wz)
            used.add((b["key"], b["rot"]))
            samples = [(mx + 2, mz + 2), (mx + wx - 3, mz + 2), (mx + 2, mz + wz - 3), (mx + wx - 3, mz + wz - 3), (mx + wx // 2, mz + wz // 2)]
            out += ["scoreboard players set #hm %s -999" % O] + [
                "execute positioned ~%d 0 ~%d positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function %s/s/max" % (x, z, P)
                for x, z in samples] + [
                "execute if score #hm %s matches -999 run scoreboard players operation #hm %s = #h0 %s" % (O, O, O),
                "scoreboard players remove #hm %s %d" % (O, meta["lift"]),
                "execute store result storage rpg:town m.y int 1 run scoreboard players get #hm %s" % O,
                "function %s/t/%d/%d with storage rpg:town m" % (P, i, n)]
            cx, cz = mx + wx // 2, mz + wz // 2
            sub = ["$execute positioned ~%d $(y) ~%d run function %s/b/%s/%s with storage rpg:town m" % (px, pz, P, b["key"], rot_name(b["rot"]))]
            if b["role"] in ("granary", "church", "tavern", "rent", "elder", "priest", "keep", "center"):
                sub.append('$execute positioned ~%d $(y) ~%d run summon minecraft:marker ~ ~%d ~ {Tags:["rpg.tw.a","rpg.tw.in.%s","rpg.tw.new"]}'
                           % (cx, cz, meta["lift"], b["role"]))
            if b["role"] == "camp":
                sub.append('$execute positioned ~%d $(y) ~%d run summon minecraft:marker ~ ~%d ~ {Tags:["rpg.tw.a","rpg.tw.at.camp","rpg.tw.new"]}' % (cx, cz, meta["lift"]))
            elif b["role"] != "center":
                dx, dz = door_point(b, META)
                sub.append('execute positioned ~%d 0 ~%d positioned over motion_blocking_no_leaves run summon minecraft:marker ~ ~ ~ {Tags:["rpg.tw.a","rpg.tw.at.%s","rpg.tw.new"]}'
                           % (dx, dz, b["role"]))
                roles.setdefault(b["role"], (dx, dz))
            fn("t/%d/%d" % (i, n), sub)
        c = placed[0]["rect"]
        spawn = (c[0] + c[2] // 2, c[1] + c[3] + 3)
        if t.get("lm"):
            out += ['summon minecraft:marker ~ 0 ~ {Tags:["rpg.tw.a","rpg.tw.c","rpg.tw.lm","rpg.tw.new"]}',
                    "execute positioned ~%d 0 ~%d positioned over motion_blocking_no_leaves run tp @e[type=minecraft:marker,tag=rpg.tw.c,tag=rpg.tw.new] ~ ~ ~" % spawn]
            if t["key"] == "lone_fort":
                out.append("execute positioned ~%d 0 ~%d positioned over motion_blocking_no_leaves run function %s/lm/fort" % (spawn[0], spawn[1], P))
            out += ["scoreboard players set @e[type=minecraft:marker,tag=rpg.tw.new] %s_id %d" % (O, i),
                    "tag @e[type=minecraft:marker,tag=rpg.tw.new] remove rpg.tw.new"]
            fn("build/t%d" % i, out)
            info[i] = dict(t, R=R, roles={}, spawn=spawn, cells=0, n=1)
            continue
        bench = (c[0] - 3, c[1] + c[3] // 2)
        board = (c[0] + c[2] + 2, c[1] + c[3] // 2)
        anchors = {"plaza": (plaza[0] + plaza[2] // 2, plaza[1] + plaza[3] // 2), "grave": (grave[0] + grave[2] // 2, grave[1] + grave[3] // 2),
                   "spawn": spawn, "bench": bench, "board": board}
        for role, (x, z) in anchors.items():
            out.append('execute positioned ~%d 0 ~%d positioned over motion_blocking_no_leaves run summon minecraft:marker ~ ~ ~ {Tags:["rpg.tw.a","rpg.tw.at.%s","rpg.tw.new"]}' % (x, z, role))
        out.append("execute positioned ~%d 0 ~%d positioned over motion_blocking_no_leaves run setblock ~ ~ ~ minecraft:soul_campfire[lit=true]" % bench)
        # 土径
        for (x, z), m in sorted(cells.items()):
            out.append("execute positioned ~%d 0 ~%d positioned over motion_blocking_no_leaves run function %s/p/%s" % (x, z, P, m.lower()))
        out += ['summon minecraft:marker ~ 0 ~ {Tags:["rpg.tw.a","rpg.tw.c","rpg.tw.new"]}',
                "execute positioned ~%d 0 ~%d positioned over motion_blocking_no_leaves run tp @e[type=minecraft:marker,tag=rpg.tw.c,tag=rpg.tw.new] ~ ~ ~" % spawn,
                "scoreboard players set @e[type=minecraft:marker,tag=rpg.tw.new] %s_id %d" % (O, i),
                "tag @e[type=minecraft:marker,tag=rpg.tw.new] remove rpg.tw.new"]
        fn("build/t%d" % i, out)
        info[i] = dict(t, R=R, roles=roles, spawn=spawn, cells=len(cells), n=len(placed))
    used.update(("orc_camp", r) for r in range(4))
    camp_fns(META)
    building_fns(META, used)
    return info


def camp_fns(META):
    """林中营地：镇中心 185–215 格的一圈里，挑最平的一块（不在水上）放，脚下照样垫地基、只清植被。"""
    import math as M
    meta = META["orc_camp"]
    cands = [(dx, dz, n % 4) for n, (dx, dz) in enumerate((dx, dz) for dx in (-24, 0, 24) for dz in (-24, 0, 24))]
    find = ["# 找营地（positioned 营地中心 y=0，离镇约 200 格）：9 个候选，取高差最小的", "scoreboard players set #best %s 9999" % O, "scoreboard players set #bn %s -1" % O]
    for n, (cx, cz, rot) in enumerate(cands):
        bw, bd = footprint(meta, rot)
        smp = [(cx + dx, cz + dz) for dx in (-bw // 2 + 2, 0, bw // 2 - 2) for dz in (-bd // 2 + 2, 0, bd // 2 - 2)]
        fn("camp/c/%d" % n, ["scoreboard players set #mn %s 9999" % O, "scoreboard players set #mx %s -9999" % O, "scoreboard players set #ok %s 1" % O] +
           ["execute positioned ~%d 0 ~%d positioned over motion_blocking_no_leaves run function %s/s/mm" % (x, z, P) for x, z in smp] +
           ["scoreboard players operation #sp %s = #mx %s" % (O, O), "scoreboard players operation #sp %s -= #mn %s" % (O, O),
            "execute if score #ok %s matches 0 run scoreboard players add #sp %s 1000" % (O, O),
            "execute if score #mn %s matches ..62 run scoreboard players add #sp %s 1000" % (O, O),
            "execute if score #sp %s < #best %s run scoreboard players set #bn %s %d" % (O, O, O, n),
            "execute if score #sp %s < #best %s run scoreboard players operation #best %s = #sp %s" % (O, O, O, O)])
        find.append("function %s/camp/c/%d" % (P, n))
        mx, mz = cx - bw // 2, cz - bd // 2
        px, pz = pivot(rot, mx, mz, bw, bd)
        fn("camp/at/%d" % n, ["scoreboard players set #hm %s -999" % O] + [
            "execute positioned ~%d 0 ~%d positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function %s/s/max" % (x, z, P) for x, z in smp] + [
            "scoreboard players remove #hm %s %d" % (O, meta["lift"]),
            "execute store result storage rpg:town m.y int 1 run scoreboard players get #hm %s" % O,
            "function %s/camp/put/%d with storage rpg:town m" % (P, n)])
        fn("camp/put/%d" % n, ['data modify storage rpg:town m.sfx set value ""', "$execute positioned ~%d $(y) ~%d run function %s/b/orc_camp/%s with storage rpg:town m" % (px, pz, P, rot_name(rot)),
                               '$execute positioned ~%d $(y) ~%d run summon minecraft:marker ~ ~%d ~ {Tags:["rpg.tw.a","rpg.tw.at.camp","rpg.tw.new"]}' % (cx, cz, meta["lift"])])
    find += ["execute if score #bn %s matches %d run function %s/camp/at/%d" % (O, n, P, n) for n in range(len(cands))]
    fn("camp/find", find)
    # 营地不能压到镇上（用户 2026-11-28：林中祭坛建到了镇里）：每座镇的每个候选，离镇中心最近的一格都要在町地与缓坡之外
    for i in range(1, 21):
        a = M.radians((i * 137.5) % 360)
        ox, oz = round(CAMP_R[1] * M.cos(a)), round(CAMP_R[1] * M.sin(a))
        for cx, cz, rot in cands:
            bw, bd = footprint(meta, rot)
            x0, z0 = ox + cx - bw // 2, oz + cz - bd // 2
            gx, gz = max(x0, 0, -(x0 + bw - 1)), max(z0, 0, -(z0 + bd - 1))
            assert M.hypot(gx, gz) >= LIM + EDGE + 8, ("camp too close", i, cx, cz)


# ============================================================================ 数据包：选址任务
def job(info):
    N = len(info)
    fn("load", [
        "scoreboard objectives add %s dummy" % O, "scoreboard objectives add %s_id dummy" % O, "scoreboard objectives add %s_home dummy" % O,
        "scoreboard objectives add %s_at dummy" % O, "scoreboard objectives add %s_wait dummy" % O, "scoreboard objectives add %s_gm dummy" % O,
        "scoreboard objectives add %s_ev dummy" % O,
        "execute unless score #init %s matches 1 run function %s/init" % (O, P),
        "execute unless score #campv %s matches 1 run function %s/job/campfix" % (O, P),
        "scoreboard players set #cur %s 0" % O, "scoreboard players set #2 %s 2" % O,
        "schedule function %s/job/tick 40t" % P,
        "schedule function %s/sec 20t" % P])
    fn("init", ["scoreboard players set #init %s 1" % O] + ["scoreboard players set #s%d %s 0" % (i, O) for i in info] +
       ["data modify storage rpg:town m set value {sfx:\"\",var:0,y:0,x:0,z:0}"])
    # 名义位置与候选偏移
    fn("job/tick", ["# 选址与建造，一次只处理一座（每秒一次）；#s：0 未建 1 排队 2 在建 3 建好 4 放弃 5 待重修",
                    "schedule function %s/job/tick 20t" % P,
                    "execute if score #cur %s matches 1.. run return run function %s/job/step" % (O, P)] +
       ["execute if score #s%d %s matches 5 run return run function %s/job/re/%d" % (i, O, P, i) for i, t in sorted(info.items()) if not t.get("lm")] +
       ["execute if score #s%d %s matches 1 run return run function %s/job/begin {i:%d,nx:%d,nz:%d}" % (i, O, P, i, t["x"], t["z"]) for i, t in sorted(info.items())])
    fn("job/begin", ["$scoreboard players set #cur %s $(i)" % O, "$scoreboard players set #nx %s $(nx)" % O, "$scoreboard players set #nz %s $(nz)" % O,
                     "scoreboard players set #c %s 0" % O, "scoreboard players set #relax %s 0" % O, "scoreboard players set #ph %s 0" % O])
    fn("job/step", ["execute if score #cool %s matches 1.. run return run scoreboard players remove #cool %s 1" % (O, O),
                    "execute if score #ph %s matches 0 run return run function %s/job/probe" % (O, P),
                    "execute if score #ph %s matches 1 run return run function %s/job/eval" % (O, P),
                    "execute if score #ph %s matches 2 run return run function %s/job/wait_build" % (O, P),
                    "execute if score #ph %s matches 3 run return run function %s/job/camp_wait" % (O, P),
                    "execute if score #ph %s matches 4 run return run function %s/job/re_wait" % (O, P)])
    # 重修（2026-11-28）：旧版 job/camp_at 用 players add 加负数偏移会失败，营地落在了镇中心、压在房子上。
    # 这些镇原地重建：清掉镇上的人与道具、整块重新削平（连同更高处），重放建筑，营地放到约 200 格外。
    import math as M
    bad = []
    for i, t in sorted(info.items()):
        if t.get("lm"):
            continue
        a = M.radians((i * 137.5) % 360)
        dx, dz = round(200 * M.cos(a)), round(200 * M.sin(a))
        if dx < 0 or (dz < 0 and dx < 160):
            bad.append(i)
    fn("job/campfix", ["# 旧存档：营地错放进镇里的那些镇，排进重修（只做一次）", "scoreboard players set #campv %s 1" % O] +
       ["execute if score #s%d %s matches 3 run scoreboard players set #s%d %s 5" % (i, O, i, O) for i in bad])
    for i, t in sorted(info.items()):
        if t.get("lm"):
            continue
        fn("job/re/%d" % i, ["# 重修 %s：原址（#x/#z）、原高度（出生点锚的 y）、原地皮" % t["zh"],
                             "execute unless score #sy%d %s matches 1.. run return run scoreboard players set #s%d %s 3" % (i, O, i, O),
                             "scoreboard players set #cur %s %d" % (O, i),
                             "scoreboard players operation #px %s = #x%d %s" % (O, i, O), "scoreboard players operation #pz %s = #z%d %s" % (O, i, O),
                             "scoreboard players operation #v %s = #v%d %s" % (O, i, O), "scoreboard players operation #h0 %s = #sy%d %s" % (O, i, O),
                             "scoreboard players set #r %s %d" % (O, info[i]["R"] + 4),
                             "function %s/job/coords" % P, "function %s/job/bigcoords" % P, "function %s/job/big_add with storage rpg:town m" % P,
                             "scoreboard players set #wt %s 0" % O, "scoreboard players set #ph %s 4" % O])
    fn("job/re_wait", ["scoreboard players add #wt %s 1" % O,
                       "function %s/job/big_loaded with storage rpg:town m" % P,
                       "execute if score #ld %s matches 0 if score #wt %s matches ..120 run return 0" % (O, O),
                       "execute if score #ld %s matches 0 run return run function %s/job/re_abort" % (O, P),
                       "execute store result storage rpg:town m.h int 1 run scoreboard players get #h0 %s" % O,
                       "function %s/job/re_wipe with storage rpg:town m" % P,
                       "function %s/job/build" % P])
    fn("job/re_abort", ["# 区块迟迟不到：这次不修了（下次读档也不再修）", "function %s/job/big_rem with storage rpg:town m" % P] +
       ["execute if score #cur %s matches %d run scoreboard players set #s%d %s 3" % (O, i, i, O) for i in info] + ["scoreboard players set #cur %s 0" % O])
    wipe = ["$execute in minecraft:overworld positioned $(x) $(h) $(z) run function %s/job/re_wipe2" % P]
    fn("job/re_wipe", wipe)
    fn("job/re_wipe2", ["# 清掉这座镇上的人、骑在他们身上的模型与名牌、道具、锚点（positioned 镇中心）",
                        "execute as @e[type=minecraft:villager,tag=rpg.tnpc,distance=..170] on passengers run kill @s",
                        "kill @e[type=minecraft:villager,tag=rpg.tnpc,distance=..170]",
                        "execute as @e[type=minecraft:villager,tag=rpg.mer.smith,distance=..170] on passengers run kill @s",
                        "kill @e[type=minecraft:villager,tag=rpg.mer.smith,distance=..170]",
                        "execute as @e[tag=rpg.tw.guard,distance=..170] on passengers run kill @s",
                        "kill @e[tag=rpg.tw.guard,distance=..170]",
                        "kill @e[type=minecraft:interaction,tag=rpg.tnpc,distance=..170]",
                        "kill @e[type=minecraft:text_display,tag=rpg.tnpc.plate,distance=..170]",
                        "kill @e[tag=rpg.tw.prop,distance=..170]",
                        "kill @e[type=minecraft:marker,tag=rpg.tw.a,distance=..170]",
                        "tellraw @a[distance=..200] %s" % J(["", T("〖城镇〗", ui.BROADCAST_NAME, True), T(ui.GAP + "这座镇在重修：林中营地挪去了镇外。", ui.BROADCAST_BODY)])] +
       ["execute if score #cur %s matches %d run function %s/job/re_clear/%d" % (O, i, P, i) for i in bad])
    # 只清旧房子、旧广场墓地和错放的营地所在的地方（都在旧町地的平地上），不碰町地外的地形
    META = json.load(open(os.path.join(STRUCT, "meta.json"), encoding="utf-8"))
    for i in bad:
        t = info[i]
        _pl, _pz, _gr, old = layout(t, META, v1=True)
        rs = [(q[0] - 3, q[1] - 3, q[0] + q[2] + 2, q[1] + q[3] + 2) for q in old]
        a = M.radians((i * 137.5) % 360)
        dx = round(200 * M.cos(a))
        cx = 0 if dx < 0 else dx                    # 旧营地：dx 为负时在镇中心；否则只挪了 x
        rs.append((max(cx - 44, -PAD), -44, min(cx + 44, PAD - 1), 43))
        fn("job/re_clear/%d" % i, ["# 重修 %s：旧房子、旧营地上方清空（y 0–100），地皮重铺（positioned 镇中心，y = 地面上一格）" % t["zh"]] +
           plot_fills(rs, 0, 100, "minecraft:air") + plot_fills(rs, -1, -1, "minecraft:grass_block") +
           plot_fills(rs, -1, -1, "minecraft:snow_block", "minecraft:grass_block", "execute if score #v %s matches 1 run " % O) +
           plot_fills(rs, -1, -1, "minecraft:sand", "minecraft:grass_block", "execute if score #v %s matches 2 run " % O))
    probe = ["# 下一个候选点：名义位置 + 偏移；forceload 四周 %d 格" % PROBE, "scoreboard players set #lmk %s 0" % O] + [
        "execute if score #cur %s matches %d run scoreboard players set #lmk %s %d" % (O, i, O, LM_KIND[info[i]["key"]])
        for i in info if info[i].get("lm")]
    for c, (dx, dz) in enumerate(OFFS):
        probe.append("execute if score #c %s matches %d run function %s/job/off {dx:%d,dz:%d}" % (O, c, P, dx, dz))
    probe += ["scoreboard players operation #px %s = #nx %s" % (O, O), "scoreboard players operation #px %s += #dx %s" % (O, O),
              "scoreboard players operation #pz %s = #nz %s" % (O, O), "scoreboard players operation #pz %s += #dz %s" % (O, O),
              "function %s/job/coords" % P,
              "function %s/job/fl_add with storage rpg:town m" % P,
              "scoreboard players set #wt %s 0" % O, "scoreboard players set #lw %s 0" % O, "scoreboard players set #ph %s 1" % O]
    fn("job/probe", probe)
    co = []
    for a in ("x", "z"):
        co.append("execute store result storage rpg:town m.%s int 1 run scoreboard players get #p%s %s" % (a, a, O))
        for d in (20, 40, 48, 90, 96, 128):
            for sgn, tag in ((1, "p"), (-1, "m")):
                co += ["scoreboard players operation #t %s = #p%s %s" % (O, a, O), "scoreboard players %s #t %s %d" % ("add" if sgn > 0 else "remove", O, d),
                       "execute store result storage rpg:town m.%s%s%d int 1 run scoreboard players get #t %s" % (a, tag, d, O)]
    fn("job/coords", ["# 宏不能做加减：把候选点四周要用的坐标先算好放进 rpg:town m"] + co)
    big = []
    for a in ("x", "z"):
        for tag, op in (("lo", "remove"), ("hi", "add")):
            big += ["scoreboard players operation #t %s = #p%s %s" % (O, a, O), "scoreboard players operation #t %s %s= #r %s" % (O, "-" if op == "remove" else "+", O),
                    "execute store result storage rpg:town m.%s%s int 1 run scoreboard players get #t %s" % (a, tag, O)]
    for a in ("x", "z"):
        for n, (num, den) in enumerate(((-3, 3), (-1, 3), (1, 3), (3, 3))):
            big += ["scoreboard players operation #t %s = #r %s" % (O, O), "scoreboard players set #k %s %d" % (O, num),
                    "scoreboard players operation #t %s *= #k %s" % (O, O), "scoreboard players set #k %s %d" % (O, den),
                    "scoreboard players operation #t %s /= #k %s" % (O, O), "scoreboard players operation #t %s += #p%s %s" % (O, a, O),
                    "execute store result storage rpg:town m.%s%d int 1 run scoreboard players get #t %s" % (a, n, O)]
    fn("job/bigcoords", big)
    fn("job/off", ["$scoreboard players set #dx %s $(dx)" % O, "$scoreboard players set #dz %s $(dz)" % O])
    fn("job/fl_add", ["$execute in minecraft:overworld run forceload add %s" % box("$(x)", "$(z)", PROBE)])
    fn("job/fl_rem", ["$execute in minecraft:overworld run forceload remove %s" % box("$(x)", "$(z)", PROBE)])
    fn("job/eval", ["scoreboard players add #wt %s 1" % O,
                    "function %s/job/loaded with storage rpg:town m" % P,
                    "execute if score #ld %s matches 0 if score #wt %s matches ..90 run return 0" % (O, O),
                    "execute if score #ld %s matches 1 if score #lw %s matches 0 run scoreboard players operation #lw %s = #wt %s" % (O, O, O, O),
                    "scoreboard players operation #since %s = #wt %s" % (O, O), "scoreboard players operation #since %s -= #lw %s" % (O, O),
                    "execute if score #ld %s matches 1 if score #since %s matches ..2 run return 0" % (O, O),
                    "execute if score #ld %s matches 0 run return run function %s/job/reject" % (O, P),
                    "function %s/job/judge with storage rpg:town m" % P,
                    "execute if score #ok %s matches 1 run return run function %s/job/accept" % (O, P),
                    "function %s/job/reject" % P])
    pts = [(-40, -40), (40, -40), (-40, 40), (40, 40), (0, 0)]
    fn("job/loaded", ["scoreboard players set #ld %s 1" % O] + [
        "$execute in minecraft:overworld unless loaded %s 0 %s run scoreboard players set #ld %s 0" % (rel("$(x)", dx), rel("$(z)", dz), O) for dx, dz in pts])
    judge = ["# 判断候选点（用户 2026-11-28：小镇只建在完全平坦的地方）：九点都是危险 I–II 的群系，5×5 取样高差不过 %d，不在水上；之后整块削平" % SPREAD,
             "scoreboard players set #ok %s 1" % O, "scoreboard players set #mn %s 9999" % O, "scoreboard players set #mx %s -9999" % O]
    for dx in (-40, 0, 40):
        for dz in (-40, 0, 40):
            judge.append("$execute in minecraft:overworld positioned %s 80 %s run function %s/s/bio" % (rel("$(x)", dx), rel("$(z)", dz), P))
    judge.append("execute if score #ok %s matches 0 run return 0" % O)
    for dx in (-40, -20, 0, 20, 40):
        for dz in (-40, -20, 0, 20, 40):
            judge.append("$execute in minecraft:overworld positioned %s 0 %s positioned over motion_blocking_no_leaves run function %s/s/mm" % (rel("$(x)", dx), rel("$(z)", dz), P))
    judge += ["scoreboard players operation #sp %s = #mx %s" % (O, O), "scoreboard players operation #sp %s -= #mn %s" % (O, O),
              "execute if score #sp %s matches %d.. run scoreboard players set #ok %s 0" % (O, SPREAD + 1, O),
              "execute if score #mn %s matches ..62 run scoreboard players set #ok %s 0" % (O, O),
              "scoreboard players set #v %s 0" % O,
              "$execute in minecraft:overworld positioned $(x) 80 $(z) if biome ~ ~ ~ #rpg:town_snow run scoreboard players set #v %s 1" % O,
              "$execute in minecraft:overworld positioned $(x) 80 $(z) if biome ~ ~ ~ #rpg:town_desert run scoreboard players set #v %s 2" % O]
    fn("job/judge", judge)
    fn("s/bio", ["# 这一点的群系合不合适（positioned 那一点；#lmk 0 是城镇，1–3 是地标）",
                 "execute if score #lmk %s matches 0 unless biome ~ ~ ~ #rpg:town_ok run scoreboard players set #ok %s 0" % (O, O)] +
       ["execute if score #lmk %s matches %d if score #relax %s matches 0 unless biome ~ ~ ~ #rpg:lm_%d run scoreboard players set #ok %s 0" % (O, k, O, k, O) for k in LM_BIOMES] +
       ["execute if score #lmk %s matches %d if score #relax %s matches 1.. unless biome ~ ~ ~ #rpg:lm_%d unless biome ~ ~ ~ #rpg:town_relaxed run scoreboard players set #ok %s 0" % (O, k, O, k, O) for k in LM_BIOMES])
    fn("s/mm", ["# 取样（positioned 在地表上一格）：水和岩浆不行；树干、树叶不算",
                "execute if block ~ ~-1 ~ #rpg:town_wet run return run scoreboard players set #ok %s 0" % O,
                "execute if block ~ ~-1 ~ #rpg:town_clear run return 0",
                "execute summon minecraft:marker run function %s/s/mm2" % P])
    fn("s/mm2", ["execute store result score #s %s run data get entity @s Pos[1]" % O,
                 "scoreboard players operation #mn %s < #s %s" % (O, O), "scoreboard players operation #mx %s > #s %s" % (O, O), "kill @s"])
    fn("s/max", ["execute summon minecraft:marker run function %s/s/max2" % P])
    fn("s/max2", ["execute store result score #s %s run data get entity @s Pos[1]" % O, "scoreboard players operation #hm %s > #s %s" % (O, O), "kill @s"])
    fn("job/reject", ["function %s/job/fl_rem with storage rpg:town m" % P, "scoreboard players set #cool %s 3" % O,
                      "scoreboard players add #c %s 1" % O, "scoreboard players set #ph %s 0" % O,
                      "execute if score #c %s matches %d.. run function %s/job/give_up" % (O, len(OFFS), P)])
    fn("job/relax", ["scoreboard players set #relax %s 1" % O, "scoreboard players set #c %s 0" % O, "scoreboard players set #ph %s 0" % O])
    fn("job/give_up", ["# 实在找不到：这座镇不建（以它为故乡的人改去同国的另一座）",
                       "# 地标第一轮按群系找不到：放宽群系、不再要求湖边有水，再找一轮",
                       "execute if score #lmk %s matches 1.. if score #relax %s matches 0 run return run function %s/job/relax" % (O, O, P)] +
       ["execute if score #cur %s matches %d run scoreboard players set #s%d %s 4" % (O, i, i, O) for i in info] +
       ["scoreboard players set #cur %s 0" % O, "function %s/home/poll_all" % P])
    acc = ["# 选中：记下坐标，把整座镇的范围 forceload 上，等区块到齐再建",
           "function %s/job/fl_rem with storage rpg:town m" % P,
           "scoreboard players operation #h0 %s = #mn %s" % (O, O), "scoreboard players operation #h0 %s += #mx %s" % (O, O),
           "scoreboard players operation #h0 %s /= #2 %s" % (O, O)]
    for i in info:
        acc += ["execute if score #cur %s matches %d run scoreboard players operation #x%d %s = #px %s" % (O, i, i, O, O),
                "execute if score #cur %s matches %d run scoreboard players operation #z%d %s = #pz %s" % (O, i, i, O, O),
                "execute if score #cur %s matches %d run scoreboard players operation #v%d %s = #v %s" % (O, i, i, O, O),
                "execute if score #cur %s matches %d run scoreboard players set #r %s %d" % (O, i, O, info[i]["R"] + 4)]
    acc += ["function %s/job/bigcoords" % P, "function %s/job/big_add with storage rpg:town m" % P, "scoreboard players set #wt %s 0" % O, "scoreboard players set #ph %s 2" % O,
            ] + ["execute if score #cur %s matches %d run scoreboard players set #s%d %s 2" % (O, i, i, O) for i in info]
    fn("job/accept", acc)
    wide = ["# 整块町地（±96）：九点群系都得是危险 I–II，5×5 取样高差不过 %d" % WIDE,
            "scoreboard players set #ok %s 1" % O, "scoreboard players set #mn %s 9999" % O, "scoreboard players set #mx %s -9999" % O]
    for dx in (-96, 0, 96):
        for dz in (-96, 0, 96):
            wide.append("$execute in minecraft:overworld positioned %s 80 %s run function %s/s/bio" % (rel("$(x)", dx), rel("$(z)", dz), P))
    for dx in (-96, -48, 0, 48, 96):
        for dz in (-96, -48, 0, 48, 96):
            wide.append("$execute in minecraft:overworld positioned %s 0 %s positioned over motion_blocking_no_leaves run function %s/s/mm" % (rel("$(x)", dx), rel("$(z)", dz), P))
    wide.append("scoreboard players set #wet %s 0" % O)
    for dx, dz in ((128, 0), (-128, 0), (0, 128), (0, -128), (90, 90), (-90, 90), (90, -90), (-90, -90)):
        wide.append("$execute if score #lmk %s matches 3 in minecraft:overworld positioned %s 80 %s if biome ~ ~ ~ #rpg:lm_water run scoreboard players set #wet %s 1"
                    % (O, rel("$(x)", dx), rel("$(z)", dz), O))
    wide.append("execute if score #lmk %s matches 3 if score #relax %s matches 0 if score #wet %s matches 0 run scoreboard players set #ok %s 0" % (O, O, O, O))
    wide += ["scoreboard players operation #sp %s = #mx %s" % (O, O), "scoreboard players operation #sp %s -= #mn %s" % (O, O),
             "execute if score #sp %s matches %d.. run scoreboard players set #ok %s 0" % (O, WIDE + 1, O),
             "execute if score #mn %s matches ..62 run scoreboard players set #ok %s 0" % (O, O),
             "execute if score #ok %s matches 1 run scoreboard players operation #h0 %s = #mn %s" % (O, O, O),
             "execute if score #ok %s matches 1 run scoreboard players operation #h0 %s += #mx %s" % (O, O, O),
             "execute if score #ok %s matches 1 run scoreboard players operation #h0 %s /= #2 %s" % (O, O, O)]
    fn("job/wide", wide)
    fn("job/wide_fail", ["# 整块不够平：放掉这块，接着找", "function %s/job/big_rem with storage rpg:town m" % P] +
       ["execute if score #cur %s matches %d run scoreboard players set #s%d %s 1" % (O, i, i, O) for i in info] +
       ["scoreboard players add #c %s 1" % O, "scoreboard players set #ph %s 0" % O,
        "execute if score #c %s matches %d.. run function %s/job/give_up" % (O, len(OFFS), P)])
    fn("job/big_add", ["$execute in minecraft:overworld run forceload add %s" % b for b in bigbox()])
    fn("job/big_rem", ["$execute in minecraft:overworld run forceload remove %s" % b for b in bigbox()])
    fn("job/wait_build", ["scoreboard players add #wt %s 1" % O,
                          "function %s/job/big_loaded with storage rpg:town m" % P,
                          "execute if score #ld %s matches 0 if score #wt %s matches ..90 run return 0" % (O, O),
                          "function %s/job/wide with storage rpg:town m" % P,
                          "execute if score #ok %s matches 0 run return run function %s/job/wide_fail" % (O, P),
                          "function %s/job/build" % P])
    fn("job/big_loaded", ["scoreboard players set #ld %s 1" % O] + [
        "$execute in minecraft:overworld unless loaded %s 0 %s run scoreboard players set #ld %s 0" % (rel2("$(x)", sx), rel2("$(z)", sz), O)
        for sx in (-1, 0, 1) for sz in (-1, 0, 1)])
    b = ["# 区块到齐：建（positioned 镇中心）",
         "execute store result storage rpg:town m.h int 1 run scoreboard players get #h0 %s" % O,
         "execute store result storage rpg:town m.var int 1 run scoreboard players get #v %s" % O,
         'data modify storage rpg:town m.sfx set value ""',
         'execute if score #v %s matches 1 run data modify storage rpg:town m.sfx set value "_snow"' % O,
         'execute if score #v %s matches 2 run data modify storage rpg:town m.sfx set value "_desert"' % O]
    for i in info:
        b.append("execute if score #cur %s matches %d run data modify storage rpg:town m.f set value \"t%d\"" % (O, i, i))
    b.append("function %s/job/build_go with storage rpg:town m" % P)
    # 镇上的人要趁镇子的区块还加载着就放（营地阶段会放掉这些区块）
    b += ["scoreboard players operation #built %s = #cur %s" % (O, O), "function #rpg:town_built"]
    # 削平、放建筑时被连带打掉的花草、雪、火把会变成掉落物；数千个掉落物第一次载入时会让 rpg:command/index 撞上每刻命令上限
    b += ["data modify storage rpg:town m.tx set from storage rpg:town m.x", "data modify storage rpg:town m.tz set from storage rpg:town m.z",
          "function %s/job/items with storage rpg:town m" % P]
    b += ["function %s/job/big_rem with storage rpg:town m" % P]
    for i in info:
        if info[i].get("lm"):
            b.append("execute if score #cur %s matches %d run return run function %s/job/done" % (O, i, P))
        a = math.radians((i * 137.5) % 360)
        b.append("execute if score #cur %s matches %d run function %s/job/camp_at {dx:%d,dz:%d}" % (O, i, P, round(CAMP_R[1] * math.cos(a)), round(CAMP_R[1] * math.sin(a))))
    b += ["function %s/job/coords" % P, "function %s/job/fl_add with storage rpg:town m" % P,
          "scoreboard players set #wt %s 0" % O, "scoreboard players set #ph %s 3" % O]
    fn("job/build", b)
    fn("job/camp_at", ["# 营地的中心：镇中心 + 约 200 格（偏移可能是负数，players add 不收负数）",
                       "$scoreboard players set #t %s $(dx)" % O, "scoreboard players operation #px %s += #t %s" % (O, O),
                       "$scoreboard players set #t %s $(dz)" % O, "scoreboard players operation #pz %s += #t %s" % (O, O)])
    fn("job/items", ["$execute in minecraft:overworld positioned $(tx) -64 $(tz) positioned ~-180 ~ ~-180 run kill @e[type=minecraft:item,dx=360,dy=720,dz=360]"])
    fn("job/camp_wait", ["function %s/job/items with storage rpg:town m" % P,
                         "scoreboard players add #wt %s 1" % O,
                         "function %s/job/loaded with storage rpg:town m" % P,
                         "execute if score #ld %s matches 0 if score #wt %s matches ..60 run return 0" % (O, O),
                         "execute if score #ld %s matches 1 run function %s/job/camp_go with storage rpg:town m" % (O, P),
                         "execute if score #ld %s matches 1 run function #rpg:camp_built" % O,
                         "function %s/job/fl_rem with storage rpg:town m" % P,
                         "function %s/job/done" % P])
    fn("job/camp_go", ["$execute in minecraft:overworld positioned $(x) 0 $(z) run function %s/camp/find" % P,
                       "scoreboard players operation @e[type=minecraft:marker,tag=rpg.tw.new] %s_id = #cur %s" % (O, O),
                       "tag @e[type=minecraft:marker,tag=rpg.tw.new] remove rpg.tw.new"])
    done = ["# 这座镇（连同营地）建完"]
    for i in info:
        done.append("execute if score #cur %s matches %d run scoreboard players set #s%d %s 3" % (O, i, i, O))
    done += ["scoreboard players operation #built %s = #cur %s" % (O, O), "scoreboard players set #cur %s 0" % O,
             "function %s/home/poll_all" % P]
    fn("job/done", done)
    fn("job/build_go", ["$execute if score #cur %s matches %d in minecraft:overworld positioned $(x) 0 $(z) run function %s/build/t%d with storage rpg:town m" % (O, i, P, i) for i in info])
    hook_tag_custom("town_built", [])
    hook_tag_custom("camp_built", [])          # 营地放好之后（#built = 镇号，营地区块加载着）
    fn("req", ["# 请求建一座镇（宏 i）：还没动过就排进队列",
               "$execute if score #s$(i) %s matches 0 run scoreboard players set #s$(i) %s 1" % (O, O)])


def pad_fns():
    """町地的公用部分：删掉旧的世界生成町地文件，写地皮标签。每座镇的削平见 plot_fns。
    原本想在世界生成里用结构的地形自适应预留平地，但这片自定义地形的密度函数太大，带地形自适应的结构一生成就把内存吃光（2026-11-28 实测），只好在建镇时做。"""
    for rel_ in ("worldgen/structure/town_pad.json", "worldgen/structure_set/town_pad.json", "worldgen/template_pool/town/pad.json", "structure/town/pad.nbt"):
        q = os.path.join(DP, "data", "rpg", rel_)
        if os.path.exists(q):
            os.remove(q)
    wj("rpg/tags/block/town_regrass.json", {"values": ["minecraft:dirt", "minecraft:stone", "minecraft:deepslate", "minecraft:tuff", "minecraft:andesite",
                                                       "minecraft:diorite", "minecraft:granite", "minecraft:coarse_dirt", "minecraft:gravel", "minecraft:rooted_dirt"]})


def plot_shape(i, rects):
    """町地轮廓（用户 2026-11-28：「这块地应该是不规则的」「边框要更扭曲一点，这样和地形衔接更自然」）：
    起伏的圆盘 ∪ 每栋建筑/广场/墓地外扩 4–20 格；再用一层「扭曲场」把边界整体弯一弯（直边变成自然的弯），
    最后闭运算抹平、填洞，并保证每栋建筑外 2 格都在町地里。网格 PLOT_G 格一块；返回块坐标的长方形列表 (x0, z0, x1, z1)。"""
    import numpy as np
    G = PLOT_G
    n = LIM // G
    seed = i * 101 + 17
    span = lambda q: max(abs(q[0]), abs(q[0] + q[2]), abs(q[1]), abs(q[1] + q[3]))
    ext = max(span(q) for q in rects)
    N2 = 2 * n
    m = np.zeros((N2, N2), bool)
    core = np.zeros((N2, N2), bool)
    for a in range(N2):
        for b in range(N2):
            cx, cz = a - n, b - n
            x, z = cx * G + G / 2.0, cz * G + G / 2.0
            th = math.atan2(z, x)
            f = (0.45 * noise(3 * math.cos(th) + 5, 3 * math.sin(th) + 5, seed, 1) + 0.3 * noise(7 * math.cos(th) + 9, 7 * math.sin(th) + 9, seed + 1, 1)
                 + 0.25 * noise(13 * math.cos(th) + 21, 13 * math.sin(th) + 21, seed + 2, 1))
            if math.hypot(x, z) <= (ext * (0.5 + 0.6 * f) if len(rects) > 1 else ext * 1.2 * (0.8 + 0.6 * f)):
                m[a, b] = True
            mg = 4 + 16 * noise(x, z, seed + 5, 12.0)
            x0, z0, x1, z1 = cx * G, cz * G, cx * G + G - 1, cz * G + G - 1
            for q in rects:
                gx = max(q[0] - x1, 0, x0 - (q[0] + q[2] - 1))
                gz = max(q[1] - z1, 0, z0 - (q[1] + q[3] - 1))
                dd = math.hypot(gx, gz)
                if dd <= 2:
                    core[a, b] = True
                if dd <= mg:
                    m[a, b] = True
    # 扭曲场：每一格去看偏移后那一格（两档噪声：约 22 格的大弯 + 7 格的小弯）
    warped = np.zeros_like(m)
    for a in range(N2):
        for b in range(N2):
            x, z = (a - n) * G, (b - n) * G
            ox = 28 * (noise(x, z, seed + 31, 22.0) - 0.5) + 10 * (noise(x, z, seed + 33, 7.0) - 0.5)
            oz = 28 * (noise(x, z, seed + 32, 22.0) - 0.5) + 10 * (noise(x, z, seed + 34, 7.0) - 0.5)
            sa, sb = a + int(round(ox / G)), b + int(round(oz / G))
            if 0 <= sa < N2 and 0 <= sb < N2:
                warped[a, b] = m[sa, sb]
    m = warped | core
    disk = [(dx, dz) for dx in range(-3, 4) for dz in range(-3, 4) if dx * dx + dz * dz <= 9]

    def dil(v):
        pad = np.pad(v, 4)
        out = np.zeros_like(pad)
        for dx, dz in disk:
            out |= np.roll(np.roll(pad, dx, 0), dz, 1)
        return out[4:-4, 4:-4]
    m = ~dil(~dil(m))                       # 闭运算：填掉建筑之间的豁口
    # 只留和建筑连着的那一块（扭曲可能甩出小岛）
    keep = np.zeros_like(m)
    stack = [tuple(q) for q in np.argwhere(core)]
    while stack:
        a, b = stack.pop()
        if not (0 <= a < N2 and 0 <= b < N2) or keep[a, b] or not m[a, b]:
            continue
        keep[a, b] = True
        stack += [(a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)]
    m = keep
    # 填洞：从外面淹不到的空格都算町地
    seen = np.zeros_like(m)
    stack = [(a, b) for a in range(N2) for b in (0, N2 - 1)] + [(a, b) for b in range(N2) for a in (0, N2 - 1)]
    while stack:
        a, b = stack.pop()
        if not (0 <= a < N2 and 0 <= b < N2) or seen[a, b] or m[a, b]:
            continue
        seen[a, b] = True
        stack += [(a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)]
    m |= ~seen
    cells = {(a - n, b - n) for a, b in zip(*np.nonzero(m))}
    for q in rects:                         # 每栋建筑都得整个落在町地上
        for x in range(q[0], q[0] + q[2]):
            for z in range(q[1], q[1] + q[3]):
                assert (x // G, z // G) in cells, ("plot", i, q)
    return [(x0 * G, z0 * G, x1 * G + G - 1, z1 * G + G - 1) for x0, z0, x1, z1 in rects_of(cells)]


def plot_fills(rs, y0, y1, block, filt=None, pre=""):
    """一组长方形、一段高度的 fill；每条不超过 32768 格。"""
    res = []
    for x0, z0, x1, z1 in rs:
        for x in range(x0, x1 + 1, 128):
            for z in range(z0, z1 + 1, 128):
                xa, za = min(x + 127, x1), min(z + 127, z1)
                h = max(1, 32768 // ((xa - x + 1) * (za - z + 1)))
                for y in range(y0, y1 + 1, h):
                    res.append("%sfill ~%d ~%d ~%d ~%d ~%d ~%d %s%s" % (pre, x, y, z, xa, min(y + h - 1, y1), za, block, (" replace " + filt) if filt else ""))
    return res


def plot_fns(i, rects):
    """削平这座镇的町地（positioned 镇中心、y = 地面上一格）：轮廓不规则；外圈 EDGE 格 1:1 的缓坡。
    D_k = 町地向外扩 k 格（切比雪夫）。第 k 圈：k 格以上削空、-k-2 格以下填土，-k-1 格补草皮（只补空处），k-1 格的裸土石换草皮。
    按层写成 fill，不用逐列 setblock。"""
    base = plot_shape(i, rects)
    D = lambda k: [(x0 - k, z0 - k, x1 + k, z1 + k) for x0, z0, x1, z1 in base]
    out = ["# 削平町地（不规则轮廓，%d 个长方形）：positioned 镇中心、y = 地面上一格" % len(base)]
    out += plot_fills(D(EDGE), EDGE, PAD_H, "minecraft:air")
    for y in range(0, EDGE):
        out += plot_fills(D(y), y, y, "minecraft:air")
    for y in range(-2, -EDGE - 3, -1):
        out += plot_fills(D(-y - 2), y, y, "minecraft:dirt", "#rpg:town_soft")
    out += plot_fills(D(0), -1, -1, "minecraft:grass_block")
    for k in range(1, EDGE + 1):
        out += plot_fills(D(k), -k - 1, -k - 1, "minecraft:grass_block", "#rpg:town_soft")
        out += plot_fills(D(k), k - 1, k - 1, "minecraft:grass_block", "#rpg:town_regrass")
    out.append("# 地皮随群系：雪原换雪、沙漠换沙")
    out += plot_fills(D(EDGE), -EDGE - 1, EDGE, "minecraft:snow_block", "minecraft:grass_block", "execute if score #var %s matches 1 run " % O)
    out += plot_fills(D(EDGE), -EDGE - 1, EDGE, "minecraft:sand", "minecraft:grass_block", "execute if score #var %s matches 2 run " % O)
    fn("pad/t%d" % i, out)
    PLOT_LINES.append((i, len(base), len(out)))


PLOT_LINES = []


def box(x, z, r):
    return "%s %s %s %s" % (rel(x, -r), rel(z, -r), rel(x, r), rel(z, r))


def rel(v, d):
    """宏坐标加常数：forceload/positioned 不支持表达式，所以把偏移放进宏参数之外——这里用 ~ 不行，只能另存。"""
    return "$(%s%s%d)" % (v[2:-1], "p" if d >= 0 else "m", abs(d)) if d else v


def rel2(v, s):
    return "$(%s%s)" % (v[2:-1], {-1: "lo", 0: "", 1: "hi"}[s]) if s else v


def bigbox():
    """整座镇分成四块 forceload（一条命令最多 256 个区块）。"""
    return ["$(x%d) $(z%d) $(x%d) $(z%d)" % (i, j, i + 1, j + 1) for i in range(3) for j in range(3)]


def hook_tag_custom(name, values):
    path = os.path.join(DP, "data", "rpg", "tags", "function", name + ".json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"values": values}, fh, indent=1)


# ============================================================================ 数据包：故乡、标题、安全区
GOLD_NAME = ui.BROADCAST_NAME


def title_fn(t, home):
    if t.get("lm"):
        return ["title @s times 10 50 20", "title @s subtitle " + J(["", T(t["sub"], ui.BROADCAST_BODY), T("  " + ui.fraktur(t["en"]), ui.BROADCAST_GLOSS)]),
                "title @s title " + J(["", T(t["zh"], GOLD_NAME, True)])]
    sub = [T("%s · %s" % (NATIONS[t["nation"]], KIND[t["type"]]), ui.BROADCAST_BODY), T("  " + ui.fraktur(t["en"]), ui.BROADCAST_GLOSS)]
    if home:
        sub = [T("故乡 · ", ui.BROADCAST_HOLY, True)] + sub
    return ["title @s times 10 50 20", "title @s subtitle " + J([""] + sub), "title @s title " + J(["", T(t["zh"], GOLD_NAME, True)])]


def life(info):
    N = sorted(info)
    fn("sec", ["# 每秒：等故乡的人、进镇标题、安全区（rpg:town/load 起的循环）",
               "schedule function %s/sec 20t" % P,
               "execute as @a[tag=rpg.tw.wait] run function %s/home/go" % P,
               "execute as @a[tag=rpg.ob] unless score @s %s_home matches 1.. run function %s/home/early" % (O, P),
               "execute as @a[gamemode=!spectator] at @s run function %s/where" % P,
               "execute as @a[scores={rpg_ob=100..}] unless score @s %s_home matches 1.. run function %s/home/legacy" % (O, P),
               "execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] at @s unless score @s %s_ev matches 1.. run function %s/safe" % (O, P),
               "execute in minecraft:overworld run function %s/lm/wake" % P])
    fn("safe", ["# 镇内不刷敌对怪：外来的普通怪直接送走（副本的怪、骑着模型的首领、友军不动）",
                "execute if entity @s[tag=rpg.tw.lm] run return 0",
                "tp @e[type=#rpg:elite_pool,distance=..72,tag=!rpg.tw.ev,tag=!rpg.ally,predicate=!rpg:town/ridden] ~ -400 ~"])
    fn("lm/fort", ["# 孤堡门前（教廷前哨）：四名站岗的圣卫与一位审判官；恶魔阵营的人靠近就醒",
                   "execute positioned ~4 ~ ~2 run function rpg:tower_guard/summon", "execute positioned ~-4 ~ ~2 run function rpg:tower_guard/summon",
                   "execute positioned ~8 ~ ~4 run function rpg:royal_guard/summon", "execute positioned ~-8 ~ ~4 run function rpg:royal_guard/summon",
                   "execute as @e[tag=rpg.hg,distance=..12] run data merge entity @s {NoAI:1b,PersistenceRequired:1b}",
                   "tag @e[tag=rpg.hg,distance=..12] add rpg.lm.guard",
                   'summon minecraft:vindicator ~ ~ ~3 {Tags:["rpg.te.inq","rpg.lm.guard","rpg.lm.inq"],NoAI:1b,PersistenceRequired:1b,CanPickUpLoot:0b,CustomName:%s,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:160},{id:"minecraft:armor",base:14},{id:"minecraft:attack_damage",base:10}],Health:160f}' % J(T("审判官", "#B8902F", True)),
                   "execute as @e[type=minecraft:vindicator,tag=rpg.lm.inq,distance=..6] at @s run function #rpg:town_dress"])
    fn("lm/wake", ["# 每秒：恶魔阵营的人走近孤堡，站岗的醒过来",
                   "execute as @e[tag=rpg.lm.guard,tag=!rpg.lm.awake] at @s if entity @a[tag=rpg.dm,distance=..20,gamemode=!spectator] run function %s/lm/wake_one" % P])
    fn("lm/wake_one", ["data merge entity @s {NoAI:0b}", "tag @s add rpg.lm.awake",
                       "execute if entity @s[tag=rpg.lm.inq] run tellraw @a[distance=..32] " + J(["", T("〖审判官〗", "#B8902F", True), T(ui.GAP + "孤堡的墙不是为挡恶魔造的，是为挡忘了神的人。", ui.BROADCAST_BODY)])])
    wj("rpg/predicate/town/ridden.json", {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"passenger": {}}})
    where = ["# 进镇标题（as/at 玩家）",
             "scoreboard players set #w %s 0" % O,
             "execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c,distance=..100,limit=1,sort=nearest] run scoreboard players operation #w %s = @s %s_id" % (O, O),
             "execute if score #w %s = @s %s_at run return 0" % (O, O),
             "scoreboard players operation @s %s_at = #w %s" % (O, O),
             "execute if score #w %s matches 0 run return 0" % O,
             "execute if score #w %s = @s %s_home run return run function %s/title_home" % (O, O, P),
             "function %s/title" % P]
    fn("where", where)
    fn("title", ["execute if score #w %s matches %d run return run function %s/ti/%d" % (O, i, P, i) for i in N])
    fn("title_home", ["execute if score #w %s matches %d run return run function %s/ti/h%d" % (O, i, P, i) for i in N])
    for i in N:
        fn("ti/%d" % i, title_fn(info[i], False))
        fn("ti/h%d" % i, title_fn(info[i], True) + ["playsound minecraft:block.bell.use ambient @s ~ ~ ~ 0.6 0.8"])
    # 故乡
    nat = ["# 宏：玩家的国家（rpg:onboard p<id>.nation）→ #nat", '$data modify storage rpg:town n set value "$(nation)"', "scoreboard players set #nat %s -1" % O]
    nat += ['execute if data storage rpg:town {n:"%s"} run scoreboard players set #nat %s %d' % (n, O, k) for k, n in enumerate(NATIONS)]
    fn("home/nation_m", nat)
    fn("home/nation", ["$execute if data storage rpg:onboard p$(id).nation run function %s/home/nation_m with storage rpg:onboard p$(id)" % P])
    pick = ["# 抽故乡（as 玩家）：自己国家的两座镇里随机一座；没有国家就全大陆随机",
            "execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id",
            "scoreboard players set #nat %s -1" % O,
            "function %s/home/nation with storage rpg:onboard tmp" % P,
            "execute store result score #r %s run random value 0..1" % O,
            "scoreboard players operation @s %s_home = #nat %s" % (O, O),
            "scoreboard players add @s %s_home 1" % O,
            "execute if score #r %s matches 1 run scoreboard players add @s %s_home 10" % (O, O),
            "execute if score #nat %s matches -1 store result score @s %s_home run random value 1..%d" % (O, O, len([i for i in N if not info[i].get("lm")]))]
    fn("home/pick", pick)
    fn("home/start", ["# 新手开局结束（as 玩家，原来的「回到出生位置」换成这里）：去故乡（开局里抽到国家时就已经排上队）",
                      "scoreboard players operation @s %s_gm = @s rpg_ob_gm" % O,
                      "execute unless score @s %s_home matches 1.. run function %s/home/pick" % (O, P), "function %s/home/go" % P])
    fn("home/early", ["# 开局里（as 玩家，还没有故乡）：一抽到国家就定下故乡、先排队去建，开局走完时多半已经建好",
                      "function %s/home/pick" % P,
                      "execute if score #nat %s matches -1 run return run scoreboard players reset @s %s_home" % (O, O),
                      "execute store result storage rpg:town h.i int 1 run scoreboard players get @s %s_home" % O,
                      "function %s/req with storage rpg:town h" % P])
    fn("home/go", ["execute store result storage rpg:town h.i int 1 run scoreboard players get @s %s_home" % O,
                   "function %s/home/go_m with storage rpg:town h" % P])
    fn("home/go_m", ["$execute if score #s$(i) %s matches 3 run return run function %s/home/arrive" % (O, P),
                     "$execute if score #s$(i) %s matches 4 run return run function %s/home/other" % (O, P),
                     "$execute if score #s$(i) %s matches 0 run scoreboard players set #s$(i) %s 1" % (O, O),
                     "function %s/home/hold" % P])
    fn("home/other", ["# 这座镇建不起来：换同国的另一座；两座都不行就往后换",
                      "execute if score @s %s_home matches 11.. run return run scoreboard players remove @s %s_home 10" % (O, O),
                      "scoreboard players add @s %s_home 10" % O,
                      "execute store result storage rpg:town h.i int 1 run scoreboard players get @s %s_home" % O,
                      "function %s/home/other_m with storage rpg:town h" % P])
    fn("home/other_m", ["$execute if score #s$(i) %s matches 4 run scoreboard players remove @s %s_home 9" % (O, O),
                        "execute if score @s %s_home matches %d.. run scoreboard players set @s %s_home 1" % (O, len(N) + 1, O)])
    fn("home/hold", ["# 故乡还在建：先在黑幕里等",
                     "execute unless entity @s[tag=rpg.tw.wait] run gamemode spectator @s",
                     "tag @s add rpg.tw.wait",
                     "effect give @s minecraft:blindness infinite 0 true",
                     "title @s actionbar " + J(["", T("正在为你的故乡清出一块平地……", ui.BROADCAST_BODY)])])
    arr = ["# 到故乡（as 玩家）：复活点设在天使像前"]
    for i in N:
        for a in "xyz":
            arr.append("execute if score @s %s_home matches %d store result storage rpg:town h.%s int 1 run scoreboard players get #s%s%d %s" % (O, i, a, a, i, O))
    arr += ["function %s/home/tp with storage rpg:town h" % P,
            "execute if entity @s[tag=rpg.tw.wait] run function %s/home/unhold" % P,
            "scoreboard players operation @s %s_at = @s %s_home" % (O, O),
            "scoreboard players operation #w %s = @s %s_home" % (O, O),
            "function %s/title_home" % P,
            "function #rpg:town_arrive"]
    fn("home/arrive", arr)
    fn("home/tp", ["$execute in minecraft:overworld run tp @s $(x) $(y) $(z)", "$execute in minecraft:overworld run spawnpoint @s $(x) $(y) $(z)"])
    fn("home/unhold", ["tag @s remove rpg.tw.wait", "effect clear @s minecraft:blindness", "gamemode survival @s",
                       "execute if score @s %s_gm matches 1 run gamemode creative @s" % O, "execute if score @s %s_gm matches 2 run gamemode adventure @s" % O])
    fn("home/poll_all", ["execute as @a[tag=rpg.tw.wait] run function %s/home/go" % P])
    fn("home/legacy", ["# 老存档：开局早就走完了，没有故乡 → 按国家分一座，不传送，只告诉一声",
                       "function %s/home/pick" % P,
                       "execute store result storage rpg:town h.i int 1 run scoreboard players get @s %s_home" % O,
                       "function %s/req with storage rpg:town h" % P,
                       "tellraw @s " + J(["", T("〖故乡〗", ui.BROADCAST_HOLY, True), T(ui.GAP + "大陆上建起了城镇。你出生的那一座，在你的国家境内；神父会在那里等你。", ui.BROADCAST_BODY)])])
    hook_tag_custom("town_arrive", [])
    near = ["# 每 5 秒：有人走到某座镇名义位置 700 格内，就排队建它"]
    for i in N:
        near.append("execute if score #s%d %s matches 0 in minecraft:overworld positioned %d 100 %d if entity @a[distance=..700] run scoreboard players set #s%d %s 1"
                    % (i, O, info[i]["x"], info[i]["z"], i, O))
    fn("near", ["schedule function %s/near 100t" % P] + near)


def path_fns():
    # 雪原：踩实的雪（方解石偏灰白，比纯雪暗一点，看得出是路）；沙漠：砂岩与粗土
    mats = {"P": ("dirt_path", "calcite", "sandstone"), "C": ("coarse_dirt", "snow_block", "coarse_dirt"),
            "G": ("gravel", "gravel", "smooth_sandstone"), "M": ("moss_block", "snow_block", "sand")}
    for k, (a, b, c) in mats.items():
        fn("p/%s" % k.lower(), ["# 土径的一格（positioned 地表上一格）：只换地表那一层；#var 0 普通、1 雪原、2 沙漠",
                        "execute unless block ~ ~-1 ~ #rpg:town_pathable run return 0",
                        "execute if block ~ ~ ~ #rpg:town_plant run setblock ~ ~ ~ minecraft:air",
                        "execute if score #var %s matches 1 run return run setblock ~ ~-1 ~ minecraft:%s" % (O, b),
                        "execute if score #var %s matches 2 run return run setblock ~ ~-1 ~ minecraft:%s" % (O, c),
                        "setblock ~ ~-1 ~ minecraft:%s" % a])


def tags():
    plants = ["#minecraft:flowers", "#minecraft:saplings", "minecraft:short_grass", "minecraft:tall_grass", "minecraft:fern", "minecraft:large_fern",
              "minecraft:dead_bush", "minecraft:snow", "minecraft:sweet_berry_bush", "minecraft:moss_carpet", "minecraft:leaf_litter", "minecraft:bush",
              "minecraft:firefly_bush", "minecraft:short_dry_grass", "minecraft:tall_dry_grass", "minecraft:brown_mushroom", "minecraft:red_mushroom",
              "minecraft:glow_lichen", "minecraft:vine", "minecraft:sugar_cane", "minecraft:cactus", "minecraft:cactus_flower", "minecraft:bamboo",
              "minecraft:bamboo_sapling", "minecraft:hanging_roots", "minecraft:pink_petals", "minecraft:wildflowers"]
    wj("rpg/tags/block/town_plant.json", {"values": plants})
    wj("rpg/tags/block/town_clear.json", {"values": [v for v in plants if v != "minecraft:snow"] + ["#minecraft:logs", "#minecraft:leaves", "minecraft:brown_mushroom_block",
                                                     "minecraft:red_mushroom_block", "minecraft:mushroom_stem", "minecraft:bee_nest", "minecraft:cocoa",
                                                     "minecraft:mangrove_roots", "minecraft:pale_moss_carpet", "minecraft:pale_hanging_moss"]})
    wj("rpg/tags/block/town_soft.json", {"values": ["minecraft:air", "minecraft:cave_air", "minecraft:water", "#rpg:town_plant", "#minecraft:leaves"]})
    wj("rpg/tags/block/town_wet.json", {"values": ["minecraft:water", "minecraft:lava", "minecraft:ice", "minecraft:packed_ice", "minecraft:blue_ice",
                                                   "minecraft:seagrass", "minecraft:kelp", "minecraft:kelp_plant"]})
    wj("rpg/tags/block/town_pathable.json", {"values": ["minecraft:grass_block", "minecraft:dirt", "minecraft:coarse_dirt", "minecraft:podzol",
                                                        "minecraft:rooted_dirt", "minecraft:mycelium", "minecraft:moss_block", "minecraft:sand",
                                                        "minecraft:red_sand", "minecraft:snow_block", "minecraft:gravel", "minecraft:mud",
                                                        "minecraft:muddy_mangrove_roots", "minecraft:dirt_path", "minecraft:clay"]})
    ok = ["rpg:plains", "rpg:forest", "rpg:wildfield", "rpg:lavender_forest", "rpg:golden_forest", "rpg:geyser_taiga", "rpg:snowfield", "rpg:desert"]
    wj("rpg/tags/worldgen/biome/town_ok.json", {"values": ok})
    wj("rpg/tags/worldgen/biome/town_relaxed.json", {"values": ok + ["rpg:eroded_desert", "rpg:mesa_valley", "rpg:stone_forest", "rpg:ashwood",
                                                                     "rpg:alpine", "rpg:warped_plateau"]})
    wj("rpg/tags/worldgen/biome/town_snow.json", {"values": ["rpg:snowfield", "rpg:geyser_taiga"]})
    for k, v in LM_BIOMES.items():
        wj("rpg/tags/worldgen/biome/lm_%d.json" % k, {"values": v})
    wj("rpg/tags/worldgen/biome/lm_water.json", {"values": ["rpg:river", "rpg:frozen_river", "rpg:ocean", "rpg:beach", "rpg:snowy_beach"]})
    wj("rpg/tags/worldgen/biome/town_desert.json", {"values": ["rpg:desert", "rpg:eroded_desert", "rpg:mesa_valley"]})


def structs():
    dst = os.path.join(DP, "data", "rpg", "structure", "town")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    n = 0
    for f in os.listdir(STRUCT):
        if f.endswith(".nbt"):
            shutil.copyfile(os.path.join(STRUCT, f), os.path.join(dst, f))
            n += 1
    return n


def patch_onboard():
    p = os.path.join(FUNC, "onboard", "finish.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    old = "function rpg:onboard/back with storage rpg:onboard tmp"
    if old in s:
        s = s.replace(old, "function %s/home/start" % P)
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    assert "%s/home/start" % P in s, "towns: onboard/finish 里找不到回原位那一行"


def spawn_scores(info):
    """建好时把复活点（天使像前，c 标记的位置）存进 #sx<i> #sy<i> #sz<i>。"""
    for i in info:
        p = os.path.join(FUNC, "town", "build", "t%d.mcfunction" % i)
        lines = io.open(p, encoding="utf-8").read().rstrip("\n").split("\n")
        k = next(n for n, l in enumerate(lines) if l.startswith("scoreboard players set @e[type=minecraft:marker,tag=rpg.tw.new]"))
        add = ["execute as @e[type=minecraft:marker,tag=rpg.tw.c,tag=rpg.tw.new,limit=1] store result score #s%s%d %s run data get entity @s Pos[%d]" % (a, i, O, n)
               for n, a in enumerate("xyz")]
        lines[k:k] = add
        io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def main():
    if os.path.isdir(os.path.join(FUNC, "town")):
        shutil.rmtree(os.path.join(FUNC, "town"))
    META = json.load(open(os.path.join(STRUCT, "meta.json"), encoding="utf-8"))
    info = town_fns(META)
    spawn_scores(info)
    job(info)
    life(info)
    path_fns()
    tags()
    n = structs()
    pad_fns()
    patch_onboard()
    hook_tag(DP, "load", P + "/load", False)
    fn("load2", ["schedule function %s/near 100t" % P])
    props = ["pyre", "cage", "grave_a", "grave_b", "candles_a", "candles_b", "cauldron", "bell", "barrel", "crate", "crate_pile", "cart"]
    have = [n for n in props if os.path.exists(os.path.join(FUNC, "town_models", "prop", n + ".mcfunction"))]
    fn("prop", ["# 地下城道具（add_town_models.py 的 rpg:town_models/prop/<名>；构建时还没有的就不放）",
                '$data modify storage rpg:town pn set value "$(n)"'] +
       ['execute if data storage rpg:town {pn:"%s"} run function rpg:town_models/prop/%s' % (n, n) for n in have])
    hook_tag(DP, "load", P + "/load2", False)
    json.dump({str(i): {k: v for k, v in d.items() if k in ("zh", "en", "nation", "type", "x", "z", "R", "cells", "n", "roles", "spawn", "lm", "sub", "key")} for i, d in info.items()},
              open(os.path.join(HERE, "town_ref", "towns.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("towns: 町地长方形/行数 %s；合计 %d 行" % (PLOT_LINES, sum(q[2] for q in PLOT_LINES)))
    print("towns: %d 座镇、%d 个结构、%d 个函数；土径格数 %s" % (len(info), n, COUNT[0], [info[i]["cells"] for i in sorted(info)]))


if __name__ == "__main__":
    main()
