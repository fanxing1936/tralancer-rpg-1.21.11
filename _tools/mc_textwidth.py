# -*- coding: utf-8 -*-
"""按原版字体算一段文字的像素宽（GUI 像素），给对话框里「左对齐」用。

对话框的文字元素只会居中：每行补一段精确宽度的空白（字体 rpg:pad），所有行一样宽，
居中以后左边就对齐了。

算法照原版：
- 位图字形：宽 = 最右一列非透明像素 + 1，按 height/格高缩放、四舍五入，再 +1；
- unifont（unihex）：(右 - 左 + 1) // 2 + 1，size_overrides 固定左右；
- 空格表里的直接取；粗体每个字形再 +1。
原版字体从客户端 jar 读，unifont 从启动器的资源库读（1.21.11 起不在 jar 里）。
找不到就返回 None，调用方照旧居中。
"""

import glob
import io
import json
import os
import zipfile

from PIL import Image

PAD_FONT = "rpg:pad"
PAD_BITS = [(0xE600 + i, 1 << i) for i in range(9)]         # 1..256 像素
import mc_env

# 资源库：本地实例的（mc_env，可用 RPG_MC_GAME 改）、默认 .minecraft 的
ASSETS = [os.path.join(mc_env.GAME, "assets"), os.path.expanduser("~/AppData/Roaming/.minecraft/assets")]

_W = None


def _jar():
    return mc_env.JAR if os.path.isfile(mc_env.JAR) else None


def _asset(key):
    for root in ASSETS:
        for idx in sorted(glob.glob(os.path.join(root, "indexes", "*.json")), key=os.path.getmtime, reverse=True):
            objs = json.load(io.open(idx, encoding="utf-8")).get("objects", {})
            if key in objs:
                h = objs[key]["hash"]
                p = os.path.join(root, "objects", h[:2], h)
                if os.path.isfile(p):
                    return p
    return None


def _load():
    jar = _jar()
    uj = _asset("minecraft/font/include/unifont.json")
    if not jar or not uj:
        return None
    z = zipfile.ZipFile(jar)
    widths = {" ": 4.0, "\u200c": 0.0}
    inc = json.loads(z.read("assets/minecraft/font/include/default.json"))
    for p in inc["providers"]:
        if p["type"] != "bitmap":
            continue
        ns, path = p["file"].split(":")
        im = Image.open(io.BytesIO(z.read("assets/%s/textures/%s" % (ns, path)))).convert("RGBA")
        rows = p["chars"]
        cw, chh = im.size[0] // len(rows[0]), im.size[1] // len(rows)
        scale = p.get("height", 8) / float(chh)
        a = im.getchannel("A").load()
        for r, line in enumerate(rows):
            for c, chx in enumerate(line):
                if chx == "\u0000" or chx in widths:
                    continue
                w = 0
                for x in range(cw - 1, -1, -1):
                    if any(a[c * cw + x, r * chh + y] for y in range(chh)):
                        w = x + 1
                        break
                widths[chx] = float(int(0.5 + w * scale) + 1)
    # unifont
    uni = json.load(io.open(uj, encoding="utf-8"))
    for p in uni["providers"]:
        if p["type"] != "unihex" or p.get("filter", {}).get("jp"):
            continue
        zp = _asset("minecraft/font/" + p["hex_file"].split(":")[1].split("/")[-1])
        if not zp:
            continue
        over = [(ord(o["from"]), ord(o["to"]), o["left"], o["right"]) for o in p.get("size_overrides", [])]
        zz = zipfile.ZipFile(zp)
        for n in zz.namelist():
            if not n.endswith(".hex"):
                continue
            for line in io.TextIOWrapper(zz.open(n), encoding="ascii"):
                cp, _, bits = line.strip().partition(":")
                if not bits:
                    continue
                ch = chr(int(cp, 16))
                if ch in widths:
                    continue
                k = int(cp, 16)
                o = next(((l, r) for f, t, l, r in over if f <= k <= t), None)
                if o:
                    left, right = o
                else:
                    gw = len(bits) * 4 // 16           # 8 或 16 宽
                    rows = [int(bits[i:i + gw // 4], 16) for i in range(0, len(bits), gw // 4)]
                    acc = 0
                    for v in rows:
                        acc |= v
                    if acc == 0:              # 空白字形（如全角空格）按整格宽
                        left, right = 0, gw - 1
                    else:
                        cols = [x for x in range(gw) if acc >> (gw - 1 - x) & 1]
                        left, right = cols[0], cols[-1]
                widths[ch] = float((right - left + 1) // 2 + 1)
    return widths


def table():
    global _W
    if _W is None:
        _W = _load() or {}
    return _W or None


def width(comps, fonts=None):
    """comps：文字组件（dict / list / str）。fonts：{字体名: {字符: 宽}}，自定义字体用。"""
    t = table()
    if t is None:
        return None
    fonts = fonts or {}
    total = [0.0]

    def walk(c, bold=False, font=None):
        if isinstance(c, str):
            c = {"text": c}
        if isinstance(c, list):
            if not c:
                return
            walk(c[0], bold, font)
            for x in c[1:]:
                walk(x, bold, font)       # 列表里后面的继承第一个的样式（这里只用到粗体与字体，近似为不继承）
            return
        b = c.get("bold", bold)
        f = c.get("font", font)
        tab = fonts.get(f) if f else None
        for chx in c.get("text", ""):
            if chx == "\n":
                continue
            if tab is not None:
                w = tab.get(chx, 0.0)
                total[0] += w + (1 if b and w > 0 else 0)
            else:
                w = t.get(chx, 9.0)
                total[0] += w + (1 if b else 0)
        for x in c.get("extra", []):
            walk(x, b, f)
    walk(comps)
    return total[0]


def pad(px):
    """px 像素的空白（rpg:pad 字体）。"""
    px = max(0, int(round(px)))
    s = "".join(chr(cp) for cp, v in reversed(PAD_BITS) if px & v)
    return {"text": s, "font": PAD_FONT, "bold": False, "italic": False} if s else None


def pad_font():
    return {"providers": [{"type": "space", "advances": {chr(cp): v for cp, v in PAD_BITS}}]}
