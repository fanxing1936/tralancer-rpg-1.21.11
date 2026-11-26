# -*- coding: utf-8 -*-
"""达阿特试炼的专属特效贴图：Codex 的序列帧与贴花（daath_ref/{anim,decal}/），切帧、缩到 32×32、吸附到灰银色阶。

    python add_daath_fx_art.py ../resourcepack

产物：字体 rpg:daath_vfx（序列帧，码位固定）、物品模型 rpg:daath_fx/*（地面贴花，朝上的平面，可着色）。
没交付的图：码位照留，daath_lib 会退回现成的替身。用法同 add_michael_fx_art.py（boss_fx.Fx 的 arts）。
"""
import os
import sys

import numpy as np
from PIL import Image

import display_mob as dm
import add_michael_fx_art as M

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "daath_ref")
ANIM = os.path.join(REF, "anim")
DECAL = os.path.join(REF, "decal")
KEY = "daath_vfx"
FONT = "rpg:" + KEY
NS = "rpg:daath_fx"
GLYPH_BASE = 0xE000
STRIDE = 16
RAMP = [tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in ("0B0C10", "1A1D24", "2A2E38", "4A505C", "7C8593", "AAB4C3", "D8DEE8", "FFFFFF", "FFF2A8")]
# 名: (文件, 帧数)
SHEETS = {"d_eye": ("eye_know_sheet", 6), "d_shards": ("shard_burst_sheet", 6), "d_shard": ("shard_single_sheet", 4), "d_ink": ("ink_rise_sheet", 6),
          "d_splash": ("ink_splash_sheet", 6), "d_slash": ("slash_shadow_sheet", 6), "d_axe": ("slash_axe_sheet", 6), "d_thrust": ("thrust_sheet", 6),
          "d_smash": ("smash_sheet", 6), "d_clash": ("clash_sheet", 6), "d_chain": ("chain_sheet", 4), "d_motes": ("soul_motes_sheet", 4), "d_grab": ("grab_sheet", 6)}
DECALS = ("seal_daath", "seal_daath_lit", "seal_question", "crack_mirror", "skin_crack")
_T = None


def have(name):
    f = SHEETS[name][0] if name in SHEETS else None
    return os.path.isfile(os.path.join(ANIM, f + ".png")) if f else os.path.isfile(os.path.join(DECAL, name + ".png"))


def glyph_table():
    global _T
    if _T is None:
        _T = {n: (GLYPH_BASE + i * STRIDE, 32, c) for i, (n, (_f, c)) in enumerate(SHEETS.items())}
    return _T


def glyph_text(name, frame=0):
    return chr(glyph_table()[name][0] + frame)


def palette(im):
    """每个像素吸附到色阶里最近的颜色（大图缩小会混出脏色）。"""
    a = np.array(im.convert("RGBA")).astype(int)
    pal = np.array(RAMP)
    d = ((a[..., None, :3] - pal[None, None]) ** 2).sum(-1)
    a[..., :3] = pal[d.argmin(-1)]
    return Image.fromarray(a.astype(np.uint8))


def frames(name):
    f, n = SHEETS[name]
    return [palette(M.fit(x, 32, cut=96)) for x in M.split_sheet(os.path.join(ANIM, f + ".png"), n)]


def main():
    rp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "resourcepack")
    A = os.path.join(rp, "assets", "rpg")
    fd, td = os.path.join(A, "textures", "font", KEY), os.path.join(A, "textures", "item", "daath_fx")
    os.makedirs(fd, exist_ok=True)
    os.makedirs(td, exist_ok=True)
    prov, miss, n = [], [], 0

    def item(name):
        dm.wj(os.path.join(A, "models", "daath_fx", name + ".json"), M.plane_model("rpg:item/daath_fx/" + name))
        dm.wj(os.path.join(A, "items", "daath_fx", name + ".json"), {"model": {"type": "minecraft:model", "model": "rpg:daath_fx/" + name, "tints": [
            {"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]}})
    for name, (code, size, count) in glyph_table().items():
        if not have(name):
            miss.append(name)
            continue
        fr = frames(name)
        assert len(fr) == count, name
        for i, im in enumerate(fr):
            im.save(os.path.join(fd, "%s_%d.png" % (name, i)))
            prov.append({"type": "bitmap", "file": "rpg:font/%s/%s_%d.png" % (KEY, name, i), "height": 32, "ascent": 13, "chars": [chr(code + i)]})
            if name in ("d_smash",):                # 俯视的一套另做成贴花
                im.save(os.path.join(td, "smash_%d.png" % i))
                item("smash_%d" % i)
        n += 1
    for name in DECALS:
        p = os.path.join(DECAL, name + ".png")
        if not os.path.isfile(p):
            miss.append(name)
            continue
        im = palette(M.fit(M.square(Image.open(p).convert("RGBA"), 4), 32, cut=60 if "crack" in name else 96))
        im.save(os.path.join(td, name + ".png"))
        item(name)
        n += 1
    prov.append({"type": "space", "advances": {"": -1}})
    dm.wj(os.path.join(A, "font", KEY + ".json"), {"providers": prov})
    print("daath fx art: %d sets%s" % (n, " (missing: %s)" % ", ".join(miss) if miss else ""))


if __name__ == "__main__":
    main()
