# -*- coding: utf-8 -*-
"""罪仆·沉没骷髅 (Sunken Skeleton) -- Bedrock geometry after Minecraft
Dungeons' Sunken Skeleton, rebuilt from the original Tier 1 texture in
sunken_skeleton_ref/.

* The texture (64x32) keeps the skeleton nets, except that arms and legs
  trade places: the mossy limb net at 0,16 is the arms, the one with the
  purple feet at 40,16 the legs.  Head 8x8x8 at 0,0 and the kelp-hung
  ribcage 8x12x4 at 16,16 are as in vanilla.
* The coral that grows out of the skull is drawn as sprites in the free
  rows at 24..40,0..10: the purple branch (32..40) stands on the crown as
  two crossed planes, the small purple-and-orange piece (26..32) sticks out
  of the right side.
* The crossbow the Tier 1 skeleton carries has no texture on the wiki; it
  is built from cubes and painted from four swatches (wood, dark wood,
  iron, string) in the atlas.

Output: sunken_skeleton_ref/sunken_skeleton.geo.json, imported into
Blockbench through the MCP and refined there (pose, animations).
sunken_skeleton.bbmodel is the source add_sunken_skeleton.py reads;
re-running this script does not reproduce the edits made in Blockbench.
"""

import io
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "sunken_skeleton_ref")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REF, "sunken_skeleton.geo.json")
ATLAS = os.path.join(REF, "sunken_skeleton_atlas.png")

SWATCH = {                      # name -> (u, v), 2x2 each, below the texture
    "wood": ((116, 77, 44, 255), (0, 32)),
    "wood_dark": ((72, 46, 26, 255), (2, 32)),
    "iron": ((122, 122, 122, 255), (4, 32)),
    "string": ((52, 40, 30, 255), (6, 32)),
}


def build_atlas():
    atlas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    atlas.alpha_composite(Image.open(os.path.join(REF, "MCD_Sunken_Skeleton_(Tier_1_texture).png")).convert("RGBA"))
    px = atlas.load()
    for colour, (u, v) in SWATCH.values():
        for y in range(2):
            for x in range(2):
                px[u + x, v + y] = colour
    atlas.save(ATLAS)


def box(origin, size, uv, mirror=False):
    c = {"origin": origin, "size": size, "uv": uv}
    if mirror:
        c["mirror"] = True
    return c


def faces(origin, size, uvmap):
    uv = {}
    for f, (u0, v0, u1, v1) in uvmap.items():
        uv[f] = {"uv": [u0, v0], "uv_size": [u1 - u0, v1 - v0]}
    return {"origin": origin, "size": size, "uv": uv}


def solid(origin, size, swatch):
    u, v = SWATCH[swatch][1]
    t = (u, v, u + 1, v + 1)
    return faces(origin, size, {f: t for f in ("north", "south", "east", "west", "up", "down")})


def bone(name, pivot, cubes=(), parent=None, rotation=None):
    b = {"name": name, "pivot": pivot}
    if parent:
        b["parent"] = parent
    if rotation:
        b["rotation"] = rotation
    if cubes:
        b["cubes"] = list(cubes)
    return b


build_atlas()
BRANCH = (32, 0, 40, 10)
BRANCH_BACK = (40, 0, 32, 10)
SPRIG = (26, 0, 32, 8)
SPRIG_BACK = (32, 0, 26, 8)

bones = [
    bone("root", [0, 0, 0]),
    bone("body", [0, 12, 0], parent="root", cubes=[
        box([-4, 12, -2], [8, 12, 4], [16, 16]),
    ]),
    bone("head", [0, 24, 0], parent="body", cubes=[
        box([-4, 24, -4], [8, 8, 8], [0, 0]),
    ]),
    # two crossed planes on the crown, and a sprig out of the right side
    bone("coral", [0, 32, 0], parent="head", rotation=[0, 45, 0], cubes=[
        faces([-4, 31, 0], [8, 10, 0], {"north": BRANCH, "south": BRANCH_BACK}),
        faces([0, 31, -4], [0, 10, 8], {"east": BRANCH, "west": BRANCH_BACK}),
    ]),
    bone("sprig", [-4, 28, 1], parent="head", rotation=[0, 0, -20], cubes=[
        faces([-10, 26, 1], [6, 8, 0], {"north": SPRIG, "south": SPRIG_BACK}),
    ]),
    bone("right_arm", [-5, 22, 0], parent="body", cubes=[
        box([-6, 12, -1], [2, 12, 2], [0, 16]),
    ]),
    bone("left_arm", [5, 22, 0], parent="body", cubes=[
        box([4, 12, -1], [2, 12, 2], [0, 16], mirror=True),
    ]),
    # crossbow in the right fist, level and pointing forward (-z): stock,
    # prod with iron tips swept back, string; posed in Blockbench
    bone("crossbow", [-5, 13, 0], parent="right_arm", cubes=[
        solid([-6, 12, -9], [2, 2, 12], "wood"),
        solid([-6, 11, 1], [2, 1, 2], "wood_dark"),
        solid([-9, 12.25, -9], [8, 1.5, 1.5], "wood_dark"),
        solid([-13, 12.25, -8], [4, 1.5, 1.5], "wood_dark"),
        solid([-1, 12.25, -8], [4, 1.5, 1.5], "wood_dark"),
        solid([-14, 12.25, -7], [1.5, 1.5, 1.5], "iron"),
        solid([2.5, 12.25, -7], [1.5, 1.5, 1.5], "iron"),
        solid([-13, 12.75, -5.75], [16, 0.5, 0.5], "string"),
    ]),
    bone("right_leg", [-2, 12, 0], parent="root", cubes=[
        box([-3, 0, -1], [2, 12, 2], [40, 16]),
    ]),
    bone("left_leg", [2, 12, 0], parent="root", cubes=[
        box([1, 0, -1], [2, 12, 2], [40, 16], mirror=True),
    ]),
]

geo = {
    "format_version": "1.12.0",
    "minecraft:geometry": [{
        "description": {
            "identifier": "geometry.sunken_skeleton",
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
