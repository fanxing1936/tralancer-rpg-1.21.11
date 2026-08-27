# -*- coding: utf-8 -*-
"""Build the raised demon-prompt font used by the two-layer Actionbar.

Normal builds only validate and copy the retained authored atlas, so they need
no imaging dependency.  ``--bake`` is the deliberate art-authoring path; it
uses Pillow and the bundled Windows CJK font to regenerate that atlas and its
width manifest when prompt copy changes.
"""

import io
import json
import os
import shutil
import struct
import sys
import zlib

import add_pact


HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "combat_prompt_art")
SOURCE_PNG = os.path.join(ART, "combat_prompt.png")
MANIFEST = os.path.join(ART, "manifest.json")
CELL_W = 384
GLYPH_W = 192
FONT_SIZE = 11
ALPHA_CUTOFF = 96
# Leave a visible gap above vanilla's baseline.  The old 20/19 layout merely
# touched the normal line and looked like one crowded row in the real HUD.
CELL_H = 28
# Vanilla 1.21.11's bundled Unifont PUA owns E000..E6xx and can win the
# fallback race even when a resource-pack provider exists.  F000/F1xx/F2xx
# are verified absent from unifont_pua-17.0.01 and from this pack.
TOP0 = 0xF000
BACK0 = 0xF100
FORWARD0 = 0xF200
RIGHT0 = 0xF040
STATUS0 = 0xF300
STATUS_BACK = 0xF310
STATUS_W = 64
STATUS_ADVANCE = STATUS_W + 1


# Tiny authored 5x7 capitals for the four persistent relic-stage sprites.
# Keeping these patterns in the generator makes the normal build deterministic
# and dependency-free; --bake and normal build use the exact same pixels.
PIXEL_FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01111"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
}


def _png_rgba(width, height, pixels):
    """Return a minimal non-interlaced RGBA PNG using only stdlib."""
    raw = b"".join(b"\0" + bytes(pixels[y * width * 4:(y + 1) * width * 4])
                   for y in range(height))

    def chunk(kind, payload):
        return (struct.pack(">I", len(payload)) + kind + payload +
                struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))

    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def build_status_atlas(rp):
    """Bake four fixed relic-stage images into the raised actionbar font."""
    labels = ("SLEEP", "AGIT", "DANGER", "CRIT")
    colours = ((118, 118, 128, 255), (213, 150, 242, 255),
               (255, 216, 90, 255), (255, 51, 0, 255))
    height = CELL_H * len(labels)
    pixels = bytearray(STATUS_W * height * 4)

    def dot(x, y, colour):
        if 0 <= x < STATUS_W and 0 <= y < height:
            pos = (y * STATUS_W + x) * 4
            pixels[pos:pos + 4] = bytes(colour)

    for row_index, (label, colour) in enumerate(zip(labels, colours)):
        y0 = row_index * CELL_H + 4
        # Four distinct fixed emblems: sleep dash, agitation wave, danger
        # chevron and critical double bar. The adjacent label is part of the
        # same baked glyph, not dynamic actionbar text.
        for x in range(2, 13):
            if row_index == 0 and x not in (6, 7):
                dot(x, y0 + 8, colour)
            elif row_index == 1:
                dot(x, y0 + 6 + (x % 3), colour)
            elif row_index == 2:
                dot(x, y0 + abs(7 - x), colour)
            elif row_index == 3 and x in (5, 6, 9, 10):
                for yy in range(1, 9):
                    dot(x, y0 + yy, colour)
        x0 = 17
        for letter in label:
            glyph = PIXEL_FONT[letter]
            for yy, bits in enumerate(glyph):
                for xx, bit in enumerate(bits):
                    if bit == "1":
                        dot(x0 + xx, y0 + 2 + yy, colour)
            x0 += 6
        # Pin every row to one measured advance while remaining visually clear.
        dot(STATUS_W - 1, y0 + 11, (colour[0], colour[1], colour[2], 1))

    texture = os.path.join(rp, "assets/rpg/textures/font/seal_status.png")
    parent = os.path.dirname(texture)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    with open(texture, "wb") as f:
        f.write(_png_rgba(STATUS_W, height, pixels))
    return {"type": "bitmap", "file": "rpg:font/seal_status.png",
            "height": CELL_H, "ascent": CELL_H - 1,
            "chars": [chr(STATUS0 + i) for i in range(len(labels))]}


def notices():
    out = []
    for q in add_pact.combat_notices():
        head, middle, tail = add_pact.notice_text(q)
        out.append({"text": head + middle + tail,
                    "parts": [(head, q["ui"]["main"], True),
                              (middle, q["ui"]["soft"], False),
                              (tail, q["ui"]["glint"], q["ultimate"])]})
    return out


def bake():
    from PIL import Image, ImageDraw, ImageFont

    font_regular = r"C:/Windows/Fonts/msyh.ttc"
    font_bold = r"C:/Windows/Fonts/msyhbd.ttc"
    if not os.path.isfile(font_regular) or not os.path.isfile(font_bold):
        raise RuntimeError("Microsoft YaHei fonts are required to bake prompt art")
    # A slightly smaller all-bold face reads closer to vanilla's compact HUD
    # than the former 12 px regular/bold mix.  Binary alpha below removes the
    # grey antialias fringe that became muddy at GUI scale 2/3.
    regular = ImageFont.truetype(font_bold, FONT_SIZE)
    bold = ImageFont.truetype(font_bold, FONT_SIZE)
    rows = notices()
    image = Image.new("RGBA", (CELL_W, CELL_H * len(rows)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    widths = []
    parts = []
    for i, q in enumerate(rows):
        x, y = 0, i * CELL_H
        # Keep four transparent pixels below the authored 20 px band.  With
        # ascent 27 this raises the visible prompt by four real screen pixels
        # instead of cancelling the extra cell height with bottom padding.
        paint_y = y + 4
        for text, colour, is_bold in q["parts"]:
            # YaHei lacks these decorative marks. Draw them ourselves so the
            # prompt never ends in Minecraft's missing-glyph square.
            mark = text[-1] if text and text[-1] in {"◆", "✦"} else ""
            if mark:
                text = text[:-1]
            font = bold if is_bold else regular
            # YaHei's bbox starts a few pixels below the logical origin.  Move
            # it back up so the compact glyphs sit wholly in the raised band.
            if text:
                box = draw.textbbox((0, 0), text, font=font)
                draw.text((x, paint_y - box[1]), text, font=font, fill=colour)
                x += int(round(draw.textlength(text, font=font)))
            if mark == "◆":
                draw.polygon([(x + 4, paint_y + 2), (x + 7, paint_y + 5),
                              (x + 4, paint_y + 8), (x + 1, paint_y + 5)], fill=colour)
                x += 9
            elif mark == "✦":
                draw.polygon([(x + 4, paint_y + 1), (x + 5, paint_y + 4),
                              (x + 8, paint_y + 5), (x + 5, paint_y + 6),
                              (x + 4, paint_y + 9), (x + 3, paint_y + 6),
                              (x, paint_y + 5), (x + 3, paint_y + 4)], fill=colour)
                x += 10
        crop = image.crop((0, y, CELL_W, y + CELL_H))
        alpha = crop.getchannel("A").point(
            lambda value: 255 if value >= ALPHA_CUTOFF else 0)
        crop.putalpha(alpha)
        image.paste(crop, (0, y))
        bbox = crop.getbbox()
        if not bbox:
            raise AssertionError("empty prompt row %d" % (i + 1))
        # Keep every baked glyph below the client's glyph-page limit.  Long
        # notices become two adjacent 192 px glyphs; short right cells are
        # represented later by a zero-width space glyph.
        left = crop.crop((0, 0, GLYPH_W, CELL_H)).getbbox()
        right = crop.crop((GLYPH_W, 0, CELL_W, CELL_H)).getbbox()
        if not left:
            raise AssertionError("empty prompt left half %d" % (i + 1))
        n = 2 if right else 1
        advance = left[2] + 1
        if right:
            advance += right[2] + 1
        widths.append(advance)
        parts.append(n)
    if not os.path.isdir(ART):
        os.makedirs(ART)
    image.save(SOURCE_PNG, optimize=True)
    doc = {"cell_width": CELL_W, "cell_height": CELL_H,
           "notices": [q["text"] for q in rows], "advances": widths,
           "parts": parts}
    with io.open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("combat prompt art baked: %d rows, max advance %d" %
          (len(rows), max(widths)))


def write_json(path, doc):
    parent = os.path.dirname(path)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=True, indent=2)
        f.write("\n")


def build(rp):
    if not os.path.isfile(SOURCE_PNG) or not os.path.isfile(MANIFEST):
        raise RuntimeError("missing retained combat prompt art; run --bake once")
    manifest = json.load(io.open(MANIFEST, encoding="utf-8"))
    if (manifest.get("cell_width") != CELL_W or
            manifest.get("cell_height") != CELL_H):
        raise RuntimeError("combat prompt cell geometry changed; rebake retained atlas")
    current = [q["text"] for q in notices()]
    if manifest.get("notices") != current:
        raise RuntimeError("combat prompt copy changed; rebake retained atlas")
    advances = manifest.get("advances", [])
    parts = manifest.get("parts", [])
    if (len(advances) != len(current) or any(n <= 0 for n in advances) or
            len(parts) != len(current) or any(n not in (1, 2) for n in parts)):
        raise RuntimeError("invalid combat prompt advance manifest")

    texture = os.path.join(rp, "assets/rpg/textures/font/combat_prompt.png")
    parent = os.path.dirname(texture)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    shutil.copyfile(SOURCE_PNG, texture)

    chars = [chr(TOP0 + i) + (chr(RIGHT0 + i) if parts[i] == 2 else "\0")
             for i in range(len(current))]
    prompt_provider = {"type": "bitmap", "file": "rpg:font/combat_prompt.png",
                       "height": CELL_H, "ascent": CELL_H - 1,
                       "chars": chars}
    spaces = {}
    for i, width in enumerate(advances):
        spaces[chr(BACK0 + i)] = -int(width)
        spaces[chr(FORWARD0 + i)] = int(width)
        if parts[i] == 1:
            spaces[chr(RIGHT0 + i)] = 0
    space_provider = {"type": "space", "advances": spaces}
    status_provider = build_status_atlas(rp)
    spaces[chr(STATUS_BACK)] = -STATUS_ADVANCE

    # Remove older injected providers from minecraft:default.  Its merged
    # 1.21.11 fallback chain may resolve Unifont/missing glyphs first.
    default_path = os.path.join(rp, "assets/minecraft/font/default.json")
    default = json.load(io.open(default_path, encoding="utf-8"))
    kept = []
    for provider in default.get("providers", []):
        if provider.get("file") == "rpg:font/combat_prompt.png":
            continue
        advances0 = provider.get("advances", {})
        if any((BACK0 <= ord(k) < BACK0 + len(chars) or
                FORWARD0 <= ord(k) < FORWARD0 + len(chars) or
                0xE500 <= ord(k) < 0xE500 + len(chars) or
                0xE600 <= ord(k) < 0xE600 + len(chars))
               for k in advances0):
            continue
        kept.append(provider)
    default["providers"] = kept
    write_json(default_path, default)

    # Bitmap and cursor movement share one explicit font, avoiding both the
    # default-font merge and cross-font fallback.
    write_json(os.path.join(rp, "assets/rpg/font/combat_prompt.json"),
               {"providers": [prompt_provider, status_provider, space_provider]})

    for rel in ("assets/rpg/font/hud_space.json",):
        obsolete = os.path.join(rp, rel)
        if os.path.isfile(obsolete):
            os.remove(obsolete)
    print("combat prompt font: %d raised dedicated glyphs, two-layer spacing wired" % len(chars))


def main():
    args = [a for a in sys.argv[1:] if a != "--bake"]
    if "--bake" in sys.argv:
        bake()
    rp = args[0] if args else "../resourcepack"
    build(rp)


if __name__ == "__main__":
    main()
