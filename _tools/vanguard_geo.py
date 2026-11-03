# -*- coding: utf-8 -*-
"""罪仆·先锋 (Vanguard) -- Bedrock geometry after Minecraft Dungeons'
Vanguard, the Nameless One's skeleton guard, rebuilt from the original
textures in vanguard_ref/.

* The skeleton (64x32) keeps the vanilla nets: head 8x8x8 at 0,0, ribcage
  8x12x4 at 16,16, arms and legs 2x12x2 at 40,16 and 0,16.
* The desert armour (64x64) is box UV too: helmet 10x8x10 at 0,0 (open
  bottom, face slot in the lower front rows, cheek guards on the front
  corners), its gold crest 2x8x1 in the helmet net's free corner at 0,0,
  and a 10x12x6 cuirass at 0,18.  The brown loincloth panels (40..56)
  do not form one net and are mapped per face.
* The desert shield (36x36) holds the front and back silhouettes side by
  side; it is built from four slabs, edges from the gold swatch at 0..3,0.
* The glaive (29x30) is an item sprite, extruded like a Java generated item.

The four textures are packed into one 128x128 atlas.  The `_S` layers are
specular, not emissive (the renders show neither eyes nor blade glowing),
so nothing glows.

Output: vanguard_ref/vanguard.geo.json, imported into Blockbench through
the MCP and refined there (poses, animations).  vanguard.bbmodel is the
source add_vanguard.py reads; re-running this script does not reproduce
the edits made in Blockbench.
"""

import io
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "vanguard_ref")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REF, "vanguard.geo.json")
ATLAS = os.path.join(REF, "vanguard_atlas.png")

ARMOR_AT = (64, 0)
SHIELD_AT = (0, 64)
GLAIVE_AT = (40, 64)
GLAIVE_W, GLAIVE_H = 29, 30


def build_atlas():
    atlas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    for name, at in (("MCD_Skeleton_(texture).png", (0, 0)), ("T_DesertArmor.png", ARMOR_AT),
                     ("T_desertShield.png", SHIELD_AT), ("T_Glaive.png", GLAIVE_AT)):
        atlas.alpha_composite(Image.open(os.path.join(REF, name)).convert("RGBA"), at)
    atlas.save(ATLAS)


def glaive_pixels():
    tex = Image.open(os.path.join(REF, "T_Glaive.png")).convert("RGBA").load()
    # row 0, x 0..5 is the texture's palette swatch, not part of the glaive
    return {(x, y) for y in range(GLAIVE_H) for x in range(GLAIVE_W)
            if tex[x, y][3] and not (y == 0 and x < 6)}


def box(origin, size, uv, inflate=0, mirror=False):
    c = {"origin": origin, "size": size, "uv": uv}
    if inflate:
        c["inflate"] = inflate
    if mirror:
        c["mirror"] = True
    return c


def faces(origin, size, uvmap, inflate=0):
    """Per-face UV: uvmap = {face: (u0, v0, u1, v1)} in atlas pixels."""
    uv = {}
    for f, (u0, v0, u1, v1) in uvmap.items():
        uv[f] = {"uv": [u0, v0], "uv_size": [u1 - u0, v1 - v0]}
    return box(origin, size, uv, inflate)


def A(u0, v0, u1, v1):
    return (ARMOR_AT[0] + u0, ARMOR_AT[1] + v0, ARMOR_AT[0] + u1, ARMOR_AT[1] + v1)


def S(u0, v0, u1, v1):
    return (SHIELD_AT[0] + u0, SHIELD_AT[1] + v0, SHIELD_AT[0] + u1, SHIELD_AT[1] + v1)


def sprite_cubes(pixels, at, scale, origin):
    """Extrude sprite pixels like a Java generated item: one cube per
    horizontal run, laid in the YZ plane so the sprite's x runs toward -z
    (forward) and its y runs down.  The flat sides are east/west."""
    ox, oy, oz = origin
    au, av = at
    cubes = []
    for y in range(GLAIVE_H):
        x = 0
        while x < GLAIVE_W:
            if (x, y) not in pixels:
                x += 1
                continue
            x0 = x
            while x < GLAIVE_W and (x, y) in pixels:
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
GOLD = S(2, 0, 3, 1)          # rim colour swatch in the shield texture
SHIELD_X, SHIELD_TOP, SHIELD_Z = 5, 25, (-4.5, 1.5)


def shield_slab(c0, c1, r0, r1):
    """Columns c0..c1, rows r0..r1 of the 16x21 front silhouette (the back
    one sits 16 columns to the right), centred on the left forearm."""
    x0 = SHIELD_X + (8 - c1)
    return faces([x0, SHIELD_TOP - r1, SHIELD_Z[0]], [c1 - c0, r1 - r0, SHIELD_Z[1]], {
        "north": S(c0, r0, c1, r1), "south": S(c1 + 16, r0, c0 + 16, r1),
        "east": GOLD, "west": GOLD, "up": GOLD, "down": GOLD})


# glaive grip: shaft pixel (12,17) in the right fist at (-5, 12, 0)
GRIP = (12, 17)

bones = [
    bone("root", [0, 0, 0]),
    bone("body", [0, 12, 0], parent="root", cubes=[
        box([-4, 12, -2], [8, 12, 4], [16, 16]),
    ]),
    bone("cuirass", [0, 12, 0], parent="body", cubes=[
        box([-5, 12, -3], [10, 12, 6], [ARMOR_AT[0], ARMOR_AT[1] + 18]),
    ]),
    bone("loincloth", [0, 12, 0], parent="body", cubes=[
        faces([-4.5, 4, -2.5], [9, 9, 5], {
            "north": A(47, 5, 56, 14), "south": A(47, 19, 56, 28),
            "east": A(42, 5, 47, 14), "west": A(47, 5, 42, 14)}),
    ]),
    bone("head", [0, 24, 0], parent="body", cubes=[
        box([-4, 24, -4], [8, 8, 8], [0, 0]),
    ]),
    bone("helmet", [0, 24, 0], parent="head", cubes=[
        box([-5, 26, -5], [10, 8, 10], list(ARMOR_AT)),
        box([-1, 27, -5.5], [2, 8, 1], list(ARMOR_AT)),
    ]),
    bone("right_arm", [-5, 22, 0], parent="body", cubes=[
        box([-6, 12, -1], [2, 12, 2], [40, 16]),
    ]),
    bone("left_arm", [5, 22, 0], parent="body", cubes=[
        box([4, 12, -1], [2, 12, 2], [40, 16], mirror=True),
    ]),
    bone("shield", [5, 13, -1], parent="left_arm", cubes=[
        shield_slab(5, 11, 0, 2), shield_slab(2, 14, 2, 6),
        shield_slab(0, 16, 6, 11), shield_slab(3, 13, 11, 21),
    ]),
    bone("glaive", [-5, 12, 0], parent="right_arm", cubes=
         sprite_cubes(glaive_pixels(), GLAIVE_AT, 1.0,
                      (-5.5, 12 + GRIP[1] + 0.5, GRIP[0] + 0.5))),
    bone("right_leg", [-2, 12, 0], parent="root", cubes=[
        box([-3, 0, -1], [2, 12, 2], [0, 16]),
    ]),
    bone("left_leg", [2, 12, 0], parent="root", cubes=[
        box([1, 0, -1], [2, 12, 2], [0, 16], mirror=True),
    ]),
]

geo = {
    "format_version": "1.12.0",
    "minecraft:geometry": [{
        "description": {
            "identifier": "geometry.vanguard",
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
