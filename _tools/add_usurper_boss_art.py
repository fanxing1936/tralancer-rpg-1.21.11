# -*- coding: utf-8 -*-
"""篡夺者的位图血条（docs/USURPER-DESIGN.md §5）。

    python add_usurper_boss_art.py ../resourcepack

做法与教皇战、最终 Boss 路西法相同（add_pope_fx_art.py、add_lucifer_boss_art.py）：
原版血条藏起来（粉色档的贴图已由教皇战改成全透明），血条名字换成一整张位图横幅，
每段 20 档，每 50 血一档，跨档才换图。横幅形状由程序画；一阶段附魔紫，二阶段篡夺白金。

中央饰物与花体标题在 usurper_boss_ref/bar/：
  emblem_enchanter   一阶段：原作附魔师之书（T_EnchantersTome 物品图标）
  emblem_paraclete   二阶段：原作秩序避雷针（T_LightningRodOfOrder 物品图标），蓝宝石改成白金：权柄的权杖
  title_en_usurper / title_en_paraclete   The Usurper / The False Paraclete
四张都是占位：饰物取原作图标，标题用系统的哥特字体渲染一次后存成图片（构建不读系统字体）。
正式稿交给 Codex 按 usurper_boss_ref/BAR-BRIEF.md 画，同名覆盖即可，代码不用改。
"""

import os
import sys

import numpy as np
from PIL import Image

import rpg_ui_style as ui
from add_pope_fx_art import (BAR_ASCENT, BAR_H, BAR_W, TITLE_ASCENT, TITLE_HEIGHT, TITLE_MAX_WIDTH, TITLE_PIXELS,
                             _box, bar_body, dump, save, solid, trimmed)

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = os.path.join(HERE, "usurper_boss_ref", "bar")
FONT = "rpg:usurper_boss"
STEPS = 20
FIRST = 0xE200          # 每段 32 个码位：第 s 段第 k 档 = FIRST + (s-1)*32 + k
TITLE0 = 0xE1F0         # 标题、退格、进格各占一组


def rgb(hexcolour):
    h = ui.hex_of(hexcolour).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PURPLE = [rgb("#E8D5FF"), rgb("#B784D6"), rgb("#8A55AE"), rgb("#5B2C6F")]
WHITE_GOLD = [rgb(ui.WHITE_GOLD[0]), rgb(ui.WHITE_GOLD[1]), rgb("#D4AF52"), rgb(ui.WHITE_GOLD[2])]
# 段号: (横幅配色, 饰物文件, 标题文件)
STAGES = {1: (PURPLE, "emblem_enchanter", "title_en_usurper"), 2: (WHITE_GOLD, "emblem_paraclete", "title_en_paraclete")}


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
    ramp, emblem, _ = STAGES[stage]
    a, shape = bar_body(ramp)
    columns = np.flatnonzero(shape.any(axis=0))
    split = columns[0] + (columns[-1] + 1 - columns[0]) * step // STEPS
    lost = shape.copy()
    lost[:, :split] = False                 # 失去的部分从右往左变暗，轮廓保留
    a[lost, :3] = (a[lost, :3] * 0.16).astype(np.uint8) + 12
    out = Image.fromarray(a, "RGBA")
    drawn = trimmed(os.path.join(BAR, emblem + ".png"))
    width = max(1, round(drawn.width * float(BAR_H) / drawn.height))
    out.alpha_composite(solid(_box(drawn, width, BAR_H), 12), ((BAR_W - width) // 2, 0))
    return out


def main():
    pack = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    rp = os.path.join(pack, "assets", "rpg")
    out = os.path.join(rp, "textures", "font", "usurper_boss")
    providers, advances = [], {}
    for stage, (_, _, title) in STAGES.items():
        for step in range(STEPS + 1):
            stem = "bar_%d_%d" % (stage, step)
            save(banner(stage, step), os.path.join(out, stem + ".png"))
            providers.append({"type": "bitmap", "file": "rpg:font/usurper_boss/%s.png" % stem,
                              "height": BAR_H, "ascent": BAR_ASCENT, "chars": [chr(bar_code(stage, step))]})
        drawn = trimmed(os.path.join(BAR, title + ".png"))
        pixels = min(TITLE_PIXELS, TITLE_MAX_WIDTH * drawn.height // drawn.width)
        width = round(drawn.width * float(pixels) / drawn.height)
        letters = np.array(_box(drawn, width, pixels))
        letters[..., 3] = np.where(letters[..., 3] > 110, 255, 0)
        save(Image.fromarray(letters, "RGBA"), os.path.join(out, "title_%d.png" % stage))
        t, back, on = title_codes(stage)
        providers.append({"type": "bitmap", "file": "rpg:font/usurper_boss/title_%d.png" % stage,
                          "height": TITLE_HEIGHT, "ascent": TITLE_ASCENT, "chars": [chr(t)]})
        shown = width * TITLE_HEIGHT // pixels + 1
        advances[chr(back)] = -(BAR_W + 1 + shown) // 2
        advances[chr(on)] = (BAR_W + 1 - shown) // 2
    providers.append({"type": "space", "advances": advances})
    dump(os.path.join(rp, "font", "usurper_boss.json"), {"providers": providers})
    print("usurper boss bar: %d glyphs, %d stages x %d steps" % (len(providers), len(STAGES), STEPS + 1))


if __name__ == "__main__":
    main()
