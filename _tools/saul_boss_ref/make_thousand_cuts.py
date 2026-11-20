# -*- coding: utf-8 -*-
"""One-off: 千刀（The Thousand Cuts，Dungeons II 的细剑独特变体）的贴图。

    python saul_boss_ref/make_thousand_cuts.py

二代的千刀本体里没有；一代有同一类武器细剑（SM_Rapier + 18×18 的 T_Rapier）。网格照用一代细剑，
贴图逐色换成千刀的配色（wiki 图标 MCD2_Render_The_Thousand_Cuts_Icon：银白剑身、金色护手、蓝色握柄），
不重画像素。输出 saul_boss_ref/thousand_cuts.png，dungeons_models.py 的 saul 用它覆盖细剑材质。
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = ("D:/agent/dungeons_extract/upgrade/saul/assets/Dungeons/Content/Patch2/Actors/Equipment/MeleeWeapons/"
       "Rapier/T_Rapier.png")
SWAP = {
    # 剑身：原作的灰调成更冷的银白
    (163, 180, 182): (198, 216, 228), (115, 126, 130): (134, 150, 168), (220, 220, 220): (234, 242, 250),
    # 护手：红 → 金
    (232, 0, 23): (255, 220, 110), (147, 0, 13): (218, 166, 52), (85, 0, 7): (142, 98, 30),
    # 握柄：褐 → 蓝
    (144, 68, 38): (92, 132, 218), (122, 57, 26): (62, 100, 188), (98, 40, 19): (42, 72, 152), (75, 25, 19): (28, 48, 108),
}


def main():
    im = Image.open(SRC).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if (r, g, b) in SWAP:
                px[x, y] = SWAP[(r, g, b)] + (a,)
    im.save(os.path.join(HERE, "thousand_cuts.png"))
    print("thousand_cuts.png written", im.size)


if __name__ == "__main__":
    main()
