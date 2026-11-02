# -*- coding: utf-8 -*-
"""Tower Guard (Minecraft Dungeons) -- Bedrock geometry rebuilt from the
original 128x128 texture in tower_guard_ref/.

The texture is the vanilla illager layout plus armour nets.  Every box below
was read off the texture by its net: top/bottom strip `d` rows tall at
x = u+d .. u+d+2w, side strip `h` rows tall spanning 2(w+d) pixels.
Boxes whose net does not follow that shape use per-face UV instead.

Output: tower_guard_ref/tower_guard.geo.json, imported into Blockbench
through the MCP and refined there.

This is the one-off starting point only.  tower_guard.bbmodel has since
been edited in Blockbench (body pivot at the hips, the cape as a 12x20x1
slab centred on the back, the animations) and is the source add_tower_guard.py reads;
re-running this script does not reproduce those edits.
"""

import io
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "tower_guard_ref")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    REF, "tower_guard.geo.json")
ATLAS = os.path.join(REF, "tower_guard_atlas.png")

# Bedrock entities take one texture, so the shield (32x32) and spear (25x25)
# go into the empty lower half of the 128x128 body texture.
SHIELD_AT = (0, 72)
SPEAR_AT = (40, 72)


def build_atlas():
    atlas = Image.open(os.path.join(REF, "T_IllagerTowerGuard.png")).convert("RGBA")
    shield = Image.open(os.path.join(REF, "T_TowerGuardShield.png")).convert("RGBA")
    # the shield file has no alpha: pure black is the empty background
    px = shield.load()
    for y in range(shield.height):
        for x in range(shield.width):
            if px[x, y][:3] == (0, 0, 0):
                px[x, y] = (0, 0, 0, 0)
    atlas.alpha_composite(shield, SHIELD_AT)
    atlas.alpha_composite(
        Image.open(os.path.join(REF, "T_TowerGuard_Spear.png")).convert("RGBA"), SPEAR_AT)
    # face after the vanilla vindicator: its angry brows on head-front rows
    # 12..13, and a white/pale-blue swatch for the glowing eyes (row 14)
    brows = {12: ["393939", "393939", "848989", "8e9393", "8e9393", "848989", "393939", "393939"],
             13: ["252525", "393939", "393939", "939999", "939999", "393939", "393939", "252525"]}
    for y, row in brows.items():
        for i, h in enumerate(row):
            atlas.putpixel((8 + i, y), tuple(int(h[k:k + 2], 16) for k in (0, 2, 4)) + (255,))
    atlas.putpixel((6, 6), (255, 255, 255, 255))
    atlas.putpixel((7, 6), (150, 226, 255, 255))
    atlas.save(ATLAS)


def spear_pixels():
    """Opaque spear pixels, and which of them the _S layer marks as glowing."""
    tex = Image.open(os.path.join(REF, "T_TowerGuard_Spear.png")).convert("RGBA").load()
    glow = Image.open(os.path.join(REF, "T_TowerGuard_Spear_S.png")).convert("RGB").load()
    solid, lit = set(), set()
    for y in range(25):
        for x in range(25):
            if tex[x, y][3]:
                solid.add((x, y))
                r, g, b = glow[x, y]
                if r and g:          # yellow in _S: the blade
                    lit.add((x, y))
    return solid, lit


def box(origin, size, uv, inflate=0, mirror=False, rotation=None, pivot=None):
    c = {"origin": origin, "size": size, "uv": uv}
    if inflate:
        c["inflate"] = inflate
    if mirror:
        c["mirror"] = True
    if rotation:
        c["rotation"] = rotation
        c["pivot"] = pivot
    return c


def faces(origin, size, uvmap, inflate=0, rotation=None, pivot=None):
    """Per-face UV: uvmap = {face: (u0, v0, u1, v1)} in texture pixels."""
    uv = {}
    for f, (u0, v0, u1, v1) in uvmap.items():
        uv[f] = {"uv": [u0, v0], "uv_size": [u1 - u0, v1 - v0]}
    return box(origin, size, uv, inflate, rotation=rotation, pivot=pivot)


def sprite_cubes(pixels, at, scale, origin):
    """Extrude sprite pixels like a Java generated item: one cube per
    horizontal run, laid in the YZ plane so the sprite's x runs toward -z
    (forward) and its y runs down.  The flat sides are east/west."""
    ox, oy, oz = origin
    au, av = at
    cubes = []
    for y in range(25):
        x = 0
        while x < 25:
            if (x, y) not in pixels:
                x += 1
                continue
            x0 = x
            while x < 25 and (x, y) in pixels:
                x += 1
            n = x - x0
            u0, v0 = au + x0, av + y
            edge_l = (au + x0, av + y, au + x0 + 1, av + y + 1)
            edge_r = (au + x - 1, av + y, au + x, av + y + 1)
            row = (u0, v0, u0 + n, v0 + 1)
            cubes.append(faces(
                [ox, oy - (y + 1) * scale, oz - x * scale],
                [scale, scale, n * scale],
                {"east": row, "west": (row[2], row[1], row[0], row[3]),
                 "up": edge_l, "down": edge_l,
                 "north": edge_r, "south": edge_l}))
    return cubes


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
SPEAR, SPEAR_LIT = spear_pixels()
SU, SV = SHIELD_AT
S = 1.25                     # spear: model units per sprite pixel


def sh(u0, v0, u1, v1):
    return (SU + u0, SV + v0, SU + u1, SV + v1)


bones = [
    bone("root", [0, 0, 0]),
    bone("body", [0, 24, 0], parent="root", cubes=[
        box([-4, 12, -3], [8, 12, 6], [16, 20]),               # navy tunic
    ]),
    # waist plate: black with grey bars, red band on top; the top face is
    # a black ring, i.e. it is worn around the body
    bone("belt", [0, 24, 0], parent="body", cubes=[
        box([-5, 12, -3], [10, 7, 6], [60, 18], inflate=0.25),
    ]),
    # gold-framed chin guard: front 11x7, red band at the mouth, grey core
    bone("chin_guard", [0, 24, 0], parent="body", cubes=[
        faces([-5.5, 19, -5.5], [11, 7, 3], {
            "north": (63, 42, 74, 49),
            "east": (60, 45, 63, 49), "west": (74, 45, 77, 49),
            "up": (63, 42, 74, 45), "down": (63, 49, 74, 55),
        }),
    ]),
    bone("head", [0, 24, 0], parent="body", cubes=[
        box([-4, 24, -4], [8, 10, 8], [0, 0]),
        box([-1, 23, -6], [2, 4, 2], [24, 0]),
    ]),
    bone("helmet", [0, 24, 0], parent="head", cubes=[
        box([-5, 25, -4.5], [10, 10, 9], [64, 0]),
    ]),
    bone("neck_guard", [0, 28, 4.5], parent="helmet", rotation=[-25, 0, 0], cubes=[
        box([-5, 21, 4.5], [10, 8, 2], [85, 34]),
    ]),
    # in the eye sockets (head front v=14, i.e. y 27..28), white outside and
    # the pale-blue pupil inside like the vindicator's eyes
    bone("eyes_glow", [0, 24, 0], parent="head", cubes=[
        faces([-3, 27, -4.05], [2, 1, 0], {"north": (6, 6, 8, 7)}),
        faces([1, 27, -4.05], [2, 1, 0], {"north": (8, 6, 6, 7)}),
    ]),
    # navy sleeve (44,22) under a dark plate vambrace whose bottom face is
    # the grey hand -- the "without equipment" render shows the same arm
    bone("right_arm", [-5, 22, 0], parent="body", cubes=[
        box([-8, 12, -2], [4, 12, 4], [44, 22]),
        box([-8, 12, -2], [4, 12, 4], [32, 2], inflate=0.5),
    ]),
    bone("right_pauldron", [-5, 22, 0], parent="right_arm", cubes=[
        box([-10, 19, -3], [6, 7, 6], [102, 0], inflate=0.25),
    ]),
    bone("left_arm", [5, 22, 0], parent="body", cubes=[
        box([4, 12, -2], [4, 12, 4], [44, 22], mirror=True),
        box([4, 12, -2], [4, 12, 4], [48, 2], inflate=0.5),
    ]),
    bone("left_pauldron", [5, 22, 0], parent="left_arm", cubes=[
        box([4, 19, -3], [6, 7, 6], [102, 0], inflate=0.25, mirror=True),
    ]),
    # tower shield on the left forearm.  Outer (glyph) face looks north;
    # the 1px orange strip at x=14/29 is its rim.  Texels are scaled 1.1x.
    bone("shield", [6, 13, -4], parent="left_arm", cubes=[
        faces([-1.7, -2, -6], [15.4, 24.2, 1.5], {
            "north": sh(15, 5, 29, 27), "south": sh(0, 5, 14, 27),
            "east": sh(14, 6, 15, 27), "west": sh(29, 6, 30, 27),
            "down": sh(0, 27, 14, 28), "up": sh(15, 5, 29, 6)}),
        faces([0.5, 22.2, -6], [11, 4.4, 1.5], {
            "north": sh(17, 1, 27, 5), "south": sh(3, 3, 11, 5),
            "east": sh(14, 6, 15, 7), "west": sh(29, 6, 30, 7),
            "up": sh(17, 1, 27, 2)}),
    ]),
    # glaive in the right hand: extruded sprite, shaft rotated level so the
    # glowing blade points forward
    # grip = sprite pixel (9,14), a third of the way up from the pommel,
    # sits in the fist at (-6,12,0)
    bone("spear", [-6, 12, 0], parent="right_arm", rotation=[45, 0, 0], cubes=
         sprite_cubes(SPEAR - SPEAR_LIT, SPEAR_AT, S, (-6.6, 12 + 15 * S, 9 * S))),
    bone("spear_glow", [-6, 12, 0], parent="spear", cubes=
         sprite_cubes(SPEAR_LIT, SPEAR_AT, S, (-6.6, 12 + 15 * S, 9 * S))),
    bone("cape", [5, 24, 3], parent="body", rotation=[8, 0, 0], cubes=[
        faces([0, 4, 3.5], [12, 20, 0],
              {"south": (98, 47, 110, 67), "north": (86, 47, 98, 67)}),
    ]),
    # navy leg, riveted greave below the knee (one half of the 8x12x6
    # plate net at 0,38 per leg -- rivet columns at x7 and x12), and a flat
    # knee cop (104,17): grey top, dark rim
    bone("right_leg", [-2, 12, 0], parent="root", cubes=[
        box([-4, 0, -2], [4, 12, 4], [0, 22]),
        faces([-4.5, 0, -2.5], [5, 7, 5], {
            "north": (6, 47, 10, 56), "south": (24, 47, 28, 56),
            "east": (0, 47, 6, 56), "west": (14, 47, 20, 56),
            "down": (14, 38, 18, 44)}),
        box([-5, 7, -3.5], [6, 2, 3], [104, 17]),
    ]),
    bone("left_leg", [2, 12, 0], parent="root", cubes=[
        box([0, 0, -2], [4, 12, 4], [0, 22], mirror=True),
        faces([-0.5, 0, -2.5], [5, 7, 5], {
            "north": (10, 47, 14, 56), "south": (20, 47, 24, 56),
            "east": (0, 47, 6, 56), "west": (14, 47, 20, 56),
            "down": (14, 38, 18, 44)}),
        box([-1, 7, -3.5], [6, 2, 3], [104, 17], mirror=True),
    ]),
]

geo = {
    "format_version": "1.12.0",
    "minecraft:geometry": [{
        "description": {
            "identifier": "geometry.tower_guard",
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
