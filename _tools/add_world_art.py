# -*- coding: utf-8 -*-
"""世界掉落与锻造的新图标（Codex 交付在 world_ref/art，2026-11-23）→ 资源包。

    python add_world_art.py ../resourcepack

* 物品：rpg:world/<名>（item_model），16×16（图纸碎片是地下城原图，32×32 原样）。
  罪印碎片画成浅灰白，物品定义带 custom_model_data 着色，七柱按柱色染。
* 称号图标：字体 rpg:world_titles，每个称号一个私用区字符（TITLE_CHARS），放在名字前面。
"""
import io
import json
import os
import shutil
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "world_ref", "art")
RP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "resourcepack")

ITEMS = ["elite_badge", "sin_shard", "blueprint_epic", "blueprint_legend", "star_fragment", "wind_essence",
         "abyss_tear", "molten_core", "mountain_heart", "temple_bronze", "grave_soil"]
TINTED = {"sin_shard"}
TITLES = ["gate", "ledger", "waverer", "grandmaster", "meteor", "merchant"]
TITLE_CHARS = dict((k, chr(0xE6A0 + i)) for i, k in enumerate(TITLES))
# 精英词缀图标（名牌前缀，用户 2026-11-23「前缀也用图标烘焙」）：编号同 add_elites.AFFIX，0 = 首领
AFFIX_ICONS = {1: "swift", 2: "iron", 3: "rage", 4: "leech", 5: "frost", 6: "venom", 7: "burst", 8: "summon",
               9: "taint", 10: "holy", 0: "champion"}
AFFIX_CHARS = dict((k, chr(0xE6B0 + k)) for k in AFFIX_ICONS)


def affix_icons_ready():
    return all(os.path.exists(os.path.join(ART, "affix_%s.png" % v)) for v in AFFIX_ICONS.values())


def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)


def item(name, src):
    tex = os.path.join(RP, "assets", "rpg", "textures", "item", "world", name + ".png")
    os.makedirs(os.path.dirname(tex), exist_ok=True)
    im = Image.open(src).convert("RGBA")
    assert im.size in ((16, 16), (32, 32)), (name, im.size)
    im.save(tex)
    wj(os.path.join(RP, "assets", "rpg", "models", "world", name + ".json"),
       {"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/world/" + name}})
    model = {"type": "minecraft:model", "model": "rpg:world/" + name}
    if name in TINTED:
        model["tints"] = [{"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]
    wj(os.path.join(RP, "assets", "rpg", "items", "world", name + ".json"), {"model": model})


def main():
    n = 0
    for name in ITEMS:
        item(name, os.path.join(ART, name + ".png"))
        n += 1
    item("blueprint_fragment", os.path.join(ART, "dungeons", "T_Paper_Graph_02.png"))
    n += 1
    providers = []
    for k in TITLES:
        src = os.path.join(ART, "title_%s.png" % k)
        dst = os.path.join(RP, "assets", "rpg", "textures", "font", "world_titles", k + ".png")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        providers.append({"type": "bitmap", "file": "rpg:font/world_titles/%s.png" % k, "height": 8, "ascent": 7,
                          "chars": [TITLE_CHARS[k]]})
    wj(os.path.join(RP, "assets", "rpg", "font", "world_titles.json"), {"providers": providers})
    if affix_icons_ready():
        prov = []
        for k, v in AFFIX_ICONS.items():
            dst = os.path.join(RP, "assets", "rpg", "textures", "font", "world_affix", v + ".png")
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(os.path.join(ART, "affix_%s.png" % v), dst)
            prov.append({"type": "bitmap", "file": "rpg:font/world_affix/%s.png" % v, "height": 8, "ascent": 7,
                         "chars": [AFFIX_CHARS[k]]})
        prov.append({"type": "space", "advances": {"": 2}})
        wj(os.path.join(RP, "assets", "rpg", "font", "world_affix.json"), {"providers": prov})
        print("world art: %d affix icons" % len(prov))
    print("world art: %d item icons, %d title glyphs" % (n, len(TITLES)))


if __name__ == "__main__":
    main()
