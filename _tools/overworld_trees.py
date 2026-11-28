# -*- coding: utf-8 -*-
"""主世界大树：Planet Minecraft 公开树包 → 结构模板 + 按群系的单件拼图结构。

来源（用户确认可用，2026-11-26）：
  treepack1.schem、treepack2.schem —— Planet Minecraft 公开树包
  27-castanopsis-tree-ferns-spruces-trees-bundle-by-mine67.schem —— Planet Minecraft，作者 mine67
署名写在 _tools/tree_ref/CREDITS.md。

两步：
  python overworld_trees.py extract SCHEM...   一次性：去展台底座、按 3D 连通拆树、树叶改 persistent、
                                              树干向下补 EXT 格（坡地不悬空），写 _tools/tree_ref/*.nbt + index.json
  write(g)（overworld_world.write 调用）       把模板拷进数据包，写模板池 / 结构 / 结构集
extract 需要 numpy + scipy；write 只用标准库。
"""
import io, json, os, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "tree_ref")
sys.path.insert(0, os.path.join(HERE, "fortress_ref"))
import nbt  # noqa: E402

NS = "rpg"
DATA_VERSION = 4671
EXT = 3                      # 树干向下补的格数
BASE = ("concrete", "wool", "terracotta", "stained_glass", "prismarine", "glass")
TREEISH = ("log", "wood", "leaves", "fence", "stairs", "slab", "trapdoor", "vine", "button", "gate", "planks", "wall", "nether_brick", "tripwire_hook")
WOODY = ("log", "_wood", "stem", "hyphae")
RENAME = {"minecraft:grass": "minecraft:short_grass"}


# ------------------------------------------------------------------ 提取（一次性）
def _varints(b):
    out, i, n = [], 0, len(b)
    while i < n:
        v = s = 0
        while True:
            x = b[i]; i += 1
            v |= (x & 0x7F) << s; s += 7
            if not x & 0x80: break
        out.append(v)
    return out


def _load(path):
    import numpy as np
    d = nbt.loads(open(path, "rb").read())
    d = d.get("Schematic", d)
    W, H, L = (d[k].value for k in ("Width", "Height", "Length"))
    if "Blocks" in d: pal, data = d["Blocks"]["Palette"], d["Blocks"]["Data"].value
    else: pal, data = d["Palette"], d["BlockData"].value
    inv = {v.value: k for k, v in pal.items()}
    names = [inv.get(i, "minecraft:air") for i in range(max(inv) + 1)]
    raw = bytes(x & 0xFF for x in data) if not isinstance(data, (bytes, bytearray)) else data
    vol = np.array(_varints(raw), np.int32)[:W * H * L].reshape(H, L, W)
    return names, vol


def _parse(state):
    name, props = state, {}
    if "[" in state:
        name, rest = state[:-1].split("[", 1)
        props = dict(kv.split("=", 1) for kv in rest.split(",") if kv)
    name = RENAME.get(name, name)
    if name.endswith("_leaves"): props["persistent"] = "true"
    return name, props


def extract(paths):
    import numpy as np
    from scipy.ndimage import label, binary_dilation
    os.makedirs(REF, exist_ok=True)
    index = []
    for path in paths:
        stem = os.path.splitext(os.path.basename(path))[0]
        src = "castanopsis" if "castanopsis" in stem else stem.split()[0]
        names, vol = _load(path)
        keep = np.array([not any(b in n for b in BASE) and any(t in n.split("[")[0] for t in TREEISH) for n in names])
        woody = np.array([any(t in n.split("[")[0] for t in WOODY) for n in names])
        leafy = np.array(["leaves" in n for n in names])
        trunk = np.array([any(t in n.split("[")[0] for t in WOODY + ("fence", "wall", "nether_brick")) for n in names])
        m = keep[vol]
        lab, n = label(binary_dilation(m, iterations=1), structure=np.ones((3, 3, 3)))
        lab = lab * m
        k_out = 0
        for k in range(1, n + 1):
            sel = lab == k
            cnt = int(sel.sum())
            if cnt < 40 or not (woody[vol][sel].any() or leafy[vol][sel].any()): continue
            ys, zs, xs = np.where(sel)
            sub = np.where(sel, vol, -1)[ys.min():ys.max() + 1, zs.min():zs.max() + 1, xs.min():xs.max() + 1]
            h, l, w = sub.shape
            # 统计
            leaf = {}
            for i in sub[sub >= 0].ravel():
                nm = names[i].split("[")[0].split(":")[1]
                if nm.endswith("_leaves"): leaf[nm] = leaf.get(nm, 0) + 1
            # 底层的木头向下补 EXT 格
            base_y = 0
            base_cells = [(z, x) for z in range(l) for x in range(w) if sub[base_y, z, x] >= 0 and trunk[sub[base_y, z, x]]]
            pal, pal_idx, blocks = [], {}, []
            def idx(state):
                if state not in pal_idx:
                    name, props = _parse(state)
                    e = nbt.Compound(); e["Name"] = nbt.String(name)
                    if props:
                        pc = nbt.Compound()
                        for a, b in sorted(props.items()): pc[a] = nbt.String(b)
                        e["Properties"] = pc
                    pal_idx[state] = len(pal); pal.append(e)
                return pal_idx[state]
            def put(x, y, z, state):
                b = nbt.Compound()
                b["pos"] = nbt.List(nbt.TAG_INT, [nbt.Int(x), nbt.Int(y), nbt.Int(z)])
                b["state"] = nbt.Int(idx(state)); blocks.append(b)
            for (z, x) in base_cells:
                st = names[sub[base_y, z, x]]
                for e_ in range(EXT): put(x, e_, z, st)
            for y in range(h):
                for z in range(l):
                    for x in range(w):
                        i = sub[y, z, x]
                        if i >= 0: put(x, y + EXT, z, names[i])
            root = nbt.Compound()
            root["DataVersion"] = nbt.Int(DATA_VERSION)
            root["size"] = nbt.List(nbt.TAG_INT, [nbt.Int(w), nbt.Int(h + EXT), nbt.Int(l)])
            root["palette"] = nbt.List(nbt.TAG_COMPOUND, pal)
            root["blocks"] = nbt.List(nbt.TAG_COMPOUND, blocks)
            root["entities"] = nbt.List(nbt.TAG_COMPOUND)
            tid = "%s_%02d" % (src, k_out); k_out += 1
            nbt.write_file(os.path.join(REF, tid + ".nbt"), root)
            main_leaf = max(leaf, key=leaf.get) if leaf else ""
            index.append({"id": tid, "src": src, "w": int(w), "h": int(h), "d": int(l), "blocks": cnt, "leaf": main_leaf,
                          "leaf_mix": {a: int(b) for a, b in sorted(leaf.items(), key=lambda kv: -kv[1])}})
    for t in index: t["group"] = classify(t)
    with io.open(os.path.join(REF, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=1)
    return index


def classify(t):
    """按树叶、高度、宽度分组。"""
    leaf, h, w = t["leaf"], t["h"], max(t["w"], t["d"])
    if t["src"] == "castanopsis":
        return "conifer_small" if leaf == "spruce_leaves" else "broad_small"
    if leaf == "spruce_leaves":
        return "redwood" if h >= 50 else "conifer"
    if leaf == "jungle_leaves":
        return "broad_jungle"
    if h >= 50: return "redwood"
    if w >= h * 0.8: return "oak_wide"
    return "oak_tall"


# ------------------------------------------------------------------ 写入数据包：树丛
# 用户 2026-11-26：一律不用原版树，全部从树木包里选；要换叶子就直接换。
# 一棵树一个拼图结构太贵（每次投影地表高度都要新建一个 NoiseChunk），所以构建时把几棵树拼成一个「树丛」模板，
# 一丛只取一次地表高度。树干统一向下补到 EXT_ALL 格，坡地上个别树高出/低于中心几格也看不出来。
EXT_ALL = 6
WOODS = ("dark_oak", "oak", "spruce", "jungle", "birch", "acacia", "mangrove", "cherry")
WOOD_PARTS = ("_log", "_wood", "_planks", "_fence_gate", "_fence", "_slab", "_stairs", "_trapdoor", "_button")


def _swap_wood(name, to):
    """把木头种类换成 to（樱花/白桦/诡异）。诡异：log→stem、wood→hyphae。"""
    base = name.split(":")[1]
    strip = base.startswith("stripped_")
    core = base[9:] if strip else base
    for w in WOODS:
        if core.startswith(w + "_") and any(core.endswith(p) for p in WOOD_PARTS):
            part = core[len(w):]
            if to == "warped":
                part = {"_log": "_stem", "_wood": "_hyphae"}.get(part, part)
            return "minecraft:" + ("stripped_" if strip else "") + to + part
    return name


# 变体：叶子换成什么、木头换成什么
VARIANTS = {
    "as": (None, None),
    "cherry": ("minecraft:cherry_leaves", "cherry"),
    "birch": ("minecraft:birch_leaves", "birch"),
    "yellow": ("minecraft:pale_oak_leaves", None),       # 资源包把苍白橡树叶重绘成金黄色（add_overworld）
    "warped": ("minecraft:warped_wart_block", "warped"),
}

# 群系 → (密度档, 每丛棵数范围, [(分组, 变体, 权重)])
PLAN = {
    "lavender_forest": ("dense", (2, 4), [("broad_jungle", "as", 4), ("oak_wide", "as", 2), ("oak_tall", "as", 2), ("broad_small", "as", 3)]),
    "golden_forest":   ("dense", (2, 4), [("oak_wide", "as", 3), ("oak_tall", "as", 3), ("broad_jungle", "as", 3), ("broad_small", "as", 2), ("redwood", "as", 1)]),
    "geyser_taiga":    ("dense", (3, 5), [("conifer", "as", 5), ("conifer_small", "as", 3), ("redwood", "as", 1)]),
    "forest":          ("dense", (2, 4), [("oak_tall", "as", 3), ("broad_small", "as", 3), ("oak_wide", "as", 2), ("broad_small", "birch", 1), ("redwood", "as", 1)]),
    "wildfield":       ("mid", (1, 3), [("broad_small", "cherry", 2), ("broad_small", "birch", 2), ("broad_small", "as", 2), ("broad_small", "yellow", 2),
                                        ("oak_tall", "cherry", 1), ("oak_tall", "birch", 1), ("oak_tall", "as", 1), ("oak_tall", "yellow", 1)]),
    "stone_forest":    ("mid", (1, 3), [("broad_small", "as", 3), ("broad_jungle", "as", 1)]),
    # 诡异高原的树不特殊处理：原树叶，颜色随群系染（用户 2026-11-27）
    "warped_plateau":  ("mid", (1, 2), [("broad_small", "as", 3), ("conifer_small", "as", 1), ("oak_tall", "as", 1)]),
    "alpine":          ("mid", (1, 2), [("conifer_small", "as", 3), ("conifer", "as", 2)]),
    "plains":          ("sparse", (1, 2), [("oak_wide", "as", 3), ("oak_tall", "as", 1), ("broad_small", "as", 2)]),
    "snowfield":       ("sparse", (1, 2), [("conifer", "as", 2), ("conifer_small", "as", 2)]),
    "sea_cliffs":      ("sparse", (1, 2), [("broad_small", "as", 2), ("oak_wide", "as", 1)]),
}
DENSITY = {"dense": (5, 2, 718201), "mid": (7, 3, 718202), "sparse": (12, 5, 718203)}     # 用户 2026-11-26：稀疏一点，别拥挤
GROVES = 14                  # 每个群系拼几种树丛
START_Y = 1 - EXT_ALL        # 拼图：地表高度 + start_height；原树根那一层落在地面上一格（实测 EXT=3 时 1-EXT 正好）


def _load_tree(tid):
    d = nbt.read_file(os.path.join(REF, tid + ".nbt"))
    pal = []
    for e in d["palette"].value:
        props = {k: v.value for k, v in e["Properties"].items()} if "Properties" in e else {}
        pal.append((e["Name"].value, props))
    blocks = [(tuple(p.value for p in b["pos"].value), b["state"].value) for b in d["blocks"].value]
    size = [v.value for v in d["size"].value]
    return pal, blocks, size


def _state(name, props, variant):
    leaf_to, wood_to = VARIANTS[variant]
    if name.endswith("_leaves") and leaf_to:
        if leaf_to.endswith("_leaves"):
            return leaf_to, {"distance": "1", "persistent": "true", "waterlogged": props.get("waterlogged", "false")}
        return leaf_to, {}
    if wood_to:
        n2 = _swap_wood(name, wood_to)
        if n2 != name:
            props = dict(props)
            if wood_to == "warped": props.pop("waterlogged", None) if n2.endswith(("_stem", "_hyphae")) else None
            return n2, props
    return name, props


def _rot(x, z, w, d, r):
    """绕竖轴转 r×90°，返回新坐标与新尺寸。方向性方块（台阶朝向等）不转——树皮细节看不出来。"""
    if r == 0: return x, z, w, d
    if r == 1: return d - 1 - z, x, d, w
    if r == 2: return w - 1 - x, d - 1 - z, w, d
    return z, w - 1 - x, d, w


def _grove(rng, picks, trees):
    """在方块内放几棵树，树冠半径按 0.7 允许互相交叠。返回 (palette, blocks, size)。"""
    placed, spots = [], []
    for grp, var in picks:
        pal, blocks, (w, h, d) = rng.choice(trees[grp])["data"]
        r = rng.randrange(4)
        rw, rd = (d, w) if r % 2 else (w, d)
        rad = 0.35 * max(rw, rd)
        for _ in range(40):
            cx, cz = rng.uniform(0, 40), rng.uniform(0, 40)
            if all((cx - a) ** 2 + (cz - b) ** 2 >= (rad + c) ** 2 for a, b, c in spots):
                spots.append((cx, cz, rad)); placed.append((pal, blocks, (w, h, d), r, cx - rw / 2.0, cz - rd / 2.0, var)); break
    if not placed: return None
    minx = min(int(round(p[4])) for p in placed); minz = min(int(round(p[5])) for p in placed)
    grid, H = {}, 0
    for pal, blocks, (w, h, d), r, ox, oz, var in placed:
        ox, oz = int(round(ox)) - minx, int(round(oz)) - minz
        add_ext = EXT_ALL - EXT
        H = max(H, h + add_ext)
        bottom = [(p, s) for p, s in blocks if p[1] == 0]
        for (x, y, z), s in blocks + [((p[0], -k, p[2]), s) for p, s in bottom for k in range(1, add_ext + 1)]:
            rx, rz, _, _ = _rot(x, z, w, d, r)
            key = (rx + ox, y + add_ext, rz + oz)
            name, props = _state(*pal[s], var)
            old = grid.get(key)
            if old is None or (old[0].endswith(("_leaves", "wart_block")) and not name.endswith(("_leaves", "wart_block"))):
                grid[key] = (name, props)
    sx = max(k[0] for k in grid) + 1; sz = max(k[2] for k in grid) + 1; sy = max(k[1] for k in grid) + 1
    return grid, (sx, sy, sz)


def _write_nbt(path, grid, size):
    pal, idx, blocks = [], {}, []
    for (x, y, z), (name, props) in sorted(grid.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0])):
        key = (name, tuple(sorted(props.items())))
        if key not in idx:
            e = nbt.Compound(); e["Name"] = nbt.String(name)
            if props:
                pc = nbt.Compound()
                for a, b in sorted(props.items()): pc[a] = nbt.String(b)
                e["Properties"] = pc
            idx[key] = len(pal); pal.append(e)
        b = nbt.Compound()
        b["pos"] = nbt.List(nbt.TAG_INT, [nbt.Int(x), nbt.Int(y), nbt.Int(z)]); b["state"] = nbt.Int(idx[key]); blocks.append(b)
    root = nbt.Compound()
    root["DataVersion"] = nbt.Int(DATA_VERSION)
    root["size"] = nbt.List(nbt.TAG_INT, [nbt.Int(v) for v in size])
    root["palette"] = nbt.List(nbt.TAG_COMPOUND, pal)
    root["blocks"] = nbt.List(nbt.TAG_COMPOUND, blocks)
    root["entities"] = nbt.List(nbt.TAG_COMPOUND)
    nbt.write_file(path, root)


def write(g):
    import random
    with io.open(os.path.join(REF, "index.json"), encoding="utf-8") as fh:
        index = json.load(fh)
    trees = {}
    for t in index:
        t = dict(t); t["data"] = _load_tree(t["id"]); trees.setdefault(t["group"], []).append(t)
    sdir = os.path.join(g.data, NS, "structure", "ow", "groves")
    os.makedirs(sdir, exist_ok=True)
    sets, n = {}, 0
    for biome, (dens, (lo, hi), mix) in PLAN.items():
        rng = random.Random("grove/" + biome)
        weights = [m[2] for m in mix]
        els = []
        for k in range(GROVES):
            picks = [tuple(rng.choices(mix, weights)[0][:2]) for _ in range(rng.randint(lo, hi))]
            res = _grove(rng, picks, trees)
            if not res: continue
            grid, size = res
            name = "%s_%02d" % (biome, k)
            _write_nbt(os.path.join(sdir, name + ".nbt"), grid, size)
            els.append({"weight": 1, "element": {"element_type": "minecraft:single_pool_element", "location": "%s:ow/groves/%s" % (NS, name),
                                                 "projection": "rigid", "processors": "minecraft:empty"}})
            n += 1
        g.w("%s/worldgen/template_pool/ow/groves/%s.json" % (NS, biome), {"fallback": "minecraft:empty", "elements": els})
        g.w("%s/worldgen/structure/ow/grove_%s.json" % (NS, biome), {
            "type": "minecraft:jigsaw", "biomes": ["%s:%s" % (NS, biome)], "step": "surface_structures",
            "terrain_adaptation": "none", "start_pool": "%s:ow/groves/%s" % (NS, biome), "size": 1,
            "start_height": {"absolute": START_Y}, "project_start_to_heightmap": "WORLD_SURFACE_WG",
            "max_distance_from_center": 80, "use_expansion_hack": False, "spawn_overrides": {}})
        sets.setdefault(dens, []).append({"structure": "%s:ow/grove_%s" % (NS, biome), "weight": 1})
    for dens, structs in sets.items():
        sp, se, salt = DENSITY[dens]
        g.w("%s/worldgen/structure_set/ow/groves_%s.json" % (NS, dens), {
            "placement": {"type": "minecraft:random_spread", "salt": salt, "spacing": sp, "separation": se}, "structures": structs})
    return n


def yellow_leaves(rp, jar):
    """苍白橡树叶 → 金黄色（原野的黄叶橡树）。取客户端 jar 里的原版贴图按亮度映射到金黄渐变，保留透明。"""
    import zipfile
    from PIL import Image
    src = "assets/minecraft/textures/block/pale_oak_leaves.png"
    with zipfile.ZipFile(jar) as z:
        im = Image.open(io.BytesIO(z.read(src))).convert("RGBA")
    px = im.load()
    lo, hi = (122, 82, 14), (246, 206, 72)
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g_, b, a = px[x, y]
            if not a: continue
            L = (0.3 * r + 0.59 * g_ + 0.11 * b) / 255.0
            t = min(1.0, max(0.0, (L - 0.25) / 0.6))
            px[x, y] = tuple(int(lo[i] + (hi[i] - lo[i]) * t) for i in range(3)) + (a,)
    out = os.path.join(rp, src)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out)
    return out


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "extract":
        idx = extract(sys.argv[2:])
        from collections import Counter
        print("拆出 %d 棵；分组：%s" % (len(idx), dict(Counter(t["group"] for t in idx))))
        for t in idx: print("  %-16s %-13s 宽%2d 深%2d 高%2d  %s" % (t["id"], t["group"], t["w"], t["d"], t["h"], t["leaf_mix"]))
