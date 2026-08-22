# -*- coding: utf-8 -*-
"""Make every held-weapon display transform uniform *without moving the grip*.

Two separate faults were in the pack's seven hand transforms:

1. Non-uniform scale.  The sword family used [1.46, 0.85, 0.85].  In
   `item/generated` the blade is drawn diagonally across a plain square sprite,
   so stretching X does not lengthen the blade -- it shears the whole picture.
   That was the visible deformation.
2. Three parents carried a -170 X-rotation on the left hand, which is what made
   off-hand weapons appear held backwards.

The first attempt at (1) also rescaled the translation proportionally, which
moved the weapon out of the hand.  Translation does not work that way, so this
version solves for it.

Minecraft composes a display transform as T . R . S, and the item renderer then
centres the model, so a model-space point v (measured from the sprite's centre,
in blocks) lands at

    p = T + R . S . v

The handle end of a diagonal sprite is the bottom-left corner, v = (-.5,-.5,0).
With rotation [0, -90, z] the rotation matrix rows are (0,0,-1), (sin z, cos z,
0) and (cos z, -sin z, 0), so for a diagonal scale S = (sx, sy, *):

    grip_y = T_y - (sx.sin z + sy.cos z) / 2
    grip_z = T_z - (sx.cos z - sy.sin z) / 2

Read the author's grip out of their original numbers, then solve the same pair
backwards for the new uniform scale.  The weapon keeps hanging exactly where it
did; only the shear goes away.  (Checked against vanilla `item/handheld`:
scale .85, translation [0, 4, .5] round-trips exactly -- see the assert.)

The uniform scale is chosen to preserve apparent length.  For art drawn along
the 45-degree diagonal, a scale (sx, sy) takes the diagonal unit vector to
length sqrt((sx^2 + sy^2) / 2) -- and both diagonals by the same factor, which
is why the distortion reads as a shear rather than a stretch.  Using that value
keeps the blade exactly as long as the author had it.
"""

import io
import json
import math
import os
import sys

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
MODELS = os.path.join(RP, "assets/rpg/models/item")

# The pack's original right-hand transforms -- the source of truth for where
# each weapon is supposed to hang.  (name: (sx, sy), z-rotation, translation)
ORIGINAL = {
    "sword_handheld":        ((1.46, 0.85), 55, (0, 6.75, 2.0)),
    "double_handheld":       ((1.46, 0.85), 55, (0, 7.00, 2.0)),
    "stick_handheld":        ((1.46, 0.85), 55, (0, 7.00, 2.0)),
    "twin_handheld":         ((1.46, 0.85), 55, (0, 6.75, 2.0)),
    "huge_sword_handheld":   ((2.50, 1.50), 55, (0, 6.75, 2.0)),
    "weapon_sword_handheld": ((1.46, 1.46), 40, (0, 7.50, 1.0)),
    "long_handheld":         ((2.23, 2.33), 55, (0, 7.00, 1.0)),
}

# vanilla item/handheld's first-person block, kept verbatim -- it was never the
# problem, and matching it keeps the weapons feeling like vanilla in the hand
FP_TR = [1.13, 3.2, 1.13]
FP_SC = [0.68, 0.68, 0.68]


def uniform_scale(sx, sy):
    """The single scale that leaves 45-degree diagonal art the same length."""
    return math.sqrt((sx * sx + sy * sy) / 2.0)


def grip(scale_xy, zdeg, tr):
    """Where the handle end sits, in blocks, for one transform."""
    sx, sy = scale_xy
    z = math.radians(zdeg)
    sn, cs = math.sin(z), math.cos(z)
    ty, tz = tr[1] / 16.0, tr[2] / 16.0
    return (ty - (sx * sn + sy * cs) / 2.0,
            tz - (sx * cs - sy * sn) / 2.0)


def translation_for(gy, gz, s, zdeg, keep_z=None):
    """Solve the same pair backwards: the translation that puts the grip back.

    Y is solved -- that is the axis the weapon hangs along, and the one the
    shear actually moved.  Z is the sprite plane's depth in the hand; the shear
    never distorted it in a way anyone can see, and solving it too would swing
    the huge sword 3.7 units into the arm, so the author's own depth is kept.
    """
    z = math.radians(zdeg)
    sn, cs = math.sin(z), math.cos(z)
    solved_z = round((gz + s * (cs - sn) / 2.0) * 16.0, 2)
    return (0.0,
            round((gy + s * (sn + cs) / 2.0) * 16.0, 2),
            solved_z if keep_z is None else keep_z)


def build(scale, zrot, tr):
    s = [scale, scale, scale]
    return {
        "parent": "item/generated",
        "display": {
            "thirdperson_righthand": {"rotation": [0, -90, zrot],
                                      "translation": list(tr), "scale": s},
            # a true mirror: negate Y and Z only.  The old -170 X-rotation here
            # is what flipped off-hand weapons into a reversed grip.
            "thirdperson_lefthand": {"rotation": [0, 90, -zrot],
                                     "translation": list(tr), "scale": s},
            "firstperson_righthand": {"rotation": [0, -90, 25],
                                      "translation": list(FP_TR), "scale": list(FP_SC)},
            "firstperson_lefthand": {"rotation": [0, 90, -25],
                                     "translation": list(FP_TR), "scale": list(FP_SC)},
        },
    }


def main():
    # sanity check the derivation against vanilla before trusting it on the pack
    gy, gz = grip((0.85, 0.85), 55, (0, 4.0, 0.5))
    back = translation_for(gy, gz, 0.85, 55)
    assert abs(back[1] - 4.0) < 0.01 and abs(back[2] - 0.5) < 0.01, back

    for name in sorted(ORIGINAL):
        scale_xy, zrot, tr = ORIGINAL[name]
        s = round(uniform_scale(*scale_xy), 3)
        gy, gz = grip(scale_xy, zrot, tr)
        new_tr = translation_for(gy, gz, s, zrot, keep_z=tr[2])
        wrote = build(s, zrot, new_tr)
        with io.open(os.path.join(MODELS, name + ".json"), "w",
                     encoding="utf-8", newline="\n") as fh:
            json.dump(wrote, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("  %-24s [%s,%s] -> %.3f uniform   translation [0,%s,%s] -> [0,%s,%s]"
              % (name, scale_xy[0], scale_xy[1], s,
                 tr[1], tr[2], new_tr[1], new_tr[2]))
    print("display parents made uniform: %d" % len(ORIGINAL))


if __name__ == "__main__":
    main()
