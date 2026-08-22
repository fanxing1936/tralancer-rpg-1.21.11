# -*- coding: utf-8 -*-
"""Bring the author's twin-blade art into the pack at its native resolution.

The two uploads are clean 8x nearest-neighbour blow-ups of 16x16 sprites, so
taking every 8th pixel recovers the original art exactly -- no resampling, no
colour loss, and the file drops from ~1 KB of stretched pixels to a real 16x16.
"""

import io
import os
import shutil
import sys

import png_tool as P

SRC = r"C:/Users/A/.claude/uploads/452820ef-8f59-425a-915b-6ef790c13ac8"
RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
TEX = os.path.join(RP, "assets/rpg/textures/item")
KEEP = os.path.join(os.path.dirname(__file__), "twin_art")

# upload -> the blade it belongs to (identified by dominant hue)
MAP = {"50fdca1e-862242.png": "jachin",   # purple blade, gold furniture
       "2d4d4a4d-862244.png": "boaz"}     # teal blade, pink edge


def downscale(w, h, rgba, factor):
    n = w // factor
    out = bytearray(n * n * 4)
    for y in range(n):
        for x in range(n):
            s = ((y * factor) * w + x * factor) * 4
            out[(y * n + x) * 4:(y * n + x) * 4 + 4] = rgba[s:s + 4]
    return n, bytes(out)


def block_factor(w, h, rgba):
    """Largest k for which every kxk block is a single colour."""
    for k in (16, 8, 4, 2):
        if w % k or h % k:
            continue
        ok = True
        for by in range(h // k):
            for bx in range(w // k):
                ref = rgba[((by * k) * w + bx * k) * 4:((by * k) * w + bx * k) * 4 + 4]
                for dy in range(k):
                    row = ((by * k + dy) * w + bx * k) * 4
                    if rgba[row:row + k * 4] != ref * k:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            return k
    return 1


def main():
    if not os.path.isdir(KEEP):
        os.makedirs(KEEP)
    done = []
    for upload, name in MAP.items():
        src = os.path.join(SRC, upload)
        kept = os.path.join(KEEP, name + ".png")
        if os.path.isfile(src):
            w, h, rgba = P.read(src)
            k = block_factor(w, h, rgba)
            n, small = downscale(w, h, rgba, k)
            P.write(kept, n, n, small)
            note = "%dx%d /%d -> %dx%d" % (w, h, k, n, n)
        elif os.path.isfile(kept):
            n = P.read(kept)[0]
            note = "from _tools/twin_art (upload no longer on disk)"
        else:
            print("  %-8s no source art found" % name)
            continue
        shutil.copy(kept, os.path.join(TEX, name + ".png"))
        done.append("%s (%s)" % (name, note))
    print("twin art imported: %s" % "; ".join(done))


if __name__ == "__main__":
    main()
