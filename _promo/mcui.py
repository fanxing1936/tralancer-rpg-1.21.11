# -*- coding: utf-8 -*-
"""宣传片用的原版 GUI 像素绘制：字形、Tooltip、物品格，跟美术规范（ART-STYLE.md）对齐。

- 拉丁字母用客户端 jar 里的 ascii.png（8×8 位图，1 纹素 = 1 GUI 单位）；
  其余字符（中文、希伯来文等）用原版 Unifont（16×16，1 纹素 = 0.5 GUI 单位）。
- Tooltip 用原版 9 宫格精灵 tooltip/background + tooltip/frame，按原版的外扩 12 单位铺开。
- 颜色一律经 _tools/rpg_ui_style.py 解析（命名色、Hex 都认），不在这里另造。

所有尺寸以「GUI 单位」计，u 是每单位的像素数（必须是偶数，Unifont 纹素才落在整像素上）。
"""
import io
import json
import os
import sys
import zipfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "_tools"))
import rpg_ui_style as ui  # noqa: E402
from mc_env import GAME, JAR  # noqa: E402

LINE = 10          # 原版 Tooltip 行高（单位）
TITLE_GAP = 2      # 第一行（物品名）下面多空的 2 单位


def rgba(colour, a=255):
    r, g, b = (int(round(c * 255)) for c in ui.rgb(colour))
    return (r, g, b, a)


# ---------------------------------------------------------------- 资源

def _jar():
    return zipfile.ZipFile(JAR)


def _unifont():
    """原版 Unifont：从本机 assets 索引里找 unifont.zip（与 build_combat_prompt_font 同法）。"""
    idx_dir = os.path.join(GAME, "assets", "indexes")
    for name in sorted(os.listdir(idx_dir), reverse=True):
        doc = json.load(io.open(os.path.join(idx_dir, name), encoding="utf-8"))
        obj = doc.get("objects", {}).get("minecraft/font/unifont.zip")
        if not obj:
            continue
        h = obj["hash"]
        with zipfile.ZipFile(os.path.join(GAME, "assets", "objects", h[:2], h)) as z:
            hex_name = next(n for n in z.namelist() if n.endswith(".hex"))
            out = {}
            for line in z.read(hex_name).decode("ascii").splitlines():
                cp, _, bits = line.partition(":")
                out[int(cp, 16)] = bits
            return out
    raise RuntimeError("vanilla unifont.zip not found under %s" % idx_dir)


with _jar() as _z:
    _ASCII = Image.open(io.BytesIO(_z.read("assets/minecraft/textures/font/ascii.png"))).convert("RGBA")
    _TT_BG = Image.open(io.BytesIO(_z.read("assets/minecraft/textures/gui/sprites/tooltip/background.png"))).convert("RGBA")
    _TT_FRAME = Image.open(io.BytesIO(_z.read("assets/minecraft/textures/gui/sprites/tooltip/frame.png"))).convert("RGBA")
    _SLOT = Image.open(io.BytesIO(_z.read("assets/minecraft/textures/gui/sprites/container/slot.png"))).convert("RGBA")
_UNI = _unifont()
_glyph_cache = {}


def _glyph(ch):
    """→ (mask 'L' 图, 纹素/单位比例 1 或 2, 墨迹宽（纹素）)。空格类返回 None 掩码。"""
    if ch in _glyph_cache:
        return _glyph_cache[ch]
    cp = ord(ch)
    res = None
    if cp < 128 and ch != " ":
        cx, cy = cp % 16 * 8, cp // 16 * 8
        cell = _ASCII.crop((cx, cy, cx + 8, cy + 8)).getchannel("A")
        bb = cell.getbbox()
        if bb:
            w = bb[2]                      # 原版按最右墨迹列算宽，左侧留白保留
            res = (cell.crop((0, 0, w, 8)), 1, w)
    elif ch not in " 　":
        bits = _UNI.get(cp)
        if bits:
            width = len(bits) // 4
            rows = [int(bits[i * width // 4:(i + 1) * width // 4], 16) for i in range(16)]
            cols = [x for x in range(width) if any(r >> (width - 1 - x) & 1 for r in rows)]
            if cols:
                l, r = cols[0], cols[-1]
                m = Image.new("L", (r - l + 1, 16), 0)
                for yy, row in enumerate(rows):
                    for xx in range(l, r + 1):
                        if row >> (width - 1 - xx) & 1:
                            m.putpixel((xx - l, yy), 255)
                res = (m, 2, r - l + 1)
    _glyph_cache[ch] = res
    return res


def _space(ch):
    return 8 if ch == "　" else 4      # 全角空格 8 单位，半角 4 单位


# ---------------------------------------------------------------- 文字

def measure(runs, u):
    """runs: [(text, colour, bold), ...] → 像素宽。"""
    w = 0
    for text, _c, bold in runs:
        for ch in text:
            g = _glyph(ch)
            if g is None:
                w += _space(ch) * u
                continue
            mask, k, ink = g
            w += ink * u // k + u + ((u // k) if bold else 0)
    return w


def draw_runs(img, x, y, runs, u, shadow=True, alpha=255):
    """在 img 上按原版规则画一行：阴影 = 本色 /4、偏移 1 单位；粗体 = 右移 1 纹素再描一遍。"""
    for pass_ in ((0, 1) if shadow else (1,)):
        px = x
        for text, colour, bold in runs:
            base = rgba(colour, alpha)
            col = base if pass_ else (base[0] // 4, base[1] // 4, base[2] // 4, alpha)
            off = 0 if pass_ else u
            for ch in text:
                g = _glyph(ch)
                if g is None:
                    px += _space(ch) * u
                    continue
                mask, k, ink = g
                t = u // k                    # 每纹素像素数
                m = mask.resize((mask.width * t, mask.height * t), Image.NEAREST)
                layer = Image.new("RGBA", m.size, col)
                gy = y + off + (0 if k == 2 else 0)
                for b in ((0, t) if bold else (0,)):
                    img.paste(layer, (px + off + b, gy), m)
                px += ink * t + u + (t if bold else 0)
    return x + measure(runs, u)


def text(runs, u, shadow=True):
    """单行文字 → 紧凑 RGBA 图层（含阴影）。runs 也可直接给 (text, colour[, bold])。"""
    if isinstance(runs, tuple):
        runs = [runs + (False,) if len(runs) == 2 else runs]
    w = measure(runs, u) + u
    h = 8 * u + u
    img = Image.new("RGBA", (max(1, w), h), (0, 0, 0, 0))
    draw_runs(img, 0, 0, runs, u, shadow)
    return img


# ---------------------------------------------------------------- 文本组件（物品名与 Lore）

def component_runs(node, inherit=None):
    """原版 JSON 文本组件（已解析成 Python 结构）→ runs。只认 text/color/bold/extra。"""
    inherit = inherit or {"color": "white", "bold": False}
    out = []
    if isinstance(node, str):
        if node:
            out.append((node, inherit["color"], inherit["bold"]))
    elif isinstance(node, list):
        if node:
            head = node[0]
            style = dict(inherit)
            if isinstance(head, dict):
                style.update({k: head[k] for k in ("color", "bold") if k in head})
            out += component_runs(head, inherit)
            for n in node[1:]:
                out += component_runs(n, style)
    elif isinstance(node, dict):
        style = dict(inherit)
        style.update({k: node[k] for k in ("color", "bold") if k in node})
        if node.get("text"):
            out.append((node["text"], style["color"], bool(style["bold"])))
        for n in node.get("extra", []):
            out += component_runs(n, style)
    return out


# ---------------------------------------------------------------- Tooltip 与物品格

def _nine(src, border, w, h, u):
    """9 宫格放大：角块与边框按 u 倍最近邻放大，中段拉伸。"""
    sw, sh = src.size
    out = Image.new("RGBA", (w * u, h * u), (0, 0, 0, 0))
    xs = [(0, border, 0, border), (border, sw - border, border, w - border), (sw - border, sw, w - border, w)]
    ys = [(0, border, 0, border), (border, sh - border, border, h - border), (sh - border, sh, h - border, h)]
    for sx0, sx1, dx0, dx1 in xs:
        for sy0, sy1, dy0, dy1 in ys:
            if dx1 <= dx0 or dy1 <= dy0:
                continue
            piece = src.crop((sx0, sy0, sx1, sy1)).resize(((dx1 - dx0) * u, (dy1 - dy0) * u), Image.NEAREST)
            out.alpha_composite(piece, (dx0 * u, dy0 * u))
    return out


def panel(w, h, u):
    """内容区 w×h 单位的原版 Tooltip（背景 + 紫框），返回图层与内容左上角偏移（像素）。"""
    W, H = w + 24, h + 24                 # 原版：精灵比内容四周各外扩 3+9 单位
    img = _nine(_TT_BG, 9, W, H, u)
    img.alpha_composite(_nine(_TT_FRAME, 10, W, H, u))
    return img, (12 * u, 12 * u)


def tooltip(lines, u, min_w=0, centre=False):
    """lines: 每行一组 runs → 原版样式的 Tooltip 图层。第一行后多空 2 单位。"""
    widths = [measure(r, u) // u for r in lines]
    w = max([min_w] + widths)
    h = LINE * len(lines) - 2 + (TITLE_GAP if len(lines) > 1 else 0)
    img, (ox, oy) = panel(w, h, u)
    y = oy
    for i, runs in enumerate(lines):
        x = ox + ((w - widths[i]) * u // 2 if centre else 0)
        draw_runs(img, x, y, runs, u)
        y += LINE * u + (TITLE_GAP * u if i == 0 else 0)
    return img


def slot(u, item=None):
    """原版 18×18 物品格，item 为 16×16 图标（PIL 图）时居中放进去。"""
    img = _SLOT.resize((18 * u, 18 * u), Image.NEAREST)
    if item is not None:
        ic = item.convert("RGBA").resize((16 * u, 16 * u), Image.NEAREST)
        img.alpha_composite(ic, (u, u))
    return img
