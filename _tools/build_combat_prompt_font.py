# -*- coding: utf-8 -*-
"""Build the raised demon-prompt font used by the two-layer Actionbar.

Normal builds only validate and copy the retained atlases, so they need no
imaging dependency.  ``--bake`` is the deliberate art-authoring path; it uses
Pillow and the vanilla client's own GNU Unifont to regenerate the atlases and
their width manifest when prompt copy changes.

Why Unifont (ART-STYLE.md §5): the lower Actionbar row is vanilla text, which
draws CJK from Unifont at 2 texels per GUI unit.  The raised row used to be a
TrueType face thresholded at 11 px and 1 texel per unit -- strokes merged into
blocks and the two rows read as two different UIs.  Baking the very same
Unifont glyphs at the same density makes the raised row indistinguishable in
letterform from the row under it.  It also stops shipping a rasterised
Microsoft YaHei inside an open-source pack; Unifont is GPLv2+ (with the font
embedding exception) / SIL OFL 1.1, credited in README.
"""

import io
import json
import os
import shutil
import sys
import zipfile

import add_pact
import rpg_ui_style as ui


HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "combat_prompt_art")
SOURCE_PNG = os.path.join(ART, "combat_prompt.png")
STATUS_PNG = os.path.join(ART, "seal_status.png")
MANIFEST = os.path.join(ART, "manifest.json")

# Texels per GUI unit.  Unifont glyphs are 16 texels tall and vanilla draws
# them 8 units tall, so 2 keeps the raised row on vanilla's own pixel grid.
SCALE = 2
CELL_H = 28                      # GUI units; ascent 27 keeps the raised band
CELL_TEX_H = CELL_H * SCALE
GLYPH_W = 192                    # texels; stays inside the 256 px glyph page
PARTS = 4                        # glyph slices per notice
CELL_W = GLYPH_W * PARTS
# Text bottom sits on the same line the former 11 px atlas used (unit 15).
PAINT_Y = 7 * SCALE

# Vanilla 1.21.11's bundled Unifont PUA owns E000..E6xx and can win the
# fallback race even when a resource-pack provider exists.  F0xx/F1xx/F2xx/F3xx
# are verified absent from unifont_pua-17.0.01 and from this pack.
TOP0 = 0xF000                    # slice 0; slices 1..3 follow at +0x40
SLICE0 = (0xF000, 0xF040, 0xF080, 0xF0C0)
BACK0 = 0xF100
FORWARD0 = 0xF200
RIGHT0 = SLICE0[1]
STATUS0 = 0xF300
STATUS_BACK = 0xF310
STATUS_W = 64 * SCALE            # texels
STATUS_ADVANCE = STATUS_W // SCALE + 1

# The four relic stages: label and colour (lower HUD row uses the same words).
STAGES = (("沉眠", "#76767F"), ("躁动", ui.RITUAL),
          ("危险", ui.HOLY), ("临界", ui.WARN))


# ---------------------------------------------------------------------------
# Unifont
# ---------------------------------------------------------------------------
def unifont_hex():
    """The vanilla client's own Unifont, read from the local assets store."""
    from mc_env import GAME
    idx_dir = os.path.join(GAME, "assets", "indexes")
    for name in sorted(os.listdir(idx_dir), reverse=True):
        doc = json.load(io.open(os.path.join(idx_dir, name), encoding="utf-8"))
        obj = doc.get("objects", {}).get("minecraft/font/unifont.zip")
        if not obj:
            continue
        h = obj["hash"]
        path = os.path.join(GAME, "assets", "objects", h[:2], h)
        with zipfile.ZipFile(path) as z:
            hex_name = next(n for n in z.namelist() if n.endswith(".hex"))
            glyphs = {}
            for line in z.read(hex_name).decode("ascii").splitlines():
                cp, _, bits = line.partition(":")
                glyphs[int(cp, 16)] = bits
            return glyphs
    raise RuntimeError("vanilla unifont.zip not found under %s" % idx_dir)


def glyph_rows(glyphs, ch):
    """(rows, left, right) -- rows are 16 ints, left/right the inked columns."""
    bits = glyphs.get(ord(ch))
    if bits is None:
        raise RuntimeError("Unifont has no glyph for %r" % ch)
    width = len(bits) // 4           # 8 or 16 columns
    rows = [int(bits[i * width // 4:(i + 1) * width // 4], 16) for i in range(16)]
    cols = [x for x in range(width) if any(r >> (width - 1 - x) & 1 for r in rows)]
    if not cols:
        return rows, width, None, None
    return rows, width, cols[0], cols[-1]


def draw_text(image, glyphs, x, y, text, colour, bold=False):
    """Draw like vanilla's unihex provider; return the new pen x (texels)."""
    fill = tuple(int(c * 255) for c in ui.rgb(colour)) + (255,)
    for ch in text:
        if ch == " ":
            x += 4 * SCALE
            continue
        rows, width, left, right = glyph_rows(glyphs, ch)
        if left is None:                   # ideographic space and friends
            x += width // 2 * SCALE
            continue
        for yy, row in enumerate(rows):
            for xx in range(left, right + 1):
                if row >> (width - 1 - xx) & 1:
                    for b in ((0, 1) if bold else (0,)):
                        image.putpixel((x + xx - left + b, y + yy), fill)
        # vanilla: glyph width + 1 unit gap; bold adds half a unit (1 texel)
        x += (right - left + 1) + SCALE + (1 if bold else 0)
    return x


# ---------------------------------------------------------------------------
# Atlases
# ---------------------------------------------------------------------------
def notices():
    """Three runs per notice: [lord] in the pillar's lit colour, the move in
    white, the closing mark back in the lit colour (ART-STYLE.md §5)."""
    out = []
    for q in add_pact.combat_notices():
        head, middle, tail = add_pact.notice_text(q)
        lit = q["ui"]["main"]
        out.append({"text": head + middle + tail,
                    "parts": [(head, lit, True), (middle, ui.WHITE, q["ultimate"]),
                              (tail, lit, True)]})
    return out


def pin(image, x, y):
    """An alpha-1 texel in a slice's last column.  The client measures a
    bitmap glyph's advance from its rightmost visible column, so without this
    a slice that happens to end in a gap would pull the next slice left.
    Alpha 1 is below the text shader's discard threshold -- never drawn."""
    image.putpixel((x, y), (255, 255, 255, 1))


def bake():
    from PIL import Image

    glyphs = unifont_hex()
    rows = notices()
    image = Image.new("RGBA", (CELL_W, CELL_TEX_H * len(rows)), (0, 0, 0, 0))
    advances, parts = [], []
    for i, q in enumerate(rows):
        y = i * CELL_TEX_H
        x = 0
        for text, colour, bold in q["parts"]:
            x = draw_text(image, glyphs, x, y + PAINT_Y, text, colour, bold)
        bbox = image.crop((0, y, CELL_W, y + CELL_TEX_H)).getbbox()
        if not bbox:
            raise AssertionError("empty prompt row %d" % (i + 1))
        width = bbox[2]
        n = -(-width // GLYPH_W)
        if n > PARTS:
            raise AssertionError("prompt row %d is %d texels, over %d" %
                                 (i + 1, width, CELL_W))
        for k in range(n - 1):
            pin(image, (k + 1) * GLYPH_W - 1, y + CELL_TEX_H - 1)
        last = width - (n - 1) * GLYPH_W
        advances.append((n - 1) * (GLYPH_W // SCALE + 1) +
                        int(0.5 + last / float(SCALE)) + 1)
        parts.append(n)

    status = Image.new("RGBA", (STATUS_W, CELL_TEX_H * len(STAGES)), (0, 0, 0, 0))
    for i, (label, colour) in enumerate(STAGES):
        y = i * CELL_TEX_H + PAINT_Y
        x = draw_text(status, glyphs, 0, y, "封印 ", ui.NAMED["gray"])
        draw_text(status, glyphs, x, y, label, colour, True)
        # Pin every row to one measured advance while remaining invisible.
        pin(status, STATUS_W - 1, i * CELL_TEX_H + CELL_TEX_H - 1)

    if not os.path.isdir(ART):
        os.makedirs(ART)
    image.save(SOURCE_PNG, optimize=True)
    status.save(STATUS_PNG, optimize=True)
    doc = {"cell_width": CELL_W, "cell_height": CELL_TEX_H, "scale": SCALE,
           "notices": [q["text"] for q in rows], "advances": advances,
           "parts": parts}
    with io.open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("combat prompt art baked from Unifont: %d rows, max advance %d" %
          (len(rows), max(advances)))


def write_json(path, doc):
    parent = os.path.dirname(path)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=True, indent=2)
        f.write("\n")


def copy(src, rp, name):
    texture = os.path.join(rp, "assets/rpg/textures/font", name)
    parent = os.path.dirname(texture)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    shutil.copyfile(src, texture)


def build(rp):
    for path in (SOURCE_PNG, STATUS_PNG, MANIFEST):
        if not os.path.isfile(path):
            raise RuntimeError("missing retained combat prompt art; run --bake once")
    manifest = json.load(io.open(MANIFEST, encoding="utf-8"))
    if (manifest.get("cell_width") != CELL_W or
            manifest.get("cell_height") != CELL_TEX_H or
            manifest.get("scale") != SCALE):
        raise RuntimeError("combat prompt cell geometry changed; rebake retained atlas")
    current = [q["text"] for q in notices()]
    if manifest.get("notices") != current:
        raise RuntimeError("combat prompt copy changed; rebake retained atlas")
    advances = manifest.get("advances", [])
    parts = manifest.get("parts", [])
    if (len(advances) != len(current) or any(n <= 0 for n in advances) or
            len(parts) != len(current) or any(n not in range(1, PARTS + 1) for n in parts)):
        raise RuntimeError("invalid combat prompt advance manifest")

    copy(SOURCE_PNG, rp, "combat_prompt.png")
    copy(STATUS_PNG, rp, "seal_status.png")

    count = len(current)
    chars = ["".join(chr(SLICE0[k] + i) if k < parts[i] else "\0"
                     for k in range(PARTS)) for i in range(count)]
    prompt_provider = {"type": "bitmap", "file": "rpg:font/combat_prompt.png",
                       "height": CELL_H, "ascent": CELL_H - 1, "chars": chars}
    status_provider = {"type": "bitmap", "file": "rpg:font/seal_status.png",
                       "height": CELL_H, "ascent": CELL_H - 1,
                       "chars": [chr(STATUS0 + i) for i in range(len(STAGES))]}
    spaces = {}
    for i, width in enumerate(advances):
        spaces[chr(BACK0 + i)] = -int(width)
        spaces[chr(FORWARD0 + i)] = int(width)
        # The data pack always sends all four slices; absent ones are
        # zero-width so a short notice never draws a missing-glyph box.
        for k in range(parts[i], PARTS):
            spaces[chr(SLICE0[k] + i)] = 0
    spaces[chr(STATUS_BACK)] = -STATUS_ADVANCE
    space_provider = {"type": "space", "advances": spaces}

    # Remove older injected providers from minecraft:default.  Its merged
    # 1.21.11 fallback chain may resolve Unifont/missing glyphs first.
    default_path = os.path.join(rp, "assets/minecraft/font/default.json")
    default = json.load(io.open(default_path, encoding="utf-8"))
    kept = []
    for provider in default.get("providers", []):
        if provider.get("file") == "rpg:font/combat_prompt.png":
            continue
        advances0 = provider.get("advances", {})
        if any((BACK0 <= ord(k) < BACK0 + count or
                FORWARD0 <= ord(k) < FORWARD0 + count or
                0xE500 <= ord(k) < 0xE500 + count or
                0xE600 <= ord(k) < 0xE600 + count)
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
    print("combat prompt font: %d raised Unifont notices, two-layer spacing wired" % count)


def main():
    args = [a for a in sys.argv[1:] if a != "--bake"]
    if "--bake" in sys.argv:
        bake()
    rp = args[0] if args else "../resourcepack"
    build(rp)


if __name__ == "__main__":
    main()
