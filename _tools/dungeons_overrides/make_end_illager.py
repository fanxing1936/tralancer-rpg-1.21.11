"""T_IllagerEvoker -> the End Illager's brown robe (cutscene): robe and crossed arms brown, trim beige, no hood."""
import colorsys, sys
import numpy as np
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
a = np.array(Image.open(src).convert("RGBA")).astype(float)
out = a.copy()
for y in range(64):
    for x in range(64):
        r, g, b, al = a[y, x]
        if al == 0:
            continue
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        hd = h * 360
        if x >= 32 and y < 21 and l > 0.4 and s < 0.25:
            out[y, x, 3] = 0                                   # the hood layer
        elif (250 <= hd <= 330 or hd < 15) and s > 0.05 and l < 0.45:
            out[y, x, :3] = np.array(colorsys.hls_to_rgb(25 / 360, min(0.42, l * 1.35 + 0.08), 0.38)) * 255
        elif 140 <= hd <= 215 and y >= 16 and s < 0.3 and 0.18 < l < 0.5:     # grey-green sleeves and chest
            out[y, x, :3] = np.array(colorsys.hls_to_rgb(24 / 360, l * 0.95, 0.34)) * 255
        elif 35 <= hd <= 65 and s > 0.35:
            out[y, x, :3] = np.array(colorsys.hls_to_rgb(32 / 360, 0.62 + 0.15 * (l - 0.5), 0.25)) * 255
Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(dst)
