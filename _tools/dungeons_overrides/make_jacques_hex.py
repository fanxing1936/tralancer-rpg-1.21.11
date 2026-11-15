"""T_Hex -> Jacques's undersuit: the brown leather of the body, arms and legs turned to the navy of Hex's own hood,
so it sits under Hero's Armor (slate teal, warm grey, gold) without a warm-brown band. Face, hair and hood untouched.

    python make_jacques_hex.py <T_Hex.png> jacques_hex.png
"""
import colorsys
import sys

import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
a = np.array(Image.open(src).convert("RGBA")).astype(float)
out = a.copy()
for y in range(16, 64):
    for x in range(64):
        r, g, b, al = a[y, x]
        if al == 0 or (x >= 56 and 20 <= y < 28):          # the second face tile
            continue
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        if (h * 360 < 35 or h * 360 > 340) and s > 0.25 and l < 0.42:   # brown leather, not skin
            out[y, x, :3] = np.array(colorsys.hls_to_rgb(208 / 360, min(0.36, l * 0.9 + 0.04), 0.26)) * 255
Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(dst)
