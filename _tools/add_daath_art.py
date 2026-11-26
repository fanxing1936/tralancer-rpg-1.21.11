# -*- coding: utf-8 -*-
"""达阿特试炼的位图血条、物品图标与 Codex 的图（docs/DAATH-DESIGN.md §5）。

    python add_daath_art.py ../resourcepack

血条做法与扫罗相同：每段 20 档，一段黑银、二段灰银白。饰物与花体标题在 daath_ref/bar/（占位，同名覆盖即可）。
Codex 交付的 daath_ref/{anim,decal,icons}/ 有了就用，没有就用现成的替身：
  icons/mark_*.png   「记住你」的记号，进字体 rpg:daath_vfx
  icons/daath_shard.png  [遗物] 达阿特的碎镜
"""
import io
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

from add_pope_fx_art import (BAR_ASCENT, BAR_H, BAR_W, TITLE_ASCENT, TITLE_HEIGHT, TITLE_MAX_WIDTH, TITLE_PIXELS, _box, bar_body, dump, save, solid,
                             trimmed)

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "daath_ref")
BAR = os.path.join(REF, "bar")
FONT = "rpg:daath"
VFX_FONT = "rpg:daath_marks"
STEPS = 20
FIRST = 0xE2C0
TITLE0 = 0xE2B0
MARKS = ("blade", "step", "bottle", "shield", "loop", "skill", "hand")
MARK0 = 0xE300


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


INK = [rgb("#AAB4C3"), rgb("#4A505C"), rgb("#1A1D24"), rgb("#0B0C10")]
PALE = [rgb("#FFFFFF"), rgb("#D8DEE8"), rgb("#7C8593"), rgb("#2A2E38")]
STAGES = {1: (INK, "emblem_umbra", "title_en_umbra"), 2: (PALE, "emblem_face", "title_en_face")}


def bar_code(stage, step):
    return FIRST + (stage - 1) * 32 + step


def title_codes(stage):
    i = stage - 1
    return TITLE0 + i, TITLE0 + 4 + i, TITLE0 + 8 + i


def bar_text(stage, step):
    t, back, on = title_codes(stage)
    return "".join(chr(c) for c in (bar_code(stage, step), back, t, on))


def icon(name):
    p = os.path.join(REF, "icons", name + ".png")
    return p if os.path.isfile(p) else None


def small(im, size):
    """Codex 的大图 → 目标像素：方框滤波、硬边、吸附到灰银色阶。"""
    import add_daath_fx_art as dart
    import add_michael_fx_art as M
    return im if im.size == (size, size) else dart.palette(M.fit(M.square(im, 4), size, cut=100))


def colour(im, size):
    """带颜色的大图（原质法阵、称号）→ 目标像素：方框滤波、硬边，减到十二色。"""
    import add_michael_fx_art as M
    im = M.fit(M.square(im.convert("RGBA"), 4), size, cut=100)
    a = im.getchannel("A")
    q = im.convert("RGB").quantize(12, dither=Image.Dither.NONE).convert("RGB")
    q.putalpha(a)
    return q


def mark(name):
    """「记住你」的记号字符；Codex 的图还没来就是 None（用文字符号代替）。"""
    return chr(MARK0 + MARKS.index(name)) if icon("mark_" + name) else None


def tree(name):
    """Codex 的原质法阵（daath_ref/tree/seal_<键>.png）；还没来就是 None（用现成法阵叠）。"""
    return "rpg:daath/seal_%s" % name if os.path.isfile(os.path.join(REF, "tree", "seal_%s.png" % name)) else None


def planes(rp):
    """原质法阵：朝上的平面模型，可着色（路径直接用扫罗突进的 beam 贴图）。"""
    A = os.path.join(rp)
    tex = os.path.join(A, "textures", "item", "daath")
    os.makedirs(tex, exist_ok=True)
    names = []
    d = os.path.join(REF, "tree")
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.startswith("seal_") and f.endswith(".png"):
                im = Image.open(os.path.join(d, f)).convert("RGBA")
                colour(im, 32).save(os.path.join(tex, f))
                names.append(f[:-4])
    for n in names:
        t = "rpg:item/daath/" + n
        dump(os.path.join(A, "models", "daath", n + ".json"), {"textures": {"0": t, "particle": t}, "elements": [{"from": [0, 8, 0], "to": [16, 8, 16], "faces": {
            "up": {"uv": [0, 0, 16, 16], "texture": "#0", "tintindex": 0}}}]})
        dump(os.path.join(A, "items", "daath", n + ".json"), {"model": {"type": "minecraft:model", "model": "rpg:daath/" + n, "tints": [
            {"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]}})
    return len(names)


def placeholders():
    """一次性占位：镜里的眼与哥特花体（系统字体只用这一次）。"""
    from PIL import ImageFont
    os.makedirs(BAR, exist_ok=True)
    for name, open_ in (("emblem_umbra", False), ("emblem_face", True)):
        p = os.path.join(BAR, name + ".png")
        if os.path.isfile(p):
            continue
        s = 32
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        ring = "#AAB4C3" if open_ else "#7C8593"
        d.ellipse((2, 2, 29, 29), fill="#0B0C10", outline=ring, width=2)
        d.ellipse((5, 5, 26, 26), outline="#2A2E38", width=1)
        if open_:
            d.polygon([(7, 16), (12, 11), (19, 11), (24, 16), (19, 21), (12, 21)], fill="#FFFFFF", outline="#AAB4C3")
            d.rectangle((14, 13, 17, 19), fill="#0B0C10")
            d.rectangle((15, 15, 16, 16), fill="#FFF2A8")
        else:
            d.line([(7, 15), (12, 18), (19, 18), (24, 15)], fill="#D8DEE8", width=2)
            for x in (10, 14, 18, 21):
                d.line([(x, 19), (x - 1, 22)], fill="#AAB4C3")
        d.polygon([(22, 2), (31, 0), (30, 10)], fill=(0, 0, 0, 0))
        d.line([(21, 4), (25, 8), (29, 10)], fill=ring)
        im.resize((256, 256), Image.NEAREST).save(p)
    font = ImageFont.truetype("C:/Windows/Fonts/OLDENGL.TTF", 150)
    for name, text, fill, edge in (("title_en_umbra", "Umbra", "#AAB4C3", "#0B0C10"), ("title_en_face", "Facie ad Faciem", "#FFFFFF", "#2A2E38")):
        p = os.path.join(BAR, name + ".png")
        if os.path.isfile(p):
            continue
        box = font.getbbox(text, stroke_width=10)
        im = Image.new("RGBA", (box[2] - box[0] + 24, box[3] - box[1] + 24), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((12 - box[0], 12 - box[1]), text, font=font, fill=fill, stroke_width=10, stroke_fill=edge)
        im.save(p)
    # 称号图标与碎镜的占位
    art = os.path.join(HERE, "world_ref", "art")
    for key, col in (("sever", "#FF5A62"), ("mirror", "#62B8F0")):
        p = os.path.join(art, "title_%s.png" % key)
        if icon("title_" + key):            # Codex 的正式图
            colour(Image.open(icon("title_" + key)), 16).save(p)
            continue
        if not os.path.isfile(p):
            im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.polygon([(8, 1), (14, 7), (9, 14), (3, 9)], fill="#AAB4C3", outline="#0B0C10")
            d.line([(8, 2), (9, 13)], fill=col, width=2) if key == "sever" else d.ellipse((6, 5, 10, 9), fill="#FFFFFF", outline=col)
            im.save(p)


def banner(stage, step):
    ramp, emblem, _ = STAGES[stage]
    a, shape = bar_body(ramp)
    columns = np.flatnonzero(shape.any(axis=0))
    split = columns[0] + (columns[-1] + 1 - columns[0]) * step // STEPS
    lost = shape.copy()
    lost[:, :split] = False
    a[lost, :3] = (a[lost, :3] * 0.16).astype(np.uint8) + 12
    out = Image.fromarray(a, "RGBA")
    drawn = trimmed(os.path.join(BAR, emblem + ".png"))
    width = max(1, round(drawn.width * float(BAR_H) / drawn.height))
    out.alpha_composite(solid(_box(drawn, width, BAR_H), 12), ((BAR_W - width) // 2, 0))
    return out


def main():
    pack = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    placeholders()
    rp = os.path.join(pack, "assets", "rpg")
    out = os.path.join(rp, "textures", "font", "daath")
    providers, advances = [], {}
    for stage, (_, _, title) in STAGES.items():
        for step in range(STEPS + 1):
            stem = "bar_%d_%d" % (stage, step)
            save(banner(stage, step), os.path.join(out, stem + ".png"))
            providers.append({"type": "bitmap", "file": "rpg:font/daath/%s.png" % stem, "height": BAR_H, "ascent": BAR_ASCENT, "chars": [chr(bar_code(stage, step))]})
        drawn = trimmed(os.path.join(BAR, title + ".png"))
        pixels = min(TITLE_PIXELS, TITLE_MAX_WIDTH * drawn.height // drawn.width)
        width = round(drawn.width * float(pixels) / drawn.height)
        letters = np.array(_box(drawn, width, pixels))
        letters[..., 3] = np.where(letters[..., 3] > 110, 255, 0)
        save(Image.fromarray(letters, "RGBA"), os.path.join(out, "title_%d.png" % stage))
        t, back, on = title_codes(stage)
        providers.append({"type": "bitmap", "file": "rpg:font/daath/title_%d.png" % stage, "height": TITLE_HEIGHT, "ascent": TITLE_ASCENT, "chars": [chr(t)]})
        shown = width * TITLE_HEIGHT // pixels + 1
        advances[chr(back)] = -(BAR_W + 1 + shown) // 2
        advances[chr(on)] = (BAR_W + 1 - shown) // 2
    providers.append({"type": "space", "advances": advances})
    dump(os.path.join(rp, "font", "daath.json"), {"providers": providers})
    planes(rp)
    vp = []
    for m in MARKS:
        p = icon("mark_" + m)
        if p:
            im = Image.open(p).convert("RGBA")
            save(small(im, 16), os.path.join(out, "mark_%s.png" % m))
            vp.append({"type": "bitmap", "file": "rpg:font/daath/mark_%s.png" % m, "height": 10, "ascent": 8, "chars": [mark(m)]})
    if vp:
        dump(os.path.join(rp, "font", "daath_marks.json"), {"providers": vp})
    # [遗物] 达阿特的碎镜
    p = icon("daath_shard")
    tex = os.path.join(rp, "textures", "item", "daath", "shard.png")
    os.makedirs(os.path.dirname(tex), exist_ok=True)
    if p:
        im = Image.open(p).convert("RGBA")
        small(im, 32).save(tex)
    else:
        im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.polygon([(16, 2), (27, 12), (20, 29), (6, 20), (9, 7)], fill="#7C8593", outline="#0B0C10")
        d.polygon([(16, 4), (25, 12), (16, 16)], fill="#D8DEE8")
        d.polygon([(8, 19), (16, 16), (19, 27)], fill="#4A505C")
        d.ellipse((13, 12, 19, 17), fill="#FFFFFF", outline="#0B0C10")
        d.rectangle((15, 13, 16, 15), fill="#0B0C10")
        im.save(tex)
    for rel, doc in (("models/item/daath_shard.json", {"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/daath/shard"}}),
                     ("items/daath_shard.json", {"model": {"type": "minecraft:model", "model": "rpg:item/daath_shard"}})):
        q = os.path.join(rp, *rel.split("/"))
        os.makedirs(os.path.dirname(q), exist_ok=True)
        json.dump(doc, io.open(q, "w", encoding="utf-8", newline="\n"))
    print("daath art: %d glyphs, marks %d" % (len(providers), len(vp)))


if __name__ == "__main__":
    main()
