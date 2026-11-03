# -*- coding: utf-8 -*-
"""把分镜渲染成成片：动态图形逐帧画、实机镜头从 _promo/raw/ 读，叠字幕，再混配乐。

    python _promo/render.py                 # 全片 → _promo/out/tralancer-promo.mp4
    python _promo/render.py --preview 30    # 只出 30 fps 的快速预览
    python _promo/render.py --still 23.5    # 只出这一秒的单帧 PNG，调画面用

画面风格跟美术规范（ART-STYLE.md）走：原版像素字形与 Tooltip（见 mcui.py），
颜色全部取自 _tools/rpg_ui_style.py，物品名与 Lore 直接读数据包里的文本组件。
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
from PIL import Image, ImageDraw, ImageFilter

import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "_tools"))
sys.path.insert(0, HERE)

import mcui  # noqa: E402
import rpg_ui_style as ui  # noqa: E402

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1920, 1080
FPS = 60
RAW = os.path.join(HERE, "raw")
BUILD = os.path.join(HERE, "build")
OUT = os.path.join(HERE, "out")
MUSIC = os.path.join(HERE, "assets", "music")
ICONS = os.path.join(BUILD, "icons")


def rgb(colour):
    return mcui.rgba(colour)[:3]


GROUND = rgb(ui.TOOLTIP_GROUND)
# 五档品质：前缀文字与颜色都取规范（限定款按 README 归入传说一行）；
# 恶魔档按柱着色，行标签用片中出场的别西卜柱亮色
TIER_ROWS = [("brave", "[勇者]", ui.tier_colour("brave")),
             ("epic", "[史诗]", ui.tier_colour("epic")),
             ("legend", "[传说]", ui.tier_colour("legend")),
             ("DEVIL", "[恶魔]", ui.pillar(4)["lit"]),
             ("HOLY", "[神圣]", ui.tier_colour("holy"))]
TIER_OF = {"brave": "brave", "epic": "epic", "legend": "legend", "LTD": "legend",
           "DEVIL": "DEVIL", "HOLY": "HOLY"}


# ---------------------------------------------------------------- 小工具

_cache = {}


def cached(key, fn):
    if key not in _cache:
        _cache[key] = fn()
    return _cache[key]


def txt(s, colour, u, bold=False):
    """单色一行原版字形（带阴影），缓存。"""
    return cached(("t", s, colour, u, bold), lambda: mcui.text([(s, colour, bold)], u))


def runs_img(runs, u):
    return cached(("r", tuple(runs), u), lambda: mcui.text(list(runs), u))


def paste(canvas, layer, cx, cy, alpha=1.0, scale=1.0):
    """把 RGBA 图层按中心点贴上去，alpha 0..1；缩放用最近邻，保住像素边。"""
    if alpha <= 0.003:
        return
    if scale != 1.0:
        w, h = layer.size
        layer = layer.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.NEAREST)
    if alpha < 1.0:
        layer = layer.copy()
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
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


def icon(path):
    return cached(("i", path), lambda: Image.open(path).convert("RGBA"))


def slot_img(path, u):
    return cached(("s", path, u), lambda: mcui.slot(u, icon(path)))


def big_icon(path, px):
    return cached(("b", path, px), lambda: icon(path).resize((px, px), Image.NEAREST))


# ---------------------------------------------------------------- 背景：Tooltip 底色 + 方形粒子

def vignette_mask():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return np.clip(1.15 - 0.55 * d ** 2, 0.35, 1.0)[..., None]


VIGNETTE = vignette_mask()
_rng = random.Random(7)
MOTES = [(_rng.random() * W, _rng.random() * H, _rng.choice((4, 4, 6, 8)), _rng.uniform(10, 34),
          _rng.random() * 6.28, _rng.random()) for _ in range(120)]


def _ground(lift):
    """Tooltip 底色 #100010 铺满，中心按 lift 色微微提亮。"""
    def make():
        base = np.zeros((H, W, 3), np.float32)
        base[:] = GROUND
        y, x = np.mgrid[0:H:4, 0:W:4].astype(np.float32)
        g = np.exp(-(((x - W / 2) / 760) ** 2 + ((y - H / 2) / 460) ** 2))
        g = np.kron(g, np.ones((4, 4), np.float32))[:H, :W, None]
        base += g * (np.array(rgb(lift), np.float32) - base) * 0.16
        return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    return cached(("g", lift), make)


def backdrop(t, lit=ui.HOLY, deep=ui.HOLY_DARK):
    """原版粒子是方块：亮端到暗端渐变（规范 §粒子：不用纯黑暗端）。"""
    im = _ground(deep).copy()
    d = ImageDraw.Draw(im)
    a, b = np.array(rgb(lit), float), np.array(rgb(deep), float)
    for (x0, y0, s, sp, ph, mix) in MOTES:
        yy = (y0 - t * sp) % H
        xx = x0 + math.sin(t * 0.4 + ph) * 16
        life = 0.5 + 0.5 * math.sin(t * 1.1 + ph)
        c = a * (1 - mix) + b * mix
        alpha = int(40 + 120 * life)
        size = max(2, int(s * (0.6 + 0.4 * life)) // 2 * 2)
        d.rectangle((xx, yy, xx + size, yy + size), fill=tuple(int(v) for v in c) + (alpha,))
    return im


SECTION = {  # 每段粒子的亮端 / 暗端
    "open": (ui.HOLY, ui.HOLY_DARK),
    "gear": (ui.HOLY, ui.HOLY_DARK),
    "demon": (ui.pillar(4)["lit"], ui.pillar(4)["deep"]),
    "pact": (ui.RITUAL, ui.pillar(6)["deep"]),
    "covenant": (ui.CYAN, ui.HOLY_DARK),
}


# ---------------------------------------------------------------- 素材

def load_catalogue():
    from rpg_catalogue import catalogue
    return cached("cat", lambda: catalogue(os.path.join(ROOT, "rpg")))


def item_tooltip(name, u, max_lines=None):
    """数据包里这件物品的名字 + Lore → 原版 Tooltip；max_lines 截掉过长的 Lore（画面放不下）。"""
    def make():
        comp = load_catalogue()[name][0]["components"]
        lines = [mcui.component_runs(comp["custom_name"])]
        lines += [mcui.component_runs(l) or [(" ", "white", False)] for l in comp.get("lore", [])]
        if max_lines and len(lines) > max_lines:
            lines = lines[:max_lines - 1] + [[("……", ui.MUTED, False)]]
        return mcui.tooltip(lines, u)
    return cached(("tt", name, u, max_lines), make)


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
            out.append((TIER_OF.get(tier, tier), name, os.path.join(ICONS, f)))
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

HEBREW = "ארץ השברים"[::-1]   # 没有双向排版，希伯来文手动倒成视觉顺序


def mg_title(t, dur):
    im = backdrop(t, *SECTION["open"])
    a = ease((t - 0.3) / 1.6)
    paste(im, txt(HEBREW, ui.HOLY, 16, True), W / 2, H / 2 - 70, a)
    paste(im, txt("ERETZ HA-SHEVARIM", ui.HOLY_LIGHT, 4), W / 2, H / 2 + 70, ease((t - 1.2) / 1.2))
    paste(im, txt("碎片之地", ui.GRAY, 4), W / 2, H / 2 + 120, ease((t - 1.6) / 1.2))
    return im


CRACKS = []
_r = random.Random(11)
for _k in range(9):
    ang = _k / 9 * 6.283 + _r.uniform(-0.3, 0.3)
    pts, x, y = [], W / 2 + _r.uniform(-40, 40), H / 2 - 50 + _r.uniform(-20, 20)
    for _s in range(14):
        ang += _r.uniform(-0.45, 0.45)
        x += math.cos(ang) * _r.uniform(40, 90)
        y += math.sin(ang) * _r.uniform(30, 70)
        pts.append((round(x / 8) * 8, round(y / 8) * 8))     # 裂纹也落在 8 像素网格上
    CRACKS.append([(W / 2, H / 2 - 50)] + pts)


def mg_shatter(t, dur):
    im = mg_title(t + 4, 99)
    d = ImageDraw.Draw(im)
    grow = ease_out(t / 2.2)
    for path in CRACKS:
        n = max(2, int(len(path) * grow))
        d.line(path[:n], fill=mcui.rgba(ui.HOLY_LIGHT, 230), width=4)
    if t > 2.4:   # 碎开：按 8 像素对齐的横条错位下坠
        k = ease((t - 2.4) / 1.4)
        arr = np.array(im)
        bands, rr = 18, random.Random(5)
        bh = H // bands
        out = np.zeros_like(arr)
        out[..., 3] = 255
        out[..., :3] = GROUND
        for b in range(bands):
            dx = int(rr.uniform(-160, 160) * k) // 8 * 8
            dy = int(rr.uniform(20, 140) * k * k) // 8 * 8
            y0 = b * bh + dy
            if y0 >= H:
                continue
            h = min(bh, H - y0)
            out[y0:y0 + h] = np.roll(arr[b * bh:(b + 1) * bh], dx, axis=1)[:h]
        im = Image.fromarray(out)
        flash = max(0.0, 1 - (t - 2.4) / 0.35)
        if flash > 0:
            im = Image.blend(im, Image.new("RGBA", im.size, mcui.rgba(ui.HOLY_LIGHT)), flash * 0.6)
    return im


def mg_weapons(t, dur, ws):
    """五档一行一档：行首是规范的 [档次] 前缀，后面是原版物品格。"""
    im = backdrop(t, *SECTION["gear"])
    u = 5
    cell = 18 * u + 6
    rows = [[w for w in ws if w[0] == key] for key, _tag, _c in TIER_ROWS]
    top = H / 2 - len(rows) * (cell + 18) / 2 - 30
    for ri, (row, (_key, tag, colour)) in enumerate(zip(rows, TIER_ROWS)):
        y = top + ri * (cell + 18) + cell / 2
        row_t = t - 0.15 - ri * 0.45
        paste(im, txt(tag, colour, 6, True), 250, y, ease(row_t / 0.4))
        for i, (_tier, _name, path) in enumerate(row):
            lt = row_t - i * 0.06
            if lt <= 0:
                continue
            p = ease_out(lt / 0.4)
            paste(im, slot_img(path, u), 380 + i * cell + cell / 2, y - (1 - p) * 48 // 4 * 4, p)
    return im


def mg_twins(t, dur):
    """雅斤与波阿斯：两张数据包里的原版 Tooltip 从两侧合拢；下方一排符文与锻造材料。"""
    im = backdrop(t, *SECTION["gear"])
    p = ease_out(t / 0.9)
    for i, name in enumerate(["雅斤", "波阿斯"]):
        tt = item_tooltip(name, 4)
        side = -1 if i == 0 else 1
        x = W / 2 + side * (tt.width / 2 + 24 + 420 * (1 - p))
        paste(im, tt, x, H / 2 - 60, p)
        ic = icons_of("III", [name])
        if ic:
            paste(im, slot_img(ic[0], 6), x, H / 2 - 60 - tt.height / 2 - 80, p)
    strip = icons_of("V") + icons_of("VI", ["铸造之石", "传说冶炼石", "冶炼石", "剑胚"])
    sx = W + 40 - t * 300
    for i, path in enumerate(strip):
        x = sx + i * 84
        if -60 < x < W + 60:
            paste(im, slot_img(path, 4), x, H / 2 + 290, ease((t - 0.4) / 0.6))
    return im


def mg_sins(t, dur):
    """七宗罪：七个 [罪名] 前缀依次亮起，各取其柱亮色；最后只留下别西卜的 [暴食]。"""
    im = backdrop(t, *SECTION["demon"])
    for i, p in enumerate(ui.PILLARS):
        lt = t - 0.2 - i * 0.32
        hi = p["n"] == 4
        a = ease(lt / 0.25)
        if t > 2.9 and not hi:
            a *= 1 - ease((t - 2.9) / 0.6) * 0.8
        sc = 1.0 + (0.5 * ease((t - 2.9) / 0.6) if hi else 0)
        x = W / 2 + (i - 3) * 256
        paste(im, txt("[%s]" % p["sin"], p["lit"], 7, True), x, H / 2 - 60, a, sc)
        paste(im, txt(p["who"], ui.WHITE, 5), x, H / 2 + 40, a * (1 - ease((t - 2.9) / 0.4)))
    return im


ROLES = ["先锋", "猎手", "司祭", "咒使", "处刑者"]


def mg_servants(t, dur):
    """七柱 × 五职：每格一张小 Tooltip，职名用该柱亮色。"""
    im = backdrop(t, *SECTION["demon"])
    u = 4
    cw, ch, gx, gy = 228, 112, 14, 6
    x0 = W / 2 - (7 * cw + 6 * gx) / 2
    y0 = H / 2 - (5 * ch + 4 * gy) / 2 + 10
    for c, p in enumerate(ui.PILLARS):
        cx = x0 + c * (cw + gx) + cw / 2
        paste(im, txt("[%s柱]" % p["who"], p["lit"], 5, True), cx, y0 - 50, ease((t - c * 0.05) / 0.4))
        for r, role in enumerate(ROLES):
            a = ease((t - 0.3 - (c * 5 + r) * 0.05) / 0.3)
            if a <= 0:
                continue
            tip = cached(("cell", c, r), lambda p=p, role=role: mcui.tooltip(
                [[(role, p["lit"], True)]], u, min_w=30, centre=True))
            paste(im, tip, cx, y0 + r * (ch + gy) + ch / 2, a)
    return im


def mg_pacts(t, dur):
    """七本罪约契约书依次翻开，最后亮出别西卜之柱的原版 Tooltip。"""
    im = backdrop(t, *SECTION["pact"])
    focus = ease((t - 2.2) / 0.6)
    for i, p in enumerate(ui.PILLARS):
        lt = t - 0.2 - i * 0.2
        if lt <= 0:
            continue
        q = ease_out(lt / 0.35)
        art = big_icon(os.path.join(ROOT, "_tools", "pact_art", "pact_%s.png" % p["slug"]), 128)
        art = art.resize((max(1, int(128 * q)), 128), Image.NEAREST)   # 横向翻开
        x = W / 2 + (i - 3) * 228
        dim = 1 - focus * (0.0 if p["n"] == 4 else 0.7)
        y = H / 2 - 60 - focus * 180
        paste(im, art, x, y, min(1.0, q * 1.5) * dim)
        paste(im, txt("[契约]", p["lit"], 3, True), x, y + 100, q * dim * (1 - focus * (p["n"] == 4)))
    if focus > 0:
        names = [n for n in load_catalogue() if n.startswith("别西卜之柱")]
        if names:
            tip = item_tooltip(names[0], 4, max_lines=9)
            paste(im, tip, W / 2, H / 2 - 120 + 64 + tip.height / 2, focus)
    return im


SEPH = [(0, 0), (1, 1), (-1, 1), (1, 2.6), (-1, 2.6), (0, 3.4), (1, 4.2), (-1, 4.2), (0, 5.0), (0, 6.2)]
SEPH_KEY = ["kether", "chokmah", "binah", "chesed", "geburah", "tiphareth",
            "netzach", "hod", "yesod", "malkuth"]
PATHS = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (1, 5), (2, 5), (3, 4), (3, 5), (4, 5), (3, 6),
         (4, 7), (5, 6), (5, 7), (6, 7), (6, 8), (7, 8), (5, 8), (8, 9), (0, 5), (6, 9), (7, 9)]


def draw_tree(im, t, cx, cy, scale, alpha=1.0):
    """生命之树：路径用秘仪紫，十个源质用规范里各自的颜色，节点画成方块。"""
    d = ImageDraw.Draw(im)
    pts = [(cx + x * scale * 1.1, cy + (y - 3.1) * scale) for x, y in SEPH]
    for k, (a, b) in enumerate(PATHS):
        p = ease((t - k * 0.05) / 0.5) * alpha
        if p > 0:
            ax, ay = pts[a]
            bx, by = pts[b]
            d.line((ax, ay, ax + (bx - ax) * p, ay + (by - ay) * p), fill=mcui.rgba(ui.RITUAL, int(150 * alpha)), width=4)
    for k, (x, y) in enumerate(pts):
        p = ease((t - 0.3 - k * 0.1) / 0.35) * alpha
        if p > 0:
            r = int(0.2 * scale) // 4 * 4
            col = ui.SEPHIROT[SEPH_KEY[k]]
            d.rectangle((x - r - 4, y - r - 4, x + r + 4, y + r + 4), fill=mcui.rgba(ui.TOOLTIP_GROUND, int(255 * p)))
            d.rectangle((x - r, y - r, x + r, y + r), fill=mcui.rgba(col, int(255 * p)))


def mg_covenants(t, dur):
    """旧约（圣金·深）与新约（权柄青）：两张原版 Tooltip，在生命之树前合拢。"""
    im = backdrop(t, *SECTION["covenant"])
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw_tree(layer, t + 1, W / 2, H / 2 - 30, 120, 0.45)
    im.alpha_composite(layer)
    p = ease_out(t / 0.9)
    merge = ease((t - 2.6) / 1.0)
    for i, name in enumerate(["旧约", "新约"]):
        tt = item_tooltip(name, 4, max_lines=9)
        side = -1 if i == 0 else 1
        x = W / 2 + side * (tt.width / 2 + 30) * (1 - merge * 0.35)
        paste(im, tt, x, H / 2 - 80, p * (1 - merge * 0.5 if i == 0 else 1))
    if merge > 0:
        f = Image.new("RGBA", im.size, mcui.rgba(ui.CYAN_LIGHT, int(90 * max(0, 1 - abs(merge - 0.6) / 0.4))))
        im.alpha_composite(f)
    return im


def mg_title_card(t, dur):
    im = backdrop(t, *SECTION["open"])
    a = ease((t - 0.2) / 1.0)
    paste(im, txt("破碎大陆", ui.HOLY, 20, True), W / 2, H / 2 - 120, a)
    paste(im, txt("TRALANCER RPG", ui.WHITE, 8, True), W / 2, H / 2 + 40, ease((t - 0.8) / 0.8))
    d = ImageDraw.Draw(im)
    ln = int(440 * ease((t - 1.0) / 0.8)) // 4 * 4
    d.rectangle((W / 2 - ln, H / 2 + 108, W / 2 + ln, H / 2 + 111), fill=mcui.rgba(ui.HOLY_DARK))
    paste(im, runs_img((("Minecraft Java 1.21.11 ", ui.WHITE, False), ("数据包 + 资源包", ui.GRAY, False),
                        ("　开源免费", ui.READY, False)), 4), W / 2, H / 2 + 160, ease((t - 1.5) / 0.8))
    return im


CREDITS = [
    [("破碎大陆 · TRALANCER RPG", ui.HOLY, True)],
    [("世界观设定：仓库作者　开源免费，非商业项目", ui.GRAY, False)],
    [(" ", ui.GRAY, False)],
    [("[配乐] ", ui.RITUAL, True), ("Minecraft Dungeons Original Soundtrack", ui.WHITE, False)],
    [("Finnbacka (title screen) / The Tower: Boss - Peter Hont", ui.GRAY, False)],
    [("Necromancer (Nameless One fight) - Johan Johnson", ui.GRAY, False)],
    [("The Arch-Illager: Stage 1 - Peter Hont", ui.GRAY, False)],
    [(" ", ui.GRAY, False)],
    [("[素材] ", ui.HOLY, True), ("圣卫与别西卜的模型参考、贴图与音效取自 Minecraft Dungeons", ui.WHITE, False)],
    [("Minecraft Dungeons music, textures and sounds (c) Mojang Studios.", ui.MUTED, False)],
    [("Minecraft fonts, GUI and block textures (c) Mojang Studios.", ui.MUTED, False)],
    [("Free, non-commercial fan project; not affiliated with Mojang or Microsoft.", ui.MUTED, False)],
]
CREDIT_REC = [("Gameplay shot with ReplayMod and Complementary Reimagined shaders.", ui.MUTED, False)]


def has_rec():
    return any(os.path.isfile(os.path.join(RAW, f)) for f in RAWFILE.values())


def mg_credits(t, dur):
    im = backdrop(t, ui.MUTED, ui.TOOLTIP_GROUND)
    lines = CREDITS + ([CREDIT_REC] if has_rec() else [])   # 有实拍才署录制工具
    paste(im, cached("credits", lambda: mcui.tooltip(lines, 4)), W / 2, H / 2 - 40, ease((t - 0.1) / 0.6))
    return im


def mg_placeholder(t, dur, code, title, note):
    im = backdrop(t, ui.MUTED, ui.TOOLTIP_GROUND)
    tip = cached(("ph", code), lambda: mcui.tooltip([
        [("[实机镜头] ", ui.WARN, True), ("%s 待录制" % code, ui.WHITE, False)],
        [(title, ui.HOLY, True)],
        [(note, ui.GRAY, False)],
        [("_promo/raw/%s" % RAWFILE[code], ui.MUTED, False)]], 4))
    paste(im, tip, W / 2, H / 2 - 80)
    return im


# ---------------------------------------------------------------- 无实拍版：顶替实机镜头的画面
#
# 没有录屏时，S1–S5 也用原版素材画出来，而不是占位卡：
# 原版方块贴图、Boss 血条、聊天栏，加上按 geo.json 画出的别西卜与圣卫模型。
# 聊天里的每一行都是数据包里真实的 tellraw 文本，不另编。

import geo_render  # noqa: E402
import zipfile  # noqa: E402

from mc_env import JAR  # noqa: E402


def jar_png(path):
    def make():
        with zipfile.ZipFile(JAR) as z:
            return Image.open(__import__("io").BytesIO(z.read(path))).convert("RGBA")
    return cached(("jar", path), make)


def block(name, px):
    return cached(("blk", name, px), lambda: jar_png("assets/minecraft/textures/block/%s.png" % name)
                  .resize((px, px), Image.NEAREST))


def model(slug, yaw, px):
    """别西卜 / 圣卫的模型图，按 2 度一档缓存（转台每帧都要）。"""
    yaw = int(round(yaw / 2.0) * 2) % 360
    return cached(("geo", slug, yaw, px), lambda: geo_render.render(
        os.path.join(ROOT, "_tools", "%s_ref" % slug, "%s.geo.json" % slug),
        os.path.join(ROOT, "_tools", "%s_ref" % slug, "%s_atlas.png" % slug), yaw=yaw, pitch=-8, px=px))


def tellraw_runs(*needles):
    """数据包里第一条同时含所有 needles 的 tellraw → runs（字体颜色按规范已写好）。"""
    def make():
        base = os.path.join(ROOT, "rpg", "data", "rpg", "function")
        for dirpath, _d, files in os.walk(base):
            for fn in files:
                if not fn.endswith(".mcfunction"):
                    continue
                for line in open(os.path.join(dirpath, fn), encoding="utf-8"):
                    if all(n in line for n in needles) and "tellraw" in line:
                        rest = line[line.index("tellraw"):]
                        js = rest[rest.index('["'):].strip()   # 文本组件数组总以 ["" 开头
                        return tuple(mcui.component_runs(json.loads(js)))
        raise KeyError(needles)
    return cached(("tr", needles), make)


def chat(im, lines, t, step=0.7, start=0.2, u=4):
    """原版聊天栏：左下角，每行半透明黑底，按 step 秒一行地冒出来。"""
    shown = [l for i, l in enumerate(lines) if t >= start + i * step]
    lh = 9 * u
    y = H - 260 - len(shown) * lh
    for i, runs in enumerate(shown):
        age = t - start - lines.index(runs) * step
        a = ease(age / 0.15)
        row = cached(("chatrow", runs, u), lambda runs=runs: _chat_row(runs, u))
        paste(im, row, 40 + row.width / 2, y + i * lh + lh / 2, a)


def _chat_row(runs, u):
    w = 320 * u
    img = Image.new("RGBA", (w, 9 * u), (0, 0, 0, 128))
    mcui.draw_runs(img, u, u // 2, list(runs), u)
    return img


def boss_bar(name_runs, frac, u=4):
    """原版 Boss 血条（包里的恶魔血条是蓝色、6 段刻度）。"""
    bg = jar_png("assets/minecraft/textures/gui/sprites/boss_bar/blue_background.png")
    fg = jar_png("assets/minecraft/textures/gui/sprites/boss_bar/blue_progress.png")
    nb = jar_png("assets/minecraft/textures/gui/sprites/boss_bar/notched_6_background.png")
    nf = jar_png("assets/minecraft/textures/gui/sprites/boss_bar/notched_6_progress.png")
    bw, bh = bg.size
    bar = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    bar.alpha_composite(bg)
    bar.alpha_composite(nb)
    cut = max(0, int(bw * frac))
    if cut:
        bar.alpha_composite(fg.crop((0, 0, cut, bh)))
        bar.alpha_composite(nf.crop((0, 0, cut, bh)))
    bar = bar.resize((bw * u, bh * u), Image.NEAREST)
    title = mcui.text(list(name_runs), u)
    out = Image.new("RGBA", (max(bar.width, title.width), title.height + bar.height + u), (0, 0, 0, 0))
    out.alpha_composite(title, ((out.width - title.width) // 2, 0))
    out.alpha_composite(bar, ((out.width - bar.width) // 2, title.height + u))
    return out


BZ_NAME = (("[恶魔]", ui.pillar(4)["lit"], True), ("别西卜", ui.WHITE, False))


def mg_land(t, dur):
    """破碎大陆：一整块原版地层（草、土、石、深板岩）从中裂成五块，各自漂开。"""
    im = backdrop(t, ui.HOLY_LIGHT, ui.HOLY_DARK)
    px = 48
    cols = 30
    layers = ["grass_block_side"] + ["dirt"] * 2 + ["stone"] * 3 + ["deepslate"] * 2
    cuts = [0, 6, 13, 18, 24, 30]
    rr = random.Random(3)
    split = ease((t - 0.6) / 2.6)
    x_left = W / 2 - cols * px / 2
    y_top = H / 2 - len(layers) * px / 2 - 40
    for f in range(len(cuts) - 1):
        c0, c1 = cuts[f], cuts[f + 1]
        dx = (f - 2) * 46 * split
        dy = rr.uniform(-60, 60) * split
        for c in range(c0, c1):
            depth = len(layers) - rr.randint(0, 3) if c in (c0, c1 - 1) else len(layers)
            for r in range(depth):
                fall = 0
                if r >= depth - 2 and (c in (c0, c1 - 1)):
                    fall = max(0.0, split - 0.3) * rr.uniform(80, 260)
                x = int(x_left + c * px + dx) // 4 * 4
                y = int(y_top + r * px + dy + fall) // 4 * 4
                im.alpha_composite(block(layers[r], px), (x, y))
        # 每块顶上一排草顶的侧影
    return im


ARMORY_PICK = ["brave", "epic", "legend", "DEVIL", "HOLY"]
ARMORY_NAME = {"epic": "漆黑之日", "legend": "利维坦之歌", "DEVIL": "别西卜", "HOLY": "朗基努斯之枪"}


def mg_armory(t, dur, ws):
    """武器长廊（无实拍版）：每档挑一件，原版 Tooltip 加物品格依次换上。"""
    im = backdrop(t, *SECTION["gear"])
    per = dur / len(ARMORY_PICK)
    i = min(len(ARMORY_PICK) - 1, int(t / per))
    lt = t - i * per
    tier = ARMORY_PICK[i]
    pick = [w for w in ws if w[0] == tier]
    pick = next((w for w in pick if w[1] == ARMORY_NAME.get(tier)), pick[0])
    a = fade(lt, per, 0.2, 0.2)
    tt = item_tooltip(pick[1], 4, max_lines=12)
    slide = (1 - ease_out(lt / 0.35)) * 80
    paste(im, slot_img(pick[2], 8), W / 2 - tt.width / 2 - 120 - slide, H / 2 - 80, a)
    paste(im, tt, W / 2 + 70 + slide, H / 2 - 80, a)
    # 底部进度：五档前缀，当前档高亮
    xs = W / 2 - 2 * 200
    for k, (key, tag, colour) in enumerate(TIER_ROWS):
        paste(im, txt(tag, colour if k == i else ui.DARK_GRAY, 5, True), xs + k * 200, H / 2 + 270)
    return im


def mg_guards(t, dur):
    """圣卫方阵：三名圣卫列队压近，头顶原版名牌。"""
    im = backdrop(t, ui.HOLY, ui.pillar(5)["deep"])
    adv = ease(t / dur)
    for k, (dx, delay) in enumerate([(-360, 0.25), (0, 0.0), (360, 0.25)]):
        px = int(13 + 4 * ease((t - delay) / dur))
        m = model("tower_guard", 22 - dx / 40, px)
        bob = abs(math.sin((t - delay) * 5.0)) * 10
        x = W / 2 + dx * (1 + 0.2 * adv)
        y = H / 2 + 40 - bob
        paste(im, m, x, y)
        tag = txt("圣卫", ui.HOLY, 5, True)
        plate = Image.new("RGBA", (tag.width + 8, tag.height + 4), (0, 0, 0, 64))
        plate.alpha_composite(tag, (4, 2))
        paste(im, plate, x, y - m.height / 2 - 30)
    return im


def mg_beelzebub(t, dur):
    """别西卜降临：模型缓缓转身，原版 Boss 血条，聊天栏里罪群应召、反仪式发动。"""
    im = backdrop(t, *SECTION["demon"])
    rise = ease_out(t / 1.2)
    m = model("beelzebub", 180 + 25 * math.sin(t * 0.6), 17)
    paste(im, m, W / 2 + 480, H / 2 + 20 + (1 - rise) * 120, rise)
    paste(im, boss_bar(BZ_NAME, 1.0 - 0.06 * t, 4), W / 2, 110, ease((t - 0.4) / 0.5))
    chat(im, [tellraw_runs("[罪群]", "别西卜 · ", "先锋 "), tellraw_runs("[罪群]", "别西卜 · ", "司祭 "),
              tellraw_runs("[反仪式・吞媒]"), tellraw_runs("腐宴开席")], t, step=1.4, start=1.0)
    return im


def mg_exorcism(t, dur):
    """驱魔与封印：法阵里裁决落笔，残魂收入封魔灯，又从遗物里重新降临。"""
    im = backdrop(t, ui.HOLY, ui.pillar(4)["deep"])
    m = model("beelzebub", 180 + 10 * math.sin(t), 17)
    dim = 1 - 0.55 * ease((t - 3.0) / 0.6)
    paste(im, m, W / 2 + 480, H / 2 + 20, dim)
    paste(im, boss_bar(BZ_NAME, max(0.0, 0.18 - 0.05 * t), 4), W / 2, 110, 1 - ease((t - 3.0) / 0.5))
    chat(im, [tellraw_runs("[裁决尚待]"), tellraw_runs("[消灭] "), tellraw_runs("[裁决・封印]"),
              tellraw_runs("[封印逃逸] \",\"color\":\"#B5D957\"")], t, step=1.2, start=0.3)
    flash = max(0.0, 1 - abs(t - 3.0) / 0.25)
    if flash > 0:
        im.alpha_composite(Image.new("RGBA", im.size, mcui.rgba(ui.CYAN_LIGHT, int(140 * flash))))
    return im


def mg_tree(t, dur):
    """生命之树（无实拍版）：十个源质按规范色依次点亮，旁注原名。"""
    im = backdrop(t, ui.RITUAL, ui.pillar(6)["deep"])
    draw_tree(im, t, W / 2, H / 2 - 50, 112)
    pts = [(W / 2 + x * 112 * 1.1, H / 2 - 50 + (y - 3.1) * 112) for x, y in SEPH]
    for k, (x, y) in enumerate(pts):
        a = ease((t - 0.5 - k * 0.1) / 0.35)
        name = SEPH_KEY[k].capitalize()
        lay = txt(name, ui.SEPHIROT[SEPH_KEY[k]] if SEPH_KEY[k] != "binah" else ui.GRAY, 4)
        side = 1 if SEPH[k][0] >= 0 else -1
        paste(im, lay, x + side * (lay.width / 2 + 40), y, a)
    return im


NO_REC = {"S1": mg_land, "S3": mg_guards, "S4a": mg_beelzebub, "S4b": mg_exorcism, "S5": mg_tree}


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
        return self.last if self.last is not None else Image.new("RGBA", (W, H), GROUND + (255,))

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
    add(12, 17, lambda t, d: mg_weapons(t, d, ws), "31 件武器 · 五档品质", "31 weapons, five tiers", "[壹・装备]")
    add(17, 22, "S2", "勇者 · 史诗 · 传说 · 恶魔 · 神圣", "Brave / Epic / Legend / Devil / Holy", "[壹・装备]",
        title="武器长廊", note="齐腰高度沿长廊推轨，从勇者推到神圣")
    add(22, 26, mg_twins, "圣殿双柱，双持联动；符文、镶嵌与锻造",
        "Jachin & Boaz in both hands - runes, gems, forging", "[壹・装备]")
    add(26, 30, "S3", "教廷圣卫，借神之名而来", "The Papal Guard marches in God's name", "[壹・装备]",
        title="圣卫方阵", note="低机位正面，圣卫迎着镜头冲来")
    add(30, 34, mg_sins, "七宗罪领主", "Seven Lords of Sin", "[贰・恶魔生态]")
    add(34, 42, "S4a", "别西卜 · 暴食", "Beelzebub, Lord of Gluttony", "[贰・恶魔生态]",
        title="别西卜降临", note="降临烟雾，接一个起手招式")
    add(42, 46, mg_servants, "35 名所罗门罪仆，七柱五职",
        "35 servants of Solomon - seven pillars, five roles", "[贰・恶魔生态]")
    add(46, 52, "S4b", "魔化 · 真名调查 · 四阶段驱魔 · 封印遗物",
        "Corruption / True-name inquest / Four-stage exorcism / Sealed relics", "[贰・恶魔生态]",
        title="万蝇饕宴", note="别西卜大招，镜头拉远看清全貌")
    add(52, 56, mg_pacts, "七十二柱罪约", "Pacts of the Seventy-Two Pillars", "[叁・契约体系]")
    add(56, 63, "S5", "卡巴拉生命之树，十源质归位", "The Tree of Life - ten sephirot restored", "[叁・契约体系]",
        title="生命之树", note="夜里，俯视角缓慢环绕粒子阵")
    add(63, 68, mg_covenants, "旧约 · 新约：权与力重新相遇",
        "Old Covenant, New Covenant: power and authority reunited", "[叁・契约体系]")
    add(68, 75, mg_title_card)
    add(75, 82, mg_credits)
    return S


def rec_fallback(code, ws):
    """实机素材缺席时，用无实拍版画面顶上（见 NO_REC）。"""
    if code == "S2":
        return lambda t, dur: mg_armory(t, dur, ws)
    return NO_REC.get(code)


# ---------------------------------------------------------------- 字幕与章节

def subtitle_panel(zh, en):
    """字幕：一张原版 Tooltip，中文白字一行、英文灰字一行，居中。"""
    def make():
        zu, eu = 6, 3
        zw = mcui.measure([(zh, ui.WHITE, False)], zu)
        ew = mcui.measure([(en, ui.GRAY, False)], eu) if en else 0
        wu = max(zw, ew) // eu + 4
        hu = (8 * zu + (6 * eu + 8 * eu if en else 0)) // eu
        img, (ox, oy) = mcui.panel(wu, hu, eu)
        mcui.draw_runs(img, ox + (wu * eu - zw) // 2, oy, [(zh, ui.WHITE, False)], zu)
        if en:
            mcui.draw_runs(img, ox + (wu * eu - ew) // 2, oy + 8 * zu + 6 * eu, [(en, ui.GRAY, False)], eu)
        return img
    return cached(("sub", zh, en), make)


def overlay_text(im, shot, t):
    dur = shot["end"] - shot["start"]
    if shot["zh"]:
        paste(im, subtitle_panel(shot["zh"], shot["en"]), W / 2, H - 140, fade(t, dur, 0.3, 0.3))
    if shot["chapter"]:
        lay = txt(shot["chapter"], ui.HOLY, 4, True)
        im.alpha_composite(lay, (96, 64))


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
                fb = rec_fallback(kind, ws)
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
# 无名者音效存于 beelzebub_ref；目录不在时跳过音效，不影响出片
SFX_DIR = {"bz": next((d for d in [os.path.join(ROOT, "_tools", "beelzebub_ref", "sounds")]
                   if os.path.isdir(d)), ""),
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
    for j, (d, prefix, at, vol) in enumerate(SFX_PLAN):
        files = [f for f in os.listdir(SFX_DIR[d]) if f.startswith(prefix)] if SFX_DIR[d] else []
        if not files:
            continue
        k = len(inputs) // 2      # 跳过缺失的音效后，输入序号要按实际个数算
        inputs += ["-i", os.path.join(SFX_DIR[d], files[0])]
        filters.append("[%d:a]aresample=48000,aformat=channel_layouts=stereo,volume=%.2f,adelay=%d|%d[s%d]"
                       % (k, vol, at * 1000, at * 1000, j))
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
