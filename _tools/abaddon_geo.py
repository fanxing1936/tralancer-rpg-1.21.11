# -*- coding: utf-8 -*-
"""亚巴顿 (Abaddon) -- Bedrock geometry after Minecraft Dungeons' Wretched
Wraith, rebuilt from the original textures in abaddon_ref/.

The boss has no animations of its own on the wiki, so it shares the Tower
Wraith's (tower_wraith.bbmodel): the bones here carry the same names and
roles (root, body, head, eyes_glow, right_arm, left_arm), and
add_abaddon_model.py bakes the Tower Wraith clips onto them.

The 256x256 texture (MCD_Wretched_Wraith_(texture).png) is read as box UV
nets, checked against the wiki's front render (MCD_Wretched_Wraith_face.png,
4 px per texel), whose head frame matches the texture pixel for pixel:

* head      14x17x17 box at 0,27: frosted top, dark sides flecked pink, the
            front open in a strip through which the face shows;
* face      the 12x13 plate at 13,89 behind the opening (eye band and jaw);
            the eyes (26,91 / 33,91) and mouth (29,98) glow as small sprites
            in front of it, where the render shows them;
* crown     eight thin shards cut from the 20x20x1 shard net at 0..41,0..19
            (the two tall spikes are its posts), round the head's rim as
            in the render; above them floats the pink gem (sides
            110..133,2..9);
* body      a 14x29x10 box at 62,13, its front open on the ribs (the grey
            strips at 0,112 and 21,112) over a dark inside;
* sleeves   6x24x7 boxes at 62,52 and 87,50 (frost along the top, rags below);
* forearms  2x23x2 boxes at 111,26;
* fists     11x20x11 boxes at 49,84 and 93,84, the fingers in the lower rows;
            laid flat so the fingers reach forward, as in the render.

Output: abaddon_ref/abaddon_atlas.png and abaddon_ref/abaddon.geo.json,
imported into Blockbench through the MCP and refined there.  abaddon.bbmodel
is the source add_abaddon_model.py reads; re-running this script does not
reproduce the edits made in Blockbench.
"""

import io
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "abaddon_ref")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REF, "abaddon.geo.json")
ATLAS = os.path.join(REF, "abaddon_atlas.png")
GLOW_DV = 100                    # emissive copy of the head net: rows 127..161


def build_atlas():
    tex = Image.open(os.path.join(REF, "MCD_Wretched_Wraith_(texture).png")).convert("RGBA")
    emi = Image.open(os.path.join(REF, "T_Wicked_Wraith_E_01.png")).convert("RGB")
    out = tex.copy()
    for y in range(27, 62):
        for x in range(0, 64):
            r, g, b = emi.getpixel((x, y))
            p = tex.getpixel((x, y))
            if p[3] and r + g + b > 60:
                out.putpixel((x, y + GLOW_DV), p)
    out.save(ATLAS)


def box(origin, size, uv, inflate=0):
    c = {"origin": origin, "size": size, "uv": uv}
    if inflate:
        c["inflate"] = inflate
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


def flip(r):
    u0, v0, u1, v1 = r
    return (u1, v0, u0, v1)


def shard(origin, w, h, col, side=False):
    """A 1-thick ice shard, w wide and h tall: the bottom h rows of columns
    col..col+w of the shard net's north face (1..20) and, behind it, the
    same columns of its south face (22..41)."""
    n = (1 + col, 20 - h, 1 + col + w, 20)
    s_ = (22 + 20 - col - w, 20 - h, 22 + 20 - col, 20)
    edge = (0, 20 - h, 1, 20)
    if side:                              # facing east-west
        return faces(origin, [1, h, w], {"east": n, "west": s_, "north": edge, "south": edge})
    return faces(origin, [w, h, 1], {"north": n, "south": s_, "east": edge, "west": edge})


def arm(side, sleeve_uv, sleeve_d, fist_uv):
    """side -1: right (bedrock -x), +1: left."""
    x = 10 * side                         # the sleeve's inner side against the torso
    name = "right" if side < 0 else "left"
    return [
        bone(name + "_arm", [x, 48, 0], parent="body", rotation=[-10, 0, -3 * side], cubes=[
            box([x - 3, 26, -sleeve_d / 2.0], [6, 24, sleeve_d], sleeve_uv),
            box([x - 1, 16, -1], [2, 23, 2], [111, 26]),
        ]),
        # the hand lies flat, its fingers (the lower rows of the net) reaching forward
        bone(name + "_fist", [x, 10, 0], parent=name + "_arm", rotation=[-90, 0, 0], cubes=[
            box([x - 5.5, 0, -5.5], [11, 20, 11], fist_uv),
        ]),
    ]


build_atlas()
DARK = (94, 27, 106, 43)              # a clean dark patch of the robe, no glowing flecks
GEM_SIDE = [(110, 3, 116, 9), (116, 3, 122, 9), (122, 3, 128, 9), (128, 3, 134, 9)]
GEM_CAP = (116, 10, 122, 16)

bones = [
    bone("root", [0, 0, 0]),
    bone("body", [0, 36, 0], parent="root", cubes=[
        box([-7, 20, -5], [14, 29, 10], [62, 13]),
        # behind the open front: dark inside, ribs across it (the render shows
        # a dark chest with pale ribs)
        faces([-6, 31, 3], [12, 14, 0], {"north": DARK}),
        faces([-5, 43, -3], [10, 1, 0], {"north": (0, 112, 16, 114)}),
        faces([-5, 39, -3], [10, 1, 0], {"north": (21, 112, 37, 114)}),
        faces([-5, 35, -3], [10, 1, 0], {"north": (0, 112, 16, 114)}),
    ]),
    bone("head", [0, 50, 0], parent="body", cubes=[
        box([-7, 48, -8.5], [14, 17, 17], [0, 27]),
        faces([-6, 50, -7.9], [12, 13, 0], {"north": (13, 89, 25, 102)}),
        faces([-6, 48, -6], [12, 16, 0], {"north": DARK}),
    ]),
    # the crown: eight thin shards cut from the one 20x20x1 shard net at 0,-1
    # (north face 1..20, south face 22..41), standing round the rim and sunk
    # into the head; crown_b turns four of them onto the corners
    bone("crown", [0, 65, 0], parent="head", cubes=[
        shard([-6, 59, -6], 5, 16, 0),
        shard([1, 59, 5], 5, 18, 14),
        shard([-6.5, 59, -1], 4, 14, 8, side=True),
        shard([5.5, 59, -3], 4, 15, 3, side=True),
    ]),
    bone("crown_b", [0, 65, 0], parent="head", rotation=[0, 45, 0], cubes=[
        shard([-2, 59, -8], 4, 13, 10),
        shard([-2, 59, 7], 5, 20, 15),
        shard([-8, 59, -2], 4, 12, 5, side=True),
        shard([7, 59, -2], 4, 17, 12, side=True),
    ]),
    bone("eyes_glow", [0, 50, 0], parent="head", cubes=[
        box([-7, 48, -8.5], [14, 17, 17], [0, 27 + GLOW_DV], inflate=0.05),
        faces([1, 59, -8.6], [3, 2, 0], {"north": (26, 91, 29, 93)}),
        faces([-4, 59, -8.6], [3, 2, 0], {"north": (33, 91, 36, 93)}),
        faces([-2, 52, -8.6], [4, 2, 0], {"north": (29, 98, 33, 100)}),
    ]),
    bone("gem", [0, 75, 0], parent="head", cubes=[
        faces([-3, 72, -3], [6, 6, 6], {
            "north": GEM_SIDE[0], "east": GEM_SIDE[1], "south": GEM_SIDE[2], "west": GEM_SIDE[3],
            "up": GEM_CAP, "down": GEM_CAP}),
    ]),
] + arm(-1, [62, 52], 7, [49, 84]) + arm(1, [87, 50], 9, [93, 84])

geo = {
    "format_version": "1.12.0",
    "minecraft:geometry": [{
        "description": {
            "identifier": "geometry.abaddon",
            "texture_width": 256,
            "texture_height": 256,
            "visible_bounds_width": 6,
            "visible_bounds_height": 6,
            "visible_bounds_offset": [0, 3, 0],
        },
        "bones": bones,
    }],
}

with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(geo, fh, indent=2)
print(OUT)
