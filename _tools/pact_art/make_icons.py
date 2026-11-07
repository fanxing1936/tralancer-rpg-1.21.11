# -*- coding: utf-8 -*-
"""Install the finished 16x16 icons from pixel16/ (ART-STYLE.md §4).

`snap` cut the first drafts from the Codex sheets in raw16/.

One-off: the results are committed beside this script and copied by the build.
Each target cell takes the most common colour under it rather than an average,
so one-pixel lines and outlines stay hard.  Seals are drawn in grey and take
each pillar's colours here.
"""

import os
import sys
from collections import Counter

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import rpg_ui_style as ui  # noqa: E402

GRID = 16
FIT = 15                 # long side: 94% of the canvas, the top of the §4 range
MAX_COLOURS = 32
PILLARS = ["lucifer", "leviathan", "abaddon", "beelzebub", "samael", "belial", "mammon"]


def split(name, count):
    sheet = Image.open(os.path.join(HERE, "raw16", name + ".png")).convert("RGBA")
    width = sheet.width // count
    out = []
    for i in range(count):
        cell = sheet.crop((i * width, 0, (i + 1) * width, sheet.height))
        out.append(cell.crop(cell.getchannel("A").point(lambda v: 255 if v > 128 else 0).getbbox()))
    return out


def snap(icon):
    """Fit into the grid with hard alpha, taking each cell's dominant colour."""
    scale = min(FIT / icon.width, FIT / icon.height)
    w, h = max(1, round(icon.width * scale)), max(1, round(icon.height * scale))
    src = icon.load()
    canvas = Image.new("RGBA", (GRID, GRID), (0, 0, 0, 0))
    ox, oy = (GRID - w) // 2, (GRID - h) // 2
    for y in range(h):
        for x in range(w):
            x0, x1 = x * icon.width // w, max((x + 1) * icon.width // w, x * icon.width // w + 1)
            y0, y1 = y * icon.height // h, max((y + 1) * icon.height // h, y * icon.height // h + 1)
            seen = Counter()
            clear = 0
            for py in range(y0, y1):
                for px in range(x0, x1):
                    r, g, b, a = src[px, py]
                    if a < 128:
                        clear += 1
                    else:
                        seen[(r // 8 * 8 + 4, g // 8 * 8 + 4, b // 8 * 8 + 4)] += 1
            if seen and sum(seen.values()) >= clear:
                canvas.putpixel((ox + x, oy + y), seen.most_common(1)[0][0] + (255,))
    return cap(canvas)


def cap(icon):
    alpha = icon.getchannel("A")
    out = icon.convert("RGB").quantize(MAX_COLOURS - 1, dither=Image.Dither.NONE).convert("RGB")
    out.putalpha(alpha)
    clean = Image.new("RGBA", icon.size, (0, 0, 0, 0))
    clean.paste(out, (0, 0), out)
    return clean


def rgb(colour):
    colour = colour.lstrip("#")
    return tuple(int(colour[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def tint(icon, n):
    """Grey to pillar: wax in the dark colour, the carving in the light one."""
    deep, lit = rgb(ui.pillar(n)["deep"]), rgb(ui.pillar(n)["lit"])
    stops = [(0, mix(deep, (0, 0, 0), 0.6)), (74, deep), (128, mix(deep, lit, 0.5)),
             (190, lit), (255, mix(lit, (255, 255, 255), 0.6))]
    out = icon.copy()
    pixels = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = pixels[x, y]
            if not a:
                continue
            v = (r + g + b) // 3
            for (v0, c0), (v1, c1) in zip(stops, stops[1:]):
                if v <= v1:
                    pixels[x, y] = mix(c0, c1, (v - v0) / (v1 - v0)) + (255,)
                    break
    return cap(out)


def main():
    """pixel16/ holds Codex's hand-finished 16x16 art: books and pages copy over."""
    src = os.path.join(HERE, "pixel16")
    for slug in PILLARS:
        for name in ("pact_%s_t2", "pact_%s_t3", "page_%s"):
            icon = Image.open(os.path.join(src, name % slug + ".png")).convert("RGBA")
            assert icon.size == (GRID, GRID), name % slug
            cap(icon).save(os.path.join(HERE, name % slug + ".png"))
    masters = [Image.open(os.path.join(src, "seal_%d.png" % role)).convert("RGBA") for role in range(1, 6)]
    for n, slug in enumerate(PILLARS, 1):
        for role, master in enumerate(masters, 1):
            assert master.size == (GRID, GRID), role
            tint(master, n).save(os.path.join(HERE, "seal_%s_%d.png" % (slug, role)))
    print("pact icons: 14 books, 7 pages, 35 seals at %d grid" % GRID)


if __name__ == "__main__":
    main()
