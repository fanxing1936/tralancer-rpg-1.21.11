"""Hand-author Feather of Michael on a native 16x16 grid; Pillow is required.

Run ``python draw.py`` to rebuild feather.png and the 8x dual-background preview.
The concept image is a visual reference only: no source image is read or resized.
"""
from collections import Counter
import json
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
SIZE = 16
SCALE = 8
BACKGROUNDS = ("#2A1A14", "#E8D9B0")

# One symbol = one native pixel. No gradients, filters, or sampled colors.
PALETTE = {
    ".": (0, 0, 0, 0),
    "x": (58, 26, 14, 255),  # #3A1A0E
    "a": (168, 64, 28, 255),  # #A8401C
    "g": (255, 216, 90, 255),  # #FFD85A
    "w": (255, 242, 200, 255),  # #FFF2C8
    "p": (255, 208, 189, 255),  # #FFD0BD
    "c": (255, 128, 95, 255),  # #FF805F
    "r": (255, 51, 0, 255),  # #FF3300
    "l": (255, 253, 244, 255),  # #FFFDF4
}

# New drawing from an empty 16x16 grid; not a reduction of the old 32x32 art.
# Broad upper-left vane, smaller lower-right barbs, and a short exposed quill.
PIXELS = (
    "................",
    "..............l.",
    "...........xwll.",
    ".........xpwwgx.",
    ".......xrpwwgpx.",
    "......xppwwgpx..",
    ".......xwwgpx...",
    "....xppwwggpcx..",
    "....xpwwgappx...",
    "...xcwwgapx.....",
    "...xwwgapprx....",
    "..xpwgappx......",
    ".xpwgapx........",
    "..xgax..........",
    ".xgx............",
    "................",
)


def draw_feather():
    if len(PIXELS) != SIZE or any(len(row) != SIZE for row in PIXELS):
        raise ValueError("Expected a 16 by 16 pixel matrix")
    if set("".join(PIXELS)) - PALETTE.keys():
        raise ValueError("Unknown palette symbol")
    icon = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    for y, row in enumerate(PIXELS):
        for x, symbol in enumerate(row):
            if symbol != ".":
                icon.putpixel((x, y), PALETTE[symbol])
    return icon


def draw_preview(icon):
    side = SIZE * SCALE
    enlarged = icon.resize((side, side), Image.Resampling.NEAREST)
    preview = Image.new("RGB", (side * len(BACKGROUNDS), side))
    for index, color in enumerate(BACKGROUNDS):
        x = index * side
        preview.paste(color, (x, 0, x + side, side))
        preview.paste(enlarged, (x, 0), enlarged.getchannel("A"))
    return preview


def validate(icon, preview):
    """Check the delivery constraints against the saved PNGs."""
    assert icon.mode == "RGBA" and icon.size == (SIZE, SIZE)
    alpha = set(icon.getchannel("A").get_flattened_data())
    assert alpha == {0, 255}, alpha
    assert preview.mode == "RGB" and preview.size == (256, 128)
    assert icon.getchannel("A").getbbox() == (1, 1, 15, 15)
    for y, row in enumerate(PIXELS):
        for x, symbol in enumerate(row):
            rgba = icon.getpixel((x, y))
            assert rgba == PALETTE[symbol]
            for side, background in enumerate(BACKGROUNDS):
                bg = tuple(bytes.fromhex(background[1:]))
                expected = rgba[:3] if rgba[3] else bg
                px, py = side * SIZE * SCALE + x * SCALE, y * SCALE
                block = preview.crop((px, py, px + SCALE, py + SCALE))
                assert block.getcolors() == [(SCALE * SCALE, expected)]
    counts = Counter("".join(PIXELS))
    return {
        "size": list(icon.size),
        "alpha": sorted(alpha),
        "bbox_exclusive": list(icon.getchannel("A").getbbox()),
        "visible_pixels": SIZE * SIZE - counts["."],
        "visible_colors": len(counts) - 1,
        "symbol_counts": dict(sorted(counts.items())),
        "preview_size": list(preview.size),
        "nearest_neighbor_blocks_verified": 2 * SIZE * SIZE,
    }


if __name__ == "__main__":
    feather = draw_feather()
    feather.save(HERE / "feather.png")
    draw_preview(feather).save(HERE / "preview.png")
    with Image.open(HERE / "feather.png") as saved_icon:
        with Image.open(HERE / "preview.png") as saved_preview:
            print(json.dumps(validate(saved_icon, saved_preview), indent=2))
