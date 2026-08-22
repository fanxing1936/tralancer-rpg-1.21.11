# -*- coding: utf-8 -*-
"""Crop the new weapons' art so it fills its canvas like the rest of the pack.

Minecraft stretches an item texture to fill the inventory slot whatever its
source resolution, so what decides the on-screen size is how much of the canvas
the drawing actually occupies.  The pack's own weapons sit at 82-100%; three of
the previously-unused textures sat at 34-66% and rendered visibly smaller.
Cropping (never resampling) to the union bounding box of the whole animation set
fixes the scale without touching a single pixel of the artwork.
"""

import io
import os
import sys

import png_tool as P

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
TEX = os.path.join(RP, "assets/rpg/textures/item")

# every frame of one set must share a crop box or the animation would jitter.
# `baby_crossbows` is a spare alternate icon no model uses -- excluded so it
# cannot inflate the box for the six frames that are actually rendered.
SETS = {
    "baby_crossbow": ["baby_crossbow.png", "baby_crossbow_arrow.png",
                      "baby_crossbow_firework.png", "baby_crossbow_pulling_0.png",
                      "baby_crossbow_pulling_1.png", "baby_crossbow_pulling_2.png"],
    "vine_whip": ["vine_whip.png", "vine_whip_cast.png"],
    "truthseeker": ["truthseeker.png"],
}


def union_bbox(files):
    x0 = y0 = 10 ** 6
    x1 = y1 = -1
    canvas = None
    for f in files:
        w, h, rgba = P.read(os.path.join(TEX, f))
        canvas = (w, h)
        bb = P.bbox(w, h, rgba)
        if bb is None:
            continue
        x0, y0 = min(x0, bb[0]), min(y0, bb[1])
        x1, y1 = max(x1, bb[2]), max(y1, bb[3])
    return (x0, y0, x1, y1), canvas


def square(box, canvas):
    """Grow the box to a square, centred, clamped to the canvas."""
    x0, y0, x1, y1 = box
    cw, ch = canvas
    side = max(x1 - x0 + 1, y1 - y0 + 1)
    cx, cy = (x0 + x1 + 1) // 2, (y0 + y1 + 1) // 2
    nx0 = max(0, min(cw - side, cx - side // 2))
    ny0 = max(0, min(ch - side, cy - side // 2))
    return nx0, ny0, side


def crop(path, x0, y0, side):
    w, h, rgba = P.read(path)
    out = bytearray(side * side * 4)
    for y in range(side):
        s = ((y0 + y) * w + x0) * 4
        out[y * side * 4:(y + 1) * side * 4] = rgba[s:s + side * 4]
    P.write(path, side, side, bytes(out))


def main():
    changed = 0
    for name, files in SETS.items():
        box, canvas = union_bbox(files)
        x0, y0, side = square(box, canvas)
        before = 100.0 * (box[2] - box[0] + 1) / canvas[0]
        if side >= canvas[0]:
            print("  %-16s already fills the canvas, left alone" % name)
            continue
        for f in files:
            crop(os.path.join(TEX, f), x0, y0, side)
            changed += 1
        print("  %-16s %dx%d -> %dx%d   art fill %.0f%% -> 100%%   (%d frames)"
              % (name, canvas[0], canvas[1], side, side, before, len(files)))
    print("cropped %d files" % changed)


if __name__ == "__main__":
    main()
