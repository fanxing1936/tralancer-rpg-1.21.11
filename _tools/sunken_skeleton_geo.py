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
* No weapon is modelled: the servant's own (vanilla) mainhand item is
  drawn in the right hand by add_sunken_skeleton.py.

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



def build_atlas():
    Image.open(os.path.join(REF, "MCD_Sunken_Skeleton_(Tier_1_texture).png")).convert("RGBA").save(ATLAS)


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
            "texture_height": 32,
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
