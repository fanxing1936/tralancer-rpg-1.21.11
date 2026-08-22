# -*- coding: utf-8 -*-
"""Wire the resource pack's unused weapon art up as real items.

The pack ships finished 32x32 art for five Minecraft-Dungeons-style weapons that
nothing ever references.  This adds a model + item-definition entry for each, and
a `give` function that hands them out in exactly the format the existing weapons
use.  Each one gets an original skill of its own -- see add_skills.py.
"""

import io
import json
import os
import re
import sys

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

RPG_MODELS = os.path.join(RP, "assets/rpg/models/item")
MC_ITEMS = os.path.join(RP, "assets/minecraft/items")
GIVE = os.path.join(DP, "data/rpg/function/command/give")


def wj(path, doc):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def model(parent, texture):
    return {"parent": parent, "textures": {"layer0": texture}}


def m(mdl):
    return {"type": "minecraft:model", "model": mdl}


# ---------------------------------------------------------------------------
# 1. models -- same shape the pack already uses for bubble_bow / soul_hunter
# ---------------------------------------------------------------------------
CROSSBOW_PARTS = ["", "_pulling_0", "_pulling_1", "_pulling_2", "_arrow", "_firework"]
BOW_PARTS = ["", "_pulling_0", "_pulling_1", "_pulling_2"]


def build_models():
    n = 0
    for base in ("azure_seeker", "baby_crossbow"):
        for part in CROSSBOW_PARTS:
            wj(os.path.join(RPG_MODELS, base + part + ".json"),
               model("item/crossbow", "rpg:item/%s%s" % (base, part)))
            n += 1
    for part in BOW_PARTS:
        wj(os.path.join(RPG_MODELS, "burst_gale_bow" + part + ".json"),
           model("item/bow", "rpg:item/burst_gale_bow" + part))
        n += 1
    for part in ("", "_cast"):
        wj(os.path.join(RPG_MODELS, "vine_whip" + part + ".json"),
           model("item/handheld_rod", "rpg:item/vine_whip" + part))
        n += 1
    wj(os.path.join(RPG_MODELS, "truthseeker.json"),
       model("rpg:item/sword_handheld", "rpg:item/truthseeker"))
    n += 1
    return n


# ---------------------------------------------------------------------------
# 2. item definitions
# ---------------------------------------------------------------------------
def crossbow_variant(base, pull0, pull1, pull2, arrow, rocket):
    return {
        "type": "minecraft:select", "property": "minecraft:charge_type",
        "cases": [{"when": "arrow", "model": m(arrow)},
                  {"when": "rocket", "model": m(rocket)}],
        "fallback": {
            "type": "minecraft:condition", "property": "minecraft:using_item",
            "on_false": m(base),
            "on_true": {
                "type": "minecraft:range_dispatch",
                "property": "minecraft:crossbow/pull", "fallback": m(pull0),
                "entries": [{"threshold": 0.58, "model": m(pull1)},
                            {"threshold": 1.0, "model": m(pull2)}]},
        },
    }


def bow_variant(base, pull0, pull1, pull2):
    return {
        "type": "minecraft:condition", "property": "minecraft:using_item",
        "on_false": m(base),
        "on_true": {
            "type": "minecraft:range_dispatch",
            "property": "minecraft:use_duration", "scale": 0.05,
            "fallback": m(pull0),
            "entries": [{"threshold": 0.65, "model": m(pull1)},
                        {"threshold": 0.9, "model": m(pull2)}]},
    }


def add_entry(rel, threshold, node):
    path = os.path.join(MC_ITEMS, rel)
    doc = json.load(io.open(path, encoding="utf-8"))
    entries = doc["model"]["entries"]
    entries[:] = [e for e in entries if e["threshold"] != threshold]
    entries.append({"threshold": threshold, "model": node})
    entries.sort(key=lambda e: e["threshold"])
    wj(path, doc)


def build_item_definitions():
    def cb(base):
        return crossbow_variant(*["rpg:item/%s%s" % (base, p) for p in
                                  ("", "_pulling_0", "_pulling_1", "_pulling_2",
                                   "_arrow", "_firework")])
    add_entry("crossbow.json", 1110003, cb("azure_seeker"))
    add_entry("crossbow.json", 1110004, cb("baby_crossbow"))
    add_entry("bow.json", 1110002, bow_variant(
        *["rpg:item/burst_gale_bow%s" % p for p in
          ("", "_pulling_0", "_pulling_1", "_pulling_2")]))
    add_entry("netherite_sword.json", 1110011, m("rpg:item/truthseeker"))

    # the pack had no fishing_rod definition at all -- build one on vanilla's shape
    cast = lambda a, b: {"type": "minecraft:condition",
                         "property": "minecraft:fishing_rod/cast",
                         "on_false": m(a), "on_true": m(b)}
    wj(os.path.join(MC_ITEMS, "fishing_rod.json"), {"model": {
        "type": "minecraft:range_dispatch",
        "property": "minecraft:custom_model_data", "index": 0,
        "fallback": cast("minecraft:item/fishing_rod", "minecraft:item/fishing_rod_cast"),
        "entries": [{"threshold": 1110001,
                     "model": cast("rpg:item/vine_whip", "rpg:item/vine_whip_cast")}],
    }})


# ---------------------------------------------------------------------------
# 3. the give function
# ---------------------------------------------------------------------------
RULE = '["",{"text":"+------------------+","italic":false,"color":"white"}]'


def line(text, colour="white", bold=False):
    parts = []
    for seg in text:
        if isinstance(seg, str):
            parts.append('{"text":"%s","italic":false,"color":"%s"}' % (seg, colour))
        else:
            t, c = seg
            parts.append('{"text":"%s","italic":false,"color":"%s","bold":true}' % (t, c))
    return '["",%s]' % ",".join(parts)


def skill_line(icon, kind, name, colour):
    return ('["",{"text":"%s%s","italic":false,"color":"white"},'
            '{"text":"[%s]","italic":false,"color":"%s","bold":true}]'
            % (icon, kind, name, colour))


def name_tag(tier, tier_colour, name, name_colour):
    return ('["",{"text":"[%s]","italic":false,"color":"%s","bold":true},'
            '{"text":"%s","italic":false,"color":"%s"}]'
            % (tier, tier_colour, name, name_colour))


ITEMS = [
    dict(key="azure_seeker", id="crossbow", cmd=1110003, tier="legend", tier_colour="gold",
         name="蔚蓝追寻者", colour="aqua",
         flavour=[[("[深海]", "aqua"), "之下沉睡的弩"], ["循着潮声", ("[追寻]", "aqua"), "猎物"]],
         icon="🏹", kind="被动技能", skill="深潜", skill_colour="gold",
         skill_text="命中后将目标拽入深渊并锚定",
         ench="{piercing:4,power:4,quick_charge:3,unbreaking:3}",
         attrs=[("oxygen_bonus", 4, "add_value", "any")],
         data="{deep_seek_tag:1b,bow_tag:1b}"),
    dict(key="baby_crossbow", id="crossbow", cmd=1110004, tier="epic", tier_colour="dark_purple",
         name="稚弩", colour="light_purple",
         flavour=[["孩童手中的", ("[玩具]", "light_purple")], ["却淬着大人的", ("[恶意]", "light_purple")]],
         icon="🏹", kind="被动技能", skill="顽劣", skill_colour="dark_purple",
         skill_text="命中后令目标眩晕脱力并现形",
         ench="{quick_charge:4,multishot:1,piercing:2}",
         attrs=[("movement_speed", 0.05, "add_multiplied_base", "mainhand")],
         data="{mischief_tag:1b,bow_tag:1b}"),
    dict(key="burst_gale_bow", id="bow", cmd=1110002, tier="legend", tier_colour="gold",
         name="疾风迸发之弓", colour="yellow",
         flavour=[["风自", ("[裂隙]", "yellow"), "中迸发"], ["每一箭都是一场", ("[风暴]", "yellow")]],
         icon="🏹", kind="被动技能", skill="裂空", skill_colour="gold",
         skill_text="命中处炸开风隙掀飞三格内敌人",
         ench="{power:5,punch:2,infinity:1,unbreaking:3}",
         attrs=[("movement_speed", 0.1, "add_multiplied_base", "mainhand")],
         data="{rift_tag:1b,bow_tag:1b}"),
    dict(key="vine_whip", id="fishing_rod", cmd=1110001, tier="epic", tier_colour="dark_purple",
         name="藤蔓之鞭", colour="green",
         flavour=[["自丛林深处", ("[垂落]", "green")], ["缠绕即是", ("[死亡]", "green")]],
         icon="🗡", kind="主动技能", skill="缠绕", skill_colour="dark_purple",
         skill_text="右键甩鞭消耗1级经验拽近敌人并连抽六鞭",
         ench="{unbreaking:3,lure:3,luck_of_the_sea:3}",
         attrs=[("attack_damage", 5, "add_value", "mainhand"),
                ("attack_speed", -1.5, "add_value", "mainhand"),
                ("entity_interaction_range", 2, "add_value", "mainhand")],
         data="{vine_tag:1b,sword_tag:1b}"),
    dict(key="truthseeker", id="netherite_sword", cmd=1110011, tier="epic", tier_colour="dark_purple",
         name="求真之刃", colour="red",
         flavour=[["刺穿谎言的", ("[利刃]", "red")], ["唯有", ("[真实]", "red"), "无法被斩断"]],
         icon="🪓", kind="被动技能", skill="洞悉", skill_colour="dark_purple",
         skill_text="命中使目标显形残血时追加真实伤害",
         ench="{sharpness:4,looting:2,sweeping_edge:3}",
         attrs=[("attack_damage", 9, "add_value", "mainhand"),
                ("attack_speed", -2.4, "add_value", "mainhand")],
         data="{truth_tag:1b,sword_tag:1b}"),
]


def build_give():
    out = [
        "# 用材质包里原本没有被引用的武器贴图做出来的五件装备。",
        "# 技能标签全部复用已有的处理逻辑，没有给每刻函数增加任何命令。",
        "",
    ]
    for it in ITEMS:
        lore = [RULE]
        for f in it["flavour"]:
            lore.append(line(f))
        lore.append(RULE)
        lore.append(skill_line(it["icon"], it["kind"], it["skill"], it["skill_colour"]))
        lore.append(line([it["skill_text"]]))
        lore.append(RULE)
        mods = ",".join(
            '{type:"%s",amount:%s,operation:%s,slot:%s,id:"rpg:extra/%s/%d"}'
            % (a, v, op, slot, it["key"], i)
            for i, (a, v, op, slot) in enumerate(it["attrs"]))
        edible = ""
        if it.get("consume"):
            edible = ("food={nutrition:0,saturation:0f,can_always_eat:1b},"
                      "consumable={consume_seconds:%df,animation:\"eat\","
                      "sound:\"minecraft:entity.generic.eat\",has_consume_particles:true,"
                      "on_consume_effects:[]}," % it["consume"])
        out.append(
            "give @a %s[custom_name=%s,lore=[%s],enchantments=%s,"
            "attribute_modifiers=[%s],%scustom_model_data={floats:[%d.0f]},"
            "custom_data=%s]"
            % (it["id"], name_tag(it["tier"], it["tier_colour"], it["name"], it["colour"]),
               ",".join(lore), it["ench"], mods, edible, it["cmd"], it["data"]))
    with io.open(os.path.join(GIVE, "extra.mcfunction"), "w",
                 encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")


ID_OK = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")


def check_ids():
    for it in ITEMS:
        for i in range(len(it["attrs"])):
            rid = "rpg:extra/%s/%d" % (it["key"], i)
            assert ID_OK.match(rid), "invalid modifier id: %s" % rid



# ---------------------------------------------------------------------------
# 4. 教条战斧 -- the pack's custom trimmable axe.  Its skill logic and its nine
#    trim models were already in the pack, but the `give` command for it lived
#    outside the data pack entirely, so nothing migrated or documented it.
#    (The author gave both of its modifiers the same id, which since 1.21.2 makes
#    the second collide with the first; they are split here.)
# ---------------------------------------------------------------------------
DOCTRINE_AXE = 'give @a iron_axe[custom_name=["",{"text":"[brave]","italic":false,"color":"aqua","bold":true},{"text":"教条战斧","italic":false,"color":"white"}],lore=[["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"教会","italic":false,"color":"aqua","bold":true},{"text":"炼制的武器","italic":false,"color":"white"}],["",{"text":"配发给每一位","italic":false,"color":"white"},{"text":"浮士德","italic":false,"color":"aqua","bold":true}],["",{"text":"+------------------+","italic":false,"color":"white"}]],enchantments={looting:1},attribute_modifiers=[{type:"attack_damage",amount:9,slot:mainhand,operation:add_value,id:"rpg:doctrine_axe/0"},{type:"attack_speed",amount:-3.1,slot:mainhand,operation:add_value,id:"rpg:doctrine_axe/1"}],custom_data={sword_tag:1b,axe_tag:1b,iron_axe:0b}]'


def build_axe():
    path = os.path.join(GIVE, "weapon.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    if "教条战斧" in s:
        return False
    note = "# 教条战斧：数据包里原本只有它的技能与模型，缺 give 指令"
    s = "\n".join([s.rstrip("\n"), "", note, DOCTRINE_AXE, ""])
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    return True


if __name__ == "__main__":
    check_ids()
    n = build_models()
    build_item_definitions()
    build_give()
    added = build_axe()
    print("models written: %d   item definitions updated: 5   give lines: %d   "
          "教条战斧 appended: %s" % (n, len(ITEMS), added))
