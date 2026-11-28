# -*- coding: utf-8 -*-
"""城镇建筑入库：把用户给的建筑（litematic、schem、整个存档）读成统一的方块网格。

三种来源：
- .litematic（Boulevardier 的作品）
- .schem（Sponge v2 / v3）
- 存档（region/*.mca）：建筑在存档的地形里，按「非自然方块」找出范围再切。

统一的结果：(size, grid)。grid 是 {(x, y, z): (方块名, ((属性, 值), ...))}，只含非空气方块；
另外给出「室内空气」集合：从包围盒外面灌不进去的空气（门窗洞会让室内连通外面，所以只当作参考）。
方块实体和实体不搬（箱子换成本包的掉落表，告示牌、旗帜图案不保留）。

只读输入文件；原始文件不进仓库（见 town_ref/SOURCES.md）。
"""
import glob
import gzip
import io
import os
import struct
import zlib

import add_eden_gate as G

NATURAL = set("""air cave_air void_air water lava stone deepslate granite diorite andesite tuff dirt coarse_dirt rooted_dirt grass_block podzol mycelium
sand red_sand gravel clay sandstone red_sandstone bedrock snow snow_block powder_snow ice packed_ice blue_ice short_grass tall_grass fern large_fern
dead_bush seagrass tall_seagrass kelp kelp_plant sugar_cane lily_pad vine glow_lichen moss_carpet moss_block dandelion poppy azure_bluet oxeye_daisy
cornflower allium blue_orchid orange_tulip red_tulip white_tulip pink_tulip lily_of_the_valley sunflower lilac rose_bush peony sweet_berry_bush
oak_log oak_leaves birch_log birch_leaves spruce_log spruce_leaves jungle_log jungle_leaves acacia_log acacia_leaves dark_oak_log dark_oak_leaves
mangrove_log mangrove_leaves mangrove_roots cherry_log cherry_leaves azalea_leaves flowering_azalea_leaves azalea flowering_azalea pumpkin melon
coal_ore iron_ore copper_ore gold_ore redstone_ore lapis_ore diamond_ore emerald_ore deepslate_coal_ore deepslate_iron_ore deepslate_copper_ore
deepslate_gold_ore deepslate_redstone_ore deepslate_lapis_ore deepslate_diamond_ore deepslate_emerald_ore calcite dripstone_block pointed_dripstone
mud muddy_mangrove_roots bubble_column brown_mushroom red_mushroom pink_petals cactus bamboo terracotta smooth_basalt amethyst_block budding_amethyst
small_amethyst_bud medium_amethyst_bud large_amethyst_bud amethyst_cluster moss_carpet hanging_roots spore_blossom cave_vines cave_vines_plant
big_dripleaf big_dripleaf_stem small_dripleaf leaf_litter bush firefly_bush short_dry_grass tall_dry_grass wildflowers cactus_flower""".split())


# ---- litematic ---------------------------------------------------------------
def from_litematic(path):
    d = G.load(path)
    r = next(iter(d["Regions"].values()))
    sx, sy, sz = (abs(int(r["Size"][a])) for a in "xyz")
    pal, arr = r["BlockStatePalette"], r["BlockStates"]
    bits = max(2, (len(pal) - 1).bit_length())
    names = [(e["Name"], tuple(sorted(e.get("Properties", {}).items()))) for e in pal]
    grid = {}
    mask = (1 << bits) - 1
    for i in range(sx * sy * sz):
        a, s = divmod(i * bits, 64)
        v = arr[a] >> s
        if s + bits > 64:
            v |= arr[a + 1] << (64 - s)
        st = names[v & mask]
        if st[0] in ("minecraft:air", "minecraft:cave_air", "minecraft:void_air"):
            continue
        y, rem = divmod(i, sx * sz)
        z, x = divmod(rem, sx)
        grid[(x, y, z)] = st
    return (sx, sy, sz), grid


# ---- schem（Sponge v2 / v3）--------------------------------------------------
def _varints(data):
    out, v, sh = [], 0, 0
    for b in data:
        b &= 0xFF
        v |= (b & 0x7F) << sh
        if b & 0x80:
            sh += 7
            continue
        out.append(v)
        v, sh = 0, 0
    return out


def _parse_state(s):
    if "[" not in s:
        return s, ()
    n, rest = s.split("[", 1)
    props = tuple(sorted(tuple(kv.split("=", 1)) for kv in rest.rstrip("]").split(",") if kv))
    return n, props


def from_schem(path):
    d = G.load(path)
    d = d.get("Schematic", d)
    W, H, L = d["Width"] & 0xFFFF, d["Height"] & 0xFFFF, d["Length"] & 0xFFFF
    if "Blocks" in d:                       # v3
        pal, data = d["Blocks"]["Palette"], d["Blocks"]["Data"]
    else:                                   # v2
        pal, data = d["Palette"], d["BlockData"]
    inv = {v: _parse_state(k) for k, v in pal.items()}
    grid = {}
    for i, v in enumerate(_varints(data)):
        st = inv[v]
        if st[0] in ("minecraft:air", "minecraft:cave_air", "minecraft:void_air"):
            continue
        y, rem = divmod(i, W * L)
        z, x = divmod(rem, W)
        grid[(x, y, z)] = st
    return (W, H, L), grid


# ---- 存档 ----------------------------------------------------------------------
def _nbt(b, i, t):
    if t == 1:
        return struct.unpack_from(">b", b, i)[0], i + 1
    if t == 2:
        return struct.unpack_from(">h", b, i)[0], i + 2
    if t == 3:
        return struct.unpack_from(">i", b, i)[0], i + 4
    if t == 4:
        return struct.unpack_from(">q", b, i)[0], i + 8
    if t == 5:
        return struct.unpack_from(">f", b, i)[0], i + 4
    if t == 6:
        return struct.unpack_from(">d", b, i)[0], i + 8
    if t == 7:
        n = struct.unpack_from(">i", b, i)[0]
        return b[i + 4:i + 4 + n], i + 4 + n
    if t == 8:
        n = struct.unpack_from(">H", b, i)[0]
        return b[i + 2:i + 2 + n].decode("utf-8", "replace"), i + 2 + n
    if t == 9:
        et = b[i]
        n = struct.unpack_from(">i", b, i + 1)[0]
        i += 5
        out = []
        for _ in range(n):
            v, i = _nbt(b, i, et)
            out.append(v)
        return out, i
    if t == 10:
        d = {}
        while True:
            tt = b[i]
            i += 1
            if tt == 0:
                return d, i
            n = struct.unpack_from(">H", b, i)[0]
            name = b[i + 2:i + 2 + n].decode("utf-8", "replace")
            i += 2 + n
            d[name], i = _nbt(b, i, tt)
    if t == 11:
        n = struct.unpack_from(">i", b, i)[0]
        return struct.unpack_from(">%di" % n, b, i + 4), i + 4 + 4 * n
    if t == 12:
        n = struct.unpack_from(">i", b, i)[0]
        return struct.unpack_from(">%dq" % n, b, i + 4), i + 4 + 8 * n
    raise ValueError(t)


def level_spawn(save):
    d = G.load(os.path.join(save, "level.dat"))
    data = d.get("Data", d)
    if "spawn" in data and isinstance(data["spawn"], dict) and "pos" in data["spawn"]:
        p = data["spawn"]["pos"]
        return int(p[0]), int(p[2])
    return int(data.get("SpawnX", 0)), int(data.get("SpawnZ", 0))


def iter_chunks(save, cx0, cz0, r):
    """以 (cx0, cz0) 为中心、半径 r 个区块内的区块：yield (cx, cz, 区块 NBT)。"""
    reg = os.path.join(save, "region")
    if not os.path.isdir(reg):
        reg = os.path.join(save, "dimensions", "minecraft", "overworld", "region")
    cache = {}
    for cx in range(cx0 - r, cx0 + r + 1):
        for cz in range(cz0 - r, cz0 + r + 1):
            rx, rz = cx >> 5, cz >> 5
            key = (rx, rz)
            if key not in cache:
                p = os.path.join(reg, "r.%d.%d.mca" % key)
                cache[key] = open(p, "rb").read() if os.path.exists(p) else None
            data = cache[key]
            if not data:
                continue
            k = (cx & 31) + (cz & 31) * 32
            off = int.from_bytes(data[k * 4:k * 4 + 3], "big")
            if not off:
                continue
            n = struct.unpack_from(">i", data, off * 4096)[0]
            comp = data[off * 4096 + 4]
            raw = data[off * 4096 + 5:off * 4096 + 4 + n]
            b = zlib.decompress(raw) if comp == 2 else (gzip.decompress(raw) if comp == 1 else raw)
            root, _ = _nbt(b, 3 + struct.unpack_from(">H", b, 1)[0], 10)
            yield cx, cz, root.get("Level", root)


def _pal_entry(e):
    if isinstance(e, str):
        return _parse_state(e)
    if "" in e and len(e) == 1:               # 新版异构列表：{"": "minecraft:stone"}
        return _parse_state(e[""])
    if "id" in e:                             # 26.x：{id, properties}
        return e["id"], tuple(sorted(e.get("properties", {}).items()))
    return e["Name"], tuple(sorted(e.get("Properties", {}).items()))


def chunk_blocks(chunk):
    """yield (局部 x, 世界 y, 局部 z, (方块名, 属性))，跳过空气。"""
    old = "Sections" in chunk and "sections" not in chunk
    for sec in chunk.get("sections", chunk.get("Sections", [])):
        if old:                               # 1.13–1.17：Palette + BlockStates
            if "Palette" not in sec or "BlockStates" not in sec:
                continue
            bs = {"palette": sec["Palette"], "data": sec["BlockStates"]}
        else:
            bs = sec.get("block_states")
        if not bs:
            continue
        pal = bs["palette"]
        names = [_pal_entry(e) for e in pal]
        sy = sec["Y"] * 16
        if len(pal) == 1:
            if names[0][0].endswith("air"):
                continue
            for i in range(4096):
                y, rem = divmod(i, 256)
                z, x = divmod(rem, 16)
                yield x, sy + y, z, names[0]
            continue
        data = bs["data"]
        bits = max(4, (len(pal) - 1).bit_length())
        per = 64 // bits
        mask = (1 << bits) - 1
        spanning = old and len(data) * 64 == 4096 * bits      # 1.16 以前：位跨 long 连续排
        for i in range(4096):
            if spanning:
                a_, s_ = divmod(i * bits, 64)
                v = (data[a_] & 0xFFFFFFFFFFFFFFFF) >> s_
                if s_ + bits > 64:
                    v |= (data[a_ + 1] & 0xFFFFFFFFFFFFFFFF) << (64 - s_)
                v &= mask
            else:
                w = data[i // per] & 0xFFFFFFFFFFFFFFFF
                v = (w >> ((i % per) * bits)) & mask
            st = names[v]
            if st[0].endswith(":air") or st[0].endswith("cave_air"):
                continue
            y, rem = divmod(i, 256)
            z, x = divmod(rem, 16)
            yield x, sy + y, z, st


def all_chunks(save):
    """存档里所有区块：yield (cx, cz, 区块 NBT)。"""
    reg = os.path.join(save, "region")
    if not os.path.isdir(reg):                # 26.x 起：dimensions/minecraft/overworld/region
        reg = os.path.join(save, "dimensions", "minecraft", "overworld", "region")
    for p in glob.glob(os.path.join(reg, "r.*.mca")):
        rx, rz = (int(v) for v in os.path.basename(p).split(".")[1:3])
        data = open(p, "rb").read()
        if len(data) < 8192:
            continue
        for k in range(1024):
            off = int.from_bytes(data[k * 4:k * 4 + 3], "big")
            if not off:
                continue
            n = struct.unpack_from(">i", data, off * 4096)[0]
            comp = data[off * 4096 + 4]
            raw = data[off * 4096 + 5:off * 4096 + 4 + n]
            try:
                b = zlib.decompress(raw) if comp == 2 else (gzip.decompress(raw) if comp == 1 else raw)
            except Exception:
                continue
            root, _ = _nbt(b, 3 + struct.unpack_from(">H", b, 1)[0], 10)
            yield rx * 32 + (k & 31), rz * 32 + (k >> 5), root.get("Level", root)


def density(save):
    """每个区块里非自然方块的个数：{(cx, cz): n}，以及最低 / 最高 y。"""
    out = {}
    for cx, cz, ch in all_chunks(save):
        n = 0
        for x, y, z, st in chunk_blocks(ch):
            if st[0].split(":")[1] not in NATURAL:
                n += 1
        if n:
            out[(cx, cz)] = n
    return out


def find_build(save, min_per_chunk=30, gap=1):
    """存档里最大的一团建筑：先按区块聚团，再在团里按方块收紧（去掉 0.3% 的离群点）。
    返回 (x0, y0, z0, x1, y1, z1)。"""
    d = density(save)
    seen, best = set(), None
    for c in d:
        if c in seen or d[c] < min_per_chunk:
            continue
        st, cl = [c], []
        seen.add(c)
        while st:
            u = st.pop()
            cl.append(u)
            for dx in range(-gap, gap + 1):
                for dz in range(-gap, gap + 1):
                    v = (u[0] + dx, u[1] + dz)
                    if v in d and v not in seen and d[v] >= min_per_chunk:
                        seen.add(v)
                        st.append(v)
        w = sum(d[q] for q in cl)
        if not best or w > best[0]:
            best = (w, set(cl))
    if not best:
        return None
    cl = best[1]
    xs, ys, zs = [], [], []
    for cx, cz, ch in all_chunks(save):
        if (cx, cz) not in cl:
            continue
        for x, y, z, st in chunk_blocks(ch):
            if st[0].split(":")[1] in NATURAL:
                continue
            xs.append(cx * 16 + x)
            ys.append(y)
            zs.append(cz * 16 + z)
    xs.sort(), ys.sort(), zs.sort()
    q = lambda a, f: a[min(len(a) - 1, max(0, int(len(a) * f)))]
    return (q(xs, 0.003), q(ys, 0.0), q(zs, 0.003), q(xs, 0.997), q(ys, 1.0), q(zs, 0.997))


LINKS = set("""dirt_path farmland wheat carrots potatoes beetroots oak_fence spruce_fence birch_fence dark_oak_fence jungle_fence acacia_fence
mangrove_fence cherry_fence oak_fence_gate spruce_fence_gate birch_fence_gate dark_oak_fence_gate lantern torch wall_torch hay_block
cobblestone_wall mossy_cobblestone_wall stone_brick_wall gravel coarse_dirt""".split())


def components(save, gap=2, min_cols=40, skip=frozenset()):
    """非自然方块按占地列（x, z）分团，空隙不超过 gap 格算连着。
    返回 [(x0, y0, z0, x1, y1, z1, 方块数)]，按方块数从大到小。"""
    cols = {}
    for cx, cz, ch in all_chunks(save):
        for x, y, z, st in chunk_blocks(ch):
            if st[0].split(":")[1] in NATURAL or st[0].split(":")[1] in skip:
                continue
            k = (cx * 16 + x, cz * 16 + z)
            lo, hi, n = cols.get(k, (y, y, 0))
            cols[k] = (min(lo, y), max(hi, y), n + 1)
    seen, out = set(), []
    for c in cols:
        if c in seen:
            continue
        st, cl = [c], []
        seen.add(c)
        while st:
            u = st.pop()
            cl.append(u)
            for dx in range(-gap, gap + 1):
                for dz in range(-gap, gap + 1):
                    v = (u[0] + dx, u[1] + dz)
                    if v in cols and v not in seen:
                        seen.add(v)
                        st.append(v)
        if len(cl) < min_cols:
            continue
        xs = [q[0] for q in cl]
        zs = [q[1] for q in cl]
        out.append((min(xs), min(cols[q][0] for q in cl), min(zs), max(xs), max(cols[q][1] for q in cl), max(zs), sum(cols[q][2] for q in cl)))
    out.sort(key=lambda r: -r[6])
    return out


def scan_save(save, radius=12):
    """出生点附近找「非自然方块」的包围盒。返回 (x0, y0, z0, x1, y1, z1, 个数)。"""
    sx, sz = level_spawn(save)
    xs, ys, zs, n = [], [], [], 0
    for cx, cz, ch in iter_chunks(save, sx >> 4, sz >> 4, radius):
        for x, y, z, st in chunk_blocks(ch):
            if st[0].split(":")[1] in NATURAL:
                continue
            xs.append(cx * 16 + x)
            ys.append(y)
            zs.append(cz * 16 + z)
            n += 1
    if not n:
        return None
    xs.sort(), ys.sort(), zs.sort()
    q = lambda a, f: a[min(len(a) - 1, max(0, int(len(a) * f)))]
    return (q(xs, 0.002), q(ys, 0.0), q(zs, 0.002), q(xs, 0.998), q(ys, 1.0), q(zs, 0.998), n, (sx, sz))


def from_save(save, box, ground_y=None):
    """按包围盒切出：box = (x0, y0, z0, x1, y1, z1)，世界坐标、含两端。"""
    x0, y0, z0, x1, y1, z1 = box
    grid = {}
    for cx, cz, ch in iter_chunks(save, (x0 + x1) // 32, (z0 + z1) // 32, max(x1 - x0, z1 - z0) // 32 + 2):
        for x, y, z, st in chunk_blocks(ch):
            wx, wz = cx * 16 + x, cz * 16 + z
            if x0 <= wx <= x1 and y0 <= y <= y1 and z0 <= wz <= z1:
                grid[(wx - x0, y - y0, wz - z0)] = st
    return (x1 - x0 + 1, y1 - y0 + 1, z1 - z0 + 1), grid


def from_structure(path):
    """原版结构文件 .nbt（存档里切出来的建筑先存成这个）。"""
    d = G.load(path)
    size = tuple(int(v) for v in d["size"])
    pal = [(e["Name"], tuple(sorted(e.get("Properties", {}).items()))) for e in d["palette"]]
    grid = {}
    for b in d["blocks"]:
        st = pal[b["state"]]
        if st[0].endswith(":air") or st[0].endswith("cave_air"):
            continue
        grid[tuple(int(v) for v in b["pos"])] = st
    return size, grid


def write_structure(path, size, grid):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as g:
        g.write(G.structure(size, grid))
    with open(path, "wb") as fh:
        fh.write(buf.getvalue())


def load_any(path):
    if path.endswith(".nbt"):
        return from_structure(path)
    if path.endswith(".litematic"):
        return from_litematic(path)
    if path.endswith(".schem"):
        return from_schem(path)
    raise ValueError(path)
