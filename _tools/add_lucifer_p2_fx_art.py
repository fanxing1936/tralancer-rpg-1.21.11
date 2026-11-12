# -*- coding: utf-8 -*-
"""路西法二阶段「知善恶树」的特效贴图、模型和字形（docs/LUCIFER-P2-DESIGN.md §5）。

    python add_lucifer_p2_fx_art.py ../resourcepack

母图在 lucifer_p2_fx_ref/raw/ 与 anim/，由 Codex 按 ART-BRIEF.md 绘制；
这里只定网格和色板。载体的选择与教皇战相同（add_pope_fx_art.py 的说明）：
发光体是 text_display 位图字形（不受光照），地面贴花与实物是 item_display。
"""

import os
import sys

import numpy as np
from PIL import Image

import rpg_ui_style as ui
from add_pope_fx_art import cut, decal_elements, dump, fit, fit_frames, line_elements, save, snap, trimmed

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "lucifer_p2_fx_ref")
RAW = os.path.join(REF, "raw")
ANIM = os.path.join(REF, "anim")

NS = "lucifer_fx"
FONT = "rpg:" + NS


def rgb(hexcolour):
    h = ui.hex_of(hexcolour).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


P = ui.pillar(1)
GREEN = [(255, 255, 255), (200, 245, 214), rgb(P["lit"]), rgb(ui.pillar_mid(1)), rgb(P["deep"])]

# 字形：名称 -> (首个码位, 宽, 高, 序列帧, 帧数, 竖排, 处理)
GLYPHS = {
    "fruit": (0xE100, 16, 16, "fruit_sheet", 4, False, "apple"),
    "juice": (0xE110, 16, 16, "juice_sheet", 6, False, "apple"),
    "burst": (0xE120, 32, 32, "burst_sheet", 8, False, "green"),
    "eye": (0xE130, 32, 32, "eye_sheet", 6, False, "solid"),
    "pollen": (0xE140, 16, 16, "pollen_sheet", 6, False, "solid"),
    # 一阶段（ART-BRIEF-P1.md）
    "glint": (0xE150, 16, 16, "glint_sheet", 4, False, "green"),
    "spear_beam": (0xE160, 32, 32, "spear_beam_sheet", 6, False, "green"),
    "crown": (0xE170, 32, 32, "crown_sheet", 4, False, "solid"),
    "slash": (0xE180, 32, 32, "slash_sheet", 6, False, "green"),
}
# 地面贴花：名称 -> (网格, 处理)。用户 2026-11-08：贴图只用 16×16 或 32×32。
DECALS = {
    "root_sigil": (32, "solid"), "eden_sigil": (32, "solid"), "vine_mark": (16, "green"),
    "fall_mark": (32, "green"), "crack": (32, "solid"), "shock_ring": (32, "green"),
    "serpent_trail": (32, "solid"), "thrust_mark": (32, "green"), "crown_ring": (32, "solid"),
    "serpent_crown": (32, "solid"),
}
FAINT = {"eden_sigil": ("eden_faint", 0.55)}
STRETCHED = {"serpent_trail", "thrust_mark"}    # 会被拉成长条：铺满整格，长轴从头到尾
OBJECTS = {"shard_scale": 16, "shard_leaf": 16, "shard_bark": 16, "feather": 16}
LURE_FRAMES = 6


EVEN = {"glint"}     # 首帧几乎透明，按空隙切会漏帧：按画布等分


def cut_even(path, count):
    im = Image.open(path).convert("RGBA")
    step = im.width / float(count)
    out = []
    for i in range(count):
        piece = im.crop((int(i * step), 0, int((i + 1) * step), im.height))
        box = piece.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
        out.append(piece.crop(box) if box else Image.new("RGBA", (1, 1), (0, 0, 0, 0)))
    return out


def glyph_code(name, frame=0):
    return GLYPHS[name][0] + frame


def glyph_text(name, frame=0):
    return chr(glyph_code(name, frame))


# 简报（ART-BRIEF.md）里的色板。按最近色取，不做全图缩色：
# 缩色会把果实、花苞这类小面积的点缀色并进大色块里。
PALETTE = [(255, 255, 255), (200, 245, 214), rgb(P["lit"]), rgb(ui.pillar_mid(1)), rgb(P["deep"]),
           (255, 60, 240), (154, 28, 142), (90, 58, 34), (58, 36, 20), (42, 26, 16), (168, 85, 247)]
APPLE = [(217, 48, 43), (122, 20, 20)]      # 只给禁果和果汁：别处的深褐会被误配成红


def paletted(im, apple=False):
    a = np.asarray(im.convert("RGBA"), dtype=np.int32)
    tones = np.array(PALETTE + (APPLE if apple else []), dtype=np.int32)
    d = ((a[..., None, :3] - tones) ** 2).sum(axis=-1)
    out = np.zeros(a.shape, np.uint8)
    out[..., :3] = tones[np.argmin(d, axis=-1)]
    out[..., 3] = np.where(a[..., 3] > 110, 255, 0)
    out[out[..., 3] == 0] = 0
    return Image.fromarray(out, "RGBA")


def treat(im, how):
    return snap(im, GREEN) if how == "green" else paletted(im, how == "apple")


def item_def(rp, name):
    dump(os.path.join(rp, "items", NS, name + ".json"), {"model": {
        "type": "minecraft:model", "model": "rpg:%s/%s" % (NS, name),
        "tints": [{"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]}})


def model(rp, name, texture, elements):
    tex = "rpg:item/%s/%s" % (NS, texture)
    dump(os.path.join(rp, "models", NS, name + ".json"),
         {"textures": {"0": tex, "particle": tex}, "elements": elements})
    item_def(rp, name)


def spike_elements():
    """两片交叉的竖直方形平面（像原版植物），底部在模型 y=0，边长 32。"""
    face = {"uv": [0, 0, 16, 16], "texture": "#0"}
    out = []
    for angle in (45, -45):
        out.append({"from": [-8, 0, 8], "to": [24, 32, 8],
                    "rotation": {"origin": [8, 0, 8], "axis": "y", "angle": angle},
                    "faces": {"north": dict(face), "south": dict(face)}})
    return out


def main():
    pack = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    rp = os.path.join(pack, "assets", "rpg")
    tex = os.path.join(rp, "textures", "item", NS)

    providers = []
    for name, (code, w, h, sheet, count, stacked, how) in GLYPHS.items():
        sheet_path = os.path.join(ANIM, sheet + ".png")
        frames = cut_even(sheet_path, count) if name in EVEN else cut(sheet_path, count, stacked)
        pieces = fit_frames(frames, w, h, False)
        for i, piece in enumerate(pieces):
            stem = "%s_%d" % (name, i)
            save(treat(piece, how), os.path.join(rp, "textures", "font", NS, stem + ".png"))
            providers.append({"type": "bitmap", "file": "rpg:font/%s/%s.png" % (NS, stem),
                              "height": h, "ascent": h // 2 - 3, "chars": [chr(code + i)]})
    dump(os.path.join(rp, "font", NS + ".json"), {"providers": providers})

    for name, (size, how) in DECALS.items():
        drawn = fit(trimmed(os.path.join(RAW, name + ".png")), size, size, name in STRETCHED)
        save(treat(drawn, how), os.path.join(tex, name + ".png"))
        model(rp, name, name, decal_elements())
    for name, (faint, alpha) in FAINT.items():
        a = np.array(Image.open(os.path.join(tex, name + ".png")).convert("RGBA"))
        a[..., 3] = (a[..., 3] * alpha).astype(np.uint8)
        save(Image.fromarray(a, "RGBA"), os.path.join(tex, faint + ".png"))
        model(rp, faint, faint, decal_elements())

    for name, size in OBJECTS.items():
        save(paletted(fit(trimmed(os.path.join(RAW, name + ".png")), size, size, False)), os.path.join(tex, name + ".png"))
        dump(os.path.join(rp, "models", NS, name + ".json"),
             {"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/%s/%s" % (NS, name)}})
        item_def(rp, name)

    spike = paletted(fit(trimmed(os.path.join(RAW, "root_spike.png")), 32, 32, False))
    save(spike, os.path.join(tex, "root_spike.png"))
    model(rp, "root_spike", "root_spike", spike_elements())

    # 诱惑之线：横条序列帧竖叠成 .mcmeta 动画，贴在一根细长方块的四个长面上。
    # 线很细，所以每帧直接拉满整格：任何一面看到的都是流动的光带。
    frames = fit_frames(cut(os.path.join(ANIM, "lure_sheet.png"), LURE_FRAMES, True), 32, 32, True)
    strip = Image.new("RGBA", (32, 32 * LURE_FRAMES))
    for i, piece in enumerate(frames):
        strip.paste(paletted(piece), (0, 32 * i))
    save(strip, os.path.join(tex, "lure.png"))
    dump(os.path.join(tex, "lure.png.mcmeta"), {"animation": {"frametime": 2}})
    model(rp, "lure", "lure", line_elements())
    print("lucifer p2 fx: %d glyphs, %d models" % (len(providers), len(DECALS) + len(FAINT) + len(OBJECTS) + 2))


if __name__ == "__main__":
    main()
