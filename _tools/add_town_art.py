# -*- coding: utf-8 -*-
"""城镇的贴图（Codex 交付，town_ref/art）：物品图标 → rpg:town/<名>；特效序列帧 → 动画贴图 + 物品模型。

python add_town_art.py ../resourcepack
"""
import io
import json
import os
import sys

from PIL import Image

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "town_ref", "art")
ICONS = ["letter", "town_badge", "eden_pass", "home_scroll", "black_candle", "pact_scroll", "map_shard", "wanted", "welfare_pack", "temper_star", "ration",
         "holy_fire", "tab_fuse", "tab_salvage", "ev_granary", "ev_hollow", "ev_witch", "rye_bread", "smoked_meat"]
VANILLA_FALLBACK = {"rye_bread": "minecraft:item/bread", "smoked_meat": "minecraft:item/cooked_beef"}
FX = {"fx_flies": 2, "fx_rev_circle": 3, "fx_fuse_spark": 2, "fx_holy_flame": 2}     # 每帧刻数


def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)


def item(name, im, anim=None):
    tex = os.path.join(RP, "assets", "rpg", "textures", "item", "town", name + ".png")
    os.makedirs(os.path.dirname(tex), exist_ok=True)
    im.save(tex)
    if anim:
        wj(tex + ".mcmeta", {"animation": {"frametime": anim, "interpolate": False}})
    wj(os.path.join(RP, "assets", "rpg", "models", "town", name + ".json"), {"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/town/" + name}})
    wj(os.path.join(RP, "assets", "rpg", "items", "town", name + ".json"), {"model": {"type": "minecraft:model", "model": "rpg:town/" + name}})


def main():
    n = 0
    for name in ICONS:
        p = os.path.join(ART, name + ".png")
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        assert im.size == (16, 16), (name, im.size)
        item(name, im)
        n += 1
    for name, ft in FX.items():
        p = os.path.join(ART, name + ".png")
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        assert im.size[0] == 32 and im.size[1] % 32 == 0, (name, im.size)
        item(name, im, ft)
        n += 1
    # 字形：副本血条、广播前的小图标（和精英词缀图标同一种做法）
    prov = []
    for ch, name in (("\ue7d0", "ev_granary"), ("\ue7d1", "ev_hollow"), ("\ue7d2", "ev_witch"), ("\ue7d3", "holy_fire"), ("\ue7d4", "wanted"), ("\ue7d5", "town_badge")):
        src = os.path.join(ART, name + ".png")
        if not os.path.exists(src):
            continue
        dst = os.path.join(RP, "assets", "rpg", "textures", "font", "town_icons", name + ".png")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        Image.open(src).convert("RGBA").save(dst)
        prov.append({"type": "bitmap", "file": "rpg:font/town_icons/%s.png" % name, "height": 8, "ascent": 7, "chars": [ch]})
    prov.append({"type": "space", "advances": {" ": 4}})          # 图标字体里的空格（没有它会显示成缺字方框）
    wj(os.path.join(RP, "assets", "rpg", "font", "town_icons.json"), {"providers": prov})
    for name, tex in VANILLA_FALLBACK.items():
        if not os.path.exists(os.path.join(ART, name + ".png")):
            wj(os.path.join(RP, "assets", "rpg", "models", "town", name + ".json"), {"parent": "minecraft:item/generated", "textures": {"layer0": tex}})
            wj(os.path.join(RP, "assets", "rpg", "items", "town", name + ".json"), {"model": {"type": "minecraft:model", "model": "rpg:town/" + name}})
    # 信：Codex 没交图之前先借地图碎片
    if not os.path.exists(os.path.join(ART, "letter.png")):
        item("letter", Image.open(os.path.join(ART, "map_shard.png")).convert("RGBA"))
    print("town art: %d 张，%d 个字形" % (n, len(prov)))


if __name__ == "__main__":
    main()
