# -*- coding: utf-8 -*-
"""将压制后的驱魔仪式改造成稳定度争夺型 Boss 二阶段。

本生成器必须在 add_exorcism_expansion.py 之后运行。它保留调查、七种反仪式、
四种裁决和既有掉落入口，只替换压制后的战斗循环，并为仪式器物补上真正的
右键入口。所有实体选择均限定到活动法阵及 rite_id，支持多人同时开阵。
"""

import io
import json
import os
import sys

import add_true_name_rite as rite
import add_exorcism_expansion as expansion


DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement")
LORDS = rite.LORDS

OBJECTIVES = {
    "rpg_ex_phase": "dummy",
    "rpg_ex_pressure": "dummy",
    "rpg_ex_pressure_roll": "dummy",
    "rpg_ex_wave": "dummy",
    "rpg_ex_wave_kind": "dummy",
    "rpg_ex_struggle": "dummy",
    "rpg_ex_hitcd": "dummy",
    "rpg_ex_usecd": "dummy",
    "rpg_ex_hud": "dummy",
    "rpg_ex_hud_t": "dummy",
}


def p(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep))


def read(rel):
    with io.open(p(rel), encoding="utf-8") as f:
        return f.read()


def write(rel, content):
    target = p(rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.rstrip("\n") + "\n")


def write_json(rel, value):
    target = os.path.join(ADV, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")


def raw(parts):
    return json.dumps([""] + parts, ensure_ascii=False, separators=(",", ":"))


def txt(value, colour="white", bold=False, italic=False):
    out = {"text": value, "color": colour, "italic": bool(italic)}
    if bold:
        out["bold"] = True
    return out


def add_objectives():
    rel = "command/soreboard.mcfunction"
    src = read(rel).rstrip()
    for name, criterion in OBJECTIVES.items():
        line = "scoreboard objectives add %s %s" % (name, criterion)
        if line not in src:
            src += "\n" + line
    write(rel, src)


# 巨长使用时间使 using_item 每刻可见、却不会真的吞下物品；是否消耗由法阵
# 成功接收后显式 clear，因而在法阵外右键不会损失材料。
USE_COMPONENT = (
    'food={nutrition:0,saturation:0f,can_always_eat:1b},'
    'consumable={consume_seconds:100140f,animation:"block",'
    'sound:"minecraft:block.amethyst_block.chime",has_consume_particles:false,'
    'on_consume_effects:[]},max_stack_size=64')


def interactive_item(model, name, colour, lore, data):
    return expansion.item(
        "paper", name, colour, lore, data + ",rpg_right_click:1b",
        USE_COMPONENT + ',item_model="minecraft:%s"' % model)


def build_interactive_items():
    pages = {}
    media = {}
    for q in LORDS:
        n = q["n"]
        pages[n] = interactive_item(
            "paper", "真名残页 · " + q["who"], q["colour"],
            ["右键活动法阵：展开已确证的真名", "首次展开提高 10 稳定度",
             "不会消耗，可交给其他驱魔者"],
            "holy_weapon_tag:1b,rpg_rite_page:1b,rpg_lord:%d" % n)
        model = q["item"].split(":", 1)[1]
        media[n] = interactive_item(
            model, q["medium"], q["colour"],
            ["对应%s的弱点媒介" % q["who"],
             "靠近活动法阵右键布下，提高 25 稳定度",
             "亦可丢入法阵，旧式投入仍然有效"],
            "holy_weapon_tag:1b,rpg_rite_medium:1b,rpg_medium:%db" % n)

    tools = {
        "nail": interactive_item(
            "iron_nugget", "银质圣钉", "#DCE6EE",
            ["靠近活动法阵右键钉入边界", "首次固定提高 20 稳定度；可抵消破阵"],
            "holy_weapon_tag:1b,rpg_rite_tool:1b,rpg_nail:1b"),
        "incense": interactive_item(
            "blaze_powder", "净罪香", "#E7D7B5",
            ["靠近活动法阵右键燃起净罪香", "提高 15 稳定度并净化阵内负面效果"],
            "holy_weapon_tag:1b,rpg_rite_tool:1b,rpg_incense:1b"),
        "lantern": interactive_item(
            "soul_lantern", "封魔灯", "#62D9E8",
            ["稳定度达到 100 后，在裁决法阵旁右键", "消耗灯盏并直接选择封印结局"],
            "holy_weapon_tag:1b,rpg_rite_tool:1b,rpg_lantern:1b"),
    }
    chalk_specs = {
        1: ("white_dye", "守御粉笔", "#BFD7FF", "降低稳定度损失"),
        2: ("gray_dye", "压制粉笔", "#C8B6E8", "延长恶魔技能间隔"),
        3: ("light_blue_dye", "疾行粉笔", "#7FE6FF", "强化攻击固阵效率"),
    }
    chalks = {}
    for n, (model, name, colour, effect) in chalk_specs.items():
        chalks[n] = interactive_item(
            model, name, colour,
            ["靠近活动法阵右键刻写", "首次刻写提高 10 稳定度；" + effect],
            "holy_weapon_tag:1b,rpg_rite_tool:1b,rpg_chalk:%db" % n)

    for n, stack in pages.items():
        write("inquest/give/page%d.mcfunction" % n, "give @s %s" % stack)
    for n, stack in media.items():
        write("inquest/give/medium%d.mcfunction" % n, "give @s %s 4" % stack)
    write("inquest/give/nail.mcfunction", "give @s %s 4" % tools["nail"])
    write("inquest/give/incense.mcfunction", "give @s %s 2" % tools["incense"])
    write("inquest/give/lantern.mcfunction", "give @s %s" % tools["lantern"])
    for n, stack in chalks.items():
        write("inquest/give/chalk%d.mcfunction" % n, "give @s %s 3" % stack)

    all_lines = ["function rpg:inquest/give/medium%d" % n for n in range(1, 8)]
    all_lines += [
        "function rpg:inquest/give/nail", "function rpg:inquest/give/bell",
        "function rpg:inquest/give/incense", "function rpg:inquest/give/lantern",
        "function rpg:inquest/give/strong_water"]
    all_lines += ["function rpg:inquest/give/chalk%d" % n for n in range(1, 4)]
    all_lines += ["function rpg:inquest/give/page%d" % n for n in range(1, 8)]
    write("inquest/give/all_tools.mcfunction", "\n".join(all_lines))

    # 聊天栏点击“封印”与直接右键封魔灯共用新的纸质交互物；纸本通过
    # item_model 仍显示原版灵魂灯笼，因此不会误放成方块。
    choice = read("inquest/choice/final.mcfunction")
    choice = choice.replace(
        "minecraft:soul_lantern[minecraft:custom_data~{rpg_lantern:1b}]",
        "minecraft:paper[minecraft:custom_data~{rpg_lantern:1b}]")
    write("inquest/choice/final.mcfunction", choice)
    write("inquest/choice/seal.mcfunction", """\
execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/tool/place/lantern
clear @s minecraft:paper[minecraft:custom_data~{rpg_lantern:1b}] 1
execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/seal
""")

    write_json("inquest/right_click.json", {
        "criteria": {"use": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {"predicates": {
                "minecraft:custom_data": "{rpg_right_click:1b}"}}}}},
        "rewards": {"function": "rpg:inquest/right_click"}})


def build_right_click_runtime():
    lines = [
        "advancement revoke @s only rpg:inquest/right_click",
        "scoreboard players add @s rpg_ex_usecd 0",
        "execute if score @s rpg_ex_usecd matches 1.. run return 0",
        "scoreboard players set @s rpg_ex_usecd 8",
        "tag @s add rpg.rite.user"]
    for q in LORDS:
        n = q["n"]
        lines.append(
            "execute if items entity @s weapon.mainhand minecraft:paper[minecraft:custom_data~{rpg_medium:%db}] at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,tag=!rpg.rite.medium,distance=..5,sort=nearest,limit=1,scores={rpg_ex_stage=2,rpg_dm_lord=%d}] run return run function rpg:inquest/right_click/medium%d" % (n, n, n))
        lines.append(
            "execute if items entity @s weapon.mainhand minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:%d}] at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,tag=!rpg.rite.page,distance=..5,sort=nearest,limit=1,scores={rpg_ex_stage=2,rpg_dm_lord=%d}] run return run function rpg:inquest/right_click/page%d" % (n, n, n))
    lines += [
        "execute if items entity @s weapon.mainhand minecraft:paper[minecraft:custom_data~{rpg_nail:1b}] at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,tag=!rpg.rite.nailed,distance=..5,sort=nearest,limit=1,scores={rpg_ex_stage=2}] run return run function rpg:inquest/right_click/nail",
        "execute if items entity @s weapon.mainhand minecraft:paper[minecraft:custom_data~{rpg_chalk:1b}] at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,tag=!rpg.layout.guard,distance=..5,sort=nearest,limit=1,scores={rpg_ex_stage=2,rpg_ex_slots=1..}] run return run function rpg:inquest/right_click/chalk1",
        "execute if items entity @s weapon.mainhand minecraft:paper[minecraft:custom_data~{rpg_chalk:2b}] at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,tag=!rpg.layout.suppress,distance=..5,sort=nearest,limit=1,scores={rpg_ex_stage=2,rpg_ex_slots=1..}] run return run function rpg:inquest/right_click/chalk2",
        "execute if items entity @s weapon.mainhand minecraft:paper[minecraft:custom_data~{rpg_chalk:3b}] at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,tag=!rpg.layout.haste,distance=..5,sort=nearest,limit=1,scores={rpg_ex_stage=2,rpg_ex_slots=1..}] run return run function rpg:inquest/right_click/chalk3",
        "execute if items entity @s weapon.mainhand minecraft:paper[minecraft:custom_data~{rpg_incense:1b}] at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..5,sort=nearest,limit=1,scores={rpg_ex_stage=2,rpg_ex_toolcd=0}] run return run function rpg:inquest/right_click/incense",
        "execute if items entity @s weapon.mainhand minecraft:paper[minecraft:custom_data~{rpg_lantern:1b}] at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..5,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run return run function rpg:inquest/right_click/lantern",
        "tag @s remove rpg.rite.user"]
    write("inquest/right_click.mcfunction", "\n".join(lines))

    for n in range(1, 8):
        write("inquest/right_click/medium%d.mcfunction" % n, """\
function rpg:inquest/tool/place/medium%(n)d
tag @s add rpg.rite.medium
scoreboard players add @s rpg_ex_stab 25
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
clear @a[tag=rpg.rite.user,distance=..6,limit=1] minecraft:paper[minecraft:custom_data~{rpg_medium:%(n)db}] 1
scoreboard players add @a[tag=rpg.rite.user,distance=..6,limit=1] rpg_ex_xp 6
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/stability/show
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
""" % {"n": n, "msg": raw([txt("[弱点媒介] ", LORDS[n - 1]["colour"], True),
                                      txt(LORDS[n - 1]["medium"] + "已布入法阵。", "gray")])})
        write("inquest/right_click/page%d.mcfunction" % n, """\
function rpg:inquest/tool/place/page
tag @s add rpg.rite.page
scoreboard players add @s rpg_ex_stab 10
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
scoreboard players add @a[tag=rpg.rite.user,distance=..6,limit=1] rpg_ex_xp 2
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/stability/show
""")

    write("inquest/right_click/nail.mcfunction", """\
function rpg:inquest/tool/place/nail
tag @s add rpg.rite.nailed
scoreboard players add @s rpg_ex_stab 20
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
clear @a[tag=rpg.rite.user,distance=..6,limit=1] minecraft:paper[minecraft:custom_data~{rpg_nail:1b}] 1
scoreboard players add @a[tag=rpg.rite.user,distance=..6,limit=1] rpg_ex_xp 3
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/stability/show
playsound minecraft:block.anvil.place player @a[distance=..16] ~ ~ ~ 0.7 1.8
""")

    for n, key in ((1, "guard"), (2, "suppress"), (3, "haste")):
        write("inquest/right_click/chalk%d.mcfunction" % n, """\
function rpg:inquest/tool/place/chalk%(n)d
tag @s add rpg.layout.%(key)s
scoreboard players remove @s rpg_ex_slots 1
scoreboard players add @s rpg_ex_stab 10
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
clear @a[tag=rpg.rite.user,distance=..6,limit=1] minecraft:paper[minecraft:custom_data~{rpg_chalk:%(n)db}] 1
scoreboard players add @a[tag=rpg.rite.user,distance=..6,limit=1] rpg_ex_xp 2
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/stability/show
playsound minecraft:block.calcite.place player @a[distance=..16] ~ ~ ~ 0.8 1.4
""" % {"n": n, "key": key})

    write("inquest/right_click/incense.mcfunction", """\
function rpg:inquest/tool/place/incense
scoreboard players set @s rpg_ex_toolcd 200
scoreboard players add @s rpg_ex_stab 15
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
clear @a[tag=rpg.rite.user,distance=..6,limit=1] minecraft:paper[minecraft:custom_data~{rpg_incense:1b}] 1
effect clear @a[distance=..6,gamemode=!spectator] minecraft:slowness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:weakness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:blindness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:darkness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:nausea
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/stability/show
particle campfire_cosy_smoke ~ ~0.4 ~ 1.2 0.3 1.2 0.03 35 force
""")

    write("inquest/right_click/lantern.mcfunction", """\
function rpg:inquest/tool/place/lantern
clear @a[tag=rpg.rite.user,distance=..6,limit=1] minecraft:paper[minecraft:custom_data~{rpg_lantern:1b}] 1
tag @a[tag=rpg.rite.user,distance=..6] add rpg.rite.chooser
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/outcome/seal
""")


def build_phase2_entry():
    write("inquest/phase2/shockwave.mcfunction", """\
tag @s add rpg.phase2.source
effect give @a[distance=..10,gamemode=!spectator,gamemode=!creative] minecraft:resistance 2 4 true
execute as @a[distance=0.25..10,gamemode=!spectator,gamemode=!creative] at @e[type=minecraft:vindicator,tag=rpg.phase2.source,limit=1] facing entity @s feet run tp @s ^ ^0.35 ^10
effect give @a[distance=..11,gamemode=!spectator,gamemode=!creative] minecraft:slow_falling 3 0 true
particle explosion_emitter ~ ~1 ~ 0 0 0 0 1 force
particle gust_emitter_large ~ ~1 ~ 0 0 0 0 1 force
particle dust{color:[1.0,0.84,0.32],scale:2.4} ~ ~0.6 ~ 5.5 0.2 5.5 0.03 130 force
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..32] ~ ~ ~ 1.2 0.62
tag @s remove rpg.phase2.source
""")
    write("inquest/phase2/tick.mcfunction", """\
scoreboard players remove @s rpg_ex_phase 1
execute if score @s rpg_ex_phase matches 20 run function rpg:inquest/phase2/warning
execute if score @s rpg_ex_phase matches ..0 run function rpg:inquest/phase2/pressure
""")
    write("inquest/phase2/warning.mcfunction", """\
title @a[distance=..24,gamemode=!spectator] times 0 25 5
title @a[distance=..24,gamemode=!spectator] subtitle ["",{"text":"罪域正在覆盖战场 · 靠近法阵","color":"#FFF2A8","bold":true,"italic":false}]
playsound minecraft:block.respawn_anchor.ambient hostile @a[distance=..28] ~ ~ ~ 1 0.5
particle trial_spawner_detection_ominous ~ ~1 ~ 7 0.5 7 0.02 80 force
""")
    dispatch = [
        "execute store result score @s rpg_ex_pressure_roll run random value 1..3",
        "execute store result score @s rpg_ex_pressure run random value 280..360",
        "function rpg:inquest/phase2/pressure_core"]
    for q in LORDS:
        for variant in range(1, 4):
            dispatch.append(
                "execute if score @s rpg_dm_lord matches %(n)d if score @s rpg_ex_pressure_roll matches %(v)d run function rpg:inquest/phase2/pressure/%(n)d_%(v)d" %
                {"n": q["n"], "v": variant})
    write("inquest/phase2/pressure.mcfunction", "\n".join(dispatch))
    write("inquest/phase2/pressure_tick.mcfunction", """\
scoreboard players remove @s rpg_ex_pressure 1
execute if score @s rpg_ex_pressure matches 40 run function rpg:inquest/phase2/pressure_warning
execute if score @s rpg_ex_pressure matches ..0 run function rpg:inquest/phase2/pressure
""")
    warning_dispatch = []
    for q in LORDS:
        warning_dispatch.append(
            "execute if score @s rpg_dm_lord matches %(n)d run function rpg:inquest/phase2/warning/%(n)d" % q)
    write("inquest/phase2/pressure_warning.mcfunction", "\n".join(warning_dispatch))
    write("inquest/phase2/pressure_core.mcfunction", """\
function rpg:inquest/stability/hit10
particle trial_omen ~ ~0.45 ~ 7 0.25 7 0.045 70 force
particle large_smoke ~ ~0.65 ~ 9 0.5 9 0.055 55 force
particle reverse_portal ~ ~1.1 ~ 11 0.9 11 0.07 75 force
particle explosion_emitter ~ ~0.4 ~ 0 0 0 0 1 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle trial_omen ~ ~1 ~ 0.45 0.7 0.45 0.04 12 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 6 minecraft:magic
playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..36] ~ ~ ~ 1.1 0.65
playsound minecraft:entity.generic.explode hostile @a[distance=..32] ~ ~ ~ 0.9 0.72
""")

    # 每柱三套真正可轮换的压场技。effects 只作用在法阵四格安全圈外；extra
    # 用于火焰、经验税、位移等不能由普通状态表达的罪性机制。
    variants = {
        1: [
            ("王冠坠落", "dragon_breath", 8, [("levitation", 4, 1), ("weakness", 8, 1)], []),
            ("蛇庭敕令", "enchanted_hit", 7, [("poison", 6, 0), ("slowness", 7, 1)], [
                "summon minecraft:evoker_fangs ~6 ~ ~ {Tags:[\"rpg.rite.pressure\"]}",
                "summon minecraft:evoker_fangs ~-6 ~ ~ {Tags:[\"rpg.rite.pressure\"]}",
                "summon minecraft:evoker_fangs ~ ~ ~6 {Tags:[\"rpg.rite.pressure\"]}",
                "summon minecraft:evoker_fangs ~ ~ ~-6 {Tags:[\"rpg.rite.pressure\"]}"]),
            ("高座拒斥", "end_rod", 10, [("weakness", 10, 2), ("glowing", 8, 0)], [
                "execute as @a[distance=4.01..9,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^0.2 ^-2.5"]),
        ],
        2: [
            ("妒海沉城", "splash", 8, [("slowness", 9, 3), ("mining_fatigue", 9, 1)], []),
            ("逆潮回卷", "bubble", 7, [("nausea", 7, 0), ("weakness", 8, 1)], [
                "execute as @a[distance=8..20,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^ ^2"]),
            ("海渊重压", "nautilus", 10, [("darkness", 7, 0), ("slowness", 8, 4)], [
                "execute as @a[distance=7..24,gamemode=!spectator,gamemode=!creative] run damage @s 5 minecraft:drown"]),
        ],
        3: [
            ("无刻停摆", "ash", 7, [("slowness", 10, 4), ("mining_fatigue", 10, 2)], []),
            ("死寂收割", "sculk_soul", 9, [("wither", 6, 0), ("weakness", 8, 1)], []),
            ("深渊张口", "large_smoke", 11, [("darkness", 9, 0), ("levitation", 3, 0)], [
                "execute as @a[distance=8..24,gamemode=!spectator,gamemode=!creative] run damage @s 4 minecraft:magic"]),
        ],
        4: [
            ("腐宴开席", "spore_blossom_air", 8, [("hunger", 12, 3), ("poison", 7, 0)], []),
            ("万蝇蔽日", "infested", 7, [("blindness", 5, 0), ("weakness", 9, 2)], []),
            ("饥啮回廊", "item{item:{id:\"minecraft:poisonous_potato\"}}", 10, [("nausea", 9, 0), ("hunger", 10, 4)], [
                "execute as @a[distance=6..24,gamemode=!spectator,gamemode=!creative] run damage @s 5 minecraft:magic"]),
        ],
        5: [
            ("怒潮焚界", "flame", 9, [("weakness", 8, 1)], [
                "execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run data merge entity @s {Fire:80s}"]),
            ("血猎标记", "damage_indicator", 10, [("glowing", 10, 0), ("wither", 5, 0)], [
                "execute as @a[distance=8..24,gamemode=!spectator,gamemode=!creative] run damage @s 5 minecraft:indirect_magic"]),
            ("暴怒裂阵", "gust_emitter_small", 12, [("slowness", 6, 1)], [
                "execute as @a[distance=4.01..10,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^0.3 ^-3"]),
        ],
        6: [
            ("紫宴朝圣", "witch", 7, [("nausea", 9, 0), ("blindness", 5, 0)], []),
            ("顾盼夺心", "heart", 9, [("slowness", 8, 3), ("weakness", 9, 2)], [
                "execute as @a[distance=6..18,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^ ^-1.5"]),
            ("欲障迷宫", "portal", 10, [("darkness", 7, 0), ("levitation", 3, 0), ("nausea", 8, 0)], []),
        ],
        7: [
            ("黄金牢城", "wax_on", 8, [("slowness", 10, 4), ("mining_fatigue", 10, 2)], []),
            ("复利追征", "trial_omen", 9, [("weakness", 9, 2), ("hunger", 9, 2)], [
                "experience add @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] -20 points"]),
            ("什一血税", "totem_of_undying", 11, [("glowing", 8, 0)], [
                "execute as @a[distance=5..24,gamemode=!spectator,gamemode=!creative] run damage @s 6 minecraft:magic"]),
        ],
    }
    # 复用罪器、史诗武器与恶魔大招已经形成的视觉语言：双色渐变负责轮廓，
    # signature 表达材质，hit 只在玩家身上做命中反馈，finisher 用于终末波。
    themes = {
        1: dict(start="[0.19,0.85,0.49]", end="[0.0,0.18,0.07]",
                signature="end_rod", hit="enchanted_hit", finisher="dragon_breath",
                alt_signature="dragon_breath", alt_hit="crit", alt_finisher="reverse_portal",
                sound="minecraft:entity.evoker.prepare_attack"),
        2: dict(start="[0.24,0.66,0.91]", end="[0.02,0.09,0.18]",
                signature="bubble_column_up", hit="bubble_pop", finisher="nautilus",
                alt_signature="splash", alt_hit="enchanted_hit", alt_finisher="splash",
                sound="minecraft:entity.guardian.attack"),
        3: dict(start="[0.57,0.57,0.61]", end="[0.04,0.03,0.07]",
                signature="soul", hit="sculk_charge_pop", finisher="reverse_portal",
                alt_signature="sculk_soul", alt_hit="damage_indicator", alt_finisher="soul_fire_flame",
                sound="minecraft:entity.warden.sonic_boom"),
        4: dict(start="[0.72,0.78,0.29]", end="[0.14,0.17,0.03]",
                signature="mycelium", hit="infested", finisher="ash",
                alt_signature="spore_blossom_air", alt_hit="item_slime", alt_finisher="spore_blossom_air",
                sound="minecraft:entity.spider.ambient"),
        5: dict(start="[0.89,0.30,0.30]", end="[0.24,0.0,0.04]",
                signature="soul_fire_flame", hit="damage_indicator", finisher="sweep_attack",
                alt_signature="flame", alt_hit="crit", alt_finisher="flame",
                sound="minecraft:entity.ravager.roar"),
        6: dict(start="[0.75,0.42,0.91]", end="[0.12,0.0,0.18]",
                signature="reverse_portal", hit="heart", finisher="portal",
                alt_signature="witch", alt_hit="enchanted_hit", alt_finisher="witch",
                sound="minecraft:entity.illusioner.prepare_mirror"),
        7: dict(start="[0.89,0.73,0.23]", end="[0.20,0.10,0.0]",
                signature="end_rod", hit="firework", finisher="totem_of_undying",
                alt_signature="wax_on", alt_hit="crit", alt_finisher="wax_on",
                sound="minecraft:block.amethyst_block.resonate"),
    }
    for q in LORDS:
        n = q["n"]
        theme = themes[n]
        transition = "dust_color_transition{from_color:%s,to_color:%s,scale:%%s}" % (
            theme["start"], theme["end"])
        warning = [
            "title @a[distance=..24,gamemode=!spectator] times 0 22 4",
            "title @a[distance=..24,gamemode=!spectator] subtitle " + raw([
                txt("%s · 罪域聚能" % q["who"], q["colour"], True),
                txt(" · 退入法阵四格庇护圈", "#FFF2A8")]),
            "particle %s ~ ~0.25 ~ 5 0.08 5 0.018 52 force" % (transition % "1.4"),
            "particle %s ~ ~0.35 ~ 10 0.12 10 0.035 82 force" % (transition % "2.1"),
            "particle %s ~ ~1.0 ~ 7 0.8 7 0.035 36 force" % theme["signature"],
            "particle trial_spawner_detection_ominous ~ ~0.2 ~ 11 0.05 11 0.012 48 force",
            "playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 0.9 0.58"]
        write("inquest/phase2/warning/%d.mcfunction" % n, "\n".join(warning))

    for q in LORDS:
        n = q["n"]
        theme = themes[n]
        transition = "dust_color_transition{from_color:%s,to_color:%s,scale:%%s}" % (
            theme["start"], theme["end"])
        colour = q["colour"].lstrip("#")
        flash_colour = int(colour, 16)
        for index, (name, particle, damage, effects, extra) in enumerate(variants[n], 1):
            signature_particle = (theme["alt_signature"] if particle == theme["signature"]
                                  else theme["signature"])
            hit_particle = theme["alt_hit"] if particle == theme["hit"] else theme["hit"]
            finisher_particle = (theme["alt_finisher"] if particle == theme["finisher"]
                                 else theme["finisher"])
            body = [
                "scoreboard players set @s rpg_ex_wave 20",
                "scoreboard players set @s rpg_ex_wave_kind %d" % (n * 10 + index),
                "particle flash{color:%d} ~ ~1.2 ~ 0 0 0 0 1 force" % flash_colour,
                "particle %s ~ ~0.25 ~ 5 0.08 5 0.025 82 force" % (transition % "1.8"),
                "particle %s ~ ~0.50 ~ 11 0.14 11 0.045 116 force" % (transition % "2.5"),
                "particle %s ~ ~1.15 ~ 12 1.8 12 0.07 138 force" % particle,
                "particle %s ~ ~1.55 ~ 8 1.2 8 0.045 58 force" % signature_particle,
                "tellraw @a[distance=..24,gamemode=!spectator] " + raw([
                    txt("[罪域·%s] " % q["who"], q["colour"], True),
                    txt(name + " · 三重罪域爆发，退入法阵四格庇护圈。", "gray")]),
                "execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle %s ~ ~1 ~ 0.65 0.95 0.65 0.06 22 force" % particle,
                "execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle %s ~ ~1 ~ 0.38 0.60 0.38 0.04 12 force" % hit_particle,
                "execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s %d minecraft:magic" % damage,
                "playsound %s hostile @a[distance=..32] ~ ~ ~ 0.95 %.2f" %
                (theme["sound"], 0.72 + index * 0.08)]
            for effect, seconds, amp in effects:
                body.append("effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:%s %d %d true" % (effect, seconds, amp))
            body.extend(extra)
            write("inquest/phase2/pressure/%d_%d.mcfunction" % (n, index), "\n".join(body))

            pulse = [
                "execute if score @s rpg_ex_wave matches 12 run particle %s ~ ~0.35 ~ 14 0.15 14 0.05 108 force" % (transition % "2.2"),
                "execute if score @s rpg_ex_wave matches 12 run particle %s ~ ~1.1 ~ 14 1.6 14 0.08 94 force" % particle,
                "execute if score @s rpg_ex_wave matches 12 run particle %s ~ ~1.5 ~ 9 1.0 9 0.035 42 force" % signature_particle,
                "execute if score @s rpg_ex_wave matches 12 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle %s ~ ~1 ~ 0.42 0.65 0.42 0.05 14 force" % hit_particle,
                "execute if score @s rpg_ex_wave matches 12 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 2 minecraft:magic",
                "execute if score @s rpg_ex_wave matches 12 run playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..32] ~ ~ ~ 0.8 0.68",
                "execute if score @s rpg_ex_wave matches 1 run particle flash{color:%d} ~ ~1.2 ~ 0 0 0 0 1 force" % flash_colour,
                "execute if score @s rpg_ex_wave matches 1 run particle %s ~ ~0.35 ~ 17 0.2 17 0.06 142 force" % (transition % "3.0"),
                "execute if score @s rpg_ex_wave matches 1 run particle %s ~ ~1.3 ~ 18 2.2 18 0.10 126 force" % particle,
                "execute if score @s rpg_ex_wave matches 1 run particle %s ~ ~1.4 ~ 12 1.4 12 0.06 62 force" % finisher_particle,
                "execute if score @s rpg_ex_wave matches 1 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle %s ~ ~1 ~ 0.68 0.9 0.68 0.07 20 force" % hit_particle,
                "execute if score @s rpg_ex_wave matches 1 as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s %d minecraft:magic" % max(4, damage // 2),
                "execute if score @s rpg_ex_wave matches 1 run playsound %s hostile @a[distance=..36] ~ ~ ~ 1.2 0.62" % theme["sound"]]
            write("inquest/phase2/wave/%d_%d.mcfunction" % (n, index), "\n".join(pulse))

    wave_dispatch = []
    for q in LORDS:
        for index in range(1, 4):
            wave_dispatch.append(
                "execute if score @s rpg_ex_wave_kind matches %d run function rpg:inquest/phase2/wave/%d_%d" %
                (q["n"] * 10 + index, q["n"], index))
    write("inquest/phase2/wave_dispatch.mcfunction", "\n".join(wave_dispatch))
    write("inquest/phase2/wave_tick.mcfunction", """\
scoreboard players remove @s rpg_ex_wave 1
execute if score @s rpg_ex_wave matches 12 run function rpg:inquest/phase2/wave_dispatch
execute if score @s rpg_ex_wave matches 1 run function rpg:inquest/phase2/wave_dispatch
""")


def build_stability_loop():
    # 法阵是稳定度的唯一权威来源；玩家只保存两刻的 HUD 镜像。
    write("inquest/stability/show.mcfunction", """\
scoreboard players operation @a[distance=..24,gamemode=!spectator] rpg_ex_hud = @s rpg_ex_stab
scoreboard players set @a[distance=..24,gamemode=!spectator] rpg_ex_hud_t 3
""")
    for amount in (5, 10, 15, 20, 25):
        guard = max(2, (amount * 2 + 4) // 5)
        write("inquest/stability/hit%d.mcfunction" % amount, """\
scoreboard players remove @s rpg_ex_stab %(amount)d
execute if entity @s[tag=rpg.layout.guard] run scoreboard players add @s rpg_ex_stab %(guard)d
execute if entity @a[distance=..10,gamemode=!spectator,scores={rpg_ex_path=2,rpg_ex_lvl=2..}] run scoreboard players add @s rpg_ex_stab 4
execute if score @s rpg_ex_stab matches ..0 run scoreboard players set @s rpg_ex_stab 0
function rpg:inquest/stability/show
""" % {"amount": amount, "guard": guard})
    write("inquest/stability/add2.mcfunction", """\
scoreboard players add @s rpg_ex_stab 2
execute if entity @s[tag=rpg.layout.haste] run scoreboard players add @s rpg_ex_stab 1
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
function rpg:inquest/stability/show
particle end_rod ~ ~0.7 ~ 0.25 0.15 0.25 0.02 4 normal
""")
    write("inquest/boss_hit.mcfunction", """\
scoreboard players set @s rpg_ex_hitcd 5
execute on attacker run scoreboard players add @s rpg_ex_xp 1
tag @s add rpg.rite.subject
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.rite.subject,limit=1] rpg_rite_id run function rpg:inquest/stability/add2
tag @s remove rpg.rite.subject
""")
    # 受缚恶魔属于法阵中心的“被镇压目标”，不参与普通击退。抗性修饰阻止
    # 客户端产生明显击退，逐 tick 回正则处理爆炸、活塞等非常规位移来源。
    write("inquest/phase2/lock_boss.mcfunction", """\
execute unless entity @s[tag=rpg.rite.locked] run attribute @s minecraft:knockback_resistance modifier remove rpg:rite_lock
execute unless entity @s[tag=rpg.rite.locked] run attribute @s minecraft:knockback_resistance modifier add rpg:rite_lock 1 add_value
tag @s add rpg.rite.locked
data merge entity @s {Motion:[0d,0d,0d],FallDistance:0f,NoAI:1b}
tag @s add rpg.rite.lock.source
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.rite.lock.source,limit=1] rpg_rite_id at @s run tp @e[type=minecraft:vindicator,tag=rpg.rite.lock.source,limit=1] ~ ~ ~
tag @s remove rpg.rite.lock.source
""")
    write("inquest/bound_tick.mcfunction", """\
scoreboard players add @s rpg_ex_hitcd 0
execute if score @s rpg_ex_hitcd matches 1.. run scoreboard players remove @s rpg_ex_hitcd 1
execute store result score @s rpg_ex_hp run data get entity @s Health 1
execute if score @s rpg_ex_hp matches ..419 if score @s rpg_ex_hitcd matches ..0 run function rpg:inquest/boss_hit
data merge entity @s {Health:420f,CustomNameVisible:1b}
effect give @s minecraft:resistance 2 3 true
effect give @s minecraft:slowness 2 255 true
effect give @s minecraft:glowing 2 0 true
effect clear @s minecraft:invisibility
function rpg:inquest/phase2/lock_boss
particle enchant ~ ~1 ~ 0.55 0.9 0.55 0.04 2 normal
scoreboard players set #anchor_found rpg_ex_tmp 0
tag @s add rpg.rite.subject
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.rite.subject,limit=1] rpg_rite_id run scoreboard players set #anchor_found rpg_ex_tmp 1
tag @s remove rpg.rite.subject
execute if score #anchor_found rpg_ex_tmp matches 0 run function rpg:inquest/fail
""")
    write("inquest/struggle_tick.mcfunction", """\
scoreboard players remove @s rpg_ex_struggle 1
execute if score @s rpg_ex_struggle matches ..0 run function rpg:inquest/struggle
""")
    write("inquest/struggle.mcfunction", """\
execute store result score @s rpg_ex_struggle run random value 120..180
function rpg:inquest/stability/hit5
particle gust ~ ~0.8 ~ 2.5 0.35 2.5 0.08 45 force
playsound minecraft:entity.ravager.roar hostile @a[distance=..24] ~ ~ ~ 0.65 0.55
tellraw @a[distance=..18,gamemode=!spectator] ["",{"text":"[恶魔挣脱] ","color":"#FF6B5E","bold":true,"italic":false},{"text":"法阵边界承受冲击，稳定度下降。","color":"gray","italic":false}]
""")
    write("inquest/counter/cast.mcfunction", """\
function rpg:inquest/stability/hit5
execute if entity @s run function rpg:inquest/counter/dispatch
""")
    write("inquest/counter/tick.mcfunction", """\
execute if score @s rpg_ex_kind matches 1 run return run function rpg:inquest/counter/lucifer_wait
execute if score @s rpg_ex_kind matches 2 run return run function rpg:inquest/counter/leviathan_wait
execute if score @s rpg_ex_kind matches 7 run return 0
scoreboard players remove @s rpg_ex_counter 1
execute if score @s rpg_ex_counter matches ..0 run function rpg:inquest/counter/cast
""")
    # 怠惰原本只延长已废弃的宣判计时；二阶段改为直接拖损稳定度。
    src = read("inquest/counter/start3.mcfunction")
    if "stability/hit10" not in src:
        src = "function rpg:inquest/stability/hit10\n" + src
    write("inquest/counter/start3.mcfunction", src)


def build_anchor_state_machine():
    for q in LORDS:
        n = q["n"]
        rel = "inquest/anchor_bind/%d.mcfunction" % n
        src = read(rel)
        src = src.replace("scoreboard players set @s rpg_ex_stab 100",
                          "scoreboard players set @s rpg_ex_stab 50")
        src = src.replace("scoreboard players set @s rpg_totem 800",
                          "scoreboard players set @s rpg_totem 2400")
        additions = [
            "scoreboard players set @s rpg_ex_phase 40",
            "scoreboard players set @s rpg_ex_pressure 0",
            "scoreboard players set @s rpg_ex_wave 0",
            "scoreboard players set @s rpg_ex_wave_kind 0",
            "execute store result score @s rpg_ex_struggle run random value 120..180"]
        for line in additions:
            if line not in src:
                src = src.rstrip() + "\n" + line
        write(rel, src)

        rel = "inquest/bind/%d.mcfunction" % n
        src = read(rel)
        marker = "tag @s remove rpg.rite.subject"
        if "phase2/shockwave" not in src:
            src = src.replace(marker, marker + "\nfunction rpg:inquest/phase2/shockwave", 1)
        src = src.replace("Ⅱ · 显　形", "Ⅱ · 镇　魔")
        src = src.replace("向图腾投入弱点媒介：", "稳定度 50 / 100 · 右键布下弱点媒介：")
        write(rel, src)

        # 丢入式媒介继续兼容，但不再跳过二阶段。
        write("inquest/offer/%d.mcfunction" % n, """\
function rpg:inquest/tool/place/medium%(n)d
function rpg:inquest/consume_offer
tag @s add rpg.rite.medium
scoreboard players add @s rpg_ex_stab 25
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
scoreboard players add @a[distance=..8,gamemode=!spectator] rpg_ex_xp 6
function rpg:inquest/stability/show
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
playsound minecraft:block.enchantment_table.use player @a[distance=..20] ~ ~ ~ 1 0.7
""" % {"n": n, "msg": raw([txt("[弱点媒介] ", q["colour"], True),
                                      txt(q["medium"] + "已布入法阵，稳定度上升。", "gray")])})
        # 旧式投入同时识别原版媒介和右键版定制媒介。
        write("inquest/scan/%d.mcfunction" % n, """\
execute as @e[type=minecraft:item,distance=..4] if items entity @s contents %(item)s run tag @s add rpg.rite.offer
execute as @e[type=minecraft:item,distance=..4] if items entity @s contents minecraft:paper[minecraft:custom_data~{rpg_medium:%(n)db}] run tag @s add rpg.rite.offer
execute if entity @e[type=minecraft:item,tag=rpg.rite.offer,distance=..4,limit=1] run return run function rpg:inquest/offer/%(n)d
tag @s remove rpg.rite.anchor.active
""" % {"item": q["item"], "n": n})

    write("inquest/anchor_tick.mcfunction", """\
scoreboard players set #bound_found rpg_ex_tmp 0
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run scoreboard players set #bound_found rpg_ex_tmp 1
execute if score #bound_found rpg_ex_tmp matches 0 run return run function rpg:inquest/anchor_orphan
scoreboard players remove @s rpg_totem 1
execute if score @s rpg_totem matches ..0 run return run function rpg:inquest/anchor_timeout
execute if score @s rpg_ex_toolcd matches 1.. run scoreboard players remove @s rpg_ex_toolcd 1
function rpg:inquest/stability/show
particle dust{color:[1.0,0.91,0.52],scale:0.7} ~ ~0.75 ~ 0.28 0.35 0.28 0.01 1 normal
execute if score @s rpg_ex_stage matches 2 run function rpg:inquest/tool/scan
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_phase matches 1.. run function rpg:inquest/phase2/tick
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_phase matches ..0 run function rpg:inquest/phase2/pressure_tick
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_wave matches 1.. run function rpg:inquest/phase2/wave_tick
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_phase matches ..0 run function rpg:inquest/counter/tick
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_phase matches ..0 run function rpg:inquest/struggle_tick
execute if score @s rpg_ex_stab matches ..0 run return run function rpg:inquest/anchor_collapse
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_stab matches 100.. run return run function rpg:inquest/start_verdict
execute if score @s rpg_ex_ransom matches 1.. run return run function rpg:inquest/counter/mammon_wait
execute if score @s rpg_ex_stage matches 2 run return run function rpg:inquest/anchor_stage2
execute if score @s rpg_ex_stage matches 4 run return run function rpg:inquest/anchor_stage4
tag @s remove rpg.rite.anchor.active
""")
    stage2 = []
    for q in LORDS:
        stage2.append("execute unless entity @s[tag=rpg.rite.medium] if score @s rpg_dm_lord matches %(n)d run return run function rpg:inquest/scan/%(n)d" % q)
    stage2 += [
        "execute if score @s rpg_totem matches 2300 run tellraw @a[distance=..18,gamemode=!spectator] [\"\",{\"text\":\"[镇魔二阶段] \",\"color\":\"#FFF2A8\",\"bold\":true,\"italic\":false},{\"text\":\"攻击恶魔与右键布置仪式器物可提高稳定度；技能和挣脱会令其下降。\",\"color\":\"gray\",\"italic\":false}]",
        "tag @s remove rpg.rite.anchor.active"]
    write("inquest/anchor_stage2.mcfunction", "\n".join(stage2))

    # 归零及任意仪式失败都直接进入“消灭”战斗，不再回到普通压制阶段。
    write("inquest/anchor_collapse.mcfunction", """\
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[仪式失败] ","color":"dark_red","bold":true,"italic":false},{"text":"稳定度归零，裁决被迫写为——消灭。","color":"gray","italic":false}]
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/outcome/eliminate_boss
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..12]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14]
function rpg:inquest/tool/cleanup
particle explosion_emitter ~ ~0.8 ~ 0 0 0 0 1 force
playsound minecraft:block.beacon.deactivate hostile @a[distance=..28] ~ ~ ~ 1 0.45
kill @s
""")
    write("inquest/fail.mcfunction", """\
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[仪式失败] ","color":"dark_red","bold":true,"italic":false},{"text":"法阵失去约束，裁决被迫进入消灭步骤。","color":"gray","italic":false}]
function rpg:inquest/outcome/eliminate_boss
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..12]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14]
""")
    src = read("inquest/outcome/eliminate_boss.mcfunction")
    src = src.replace("Health:560f", "Health:700f").replace("Health:500f", "Health:640f")
    src = src.replace("560 生命", "700 生命")
    unlock = "attribute @s minecraft:knockback_resistance modifier remove rpg:rite_lock\ntag @s remove rpg.rite.locked\ndata merge entity @s {NoAI:0b,Motion:[0d,0d,0d]}"
    if "modifier remove rpg:rite_lock" not in src:
        src = src.replace("tag @s remove rpg.exorcism.bound", unlock + "\ntag @s remove rpg.exorcism.bound", 1)
    write("inquest/outcome/eliminate_boss.mcfunction", src)


def build_hud():
    # 玩家镜像自然过期，避免离开法阵后残留最后一个数字。
    player = read("inquest/player_tick.mcfunction")
    hook = "scoreboard players add @s rpg_ex_hud_t 0\nexecute if score @s rpg_ex_hud_t matches 1.. run scoreboard players remove @s rpg_ex_hud_t 1\nscoreboard players add @s rpg_ex_usecd 0\nexecute if score @s rpg_ex_usecd matches 1.. run scoreboard players remove @s rpg_ex_usecd 1\n"
    if "rpg_ex_hud_t matches 1.." not in player:
        player = hook + player
    write("inquest/player_tick.mcfunction", player)

    # 11 档清晰条形 + 精确数值。活动仪式时稳定度拥有下层 HUD 的最高优先级，
    # 上层恶魔出招提示仍通过既有 combat_prompt 字体合成。
    lines = [
        "scoreboard players set @s rpg_hud_on 1",
        "scoreboard players operation @s rpg_hud_p = @s rpg_ex_hud",
        "scoreboard players operation @s rpg_hud_p /= #hud_seg rpg_hud"]
    for n in range(11):
        filled = "▰" * n
        empty = "▱" * (10 - n)
        colour = "#FF6B5E" if n <= 2 else ("#FFF2A8" if n <= 7 else "#62D9E8")
        component = ["", txt("法阵 ", "#D6C27A", True), txt(filled, colour),
                     txt(empty, "#46484F"), txt("  "),
                     {"score": {"name": "@s", "objective": "rpg_ex_hud"},
                      "color": colour, "bold": True}, txt(" / 100", "gray")]
        lines.append("execute if score @s rpg_hud_p matches %d run data modify storage rpg:hud d set value '%s'" %
                     (n, json.dumps(component, ensure_ascii=False, separators=(",", ":"))))
    write("inquest/hud/stability.mcfunction", "\n".join(lines))
    write("inquest/hud/actionbar.mcfunction", """\
data modify storage rpg:hud a set value '{"text":""}'
data modify storage rpg:hud b set value '{"text":""}'
data modify storage rpg:hud c set value '{"text":""}'
data modify storage rpg:hud d set value '{"text":""}'
function rpg:inquest/hud/stability
execute if score @s rpg_hud_dmt matches 1.. run return run function rpg:hud/demon/render with storage rpg:hud
function rpg:hud/render with storage rpg:hud
""")

    hud = read("hud/hud.mcfunction")
    needle = "execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=1}]"
    route = "execute if entity @s[scores={rpg_ex_hud_t=1..}] run return run function rpg:inquest/hud/actionbar\n\n"
    if route.strip() not in hud:
        hud = hud.replace(needle, route + needle, 1)
    write("hud/hud.mcfunction", hud)

    status = read("hud/status.mcfunction")
    reset_d = "data modify storage rpg:hud d set value '{\"text\":\"\"}'"
    if reset_d not in status:
        status = status.replace(
            "data modify storage rpg:hud c set value '{\"text\":\"\"}'",
            "data modify storage rpg:hud c set value '{\"text\":\"\"}'\n" + reset_d, 1)
    write("hud/status.mcfunction", status)

    render = read("hud/render.mcfunction").replace("$(a),$(b),$(c)]", "$(a),$(b),$(c),$(d)]")
    write("hud/render.mcfunction", render)
    demon_dir = os.path.join(FUNC, "hud", "demon")
    for name in os.listdir(demon_dir):
        if name.startswith("r") and name.endswith(".mcfunction"):
            rel = "hud/demon/" + name
            src = read(rel).replace("$(a),$(b),$(c)]", "$(a),$(b),$(c),$(d)]")
            write(rel, src)


def validate():
    board = read("command/soreboard.mcfunction")
    for name, criterion in OBJECTIVES.items():
        if board.count("scoreboard objectives add %s %s" % (name, criterion)) != 1:
            raise RuntimeError("phase2 objective mismatch: " + name)
    if "rpg_ex_stab 50" not in read("inquest/anchor_bind/1.mcfunction"):
        raise RuntimeError("stability does not start at 50")
    if "phase2/shockwave" not in read("inquest/bind/1.mcfunction"):
        raise RuntimeError("phase2 shockwave route missing")
    anchor = read("inquest/anchor_tick.mcfunction")
    for route in ("phase2/tick", "phase2/pressure_tick", "counter/tick", "struggle_tick", "start_verdict", "anchor_collapse"):
        if route not in anchor:
            raise RuntimeError("anchor phase2 route missing: " + route)
    if "outcome/eliminate_boss" not in read("inquest/anchor_collapse.mcfunction"):
        raise RuntimeError("zero stability does not force eliminate")
    if "Health:700f" not in read("inquest/outcome/eliminate_boss.mcfunction"):
        raise RuntimeError("eliminate phase is not 700 health")
    if "rpg:inquest/right_click" not in json.dumps(
            json.load(io.open(os.path.join(ADV, "inquest", "right_click.json"), encoding="utf-8"))):
        raise RuntimeError("right click advancement missing")
    for n in range(1, 8):
        if "rpg_right_click:1b" not in read("inquest/give/medium%d.mcfunction" % n):
            raise RuntimeError("interactive medium missing: %d" % n)
        if "right_click/medium%d" % n not in read("inquest/right_click.mcfunction"):
            raise RuntimeError("right click medium route missing: %d" % n)
        for variant in range(1, 4):
            if not os.path.isfile(p("inquest/phase2/pressure/%d_%d.mcfunction" % (n, variant))):
                raise RuntimeError("pressure variant missing: %d/%d" % (n, variant))
            route = "phase2/pressure/%d_%d" % (n, variant)
            if route not in read("inquest/phase2/pressure.mcfunction"):
                raise RuntimeError("pressure variant is unreachable: %d/%d" % (n, variant))
    if "rpg_ex_hud_t=1.." not in read("hud/hud.mcfunction"):
        raise RuntimeError("persistent ritual HUD priority route missing")
    if "$(d)" not in read("hud/render.mcfunction"):
        raise RuntimeError("ritual HUD storage segment missing")
    if "storage rpg:hud d set value" not in read("hud/status.mcfunction"):
        raise RuntimeError("normal HUD does not clear ritual segment")


def main():
    add_objectives()
    build_interactive_items()
    build_right_click_runtime()
    build_phase2_entry()
    build_stability_loop()
    build_anchor_state_machine()
    build_hud()
    validate()
    print("ritual phase2: 50 stability, shockwave + 21 rotating pressure fields, attack/tool contest")
    print("ritual phase2: persistent actionbar, 0 forced eliminate, 100 verdict")
    print("ritual input: 7 media + pages + nail/incense/chalk/lantern support right-click")


if __name__ == "__main__":
    main()
