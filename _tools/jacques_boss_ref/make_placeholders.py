# -*- coding: utf-8 -*-
"""One-off: the placeholder emblems and titles for Jacques's boss bar (bar/), like usurper_boss_ref.

    python jacques_boss_ref/make_placeholders.py <icons_jq export root>

  emblem_heros     stage 1: the original Hero's Armor icon (T_ChampionsArmor_Unique1_Icon)
  emblem_burning   stage 2: the original Grave Bane icon (T_Glaive_Unique1_Icon), its gold blade turned to flame
  title_en_grandmaster / title_en_burning   The Grand Master / The Burning Oath, Old English (system font, rendered once)
The build never reads the system font; replace these files with the final art under the same names.
"""
import colorsys
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = os.path.join(HERE, "bar")
src = sys.argv[1] if len(sys.argv) > 1 else "D:/agent/dungeons_extract/upgrade/icons_jq/assets/Dungeons/Content/Actors/Equipment"
os.makedirs(BAR, exist_ok=True)


def icon(rel):
    return Image.open(os.path.join(src, rel)).convert("RGBA").resize((256, 256), Image.LANCZOS)


heros = icon("Armor/ChampionsArmor_Unique1/T_ChampionsArmor_Unique1_Icon.png")
heros.save(os.path.join(BAR, "emblem_heros.png"))

glaive = np.array(icon("MeleeWeapons/Glaive_Unique1/T_Glaive_Unique1_Icon.png")).astype(float)
for y in range(256):
    for x in range(256):
        r, g, b, a = glaive[y, x]
        if a == 0:
            continue
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        if 25 / 360 <= h <= 70 / 360 and s > 0.3:          # gold -> flame (orange at the core, red in the shade)
            glaive[y, x, :3] = np.array(colorsys.hls_to_rgb((8 + 26 * l) / 360, min(0.75, l * 1.05), 0.95)) * 255
Image.fromarray(glaive.clip(0, 255).astype(np.uint8)).save(os.path.join(BAR, "emblem_burning.png"))

font = ImageFont.truetype("C:/Windows/Fonts/OLDENGL.TTF", 150)
for name, text, fill, edge in (("title_en_grandmaster", "The Grand Master", "#C9D8E6", "#101C28"),
                               ("title_en_burning", "The Burning Oath", "#FF9A45", "#3A0C04")):
    box = font.getbbox(text, stroke_width=10)
    im = Image.new("RGBA", (box[2] - box[0] + 24, box[3] - box[1] + 24), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((12 - box[0], 12 - box[1]), text, font=font, fill=fill, stroke_width=10, stroke_fill=edge)
    im.save(os.path.join(BAR, name + ".png"))
print("jacques bar placeholders written to", BAR)
