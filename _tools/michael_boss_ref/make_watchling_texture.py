# -*- coding: utf-8 -*-
"""Watchling (Dungeons WatcherOfTheEnd, mesh SK_Enderling) for Michael's fight (docs/MICHAEL-DESIGN.md).

    python michael_boss_ref/make_watchling_texture.py

User 2026-11-17: the body keeps the original black but is half transparent, a spirit like Michael (his
own textures are 18%..48% opaque); the eyes glow.  The body's colour is untouched, only its alpha drops to
40%..56% (a little more solid than Michael, so the black still reads as black).  The pink rim and the
white pupil of T_Endling become Michael's holy fire, #FF3300 with a slightly hotter core, fully opaque,
and the model marks every eye texel as glowing (dungeons_models.py `glow="red"`).
Grid unchanged (64x32).
"""
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"D:\agent\dungeons_extract\upgrade\watchling\assets\Dungeons\Content\Content_DLC6\Actors\Characters\Enemies\Endling\T_Endling.png"
OUT = os.path.join(HERE, "watchling.png")

FIRE = (255, 51, 0)      # Michael's holy fire (his weapons, his armour's shadow)
CORE = (255, 72, 18)     # a hotter core; still inside the "red" glow mask (R > 170, G < 80, B < 80)


def main():
    a = np.array(Image.open(SRC).convert("RGBA"))
    rgb = a[..., :3].astype(int)
    lum = (rgb @ [0.2126, 0.7152, 0.0722]) / 255.0
    eye = (rgb[..., 0] > rgb[..., 1] + 30) | (lum > 0.6)
    pupil = eye & (lum > 0.6)
    rim = eye & ~pupil
    a[rim, :3] = FIRE
    a[pupil, :3] = CORE
    body = (a[..., 3] > 0) & ~eye
    lo, hi = np.percentile(lum[body], 2), np.percentile(lum[body], 98)
    t = np.clip((lum - lo) / max(hi - lo, 1e-6), 0, 1)
    a[body, 3] = np.rint(255 * (0.40 + 0.16 * t[body])).astype(np.uint8)
    a[eye, 3] = 255
    Image.fromarray(a).save(OUT)
    print("watchling texture: %s, %d eye texels" % (OUT, int(eye.sum())))


if __name__ == "__main__":
    main()
