# -*- coding: utf-8 -*-
"""失乐园的建筑：Boulevardier 的大拱门与原始建筑包（gate_ref/*.litematic，用户 2026-11-24 给的）→ 结构 rpg:paradise/*。

    python add_eden_gate.py ../rpg

伊甸之门（eden_gate）：

四面对称的十字亭，中心 (25, *, 25)，亭台地面在 y=4。形状不动，只换两处材质：苔石换泥砖，绿与紫的蛙明灯换成赭黄，
免得和失乐园的泥地、血天打架；亭台底下的空腔填实。

四座河庭（tower_*、house_*）：原样照搬（用户：「用原版灰石」），只把脚下悬空、会掉下来的沙砾与混凝土粉末换成同色实心方块。
"""
import gzip
import io
import os
import struct
import subprocess
import sys

REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gate_ref")
CX, CZ, DECK = 25, 25, 4
DATA_VERSION = 4671
SWAP = {"mossy_cobblestone": "mud_bricks", "mossy_cobblestone_slab": "mud_brick_slab", "mossy_cobblestone_stairs": "mud_brick_stairs",
        "mossy_cobblestone_wall": "mud_brick_wall", "verdant_froglight": "ochre_froglight", "pearlescent_froglight": "ochre_froglight"}

# 原始 litematic 是第三方作品，不进仓库：本地没有时用仓库里已转换好的结构（尺寸记在这里，别处要用）
SIZE = {"eden_gate": (63, 44, 58), "tower_small": (9, 19, 9), "tower_medium": (11, 23, 11), "tower_big": (13, 27, 13), "tower_large": (15, 31, 15),
        "house_small": (13, 7, 15), "house_medium": (20, 11, 23), "house_large": (19, 16, 29)}
TOWERS = ["tower_small", "tower_medium", "tower_big", "tower_large"]
HOUSES = ["house_small", "house_medium", "house_large"]
FALL = {"minecraft:gravel": "minecraft:andesite", "minecraft:light_gray_concrete_powder": "minecraft:light_gray_concrete"}


def load(path):
    b = gzip.open(path, "rb").read()
    pos = [0]

    def rd(f):
        v = struct.unpack_from(">" + f, b, pos[0])
        pos[0] += struct.calcsize(">" + f)
        return v[0]

    def st():
        n = rd("H")
        v = b[pos[0]:pos[0] + n].decode("utf-8", "replace")
        pos[0] += n
        return v

    def val(t):
        if t in (1, 2, 3, 4, 5, 6):
            return rd(" bhiqfd"[t])
        if t == 8:
            return st()
        if t == 9:
            k, n = rd("b"), rd("i")
            return [val(k) for _ in range(n)]
        if t == 10:
            d = {}
            while True:
                k = rd("b")
                if k == 0:
                    return d
                nm = st()
                d[nm] = val(k)
        n, f = rd("i"), {7: "b", 11: "i", 12: "Q"}[t]
        fmt = ">%d%s" % (n, f)
        v = struct.unpack_from(fmt, b, pos[0])
        pos[0] += struct.calcsize(fmt)
        return v

    t = rd("b")
    st()
    return val(t)


def blocks(key="eden_gate"):
    r = next(iter(load(os.path.join(REF, key + ".litematic"))["Regions"].values()))
    sx, sy, sz = (abs(r["Size"][a]) for a in "xyz")
    pal, arr = r["BlockStatePalette"], r["BlockStates"]
    bits = max(2, (len(pal) - 1).bit_length())
    out = {}
    for i in range(sx * sy * sz):
        a, s = divmod(i * bits, 64)
        v = arr[a] >> s
        if s + bits > 64:
            v |= arr[a + 1] << (64 - s)
        e = pal[v & ((1 << bits) - 1)]
        n = e["Name"].split(":")[1]
        if n == "air":
            continue
        y, rem = divmod(i, sx * sz)
        z, x = divmod(rem, sx)
        out[(x, y, z)] = ("minecraft:" + (SWAP.get(n, n) if key == "eden_gate" else n), tuple(sorted(e.get("Properties", {}).items())))
    if key != "eden_gate":
        for (x, y, z), (n, _p) in list(out.items()):
            if n in FALL and y and (x, y - 1, z) not in out:
                out[(x, y, z)] = (FALL[n], ())
                k = y + 1
                while out.get((x, k, z), ("",))[0] in FALL:      # 压在上面的一并换
                    out[(x, k, z)] = (FALL[out[(x, k, z)][0]], ())
                    k += 1
        return (sx, sy, sz), out
    for (x, y, z) in [p for p in out if p[1] == DECK]:
        for k in range(DECK):
            out.setdefault((x, k, z), ("minecraft:mud_bricks", ()))
    return (sx, sy, sz), out


# ---- 结构 NBT（只用到 int / string / list / compound）
def s(v):
    e = v.encode("utf-8")
    return struct.pack(">H", len(e)) + e


def tint(name, v):
    return b"\x03" + s(name) + struct.pack(">i", v)


def tints(name, vs):
    return b"\x09" + s(name) + b"\x03" + struct.pack(">i", len(vs)) + b"".join(struct.pack(">i", v) for v in vs)


def structure(size, grid):
    pal = sorted(set(grid.values()))
    idx = {p: i for i, p in enumerate(pal)}
    out = [b"\x0a" + s(""), tint("DataVersion", DATA_VERSION), tints("size", size),
           b"\x09" + s("palette") + b"\x0a" + struct.pack(">i", len(pal))]
    for n, props in pal:
        out.append(b"\x08" + s("Name") + s(n))
        if props:
            out.append(b"\x0a" + s("Properties") + b"".join(b"\x08" + s(k) + s(v) for k, v in props) + b"\x00")
        out.append(b"\x00")
    out.append(b"\x09" + s("blocks") + b"\x0a" + struct.pack(">i", len(grid)))
    for p in sorted(grid, key=lambda q: (q[1], q[2], q[0])):
        out.append(tints("pos", p) + tint("state", idx[grid[p]]) + b"\x00")
    out.append(b"\x09" + s("entities") + b"\x0a" + struct.pack(">i", 0) + b"\x00")
    return b"".join(out)


def main():
    dp = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
    total = 0
    for key in ["eden_gate"] + TOWERS + HOUSES:
        path = os.path.join(dp, "data", "rpg", "structure", "paradise", key + ".nbt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(os.path.join(REF, key + ".litematic")):
            here = os.path.dirname(REF)
            got = subprocess.run(["git", "show", "HEAD:./../rpg/data/rpg/structure/paradise/%s.nbt" % key], cwd=here, capture_output=True)
            if got.returncode:
                raise SystemExit("paradise structs: 没有 %s.litematic，仓库里也没有转换好的结构" % key)
            with io.open(path, "wb") as fh:
                fh.write(got.stdout)
            continue
        size, grid = blocks(key)
        if size != SIZE[key]:
            raise SystemExit("paradise structs: %s 的尺寸变了 %s" % (key, size))
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as g:
            g.write(structure(size, grid))
        with io.open(path, "wb") as fh:
            fh.write(buf.getvalue())
        total += len(grid)
    print("paradise structs: %d, %d blocks" % (1 + len(TOWERS) + len(HOUSES), total))


if __name__ == "__main__":
    main()
