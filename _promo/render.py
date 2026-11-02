# -*- coding: utf-8 -*-
"""把分镜渲染成成片：动态图形逐帧画、实机镜头从 _promo/raw/ 读，叠字幕，再混配乐。

    python _promo/render.py                 # 全片 → _promo/out/tralancer-promo.mp4
    python _promo/render.py --preview 30    # 只出 30 fps 的快速预览
    python _promo/render.py --still 23.5    # 只出这一秒的单帧 PNG，调画面用

分镜见 storyboard.md。实机镜头文件不在时，对应位置画占位卡，片子照样能出。
依赖：Pillow、numpy、imageio_ffmpeg（自带 ffmpeg）。
"""
import json
import math
import os
import random
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "_tools"))
sys.path.insert(0, HERE)

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1920, 1080
FPS = 60
RAW = os.path.join(HERE, "raw")
BUILD = os.path.join(HERE, "build")
OUT = os.path.join(HERE, "out")
MUSIC = os.path.join(HERE, "assets", "music")
ICONS = os.path.join(BUILD, "icons")

FONTS = r"C:\Windows\Fonts"
INK = (11, 10, 13)
GOLD = (227, 176, 75)
PARCH = (217, 201, 163)
GRAY = (150, 146, 140)
TIER = {  # 与 make_datapack.py 的陈列描边色一致
    "brave": ("勇者", (191, 199, 213)),
    "epic": ("史诗", (178, 107, 255)),
    "legend": ("传说", (242, 179, 61)),
    "DEVIL": ("恶魔", (122, 143, 34)),
    "HOLY": ("神圣", (255, 242, 176)),
}


# ---------------------------------------------------------------- 字体与文字

_font_cache = {}


def font(kind, size):
    key = (kind, size)
    if key not in _font_cache:
        if kind in ("serif", "serif_bold", "serif_black"):
            f = ImageFont.truetype(os.path.join(FONTS, "NotoSerifSC-VF.ttf"), size)
            f.set_variation_by_name({"serif": "Medium", "serif_bold": "Bold",
                                     "serif_black": "Black"}[kind])
        elif kind == "en":
            f = ImageFont.truetype(os.path.join(FONTS, "georgiai.ttf"), size)
        elif kind == "en_caps":
            f = ImageFont.truetype(os.path.join(FONTS, "georgia.ttf"), size)
        elif kind == "hebrew":
            f = ImageFont.truetype(os.path.join(FONTS, "times.ttf"), size)
        else:
            raise KeyError(kind)
        _font_cache[key] = f
    return _font_cache[key]


def text_layer(text, fnt, fill, spacing=0, shadow=True, glow=None):
    """单行文字画成一张 RGBA 小图（带投影/辉光），便于整体淡入和缩放。"""
    if spacing:
        widths = [fnt.getlength(c) for c in text]
        tw = int(sum(widths) + spacing * (len(text) - 1))
    else:
        tw = int(fnt.getlength(text))
    asc, desc = fnt.getmetrics()
    pad = 40
    im = Image.new("RGBA", (tw + pad * 2, asc + desc + pad * 2), (0, 0, 0, 0))

    def draw_into(img, color):
        d = ImageDraw.Draw(img)
        if spacing:
            x = pad
            for c, w in zip(text, widths):
                d.text((x, pad), c, font=fnt, fill=color)
                x += w + spacing
        else:
            d.text((pad, pad), text, font=fnt, fill=color)

    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0))
        draw_into(g, glow + (200,))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)))
    if shadow:
        s = Image.new("RGBA", im.size, (0, 0, 0, 0))
        draw_into(s, (0, 0, 0, 200))
        im.alpha_composite(s.filter(ImageFilter.GaussianBlur(4)), (2, 3))
    top = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw_into(top, fill + (255,) if len(fill) == 3 else fill)
    im.alpha_composite(top)
    return im


_layer_cache = {}


def cached_text(*args, **kw):
    key = (args, tuple(sorted(kw.items())))
    if key not in _layer_cache:
        _layer_cache[key] = text_layer(*args, **kw)
    return _layer_cache[key]


def paste(canvas, layer, cx, cy, alpha=1.0, scale=1.0):
    """把 RGBA 图层按中心点贴上去，alpha 0..1。"""
    if alpha <= 0.003:
        return
    if scale != 1.0:
        w, h = layer.size
        layer = layer.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    if alpha < 1.0:
        layer = layer.copy()
        a = layer.getchannel("A").point(lambda v: int(v * alpha))
        layer.putalpha(a)
    w, h = layer.size
    canvas.alpha_composite(layer, (int(cx - w / 2), int(cy - h / 2)))


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def fade(t, dur, a=0.35, b=0.35):
    return min(ease(t / a) if a else 1.0, ease((dur - t) / b) if b else 1.0)


def icon(path, size):
    im = Image.open(path).convert("RGBA")
    return im.resize((size, size), Image.NEAREST)


# ---------------------------------------------------------------- 背景

_rng = random.Random(7)
DUST = [(_rng.random() * W, _rng.random() * H, _rng.uniform(0.6, 2.4), _rng.uniform(8, 30),
         _rng.random() * 6.28) for _ in range(140)]


def vignette_mask():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return np.clip(1.15 - 0.55 * d ** 2, 0.35, 1.0)[..., None]


VIGNETTE = vignette_mask()


def backdrop(t, tint=(40, 30, 22)):
    """深色底 + 缓慢漂浮的金尘，所有动态图形共用。"""
    base = np.zeros((H, W, 3), np.float32)
    base[:] = INK
    # 中心一团暖色微光
    y, x = np.mgrid[0:H:4, 0:W:4].astype(np.float32)
    glow = np.exp(-(((x - W / 2) / 700) ** 2 + ((y - H / 2) / 420) ** 2))
    glow = np.kron(glow, np.ones((4, 4), np.float32))[:H, :W, None]
    base += glow * np.array(tint, np.float32)
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im)
    for (x0, y0, r, sp, ph) in DUST:
        yy = (y0 - t * sp) % H
        xx = x0 + math.sin(t * 0.4 + ph) * 18
        a = int(70 + 60 * math.sin(t * 1.3 + ph))
        d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=GOLD + (max(0, a),))
    return im


# ---------------------------------------------------------------- 素材

def load_weapons():
    """31 件武器：名字与品质来自物品目录，图标来自图鉴导出的 icons/III_*.png。"""
    from make_datapack import weapons
    idx = json.load(open(os.path.join(ICONS, "index.json"), encoding="utf-8"))
    by_name = {}
    for rec in idx.get("III", []):
        by_name.setdefault(rec["name"], rec["file"])
    out = []
    for tier, name, _item in weapons():
        f = by_name.get(name)
        if f:
            out.append((tier, name, os.path.join(ICONS, f)))
    return out


def icons_of(section, names=None):
    idx = json.load(open(os.path.join(ICONS, "index.json"), encoding="utf-8"))
    recs = idx.get(section, [])
    if names is None:
        return [os.path.join(ICONS, r["file"]) for r in recs]
    found = {}
    for r in recs:
        found.setdefault(r["name"], os.path.join(ICONS, r["file"]))
    return [found[n] for n in names if n in found]


def ensure_icons():
    """从图鉴 HTML 里把物品图标按章节导出（只在 build/icons 不存在时跑）。"""
    if os.path.isfile(os.path.join(ICONS, "index.json")):
        return
    import base64
    html = open(os.path.join(ROOT, "TRALANCER-RPG-图鉴.html"), encoding="utf-8").read()
    secs = [(m.start(), m.group(1)) for m in
            re.finditer(r'<div class="plate-h"><span class="num">([^<]*)</span>', html)]
    secs.append((len(html), "END"))
    os.makedirs(ICONS, exist_ok=True)
    idx = {}
    for (a, num), (b, _) in zip(secs, secs[1:]):
        for i, art in enumerate(re.split(r"(?=<article )", html[a:b])[1:]):
            dn = re.search(r'data-name="([^"]*)"', art)
            sp = re.search(r"base64,([A-Za-z0-9+/=]+)", art)
            if not sp:
                continue
            name = dn.group(1).split()[0] if dn else ""
            fn = "%s_%02d.png" % (num, i)
            with open(os.path.join(ICONS, fn), "wb") as f:
                f.write(base64.b64decode(sp.group(1)))
            idx.setdefault(num, []).append({"name": name, "file": fn})
    json.dump(idx, open(os.path.join(ICONS, "index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- 动态图形

HEBREW = "ארץ השברים"[::-1]   # Pillow 没有 raqm，希伯来文得手动倒序成视觉顺序


def mg_title(t, dur):
    im = backdrop(t)
    a = ease((t - 0.3) / 1.6)
    paste(im, cached_text(HEBREW, font("hebrew", 150), GOLD, glow=(120, 80, 20)),
          W / 2, H / 2 - 60, a, 1.0 + 0.02 * t)
    paste(im, cached_text("ERETZ  HA-SHEVARIM", font("en_caps", 30), PARCH, spacing=6),
          W / 2, H / 2 + 60, ease((t - 1.2) / 1.2) * 0.85)
    paste(im, cached_text("碎 片 之 地", font("serif", 34), GRAY),
          W / 2, H / 2 + 112, ease((t - 1.6) / 1.2) * 0.85)
    return im


CRACKS = []
_r = random.Random(11)
for k in range(9):
    ang = k / 9 * 6.283 + _r.uniform(-0.3, 0.3)
    pts, x, y = [], W / 2 + _r.uniform(-40, 40), H / 2 - 40 + _r.uniform(-20, 20)
    for s in range(14):
        ang += _r.uniform(-0.45, 0.45)
        x += math.cos(ang) * _r.uniform(40, 90)
        y += math.sin(ang) * _r.uniform(30, 70)
        pts.append((x, y))
    CRACKS.append([(W / 2, H / 2 - 40)] + pts)


def mg_shatter(t, dur):
    im = mg_title(t + 4, 99)
    d = ImageDraw.Draw(im)
    grow = ease_out(t / 2.2)
    for path in CRACKS:
        n = max(2, int(len(path) * grow))
        d.line(path[:n], fill=(255, 225, 160, 230), width=3)
    if t > 2.4:   # 碎开：横条错位并下坠
        k = ease((t - 2.4) / 1.4)
        arr = np.array(im)
        bands = 18
        bh = H // bands
        rr = random.Random(5)
        out = np.zeros_like(arr)
        out[..., 3] = 255
        out[..., :3] = INK
        for b in range(bands):
            dx = int(rr.uniform(-160, 160) * k)
            dy = int(rr.uniform(20, 140) * k * k)
            src = arr[b * bh:(b + 1) * bh]
            y0 = b * bh + dy
            if y0 >= H:
                continue
            src = np.roll(src, dx, axis=1)
            h = min(bh, H - y0)
            out[y0:y0 + h] = src[:h]
        im = Image.fromarray(out)
        flash = max(0.0, 1 - (t - 2.4) / 0.35)
        if flash > 0:
            im = Image.blend(im, Image.new("RGBA", im.size, (255, 240, 210, 255)), flash * 0.6)
    return im


def mg_weapons(t, dur, ws):
    im = backdrop(t, tint=(30, 26, 34))
    order = list(TIER)
    rows = [[w for w in ws if w[0] == tier] for tier in order]
    rows = [r for r in rows if r]
    size, gap = 80, 14
    top = H / 2 - (len(rows) * (size + 28)) / 2 + 10
    k = 0
    for ri, row in enumerate(rows):
        tier = row[0][0]
        label, color = TIER[tier]
        y = top + ri * (size + 28)
        row_t = t - 0.15 - ri * 0.45
        paste(im, cached_text(label, font("serif_bold", 40), color),
              360, y + size / 2, ease(row_t / 0.4))
        for i, (_tier, _name, path) in enumerate(row):
            lt = row_t - i * 0.06
            if lt <= 0:
                continue
            p = ease_out(lt / 0.45)
            ic = icon(path, size)
            x = 480 + i * (size + gap) + size / 2
            yy = y + size / 2 - (1 - p) * 60
            glow = Image.new("RGBA", (size + 40, size + 40), (0, 0, 0, 0))
            ImageDraw.Draw(glow).ellipse((6, 6, size + 34, size + 34), fill=color + (70,))
            paste(im, glow.filter(ImageFilter.GaussianBlur(10)), x, yy, p)
            paste(im, ic, x, yy, p)
            k += 1
    return im


def mg_twins(t, dur):
    im = backdrop(t, tint=(44, 36, 18))
    paths = icons_of("III", ["雅斤", "波阿斯"])
    p = ease_out(t / 1.0)
    for i, path in enumerate(paths):
        side = -1 if i == 0 else 1
        x = W / 2 + side * (520 - 340 * p)
        paste(im, icon(path, 240), x, H / 2 - 110, p)
        name = ["雅斤 · Jachin", "波阿斯 · Boaz"][i]
        paste(im, cached_text(name, font("serif_bold", 38), GOLD), x, H / 2 + 40, ease((t - 0.6) / 0.5))
    # 下方一条：符文、符石、磨刀石、冶炼石缓缓滑过
    strip = icons_of("V") + icons_of("VI", ["铸造之石", "传说冶炼石", "冶炼石"])
    sx = W + 40 - t * 260
    for i, path in enumerate(strip):
        x = sx + i * 92
        if -60 < x < W + 60:
            paste(im, icon(path, 64), x, H / 2 + 175, ease((t - 0.4) / 0.6) * 0.9)
    return im


SINS = ["傲慢", "嫉妒", "怠惰", "暴食", "暴怒", "色欲", "贪婪"]


def mg_sins(t, dur):
    im = backdrop(t, tint=(36, 12, 12))
    for i, s in enumerate(SINS):
        lt = t - 0.2 - i * 0.32
        x = W / 2 + (i - 3) * 230
        hi = s == "暴食"
        col = (156, 178, 60) if hi else (200, 70, 60)
        a = ease(lt / 0.25)
        if t > 2.9 and not hi:    # 最后只留下暴食
            a *= 1 - ease((t - 2.9) / 0.6) * 0.75
        sc = 1.0 + (0.25 * ease((t - 2.9) / 0.6) if hi else 0)
        paste(im, cached_text(s, font("serif_black", 92), col, glow=col), x, H / 2 - 30, a, sc)
    return im


PILLARS = [("路西法", (200, 60, 60)), ("利维坦", (27, 120, 180)), ("亚巴顿", (120, 120, 130)),
           ("别西卜", (122, 143, 34)), ("萨麦尔", (190, 40, 70)), ("贝利尔", (170, 70, 210)),
           ("玛门", (215, 160, 40))]
ROLES = ["先锋", "猎手", "司祭", "咒使", "处刑者"]


def mg_servants(t, dur):
    im = backdrop(t, tint=(24, 20, 30))
    d = ImageDraw.Draw(im)
    cw, ch, gx, gy = 190, 84, 16, 14
    x0 = W / 2 - (7 * cw + 6 * gx) / 2
    y0 = H / 2 - (5 * ch + 4 * gy) / 2 + 40
    for c, (lord, col) in enumerate(PILLARS):
        paste(im, cached_text(lord + "柱", font("serif_bold", 32), col),
              x0 + c * (cw + gx) + cw / 2, y0 - 50, ease((t - c * 0.05) / 0.4))
        for r, role in enumerate(ROLES):
            lt = t - 0.3 - (c * 5 + r) * 0.06
            a = ease(lt / 0.3)
            if a <= 0:
                continue
            x = x0 + c * (cw + gx)
            y = y0 + r * (ch + gy)
            fill = tuple(int(v * 0.32) for v in col) + (int(230 * a),)
            d.rounded_rectangle((x, y, x + cw, y + ch), 10, fill=fill,
                                outline=col + (int(255 * a),), width=2)
            paste(im, cached_text(role, font("serif", 30), PARCH, shadow=False),
                  x + cw / 2, y + ch / 2, a)
    return im


def mg_pacts(t, dur):
    im = backdrop(t, tint=(38, 18, 40))
    names = ["lucifer", "leviathan", "abaddon", "beelzebub", "samael", "belial", "mammon"]
    for i, n in enumerate(names):
        lt = t - 0.2 - i * 0.22
        if lt <= 0:
            continue
        p = ease_out(lt / 0.4)
        art = icon(os.path.join(ROOT, "_tools", "pact_art", "pact_%s.png" % n), 176)
        w = max(1, int(176 * p))
        art = art.resize((w, 176), Image.NEAREST)   # 横向翻开
        x = W / 2 + (i - 3) * 230
        paste(im, art, x, H / 2 - 40, min(1.0, p * 1.5))
        paste(im, cached_text(PILLARS[i][0], font("serif", 28), PILLARS[i][1]), x, H / 2 + 80, p)
    return im


SEPH = [(0, 0), (1, 1), (-1, 1), (1, 2.6), (-1, 2.6), (0, 3.4), (1, 4.2), (-1, 4.2), (0, 5.0), (0, 6.2)]
PATHS = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (1, 5), (2, 5), (3, 4), (3, 5), (4, 5), (3, 6),
         (4, 7), (5, 6), (5, 7), (6, 7), (6, 8), (7, 8), (5, 8), (8, 9), (0, 5), (6, 9), (7, 9)]


def draw_tree(im, t, cx, cy, scale, alpha=1.0, color=(213, 150, 242)):
    d = ImageDraw.Draw(im)
    pts = [(cx + x * scale * 1.1, cy + (y - 3.1) * scale) for x, y in SEPH]
    for k, (a, b) in enumerate(PATHS):
        p = ease((t - k * 0.05) / 0.5) * alpha
        if p > 0:
            ax, ay = pts[a]
            bx, by = pts[b]
            d.line((ax, ay, ax + (bx - ax) * p, ay + (by - ay) * p), fill=color + (int(170 * alpha),), width=3)
    for k, (x, y) in enumerate(pts):
        p = ease((t - 0.3 - k * 0.1) / 0.35) * alpha
        if p > 0:
            r = 0.26 * scale
            d.ellipse((x - r, y - r, x + r, y + r), fill=(30, 20, 40, int(255 * p)),
                      outline=GOLD + (int(255 * p),), width=3)


def mg_covenants(t, dur):
    im = backdrop(t, tint=(40, 34, 20))
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw_tree(glow, t + 1, W / 2, H / 2 - 20, 120, 0.35)
    im.alpha_composite(glow)
    old, new = icons_of("XII", ["旧约", "新约"])
    p = ease_out(t / 1.0)
    merge = ease((t - 2.4) / 1.2)
    xo = W / 2 - 360 * (1 - merge) - 0
    xn = W / 2 + 360 * (1 - merge)
    paste(im, icon(old, 220), xo, H / 2 - 60, p * (1 - merge * 0.6))
    paste(im, icon(new, 240), xn, H / 2 - 60, p, 1 + 0.12 * merge)
    paste(im, cached_text("旧约", font("serif_bold", 40), PARCH), W / 2 - 360, H / 2 + 90, p * (1 - merge))
    paste(im, cached_text("新约", font("serif_bold", 40), GOLD), W / 2 + 360, H / 2 + 90, p * (1 - merge))
    if merge > 0:
        f = Image.new("RGBA", im.size, (255, 236, 190, int(110 * max(0, 1 - abs(merge - 0.6) / 0.4))))
        im.alpha_composite(f)
    return im


def mg_title_card(t, dur):
    im = backdrop(t, tint=(50, 36, 18))
    a = ease((t - 0.2) / 1.0)
    paste(im, cached_text("破碎大陆", font("serif_black", 150), GOLD, spacing=24, glow=(140, 90, 20)),
          W / 2, H / 2 - 90, a, 1.06 - 0.06 * ease_out(t / 3))
    paste(im, cached_text("TRALANCER  RPG", font("en_caps", 52), PARCH, spacing=14),
          W / 2, H / 2 + 50, ease((t - 0.8) / 0.8))
    d = ImageDraw.Draw(im)
    ln = 420 * ease((t - 1.0) / 0.8)
    d.line((W / 2 - ln, H / 2 + 105, W / 2 + ln, H / 2 + 105), fill=GOLD + (200,), width=2)
    paste(im, cached_text("Minecraft Java 1.21.11 数据包 + 资源包 · 开源免费", font("serif", 32), PARCH),
          W / 2, H / 2 + 160, ease((t - 1.5) / 0.8))
    paste(im, cached_text("Data pack & resource pack · open source, free", font("en", 26), GRAY),
          W / 2, H / 2 + 205, ease((t - 1.8) / 0.8))
    return im


CREDITS = [
    ("serif_bold", 36, GOLD, "破碎大陆 · TRALANCER RPG"),
    ("serif", 26, PARCH, "世界观设定：仓库作者　·　开源免费，非商业项目"),
    ("serif", 22, GRAY, ""),
    ("serif_bold", 28, PARCH, "配乐 · Music — Minecraft Dungeons Original Soundtrack"),
    ("en", 24, PARCH, "Finnbacka (title screen) · The Tower: Boss — Peter Hont"),
    ("en", 24, PARCH, "Necromancer (Nameless One fight) — Johan Johnson"),
    ("en", 24, PARCH, "The Arch-Illager: Stage 1 — Peter Hont"),
    ("serif", 22, GRAY, ""),
    ("serif", 24, PARCH, "圣卫与别西卜的模型参考、贴图与音效取自 Minecraft Dungeons"),
    ("en", 22, GRAY, "Minecraft Dungeons music, textures and sounds © Mojang Studios."),
    ("en", 22, GRAY, "This is a free, non-commercial fan project, not affiliated with or endorsed by Mojang or Microsoft."),
    ("en", 22, GRAY, "Shot with ReplayMod and Complementary Reimagined shaders."),
]


def mg_credits(t, dur):
    im = backdrop(t, tint=(20, 18, 16))
    y = H / 2 - 260
    for i, (k, s, c, line) in enumerate(CREDITS):
        if line:
            paste(im, cached_text(line, font(k, s), c), W / 2, y, ease((t - 0.1 - i * 0.08) / 0.5))
        y += s + 22
    return im


def mg_placeholder(t, dur, code, title, note):
    im = backdrop(t, tint=(18, 26, 30))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((W / 2 - 560, H / 2 - 200, W / 2 + 560, H / 2 + 120), 18,
                        outline=GRAY + (160,), width=2)
    paste(im, cached_text("实机镜头 %s · 待录制" % code, font("serif_bold", 44), PARCH), W / 2, H / 2 - 120)
    paste(im, cached_text(title, font("serif", 34), GOLD), W / 2, H / 2 - 50)
    paste(im, cached_text(note, font("serif", 24), GRAY), W / 2, H / 2 + 20)
    paste(im, cached_text("_promo/raw/%s" % RAWFILE[code], font("en", 24), GRAY), W / 2, H / 2 + 70)
    return im


# ---------------------------------------------------------------- 实机镜头

RAWFILE = {"S1": "S1_land.mp4", "S2": "S2_armory.mp4", "S3": "S3_guards.mp4",
           "S4a": "S4a_beelzebub.mp4", "S4b": "S4b_feast.mp4", "S5": "S5_tree.mp4"}


def probe_duration(path):
    out = subprocess.run([FFMPEG, "-hide_banner", "-i", path], capture_output=True,
                         text=True, errors="replace").stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0


class Clip:
    """顺序读一段实机素材：取素材中段 dur 秒，缩放裁切到 1920×1080。"""

    def __init__(self, path, dur, fps):
        total = probe_duration(path)
        start = max(0.0, (total - dur) / 2)
        self.proc = subprocess.Popen(
            [FFMPEG, "-v", "error", "-ss", "%.3f" % start, "-i", path, "-t", "%.3f" % (dur + 0.5),
             "-vf", "fps=%d,scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d" % (fps, W, H, W, H),
             "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            stdout=subprocess.PIPE)
        self.last = None

    def frame(self):
        buf = self.proc.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            self.last = Image.frombuffer("RGB", (W, H), buf).convert("RGBA")
        return self.last if self.last is not None else Image.new("RGBA", (W, H), INK + (255,))

    def close(self):
        self.proc.kill()


# ---------------------------------------------------------------- 分镜表

def shots(ws):
    S = []

    def add(start, end, kind, zh=None, en=None, chapter=None, **kw):
        S.append(dict(start=start, end=end, kind=kind, zh=zh, en=en, chapter=chapter, **kw))

    add(0, 4, mg_title, "世界曾经完整。", "The world was once whole.")
    add(4, 8, mg_shatter, "神陨，堕天，权柄分裂。", "Gods fell. Angels fell. Power was torn apart.")
    add(8, 12, "S1", "破碎大陆", "The Shattered Land",
        title="大陆远景", note="黄昏，开光影，高空缓慢推近")
    add(12, 17, lambda t, d: mg_weapons(t, d, ws), "31 件武器 · 五档品质", "31 weapons · five tiers", "壹 · 装备")
    add(17, 22, "S2", "勇者 · 史诗 · 传说 · 恶魔 · 神圣", "Brave · Epic · Legend · Devil · Holy", "壹 · 装备",
        title="武器长廊", note="齐腰高度沿长廊推轨，从勇者推到神圣")
    add(22, 26, mg_twins, "圣殿双柱，双持联动；符文、镶嵌与锻造",
        "Jachin & Boaz in both hands · runes, gems, forging", "壹 · 装备")
    add(26, 30, "S3", "教廷圣卫，借神之名而来", "The Papal Guard marches in God's name", "壹 · 装备",
        title="圣卫方阵", note="低机位正面，圣卫迎着镜头冲来")
    add(30, 34, mg_sins, "七宗罪领主", "Seven Lords of Sin", "贰 · 恶魔生态")
    add(34, 42, "S4a", "别西卜 · 暴食", "Beelzebub · Gluttony", "贰 · 恶魔生态",
        title="别西卜降临", note="降临烟雾，接一个起手招式")
    add(42, 46, mg_servants, "35 名所罗门罪仆，七柱五职",
        "35 servants of Solomon · seven pillars, five roles", "贰 · 恶魔生态")
    add(46, 52, "S4b", "魔化 · 真名调查 · 四阶段驱魔 · 封印遗物",
        "Corruption · True-name inquest · Four-stage exorcism · Sealed relics", "贰 · 恶魔生态",
        title="万蝇饕宴", note="别西卜大招，镜头拉远看清全貌")
    add(52, 56, mg_pacts, "七十二柱罪约", "Pacts of the Seventy-Two Pillars", "叁 · 契约体系")
    add(56, 63, "S5", "卡巴拉生命之树，十源质归位", "The Tree of Life · ten sephirot restored", "叁 · 契约体系",
        title="生命之树", note="夜里，俯视角缓慢环绕粒子阵")
    add(63, 68, mg_covenants, "旧约 · 新约：权与力重新相遇",
        "Old Covenant · New Covenant: power and authority reunited", "叁 · 契约体系")
    add(68, 75, mg_title_card)
    add(75, 82, mg_credits)
    return S


def rec_fallback(code):
    """实机素材缺席时的占位：生命之树镜头用画出来的树代替，其余画占位卡。"""
    if code == "S5":
        def f(t, dur):
            im = backdrop(t, tint=(30, 18, 44))
            draw_tree(im, t, W / 2, H / 2 - 20, 130)
            paste(im, cached_text("（实机镜头 S5 待录制）", font("serif", 24), GRAY), W / 2, 80)
            return im
        return f
    return None


# ---------------------------------------------------------------- 字幕与章节

def overlay_text(im, shot, t):
    dur = shot["end"] - shot["start"]
    if shot["zh"]:
        a = fade(t, dur, 0.3, 0.3)
        paste(im, cached_text(shot["zh"], font("serif_bold", 50), PARCH), W / 2, H - 150, a)
        if shot["en"]:
            paste(im, cached_text(shot["en"], font("en", 28), GRAY), W / 2, H - 92, a * 0.95)
    if shot["chapter"]:
        paste(im, cached_text(shot["chapter"], font("serif_bold", 30), GOLD), 200, 90)


# ---------------------------------------------------------------- 主流程

def render(fps, out, still=None):
    ensure_icons()
    ws = load_weapons()
    assert len(ws) == 31, "武器图标只对上 %d 件" % len(ws)
    plan = shots(ws)
    total = plan[-1]["end"]
    clips = {}
    rec_used = []

    if still is not None:
        frames = [int(still * fps)]
        enc = None
    else:
        frames = range(int(total * fps))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        enc = subprocess.Popen(
            [FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
             "-r", str(fps), "-i", "-", "-i", os.path.join(BUILD, "mix.wav"),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
            stdin=subprocess.PIPE)

    for fi in frames:
        tt = fi / fps
        shot = next(s for s in plan if s["start"] <= tt < s["end"])
        t = tt - shot["start"]
        dur = shot["end"] - shot["start"]
        kind = shot["kind"]
        if isinstance(kind, str):
            path = os.path.join(RAW, RAWFILE[kind])
            if os.path.isfile(path):
                if kind not in clips:
                    clips[kind] = Clip(path, dur, fps)
                    rec_used.append(kind)
                im = clips[kind].frame().copy()
            else:
                fb = rec_fallback(kind)
                im = fb(t, dur) if fb else mg_placeholder(t, dur, kind, shot["title"], shot["note"])
        else:
            im = kind(t, dur)
        overlay_text(im, shot, t)
        # 每个镜头首尾 0.15 秒压暗，切换更干净；全片首尾各 1 秒淡入淡出
        k = min(1.0, t / 0.15, (dur - t) / 0.15, tt / 1.0, (total - tt) / 1.0)
        arr = np.asarray(im.convert("RGB"), np.float32) * VIGNETTE * max(0.0, min(1.0, k))
        frame = arr.clip(0, 255).astype(np.uint8)
        if enc is None:
            Image.fromarray(frame).save(out)
            print("still ->", out)
            return
        enc.stdin.write(frame.tobytes())
        if fi % (fps * 5) == 0:
            print("  %5.1fs / %ds" % (tt, total), flush=True)
    enc.stdin.close()
    enc.wait()
    for c in clips.values():
        c.close()
    print("video ->", out, " 实机镜头已用：", rec_used or "无（全部占位）")


# 配乐：四段 Dungeons 原声，各取开头，段落处 1 秒交叉淡化；音效点在切镜处
MUSIC_PLAN = [  # (文件, 开始秒, 结束秒, 音量)
    ("Bgm_env_titleScreen2DMain-001.ogg", 0, 12.5, 1.0),
    ("S1_bgm_env_thtoBossLoop-001.ogg", 11.5, 30.5, 0.9),
    ("Bgm_env_deteNamelessFightLong-001_soundWave.ogg", 29.5, 52.5, 1.0),
    ("Bgm_mob_obpiBossStage1Loop-001.ogg", 51.5, 82, 0.9),
]
SFX_DIR = {"bz": os.path.join(ROOT, "_tools", "beelzebub_ref", "sounds"),
           "tg": os.path.join(ROOT, "_tools", "tower_guard_ref", "sounds")}
SFX_PLAN = [  # (目录, 文件名前缀, 时刻, 音量)
    ("tg", "S1_sfx_towerGuard_basicAttack_swing_01", 26.1, 0.8),
    ("bz", "Sfx_mob_namelessApproach-001", 30.0, 0.9),
    ("bz", "Sfx_mob_namelessCast-001", 34.2, 0.8),
    ("bz", "Sfx_mob_namelessLoadLongSpell-001", 46.0, 0.8),
    ("bz", "Sfx_mob_namelessDeath-001", 52.0, 0.6),
]


def mix_audio(total=82):
    os.makedirs(BUILD, exist_ok=True)
    inputs, filters, labels = [], [], []
    for i, (fn, a, b, vol) in enumerate(MUSIC_PLAN):
        inputs += ["-i", os.path.join(MUSIC, fn)]
        dur = b - a
        fo = 3.0 if b >= total else 1.0
        filters.append("[%d:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:%.2f,asetpts=PTS-STARTPTS,"
                       "afade=t=in:d=%.2f,afade=t=out:st=%.2f:d=%.2f,volume=%.2f,adelay=%d|%d[m%d]"
                       % (i, dur, 0.05 if a == 0 else 1.0, dur - fo, fo, vol, a * 1000, a * 1000, i))
        labels.append("[m%d]" % i)
    n = len(MUSIC_PLAN)
    for j, (d, prefix, at, vol) in enumerate(SFX_PLAN):
        files = [f for f in os.listdir(SFX_DIR[d]) if f.startswith(prefix)]
        if not files:
            continue
        inputs += ["-i", os.path.join(SFX_DIR[d], files[0])]
        filters.append("[%d:a]aresample=48000,aformat=channel_layouts=stereo,volume=%.2f,adelay=%d|%d[s%d]"
                       % (n + j, vol, at * 1000, at * 1000, j))
        labels.append("[s%d]" % j)
    filters.append("%samix=inputs=%d:normalize=0,atrim=0:%d,alimiter=limit=0.95[out]"
                   % ("".join(labels), len(labels), total))
    out = os.path.join(BUILD, "mix.wav")
    subprocess.run([FFMPEG, "-v", "error", "-y"] + inputs +
                   ["-filter_complex", ";".join(filters), "-map", "[out]", out], check=True)
    print("audio ->", out)


def main():
    args = sys.argv[1:]
    if "--still" in args:
        sec = float(args[args.index("--still") + 1])
        render(FPS, os.path.join(BUILD, "still_%05.1f.png" % sec), still=sec)
        return
    fps = int(args[args.index("--preview") + 1]) if "--preview" in args else FPS
    name = "tralancer-promo-preview.mp4" if "--preview" in args else "tralancer-promo.mp4"
    mix_audio()
    render(fps, os.path.join(OUT, name))


if __name__ == "__main__":
    main()
