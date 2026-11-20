# -*- coding: utf-8 -*-
"""米迦勒战专属的特效素材（用户 2026-11-18「特效太朴素了，贴图太少……这个制作水平只能更高」）。

    python add_michael_fx_art.py ../resourcepack

两路来源，都在 _tools/michael_fx_ref/：
  dungeons/  《Minecraft Dungeons》本体的通用特效贴图（只读导出，2026-11-18，见 SOURCES.md）：
             16 帧火焰 T_FireBlock1x1、火舌 T_FireSide、火滴 T_FireDroplet、羽毛 T_Feathers、星芒 T_Stars_16、
             神光 T_GodRayLight、爆环 T_fullcircle_explosion_124、白鸽 T_Doves_Flipbook、弧光 T_Combat_LongSlash /
             T_Slash_Grayscale、烟团 T_SmokeBallVariation、像素圆环、地裂、溶解噪声。
  anim/      Codex 按 ART-BRIEF.md 画的米迦勒专属序列帧（睁眼、六翼爆开、燃羽、流星、天火柱、骨刺、十字斩、
             光环、圣火环）和三张圣印；一张图一行帧，按透明空隙切开。

和篡夺者那套白图染色不同，这里的颜色在贴图里**烘焙**好：按亮度映射到两条色阶——
  HOLY 一阶段暖白金（珊瑚 → 桃 → 暖白 → 白），FIRE 二阶段圣焰（暗烬 → #FF3300 → 珊瑚 → 桃 → 暖白）。
字形用白色文字（不再染色），物品用 custom_model_data 白色。贴图只有 16×16 或 32×32（用户 2026-11-08）。

字体 rpg:michael_vfx（字形，text_display，不受光照）；物品 rpg:michael_vfx/*（地面贴花与天空印，item_display）。
"""
import io
import os
import sys

import numpy as np
from PIL import Image

import display_mob as dm

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "michael_fx_ref")
DUN = os.path.join(REF, "dungeons")
ANIM = os.path.join(REF, "anim")
KEY = "michael_vfx"
FONT = "rpg:" + KEY
NS = "rpg:" + KEY
GLYPH_BASE = 0xE000
STRIDE = 32

# 色阶：(位置, 颜色)
HOLY = ((0.0, (0xA8, 0x40, 0x1C)), (0.3, (0xFF, 0x80, 0x5F)), (0.6, (0xFF, 0xD0, 0xBD)), (0.85, (0xFF, 0xF2, 0xC8)),
        (1.0, (0xFF, 0xFF, 0xFF)))
FIRE = ((0.0, (0x7A, 0x16, 0x00)), (0.3, (0xFF, 0x33, 0x00)), (0.58, (0xFF, 0x80, 0x5F)), (0.8, (0xFF, 0xD0, 0xBD)),
        (1.0, (0xFF, 0xF5, 0xEE)))
ASH = ((0.0, (0x12, 0x08, 0x06)), (0.6, (0x2E, 0x18, 0x12)), (0.85, (0x7A, 0x16, 0x00)), (1.0, (0xFF, 0x33, 0x00)))
RED = ((0.0, (0x7A, 0x16, 0x00)), (0.5, (0xFF, 0x33, 0x00)), (1.0, (0xFF, 0x80, 0x5F)))


def ramp(t, stops):
    t = np.clip(t, 0, 1)
    out = np.zeros(t.shape + (3,))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        m = (t >= p0) & (t <= p1)
        k = ((t - p0) / max(p1 - p0, 1e-6))[..., None]
        out = np.where(m[..., None], np.array(c0, float) + (np.array(c1, float) - np.array(c0, float)) * k, out)
    return out


def tone(im, stops, lo=None, hi=None, alpha=None, lift=0.0):
    """Recolour by luminance onto a ramp; alpha kept (or given)."""
    a = np.array(im.convert("RGBA")).astype(float)
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255.0
    al = a[..., 3] if alpha is None else alpha
    seen = al > 8
    if lo is None:
        lo, hi = np.percentile(lum[seen], (3, 97)) if seen.any() else (0.0, 1.0)
    t = np.clip((lum - lo) / max(hi - lo, 1e-6), 0, 1) + lift
    rgb = ramp(t, stops)
    return Image.fromarray(np.dstack([rgb, al]).clip(0, 255).astype(np.uint8))


def by_value(v, stops, alpha=None):
    """Colour a 0..1 value field (and an alpha) onto a ramp."""
    rgb = ramp(v, stops)
    al = (v > 0.02) * 255.0 if alpha is None else alpha
    return Image.fromarray(np.dstack([rgb, al]).clip(0, 255).astype(np.uint8))


def src(name):
    return Image.open(os.path.join(DUN, name + ".png")).convert("RGBA")


def cells(im, w, h=None):
    h = h or w
    return [im.crop((c * w, r * h, (c + 1) * w, (r + 1) * h)) for r in range(im.height // h) for c in range(im.width // w)]


def fit(im, size, hard=True, cut=110):
    """Down to size: box filter (premultiplied), then hard alpha for pixel art."""
    a = np.array(im.convert("RGBA")).astype(float)
    pm = a.copy()
    pm[..., :3] *= a[..., 3:4] / 255.0
    small = np.array(Image.fromarray(pm.clip(0, 255).astype(np.uint8)).resize((size, size), Image.BOX)).astype(float)
    al = small[..., 3]
    rgb = np.where(al[..., None] > 0, small[..., :3] * 255.0 / np.maximum(al[..., None], 1), 0)
    if hard:
        al = np.where(al > cut, 255, np.where(al > cut * 0.45, 150, 0))
    return Image.fromarray(np.dstack([rgb, al]).clip(0, 255).astype(np.uint8))


def square(im, pad=0):
    box = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if box is None:
        return Image.new("RGBA", (8, 8))
    im = im.crop(box)
    side = max(im.size) + 2 * pad
    canvas = Image.new("RGBA", (side, side))
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    return canvas


def snap(im, stops):
    """Pixel-art clean-up after a downscale: every colour onto the ramp by its luminance (no muddy mixes)."""
    a = np.array(im).astype(float)
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255.0
    pos = np.array([p for p, _c in stops])
    lums = np.array([(0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255.0 for _p, c in stops])
    idx = np.abs(lum[..., None] - lums).argmin(-1)
    rgb = ramp(pos[idx], stops)
    return Image.fromarray(np.dstack([rgb, a[..., 3]]).clip(0, 255).astype(np.uint8))


# ---------------------------------------------------------------------------
# 原作素材
# ---------------------------------------------------------------------------
def fire_frames(stops, step=1):
    """T_FireBlock1x1: 16 frames of 32x32 fire stacked vertically (orange, painted): luminance onto the ramp."""
    out = []
    for f in cells(src("T_FireBlock1x1"), 32)[::step]:
        out.append(tone(f, stops, 0.18, 0.95))
    return out


def restop(im, src, dst):
    """Swap a ramp for another stop by stop (each pixel takes the stop of src nearest its colour), so the
    outline layers survive the change."""
    a = np.array(im).astype(float)
    sc = np.array([c for _p, c in src], float)
    dc = np.array([c for _p, c in dst], float)
    idx = np.abs(a[..., None, :3] - sc).sum(-1).argmin(-1)
    return Image.fromarray(np.dstack([dc[idx], a[..., 3]]).clip(0, 255).astype(np.uint8))


def flame(stops):
    """The single holy flame (Codex, anim/holyflame_sheet.png, 8 looping frames), snapped to a ramp.  Without the
    sheet: the original fire block, one 16 px tile of each other frame blown up (fallback only)."""
    fr = codex("holyflame_sheet", 8, FIRE, cut=96)
    if fr:
        return fr if stops is FIRE else [restop(f, FIRE, stops) for f in fr]
    return [f.crop((0, 16, 16, 32)).resize((32, 32), Image.NEAREST) for f in fire_frames(stops, 2)]


def tongue_frames():
    """T_FireSide: alpha holds eight flame tongues (two rows, four growth stages, 16 px each); R holds the
    inner shading.  Colour: the core (dark in R) hot, the rim deep."""
    a = np.array(src("T_FireSide")).astype(float)
    out = []
    for r in range(2):
        for c in range(4):
            blk = a[r * 16:(r + 1) * 16, c * 16:(c + 1) * 16]
            al = np.where(blk[..., 3] > 60, 255.0, 0.0)
            v = 1.0 - blk[..., 0] / 255.0 * 0.75
            out.append(by_value(v, FIRE, al))
    return out


def drop_frames():
    a = np.array(src("T_FireDroplet")).astype(float)
    out = []
    for c in range(4):
        blk = a[0:16, c * 16:(c + 1) * 16]
        al = np.where(blk[..., 3] > 60, 255.0, 0.0)
        v = 1.0 - blk[..., 0] / 255.0 * 0.7
        out.append(by_value(v, FIRE, al))
    return out


def feather(stops, lift=0.0):
    return tone(src("T_Feathers"), stops, 0.2, 0.95, lift=lift)


def stars(stops):
    return [tone(f, stops, 0.0, 1.0, alpha=np.array(f)[..., 3].astype(float), lift=0.25) for f in cells(src("T_Stars_16"), 16)]


def rays(stops):
    out = []
    for f in cells(src("T_GodRayLight"), 128):
        small = f.resize((32, 32), Image.BOX)
        a = np.array(small).astype(float)
        v = a[..., 3] / 255.0
        al = np.where(v > 0.55, 255, np.where(v > 0.3, 170, np.where(v > 0.12, 90, 0))).astype(float)
        out.append(by_value(0.5 + 0.5 * np.clip(v * 1.15, 0, 1), stops, al))
    return out


def bursts(stops):
    """T_fullcircle_explosion_124: eight 128 px frames of a ring blowing out; thin line kept, colour cooling
    from white to the deep end of the ramp over the eight frames."""
    out = []
    for i, f in enumerate(cells(src("T_fullcircle_explosion_124_spritesheet"), 128)):
        a = np.array(f)[..., 3].astype(float)
        h = 128 // 32
        al = np.zeros((32, 32))
        for y in range(32):
            for x in range(32):
                if a[y * h:(y + 1) * h, x * h:(x + 1) * h].max() > 60:
                    al[y, x] = 255
        v = np.full((32, 32), 1.0 - i / 9.0)
        out.append(by_value(v, stops, al))
    return out


def doves():
    """T_Doves_Flipbook: 5x5 frames of a dove flying; white with peach shade.  Eight frames of the wing beat."""
    sheet = src("T_Doves_Flipbook")
    side = sheet.width // 5
    frames = cells(sheet, side)
    out = []
    for f in frames[:8]:
        out.append(snap(tone(fit(square(f, 2), 32), HOLY, lift=0.35), HOLY[1:]))
    return out


def arcs(stops, n=6, span=200.0, r0=11.5, thick=6.0, flip=False):
    """A crescent slash swept open over n frames, drawn at 4x and boxed down to 32 px: the arc grows
    along its angle (thick in the middle, tapered ends), white on the inside edge, the ramp's deep end
    outside; the last frames thin out and cool."""
    S = 128
    yy, xx = np.mgrid[0:S, 0:S] + 0.5
    dx, dy = (xx - S / 2) / 4.0, (yy - S / 2) / 4.0
    if flip:
        dx = -dx
    r = np.hypot(dx, dy)
    ang = np.degrees(np.arctan2(dy, dx))          # 0 = right, sweeping through the top
    a0, a1 = -90 - span / 2, -90 + span / 2
    u = (ang - a0) / (a1 - a0)
    out = []
    for i in range(n):
        head = min(1.0, (i + 1) / (n - 2.0))
        fade = max(0, i - (n - 3)) / 2.0
        t = thick * np.sin(np.pi * np.clip(u, 0, 1)) * (1 - 0.55 * fade)
        on = (u >= 0) & (u <= head) & (r >= r0 - t * 0.35) & (r <= r0 + t * 0.65)
        w = np.clip((r - (r0 - t * 0.35)) / np.maximum(t, 1e-3), 0, 1)
        v = (1.0 - w * 0.85) * (1 - 0.35 * fade) * (0.55 + 0.45 * np.clip(u / max(head, 1e-3), 0, 1))
        al = np.where(on, 255.0, 0.0)
        out.append(fit(by_value(v, stops, al), 32, cut=100))
    return out


def smoke():
    """T_SmokeBallVariation: each channel a set of puffs; six puffs, ash dark with an ember rim."""
    a = np.array(src("T_SmokeBallVariation")).astype(float)
    out = []
    for c in (0, 1, 2):
        for k in (0, 1):
            blk = a[k * 32:(k + 1) * 32, 0:32]
            al = np.where(blk[..., 3] > 90, 255.0, np.where(blk[..., 3] > 40, 140.0, 0.0))
            shade = 1.0 - blk[..., c] / 255.0
            out.append(by_value(0.15 + shade * 0.7, ASH, al))
    return out


def flashes():
    """The full-screen gaze flash, four fading frames (white-hot -> peach -> coral -> faint orange).
    A 32x32 glyph; two of them side by side cover the screen (font provider: height 128)."""
    out = []
    for col, al in (((255, 250, 240), 170), ((255, 214, 190), 130), ((255, 150, 110), 90), ((255, 90, 40), 45)):
        a = np.zeros((32, 32, 4), np.uint8)
        a[..., :3] = col
        a[..., 3] = al
        out.append(Image.fromarray(a))
    return out


def vignette():
    """Edge glow for the gaze charge, three strengths.  One 64x32 elliptical falloff (clear middle, red rim)
    split into a left and a right glyph: frames 0-2 are the left halves, 3-5 the right halves.  The pair is
    wider than any screen, so the falloff runs all the way out and the rim shows whatever the aspect."""
    yy, xx = np.mgrid[0:32, 0:64] + 0.5
    r = np.hypot((xx - 32) / 32.0, (yy - 16) / 16.0)
    lefts, rights = [], []
    for strength in (0.4, 0.6, 0.85):
        t = np.clip((r - 0.36) / 0.4, 0, 1) ** 1.3
        al = np.where(t > 0.05, (30 + 170 * t) * strength, 0)
        im = by_value(0.25 + 0.6 * t, RED, al)
        lefts.append(im.crop((0, 0, 32, 32)))
        rights.append(im.crop((32, 0, 64, 32)))
    return lefts + rights


# ---------------------------------------------------------------------------
# Codex 画的专属序列帧（anim/），按透明空隙切
# ---------------------------------------------------------------------------
def split_sheet(path, n):
    im = Image.open(path).convert("RGBA")
    a = np.array(im)[..., 3]
    cols = a.max(axis=0) > 24
    spans, start = [], None
    for x, on in enumerate(list(cols) + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            if x - start > im.width // (n * 6):
                spans.append((start, x))
            start = None
    if len(spans) != n:                                  # fall back to equal cells
        w = im.width // n
        spans = [(i * w, (i + 1) * w) for i in range(n)]
    rows = np.where(a.max(axis=1) > 24)[0]
    y0, y1 = rows.min(), rows.max() + 1
    side = max(max(x1 - x0 for x0, x1 in spans), y1 - y0) + 8
    out = []
    for x0, x1 in spans:
        cx = (x0 + x1) // 2
        cy = (y0 + y1) // 2
        out.append(im.crop((cx - side // 2, cy - side // 2, cx - side // 2 + side, cy - side // 2 + side)))
    return out


def codex(name, n, stops, size=32, cut=100):
    path = os.path.join(ANIM, name + ".png")
    if not os.path.exists(path):
        return None
    return [snap(fit(f, size, cut=cut), stops) for f in split_sheet(path, n)]


def codex_still(name, stops, size=32, cut=90):
    path = os.path.join(ANIM, name + ".png")
    if not os.path.exists(path):
        return None
    return snap(fit(square(Image.open(path).convert("RGBA"), 4), size, cut=cut), stops)


# ---------------------------------------------------------------------------
# 程序画的地面贴花
# ---------------------------------------------------------------------------
def wedge():
    """A 120 degree sector, apex at the centre, opening toward the texture's bottom (model +z): red fill with a hot
    rim.  An item_display at yaw phi shows model +z toward phi + 180 (measured), so the fight turns it by +180."""
    yy, xx = np.mgrid[0:32, 0:32] + 0.5
    dx, dz = xx - 16, yy - 16
    r = np.hypot(dx, dz)
    ang = np.degrees(np.arctan2(dx, dz))
    inside = (np.abs(ang) <= 60) & (r <= 15.5)
    edge = inside & ((np.abs(np.abs(ang) - 60) < 5.5 * 16 / np.maximum(r, 1)) | (r > 14))
    v = np.where(edge, 1.0, 0.55)
    al = np.where(edge, 255.0, np.where(inside & ((xx.astype(int) + yy.astype(int)) % 2 == 0), 170.0, np.where(inside, 100.0, 0)))
    return by_value(v, RED, al)


def xmark():
    yy, xx = np.mgrid[0:32, 0:32] + 0.5
    d1 = np.abs((xx - 16) - (yy - 16)) / np.sqrt(2)
    d2 = np.abs((xx - 16) + (yy - 16)) / np.sqrt(2)
    r = np.hypot(xx - 16, yy - 16)
    d = np.minimum(d1, d2)
    on = (d < 1.6) & (r < 15)
    rim = (d < 2.6) & (r < 15.5) & ~on
    v = np.where(on, 1.0, 0.4)
    al = np.where(on, 255.0, np.where(rim, 150.0, 0.0))
    return by_value(v, FIRE, al)


def ring(stops, width=1.4, r0=14.5, inner=True):
    yy, xx = np.mgrid[0:32, 0:32] + 0.5
    r = np.hypot(xx - 16, yy - 16)
    on = np.abs(r - r0) < width
    glow = (np.abs(r - r0 + 1.8) < 1.0) & ~on & inner
    v = np.where(on, 0.95, 0.55)
    al = np.where(on, 255.0, np.where(glow, 110.0, 0.0))
    return by_value(v, stops, al)


def scorch():
    """A burnt crater: the original crack lines in deep ember over a dark ring, faintly glowing."""
    c = np.array(src("T_Cracks").resize((32, 32), Image.BOX))[..., 3].astype(float) / 255.0
    yy, xx = np.mgrid[0:32, 0:32] + 0.5
    r = np.hypot(xx - 16, yy - 16) / 16.0
    soot = np.clip(1.0 - r, 0, 1)
    al = np.where(c > 0.2, 230.0, np.where(soot > 0.35, 140.0 * soot, 0.0))
    v = np.where(c > 0.2, 0.75 + 0.25 * (1 - r), 0.15 * soot)
    return by_value(v, ASH, al)


def embers(frames=8):
    """Animated burning ground for the fire path: dissolve noise rolled each frame, ember colours."""
    n = np.array(src("T_Dissolve_32"))[..., 1].astype(float) / 255.0
    strip = []
    for f in range(frames):
        m = np.roll(n, f * 4, axis=0)
        m2 = np.roll(n[::-1], f * 2, axis=1)
        v = np.clip((m * 0.6 + m2 * 0.6) - 0.2, 0, 1)
        al = np.where(v > 0.5, 255.0, np.where(v > 0.3, 150.0, 0.0))
        strip.append(by_value(v, FIRE, al))
    return strip


def lane(stops):
    """A ground telegraph strip (v runs along the line): hot centre stripe, dithered rim, a rune tick every
    eight texels; scaled (width, 1, length) at run time."""
    yy, xx = np.mgrid[0:32, 0:32]
    d = np.abs(xx + 0.5 - 16)
    core = d < 3
    rim = (d >= 3) & (d < 9) & ((xx + yy) % 2 == 0)
    edge = (d >= 13) & (d < 15)
    tick = (yy % 8 == 0) & (d < 11)
    v = np.where(core, 1.0, np.where(tick, 0.85, np.where(edge, 0.6, 0.45)))
    al = np.where(core | tick | edge, 255.0, np.where(rim, 130.0, 0.0))
    return by_value(v, stops, al)


def glow(stops):
    yy, xx = np.mgrid[0:32, 0:32] + 0.5
    r = np.hypot(xx - 16, yy - 16) / 16.0
    v = np.clip(1.0 - r, 0, 1)
    dither = ((xx.astype(int) + yy.astype(int)) % 2 == 0)
    al = np.where(v > 0.55, 200.0, np.where(v > 0.3, 140.0, np.where((v > 0.08) & dither, 90.0, 0.0)))
    return by_value(0.35 + v * 0.65, stops, al)


# ---------------------------------------------------------------------------
GLYPHS = [
    # 名字, 尺寸, 帧组（函数）
    # 圣焰：Codex 画的单簇火焰八帧循环（用户 2026-11-18：原作方块火每帧是四簇小火拼的，太潦草）；一阶段同一组帧换成暖白金
    ("fire", 32, lambda: flame(FIRE)),
    ("fireh", 32, lambda: flame(HOLY)),
    ("tongue", 16, tongue_frames),                           # 火舌 8 帧（两行四级）
    ("drop", 16, drop_frames),                               # 火滴 4 帧
    ("feather", 16, lambda: [feather(HOLY, 0.1), feather(FIRE, 0.05)]),
    ("star", 16, lambda: stars(HOLY)),
    ("starf", 16, lambda: stars(FIRE)),
    ("ray", 32, lambda: rays(HOLY)),
    ("rayf", 32, lambda: rays(FIRE)),
    ("burst", 32, lambda: bursts(HOLY)),
    ("burstf", 32, lambda: bursts(FIRE)),
    ("dove", 32, doves),
    ("arc", 32, lambda: arcs(HOLY)),
    ("arcf", 32, lambda: arcs(FIRE, thick=7.0, span=160.0)),
    ("arcw", 32, lambda: arcs(HOLY, n=6, span=300.0, r0=12.5, thick=4.5)),       # 横扫的 270° 大弧
    ("smoke", 32, smoke),
    ("flash", 32, flashes),
    ("vig", 32, vignette),
    # Codex
    ("eye", 32, lambda: codex("eye_open_sheet", 6, FIRE)),
    ("gaze", 32, lambda: codex("eye_gaze_sheet", 4, FIRE)),
    ("wings", 32, lambda: codex("wingburst_sheet", 6, FIRE)),
    ("fburn", 32, lambda: codex("feather_burn_sheet", 6, FIRE)),
    ("meteor", 32, lambda: codex("meteor_sheet", 4, FIRE)),
    ("column", 32, lambda: codex("firecolumn_sheet", 6, FIRE)),
    ("spike", 32, lambda: codex("bonespike_sheet", 6, ((0.0, (0x5A, 0x3A, 0x2A)),) + HOLY[1:])),
    ("xslash", 32, lambda: codex("crossslash_sheet", 6, FIRE)),
    ("halo", 32, lambda: codex("halo_sheet", 6, FIRE)),
]

# 全屏字形（flash / vig）：两张并排盖满屏幕；其余字形以实体为中心
FULL = {"flash", "vig"}


_TABLE = None


def frames_all():
    out = {}
    for name, size, fn in GLYPHS:
        fr = fn()
        if fr:
            out[name] = (size, fr)
    return out


def glyph_table():
    """name -> (first code point, size, frame count).  Counts are fixed so the fight generator and the
    art agree even before Codex delivers (a missing sheet still reserves its codes)."""
    global _TABLE
    if _TABLE is None:
        counts = {"fire": 8, "fireh": 8, "tongue": 8, "drop": 4, "feather": 2, "star": 4, "starf": 4, "ray": 4, "rayf": 4,
                  "burst": 8, "burstf": 8, "dove": 8, "arc": 6, "arcf": 6, "arcw": 6, "smoke": 6, "flash": 4, "vig": 6,
                  "eye": 6, "gaze": 4, "wings": 6, "fburn": 6, "meteor": 4, "column": 6, "spike": 6, "xslash": 6, "halo": 6}
        _TABLE, code = {}, GLYPH_BASE
        for name, size, _fn in GLYPHS:
            _TABLE[name] = (code, size, counts[name])
            code += STRIDE
    return _TABLE


def glyph_text(name, frame=0):
    return chr(glyph_table()[name][0] + frame)


def full_text(name, frame=0):
    """Two glyphs side by side with the 1 px advance gap closed (space char U+F801 = -1): the same glyph twice,
    or for the vignette its left and right halves."""
    if name == "vig":
        return glyph_text(name, frame) + "\uf801" + glyph_text(name, frame + 3)
    g = glyph_text(name, frame)
    return g + "\uf801" + g


DECALS = {
    "ring_h": lambda: ring(HOLY),
    "ring_f": lambda: ring(FIRE),
    "ring_t": lambda: ring(FIRE, 0.7, 15.0, inner=False),                    # 往外长到几十格的环：只画一道细线
    "ring_r": lambda: ring(((0.0, (0x5A, 0x0E, 0x00)), (1.0, (0xC8, 0x28, 0x00))), 0.75, 15.0, inner=False),     # 大圈预警：细、暗
    "lane_h": lambda: lane(HOLY),
    "lane_f": lambda: lane(FIRE),
    "lane_r": lambda: lane(RED),
    "glow_h": lambda: glow(HOLY),
    "glow_f": lambda: glow(FIRE),
    "wedge": wedge,
    "xmark": xmark,
    "scorch": scorch,
    "seal_seraph": lambda: codex_still("seal_seraph", HOLY),
    "seal_eye": lambda: codex_still("seal_eye", FIRE),
    "seal_trumpet": lambda: codex_still("seal_trumpet", HOLY),
}
for _i in range(8):
    DECALS["shock_%d" % _i] = (lambda i: lambda: bursts(FIRE)[i])(_i)
    DECALS["shockh_%d" % _i] = (lambda i: lambda: bursts(HOLY)[i])(_i)
ANIMATED = {
    "embers": (embers, 2),
    "firering": (lambda: codex("sanctus_ring_sheet", 4, FIRE), 3),
}


def plane_model(texture, both=False):
    face = {"uv": [0, 0, 16, 16], "texture": "#0", "tintindex": 0}
    faces = {"up": dict(face)}
    if both:
        faces["down"] = dict(face, uv=[0, 16, 16, 0])
    return {"textures": {"0": texture, "particle": texture},
            "elements": [{"from": [0, 8, 0], "to": [16, 8, 16], "faces": faces, "shade": False, "light_emission": 15}]}


def core():
    """The white-hot core of a light shaft: white middle, peach edge (u across, v along)."""
    yy, xx = np.mgrid[0:16, 0:16]
    d = np.abs(xx + 0.5 - 8) / 8.0
    v = np.clip(1.0 - d * 0.6, 0, 1)
    al = np.where(d < 0.75, 255.0, 160.0)
    return by_value(v, HOLY, al)


def box_model(texture):
    face = {"uv": [0, 0, 16, 16], "texture": "#0", "tintindex": 0}
    faces = dict((k, dict(face)) for k in ("north", "south", "east", "west", "up", "down"))
    return {"textures": {"0": texture, "particle": texture},
            "elements": [{"from": [0, 0, 0], "to": [16, 16, 16], "light_emission": 15, "shade": False, "faces": faces}]}


def write_item(rp, name, model):
    dm.wj(os.path.join(rp, "assets", "rpg", "models", KEY, name + ".json"), model)
    dm.wj(os.path.join(rp, "assets", "rpg", "items", KEY, name + ".json"), {
        "model": {"type": "minecraft:model", "model": "rpg:%s/%s" % (KEY, name),
                  "tints": [{"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]}})


def contact_sheet(path, glyphs, decals):
    rows = []
    for name, (size, fr) in glyphs.items():
        rows.append((name, fr))
    for name, im in decals.items():
        rows.append((name, im if isinstance(im, list) else [im]))
    k, cell = 4, 32 * 4 + 6
    W = 120 + cell * 16
    sheet = Image.new("RGBA", (W, len(rows) * cell), (26, 22, 30, 255))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for r, (name, fr) in enumerate(rows):
        d.text((6, r * cell + cell // 2 - 6), name, fill=(255, 230, 200, 255))
        for i, im in enumerate(fr[:16]):
            big = im.resize((im.width * (128 // im.width), im.height * (128 // im.width)), Image.NEAREST)
            sheet.alpha_composite(big, (120 + i * cell, r * cell + 3))
    sheet.save(path)


def main():
    rp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "resourcepack")
    tex_dir = os.path.join(rp, "assets", "rpg", "textures", "item", KEY)
    font_dir = os.path.join(rp, "assets", "rpg", "textures", "font", KEY)
    os.makedirs(tex_dir, exist_ok=True)
    os.makedirs(font_dir, exist_ok=True)
    table = glyph_table()
    glyphs = frames_all()
    providers = [{"type": "space", "advances": {"\uf801": -1}}]
    missing = []
    for name, size, _fn in GLYPHS:
        code, sz, count = table[name]
        if name not in glyphs:
            missing.append(name)
            continue
        _s, fr = glyphs[name]
        assert len(fr) == count, (name, len(fr), count)
        for i, im in enumerate(fr):
            assert im.size == (size, size), (name, im.size)
            im.save(os.path.join(font_dir, "%s_%d.png" % (name, i)))
            if name in FULL:
                prov = {"height": 128, "ascent": 64}
            else:
                prov = {"height": size, "ascent": size // 2 - 3}
            providers.append(dict({"type": "bitmap", "file": "rpg:font/%s/%s_%d.png" % (KEY, name, i),
                                   "chars": [chr(code + i)]}, **prov))
    dm.wj(os.path.join(rp, "assets", "rpg", "font", KEY + ".json"), {"providers": providers})
    decals = {}
    for name, fn in DECALS.items():
        im = fn()
        if im is None:
            missing.append(name)
            continue
        assert im.size == (32, 32), (name, im.size)
        decals[name] = im
        im.save(os.path.join(tex_dir, name + ".png"))
        write_item(rp, name, plane_model("rpg:item/%s/%s" % (KEY, name), both=name.startswith("seal")))
    for name, (fn, ft) in ANIMATED.items():
        fr = fn()
        if not fr:
            missing.append(name)
            continue
        strip = Image.new("RGBA", (32, 32 * len(fr)))
        for i, im in enumerate(fr):
            strip.paste(im, (0, 32 * i))
        strip.save(os.path.join(tex_dir, name + ".png"))
        dm.wj(os.path.join(tex_dir, name + ".png.mcmeta"), {"animation": {"frametime": ft}})
        write_item(rp, name, plane_model("rpg:item/%s/%s" % (KEY, name)))
        decals[name] = fr
    core().save(os.path.join(tex_dir, "core.png"))
    write_item(rp, "core", box_model("rpg:item/%s/core" % KEY))
    contact_sheet(os.path.join(REF, "contact_sheet.png"), glyphs, decals)
    print("michael fx art: %d glyph frames in %d sets, %d decals%s" % (
        len(providers) - 1, len(glyphs), len(decals), (" (missing: %s)" % ", ".join(missing)) if missing else ""))


if __name__ == "__main__":
    main()
