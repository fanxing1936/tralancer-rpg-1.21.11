# -*- coding: utf-8 -*-
"""One-off: placeholder emblems and titles for Michael's boss bar (bar/), like saul_boss_ref.

    python michael_boss_ref/make_placeholders.py

  emblem_spine   stage 1: the 米迦勒脊骨 sprite (michael_art/michael_spine.png), warm white
  emblem_rib     stage 2: the 米迦勒肋骨 sprite (michael_art/michael_rib.png), holy fire
  title_en_quis / title_en_seraph   Quis ut Deus / The Seraph, Old English (system font, rendered once)
The build never reads the system font; replace these files with the final art under the same names.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = os.path.join(HERE, "bar")
ART = os.path.join(HERE, "..", "michael_art")
os.makedirs(BAR, exist_ok=True)


def tinted(name, lo, hi):
    a = np.array(Image.open(os.path.join(ART, name)).convert("RGBA")).astype(float)
    lum = (a[..., :3] @ [0.2126, 0.7152, 0.0722]) / 255.0
    for c in range(3):
        a[..., c] = lo[c] + (hi[c] - lo[c]) * lum
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).resize((256, 256), Image.NEAREST)


tinted("michael_spine.png", (150, 70, 40), (255, 245, 238)).save(os.path.join(BAR, "emblem_spine.png"))
tinted("michael_rib.png", (120, 20, 0), (255, 128, 95)).save(os.path.join(BAR, "emblem_rib.png"))

font = ImageFont.truetype("C:/Windows/Fonts/OLDENGL.TTF", 150)
for name, text, fill, edge in (("title_en_quis", "Quis ut Deus", "#FFF5EE", "#5A2410"),
                               ("title_en_seraph", "The Seraph", "#FF5A2A", "#2A0800")):
    box = font.getbbox(text, stroke_width=10)
    im = Image.new("RGBA", (box[2] - box[0] + 24, box[3] - box[1] + 24), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((12 - box[0], 12 - box[1]), text, font=font, fill=fill, stroke_width=10, stroke_fill=edge)
    im.save(os.path.join(BAR, name + ".png"))
print("michael bar placeholders written to", BAR)
