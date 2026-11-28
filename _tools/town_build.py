# -*- coding: utf-8 -*-
"""城镇建筑转换（一次性）：town_ref/raw/ 的原件 → town_ref/struct/<键>[_snow|_desert].nbt + meta.json。

原件不进仓库（town_ref/SOURCES.md），转换结果进仓库，构建时由 add_towns.py 拷进数据包。
只做这些事（不改造型）：
- 去掉原地形和展示底板（地面层以下的草、土、沙、苔藓等；barn 的混凝土板、orc_camp 的玻璃板与沙台）和长在上面的花草；
- 室内空气：每一列「最低方块到最高方块之间」的空气写成 air，放下时把地形的小凸起和树挖掉；其余的空气不写，所以不挖地形；
- 记下地基裙边（贴地的那些列）、门的位置、正面朝向；
- 雪原版把木材换成云杉，沙漠版换成金合欢（策划书：只换木材，不改造型）。

python town_build.py            全部转换
python town_build.py folk_house 只转一座
"""
import collections
import json
import os
import sys

import town_intake as T

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "town_ref", "raw")
OUT = os.path.join(HERE, "town_ref", "struct")

# 原件里「地面」那一层的 y：它放在世界地表最上面那一格的高度（门槛下面那层）。看侧视图和门的高度定的。
BASE = {"angel_statue": 1, "barn": 2, "church_glimmerhall": 1, "church_gothic": 2, "church_white": 1, "cottage_1000": 2, "cozy_manor": 3,
        "fisherman_house": 1, "folk_house": 1, "green_house_big": 2, "green_house_medium": 2, "green_house_small": 1, "half_timbered": 1,
        "meadow_house": 1, "medieval_street": 1, "old_fiefdom": 1, "roadside_tavern": 1, "rustic_house": 2, "serene_manor": 4,
        "tutorial_house": 0, "orc_camp": 5, "lone_fort": 1, "castle_nicolae": 1, "lake_mansion": 1,
        **{"survival_%d" % i: 1 for i in range(1, 11)}}
# 展示底板：(方块, 这一层及以下才去掉)
PLATE = {"barn": [("light_gray_concrete", 1)], "orc_camp": [("glass", 0), ("smooth_sandstone", 4), ("suspicious_sand", 4), ("sandstone", 4)]}
GROUND = set("grass_block dirt coarse_dirt rooted_dirt podzol mycelium moss_block sand red_sand snow snow_block powder_snow mud clay gravel".split())
PLANTS = set("""short_grass tall_grass fern large_fern dandelion poppy azure_bluet oxeye_daisy cornflower allium blue_orchid orange_tulip red_tulip
white_tulip pink_tulip lily_of_the_valley sunflower lilac rose_bush peony sweet_berry_bush dead_bush moss_carpet pink_petals leaf_litter bush
firefly_bush short_dry_grass tall_dry_grass wildflowers snow brown_mushroom red_mushroom torchflower wither_rose""".split())
DROP = set("structure_void barrier jigsaw structure_block command_block chain_command_block repeating_command_block spawner trial_spawner vault tnt fire soul_fire".split())
SOLID_OK = ("planks", "_log", "_wood", "bricks", "stone", "cobblestone", "deepslate", "tuff", "andesite", "diorite", "granite", "sandstone",
            "terracotta", "concrete", "mud", "blackstone", "basalt", "calcite", "dirt", "quartz_block", "_tiles")
SOLID_NO = ("stairs", "slab", "wall", "fence", "door", "pane", "glass", "button", "plate", "sign", "torch", "lantern", "carpet", "leaves", "bed", "rail",
            "chain", "bars", "ladder", "_ore", "infested", "stonecutter", "pressure")
WOODS = ("oak", "spruce", "birch", "jungle", "acacia", "dark_oak", "mangrove", "cherry", "pale_oak")
WOOD_PARTS = ("planks", "stairs", "slab", "fence", "fence_gate", "door", "trapdoor", "log", "wood", "button", "pressure_plate", "sign", "wall_sign",
              "hanging_sign", "wall_hanging_sign")
VARIANTS = {"": None, "_snow": "spruce", "_desert": "acacia"}
TOWN_KEYS = ["angel_statue", "barn", "church_glimmerhall", "church_gothic", "church_white", "cottage_1000", "cozy_manor", "fisherman_house", "folk_house",
             "green_house_big", "green_house_medium", "green_house_small", "half_timbered", "meadow_house", "medieval_street", "old_fiefdom",
             "roadside_tavern", "rustic_house", "serene_manor", "tutorial_house", "orc_camp"] + ["survival_%d" % i for i in range(1, 11)]
LANDMARK_KEYS = ["lone_fort", "castle_nicolae", "lake_mansion"]
NO_VARIANT = {"angel_statue", "orc_camp", "lone_fort", "castle_nicolae", "lake_mansion"}


def short(n):
    return n.split(":", 1)[1]


def solid(b):
    return any(t in b for t in SOLID_OK) and not any(t in b for t in SOLID_NO)


SNOW_GROUND = {"grass_block": "snow_block", "moss_block": "snow_block", "podzol": "snow_block", "mycelium": "snow_block", "rooted_dirt": "snow_block",
               "moss_carpet": None, "farmland": "snow_block"}
DESERT_GROUND = {"grass_block": "sand", "moss_block": "sand", "podzol": "coarse_dirt", "mycelium": "sand", "rooted_dirt": "coarse_dirt",
                 "moss_carpet": None, "farmland": "sand"}


def swap_wood(st, to):
    """换木材；地面（草、苔藓、灰化土）和花草也跟着群系换：雪原换雪，沙漠换沙（用户 2026-11-27：地面要和环境同色）。"""
    n, props = st
    b = short(n)
    ground = SNOW_GROUND if to == "spruce" else DESERT_GROUND
    if b in ground:
        return ("minecraft:" + ground[b], ()) if ground[b] else None
    if b in PLANTS or b.endswith("_tulip") or b in ("tall_grass", "large_fern", "fern", "short_grass"):
        return None if to == "spruce" else (("minecraft:dead_bush", ()) if b in ("short_grass", "fern") else None)
    stripped = b.startswith("stripped_")
    core = b[9:] if stripped else b
    for w in sorted(WOODS, key=len, reverse=True):
        if core.startswith(w + "_") and core[len(w) + 1:] in WOOD_PARTS:
            return ("minecraft:" + ("stripped_" if stripped else "") + to + "_" + core[len(w) + 1:], props)
    return st


def convert(key):
    size, grid = T.load_any(os.path.join(RAW, next(f for f in os.listdir(RAW) if f.rsplit(".", 1)[0] == key)))
    base = BASE[key]
    plate = PLATE.get(key, [])
    g = {}
    stripped = set()
    for (x, y, z), st in grid.items():
        b = short(st[0])
        if b in DROP:
            continue
        if y < base and b in GROUND or any(b == p and y <= top for p, top in plate):
            stripped.add((x, z, y))
            continue
        g[(x, y, z)] = st
    for (x, y, z), st in list(g.items()):          # 长在去掉的地面上的花草
        if short(st[0]) in PLANTS and ((x, z, y - 1) in stripped or y <= base):
            del g[(x, y, z)]
    if not g:
        raise SystemExit(key + ": 去完地面什么都没剩")
    ymin = min(p[1] for p in g)
    xs = [p[0] for p in g]
    zs = [p[2] for p in g]
    x0, z0 = min(xs), min(zs)
    g = {(x - x0, y - ymin, z - z0): st for (x, y, z), st in g.items()}
    sx, sy, sz = max(xs) - x0 + 1, max(p[1] for p in g) + 1, max(zs) - z0 + 1
    lift = base - ymin                             # 这一层（新坐标）放在地表上面第一格（positioned over 的高度 h），原点 y = h - lift
    cols = collections.defaultdict(list)
    for (x, y, z) in g:
        cols[(x, z)].append(y)
    air = {}
    for (x, z), ys in cols.items():
        lo, hi = min(ys), max(ys)
        have = set(ys)
        for y in range(lo + 1, hi):
            if y not in have:
                air[(x, y, z)] = ("minecraft:air", ())
    # 地基裙边：最低一格在地面层或以下的列，往下垫到地形
    skirt = {}
    counts = collections.Counter()
    for (x, z), ys in cols.items():
        lo = min(ys)
        b = short(g[(x, lo, z)][0])
        if lo <= lift and b not in PLANTS:
            skirt[(x, z)] = (lo, b if solid(b) else None)
            if solid(b):
                counts[b] += 1
    default = counts.most_common(1)[0][0] if counts else "cobblestone"
    skirt = [[x, z, lo, m or default] for (x, z), (lo, m) in sorted(skirt.items())]
    doors = []
    for (x, y, z), (n, p) in g.items():
        if short(n).endswith("_door") and dict(p).get("half") == "lower" and y <= lift + 3:
            doors.append([x, y, z])
    if doors:
        dy = min(d[1] for d in doors)
        doors = [d for d in doors if d[1] <= dy + 1]
    # 正面：离主门最近的那条边（没有门就用南边 +z）
    if doors:
        mx = sum(d[0] for d in doors) / len(doors)
        mz = sum(d[2] for d in doors) / len(doors)
        front = min((("north", mz), ("south", sz - 1 - mz), ("west", mx), ("east", sx - 1 - mx)), key=lambda t: t[1])[0]
    else:
        front = "south"
    meta = {"size": [sx, sy, sz], "lift": lift, "skirt": skirt, "doors": doors, "front": front, "blocks": len(g), "air": len(air)}
    os.makedirs(OUT, exist_ok=True)
    for suf, to in VARIANTS.items():
        if suf and key in NO_VARIANT:
            continue
        gg = {p: (swap_wood(st, to) if to else st) for p, st in g.items()}
        gg = {p: st for p, st in gg.items() if st is not None}
        gg.update(air)
        T.write_structure(os.path.join(OUT, key + suf + ".nbt"), (sx, sy, sz), gg)
    return meta


def main():
    keys = sys.argv[1:] or TOWN_KEYS + LANDMARK_KEYS
    path = os.path.join(OUT, "meta.json")
    meta = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    for k in keys:
        meta[k] = convert(k)
        m = meta[k]
        print("%-20s %s lift=%d front=%s doors=%d skirt=%d blocks=%d air=%d" % (k, m["size"], m["lift"], m["front"], len(m["doors"]), len(m["skirt"]), m["blocks"], m["air"]))
    json.dump(meta, open(path, "w", encoding="utf-8"), separators=(",", ":"))


if __name__ == "__main__":
    main()
