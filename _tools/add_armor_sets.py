# -*- coding: utf-8 -*-
"""批量护甲：圣卫残甲、驱魔人法衣、渊海套、恶魔枷甲，以及神圣套补全的腿与靴。

照现有护甲的做法：原版底材 + 锻造纹饰 + 染色，名字、描述、附魔、属性写在
组件里，custom_data 带 chestplate_tag（洗练与面板数值）。每件再带一个
armor_set 标记，穿齐四件由 rpg:armor_set/ 每秒检测一次，给出套装加成。

* 套装加成都是「穿齐时每秒重新确认」：属性修饰先删后加，效果缺了就补，
  死亡、重进服务器后不会卡在半套状态。
* 驱魔人的［驱魔圣职］复用圣器的 holy_effects，在 tick_end 里每刻清视野。
* 神圣套原有的圣荆棘冠、都灵裹尸布补上 armor_set 和套装描述。
* 掉落：圣卫残甲进试炼宝库的分部位奖池；驱魔人法衣进不祥宝库；
  渊海套挂在利维坦麾下罪仆上；恶魔枷甲挂在七柱全部罪仆上。神圣件不掉落。

必须在 add_demon_minions（罪仆掉落表）之后、make_boxes 与 polish_ui 之前。
"""
import glob
import io
import json
import os
import sys

import rpg_ui_style as ui

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")
LOOT = os.path.join(DP, "data/rpg/loot_table")
TICK_TAG = os.path.join(DP, "data/minecraft/tags/function/tick.json")

SLOTS = ("head", "chest", "legs", "feet")
SLOT_OF = {"helmet": "head", "chestplate": "chest", "leggings": "legs", "boots": "feet"}
TRIAL_TABLE = {"head": "helmet", "chest": "chestplate", "legs": "leggings", "feet": "boots"}

OBJECTIVES = ["rpg_as_clock", "rpg_as_hp", "rpg_as_max"]

EXORCIST_VAULT_WEIGHT = 1     # 不祥宝库 3 抽、总权重 72：每次开启约 4%
ABYSS_CHANCE = 0.03           # 利维坦麾下罪仆，每次击杀
DEMON_CHANCE = 0.01           # 七柱全部罪仆，每次击杀


def dye(colour):
    return int(ui.hex_of(colour)[1:], 16)


# ---------------------------------------------------------------------------
# 套装定义
#   flavour：两行引言，以「[」开头的片段用档次色加粗
#   pieces：(底材, 名字, 纹饰, 纹饰材质, 附魔, 属性, 被动名, 被动说明)
#   属性：(attribute, amount, operation)，护甲与韧性写在最前面
# ---------------------------------------------------------------------------
ADD, MUL = "add_value", "add_multiplied_base"

SETS = [
    dict(key="sentinel", tier="epic", colour=ui.tier_colour("epic"),
         flavour=[["圣塔之下的", "[守望]", "从未终结"], ["残甲仍记得那句", "[誓言]"]],
         bonus=("［圣卫之誓］", "护甲韧性 +4，击退抗性 +0.2"),
         pieces=[
             ("golden_helmet", "圣卫残盔", "ward", "quartz",
              {"protection": 2, "projectile_protection": 2},
              [("armor", 3, ADD), ("armor_toughness", 2, ADD), ("knockback_resistance", 0.05, ADD)],
              None, None),
             ("chainmail_chestplate", "圣卫胸铠", "sentry", "gold",
              {"protection": 2, "projectile_protection": 2, "blast_protection": 1},
              [("armor", 7.5, ADD), ("armor_toughness", 2.5, ADD), ("knockback_resistance", 0.05, ADD)],
              None, None),
             ("iron_leggings", "圣卫腿甲", "sentry", "gold",
              {"protection": 2, "projectile_protection": 2},
              [("armor", 6, ADD), ("armor_toughness", 2, ADD), ("knockback_resistance", 0.05, ADD)],
              None, None),
             ("leather_boots", "圣卫战靴", "ward", "gold",
              {"protection": 2, "projectile_protection": 2, "feather_falling": 2},
              [("armor", 3, ADD), ("armor_toughness", 2, ADD), ("knockback_resistance", 0.05, ADD)],
              None, None),
         ]),
    dict(key="exorcist", tier="legend", colour=ui.tier_colour("legend"),
         flavour=[["行走于", "[罪仆]", "之间的"], ["最后一盏", "[圣灯]"]],
         bonus=("［驱魔圣职］", "免疫失明与黑暗"),
         pieces=[
             ("leather_helmet", "驱魔人兜帽", "eye", "gold",
              {"protection": 3, "fire_protection": 2, "projectile_protection": 2},
              [("armor", 3, ADD), ("armor_toughness", 3, ADD), ("knockback_resistance", 0.1, ADD),
               ("entity_interaction_range", 0.5, ADD)],
              "[明察]", "攻击距离 +0.5 格"),
             ("leather_chestplate", "驱魔人法衣", "host", "gold",
              {"protection": 3, "blast_protection": 2, "fire_protection": 2},
              [("armor", 7, ADD), ("armor_toughness", 3, ADD), ("knockback_resistance", 0.1, ADD),
               ("max_health", 0.3, MUL)],
              "[誓约]", "生命上限 +30%"),
             ("chainmail_leggings", "驱魔人绑腿", "wayfinder", "gold",
              {"protection": 3, "projectile_protection": 2},
              [("armor", 5, ADD), ("armor_toughness", 3, ADD), ("knockback_resistance", 0.1, ADD),
               ("sneaking_speed", 0.3, MUL), ("step_height", 0.5, ADD)],
              "[行脚]", "潜行速度 +30%，可直接跨上一格高的台阶"),
             ("netherite_boots", "驱魔人长靴", "wayfinder", "gold",
              {"protection": 3, "feather_falling": 3},
              [("armor", 3, ADD), ("armor_toughness", 3, ADD), ("knockback_resistance", 0.1, ADD),
               ("movement_speed", 0.1, MUL), ("safe_fall_distance", 3, ADD)],
              "[巡礼]", "移动速度 +10%，安全摔落高度 +3 格"),
         ]),
    dict(key="abyss", tier="legend", colour=ui.tier_colour("legend"),
         flavour=[["沉入", "[深渊]", "的甲胄"], ["至今仍听得见", "[潮声]"]],
         bonus=("［渊海之主］", "身处水中时获得潮涌能量与海豚的恩惠"),
         pieces=[
             ("turtle_helmet", "渊海之盔", "tide", "lapis",
              {"protection": 3, "aqua_affinity": 1},
              [("armor", 3.5, ADD), ("armor_toughness", 3, ADD), ("knockback_resistance", 0.1, ADD),
               ("oxygen_bonus", 3, ADD)],
              "[鳃息]", "水下憋气时间延长，等同水下呼吸 III"),
             ("diamond_chestplate", "渊海之铠", "tide", "lapis",
              {"protection": 3, "blast_protection": 2},
              [("armor", 9, ADD), ("armor_toughness", 4, ADD), ("knockback_resistance", 0.1, ADD),
               ("max_health", 0.2, MUL)],
              "[潮涌]", "生命上限 +20%"),
             ("chainmail_leggings", "渊海之胫", "coast", "diamond",
              {"protection": 3, "projectile_protection": 2},
              [("armor", 6, ADD), ("armor_toughness", 3, ADD), ("knockback_resistance", 0.1, ADD),
               ("water_movement_efficiency", 0.5, ADD)],
              "[逆流]", "水中移动效率 +50%"),
             ("leather_boots", "渊海之履", "coast", "lapis",
              {"protection": 3, "feather_falling": 2},
              [("armor", 3.5, ADD), ("armor_toughness", 3, ADD), ("knockback_resistance", 0.3, ADD),
               ("explosion_knockback_resistance", 0.5, ADD)],
              "[踏浪]", "击退抗性 +0.2，爆炸击退抗性 +50%"),
         ]),
    dict(key="demon", tier="devil", colour=ui.NAMELESS["lit"],
         flavour=[["以", "[罪]", "为锁，以", "[血]", "为钥"], ["戴上它的人，再也", "[摘不下]"]],
         bonus=("［困兽之枷］", "生命低于一半时获得力量 II 与抗性提升 I"),
         pieces=[
             ("netherite_helmet", "恶魔枷冠", "snout", "redstone",
              {"protection": 4, "fire_protection": 3, "thorns": 2},
              [("armor", 4, ADD), ("armor_toughness", 3.5, ADD), ("knockback_resistance", 0.1, ADD),
               ("attack_damage", 0.05, MUL), ("max_health", -0.05, MUL)],
              "[罪契]", "攻击力 +5%，生命上限 −5%"),
             ("chainmail_chestplate", "恶魔枷甲", "rib", "netherite",
              {"protection": 4, "blast_protection": 3, "thorns": 2},
              [("armor", 9.5, ADD), ("armor_toughness", 4.5, ADD), ("knockback_resistance", 0.1, ADD),
               ("attack_damage", 0.05, MUL), ("max_health", -0.05, MUL)],
              "[罪契]", "攻击力 +5%，生命上限 −5%"),
             ("netherite_leggings", "恶魔枷胫", "rib", "redstone",
              {"protection": 4, "projectile_protection": 3, "thorns": 2},
              [("armor", 7.5, ADD), ("armor_toughness", 4, ADD), ("knockback_resistance", 0.1, ADD),
               ("attack_damage", 0.05, MUL), ("max_health", -0.05, MUL)],
              "[罪契]", "攻击力 +5%，生命上限 −5%"),
             ("chainmail_boots", "恶魔枷镣", "silence", "redstone",
              {"protection": 4, "feather_falling": 3, "thorns": 2},
              [("armor", 4, ADD), ("armor_toughness", 3.5, ADD), ("knockback_resistance", 0.1, ADD),
               ("attack_damage", 0.05, MUL), ("max_health", -0.05, MUL)],
              "[罪契]", "攻击力 +5%，生命上限 −5%"),
         ]),
]

HOLY_ENCH = {"blast_protection": 1, "fire_protection": 2, "projectile_protection": 2,
             "protection": 5, "thorns": 3}
# 神圣套：帽与甲是原有的受难红皮甲，补的腿与靴走黑裤白靴、金色纹饰
HOLY = dict(key="holy", tier="holy", colour=ui.tier_colour("holy"),
            bonus=("［圣骸］", "持续获得生命恢复 I"),
            pieces=[
                dict(base="netherite_leggings", name="无缝圣袍", pattern="silence", material="gold",
                     flavour=[["他们为这件", "[无缝]", "的袍子拈阄"], ["却分不走其中的", "[恩典]"]],
                     ench=HOLY_ENCH,
                     attrs=[("armor", 10, ADD), ("armor_toughness", 4, ADD),
                            ("knockback_resistance", 0.3, ADD), ("burning_time", -0.5, MUL)],
                     passive="[无缝]", text="击退抗性 +0.3，着火时间减半"),
                dict(base="leather_boots", name="各各他之履", pattern="flow", material="gold",
                     dyed=dye(ui.WHITE),
                     flavour=[["赤足走过", "[各各他]", "的人"], ["留下了这双", "[白履]"]],
                     ench=dict(HOLY_ENCH, feather_falling=4),
                     attrs=[("armor", 5, ADD), ("armor_toughness", 3, ADD),
                            ("movement_speed", 0.1, MUL), ("safe_fall_distance", 4, ADD)],
                     passive="[苦路]", text="移动速度 +10%，安全摔落高度 +4 格"),
            ])
# 神圣套原有的两件（由原包的 give/weapon 提供）
HOLY_OLD = ["圣荆棘冠", "都灵裹尸布"]


# ---------------------------------------------------------------------------
# 物品 -> 组件
# ---------------------------------------------------------------------------
def rule():
    return ui.row_value(ui.comp(ui.RULE_TEXT, ui.WHITE))


def flavour_row(parts, colour):
    return ui.row_value(*[ui.comp(p, colour, True) if p.startswith("[") else ui.comp(p, ui.WHITE)
                          for p in parts])


def set_rows(s):
    name, text = s["bonus"]
    return [ui.row_value(ui.comp("套装 · 穿齐四件", ui.WHITE), ui.comp(name, s["colour"], True)),
            ui.row_value(ui.comp(text, ui.WHITE))]


# 皮革件的染色，按件给（每套底材混搭，像原有的森焱、王者、冰霜那样）
DYES = {
    "圣卫战靴": dye(ui.HOLY_LIGHT),
    "驱魔人兜帽": dye(ui.HOLY_DARK),
    "驱魔人法衣": dye(ui.shade(ui.HOLY_DARK, 0.65)),
    "渊海之履": dye(ui.pillar(2)["deep"]),
}

# 统一耐久：底材混搭后皮革、锁链件也不至于一碰就坏（按下界合金 / 钻石的数值）
DURABILITY = {"devil": {"head": 407, "chest": 592, "legs": 555, "feet": 481},
              "legend": {"head": 407, "chest": 592, "legs": 555, "feet": 481},
              "epic": {"head": 363, "chest": 528, "legs": 495, "feet": 429}}


def item(s, base, name, pattern, material, ench, attrs, passive, text, flavour, dyed=None,
         holy=False):
    colour = s["colour"]
    lore = [rule()] + [flavour_row(f, colour) for f in flavour] + [rule()]
    if passive:
        lore += [ui.row_value(ui.comp("🛡被动技能", ui.WHITE), ui.comp(passive, colour, True)),
                 ui.row_value(ui.comp(text, ui.WHITE)),
                 rule()]
    lore += set_rows(s) + [rule()]
    slot = SLOT_OF[base.rsplit("_", 1)[1]]
    stem = "rpg:armor/%s/%s" % (s["key"], slot)
    comps = {
        "custom_name": ui.row_value(ui.comp(ui.tier_tag(s["tier"]), colour, True),
                                    ui.comp(name, ui.WHITE, False)),
        "lore": lore,
        "trim": {"pattern": "minecraft:" + pattern, "material": "minecraft:" + material},
        # 纹饰只管外观，提示行不显示（与原有武器一致）
        "tooltip_display": {"hidden_components": ["minecraft:trim"]},
        "enchantments": {"minecraft:" + k: v for k, v in ench.items()},
        "attribute_modifiers": [
            {"type": "minecraft:" + a, "amount": amt, "operation": op, "slot": slot,
             "id": "%s/%d" % (stem, i)}
            for i, (a, amt, op) in enumerate(attrs)],
    }
    dyed = DYES.get(name, dyed)
    if dyed is not None:
        comps["dyed_color"] = dyed
    if s["tier"] in DURABILITY:
        comps["max_damage"] = DURABILITY[s["tier"]][slot]
    if holy:
        comps["unbreakable"] = {}
    data = "{chestplate_tag:1b,%sarmor_set:\"%s\"}" % ("holy_weapon_tag:1b," if holy else "",
                                                         s["key"])
    return dict(base=base, name=name, slot=slot, comps=comps, data=data)


def all_items():
    out = {}
    for s in SETS:
        out[s["key"]] = [item(s, *p[:7], p[7], s["flavour"]) for p in s["pieces"]]
    out["holy"] = [item(HOLY, p["base"], p["name"], p["pattern"], p["material"], p["ench"],
                        p["attrs"], p["passive"], p["text"], p["flavour"], p.get("dyed"), True)
                   for p in HOLY["pieces"]]
    return out


def snbt(value):
    # JSON 是 SNBT 的子集（带引号的键、true/false、数字），组件值直接写 JSON
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def give_line(it, target="@a"):
    body = ",".join("%s=%s" % (k, snbt(v)) for k, v in it["comps"].items())
    return "give %s %s[%s,custom_data=%s]" % (target, it["base"], body, it["data"])


def loot_entry(it, weight=None):
    entry = {"type": "minecraft:item", "name": "minecraft:" + it["base"],
             "functions": [
                 {"function": "minecraft:set_components",
                  "components": {"minecraft:" + k: v for k, v in it["comps"].items()}},
                 {"function": "minecraft:set_custom_data", "tag": it["data"]}]}
    if weight is not None:
        entry["weight"] = weight
    return entry


# ---------------------------------------------------------------------------
# 文件读写
# ---------------------------------------------------------------------------
def read(path):
    return io.open(path, encoding="utf-8").read()


def write(path, text):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(path, "w", encoding="utf-8", newline="\n").write(text.rstrip("\n") + "\n")


def wj(path, doc):
    write(path, json.dumps(doc, ensure_ascii=False, indent=2))


def wf(rel, text):
    write(os.path.join(FUNC, rel), text)


# ---------------------------------------------------------------------------
# give
# ---------------------------------------------------------------------------
ARMOR_SUFFIXES = ("_helmet[", "_chestplate[", "_leggings[", "_boots[")


def patch_holy_old(lines):
    """圣荆棘冠、都灵裹尸布：custom_data 加 armor_set，描述末尾补套装两行。"""
    patched = 0
    for i, line in enumerate(lines):
        if not line.startswith("give ") or not any(n in line for n in HOLY_OLD):
            continue
        if 'armor_set:"holy"' in line:
            continue
        old = "custom_data={holy_weapon_tag:1b,chestplate_tag:1b}"
        assert old in line, "神圣旧件的 custom_data 变了：" + line[:80]
        line = line.replace(old, 'custom_data={holy_weapon_tag:1b,chestplate_tag:1b,armor_set:"holy"}')
        # 原包的分隔线组件键序是 text/italic/color：按原样找最后一条
        legacy = '["",{"text":"%s","italic":false,"color":"white"}]' % ui.RULE_TEXT
        end = line.index("],enchantments=")
        cut = line.rindex(legacy, 0, end)
        assert cut + len(legacy) == end, "神圣旧件的描述结尾不是分隔线：" + line[:80]
        extra = ",".join(snbt(r) for r in set_rows(HOLY) + [rule()])
        line = line[:end] + "," + extra + line[end:]
        lines[i] = line
        patched += 1
    return patched


def build_give(items):
    path = os.path.join(FUNC, "command/give/weapon.mcfunction")
    lines = read(path).rstrip("\n").split("\n")
    patched = patch_holy_old(lines)
    appended = False
    if not any("圣卫残盔" in l for l in lines):
        lines += ["", "# 批量护甲（add_armor_sets.py）：四套新护甲与神圣套补全"]
        for key in ("sentinel", "exorcist", "abyss", "demon", "holy"):
            lines += [give_line(it) for it in items[key]]
        appended = True
    write(path, "\n".join(lines))

    # 单独入口：全部护甲发给执行者自己。组件与 give/weapon 逐字相同，
    # make_boxes 按组件去重，潜影盒里仍只收一份。
    armour = [l.replace("give @a ", "give @s ", 1) for l in lines
              if l.startswith("give @a ") and any(s in l for s in ARMOR_SUFFIXES)]
    wf("command/give/armor.mcfunction", "\n".join(
        ["# 全部护甲，发给执行者自己（由 add_armor_sets.py 生成）"] + armour))
    return appended, patched, len(armour)


# ---------------------------------------------------------------------------
# 套装检测
# ---------------------------------------------------------------------------
TICK = """\
# 套装检测的秒表：每 20 刻对全部玩家确认一次。
scoreboard players add #as rpg_as_clock 1
execute if score #as rpg_as_clock matches 20.. run function rpg:armor_set/second
"""

SECOND = """\
scoreboard players set #as rpg_as_clock 0
execute as @a[gamemode=!spectator] at @s run function rpg:armor_set/player
"""

FULL = ("execute if items entity @s armor.head *[minecraft:custom_data~{{armor_set:\"{k}\"}}]"
        " if items entity @s armor.chest *[minecraft:custom_data~{{armor_set:\"{k}\"}}]"
        " if items entity @s armor.legs *[minecraft:custom_data~{{armor_set:\"{k}\"}}]"
        " if items entity @s armor.feet *[minecraft:custom_data~{{armor_set:\"{k}\"}}]"
        " run tag @s add rpg.set.{k}.now")

PLAYER_SET = """\
{full}
execute if entity @s[tag=rpg.set.{k}.now] run function rpg:armor_set/{k}_on
execute if entity @s[tag=rpg.set.{k},tag=!rpg.set.{k}.now] run function rpg:armor_set/{k}_off
tag @s remove rpg.set.{k}.now"""

FIRST_ON = ("execute if entity @s[tag=!rpg.set.{k}] run playsound "
            "minecraft:item.armor.equip_netherite player @s ~ ~ ~ 1 0.8\n"
            "tag @s add rpg.set.{k}\n")

ON = {
    # 属性修饰先删后加：每秒重新确认，重生后也补得回来
    "sentinel": """\
attribute @s minecraft:armor_toughness modifier remove rpg:armor_set/sentinel
attribute @s minecraft:armor_toughness modifier add rpg:armor_set/sentinel 4 add_value
attribute @s minecraft:knockback_resistance modifier remove rpg:armor_set/sentinel
attribute @s minecraft:knockback_resistance modifier add rpg:armor_set/sentinel 0.2 add_value
""",
    # 视野由 tick_end 每刻清除，这里只维持标签
    "exorcist": "",
    "abyss": """\
execute if block ~ ~ ~ minecraft:water run tag @s add rpg.set.abyss.wet
execute if block ~ ~1 ~ minecraft:water run tag @s add rpg.set.abyss.wet
execute if entity @s[tag=rpg.set.abyss.wet] run effect give @s minecraft:conduit_power 3 0 true
execute if entity @s[tag=rpg.set.abyss.wet] run effect give @s minecraft:dolphins_grace 3 0 true
tag @s remove rpg.set.abyss.wet
""",
    # 生命 ×100 与上限 ×50 比较：低于一半
    "demon": """\
execute store result score @s rpg_as_hp run data get entity @s Health 100
execute store result score @s rpg_as_max run attribute @s minecraft:max_health get 50
execute if score @s rpg_as_hp < @s rpg_as_max run effect give @s minecraft:strength 3 1 true
execute if score @s rpg_as_hp < @s rpg_as_max run effect give @s minecraft:resistance 3 0 true
""",
    # 无限时长：每秒补发会重置生命恢复的回血节拍，所以只在缺失时给一次
    "holy": """\
execute unless predicate rpg:armor_set/regen run effect give @s minecraft:regeneration infinite 0 true
""",
}

OFF = {
    "sentinel": """\
attribute @s minecraft:armor_toughness modifier remove rpg:armor_set/sentinel
attribute @s minecraft:knockback_resistance modifier remove rpg:armor_set/sentinel
""",
    "exorcist": "",
    "abyss": "",
    "demon": "",
    # 只撤套装给的那份无限恢复，药水给的有限时长不动
    "holy": """\
execute if predicate rpg:armor_set/regen_infinite run effect clear @s minecraft:regeneration
""",
}

SET_KEYS = ["sentinel", "exorcist", "abyss", "demon", "holy"]
SET_NAMES = {"sentinel": "圣卫残甲", "exorcist": "驱魔人法衣", "abyss": "渊海套",
             "demon": "恶魔枷甲", "holy": "神圣套"}


def build_functions():
    wf("armor_set/tick.mcfunction", TICK)
    wf("armor_set/second.mcfunction", SECOND)
    body = ["# 穿齐四件同一 armor_set 才算成套；脱下任一件，下一秒撤掉加成。"]
    for k in SET_KEYS:
        body += ["", "# " + SET_NAMES[k], PLAYER_SET.format(k=k, full=FULL.format(k=k))]
    wf("armor_set/player.mcfunction", "\n".join(body))
    for k in SET_KEYS:
        wf("armor_set/%s_on.mcfunction" % k,
           "# %s：穿齐四件，每秒确认一次\n" % SET_NAMES[k] + FIRST_ON.format(k=k) + ON[k])
        wf("armor_set/%s_off.mcfunction" % k,
           "# %s：不再成套\ntag @s remove rpg.set.%s\n" % (SET_NAMES[k], k) + OFF[k])

    # 生命恢复：有没有（任意来源）、是不是套装给的无限时长（duration 为 -1）
    pred = os.path.join(DP, "data/rpg/predicate/armor_set")
    regen = lambda extra: {"condition": "minecraft:entity_properties", "entity": "this",
                           "predicate": {"effects": {"minecraft:regeneration": extra}}}
    wj(os.path.join(pred, "regen.json"), regen({}))
    wj(os.path.join(pred, "regen_infinite.json"), regen({"duration": {"max": -1}}))

    tag = json.loads(read(TICK_TAG))
    if "rpg:armor_set/tick" not in tag["values"]:
        i = tag["values"].index("rpg:command/tick_end")
        tag["values"].insert(i, "rpg:armor_set/tick")
        wj(TICK_TAG, tag)

    path = os.path.join(FUNC, "command/tick_end.mcfunction")
    s = read(path)
    anchor = "execute as @a[tag=rpg.holy] run function rpg:command/holy_effects"
    line = ("execute as @a[tag=rpg.set.exorcist,tag=!rpg.holy] "
            "run function rpg:command/holy_effects")
    if line not in s:
        assert anchor in s, "tick_end 里没有圣器清视野的锚点"
        s = s.replace(anchor, anchor + "\n# 驱魔人法衣［驱魔圣职］：与圣器一样护住视野\n" + line, 1)
        write(path, s)


def add_objectives():
    path = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = read(path)
    block = ["scoreboard objectives add %s dummy" % o for o in OBJECTIVES
             if ("scoreboard objectives add %s " % o) not in s]
    if block:
        write(path, s.rstrip("\n") + "\n\n##套装护甲\n" + "\n".join(block))
    return block


# ---------------------------------------------------------------------------
# 掉落
# ---------------------------------------------------------------------------
MARK = "rpg:armor_set/"


def build_loot(items):
    added = []
    for key in ("exorcist", "abyss", "demon"):
        wj(os.path.join(LOOT, "armor_set/%s.json" % key),
           {"pools": [{"rolls": 1, "entries": [loot_entry(it) for it in items[key]]}]})

    # 圣卫残甲：试炼之室的主表里各一个候选（按部位抽装备的四张旧表已随装备养成重置退役）
    path = os.path.join(LOOT, "trial/trial.json")
    doc = json.loads(read(path))
    entries = doc["pools"][0]["entries"]
    for it in items["sentinel"]:
        if not any(it["name"] in json.dumps(e, ensure_ascii=False) for e in entries):
            entries.append(loot_entry(it, 1))
            added.append("trial/trial:" + it["name"])
    wj(path, doc)

    # 驱魔人法衣：不祥宝库
    path = os.path.join(LOOT, "trial/trial_ominous.json")
    doc = json.loads(read(path))
    entries = doc["pools"][0]["entries"]
    if not any(e.get("value") == MARK + "exorcist" for e in entries):
        entries.append({"type": "minecraft:loot_table", "value": MARK + "exorcist",
                        "weight": EXORCIST_VAULT_WEIGHT})
        wj(path, doc)
        added.append("trial/trial_ominous")

    # 罪仆：渊海套只在利维坦麾下，恶魔枷甲七柱都有
    def kill_pool(table, chance):
        return {"rolls": 1,
                "conditions": [{"condition": "minecraft:killed_by_player"},
                               {"condition": "minecraft:random_chance", "chance": chance}],
                "entries": [{"type": "minecraft:loot_table", "value": MARK + table}]}

    minions = sorted(glob.glob(os.path.join(LOOT, "minion", "*", "*.json")))
    assert len(minions) == 35, "罪仆掉落表应为 7 柱 × 5 名，实际 %d" % len(minions)
    for path in minions:
        doc = json.loads(read(path))
        values = [e.get("value") for p in doc["pools"] for e in p["entries"]]
        changed = False
        if MARK + "demon" not in values:
            doc["pools"].append(kill_pool("demon", DEMON_CHANCE))
            changed = True
        lord = os.path.basename(os.path.dirname(path))
        if lord == "leviathan" and MARK + "abyss" not in values:
            doc["pools"].append(kill_pool("abyss", ABYSS_CHANCE))
            changed = True
        if changed:
            wj(path, doc)
            added.append("minion/%s/%s" % (lord, os.path.basename(path)[:-5]))
    return added


if __name__ == "__main__":
    items = all_items()
    appended, patched, n = build_give(items)
    print("armor_sets: give appended: %s  holy old patched: %d  give/armor: %d pieces"
          % (appended, patched, n))
    build_functions()
    print("armor_sets: objectives added: %s" % (", ".join(add_objectives()) or "(already present)"))
    print("armor_sets: loot tables touched: %d" % len(build_loot(items)))
