# -*- coding: utf-8 -*-
"""最终 Boss 路西法的位图血条（docs/LUCIFER-BOSS-DESIGN.md §5）。

    python add_lucifer_boss_art.py ../resourcepack

做法与教皇战相同（add_pope_fx_art.py）：原版血条只有 5 个 GUI 单位高，
所以把它藏起来（粉色档的贴图已由教皇战改成全透明），血条名字换成一整张位图横幅。
横幅形状由程序画，配色换成柱绿；中央饰物和花体标题由 Codex 按
lucifer_boss_ref/BAR-BRIEF.md 绘制。每段 20 档，血量跨档才换图。
"""

import os
import sys

import numpy as np
from PIL import Image

import rpg_ui_style as ui
from add_pope_fx_art import (BAR_ASCENT, BAR_H, BAR_W, TITLE_ASCENT, TITLE_HEIGHT, TITLE_MAX_WIDTH, TITLE_PIXELS,
                             _box, bar_body, dump, save, solid, trimmed)

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = os.path.join(HERE, "lucifer_boss_ref", "bar")
FONT = "rpg:lucifer_boss"
STEPS = 20
FIRST = 0xE200          # 每段 32 个码位：第 s 段第 k 档 = FIRST + (s-1)*32 + k
TITLE0 = 0xE1F0         # 标题、退格、进格各占一组


def rgb(hexcolour):
    h = ui.hex_of(hexcolour).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


P = ui.pillar(1)
GREEN = [(200, 245, 214), rgb(P["lit"]), rgb(ui.pillar_mid(1)), rgb(P["deep"])]
# 段号: (饰物文件, 标题文件)
STAGES = {1: ("emblem_serpent", "title_en_star"), 2: ("emblem_tree", "title_en_tree")}


def bar_code(stage, step):
    return FIRST + (stage - 1) * 32 + step


def title_codes(stage):
    """(标题, 退回中线, 推到横幅末端)"""
    i = stage - 1
    return TITLE0 + i, TITLE0 + 4 + i, TITLE0 + 8 + i


def bar_text(stage, step):
    t, back, on = title_codes(stage)
    return "".join(chr(c) for c in (bar_code(stage, step), back, t, on))


def banner(stage, step):
    a, shape = bar_body(GREEN)
    columns = np.flatnonzero(shape.any(axis=0))
    split = columns[0] + (columns[-1] + 1 - columns[0]) * step // STEPS
    lost = shape.copy()
    lost[:, :split] = False                 # 失去的部分从右往左变暗，轮廓保留
    a[lost, :3] = (a[lost, :3] * 0.16).astype(np.uint8) + 12
    out = Image.fromarray(a, "RGBA")
    drawn = trimmed(os.path.join(BAR, STAGES[stage][0] + ".png"))
    width = max(1, round(drawn.width * float(BAR_H) / drawn.height))
    out.alpha_composite(solid(_box(drawn, width, BAR_H), 12), ((BAR_W - width) // 2, 0))
    return out


def main():
    pack = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    rp = os.path.join(pack, "assets", "rpg")
    out = os.path.join(rp, "textures", "font", "lucifer_boss")
    providers, advances = [], {}
    for stage, (_, title) in STAGES.items():
        for step in range(STEPS + 1):
            stem = "bar_%d_%d" % (stage, step)
            save(banner(stage, step), os.path.join(out, stem + ".png"))
            providers.append({"type": "bitmap", "file": "rpg:font/lucifer_boss/%s.png" % stem,
                              "height": BAR_H, "ascent": BAR_ASCENT, "chars": [chr(bar_code(stage, step))]})
        drawn = trimmed(os.path.join(BAR, title + ".png"))
        pixels = min(TITLE_PIXELS, TITLE_MAX_WIDTH * drawn.height // drawn.width)
        width = round(drawn.width * float(pixels) / drawn.height)
        letters = np.array(_box(drawn, width, pixels))
        letters[..., 3] = np.where(letters[..., 3] > 110, 255, 0)
        save(Image.fromarray(letters, "RGBA"), os.path.join(out, "title_%d.png" % stage))
        t, back, on = title_codes(stage)
        providers.append({"type": "bitmap", "file": "rpg:font/lucifer_boss/title_%d.png" % stage,
                          "height": TITLE_HEIGHT, "ascent": TITLE_ASCENT, "chars": [chr(t)]})
        shown = width * TITLE_HEIGHT // pixels + 1
        advances[chr(back)] = -(BAR_W + 1 + shown) // 2
        advances[chr(on)] = (BAR_W + 1 - shown) // 2
    providers.append({"type": "space", "advances": advances})
    dump(os.path.join(rp, "font", "lucifer_boss.json"), {"providers": providers})
    print("lucifer boss bar: %d glyphs, %d stages x %d steps" % (len(providers), len(STAGES), STEPS + 1))


if __name__ == "__main__":
    main()
