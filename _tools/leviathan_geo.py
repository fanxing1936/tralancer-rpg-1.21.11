# -*- coding: utf-8 -*-
"""利维坦 (Leviathan) -- Bedrock geometry after Minecraft Dungeons'
Necromancer, rebuilt from the original 64x64 texture in leviathan_ref/.

The Necromancer is the Nameless One's own recolour (the texture keeps the
same islands, silver turned to old gold and green to sea cyan), so this is
beelzebub_geo.py with the Necromancer's pixels and palette: the same
skeleton nets used as box UV, the same composed robe, crown, belt and
pauldron tiles in the right half of a 128x128 atlas.  Only the staff head
differs: a glowing cyan cube held in a three-pronged fork.

Output: leviathan_ref/leviathan.geo.json.  leviathan.bbmodel was made in
Blockbench from beelzebub.bbmodel (same rig, poses and clips) with this
atlas and this staff head; it is the source add_leviathan_model.py reads,
and re-running this script does not reproduce the edits made there.
"""

import io
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "leviathan_ref")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REF, "leviathan.geo.json")
ATLAS = os.path.join(REF, "leviathan_atlas.png")

# palette sampled from MCD_Necromancer_(texture).png (same slots as the
# Nameless One's: SILVER is the old gold of the crown and trims)
SILVER_HI = (178, 162, 132, 255)
SILVER = (153, 137, 108, 255)
SILVER_LO = (101, 91, 72, 255)
GEM = (11, 156, 187, 255)
GEM_LO = (0, 121, 162, 255)
PURPLE_HI = (126, 88, 115, 255)
PURPLE = (97, 64, 91, 255)
PURPLE_LO = (63, 36, 61, 255)
SHADOW = (44, 26, 44, 255)
CLEAR = (0, 0, 0, 0)
ORB_HI = (120, 236, 255, 255)
ORB = (40, 200, 240, 255)
ORB_MID = (4, 159, 208, 255)
ORB_LO = (0, 121, 162, 255)
EYE = (0, 255, 255, 255)
WHITE = (221, 209, 182, 255)

# tiles in the atlas's right half: name -> (u, v, w, h)
T = {
    "crown_out": (64, 0, 10, 6), "crown_in": (64, 8, 10, 6),
    "skirt_front": (80, 0, 10, 12), "skirt_side": (92, 0, 6, 12), "skirt_back": (100, 0, 10, 12),
    "belt_front": (64, 16, 10, 3), "belt_side": (76, 16, 6, 3), "belt_back": (84, 16, 10, 3),
    "belt_top": (64, 20, 10, 6),
    "paul_top": (96, 16, 6, 6), "paul_side": (104, 16, 6, 5), "paul_bottom": (112, 16, 6, 6),
    "orb_side": (64, 32, 6, 6), "orb_top": (72, 32, 6, 6), "orb_bottom": (64, 40, 6, 6),
    "eye": (80, 32, 1, 1),
}


def build_atlas():
    src = Image.open(os.path.join(REF, "MCD_Necromancer_(texture).png")).convert("RGBA")
    sp = src.load()
    atlas = Image.new("RGBA", (128, 128), CLEAR)
    atlas.paste(src, (0, 0))
    px = atlas.load()

    def put(tile, x, y, c):
        u, v, _, _ = T[tile]
        px[u + x, v + y] = c

    def fill(tile, c):
        _, _, w, h = T[tile]
        for y in range(h):
            for x in range(w):
                put(tile, x, y, c)

    # crown: silver band with the green gem centred, white spikes on the
    # corners and at the thirds (the original crown front at 0,0 is 8 wide;
    # the crown sits around the 8px hood, so it is widened to 10)
    for x in range(10):
        put("crown_out", x, 3, SILVER_HI)
        put("crown_out", x, 4, SILVER)
        put("crown_out", x, 5, SILVER_LO)
        put("crown_in", x, 3, SILVER)
        put("crown_in", x, 4, SILVER_LO)
        put("crown_in", x, 5, SHADOW)
    for x, top in ((0, 0), (3, 1), (6, 1), (9, 0)):
        for y in range(top, 3):
            put("crown_out", x, y, SILVER_HI if y > top else WHITE)
            put("crown_in", x, y, SILVER)
    for x, y, c in ((4, 3, GEM), (5, 3, GEM), (4, 4, GEM_LO), (5, 4, GEM), (4, 2, SILVER_HI), (5, 2, SILVER_HI)):
        put("crown_out", x, y, c)

    # robe skirt: the original panel at (38..47, 6..15) with its tattered
    # hem; two rows of the top colour added above, green stripes on both
    # front edges like the renders
    for tile, stripes in (("skirt_front", True), ("skirt_back", False), ("skirt_side", False)):
        _, _, w, _ = T[tile]
        for y in range(12):
            sy = 6 + max(0, y - 2)
            for x in range(w):
                put(tile, x, y, sp[38 + x, sy])
        if stripes:
            for y in range(12):
                sy = 6 + max(0, y - 2)
                g = sp[37, sy]
                if g[3]:
                    put(tile, 1, y, g)
                    put(tile, 8, y, g)

    # belt: the strip painted into the ribcage net (row 29..31), gem centred
    for x in range(10):
        for y in range(3):
            put("belt_front", x, y, sp[19 + x, 29 + y])
            put("belt_back", x, y, sp[26 + (x % 6), 29 + y])
    for x in range(6):
        for y in range(3):
            put("belt_side", x, y, sp[26 + x, 29 + y])
    fill("belt_top", PURPLE_LO)

    # pauldrons: dark plate with a lighter rim on top, silver trim at the
    # lower edge of the sides
    fill("paul_top", PURPLE_LO)
    for i in range(6):
        for x, y in ((i, 0), (i, 5), (0, i), (5, i)):
            put("paul_top", x, y, PURPLE_HI)
    for x in range(6):
        put("paul_side", x, 0, PURPLE_HI)
        put("paul_side", x, 1, PURPLE_LO)
        put("paul_side", x, 2, PURPLE if x % 3 else PURPLE_LO)
        put("paul_side", x, 3, SILVER_HI)
        put("paul_side", x, 4, SILVER_LO)
    fill("paul_bottom", SHADOW)

    # staff head: a glowing cube, lit from above -- bright top, a lighter
    # band near the top of each side, darker toward the fork
    for x in range(64, 80):
        for y in range(32, 48):
            if (x, y) != T["eye"][:2]:
                px[x, y] = CLEAR
    for y in range(6):
        for x in range(6):
            rim = x in (0, 5) or y in (0, 5)
            put("orb_top", x, y, ORB if rim else ORB_HI)
            put("orb_side", x, y, ORB_HI if y == 0 else ORB if y < 3 else ORB_MID if y < 5 else ORB_LO)
            put("orb_bottom", x, y, ORB_LO)
    fill("eye", EYE)
    atlas.save(ATLAS)


def box(origin, size, uv, inflate=0, mirror=False):
    c = {"origin": origin, "size": size, "uv": uv}
    if inflate:
        c["inflate"] = inflate
    if mirror:
        c["mirror"] = True
    return c


def faces(origin, size, uvmap, inflate=0):
    """Per-face UV: uvmap = {face: tile name | (u0, v0, u1, v1)}."""
    uv = {}
    for f, t in uvmap.items():
        if isinstance(t, str):
            u, v, w, h = T[t]
            t = (u, v, u + w, v + h)
        u0, v0, u1, v1 = t
        uv[f] = {"uv": [u0, v0], "uv_size": [u1 - u0, v1 - v0]}
    return box(origin, size, uv, inflate)


def flip(t):
    u, v, w, h = T[t]
    return (u + w, v, u, v + h)


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

POLE = (8, 33, 10, 52)       # dark staff shaft in the original, 2 x 19
ORB_C = [-5, 35, 0]          # staff head centre, in the fork


bones = [
    bone("root", [0, 0, 0]),
    bone("body", [0, 14, 0], parent="root", cubes=[
        # ribcage with its holes, belt painted into the bottom rows
        box([-4, 14, -2], [8, 12, 4], [16, 16]),
    ]),
    bone("belt", [0, 14, 0], parent="body", cubes=[
        faces([-5, 13, -3], [10, 3, 6], {
            "north": "belt_front", "south": "belt_back", "east": "belt_side", "west": "belt_side",
            "up": "belt_top", "down": "belt_top"}, inflate=0.25),
    ]),
    # the robe hangs from the belt; open at the top and the hem
    bone("skirt", [0, 14, 0], parent="body", cubes=[
        faces([-5, 2, -3], [10, 12, 6], {
            "north": "skirt_front", "south": "skirt_back", "east": "skirt_side", "west": "skirt_side"}),
    ]),
    bone("right_pauldron", [0, 14, 0], parent="body", cubes=[
        faces([-9.5, 23, -3], [6, 5, 6], {
            "north": "paul_side", "south": "paul_side", "east": "paul_side", "west": "paul_side",
            "up": "paul_top", "down": "paul_bottom"}),
    ]),
    bone("left_pauldron", [0, 14, 0], parent="body", cubes=[
        faces([3.5, 23, -3], [6, 5, 6], {
            "north": "paul_side", "south": "paul_side", "east": "paul_side", "west": "paul_side",
            "up": "paul_top", "down": "paul_bottom"}),
    ]),
    bone("head", [0, 26, 0], parent="body", cubes=[
        box([-4, 26, -4], [8, 8, 8], [0, 0]),
    ]),
    # the _E layer marks (10,12) and (13,12): head-front v=12 is y 29..30,
    # u 10 and 13 are 2px in from either edge of the 8px face
    bone("eyes_glow", [0, 26, 0], parent="head", cubes=[
        faces([-2, 29, -4.05], [1, 1, 0], {"north": "eye"}),
        faces([1, 29, -4.05], [1, 1, 0], {"north": "eye"}),
    ]),
    bone("crown", [0, 26, 0], parent="head", cubes=[
        faces([-5, 32, -5], [10, 6, 0], {"north": "crown_out", "south": "crown_in"}),
        faces([-5, 32, 5], [10, 6, 0], {"south": "crown_out", "north": flip("crown_in")}),
        faces([-5, 32, -5], [0, 6, 10], {"east": "crown_in", "west": "crown_out"}),
        faces([5, 32, -5], [0, 6, 10], {"east": "crown_out", "west": "crown_in"}),
    ]),
    bone("right_arm", [-5, 25, 0], parent="body", cubes=[
        box([-6, 14, -1], [2, 12, 2], [40, 16]),
    ]),
    bone("left_arm", [5, 25, 0], parent="body", cubes=[
        box([4, 14, -1], [2, 12, 2], [40, 16], mirror=True),
    ]),
    # staff through the right fist (y 15): shaft, then a fork whose
    # crossbar and two prongs hold the cube from below
    bone("staff", [-5, 15, 0], parent="right_arm", cubes=[
        faces([-6, -8, -1], [2, 19, 2], {f: POLE for f in ("north", "south", "east", "west", "down")}),
        faces([-6, 11, -1], [2, 19, 2], {f: POLE for f in ("north", "south", "east", "west")}),
        faces([-8.5, 30, -1], [7, 1.5, 2], {f: POLE for f in ("north", "south", "east", "west", "up", "down")}),
        faces([-8.5, 31.5, -1], [1.5, 3.5, 2], {f: POLE for f in ("north", "south", "east", "west", "up")}),
        faces([-3, 31.5, -1], [1.5, 3.5, 2], {f: POLE for f in ("north", "south", "east", "west", "up")}),
    ]),
    bone("gem", ORB_C, parent="staff", cubes=[
        faces([ORB_C[0] - 3, ORB_C[1] - 3, ORB_C[2] - 3], [6, 6, 6], {
            "north": "orb_side", "south": "orb_side", "east": "orb_side", "west": "orb_side",
            "up": "orb_top", "down": "orb_bottom"}),
    ]),
    bone("cape", [0, 27, 3], parent="body", rotation=[6, 0, 0], cubes=[
        faces([-8, 3, 3], [16, 24, 1], {
            "south": (48, 8, 64, 32), "north": (64, 8, 48, 32),
            "east": (48, 8, 49, 32), "west": (63, 8, 64, 32), "up": (48, 8, 64, 9)}),
    ]),
]

geo = {
    "format_version": "1.12.0",
    "minecraft:geometry": [{
        "description": {
            "identifier": "geometry.leviathan",
            "texture_width": 128,
            "texture_height": 128,
            "visible_bounds_width": 4,
            "visible_bounds_height": 4,
            "visible_bounds_offset": [0, 1.5, 0],
        },
        "bones": bones,
    }],
}

with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(geo, fh, indent=2)
print(OUT)
