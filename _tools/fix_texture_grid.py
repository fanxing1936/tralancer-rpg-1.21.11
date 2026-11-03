# -*- coding: utf-8 -*-
"""Store every item texture on its native pixel grid (ART-STYLE.md §4).

Several sprites reach the pack as integer blow-ups of 16 px art -- the seven
pact books and the covenant pair at 128 px (x8), 熔岩链锯 at 32 px (x2).  The
client stretches every item texture to the slot anyway, so the blow-up buys
nothing on screen; it only hides the real grid from anyone reading the pack
and costs atlas space.  A sprite that is *exactly* a nearest-neighbour blow-up
is shrunk back losslessly -- every pixel of the artwork survives.

One sprite is not exact: the authored 新约 (new_covenant) arrived as a 192 px
smooth resample of 16 px art, carrying ~4300 noise colours.  It is recovered
with the same majority-vote reconstruction the Lucifer spear uses
(``add_lucifer.reconstruct``), as agreed in ART-STYLE.md decision D6.

Runs last in both rp_build.sh and build.sh, after every generator that
writes item textures.
"""

import os
import sys

import png_tool as P

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
TEX = os.path.join(RP, "assets/rpg/textures/item")

# Sprites known to be smooth resamples rather than exact blow-ups.
RESAMPLED = {"new_covenant": 16}


def exact_native(w, h, rgba):
    """The vanilla-sized grid (16, else 32) this square sprite is an exact
    nearest blow-up of, or None."""
    if w != h:
        return None
    for n in (16, 32):
        if n >= w or w % n:
            continue
        if P.nearest(n, n, P.nearest(w, h, rgba, n, n), w, h) == rgba:
            return n
    return None


def main():
    changed = []
    for name in sorted(os.listdir(TEX)):
        if not name.endswith(".png"):
            continue
        stem = name[:-4]
        path = os.path.join(TEX, name)
        w, h, rgba = P.read(path)
        if stem in RESAMPLED and w > RESAMPLED[stem]:
            import add_lucifer
            n = RESAMPLED[stem]
            P.write(path, n, n, add_lucifer.reconstruct(w, h, rgba, n))
            changed.append("%s %d->%d (reconstructed)" % (stem, w, n))
            continue
        if w < 32:
            continue
        n = exact_native(w, h, rgba)
        # only ever to a vanilla-sized grid; an author's 32 px sprite with no
        # 2x2 redundancy is left exactly as drawn
        if n:
            P.write(path, n, n, P.nearest(w, h, rgba, n, n))
            changed.append("%s %d->%d" % (stem, w, n))
    print("texture grid: %d stored at native size%s" % (
        len(changed), (": " + ", ".join(changed)) if changed else ""))


if __name__ == "__main__":
    main()
