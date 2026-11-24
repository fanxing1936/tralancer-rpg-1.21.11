# -*- coding: utf-8 -*-
"""药水、驱魔器具、真名残页、裁决罪物、传承书、试炼钥匙的图标（Codex 按 docs/RELIC-ART-PROMPT.md 交付到 relic_ref/art）。

    python add_relic_art.py ../resourcepack

做法：物品本身不改。原来借用的原版物品模型（minecraft:items/<id>.json）外面套一层 minecraft:component 条件，
按 custom_data 认出本包的物品就换成自己的图标，其余照旧。所以背包里的旧物品也立刻换图。
新物品（空瓶、空白圣具、失乐园三种遗物）用 rpg:relic/<键>；图还没到就先借原版的。
"""
import io
import json
import os
import shutil
import sys
import zipfile

from mc_env import JAR
import potion_spec as PS

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "relic_ref", "art")
RP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "resourcepack")
OWN = {"empty_vial": "minecraft:item/glass_bottle", "blank_rite": "minecraft:item/iron_nugget", "forbidden_fruit": "minecraft:item/apple",
       "blood_mud": "minecraft:item/clay_ball", "broken_feather": "minecraft:item/feather"}


def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def rules():
    """原版物品模型 id → [(custom_data 谓词, 图标键)]，靠前的先认。"""
    r = {}

    def add(item, data, key):
        r.setdefault(item, []).append((data, key))

    for k, p in PS.POTIONS.items():
        add(PS.USE[p[2]][0], '{rpg_potion:"%s"}' % k, "potion_" + k)
    add("lingering_potion", "{rpg_strong_water:1b}", "strong_water")
    add("lingering_potion", "{rite_tag:1b}", "holy_water")
    add("allay_spawn_egg", "{holy_weapon_tag:1b}", "rite_doll")
    add("nether_star", "{holy_weapon_tag:1b}", "rite_star")
    add("iron_nugget", "{rpg_nail:1b}", "rite_nail")
    add("goat_horn", "{rpg_bell:1b}", "rite_bell")
    add("blaze_powder", "{rpg_incense:1b}", "rite_incense")
    add("soul_lantern", "{rpg_lantern:1b}", "rite_lantern")
    for n, dye in ((1, "white_dye"), (2, "gray_dye"), (3, "light_blue_dye")):
        add(dye, "{rpg_chalk:%db}" % n, "chalk_%d" % n)
    for n, item in enumerate(("feather", "prismarine_crystals", "clock", "poisonous_potato", "snowball", "amethyst_shard", "gold_ingot"), 1):
        add(item, "{rpg_medium:%db}" % n, "medium_%d" % n)
    for n in range(1, 8):
        add("paper", "{rpg_rite_page:1b,rpg_lord:%d}" % n, "page_%d" % n)
        add("echo_shard", "{rpg_sealed:1b,rpg_lord:%d}" % n, "sealed_%d" % n)
        add("nether_star", "{rpg_weapon_core:1b,rpg_lord:%d}" % n, "core_%d" % n)
    for n, b in ((31, "pope"), (32, "usurper"), (33, "jacques"), (34, "saul"), (35, "michael"), (36, "lucifer")):
        add("enchanted_book", "{rpg_legacy:%d}" % n, "legacy_" + b)
    return r


def base_model(item):
    p = os.path.join(RP, "assets", "minecraft", "items", item + ".json")
    if os.path.exists(p):
        return json.load(io.open(p, encoding="utf-8"))
    with zipfile.ZipFile(JAR) as z:
        return json.loads(z.read("assets/minecraft/items/%s.json" % item))


def model_of(key):
    """图到了就装贴图与模型，返回模型 id；没到返回 None。"""
    src = os.path.join(ART, key + ".png")
    if not os.path.exists(src):
        return None
    dst = os.path.join(RP, "assets", "rpg", "textures", "item", "relic", key + ".png")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    wj(os.path.join(RP, "assets", "rpg", "models", "relic", key + ".json"),
       {"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/relic/" + key}})
    return "rpg:relic/" + key


def main():
    have = want = 0
    for item, lst in rules().items():
        doc = base_model(item)
        node = doc["model"]
        for data, key in reversed(lst):
            want += 1
            m = model_of(key)
            if not m:
                continue
            have += 1
            node = {"type": "minecraft:condition", "property": "minecraft:component", "predicate": "minecraft:custom_data", "value": data,
                    "on_true": {"type": "minecraft:model", "model": m}, "on_false": node}
        if node is not doc["model"]:
            doc["model"] = node
            wj(os.path.join(RP, "assets", "minecraft", "items", item + ".json"), doc)
    for key, fallback in OWN.items():
        want += 1
        m = model_of(key)
        have += bool(m)
        wj(os.path.join(RP, "assets", "rpg", "items", "relic", key + ".json"), {"model": {"type": "minecraft:model", "model": m or fallback}})
    # 钥匙：本包的钥匙没有 custom_data（宝库锁要整个相等），两种原版钥匙直接换图
    for item, key in (("trial_key", "trial_key"), ("ominous_trial_key", "ominous_key")):
        want += 1
        m = model_of(key)
        if m:
            have += 1
            wj(os.path.join(RP, "assets", "minecraft", "items", item + ".json"), {"model": {"type": "minecraft:model", "model": m}})
    print("relic art: %d of %d icons installed" % (have, want))


if __name__ == "__main__":
    main()
