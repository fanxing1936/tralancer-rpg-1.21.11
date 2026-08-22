# -*- coding: utf-8 -*-
"""雅斤 / 波阿斯 -- a paired legendary sword set.

Named for the two bronze pillars of Solomon's temple, which is the register the
rest of the pack's legendary gear already uses (亚巴顿, 别西卜, 贝利尔, 萨麦尔).

  雅斤 Jachin  "他必坚立"  active  -- 立柱: plant a pillar of light, rooting and
                                     damaging everything around you
  波阿斯 Boaz  "力量在他"  passive -- 承力: every third landed hit becomes a
                                     reinforced blow
  dual wield              synergy -- 圣殿: hold one in each hand and the pillar
                                     widens, 承力 fires every second hit, and the
                                     pillar also shields you

Off-hand detection needs an index scope the pack did not have, so this adds an
`rpg.o.*` block to rpg:command/index alongside the existing main-hand one.
"""

import io
import json
import os
import sys

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

RPG_MODELS = os.path.join(RP, "assets/rpg/models/item")
MC_ITEMS = os.path.join(RP, "assets/minecraft/items")
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement/item")

# every colour below is sampled out of the two sprites themselves
# 雅斤: 紫刃 + 金柄       波阿斯: 青刃 + 品红刃口
JACHIN_PURPLE = 8001173     # #7A1695  15% of 雅斤's pixels
JACHIN_GOLD = 15915367      # #F2D967  14%
BOAZ_TEAL = 1344145         # #148291  23% of 波阿斯's pixels
BOAZ_PINK = 14585842        # #DE8FF2  13%

P_PUR = "[0.478,0.086,0.584]"    # 雅斤紫
P_GLD = "[0.949,0.851,0.404]"    # 雅斤金
P_TEA = "[0.078,0.510,0.569]"    # 波阿斯青
P_PNK = "[0.871,0.561,0.949]"    # 波阿斯粉
CONSUME = 100080     # unused by every other active skill in the pack

MAINHAND = ["jachin_tag", "boaz_tag"]
OFFHAND = ["jachin_tag", "boaz_tag"]
OBJECTIVES = [("boaz", "minecraft.custom:minecraft.damage_dealt"),
              ("rpg_boaz_stack", "dummy")]


def wj(path, doc):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def wf(rel, text):
    path = os.path.join(FUNC, rel)
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text.rstrip("\n") + "\n")


# ---------------------------------------------------------------------------
# resource pack
# ---------------------------------------------------------------------------
TWIN_HANDHELD = {
    "parent": "item/generated",
    # 包里原本的 sword_handheld 给左手用了 rotation [-170,-90,-55]，
    # 那个 -170 的 X 翻转就是副手"反手拿"的来源。
    # 这里按原版 item/handheld 的做法，左手只把 Y、Z 取反，于是双手都是正手。
    "display": {
        "thirdperson_righthand": {"rotation": [0, -90, 55],
                                  "translation": [0, 6.75, 2],
                                  "scale": [1.46, 0.85, 0.85]},
        "thirdperson_lefthand": {"rotation": [0, 90, -55],
                                 "translation": [0, 6.75, 2],
                                 "scale": [1.46, 0.85, 0.85]},
        "firstperson_righthand": {"rotation": [0, -90, 25],
                                  "translation": [1.13, 3.2, 1.13],
                                  "scale": [0.68, 0.68, 0.68]},
        "firstperson_lefthand": {"rotation": [0, 90, -25],
                                 "translation": [1.13, 3.2, 1.13],
                                 "scale": [0.68, 0.68, 0.68]},
    },
}


def build_models():
    wj(os.path.join(RPG_MODELS, "twin_handheld.json"), TWIN_HANDHELD)
    for name in ("jachin", "boaz"):
        wj(os.path.join(RPG_MODELS, name + ".json"),
           {"parent": "rpg:item/twin_handheld",
            "textures": {"layer0": "rpg:item/" + name}})

    path = os.path.join(MC_ITEMS, "netherite_sword.json")
    doc = json.load(io.open(path, encoding="utf-8"))
    entries = doc["model"]["entries"]
    for cmd, name in ((1110012, "jachin"), (1110013, "boaz")):
        entries[:] = [e for e in entries if e["threshold"] != cmd]
        entries.append({"threshold": cmd,
                        "model": {"type": "minecraft:model",
                                  "model": "rpg:item/" + name}})
    entries.sort(key=lambda e: e["threshold"])
    wj(path, doc)


# ---------------------------------------------------------------------------
# the two items
# ---------------------------------------------------------------------------
RULE = '["",{"text":"+------------------+","italic":false,"color":"white"}]'


def seg(text, colour="white", bold=False):
    return ('{"text":"%s","italic":false,"color":"%s"%s}'
            % (text, colour, ',"bold":true' if bold else ""))


def row(*segs):
    return '["",%s]' % ",".join(segs)


CONSUMABLE = ('{consume_seconds:%df,animation:"eat",'
              'sound:"minecraft:entity.generic.eat",has_consume_particles:true,'
              'on_consume_effects:[]}' % CONSUME)

JACHIN = ("give @a netherite_sword["
          "custom_name=" + row(seg("[legend]", "gold", True), seg("雅斤", "light_purple")) + ","
          "lore=[" + ",".join([
              RULE,
              row(seg("所罗门圣殿右侧的"), seg("[石柱]", "light_purple", True)),
              row(seg("其名为"), seg("[他必坚立]", "light_purple", True)),
              RULE,
              row(seg("🗡主动技能"), seg("[称量]", "gold", True)),
              row(seg("消耗1级经验称量周围敌人，残血者显出亏欠")),
              row(seg("与"), seg("[波阿斯]", "aqua", True), seg("双持时范围与判决同时加重")),
              RULE]) + "],"
          "enchantments={sharpness:5,sweeping_edge:3,looting:2,unbreaking:3},"
          "attribute_modifiers=["
          '{type:"attack_damage",amount:11,operation:add_value,slot:mainhand,id:"rpg:twin/jachin/0"},'
          '{type:"attack_speed",amount:-2.6,operation:add_value,slot:mainhand,id:"rpg:twin/jachin/1"},'
          '{type:"attack_damage",amount:6,operation:add_value,slot:offhand,id:"rpg:twin/jachin/2"}],'
          "food={nutrition:0,saturation:0f,can_always_eat:1b},"
          "consumable=" + CONSUMABLE + ","
          "unbreakable={},custom_model_data={floats:[1110012.0f]},"
          "custom_data={jachin_tag:1b,sword_tag:1b}]")

BOAZ = ("give @a netherite_sword["
        "custom_name=" + row(seg("[legend]", "gold", True), seg("波阿斯", "aqua")) + ","
        "lore=[" + ",".join([
            RULE,
            row(seg("所罗门圣殿左侧的"), seg("[石柱]", "aqua", True)),
            row(seg("其名为"), seg("[力量在他]", "aqua", True)),
            RULE,
            row(seg("🪓被动技能"), seg("[承力]", "aqua", True)),
            row(seg("每第三次命中造成一次强化打击")),
            row(seg("与"), seg("[雅斤]", "light_purple", True), seg("双持时改为每两次")),
            RULE]) + "],"
        "enchantments={smite:4,knockback:2,unbreaking:3,looting:2},"
        "attribute_modifiers=["
        '{type:"attack_damage",amount:9,operation:add_value,slot:mainhand,id:"rpg:twin/boaz/0"},'
        '{type:"attack_speed",amount:-2.2,operation:add_value,slot:mainhand,id:"rpg:twin/boaz/1"},'
        '{type:"attack_knockback",amount:0.5,operation:add_value,slot:mainhand,id:"rpg:twin/boaz/2"},'
        '{type:"attack_damage",amount:5,operation:add_value,slot:offhand,id:"rpg:twin/boaz/3"}],'
        "unbreakable={},custom_model_data={floats:[1110013.0f]},"
        "custom_data={boaz_tag:1b,sword_tag:1b}]")


def build_give():
    path = os.path.join(FUNC, "command/give/extra.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    if "雅斤" in s:
        return False
    body = [s.rstrip("\n"), "",
            "# 双生剑：雅斤（主动）与波阿斯（被动），左右手双持触发圣殿联动",
            JACHIN, BOAZ, ""]
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(body))
    return True


def build_advancement():
    wj(os.path.join(ADV, "jachin.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {"components": {
                "minecraft:food": {"nutrition": 0, "saturation": 0,
                                   "can_always_eat": True},
                "minecraft:consumable": {
                    "consume_seconds": float(CONSUME), "animation": "eat",
                    "sound": "minecraft:entity.generic.eat",
                    "has_consume_particles": True, "on_consume_effects": []},
            }}}}},
        "rewards": {"function": "rpg:item/extra/jachin_trigger"},
    })


# ---------------------------------------------------------------------------
# skills
# ---------------------------------------------------------------------------
TRIGGER = """\
# 雅斤［立柱］—— 由 rpg:advancement/item/jachin 在右键使用时触发
advancement revoke @s only rpg:item/jachin
execute if entity @s[level=..0] run playsound minecraft:entity.villager.no player @s
execute if entity @s[level=1..] run function rpg:item/extra/jachin_cast
"""

CAST = """\
# 称量［TEKEL］——"你被称在天平里，显出你的亏欠"（但以理书 5:27）
# 判决直接读 damage_action：那是 rpg:command/index 每刻已经抓好的血量，零额外开销。
xp add @s -1 levels
tag @s add rpg.jachin.cast
execute if entity @s[tag=rpg.twin] run tag @s add rpg.jachin.temple

particle dust_color_transition{{from_color:{P_PUR},to_color:{P_GLD},scale:1}} ~ ~1 ~ 0.3 0.4 0.3 0.02 12
playsound minecraft:block.enchantment_table.use player @a[distance=..16] ~ ~ ~ 1 0.7
playsound minecraft:entity.evoker.prepare_summon player @a[distance=..16] ~ ~ ~ 0.6 1.4

execute unless entity @s[tag=rpg.twin] as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run function rpg:item/extra/jachin_weigh
execute if entity @s[tag=rpg.twin] as @e[distance=0.1..9,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run function rpg:item/extra/jachin_weigh
execute if entity @s[tag=rpg.twin] run effect give @s minecraft:absorption 8 1 true
execute if entity @s[tag=rpg.twin] run playsound minecraft:block.respawn_anchor.charge player @a[distance=..16]

tag @s remove rpg.jachin.cast
tag @s remove rpg.jachin.temple
"""

STRIKE = """\
# 天平在目标头顶张开，然后落下判决。
# 生命值还厚的，削去"亏欠"；已经残破的，直接显出亏欠 —— 重创。
particle dust_color_transition{{from_color:{P_PUR},to_color:{P_GLD},scale:1}} ~ ~1.3 ~ 0.28 0.45 0.28 0.02 16
particle end_rod ~ ~1.7 ~ 0.32 0.12 0.32 0.01 6
particle minecraft:flash{{color:{J_GLD}}} ~ ~1.5 ~ 0 0 0 0 1
effect give @s minecraft:glowing 5 0 true

execute unless entity @a[tag=rpg.jachin.temple,distance=..16] if entity @s[scores={{damage_action=20..}}] run damage @s 8 minecraft:magic by @a[tag=rpg.jachin.cast,limit=1,sort=nearest]
execute unless entity @a[tag=rpg.jachin.temple,distance=..16] if entity @s[scores={{damage_action=..19}}] run damage @s 14 minecraft:magic by @a[tag=rpg.jachin.cast,limit=1,sort=nearest]
execute if entity @a[tag=rpg.jachin.temple,distance=..16] if entity @s[scores={{damage_action=30..}}] run damage @s 12 minecraft:magic by @a[tag=rpg.jachin.cast,limit=1,sort=nearest]
execute if entity @a[tag=rpg.jachin.temple,distance=..16] if entity @s[scores={{damage_action=..29}}] run damage @s 20 minecraft:magic by @a[tag=rpg.jachin.cast,limit=1,sort=nearest]

# 显出亏欠的那一下额外给个紫色爆闪与判决音
execute if entity @s[scores={{damage_action=..19}}] run particle minecraft:flash{{color:{J_PUR}}} ~ ~1.1 ~ 0 0 0 0 1
execute if entity @s[scores={{damage_action=..19}}] run particle dust_color_transition{{from_color:{P_GLD},to_color:{P_PUR},scale:2}} ~ ~1 ~ 0.4 0.5 0.4 0.06 30
execute if entity @s[scores={{damage_action=..19}}] run playsound minecraft:entity.evoker.cast_spell player @a[distance=..16] ~ ~ ~ 1 0.8
"""

TWIN = """\
# 波阿斯［承力］与双生联动［圣殿］
# 圣殿：任意一手雅斤 + 另一手波阿斯即成立
tag @a remove rpg.twin
tag @a[tag=rpg.h.jachin_tag1,tag=rpg.o.boaz_tag1] add rpg.twin
tag @a[tag=rpg.h.boaz_tag1,tag=rpg.o.jachin_tag1] add rpg.twin

# 承力：本次是否有命中（主手或副手握着波阿斯都算）
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={{boaz=0..}},tag=rpg.h.boaz_tag1] run tag @s add rpg.boaz.src
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={{boaz=0..}},tag=rpg.o.boaz_tag1] run tag @s add rpg.boaz.src
execute as @a[tag=rpg.boaz.src] run scoreboard players add @s rpg_boaz_stack 1
execute as @a[tag=rpg.boaz.src,tag=!rpg.twin,scores={{rpg_boaz_stack=3..}}] run tag @s add rpg.boaz.burst
execute as @a[tag=rpg.boaz.src,tag=rpg.twin,scores={{rpg_boaz_stack=2..}}] run tag @s add rpg.boaz.burst
execute as @a[tag=rpg.boaz.burst] run scoreboard players set @s rpg_boaz_stack 0
execute as @a[tag=rpg.boaz.burst] at @s run playsound minecraft:item.mace.smash_ground_heavy player @a[distance=..14]

# 强化打击落在刚被打中的目标上
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.boaz.burst,distance=..7] run particle dust_color_transition{{from_color:{P_TEA},to_color:{P_PNK},scale:3}} ~ ~1 ~ 0.4 0.5 0.4 0.05 40
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.boaz.burst,distance=..7] run particle sweep_attack ~ ~1 ~ 0.4 0.3 0.4 0 4
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.boaz.burst,distance=..7] run particle minecraft:flash{{color:{B_PNK}}} ~ ~1 ~ 0 0 0 0 1
execute as @e[tag=rpg.hurt,type=!player] at @s if entity @a[tag=rpg.boaz.burst,distance=..7] run damage @s 6 minecraft:player_attack by @a[tag=rpg.boaz.burst,limit=1,sort=nearest]
execute as @e[tag=rpg.hurt,type=!player] at @s if entity @a[tag=rpg.boaz.burst,distance=..7] run effect give @s minecraft:weakness 4 1 true

# 圣殿：两把剑各掠一道，紫金与青粉同时闪过
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.twin,distance=..7] run particle dust_color_transition{{from_color:{P_PUR},to_color:{P_GLD},scale:2}} ~ ~1 ~ 0.45 0.5 0.45 0.06 22
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.twin,distance=..7] run particle dust_color_transition{{from_color:{P_TEA},to_color:{P_PNK},scale:2}} ~ ~1.2 ~ 0.45 0.5 0.45 0.06 22

tag @a[tag=rpg.boaz.src] remove rpg.boaz.src
tag @a[tag=rpg.boaz.burst] remove rpg.boaz.burst
scoreboard players reset * boaz
"""


def build_functions():
    wf("item/extra/jachin_trigger.mcfunction", TRIGGER)
    palette = dict(P_PUR=P_PUR, P_GLD=P_GLD, P_TEA=P_TEA, P_PNK=P_PNK,
                   J_PUR=JACHIN_PURPLE, J_GLD=JACHIN_GOLD,
                   B_TEA=BOAZ_TEAL, B_PNK=BOAZ_PINK)
    wf("item/extra/jachin_cast.mcfunction", CAST.format(**palette))
    wf("item/extra/jachin_weigh.mcfunction", STRIKE.format(**palette))
    wf("item/extra/twin.mcfunction", TWIN.format(**palette))

    path = os.path.join(FUNC, "item/extra/skills.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    # 承力要在命中的那一刻结算，所以守卫看的是握持（主手或副手），不是命中痕迹
    TWIN_DISPATCH = (
        "execute if entity @a[tag=rpg.h.boaz_tag1] "
        "run function rpg:item/extra/twin\n"
        "execute unless entity @a[tag=rpg.h.boaz_tag1] "
        "if entity @a[tag=rpg.o.boaz_tag1] run function rpg:item/extra/twin\n")
    if "item/extra/twin" not in s:
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n" + TWIN_DISPATCH)


def add_objectives():
    path = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    block = ["scoreboard objectives add %s %s" % (o, c)
             for o, c in OBJECTIVES
             if ("scoreboard objectives add %s " % o) not in s]
    if block:
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n\n##双生剑\n" + "\n".join(block) + "\n")
    return [b.split()[3] for b in block]


def register_index():
    """Main-hand flags join the existing block; off-hand needs a new one."""
    path = os.path.join(FUNC, "command/index.mcfunction")
    lines = io.open(path, encoding="utf-8").read().split("\n")
    have = set(lines)

    clears = ["tag @a remove rpg.h.%s1" % t for t in MAINHAND]
    sets = ["execute as @a if items entity @s weapon.mainhand "
            "*[minecraft:custom_data~{%s:1b}] run tag @s add rpg.h.%s1" % (t, t)
            for t in MAINHAND]
    off = (["## off-hand item flags"]
           + ["tag @a remove rpg.o.%s1" % t for t in OFFHAND]
           + ["execute as @a if items entity @s weapon.offhand "
              "*[minecraft:custom_data~{%s:1b}] run tag @s add rpg.o.%s1" % (t, t)
              for t in OFFHAND]
           + [""])

    out, did_clear, did_set = [], False, False
    for l in lines:
        if not did_clear and l.startswith("execute as @a if items entity @s weapon.mainhand"):
            out.extend([c for c in clears if c not in have])
            did_clear = True
        if not did_set and did_clear and l.startswith("## "):
            out.extend([d for d in sets if d not in have])
            out.append("")
            if "## off-hand item flags" not in have:
                out.extend(off)
            did_set = True
        out.append(l)
    if not did_set:
        out.extend([d for d in sets if d not in have])
        if "## off-hand item flags" not in have:
            out.extend(off)
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return len([d for d in sets if d not in have]), ("## off-hand item flags" not in have)


if __name__ == "__main__":
    build_models()
    build_functions()
    build_advancement()
    print("give appended: %s" % build_give())
    print("objectives added: %s" % (", ".join(add_objectives()) or "(already present)"))
    n, off = register_index()
    print("index: %d main-hand flags added, off-hand block added: %s" % (n, off))
