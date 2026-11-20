# -*- coding: utf-8 -*-
"""One-off: the placeholder emblems and titles for Saul's boss bar (bar/), like jacques_boss_ref.

    python saul_boss_ref/make_placeholders.py

  emblem_stalwart   stage 1: the original Stalwart Armor icon (T_ReinforcedMail_Unique1_Icon)
  emblem_madking    stage 2: the original Rapier icon (T_Rapier_Icon) in the Thousand Cuts colours, darkened
  title_en_marshal / title_en_madking   The Marshal / The Mad King, Old English (system font, rendered once)
The build never reads the system font; replace these files with the final art under the same names.
"""
import colorsys
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = os.path.join(HERE, "bar")
SRC = "D:/agent/dungeons_extract/upgrade/saul/assets/Dungeons/Content/"
os.makedirs(BAR, exist_ok=True)


def icon(rel):
    return Image.open(SRC + rel).convert("RGBA").resize((256, 256), Image.LANCZOS)


icon("Actors/Equipment/Armor/ReinforcedMail_Unique1/T_ReinforcedMail_Unique1_Icon.png").save(os.path.join(BAR, "emblem_stalwart.png"))

blade = np.array(icon("Patch2/Actors/Equipment/MeleeWeapons/Rapier/T_Rapier_Icon.png")).astype(float)
for y in range(256):
    for x in range(256):
        r, g, b, a = blade[y, x]
        if a == 0:
            continue
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        if s > 0.35 and (h < 20 / 360 or h > 330 / 360):        # red guard -> gold
            blade[y, x, :3] = np.array(colorsys.hls_to_rgb(42 / 360, min(0.72, l * 1.25), 0.75)) * 255
        elif s > 0.2 and 15 / 360 <= h <= 40 / 360:              # brown grip -> blue
            blade[y, x, :3] = np.array(colorsys.hls_to_rgb(220 / 360, l, 0.6)) * 255
        blade[y, x, :3] *= 0.86                                  # a little darker: the mad king
Image.fromarray(blade.clip(0, 255).astype(np.uint8)).save(os.path.join(BAR, "emblem_madking.png"))

font = ImageFont.truetype("C:/Windows/Fonts/OLDENGL.TTF", 150)
for name, text, fill, edge in (("title_en_marshal", "The Marshal", "#D8DEE6", "#1A1E24"),
                               ("title_en_madking", "The Mad King", "#C9505A", "#2A060A")):
    box = font.getbbox(text, stroke_width=10)
    im = Image.new("RGBA", (box[2] - box[0] + 24, box[3] - box[1] + 24), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((12 - box[0], 12 - box[1]), text, font=font, fill=fill, stroke_width=10, stroke_fill=edge)
    im.save(os.path.join(BAR, name + ".png"))
print("saul bar placeholders written to", BAR)
