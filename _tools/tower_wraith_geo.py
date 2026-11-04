# -*- coding: utf-8 -*-
"""罪仆·塔中幽魂 (Tower Wraith) -- Bedrock geometry after Minecraft Dungeons'
Tower Wraith, rebuilt from the original texture in tower_wraith_ref/.

The 64x64 texture (T_TowerWraith.png) is read as these nets:

* hood    8x12x8 box at 12,40: the gold-cornered top with its two gold
          squares, the front net open in a 4-wide strip down which the face
          and spine show, the back gold-edged;
* face    6x4x6 box at 2,2 inside the hood, eyes on its front; the blue gem
          below it is the 4x3 sprite at 9,12;
* sleeves 4x12x4 boxes at 4,16 and 44,16, gold square on the shoulder and
          gold-tipped rags at the cuff;
* robe    8x19x4 box at 20,16: sides at 20 and 32, the gold-hemmed back at
          36, its front open;
* brim    the two gold-edged panels at 39..62,0..10: front and back of a
          10x9x2 flap swept back from the top of the hood;
* banner  the gold and red tapestry at 50,39, hung down the back;
* bones   the grey strips at row 10 (ribs, claws) and 44,32 (spine).

The glowing eyes and gem (T_TowerWraith_S.png) are their own bone,
`eyes_glow`, of thin planes over those pixels.

Output: tower_wraith_ref/tower_wraith.geo.json, imported into Blockbench
through the MCP and refined there (pose, animations).  tower_wraith.bbmodel
is the source add_tower_wraith.py reads; re-running this script does not
reproduce the edits made in Blockbench.
"""

import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "tower_wraith_ref")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REF, "tower_wraith.geo.json")


def box(origin, size, uv):
    return {"origin": origin, "size": size, "uv": uv}


def faces(origin, size, uvmap):
    uv = {}
    for f, (u0, v0, u1, v1) in uvmap.items():
        uv[f] = {"uv": [u0, v0], "uv_size": [u1 - u0, v1 - v0]}
    return {"origin": origin, "size": size, "uv": uv}


def bone(name, pivot, cubes=(), parent=None, rotation=None):
    b = {"name": name, "pivot": pivot}
    if parent:
        b["parent"] = parent
    if rotation:
        b["rotation"] = rotation
    if cubes:
        b["cubes"] = list(cubes)
    return b


RIB = (36, 10, 41, 11)          # 5 grey pixels of the long bone strip
CLAW = (45, 38, 46, 41)          # a 1x3 run of the grey spine strip
CLAW_END = (45, 41, 46, 42)
DARK = (33, 26, 37, 37)


def claws(x0, side):
    """Three claws under a sleeve whose inner edge is x0."""
    out = []
    for i in range(3):
        x = x0 + side * (0.5 + 1.25 * i) - (1 if side < 0 else 0)
        out.append(faces([x, 4.5, -1.5 + 0.5 * i], [1, 3, 1], {
            "north": CLAW, "south": CLAW, "east": CLAW, "west": CLAW, "down": CLAW_END}))
    return out


bones = [
    bone("root", [0, 0, 0]),
    bone("body", [0, 16, 0], parent="root", cubes=[
        box([-4, 1, -2], [8, 19, 4], [20, 16]),
        # the robe's front is open: dark inside
        faces([-4, 1, 1], [8, 19, 0], {"north": DARK}),
    ]),
    bone("head", [0, 22, 0], parent="body", cubes=[
        box([-4, 14, -4], [8, 12, 8], [12, 40]),
        box([-3, 21, -3.5], [6, 4, 6], [2, 2]),
        faces([-2, 18, -3.5], [4, 3, 0], {"north": (9, 12, 13, 15)}),
        # what shows through the opening below the gem: ribs on a spine
        faces([-0.5, 14, -3], [1, 4, 1], {
            "north": (45, 33, 46, 37), "east": (44, 33, 45, 37), "west": (46, 33, 47, 37)}),
        faces([-2, 16.5, -3.2], [4, 0.75, 0.75], {"north": RIB, "up": RIB, "down": RIB}),
        faces([-2, 14.5, -3.2], [4, 0.75, 0.75], {"north": RIB, "up": RIB, "down": RIB}),
        # the hood's inside, so the opening does not show through to the back
        faces([-2, 14, 1], [4, 11, 0], {"north": DARK}),
    ]),
    bone("eyes_glow", [0, 22, 0], parent="head", cubes=[
        faces([-3, 23.5, -3.6], [2, 1, 0], {"north": (8, 9, 10, 10)}),
        faces([1, 23.5, -3.6], [2, 1, 0], {"north": (12, 9, 14, 10)}),
        faces([-1, 19, -3.6], [2, 1, 0], {"north": (10, 13, 12, 14)}),
    ]),
    # a 10x9x2 slab: front net 41..50 and back net 53..62, both gold-edged;
    # it hangs from the back of the hood top, swung back to lie nearly flat
    bone("brim", [0, 26, 4], parent="head", rotation=[65, 0, 0], cubes=[
        faces([-5, 17, 2], [10, 9, 2], {
            "north": (41, 0, 51, 9), "south": (53, 0, 63, 9),
            "east": (39, 0, 41, 9), "west": (51, 0, 53, 9), "down": (41, 8, 51, 9)}),
    ]),
    # flat on the robe's back, hung from under the hood, the fringe past the hem
    bone("banner", [0, 17, 2], parent="body", rotation=[8, 0, 0], cubes=[
        faces([-4.5, -3, 2], [9, 20, 1], {
            "south": (51, 40, 60, 60), "north": (60, 40, 51, 60),
            "east": (50, 40, 51, 60), "west": (60, 40, 61, 60), "up": (51, 39, 60, 40)}),
    ]),
    bone("right_arm", [-6, 19, 0], parent="body", rotation=[-25, 0, -8], cubes=[
        box([-8, 7, -2], [4, 12, 4], [4, 16]),
    ] + claws(-4, -1)),
    bone("left_arm", [6, 19, 0], parent="body", rotation=[-25, 0, 8], cubes=[
        box([4, 7, -2], [4, 12, 4], [44, 16]),
    ] + claws(4, 1)),
]

geo = {
    "format_version": "1.12.0",
    "minecraft:geometry": [{
        "description": {
            "identifier": "geometry.tower_wraith",
            "texture_width": 64,
            "texture_height": 64,
            "visible_bounds_width": 3,
            "visible_bounds_height": 3,
            "visible_bounds_offset": [0, 1.5, 0],
        },
        "bones": bones,
    }],
}

with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(geo, fh, indent=2)
print(OUT)
