# -*- coding: utf-8 -*-
"""天使长米迦勒的位图血条与「注视」的眼睛（docs/MICHAEL-DESIGN.md §5、§6）。

    python add_michael_boss_art.py ../resourcepack

血条做法同扫罗（add_saul_boss_art.py）：原版血条藏起来，名字换成一整张位图横幅，每段 20 档，每 60 血一档。
一阶段暖白（灵体的皮肤色），二阶段圣焰橙红。饰物与标题在 michael_boss_ref/bar/（占位，make_placeholders.py 生成一次）：
  emblem_spine / emblem_rib            米迦勒脊骨 / 米迦勒肋骨的贴图
  title_en_quis / title_en_seraph      Quis ut Deus / The Seraph
正式稿交给 Codex 同名覆盖即可。

「注视」的眼睛：字体 rpg:michael_fx，三帧 32×32（闭眼、半睁、全睁），圣焰橙红配暖白，和守望者的眼睛同色；
另有一张满屏闪光（32×16 半透明白，放进 title 里放大到盖满屏幕，颜色由文字颜色给）。

战斗里用到的物品模型（rpg:michael_boss/*）：
  spine / rib     玩家版米迦勒脊骨、肋骨的手持模型（实心贴图），给插在中心的骨柱、飞出去的肋骨、最后留在地上的骨头
  feather         羽刃、天火羽雨的一片燃烧的羽毛（16×16，暖白到圣焰橙红）
"""

import os
import sys

import numpy as np
from PIL import Image

from add_pope_fx_art import (BAR_ASCENT, BAR_H, BAR_W, TITLE_ASCENT, TITLE_HEIGHT, TITLE_MAX_WIDTH, TITLE_PIXELS,
                             _box, bar_body, dump, save, solid, trimmed)

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = os.path.join(HERE, "michael_boss_ref", "bar")
FONT = "rpg:michael_boss"
FX_FONT = "rpg:michael_fx"
STEPS = 20
FIRST = 0xE300          # 每段 32 个码位：第 s 段第 k 档 = FIRST + (s-1)*32 + k
TITLE0 = 0xE2F0
EYE0 = 0xE000           # 闭眼、半睁、全睁
FLASH = 0xE010
EYE_HEIGHT = 16


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


WARM = [rgb("#FFF5EE"), rgb("#FFD0BD"), rgb("#C8765A"), rgb("#3A1A10")]
FIRE = [rgb("#FFB08A"), rgb("#FF3300"), rgb("#8A1A00"), rgb("#240600")]
STAGES = {1: (WARM, "emblem_spine", "title_en_quis"), 2: (FIRE, "emblem_rib", "title_en_seraph")}


def bar_code(stage, step):
    return FIRST + (stage - 1) * 32 + step


def title_codes(stage):
    i = stage - 1
    return TITLE0 + i, TITLE0 + 4 + i, TITLE0 + 8 + i


def bar_text(stage, step):
    t, back, on = title_codes(stage)
    return "".join(chr(c) for c in (bar_code(stage, step), back, t, on))


def eye_text(frame):
    return chr(EYE0 + frame)


def flash_text():
    return chr(FLASH)


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


def eye(frame):
    """32x32 eye: 0 closed, 1 half open, 2 wide open.  Holy fire rim, warm white, a burning pupil."""
    rim, white, iris, pupil, glow = rgb("#FF3300"), rgb("#FFF5EE"), rgb("#FF805F"), rgb("#8A1A00"), rgb("#FFD0BD")
    a = np.zeros((32, 32, 4), np.uint8)
    cx, cy = 15.5, 15.5
    half = (0.6, 4.5, 8.5)[frame]           # half height of the almond at its middle
    for y in range(32):
        for x in range(32):
            u = (x - cx) / 14.0
            if abs(u) > 1:
                continue
            h = half * (1 - u * u)              # almond: a parabola above and below
            d = abs(y - cy)
            if frame == 0:
                if d <= 1.0 and abs(u) <= 0.97:
                    a[y, x] = rim + (255,)
                continue
            if d <= h + 1.0:
                a[y, x] = rim + (255,)
            if d <= h - 0.6:
                a[y, x] = white + (235,)
                r = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if r <= min(5.5, h + 0.5):
                    a[y, x] = iris + (255,)
                if r <= min(2.6, h):
                    a[y, x] = pupil + (255,)
                if abs(x - (cx - 1.5)) < 1 and abs(y - (cy - 1.5)) < 1 and frame == 2:
                    a[y, x] = glow + (255,)
    if frame == 0:                           # lashes on the closed eye
        for x in (8, 12, 16, 20, 24):
            a[17, x] = rim + (255,)
            a[18, x] = rim + (180,)
    return Image.fromarray(a, "RGBA")


def feather():
    """16x16 burning feather, quill bottom-left to tip top-right: warm white vane, holy-fire edge and tip."""
    a = np.zeros((16, 16, 4), np.uint8)
    white, mid, fire, quill = rgb("#FFF5EE"), rgb("#FFD0BD"), rgb("#FF3300"), rgb("#FF805F")
    for i in range(1, 15):                       # the shaft along the diagonal
        x, y = i, 15 - i
        a[y, x] = quill + (255,)
        if i < 3:
            continue
        w = 2 if i < 12 else 1                   # vane width either side
        for d in range(1, w + 1):
            for (xx, yy) in ((x - d, y - d), (x + d, y + d)):
                if 0 <= xx < 16 and 0 <= yy < 16:
                    a[yy, xx] = (white if d == 1 else mid) + (255,)
        if i >= 11:
            for (xx, yy) in ((x - w, y - w), (x + w, y + w), (x, y)):
                if 0 <= xx < 16 and 0 <= yy < 16:
                    a[yy, xx] = fire + (255,)
    a[1, 14] = fire + (255,)
    return Image.fromarray(a, "RGBA")


def main():
    pack = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    rp = os.path.join(pack, "assets", "rpg")
    out = os.path.join(rp, "textures", "font", "michael_boss")
    providers, advances = [], {}
    for stage, (_, _, title) in STAGES.items():
        for step in range(STEPS + 1):
            stem = "bar_%d_%d" % (stage, step)
            save(banner(stage, step), os.path.join(out, stem + ".png"))
            providers.append({"type": "bitmap", "file": "rpg:font/michael_boss/%s.png" % stem,
                              "height": BAR_H, "ascent": BAR_ASCENT, "chars": [chr(bar_code(stage, step))]})
        drawn = trimmed(os.path.join(BAR, title + ".png"))
        pixels = min(TITLE_PIXELS, TITLE_MAX_WIDTH * drawn.height // drawn.width)
        width = round(drawn.width * float(pixels) / drawn.height)
        letters = np.array(_box(drawn, width, pixels))
        letters[..., 3] = np.where(letters[..., 3] > 110, 255, 0)
        save(Image.fromarray(letters, "RGBA"), os.path.join(out, "title_%d.png" % stage))
        t, back, on = title_codes(stage)
        providers.append({"type": "bitmap", "file": "rpg:font/michael_boss/title_%d.png" % stage,
                          "height": TITLE_HEIGHT, "ascent": TITLE_ASCENT, "chars": [chr(t)]})
        shown = width * TITLE_HEIGHT // pixels + 1
        advances[chr(back)] = -(BAR_W + 1 + shown) // 2
        advances[chr(on)] = (BAR_W + 1 - shown) // 2
    providers.append({"type": "space", "advances": advances})
    dump(os.path.join(rp, "font", "michael_boss.json"), {"providers": providers})

    # 「注视」的眼睛和全屏闪光自 2026-11-18 起在 add_michael_fx_art.py（字体 rpg:michael_vfx，Codex 画的六帧睁眼、
    # 四帧渐褪的闪光）；这里的三帧旧眼睛与 32×16 闪光不再生成。
    for name, model in (("spine", "rpg:item/michael_spine_in_hand"), ("rib", "rpg:item/michael_rib_in_hand"),
                        ("feather", "rpg:michael_boss/feather")):
        dump(os.path.join(rp, "items", "michael_boss", name + ".json"), {"model": {"type": "minecraft:model", "model": model}})
    save(feather(), os.path.join(rp, "textures", "item", "michael_boss", "feather.png"))
    dump(os.path.join(rp, "models", "michael_boss", "feather.json"),
         {"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/michael_boss/feather"}})
    print("michael boss bar: %d glyphs, %d stages x %d steps" % (len(providers), len(STAGES), STEPS + 1))


if __name__ == "__main__":
    main()
