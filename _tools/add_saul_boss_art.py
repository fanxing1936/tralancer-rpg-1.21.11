# -*- coding: utf-8 -*-
"""疯人王扫罗的位图血条（docs/SAUL-DESIGN.md §5）。

    python add_saul_boss_art.py ../resourcepack

做法与雅克相同（add_jacques_boss_art.py）：原版血条藏起来（粉色档贴图已由教皇战改成全透明），
血条名字换成一整张位图横幅，每段 20 档，每 50 血一档。一阶段银灰，二阶段暗红。

中央饰物与花体标题在 saul_boss_ref/bar/（占位，saul_boss_ref/make_placeholders.py 生成一次）：
  emblem_stalwart  一阶段：原作坚毅铠甲图标（T_ReinforcedMail_Unique1_Icon）
  emblem_madking   二阶段：原作细剑图标（T_Rapier_Icon）换成千刀配色
  title_en_marshal / title_en_madking   The Marshal / The Mad King
正式稿交给 Codex 同名覆盖即可，代码不用改。
"""

import os
import sys

import numpy as np
from PIL import Image

from add_pope_fx_art import (BAR_ASCENT, BAR_H, BAR_W, TITLE_ASCENT, TITLE_HEIGHT, TITLE_MAX_WIDTH, TITLE_PIXELS,
                             _box, bar_body, dump, save, solid, trimmed)

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = os.path.join(HERE, "saul_boss_ref", "bar")
FONT = "rpg:saul_boss"
STEPS = 20
FIRST = 0xE280          # 每段 32 个码位：第 s 段第 k 档 = FIRST + (s-1)*32 + k
TITLE0 = 0xE270


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


SILVER = [rgb("#EEF2F6"), rgb("#B4BEC8"), rgb("#66707C"), rgb("#22262C")]
BLOOD = [rgb("#E08A90"), rgb("#B0303C"), rgb("#6A1018"), rgb("#24060A")]
# 段号: (横幅配色, 饰物文件, 标题文件)
STAGES = {1: (SILVER, "emblem_stalwart", "title_en_marshal"), 2: (BLOOD, "emblem_madking", "title_en_madking")}


def bar_code(stage, step):
    return FIRST + (stage - 1) * 32 + step


def title_codes(stage):
    i = stage - 1
    return TITLE0 + i, TITLE0 + 4 + i, TITLE0 + 8 + i


def bar_text(stage, step):
    t, back, on = title_codes(stage)
    return "".join(chr(c) for c in (bar_code(stage, step), back, t, on))


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
    rp = os.path.join(pack, "assets", "rpg")
    out = os.path.join(rp, "textures", "font", "saul_boss")
    providers, advances = [], {}
    for stage, (_, _, title) in STAGES.items():
        for step in range(STEPS + 1):
            stem = "bar_%d_%d" % (stage, step)
            save(banner(stage, step), os.path.join(out, stem + ".png"))
            providers.append({"type": "bitmap", "file": "rpg:font/saul_boss/%s.png" % stem,
                              "height": BAR_H, "ascent": BAR_ASCENT, "chars": [chr(bar_code(stage, step))]})
        drawn = trimmed(os.path.join(BAR, title + ".png"))
        pixels = min(TITLE_PIXELS, TITLE_MAX_WIDTH * drawn.height // drawn.width)
        width = round(drawn.width * float(pixels) / drawn.height)
        letters = np.array(_box(drawn, width, pixels))
        letters[..., 3] = np.where(letters[..., 3] > 110, 255, 0)
        save(Image.fromarray(letters, "RGBA"), os.path.join(out, "title_%d.png" % stage))
        t, back, on = title_codes(stage)
        providers.append({"type": "bitmap", "file": "rpg:font/saul_boss/title_%d.png" % stage,
                          "height": TITLE_HEIGHT, "ascent": TITLE_ASCENT, "chars": [chr(t)]})
        shown = width * TITLE_HEIGHT // pixels + 1
        advances[chr(back)] = -(BAR_W + 1 + shown) // 2
        advances[chr(on)] = (BAR_W + 1 - shown) // 2
    providers.append({"type": "space", "advances": advances})
    dump(os.path.join(rp, "font", "saul_boss.json"), {"providers": providers})
    print("saul boss bar: %d glyphs, %d stages x %d steps" % (len(providers), len(STAGES), STEPS + 1))


if __name__ == "__main__":
    main()
