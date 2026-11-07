# -*- coding: utf-8 -*-
"""教皇战的特效贴图、模型和字形。母图在 pope_fx_ref/raw/，由 Codex 绘制。

    python add_pope_fx_art.py ../resourcepack

Two carriers, because of how the client lights things (measured in a real
client, 2026-11-05):

* item_display goes through the normal-based item lighting whatever the model's
  `shade` says: only an up face is at full brightness, side faces drop to 50-74%.
  So item models are for ground decals (up faces) and for solid objects.
* text_display is unlit, so anything that must read as light is a bitmap glyph.
  A glyph has one visible side.

Everything lands on a coarse pixel grid with a few colours (ART-STYLE §0.3).
The generated masters are only the drawing; palette and grid are decided here.

The image tool makes no GIFs, so a motion is one image of frames set side by
side, cut here at the empty gaps between them.  Item decals animate through
.mcmeta.  Fonts cannot, so a glyph animation is a run of codepoints the fight
steps through (add_pope_fight.py).
"""

import io
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import rpg_ui_style as ui

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "pope_fx_ref", "raw")
ANIM = os.path.join(HERE, "pope_fx_ref", "anim")
STARS = os.path.join(HERE, "heart_of_ender_ref", "MCD_Decal_Puddle_(texture).png")

FONT = "rpg:pope_fx"
TEXT_UNIT = 0.025       # blocks per glyph pixel at scale 1

# name: (first codepoint, width, height)
GLYPHS = {
    "halo": (0xE100, 64, 64),
    "halo_arc": (0xE10F, 32, 32),
    "orb": (0xE110, 24, 24),
    "column": (0xE120, 32, 128),
    "flare": (0xE130, 64, 64),
    "beam": (0xE140, 64, 8),
    "impact": (0xE150, 48, 48),
    "impact_void": (0xE160, 48, 48),
    "vortex": (0xE170, 48, 96),
    "beam_gold": (0xE180, 64, 8),
    "vortex_void": (0xE190, 48, 96),
    "slash": (0xE1A0, 64, 64),
}
# name: (sheet in ANIM, frames, stacked top to bottom)
SHEETS = {
    "halo": ("halo_sheet", 6, False), "orb": ("orb_sheet", 8, False), "column": ("column_sheet", 6, False),
    "flare": ("flare_sheet", 6, False), "beam": ("beam_sheet", 6, True), "impact": ("impact_sheet", 8, False),
    "impact_void": ("impact_void_sheet", 8, False), "vortex": ("vortex_sheet", 6, False),
    # the same drawing in the other side's colours
    "beam_gold": ("beam_sheet", 6, True), "vortex_void": ("vortex_sheet", 6, False),
    "slash": ("slash_sheet", 6, False),
}
# The boss bar is one bitmap, one glyph per step of health, because the vanilla
# bar is 5 GUI units high and cannot have this shape.  The vanilla bar is hidden
# (pink, transparent here).  One texture pixel is one GUI unit: chunky on purpose.
BAR_W, BAR_H = 240, 36
BAR_ASCENT = 10         # a name is drawn at y 3, so this puts the top at the screen's edge
BAR_FIRST = 0xE200
# kind: (body colour, emblem, title, steps)
BANNERS = {
    "guard": ("gold", "emblem_guard", "guard", 4),
    "pope": ("gold", "emblem_pope", "pope", 20),
    "heart": ("void", "emblem_heart", "heart", 20),
    "weak": ("gold", "emblem_heart", "heart", 20),
}
BAR_MID = 15            # the banner's centre line
BAR_RISE = 9            # half the main body's height
BAR_TIP = 18            # length of its tapered ends: two across for one down, as in font/story
BAR_GEM = 8             # half the width of the small diamonds
BAR = os.path.join(HERE, "pope_fx_ref", "bar")
HIDDEN_BAR = "pink"

# titles sit under the banner: drawn fine, shown at 11 GUI units high
TITLE_PIXELS = 32        # a whole multiple of TITLE_HEIGHT, or thin strokes drop out
TITLE_MAX_WIDTH = 252   # a font page is 256 wide
TITLE_HEIGHT = 8
TITLE_ASCENT = -28
TITLES = {"guard": 0xE1F0, "pope": 0xE1F1, "heart": 0xE1F2}
TITLE_BACK = {"guard": 0xE1F4, "pope": 0xE1F5, "heart": 0xE1F6}
TITLE_ON = {"guard": 0xE1F8, "pope": 0xE1F9, "heart": 0xE1FA}


def bar_code(kind, step):
    return BAR_FIRST + list(BANNERS).index(kind) * 32 + step


def bar_text(kind, step):
    """Banner, step back to the middle, title, step on to the banner's end."""
    title = BANNERS[kind][2]
    return "".join(chr(c) for c in (bar_code(kind, step), TITLE_BACK[title], TITLES[title], TITLE_ON[title]))
DECALS = {"seal_outer": 96, "seal_inner": 96, "mark_ring": 64}
FAINT = {"seal_outer": "doom_outer", "seal_inner": "doom_inner"}
FAINT_ALPHA = 0.4
MARK_FRAMES = 6
OBJECTS = {"shard_a": 16, "shard_b": 16, "shard_c": 16}
PUDDLE_SIZE = 128
PUDDLE_FRAMES = 4
STAR_CROP = 300         # the source has marker rows further down


def rgb(hexcolour):
    h = ui.hex_of(hexcolour).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def scaled(colour, k):
    return tuple(int(c * k) for c in colour)


WHITE = (255, 255, 255)
HOLY_RAMP = [WHITE, rgb(ui.HOLY_LIGHT), rgb(ui.HOLY), rgb(ui.HOLY_DARK)]
VOID = rgb(ui.RITUAL)
VOID_RAMP = [WHITE, VOID, scaled(VOID, 0.62), scaled(VOID, 0.34)]
ALPHAS = np.array([0, 110, 180, 255])
BAR_RAMPS = {
    "gold": [rgb(ui.HOLY_LIGHT), rgb(ui.HOLY), rgb(ui.HOLY_DARK), scaled(rgb(ui.HOLY_DARK), 0.7)],
    "void": [scaled(VOID, 1.0), scaled(VOID, 0.8), scaled(VOID, 0.6), scaled(VOID, 0.42)],
}

RAMPS = {
    "seal_outer": HOLY_RAMP, "seal_inner": HOLY_RAMP, "halo": HOLY_RAMP, "halo_arc": HOLY_RAMP,
    "orb": HOLY_RAMP, "column": HOLY_RAMP, "impact": HOLY_RAMP, "vortex": HOLY_RAMP,
    "mark_ring": VOID_RAMP, "flare": VOID_RAMP, "beam": VOID_RAMP, "impact_void": VOID_RAMP,
    "beam_gold": HOLY_RAMP, "vortex_void": VOID_RAMP, "slash": HOLY_RAMP,
}
STRETCH = {"column", "beam", "beam_gold"}    # fill the grid; everything else keeps its proportions


def trimmed(path):
    im = Image.open(path).convert("RGBA")
    box = im.getchannel("A").point(lambda a: 255 if a > 24 else 0).getbbox()
    if box is None:
        raise SystemExit("%s is empty or has no transparency" % path)
    return im.crop(box)


def runs(on):
    """Start and end of each stretch of True."""
    edges = np.flatnonzero(np.diff(np.concatenate(([0], on.astype(np.int8), [0]))))
    return list(zip(edges[::2], edges[1::2]))


def cut(path, count, stacked):
    """Split a sheet at its empty gaps.  Debris makes extra stretches: close the narrowest gaps."""
    im = Image.open(path).convert("RGBA")
    solid_px = np.asarray(im.getchannel("A")) > 24
    spans = runs(solid_px.any(axis=1 if stacked else 0))
    while len(spans) > count:
        gaps = [spans[i + 1][0] - spans[i][1] for i in range(len(spans) - 1)]
        i = gaps.index(min(gaps))
        spans[i:i + 2] = [(spans[i][0], spans[i + 1][1])]
    if len(spans) < count:      # frames that touch: equal shares of the drawn extent
        lo, hi = spans[0][0], spans[-1][1]
        step = (hi - lo) / float(count)
        spans = [(int(lo + i * step), int(lo + (i + 1) * step)) for i in range(count)]
    out = []
    for lo, hi in spans:
        box = (0, lo, im.width, hi) if stacked else (lo, 0, hi, im.height)
        piece = im.crop(box)
        out.append(piece.crop(piece.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()))
    return out


def fit_frames(pieces, w, h, stretch):
    """One scale for every frame, so a pulse stays a pulse."""
    if stretch:
        return [_box(p, w, h) for p in pieces]
    k = min(float(w) / max(p.width for p in pieces), float(h) / max(p.height for p in pieces))
    out = []
    for p in pieces:
        nw, nh = max(1, round(p.width * k)), max(1, round(p.height * k))
        canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        canvas.paste(_box(p, nw, nh), ((w - nw) // 2, (h - nh) // 2))
        out.append(canvas)
    return out


def fit(im, w, h, stretch):
    """Premultiplied box filter onto the grid."""
    if stretch:
        return _box(im, w, h)
    k = min(float(w) / im.width, float(h) / im.height)
    nw, nh = max(1, round(im.width * k)), max(1, round(im.height * k))
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(_box(im, nw, nh), ((w - nw) // 2, (h - nh) // 2))
    return canvas


def _box(im, w, h):
    a = np.asarray(im, dtype=np.float32) / 255.0
    a = np.dstack([a[..., :3] * a[..., 3:], a[..., 3]])
    small = Image.fromarray((a * 255).astype(np.uint8), "RGBA").resize((w, h), Image.BOX)
    b = np.asarray(small, dtype=np.float32) / 255.0
    alpha = b[..., 3:]
    colour = np.where(alpha > 0, b[..., :3] / np.maximum(alpha, 1e-3), 0)
    out = np.dstack([np.clip(colour, 0, 1), alpha])
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


def snap(im, ramp):
    """Nearest ramp tone by brightness; four alpha levels."""
    a = np.asarray(im, dtype=np.float32)
    tones = np.array(ramp, dtype=np.float32)
    luma = lambda c: c[..., 0] * 0.3 + c[..., 1] * 0.59 + c[..., 2] * 0.11
    d = np.abs(luma(a[..., :3])[..., None] - luma(tones))
    picked = tones[np.argmin(d, axis=-1)]
    alpha = ALPHAS[np.argmin(np.abs(a[..., 3:] - ALPHAS), axis=-1)]
    out = np.dstack([picked, alpha]).astype(np.uint8)
    out[alpha == 0] = 0
    return Image.fromarray(out, "RGBA")


def inside(im, threshold=60):
    """Pixels the drawing encloses.  The edge is grown a pixel so a nick does not leak."""
    edge = np.asarray(im.getchannel("A").point(lambda v: 255 if v > threshold else 0)
                      .filter(ImageFilter.MaxFilter(3))) > 0
    out = np.zeros(edge.shape, bool)
    out[0, :] = out[-1, :] = True
    out[:, 0] = out[:, -1] = True
    out &= ~edge
    while True:
        grown = out.copy()
        grown[1:, :] |= out[:-1, :]
        grown[:-1, :] |= out[1:, :]
        grown[:, 1:] |= out[:, :-1]
        grown[:, :-1] |= out[:, 1:]
        grown &= ~edge
        if (grown == out).all():
            return ~out
        out = grown


def filled(im, colour, reach):
    """The master came back with its middle empty: close it, as far out as `reach`."""
    a = np.array(im)
    h, w = a.shape[:2]
    ys, xs = np.mgrid[0:h, 0:w]
    hole = inside(im) & (a[..., 3] < 200) & (np.hypot(xs - w / 2.0 + 0.5, ys - h / 2.0 + 0.5) <= reach)
    a[hole] = colour + (255,)
    return Image.fromarray(a, "RGBA")


def veined(im):
    """A see-through disc: only the cracks and the rim stay solid."""
    a = np.array(im, dtype=np.float32)
    tone = a[..., 0] + a[..., 2]
    lo, hi = np.percentile(tone[a[..., 3] > 0], (40, 97))
    level = np.clip((tone - lo) / max(hi - lo, 1), 0, 1)
    out = np.zeros(a.shape, np.uint8)
    solid_px = a[..., 3] > 110
    out[solid_px, :3] = VOID_RAMP[2]
    out[solid_px, 3] = 110
    bright = solid_px & (level > 0.55)
    out[bright, :3] = VOID
    out[bright, 3] = 255
    return Image.fromarray(out, "RGBA")


def solid(im, colours=12):
    """A solid object keeps its own colours, reduced, with a hard edge."""
    a = np.array(im)
    a[..., 3] = np.where(a[..., 3] > 110, 255, 0)
    hard = Image.fromarray(a, "RGBA")
    flat = hard.convert("RGB").quantize(colours, dither=Image.NONE).convert("RGB")
    out = flat.convert("RGBA")
    out.putalpha(hard.getchannel("A"))
    return out


def stars_frame(frame):
    """The original star field, one pixel a star; its channels are layers that take turns."""
    src = np.asarray(Image.open(STARS).convert("RGB"), dtype=np.uint8)
    cell = STAR_CROP // PUDDLE_SIZE
    sky = np.zeros((PUDDLE_SIZE, PUDDLE_SIZE), bool)
    ys, xs = np.nonzero(src[:STAR_CROP, :STAR_CROP, 1 if frame % 2 else (2 if frame < 2 else 0)] > 50)
    sky[np.minimum(ys // cell, PUDDLE_SIZE - 1), np.minimum(xs // cell, PUDDLE_SIZE - 1)] = True
    return sky


def puddle():
    drawn = fit(trimmed(os.path.join(RAW, "puddle.png")), PUDDLE_SIZE, PUDDLE_SIZE, False)
    rim = np.array(snap(drawn, [scaled(VOID, 0.06), scaled(VOID, 0.3), VOID]))
    pool = inside(drawn)
    ground = rim[..., 3] > 110
    bright = ground & (rim[..., :3].sum(axis=-1) > 90)
    tones = np.zeros(rim.shape, np.uint8)
    tones[pool | ground] = scaled(VOID, 0.06) + (255,)
    tones[bright & ~(pool & ~ground)] = scaled(VOID, 0.3) + (255,)
    strip = Image.new("RGBA", (PUDDLE_SIZE, PUDDLE_SIZE * PUDDLE_FRAMES))
    for f in range(PUDDLE_FRAMES):
        a = tones.copy()
        a[stars_frame(f) & pool & ~bright, :3] = WHITE if f % 2 else VOID
        strip.paste(Image.fromarray(a, "RGBA"), (0, PUDDLE_SIZE * f))
    return strip


def dump(path, obj):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)


def save(im, path):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    im.save(path)


def item_def(rp, name):
    dump(os.path.join(rp, "items", "pope_fx", name + ".json"), {"model": {
        "type": "minecraft:model", "model": "rpg:pope_fx/" + name,
        "tints": [{"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]}})


def model(rp, name, texture, elements):
    tex = "rpg:item/pope_fx/" + texture
    dump(os.path.join(rp, "models", "pope_fx", name + ".json"),
         {"textures": {"0": tex, "particle": tex}, "elements": elements})
    item_def(rp, name)


def decal_elements():
    face = {"uv": [0, 0, 16, 16], "texture": "#0", "tintindex": 0}
    return [{"from": [0, 8, 0], "to": [16, 8, 16], "light_emission": 15, "shade": False, "faces": {"up": face}}]


def line_elements():
    face = {"uv": [0, 0, 16, 16], "texture": "#0", "tintindex": 0}
    faces = dict((k, dict(face)) for k in ("north", "south", "east", "west", "up", "down"))
    return [{"from": [0, 0, 0], "to": [16, 16, 16], "light_emission": 15, "shade": False, "faces": faces}]


def chain_elements():
    """A ring of eight straight runs around the model's centre."""
    half = 3.3
    out = []
    for turn in (0, 45):
        for (a, b) in (((8 - half, 7, 0.5), (8 + half, 9, 1.5)), ((8 - half, 7, 14.5), (8 + half, 9, 15.5)),
                       ((0.5, 7, 8 - half), (1.5, 9, 8 + half)), ((14.5, 7, 8 - half), (15.5, 9, 8 + half))):
            along_x = b[0] - a[0] > b[2] - a[2]
            long_uv = {"uv": [0, 0, 16, 8], "texture": "#0", "tintindex": 0}
            end_uv = {"uv": [0, 0, 2, 8], "texture": "#0", "tintindex": 0}
            faces = {"up": long_uv, "down": long_uv}
            if along_x:
                faces.update(north=long_uv, south=long_uv, east=end_uv, west=end_uv)
            else:
                faces.update(east=long_uv, west=long_uv, north=end_uv, south=end_uv)
            e = {"from": list(a), "to": list(b), "faces": faces}
            if turn:
                e["rotation"] = {"origin": [8, 8, 8], "axis": "y", "angle": 45}
            out.append(e)
    return out


def bar_shape():
    """The author's banner from font/story: a long diamond and a small one each side."""
    ys, xs = np.mgrid[0:BAR_H, 0:BAR_W]
    rows = np.abs(ys - BAR_MID + 0.5)
    left, right = 2 * BAR_GEM + 3, BAR_W - 2 * BAR_GEM - 4
    body = (rows < np.minimum(BAR_RISE, (np.minimum(xs - left, right - xs) + 1) / 2.0))
    gems = (rows < (BAR_GEM - np.abs(xs - BAR_GEM + 0.5)) / 2.0 + 0.5) & (xs < 2 * BAR_GEM)
    return body | gems | gems[:, ::-1]


def bar_body(ramp):
    shape = bar_shape()
    ys = np.mgrid[0:BAR_H, 0:BAR_W][0]
    top = ys - (BAR_MID - BAR_RISE)
    tone = np.clip(top * len(ramp) // (2 * BAR_RISE), 0, len(ramp) - 1)
    # the darker slanted face along the bottom
    xs = np.mgrid[0:BAR_H, 0:BAR_W][1]
    face = top + np.abs(xs - BAR_W // 2) // 32 > 2 * BAR_RISE - 5
    tone[face] = len(ramp) - 1
    gems = (xs < 2 * BAR_GEM) | (xs >= BAR_W - 2 * BAR_GEM)
    tone[gems] = np.clip((ys[gems] - (BAR_MID - BAR_GEM // 2)) * (len(ramp) - 1) // BAR_GEM, 0, len(ramp) - 1)
    out = np.zeros((BAR_H, BAR_W, 4), np.uint8)
    edge = np.asarray(Image.fromarray((shape * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))) > 0
    under = edge | np.roll(edge, 1, axis=0)     # the hard shadow under each shape
    out[under] = (0, 0, 0, 255)
    out[shape] = np.dstack([np.array(ramp, np.uint8)[tone], np.full((BAR_H, BAR_W), 255, np.uint8)])[shape]
    return out, shape


def banner(kind, step):
    body_colour, emblem_name, _, steps = BANNERS[kind]
    a, shape = bar_body(BAR_RAMPS[body_colour])
    columns = np.flatnonzero(shape.any(axis=0))
    split = columns[0] + (columns[-1] + 1 - columns[0]) * step // steps
    # what has been lost goes dark, from the right; the outline stays
    lost = shape.copy()
    lost[:, :split] = False
    a[lost, :3] = (a[lost, :3] * 0.16).astype(np.uint8) + 12
    out = Image.fromarray(a, "RGBA")
    drawn = trimmed(os.path.join(BAR, emblem_name + ".png"))
    width = max(1, round(drawn.width * float(BAR_H) / drawn.height))
    small = solid(_box(drawn, width, BAR_H), 12)
    out.alpha_composite(small, ((BAR_W - width) // 2, 0))
    return out


def hide_vanilla_bar(pack):
    empty = Image.new("RGBA", (182, 5), (0, 0, 0, 0))
    for part in ("background", "progress"):
        save(empty, os.path.join(pack, "assets", "minecraft", "textures", "gui", "sprites", "boss_bar",
                                 "%s_%s.png" % (HIDDEN_BAR, part)))


def stream_music(pack):
    """Long tracks stream from disk: decoded whole they stall the client on first play."""
    path = os.path.join(pack, "assets", "minecraft", "sounds.json")
    with io.open(path, encoding="utf-8-sig") as fh:
        sounds = json.load(fh)
    for event in ("boss1", "boss2", "boss3"):
        entry = sounds[event]["sounds"][0]
        name = entry["name"] if isinstance(entry, dict) else entry
        sounds[event]["sounds"][0] = {"name": name, "stream": True}
    dump(path, sounds)


def main():
    pack = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    stream_music(pack)
    hide_vanilla_bar(pack)
    rp = os.path.join(pack, "assets", "rpg")
    tex = os.path.join(rp, "textures", "item", "pope_fx")

    providers = []
    for name, (code, w, h) in GLYPHS.items():
        if name in SHEETS:
            sheet, count, stacked = SHEETS[name]
            pieces = fit_frames(cut(os.path.join(ANIM, sheet + ".png"), count, stacked), w, h, name in STRETCH)
        else:
            pieces = [fit(trimmed(os.path.join(RAW, name + ".png")), w, h, False)]
        for i, piece in enumerate(pieces):
            stem = "%s_%d" % (name, i)
            im = snap(piece, RAMPS[name])
            if name in ("beam", "beam_gold"):      # moving light over the steady beam, or it reads as gaps at range
                im = Image.alpha_composite(snap(fit(trimmed(os.path.join(RAW, "beam.png")), w, h, True), RAMPS[name]), im)
            save(im, os.path.join(rp, "textures", "font", "pope_fx", stem + ".png"))
            # top of a glyph sits at -3-ascent in text units, which centres it on the entity
            providers.append({"type": "bitmap", "file": "rpg:font/pope_fx/%s.png" % stem,
                              "height": h, "ascent": h // 2 - 3, "chars": [chr(code + i)]})
    advances = {}
    for kind, (_, _, _, steps) in BANNERS.items():
        for step in range(steps + 1):
            stem = "bar_%s_%d" % (kind, step)
            save(banner(kind, step), os.path.join(rp, "textures", "font", "pope_fx", stem + ".png"))
            providers.append({"type": "bitmap", "file": "rpg:font/pope_fx/%s.png" % stem,
                              "height": BAR_H, "ascent": BAR_ASCENT, "chars": [chr(bar_code(kind, step))]})
    for name, code in TITLES.items():
        drawn = trimmed(os.path.join(ANIM, "title_en_%s.png" % name))
        pixels = min(TITLE_PIXELS, TITLE_MAX_WIDTH * drawn.height // drawn.width)
        width = round(drawn.width * float(pixels) / drawn.height)
        letters = np.array(_box(drawn, width, pixels))
        letters[..., 3] = np.where(letters[..., 3] > 110, 255, 0)
        save(Image.fromarray(letters, "RGBA"), os.path.join(rp, "textures", "font", "pope_fx", "title_%s.png" % name))
        providers.append({"type": "bitmap", "file": "rpg:font/pope_fx/title_%s.png" % name,
                          "height": TITLE_HEIGHT, "ascent": TITLE_ASCENT, "chars": [chr(code)]})
        shown = width * TITLE_HEIGHT // pixels + 1
        advances[chr(TITLE_BACK[name])] = -(BAR_W + 1 + shown) // 2
        advances[chr(TITLE_ON[name])] = (BAR_W + 1 - shown) // 2
    providers.append({"type": "space", "advances": advances})
    dump(os.path.join(rp, "font", "pope_fx.json"), {"providers": providers})

    for name, size in DECALS.items():
        drawn = fit(trimmed(os.path.join(RAW, name + ".png")), size, size, False)
        save(snap(drawn, RAMPS[name]), os.path.join(tex, name + ".png"))
        model(rp, name, name, decal_elements())
    # the seals again, faint: drawn across the whole arena they must not hide the floor
    for name, faint in FAINT.items():
        a = np.array(Image.open(os.path.join(tex, name + ".png")).convert("RGBA"))
        a[..., 3] = (a[..., 3] * FAINT_ALPHA).astype(np.uint8)
        save(Image.fromarray(a, "RGBA"), os.path.join(tex, faint + ".png"))
        model(rp, faint, faint, decal_elements())

    pieces = fit_frames(cut(os.path.join(ANIM, "mark_fill_sheet.png"), MARK_FRAMES, False), 64, 64, False)
    strip = Image.new("RGBA", (64, 64 * MARK_FRAMES))
    for i, piece in enumerate(pieces):
        strip.paste(veined(piece), (0, 64 * i))
    save(strip, os.path.join(tex, "mark_fill.png"))
    dump(os.path.join(tex, "mark_fill.png.mcmeta"), {"animation": {"frametime": 3}})
    model(rp, "mark_fill", "mark_fill", decal_elements())

    save(puddle(), os.path.join(tex, "puddle.png"))
    dump(os.path.join(tex, "puddle.png.mcmeta"), {"animation": {"frametime": 6}})
    model(rp, "puddle", "puddle", decal_elements())

    for name, size in OBJECTS.items():
        save(solid(fit(trimmed(os.path.join(RAW, name + ".png")), size, size, False)),
             os.path.join(tex, name + ".png"))
        dump(os.path.join(rp, "models", "pope_fx", name + ".json"),
             {"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/pope_fx/" + name}})
        item_def(rp, name)

    chain = fit(trimmed(os.path.join(RAW, "chain.png")), 32, 16, True)
    save(solid(chain, 6), os.path.join(tex, "chain.png"))
    model(rp, "chain", "chain", chain_elements())

    line = Image.new("RGBA", (4, 4), HOLY_RAMP[1] + (255,))
    save(line, os.path.join(tex, "line.png"))
    model(rp, "line", "line", line_elements())
    print("pope fx: %d glyphs, %d models" % (len(providers), len(DECALS) + len(OBJECTS) + 4))


if __name__ == "__main__":
    main()
