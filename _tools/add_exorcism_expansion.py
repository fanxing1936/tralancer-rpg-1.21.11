# -*- coding: utf-8 -*-
"""扩展驱魔体系：反仪式、四结局、驱魔师成长与仪式工具。

必须在 add_true_name_rite.py 之后运行。所有持续逻辑都挂在已经存在的
玩家/法阵热路径上，并以活动标签或分数作为守卫，空场不扫描世界实体。
"""

import io
import json
import os
import sys

import add_true_name_rite as rite


DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")
LORDS = rite.LORDS

OBJECTIVES = {
    "rpg_ex_stab": "dummy",
    "rpg_ex_counter": "dummy",
    "rpg_ex_kind": "dummy",
    "rpg_ex_ctime": "dummy",
    "rpg_ex_ransom": "dummy",
    "rpg_ex_slots": "dummy",
    "rpg_ex_toolcd": "dummy",
    "rpg_ex_choice": "trigger",
    "rpg_ex_xp": "dummy",
    "rpg_ex_lvl": "dummy",
    "rpg_ex_path": "dummy",
    "rpg_ex_seen": "dummy",
    "rpg_ex_prev": "dummy",
    "rpg_ex_use": "minecraft.used:minecraft.goat_horn",
    "rpg_seal_t": "dummy",
    "rpg_seal_roll": "dummy",
    "rpg_seal_i": "dummy",
    "rpg_prop_t": "dummy",
}


def path(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep))


def read(rel):
    with io.open(path(rel), encoding="utf-8") as f:
        return f.read()


def write(rel, content):
    p = path(rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.rstrip("\n") + "\n")


def write_data(rel, value):
    p = os.path.join(DP, "data", rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")


def patch_once(rel, needle, insert, before=False):
    src = read(rel)
    if insert.strip() in src:
        return
    if needle not in src:
        raise RuntimeError("patch anchor missing in %s: %s" % (rel, needle))
    rep = insert + needle if before else needle + insert
    write(rel, src.replace(needle, rep, 1))


def raw(parts):
    return json.dumps([""] + parts, ensure_ascii=False, separators=(",", ":"))


def txt(value, colour="white", bold=False, italic=False, click=None):
    out = {"text": value, "color": colour}
    if bold:
        out["bold"] = True
    if italic:
        out["italic"] = True
    if click:
        out["click_event"] = {"action": "run_command", "command": click}
    return out


def item_txt(value, colour="white", bold=False):
    """Item text style shared by the established RPG item catalogue."""
    out = {"text": value, "italic": False, "color": colour}
    if bold:
        out["bold"] = True
    return out


def item(base, name, colour, lore, data, extra=""):
    name_json = json.dumps(["", item_txt("[驱魔]", "#FFD85A", True),
                            item_txt(name, colour, True)], ensure_ascii=False,
                           separators=(",", ":"))
    rule = ["", item_txt("+------------------+", "white")]
    lore_json = json.dumps([rule] +
                           [["", item_txt(line, "gray")] for line in lore] +
                           [rule],
                           ensure_ascii=False, separators=(",", ":"))
    comps = "custom_name=%s,lore=%s,enchantment_glint_override=true,custom_data={%s}" % (
        name_json, lore_json, data)
    if extra:
        comps += "," + extra
    return "%s[%s]" % (base, comps)


PAGE_ITEMS = {}
for q in LORDS:
    PAGE_ITEMS[q["n"]] = item(
        "paper", "真名残页 · " + q["who"], q["colour"],
        ["调查档案的可携带抄本", "携带时可替代本人真名记录参与宣判",
         "参与宣判时会显现在法阵一侧", "不会消耗，可交给其他驱魔者"],
        "holy_weapon_tag:1b,rpg_rite_page:1b,rpg_lord:%d" % q["n"])

NAIL = item("iron_nugget", "银质圣钉", "#DCE6EE",
            ["投入活动法阵，在落点立为圣钉", "抵消萨麦尔的破阵，并提高稳定度"],
            "holy_weapon_tag:1b,rpg_rite_tool:1b,rpg_nail:1b")
BELL = item("goat_horn", "告解铃", "#FFF2A8",
            ["右键将铃影立于法阵并打断反仪式", "铃声会激怒恶魔，并暴露敲铃者"],
            "holy_weapon_tag:1b,rpg_rite_tool:1b,rpg_bell:1b",
            'instrument="minecraft:ponder_goat_horn",max_stack_size=1')
INCENSE = item("blaze_powder", "净罪香", "#E7D7B5",
               ["投入活动法阵，在落点燃起净罪香", "净化六格负面效果；恶魔短暂狂暴"],
               "holy_weapon_tag:1b,rpg_rite_tool:1b,rpg_incense:1b")
LANTERN = item("soul_lantern", "封魔灯", "#62D9E8",
               ["裁决封印时置于法阵并消耗", "封存残魂；长期携带仍有逃逸风险"],
               "holy_weapon_tag:1b,rpg_rite_tool:1b,rpg_lantern:1b")
CHALKS = {
    1: item("white_dye", "守御粉笔", "#BFD7FF",
            ["投入法阵：在落点刻写守御印", "降低稳定度损失；占用一个槽位"],
            "holy_weapon_tag:1b,rpg_rite_tool:1b,rpg_chalk:1b"),
    2: item("gray_dye", "压制粉笔", "#C8B6E8",
            ["投入法阵：在落点刻写压制印", "延长反仪式间隔；占用一个槽位"],
            "holy_weapon_tag:1b,rpg_rite_tool:1b,rpg_chalk:2b"),
    3: item("light_blue_dye", "疾行粉笔", "#7FE6FF",
            ["投入法阵：在落点刻写疾行印", "宣判速度翻倍；占用一个槽位"],
            "holy_weapon_tag:1b,rpg_rite_tool:1b,rpg_chalk:3b"),
}
STRONG_WATER = item(
    "lingering_potion", "浓缩驱魔圣水", "#FFF2A8",
    ["高阶圣水；净罪效率为普通圣水两倍", "投掷后会在图腾旁留下圣水瓶影"],
    "holy_weapon_tag:1b,rite_tag:1b,rpg_strong_water:1b",
    'potion_contents={custom_color:16773320,custom_effects:[{id:"minecraft:water_breathing",duration:100,amplifier:0}]},tooltip_display={hidden_components:["minecraft:potion_contents"]}')


def add_objectives():
    rel = "command/soreboard.mcfunction"
    src = read(rel).rstrip()
    for name, criterion in OBJECTIVES.items():
        line = "scoreboard objectives add %s %s" % (name, criterion)
        if line not in src:
            src += "\n" + line
    write(rel, src)


def build_give_functions():
    for n, stack in PAGE_ITEMS.items():
        write("inquest/give/page%d.mcfunction" % n, "give @s %s" % stack)
    write("inquest/give/nail.mcfunction", "give @s %s 4" % NAIL)
    write("inquest/give/bell.mcfunction", "give @s %s" % BELL)
    write("inquest/give/incense.mcfunction", "give @s %s 2" % INCENSE)
    write("inquest/give/lantern.mcfunction", "give @s %s" % LANTERN)
    write("inquest/give/strong_water.mcfunction", "give @s %s 2" % STRONG_WATER)
    for n, stack in CHALKS.items():
        write("inquest/give/chalk%d.mcfunction" % n, "give @s %s 3" % stack)
    all_lines = ["function rpg:inquest/give/nail", "function rpg:inquest/give/bell",
                 "function rpg:inquest/give/incense", "function rpg:inquest/give/lantern",
                 "function rpg:inquest/give/strong_water"]
    all_lines += ["function rpg:inquest/give/chalk%d" % n for n in range(1, 4)]
    all_lines += ["function rpg:inquest/give/page%d" % n for n in range(1, 8)]
    write("inquest/give/all_tools.mcfunction", "\n".join(all_lines))


def build_career():
    menu = raw([
        txt("[驱魔师档案] ", "#FFF2A8", True), txt("等级 ", "gray"),
        {"score": {"name": "@s", "objective": "rpg_ex_lvl"}, "color": "white"},
        txt("　阅历 ", "gray"),
        {"score": {"name": "@s", "objective": "rpg_ex_xp"}, "color": "#FFD85A"}])
    choose = raw([
        txt("选择路线： ", "gray"),
        txt("[审判]", "#FF806B", True, click="/trigger rpg_ex_choice set 21"), txt("  "),
        txt("[守护]", "#8FC7FF", True, click="/trigger rpg_ex_choice set 22"), txt("  "),
        txt("[秘仪]", "#D596F2", True, click="/trigger rpg_ex_choice set 23")])
    write("inquest/career.mcfunction", """\
scoreboard players add @s rpg_ex_xp 0
scoreboard players add @s rpg_ex_lvl 0
scoreboard players add @s rpg_ex_path 0
function rpg:inquest/career/sync
tellraw @s %(menu)s
execute if score @s rpg_ex_path matches 0 run tellraw @s %(choose)s
execute if score @s rpg_ex_path matches 1 run tellraw @s %(p1)s
execute if score @s rpg_ex_path matches 2 run tellraw @s %(p2)s
execute if score @s rpg_ex_path matches 3 run tellraw @s %(p3)s
function rpg:inquest/career/claim
""" % dict(menu=menu, choose=choose,
           p1=raw([txt("路线：审判 · 识破、打断、处决", "#FF806B", True)]),
           p2=raw([txt("路线：守护 · 固阵、减损、封印", "#8FC7FF", True)]),
           p3=raw([txt("路线：秘仪 · 净化、加速、通晓", "#D596F2", True)])))

    write("inquest/career/sync.mcfunction", """\
scoreboard players operation @s rpg_ex_prev = @s rpg_ex_lvl
scoreboard players set @s rpg_ex_lvl 1
execute if score @s rpg_ex_xp matches 40.. run scoreboard players set @s rpg_ex_lvl 2
execute if score @s rpg_ex_xp matches 100.. run scoreboard players set @s rpg_ex_lvl 3
execute if score @s rpg_ex_xp matches 180.. run scoreboard players set @s rpg_ex_lvl 4
execute if score @s rpg_ex_xp matches 280.. run scoreboard players set @s rpg_ex_lvl 5
execute if score @s rpg_ex_lvl > @s rpg_ex_prev run function rpg:inquest/career/level_up
scoreboard players operation @s rpg_ex_seen = @s rpg_ex_xp
""")
    write("inquest/career/level_up.mcfunction", """\
title @s times 5 45 15
title @s title %(title)s
title @s subtitle %(sub)s
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 0.8 1.4
function rpg:inquest/career/claim
""" % {"title": raw([txt("驱 魔 师 晋 阶", "#FFF2A8", True)]),
         "sub": raw([txt("使用 /function rpg:inquest/career 查看档案", "gray")])})

    for n, name, colour in ((1, "审判", "#FF806B"), (2, "守护", "#8FC7FF"),
                            (3, "秘仪", "#D596F2")):
        write("inquest/career/choose%d.mcfunction" % n, """\
execute unless score @s rpg_ex_path matches 0 run return 0
scoreboard players set @s rpg_ex_path %(n)d
tellraw @s %(msg)s
playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1.2
function rpg:inquest/career/claim
""" % {"n": n, "msg": raw([txt("[路线确立] ", colour, True),
                                      txt(name + "。此选择不可随意撤销。", "gray")])})

    write("inquest/career/claim.mcfunction", """\
execute if score @s rpg_ex_lvl matches 2.. unless entity @s[tag=rpg.ex.claim2] if score @s rpg_ex_path matches 1..3 run function rpg:inquest/career/claim2
execute if score @s rpg_ex_lvl matches 3.. unless entity @s[tag=rpg.ex.claim3] if score @s rpg_ex_path matches 1..3 run function rpg:inquest/career/claim3
execute if score @s rpg_ex_lvl matches 4.. unless entity @s[tag=rpg.ex.claim4] run function rpg:inquest/career/claim4
execute if score @s rpg_ex_lvl matches 5.. unless entity @s[tag=rpg.ex.claim5] run function rpg:inquest/career/claim5
""")
    write("inquest/career/claim2.mcfunction", """\
tag @s add rpg.ex.claim2
execute if score @s rpg_ex_path matches 1 run function rpg:inquest/give/bell
execute if score @s rpg_ex_path matches 2 run function rpg:inquest/give/nail
execute if score @s rpg_ex_path matches 3 run function rpg:inquest/give/incense
tellraw @s %(msg)s
""" % {"msg": raw([txt("[职业解锁] ", "#FFF2A8", True), txt("获得本路线的第一件仪式工具。", "gray")])})
    write("inquest/career/claim3.mcfunction", """\
tag @s add rpg.ex.claim3
execute if score @s rpg_ex_path matches 1 run function rpg:inquest/give/chalk2
execute if score @s rpg_ex_path matches 2 run function rpg:inquest/give/chalk1
execute if score @s rpg_ex_path matches 3 run function rpg:inquest/give/chalk3
tellraw @s %(msg)s
""" % {"msg": raw([txt("[职业解锁] ", "#FFF2A8", True), txt("获得本路线的仪式粉笔。", "gray")])})
    write("inquest/career/claim4.mcfunction", """\
tag @s add rpg.ex.claim4
function rpg:inquest/give/lantern
function rpg:inquest/give/strong_water
tellraw @s %(msg)s
""" % {"msg": raw([txt("[职业解锁] ", "#FFF2A8", True), txt("封魔灯与浓缩驱魔圣水。", "gray")])})
    write("inquest/career/claim5.mcfunction", """\
tag @s add rpg.ex.claim5
function rpg:inquest/give/nail
function rpg:inquest/give/bell
function rpg:inquest/give/incense
function rpg:inquest/give/chalk1
function rpg:inquest/give/chalk2
function rpg:inquest/give/chalk3
tellraw @s %(msg)s
""" % {"msg": raw([txt("[职业解锁] ", "#FFF2A8", True), txt("仪式槽位提升为 2，并通晓全部基础工具。", "gray")])})


def build_player_runtime():
    write("inquest/player_tick.mcfunction", """\
scoreboard players enable @s rpg_ex_choice
scoreboard players add @s rpg_ex_xp 0
scoreboard players add @s rpg_ex_lvl 0
scoreboard players add @s rpg_ex_path 0
scoreboard players add @s rpg_ex_seen 0
execute unless score @s rpg_ex_xp = @s rpg_ex_seen run function rpg:inquest/career/sync
execute if score @s rpg_ex_lvl matches 0 run function rpg:inquest/career/sync
execute if score @s rpg_ex_choice matches 1..4 run function rpg:inquest/choice/final
execute if score @s rpg_ex_choice matches 11..13 run function rpg:inquest/choice/ransom
execute if score @s rpg_ex_choice matches 21 run function rpg:inquest/career/choose1
execute if score @s rpg_ex_choice matches 22 run function rpg:inquest/career/choose2
execute if score @s rpg_ex_choice matches 23 run function rpg:inquest/career/choose3
execute if score @s rpg_ex_choice matches 1.. run scoreboard players set @s rpg_ex_choice 0
execute if score @s rpg_ex_use matches 1.. if items entity @s weapon.mainhand minecraft:goat_horn[minecraft:custom_data~{rpg_bell:1b}] run function rpg:inquest/tool/bell
execute if score @s rpg_ex_use matches 1.. run scoreboard players set @s rpg_ex_use 0
scoreboard players add @s rpg_seal_i 1
execute if score @s rpg_seal_i matches 100.. run function rpg:inquest/seal/reindex
execute if entity @s[tag=rpg.seal.carrier] run function rpg:inquest/seal/tick
execute unless entity @s[tag=rpg.seal.carrier] run scoreboard players set @s rpg_seal_t 0
""")

    # Full-inventory matching is intentionally throttled to once per five
    # seconds per player.  Verdict rewards tag their receiver immediately;
    # this slow pass only reconciles dropped or transferred relics.
    write("inquest/seal/reindex.mcfunction", """\
scoreboard players set @s rpg_seal_i 0
tag @s remove rpg.seal.carrier
execute if items entity @s inventory.* minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b}] run tag @s add rpg.seal.carrier
execute unless entity @s[tag=rpg.seal.carrier] run scoreboard players set @s rpg_seal_t 0
""")

    write("inquest/tool/bell.mcfunction", """\
execute if entity @s[scores={rpg_ex_toolcd=1..}] run return 0
tag @s add rpg.rite.chooser
execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..16,sort=nearest,limit=1,scores={rpg_ex_stage=2..4}] run function rpg:inquest/tool/bell_anchor
tag @s remove rpg.rite.chooser
scoreboard players set @s rpg_ex_toolcd 300
effect give @s minecraft:glowing 8 0 true
effect give @s minecraft:weakness 8 0 true
""")
    write("inquest/tool/bell_anchor.mcfunction", """\
scoreboard players set @s rpg_ex_kind 0
scoreboard players set @s rpg_ex_ctime 0
scoreboard players set @s rpg_ex_ransom 0
scoreboard players set @s rpg_ex_counter 180
scoreboard players add @s rpg_ex_stab 12
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..10]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..12]
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14,limit=1] run effect give @s minecraft:strength 8 1 true
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14,limit=1] run effect give @s minecraft:speed 8 1 true
scoreboard players add @a[tag=rpg.rite.chooser,distance=..16] rpg_ex_xp 2
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
particle flash{color:16773574} ~ ~1 ~ 0 0 0 0 1 force
""" % {"msg": raw([txt("[告解铃] ", "#FFF2A8", True),
                         txt("反仪式被打断；敲铃者已被恶魔注视。", "gray")])})

    # 遗物只在携带者身上计时：每十分钟掷一次，平均约一小时逃逸一次。
    write("inquest/seal/tick.mcfunction", """\
scoreboard players add @s rpg_seal_t 1
execute if score @s rpg_seal_t matches 12000.. run execute store result score @s rpg_seal_roll run random value 1..6
execute if score @s rpg_seal_t matches 12000.. run scoreboard players set @s rpg_seal_t 0
execute if score @s rpg_seal_roll matches 1 run function rpg:inquest/seal/escape
execute if score @s rpg_seal_roll matches 1.. run scoreboard players set @s rpg_seal_roll 0
""")
    escape = []
    for q in LORDS:
        escape.append("execute if items entity @s inventory.* minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:%d}] run return run function rpg:inquest/seal/escape%d" % (q["n"], q["n"]))
        write("inquest/seal/escape%d.mcfunction" % q["n"], """\
clear @s minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:%(n)d}] 1
scoreboard players add @s rpg_taint 15
execute at @s run function rpg:taint/lord%(n)d
tellraw @a[distance=..24,gamemode=!spectator] %(msg)s
playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..32] ~ ~ ~ 1 0.55
function rpg:inquest/seal/reindex
""" % {"n": q["n"], "msg": raw([txt("[封印逃逸] ", q["colour"], True),
                                            txt(q["who"] + "的残魂从遗物中重新降临。", "gray")])})
    write("inquest/seal/escape.mcfunction", "\n".join(escape))


def build_stability():
    write("inquest/stability/show.mcfunction", "tellraw @a[distance=..16,gamemode=!spectator] " + raw([
        txt("[法阵稳定] ", "#FFF2A8", True),
        {"score": {"name": "@s", "objective": "rpg_ex_stab"}, "color": "white"},
        txt(" / 100", "gray")]))
    for amount in (10, 15, 20, 25):
        guard = (amount * 2 + 4) // 5
        write("inquest/stability/hit%d.mcfunction" % amount, """\
scoreboard players remove @s rpg_ex_stab %(amount)d
execute if entity @s[tag=rpg.layout.guard] run scoreboard players add @s rpg_ex_stab %(guard)d
execute if entity @a[distance=..10,gamemode=!spectator,scores={rpg_ex_path=2,rpg_ex_lvl=2..}] run scoreboard players add @s rpg_ex_stab 4
execute if score @s rpg_ex_stab matches ..0 run return run function rpg:inquest/anchor_collapse
function rpg:inquest/stability/show
""" % {"amount": amount, "guard": guard})
    write("inquest/stability/restore.mcfunction", """\
scoreboard players add @s rpg_ex_stab 15
execute if entity @a[distance=..10,gamemode=!spectator,scores={rpg_ex_path=1,rpg_ex_lvl=2..}] run scoreboard players add @s rpg_ex_stab 5
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
scoreboard players add @a[distance=..10,gamemode=!spectator] rpg_ex_xp 3
function rpg:inquest/stability/show
""")
    write("inquest/anchor_collapse.mcfunction", """\
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/fail
tellraw @a[distance=..20,gamemode=!spectator] %(msg)s
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..10]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..12]
particle explosion ~ ~0.8 ~ 0.4 0.4 0.4 0.05 4 force
playsound minecraft:block.beacon.deactivate hostile @a[distance=..24] ~ ~ ~ 1 0.5
kill @s
""" % {"msg": raw([txt("[法阵崩溃] ", "dark_red", True),
                         txt("稳定度归零，反仪式撕开了边界。", "gray")])})


def build_tool_runtime():
    write("inquest/tool/consume.mcfunction", """\
execute store result score #tool_count rpg_ex_tmp run data get entity @s Item.count 1
scoreboard players remove #tool_count rpg_ex_tmp 1
execute if score #tool_count rpg_ex_tmp matches 1.. store result entity @s Item.count int 1 run scoreboard players get #tool_count rpg_ex_tmp
execute if score #tool_count rpg_ex_tmp matches ..0 run kill @s
""")
    write("inquest/tool/scan.mcfunction", """\
execute as @e[type=minecraft:item,distance=..3] if items entity @s contents *[minecraft:custom_data~{rpg_nail:1b}] run tag @s add rpg.rite.tool.nail
execute unless entity @s[tag=rpg.rite.nailed] as @e[type=minecraft:item,tag=rpg.rite.tool.nail,distance=..3,sort=nearest,limit=1] run return run function rpg:inquest/tool/nail_item
tag @e[type=minecraft:item,tag=rpg.rite.tool.nail,distance=..3] remove rpg.rite.tool.nail
execute as @e[type=minecraft:item,distance=..3] if items entity @s contents *[minecraft:custom_data~{rpg_chalk:1b}] run tag @s add rpg.rite.tool.chalk1
execute if score @s rpg_ex_slots matches 1.. unless entity @s[tag=rpg.layout.guard] as @e[type=minecraft:item,tag=rpg.rite.tool.chalk1,distance=..3,sort=nearest,limit=1] run return run function rpg:inquest/tool/chalk1_item
tag @e[type=minecraft:item,tag=rpg.rite.tool.chalk1,distance=..3] remove rpg.rite.tool.chalk1
execute as @e[type=minecraft:item,distance=..3] if items entity @s contents *[minecraft:custom_data~{rpg_chalk:2b}] run tag @s add rpg.rite.tool.chalk2
execute if score @s rpg_ex_slots matches 1.. unless entity @s[tag=rpg.layout.suppress] as @e[type=minecraft:item,tag=rpg.rite.tool.chalk2,distance=..3,sort=nearest,limit=1] run return run function rpg:inquest/tool/chalk2_item
tag @e[type=minecraft:item,tag=rpg.rite.tool.chalk2,distance=..3] remove rpg.rite.tool.chalk2
execute as @e[type=minecraft:item,distance=..3] if items entity @s contents *[minecraft:custom_data~{rpg_chalk:3b}] run tag @s add rpg.rite.tool.chalk3
execute if score @s rpg_ex_slots matches 1.. unless entity @s[tag=rpg.layout.haste] as @e[type=minecraft:item,tag=rpg.rite.tool.chalk3,distance=..3,sort=nearest,limit=1] run return run function rpg:inquest/tool/chalk3_item
tag @e[type=minecraft:item,tag=rpg.rite.tool.chalk3,distance=..3] remove rpg.rite.tool.chalk3
execute as @e[type=minecraft:item,distance=..3] if items entity @s contents *[minecraft:custom_data~{rpg_incense:1b}] run tag @s add rpg.rite.tool.incense
execute unless score @s rpg_ex_toolcd matches 1.. as @e[type=minecraft:item,tag=rpg.rite.tool.incense,distance=..3,sort=nearest,limit=1] run return run function rpg:inquest/tool/incense_item
tag @e[type=minecraft:item,tag=rpg.rite.tool.incense,distance=..3] remove rpg.rite.tool.incense
""")
    write("inquest/tool/nail_item.mcfunction", """\
tag @e[type=minecraft:item,tag=rpg.rite.tool.nail,distance=..4] remove rpg.rite.tool.nail
function rpg:inquest/tool/consume
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run tag @s add rpg.rite.nailed
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run scoreboard players add @s rpg_ex_stab 20
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1,scores={rpg_ex_stab=101..}] run scoreboard players set @s rpg_ex_stab 100
particle end_rod ~ ~0.2 ~ 0.35 0.1 0.35 0.02 30 force
playsound minecraft:block.anvil.place player @a[distance=..14] ~ ~ ~ 0.7 1.8
tellraw @a[distance=..14,gamemode=!spectator] %(msg)s
""" % {"msg": raw([txt("[银质圣钉] ", "#DCE6EE", True), txt("法阵边界已固定。", "gray")])})
    for n, key, name, colour in ((1, "guard", "守御", "#BFD7FF"),
                                 (2, "suppress", "压制", "#C8B6E8"),
                                 (3, "haste", "疾行", "#7FE6FF")):
        write("inquest/tool/chalk%d_item.mcfunction" % n, """\
tag @e[type=minecraft:item,tag=rpg.rite.tool.chalk%(n)d,distance=..4] remove rpg.rite.tool.chalk%(n)d
function rpg:inquest/tool/consume
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run tag @s add rpg.layout.%(key)s
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run scoreboard players remove @s rpg_ex_slots 1
particle dust{color:[0.72,0.86,1.0],scale:0.8} ~ ~0.15 ~ 1.8 0.05 1.8 0.01 45 force
playsound minecraft:block.calcite.place player @a[distance=..14] ~ ~ ~ 0.8 1.4
tellraw @a[distance=..14,gamemode=!spectator] %(msg)s
""" % {"n": n, "key": key, "msg": raw([txt("[仪式粉笔] ", colour, True), txt(name + "法阵已刻写。", "gray")])})
    write("inquest/tool/incense_item.mcfunction", """\
tag @e[type=minecraft:item,tag=rpg.rite.tool.incense,distance=..4] remove rpg.rite.tool.incense
function rpg:inquest/tool/consume
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run scoreboard players set @s rpg_ex_toolcd 200
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run scoreboard players add @s rpg_ex_stab 15
effect clear @a[distance=..6,gamemode=!spectator] minecraft:slowness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:weakness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:blindness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:darkness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:nausea
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14,limit=1] run effect give @s minecraft:strength 8 1 true
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14,limit=1] run effect give @s minecraft:speed 8 1 true
particle campfire_cosy_smoke ~ ~0.4 ~ 1.2 0.3 1.2 0.03 35 force
tellraw @a[distance=..14,gamemode=!spectator] %(msg)s
""" % {"msg": raw([txt("[净罪香] ", "#E7D7B5", True), txt("污秽暂退，恶魔因香火而狂怒。", "gray")])})


def build_ritual_props():
    """把仪式消耗品转成贴地 item_display，并与所属法阵一起回收。"""

    def place(rel, item_id, prop_tag, offset="~ ~0.06 ~", scale="0.80",
              ttl=900, linger=False, extra_components=""):
        tags = ['"rpg.rite.prop"', '"rpg.rite.prop.new"',
                '"rpg.rite.prop.%s"' % prop_tag]
        if linger:
            tags.append('"rpg.rite.prop.linger"')
        components = '"minecraft:enchantment_glint_override":1b'
        if extra_components:
            components += "," + extra_components
        nbt = (
            '{Tags:[%s],item:{id:"minecraft:%s",count:1,components:{%s}},'
            'item_display:"ground",view_range:0.65f,shadow_radius:0.18f,'
            'shadow_strength:0.45f,brightness:{block:15,sky:12},'
            'transformation:{translation:[0f,0.03f,0f],'
            'scale:[%sf,%sf,%sf],left_rotation:[0f,0f,0f,1f],'
            'right_rotation:[0f,0f,0f,1f]}}' %
            (",".join(tags), item_id, components, scale, scale, scale))
        write("inquest/tool/place/%s.mcfunction" % rel, """\
scoreboard players add @s rpg_rite_id 0
summon minecraft:item_display %(offset)s %(nbt)s
scoreboard players operation @e[type=minecraft:item_display,tag=rpg.rite.prop.new,distance=..3,sort=nearest,limit=1] rpg_rite_id = @s rpg_rite_id
scoreboard players set @e[type=minecraft:item_display,tag=rpg.rite.prop.new,distance=..3,sort=nearest,limit=1] rpg_prop_t %(ttl)d
tag @e[type=minecraft:item_display,tag=rpg.rite.prop.new,distance=..3] remove rpg.rite.prop.new
""" % {"offset": offset, "nbt": nbt, "ttl": ttl})

    place("nail", "iron_nugget", "nail", scale="0.64")
    place("bell", "goat_horn", "bell", offset="~-1.35 ~0.06 ~0.65", scale="0.88")
    place("incense", "blaze_powder", "incense", scale="0.78")
    place("lantern", "soul_lantern", "lantern", offset="~0.95 ~0.06 ~1.05",
          scale="0.92", ttl=120, linger=True)
    place("chalk1", "white_dye", "chalk1", scale="0.86")
    place("chalk2", "gray_dye", "chalk2", scale="0.86")
    place("chalk3", "light_blue_dye", "chalk3", scale="0.86")
    place("page", "paper", "page", offset="~-0.95 ~0.06 ~1.10", scale="0.82")
    place("water", "lingering_potion", "water", offset="~0.65 ~0.06 ~-0.85",
          scale="0.76", ttl=200,
          extra_components='"minecraft:potion_contents":{custom_color:16773320}')
    for q in LORDS:
        place("medium%d" % q["n"], q["item"].split(":", 1)[-1],
              "medium", offset="~1.15 ~0.06 ~0.75", scale="0.84")

    write("inquest/tool/prop_tick.mcfunction", """\
scoreboard players remove @s rpg_prop_t 1
execute if score @s rpg_prop_t matches ..0 run kill @s
""")
    write("inquest/tool/cleanup.mcfunction", """\
tag @s add rpg.rite.prop.owner
execute as @e[type=minecraft:item_display,tag=rpg.rite.prop,tag=!rpg.rite.prop.linger,distance=..18] if score @s rpg_rite_id = @e[tag=rpg.rite.prop.owner,limit=1] rpg_rite_id run kill @s
tag @s remove rpg.rite.prop.owner
""")

    # 投入型工具在物品实体落点留下实物；原有消耗与功能随后照常结算。
    direct = {
        "inquest/tool/nail_item.mcfunction": "nail",
        "inquest/tool/chalk1_item.mcfunction": "chalk1",
        "inquest/tool/chalk2_item.mcfunction": "chalk2",
        "inquest/tool/chalk3_item.mcfunction": "chalk3",
        "inquest/tool/incense_item.mcfunction": "incense",
    }
    for rel, prop in direct.items():
        src = read(rel)
        needle = "function rpg:inquest/tool/consume"
        line = ("execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,"
                "distance=..3,sort=nearest,limit=1] run function "
                "rpg:inquest/tool/place/%s\n" % prop)
        if line.strip() not in src:
            write(rel, src.replace(needle, line + needle, 1))

    # 右键铃、弱点媒介、真名残页、封印灯与圣水分别在实际生效时显形。
    src = read("inquest/tool/bell_anchor.mcfunction")
    if "tool/place/bell" not in src:
        write("inquest/tool/bell_anchor.mcfunction",
              "function rpg:inquest/tool/place/bell\n" + src)
    for q in LORDS:
        rel = "inquest/offer/%d.mcfunction" % q["n"]
        src = read(rel)
        if "tool/place/medium%d" % q["n"] not in src:
            write(rel, src.replace("function rpg:inquest/consume_offer",
                                   "function rpg:inquest/tool/place/medium%d\n"
                                   "function rpg:inquest/consume_offer" % q["n"], 1))

    src = read("inquest/choice/seal.mcfunction")
    lantern = ("execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,"
               "distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] "
               "run function rpg:inquest/tool/place/lantern")
    if "tool/place/lantern" not in src:
        write("inquest/choice/seal.mcfunction", lantern + "\n" + src)

    src = read("rite/light.mcfunction")
    if "tool/place/water" not in src:
        write("rite/light.mcfunction",
              src.replace("tag @s add rpg.totem.lit",
                          "function rpg:inquest/tool/place/water\n"
                          "tag @s add rpg.totem.lit", 1))

    src = read("inquest/anchor_stage3.mcfunction")
    if "#page_used" not in src:
        scans = ["scoreboard players set #page_used rpg_ex_tmp 0"]
        for q in LORDS:
            scans.append(
                "execute if score @s rpg_dm_lord matches %(n)d as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:%(n)d}] run scoreboard players set #page_used rpg_ex_tmp 1" % q)
        scans.append(
            "execute if score #page_used rpg_ex_tmp matches 1 unless entity @e[type=minecraft:item_display,tag=rpg.rite.prop.page,distance=..6] run function rpg:inquest/tool/place/page")
        needle = "scoreboard players set #channel rpg_ex_tmp 0"
        write("inquest/anchor_stage3.mcfunction",
              src.replace(needle, needle + "\n" + "\n".join(scans), 1))

    # 无器物时零扫描；存在摆件时才进入一次带类型的短生命周期遍历。
    src = read("exorcism.mcfunction").rstrip()
    hook = ("execute if entity @e[type=minecraft:item_display,tag=rpg.rite.prop,limit=1] "
            "run execute as @e[type=minecraft:item_display,tag=rpg.rite.prop] "
            "run function rpg:inquest/tool/prop_tick")
    if "tool/prop_tick" not in src:
        write("exorcism.mcfunction", src + "\n" + hook)

    # 所有法阵出口均回收同一 rite_id 的摆件；封魔灯作为结果演出多留六秒。
    cleanup_targets = (
        "inquest/fail.mcfunction",
        "inquest/anchor_success.mcfunction",
        "inquest/anchor_timeout.mcfunction",
        "inquest/anchor_orphan.mcfunction",
        "inquest/anchor_collapse.mcfunction",
        "inquest/outcome/eliminate.mcfunction",
        "inquest/outcome/seal.mcfunction",
        "inquest/outcome/pact.mcfunction",
    )
    for rel in cleanup_targets:
        src = read(rel)
        if "tool/cleanup" not in src:
            if "kill @s" in src:
                src = src.replace("kill @s",
                                  "function rpg:inquest/tool/cleanup\nkill @s", 1)
            else:
                src = src.rstrip() + "\nfunction rpg:inquest/tool/cleanup\n"
            write(rel, src)


def build_counters():
    write("inquest/counter/tick.mcfunction", """\
execute if score @s rpg_ex_kind matches 1 run return run function rpg:inquest/counter/lucifer_wait
execute if score @s rpg_ex_kind matches 2 run return run function rpg:inquest/counter/leviathan_wait
execute if score @s rpg_ex_kind matches 7 run return 0
scoreboard players remove @s rpg_ex_counter 1
execute if score @s rpg_ex_counter matches ..0 run function rpg:inquest/counter/dispatch
""")
    dispatch = ["execute store result score @s rpg_ex_counter run random value 180..260",
                "execute if entity @s[tag=rpg.layout.suppress] run scoreboard players add @s rpg_ex_counter 80"]
    for q in LORDS:
        dispatch.append("execute if score @s rpg_dm_lord matches %(n)d run return run function rpg:inquest/counter/start%(n)d" % q)
    write("inquest/counter/dispatch.mcfunction", "\n".join(dispatch))

    # 1 傲慢：三个可攻击名号，击中伪名扣稳定，击中真名解局。
    write("inquest/counter/start1.mcfunction", """\
scoreboard players set @s rpg_ex_kind 1
scoreboard players set @s rpg_ex_ctime 140
summon minecraft:armor_stand ~2 ~ ~ {Tags:["rpg.counter.name","rpg.counter.false"],Invisible:1b,NoGravity:1b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:[{"text":"晨星之王","color":"#A8FFCB","bold":true,"italic":false}],Health:200f,attributes:[{id:"max_health",base:200f}]}
summon minecraft:armor_stand ~-2 ~ ~ {Tags:["rpg.counter.name","rpg.counter.true"],Invisible:1b,NoGravity:1b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:[{"text":"路西法","color":"#31D97C","bold":true,"italic":false}],Health:200f,attributes:[{id:"max_health",base:200f}]}
summon minecraft:armor_stand ~ ~ ~2 {Tags:["rpg.counter.name","rpg.counter.false"],Invisible:1b,NoGravity:1b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:[{"text":"光耀者","color":"#A8FFCB","bold":true,"italic":false}],Health:200f,attributes:[{id:"max_health",base:200f}]}
scoreboard players operation @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..4] rpg_rite_id = @s rpg_rite_id
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
playsound minecraft:entity.illusioner.prepare_mirror hostile @a[distance=..20] ~ ~ ~ 1 0.8
""" % {"msg": raw([txt("[反仪式·傲慢] ", "#31D97C", True),
                         txt("王冠伪造了三个名号。攻击错误名字会撕裂法阵。", "gray")])})
    write("inquest/counter/lucifer_wait.mcfunction", """\
scoreboard players remove @s rpg_ex_ctime 1
execute if score @s rpg_ex_ctime matches ..0 run function rpg:inquest/counter/lucifer_timeout
""")
    write("inquest/counter/lucifer_timeout.mcfunction", """\
scoreboard players set @s rpg_ex_kind 0
function rpg:inquest/stability/hit20
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..10]
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
""" % {"msg": raw([txt("[伪名坐实] ", "dark_red", True), txt("无人宣认真名，法阵承认了谎言。", "gray")])})
    write("inquest/counter/name_tick.mcfunction", """\
execute store result score #name_hurt rpg_ex_tmp run data get entity @s HurtTime 1
execute if score #name_hurt rpg_ex_tmp matches 1.. if entity @s[tag=rpg.counter.true] run return run function rpg:inquest/counter/name_true
execute if score #name_hurt rpg_ex_tmp matches 1.. if entity @s[tag=rpg.counter.false] run return run function rpg:inquest/counter/name_false
""")
    write("inquest/counter/name_true.mcfunction", """\
execute on attacker run scoreboard players add @s rpg_ex_xp 3
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1] run scoreboard players set @s rpg_ex_kind 0
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1] run function rpg:inquest/stability/restore
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
playsound minecraft:block.amethyst_block.chime player @a[distance=..18] ~ ~ ~ 0.9 1.6
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..10]
""" % {"msg": raw([txt("[真名击破] ", "#31D97C", True), txt("傲慢的伪名失去效力。", "gray")])})
    write("inquest/counter/name_false.mcfunction", """\
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1] run scoreboard players set @s rpg_ex_kind 0
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1] run function rpg:inquest/stability/hit20
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
playsound minecraft:block.glass.break hostile @a[distance=..18] ~ ~ ~ 1 0.65
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..10]
""" % {"msg": raw([txt("[伪名误判] ", "dark_red", True), txt("错误的名字划伤了法阵。", "gray")])})

    # 2 嫉妒：复制最近玩家的六个装备槽，限时击破可修复稳定度。
    write("inquest/counter/start2.mcfunction", """\
scoreboard players set @s rpg_ex_kind 2
scoreboard players set @s rpg_ex_ctime 200
summon minecraft:husk ~2 ~ ~ {Tags:["rpg.counter.clone"],PersistenceRequired:1b,CanPickUpLoot:0b,CustomNameVisible:1b,CustomName:[{"text":"妒影","color":"#3DA9E8","bold":true,"italic":false}],Health:60f,attributes:[{id:"max_health",base:60f},{id:"attack_damage",base:9f},{id:"movement_speed",base:0.31f}],drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f,legs:0f,feet:0f}}
scoreboard players operation @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] rpg_rite_id = @s rpg_rite_id
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] weapon.mainhand from entity @p[distance=..14] weapon.mainhand
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] weapon.offhand from entity @p[distance=..14] weapon.offhand
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] armor.head from entity @p[distance=..14] armor.head
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] armor.chest from entity @p[distance=..14] armor.chest
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] armor.legs from entity @p[distance=..14] armor.legs
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] armor.feet from entity @p[distance=..14] armor.feet
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..20] ~ ~ ~ 1 0.75
""" % {"msg": raw([txt("[反仪式·嫉妒] ", "#3DA9E8", True),
                         txt("利维坦复制了最近驱魔者的装备；十秒内击破妒影。", "gray")])})
    write("inquest/counter/leviathan_wait.mcfunction", """\
scoreboard players set #clone_found rpg_ex_tmp 0
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run scoreboard players set #clone_found rpg_ex_tmp 1
tag @s remove rpg.rite.anchor.active
execute if score #clone_found rpg_ex_tmp matches 0 run return run function rpg:inquest/counter/leviathan_win
scoreboard players remove @s rpg_ex_ctime 1
execute if score @s rpg_ex_ctime matches ..0 run function rpg:inquest/counter/leviathan_timeout
""")
    write("inquest/counter/leviathan_win.mcfunction", """\
scoreboard players set @s rpg_ex_kind 0
function rpg:inquest/stability/restore
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
""" % {"msg": raw([txt("[妒影击破] ", "#3DA9E8", True), txt("被复制的力量回流法阵。", "gray")])})
    write("inquest/counter/leviathan_timeout.mcfunction", """\
scoreboard players set @s rpg_ex_kind 0
function rpg:inquest/stability/hit20
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14]
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
""" % {"msg": raw([txt("[嫉妒得逞] ", "dark_red", True), txt("妒影带走了法阵的一部分力量。", "gray")])})

    # 3 怠惰（亚巴顿）：直接拖慢进度。用户概念里的贝利尔/怠惰与现有七柱命名
    # 不一致；本包以既有柱位为准，怠惰属于亚巴顿、色欲属于贝利尔。
    write("inquest/counter/start3.mcfunction", """\
scoreboard players add @s rpg_ex_time 60
effect give @a[distance=..8,gamemode=!spectator] minecraft:slowness 6 2 true
effect give @a[distance=..8,gamemode=!spectator] minecraft:mining_fatigue 6 1 true
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
particle ash ~ ~0.7 ~ 2.5 0.4 2.5 0.02 55 normal
""" % {"msg": raw([txt("[反仪式·怠惰] ", "#D1D1D8", True), txt("亚巴顿令时间停滞，宣判延后了三秒。", "gray")])})

    # 4 暴食：只吞七种弱点媒介，不碰普通掉落物。
    write("inquest/counter/start4.mcfunction", """\
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:item,distance=..6] if items entity @s contents #rpg:rite_media run tag @s add rpg.counter.food
execute if entity @e[type=minecraft:item,tag=rpg.counter.food,distance=..6,limit=1] run return run function rpg:inquest/counter/beelzebub_eat
execute unless entity @e[type=minecraft:item,tag=rpg.counter.food,distance=..6,limit=1] run tellraw @a[distance=..16,gamemode=!spectator] %(miss)s
tag @e[type=minecraft:item,tag=rpg.counter.food,distance=..6] remove rpg.counter.food
tag @s remove rpg.rite.anchor.active
""" % {"miss": raw([txt("[反仪式·暴食] ", "#DCEB72", True), txt("别西卜没有找到可吞食的媒介。", "gray")])})
    write("inquest/counter/beelzebub_eat.mcfunction", """\
execute as @e[type=minecraft:item,tag=rpg.counter.food,distance=..6,limit=1,sort=nearest] run function rpg:inquest/tool/consume
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14,limit=1] run data merge entity @s {Health:455f}
function rpg:inquest/stability/hit10
tag @e[type=minecraft:item,tag=rpg.counter.food,distance=..6] remove rpg.counter.food
particle item{item:{id:"minecraft:poisonous_potato"}} ~ ~1 ~ 0.8 0.6 0.8 0.08 35 normal
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
tag @s remove rpg.rite.anchor.active
""" % {"msg": raw([txt("[反仪式·吞媒] ", "#DCEB72", True), txt("别西卜吞下一件地面媒介并恢复生命。", "gray")])})

    # 5 暴怒：圣钉可完整抵消一次破阵，否则崩裂边缘并击退阵内玩家。
    write("inquest/counter/start5.mcfunction", """\
execute if entity @s[tag=rpg.rite.nailed] run return run function rpg:inquest/counter/samael_blocked
function rpg:inquest/stability/hit25
tag @s add rpg.rite.anchor.active
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^0.25 ^-1.4
tag @s remove rpg.rite.anchor.active
particle dust{color:[1.0,0.12,0.08],scale:1.5} ~2 ~0.1 ~ 0.2 0.1 2 0.02 35 force
particle dust{color:[1.0,0.12,0.08],scale:1.5} ~-2 ~0.1 ~ 0.2 0.1 2 0.02 35 force
particle dust{color:[1.0,0.12,0.08],scale:1.5} ~ ~0.1 ~2 2 0.1 0.2 0.02 35 force
particle dust{color:[1.0,0.12,0.08],scale:1.5} ~ ~0.1 ~-2 2 0.1 0.2 0.02 35 force
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
""" % {"msg": raw([txt("[反仪式·暴怒] ", "#FF7A70", True), txt("萨麦尔击碎法阵边缘并震开守阵者。", "gray")])})
    write("inquest/counter/samael_blocked.mcfunction", """\
tag @s remove rpg.rite.nailed
scoreboard players add @a[distance=..10,gamemode=!spectator] rpg_ex_xp 3
particle end_rod ~ ~0.5 ~ 1.8 0.25 1.8 0.04 55 force
playsound minecraft:item.shield.block player @a[distance=..18] ~ ~ ~ 1 0.75
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
""" % {"msg": raw([txt("[银钉守界] ", "#DCE6EE", True), txt("圣钉替法阵承受了暴怒的一击。", "gray")])})

    # 6 色欲：把守阵者从中心向外拖；圣钉降低位移与稳定损失。
    write("inquest/counter/start6.mcfunction", """\
execute unless entity @s[tag=rpg.rite.nailed] run function rpg:inquest/stability/hit15
tag @s add rpg.rite.anchor.active
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^ ^-1.8
execute if entity @s[tag=rpg.rite.nailed] as @a[distance=..7,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^ ^0.8
tag @s remove rpg.rite.anchor.active
effect give @a[distance=..10,gamemode=!spectator] minecraft:nausea 5 0 true
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
playsound minecraft:entity.allay.ambient_with_item hostile @a[distance=..20] ~ ~ ~ 1 0.45
""" % {"msg": raw([txt("[反仪式·色欲] ", "#D596F2", True), txt("贝利尔诱使守阵者背离法阵中心。", "gray")])})

    # 7 贪婪：点击支付三种赎金之一，否则倒计时结束扣稳定。
    write("inquest/counter/start7.mcfunction", """\
scoreboard players set @s rpg_ex_kind 7
scoreboard players set @s rpg_ex_ransom 1
scoreboard players set @s rpg_ex_ctime 200
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
playsound minecraft:block.vault.activate hostile @a[distance=..20] ~ ~ ~ 1 0.65
""" % {"msg": raw([
        txt("[反仪式·贪婪] ", "#FFD85A", True), txt("玛门暂停宣判，要求赎金： ", "gray"),
        txt("[支付3级]", "aqua", True, click="/trigger rpg_ex_choice set 11"), txt("  "),
        txt("[献出4心]", "red", True, click="/trigger rpg_ex_choice set 12"), txt("  "),
        txt("[交出金锭]", "gold", True, click="/trigger rpg_ex_choice set 13")])})
    write("inquest/counter/mammon_wait.mcfunction", """\
scoreboard players remove @s rpg_ex_ctime 1
particle wax_on ~ ~0.8 ~ 0.8 0.25 0.8 0.03 3 normal
execute if score @s rpg_ex_ctime matches ..0 run function rpg:inquest/counter/mammon_default
""")
    write("inquest/counter/mammon_default.mcfunction", """\
scoreboard players set @s rpg_ex_kind 0
scoreboard players set @s rpg_ex_ransom 0
function rpg:inquest/stability/hit25
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
""" % {"msg": raw([txt("[逾期加征] ", "dark_red", True), txt("无人付账，玛门从法阵本身收取代价。", "gray")])})
    write("inquest/counter/mammon_paid.mcfunction", """\
scoreboard players set @s rpg_ex_kind 0
scoreboard players set @s rpg_ex_ransom 0
scoreboard players set @s rpg_ex_counter 220
function rpg:inquest/stability/restore
tellraw @a[distance=..16,gamemode=!spectator] %(msg)s
""" % {"msg": raw([txt("[赎金已付] ", "#FFD85A", True), txt("账目暂平，宣判继续。", "gray")])})


def build_choices():
    write("inquest/choice/ransom.mcfunction", """\
execute if score @s rpg_ex_choice matches 11 if entity @s[level=3..] run return run function rpg:inquest/choice/ransom_xp
execute if score @s rpg_ex_choice matches 11 unless entity @s[level=3..] run tellraw @s %(xp)s
execute if score @s rpg_ex_choice matches 12 if score @s health matches 9.. run return run function rpg:inquest/choice/ransom_hp
execute if score @s rpg_ex_choice matches 12 unless score @s health matches 9.. run tellraw @s %(hp)s
execute if score @s rpg_ex_choice matches 13 if items entity @s inventory.* minecraft:gold_ingot run return run function rpg:inquest/choice/ransom_gold
execute if score @s rpg_ex_choice matches 13 unless items entity @s inventory.* minecraft:gold_ingot run tellraw @s %(gold)s
""" % {
        "xp": raw([txt("[赎金失败] 需要至少 3 级经验。", "red")]),
        "hp": raw([txt("[赎金失败] 生命不足以献出 4 颗心。", "red")]),
        "gold": raw([txt("[赎金失败] 背包中没有金锭。", "red")])})
    write("inquest/choice/ransom_xp.mcfunction", "experience add @s -3 levels\nfunction rpg:inquest/choice/ransom_commit")
    write("inquest/choice/ransom_hp.mcfunction", "damage @s 8 minecraft:magic\nfunction rpg:inquest/choice/ransom_commit")
    write("inquest/choice/ransom_gold.mcfunction", "clear @s minecraft:gold_ingot 1\nfunction rpg:inquest/choice/ransom_commit")
    write("inquest/choice/ransom_commit.mcfunction", """\
tag @s add rpg.rite.chooser
execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..12,sort=nearest,limit=1,scores={rpg_ex_ransom=1..}] run function rpg:inquest/counter/mammon_paid
tag @s remove rpg.rite.chooser
scoreboard players add @s rpg_ex_xp 3
""")

    write("inquest/start_verdict.mcfunction", """\
tag @s add rpg.rite.anchor.active
scoreboard players set @s rpg_ex_stage 4
scoreboard players set @s rpg_ex_time 300
scoreboard players set @s rpg_ex_kind 0
scoreboard players set @s rpg_ex_ransom 0
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/boss_stage4
title @a[distance=..14,gamemode=!spectator] times 5 40 15
title @a[distance=..14,gamemode=!spectator] title %(title)s
title @a[distance=..14,gamemode=!spectator] subtitle %(sub)s
tellraw @a[distance=..14,gamemode=!spectator] %(choices)s
playsound minecraft:block.end_portal.spawn player @a[distance=..28] ~ ~ ~ 0.8 1.5
tag @s remove rpg.rite.anchor.active
""" % {
        "title": raw([txt("Ⅳ · 裁　决", "#FFF2A8", True)]),
        "sub": raw([txt("选择恶魔离开此世的方式", "white")]),
        "choices": raw([
            txt("[消灭]", "#FF6B5E", True, click="/trigger rpg_ex_choice set 1"), txt("  "),
            txt("[放逐]", "#FFF2A8", True, click="/trigger rpg_ex_choice set 2"), txt("  "),
            txt("[封印]", "#62D9E8", True, click="/trigger rpg_ex_choice set 3"), txt("  "),
            txt("[契约]", "#D596F2", True, click="/trigger rpg_ex_choice set 4")])})

    write("inquest/choice/final.mcfunction", """\
tag @s add rpg.rite.chooser
execute if score @s rpg_ex_choice matches 1 at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/eliminate
execute if score @s rpg_ex_choice matches 2 at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/banish
execute if score @s rpg_ex_choice matches 3 if items entity @s inventory.* minecraft:soul_lantern[minecraft:custom_data~{rpg_lantern:1b}] if entity @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,scores={rpg_ex_stage=4}] run tag @s add rpg.rite.choice.ok
execute if score @s rpg_ex_choice matches 3 if entity @s[tag=rpg.rite.choice.ok] run function rpg:inquest/choice/seal
execute if score @s rpg_ex_choice matches 3 unless entity @s[tag=rpg.rite.choice.ok] run tellraw @s %(lantern)s
execute if score @s rpg_ex_choice matches 4 at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/pact
tag @s remove rpg.rite.choice.ok
tag @s remove rpg.rite.chooser
""" % {"lantern": raw([txt("[封印失败] 需要一盏封魔灯，并站在裁决法阵十格内。", "red")])})
    write("inquest/choice/seal.mcfunction", """\
clear @s minecraft:soul_lantern[minecraft:custom_data~{rpg_lantern:1b}] 1
execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/seal
""")

    write("inquest/outcome/banish.mcfunction", """\
tag @s add rpg.rite.anchor.active
scoreboard players add @a[tag=rpg.rite.chooser,distance=..10] rpg_ex_xp 20
tellraw @a[distance=..20,gamemode=!spectator] %(msg)s
function rpg:inquest/anchor_success
""" % {"msg": raw([txt("[裁决·放逐] ", "#FFF2A8", True), txt("完整判词将恶魔逐离此世。", "gray")])})

    write("inquest/outcome/eliminate.mcfunction", """\
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/outcome/eliminate_boss
particle explosion ~ ~0.7 ~ 0.4 0.3 0.4 0.04 3 force
playsound minecraft:entity.wither.spawn hostile @a[distance=..32] ~ ~ ~ 0.8 1.25
kill @s
""")
    write("inquest/outcome/eliminate_boss.mcfunction", """\
scoreboard players set @s rpg_ex_stage 5
data merge entity @s {Health:560f,CustomNameVisible:1b}
execute if entity @a[tag=rpg.rite.chooser,distance=..14,scores={rpg_ex_path=1,rpg_ex_lvl=4..}] run data merge entity @s {Health:500f}
tag @s remove rpg.exorcism.bound
tag @s remove rpg.exorcism.visible
effect clear @s minecraft:resistance
effect clear @s minecraft:slowness
effect clear @s minecraft:glowing
effect give @s minecraft:strength 20 1 true
effect give @s minecraft:speed 20 1 true
execute on passengers run tag @s add rpg.outcome.eliminate
execute on passengers run scoreboard players operation @s rpg_dm_lord = @e[type=minecraft:vindicator,tag=rpg.rite.subject,limit=1] rpg_dm_lord
scoreboard players add @a[tag=rpg.rite.chooser,distance=..14] rpg_ex_xp 8
tellraw @a[distance=..24,gamemode=!spectator] %(msg)s
""" % {"msg": raw([txt("[裁决·消灭] ", "#FF6B5E", True), txt("仪式解除锁血；恶魔以 560 生命狂暴复苏。", "gray")])})

    # 上一行复制 lord 需要一个临时 subject 标签。
    # outcome/eliminate 在调用前由 anchor 给目标打标，调用后清理（见 patch_runtime）。
    relics = {}
    cores = {}
    for q in LORDS:
        relics[q["n"]] = item("echo_shard", "封印遗物 · " + q["who"], q["colour"],
                              ["封魔灯中的罪性残魂", "长期携带可能挣脱封印并重新降临"],
                              "holy_weapon_tag:1b,rpg_sealed:1b,rpg_lord:%d" % q["n"])
        cores[q["n"]] = item("nether_star", "武器核心 · " + q["who"], q["colour"],
                             ["以消灭结局取得的完整罪核", "可用于后续罪器锻造"],
                             "rpg_weapon_core:1b,rpg_lord:%d" % q["n"])
        write("inquest/give/relic%d.mcfunction" % q["n"],
              "give @s %s" % relics[q["n"]])
        write("inquest/give/core%d.mcfunction" % q["n"],
              "give @s %s" % cores[q["n"]])

    seal_lines = []
    pact_lines = []
    drop_lines = []
    weapon_lines = (read("command/give/weapon.mcfunction") + "\n" +
                    read("command/give/extra.mcfunction")).splitlines()
    for q in LORDS:
        n = q["n"]
        contract = next((line for line in read("pact/unsign%d.mcfunction" % n).splitlines()
                         if line.startswith("give @s ")), None)
        if not contract:
            raise RuntimeError("pact reward line missing: %d" % n)
        write("inquest/give/pact%d.mcfunction" % n, contract)
        weapon = next((line for line in weapon_lines
                       if line.startswith("give @a ") and "devil_tag:1b" in line
                       and ('\"text\":\"%s\"' % q["who"]) in line), None)
        if not weapon:
            raise RuntimeError("sin weapon reward line missing: %d" % n)
        write("inquest/give/pact_weapon%d.mcfunction" % n,
              weapon.replace("give @a ", "give @s ", 1))
        seal_lines.append("execute if score @s rpg_dm_lord matches %d as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/relic%d" % (n, n))
        pact_lines.append("execute if score @s rpg_dm_lord matches %d as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact%d" % (n, n))
        pact_lines.append("execute if score @s rpg_dm_lord matches %d as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact_weapon%d" % (n, n))
        drop_lines.append("execute if score @s rpg_dm_lord matches %d as @p[distance=..20] run function rpg:inquest/give/core%d" % (n, n))
    common_finish = """
execute on passengers run kill @s
particle sculk_soul ~ ~1 ~ 1.2 1.2 1.2 0.12 80 force
kill @s
"""
    write("inquest/outcome/seal_boss.mcfunction", "\n".join(seal_lines) + "\n" + """\
tag @a[tag=rpg.rite.chooser,distance=..14] add rpg.seal.carrier
scoreboard players add @a[tag=rpg.rite.chooser,distance=..14] rpg_ex_xp 18
scoreboard players add @a[tag=rpg.rite.chooser,distance=..14] rpg_taint 5
""" + common_finish)
    write("inquest/outcome/pact_boss.mcfunction", "\n".join(pact_lines) + "\n" + """\
scoreboard players add @a[tag=rpg.rite.chooser,distance=..14] rpg_ex_xp 15
scoreboard players add @a[tag=rpg.rite.chooser,distance=..14] rpg_taint 25
""" + common_finish)
    write("inquest/outcome/seal.mcfunction", """\
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/outcome/seal_boss
tellraw @a[distance=..20,gamemode=!spectator] %(msg)s
particle soul_fire_flame ~ ~0.8 ~ 1.1 0.6 1.1 0.08 80 force
playsound minecraft:block.respawn_anchor.charge player @a[distance=..24] ~ ~ ~ 1 1.4
kill @s
""" % {"msg": raw([txt("[裁决·封印] ", "#62D9E8", True), txt("残魂已收入封魔灯；封印并非永恒。", "gray")])})
    write("inquest/outcome/pact.mcfunction", """\
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/outcome/pact_boss
tellraw @a[distance=..20,gamemode=!spectator] %(msg)s
particle sculk_charge_pop ~ ~0.8 ~ 1.1 0.7 1.1 0.1 90 force
playsound minecraft:block.end_portal.spawn hostile @a[distance=..28] ~ ~ ~ 0.8 0.6
kill @s
""" % {"msg": raw([txt("[裁决·契约] ", "#D596F2", True), txt("恶魔以柱之书留下力量；接受者增加 25 魔化。", "gray")])})
    write("inquest/outcome/eliminate_drop.mcfunction", "\n".join(drop_lines) + "\n" + """\
scoreboard players add @a[distance=..20,gamemode=!spectator] rpg_ex_xp 25
tellraw @a[distance=..24,gamemode=!spectator] %(msg)s
function rpg:taint/demon_boom
""" % {"msg": raw([txt("[裁决·消灭] ", "#FF6B5E", True), txt("恶魔形体崩解，留下完整武器核心。", "gray")])})


def patch_runtime():
    # 每位玩家原本就会进入 taint；在同一次遍历内完成职业与触发器处理。
    patch_once("taint/taint.mcfunction", "", "") if False else None
    src = read("taint/taint.mcfunction").rstrip()
    if "function rpg:inquest/player_tick" not in src:
        write("taint/taint.mcfunction", src + "\nfunction rpg:inquest/player_tick")

    src = read("exorcism.mcfunction").rstrip()
    block = """
# 反仪式临时实体均有显式类型、标签与存在性守卫。
execute if entity @e[type=minecraft:armor_stand,tag=rpg.counter.name,limit=1] run execute as @e[type=minecraft:armor_stand,tag=rpg.counter.name] at @s run function rpg:inquest/counter/name_tick
"""
    if "counter/name_tick" not in src:
        write("exorcism.mcfunction", src + "\n" + block.strip())

    # Any ritual failure path must also remove temporary counter-rite actors.
    # This covers timeout, orphaned anchors and ordinary interruption without
    # leaving attackable false names or equipment-copying husks in the world.
    src = read("inquest/fail.mcfunction").rstrip()
    cleanup = """
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..12]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14]
"""
    if "tag=rpg.counter.name" not in src:
        write("inquest/fail.mcfunction", src + "\n" + cleanup.strip())

    # These anchor-owned exits can occur without a surviving bound boss, so
    # they cannot rely on fail.mcfunction to perform the cleanup.
    for rel in ("inquest/anchor_orphan.mcfunction",
                "inquest/anchor_timeout.mcfunction"):
        src = read(rel)
        if "tag=rpg.counter.name" not in src:
            write(rel, src.replace("kill @s", cleanup.strip() + "\nkill @s", 1))

    # A counter-rite may begin on the same tick that channel progress reaches
    # zero.  Clear its actors before stage 4 disables counter ticking.
    src = read("inquest/start_verdict.mcfunction")
    if "tag=rpg.counter.name" not in src:
        needle = "scoreboard players set @s rpg_ex_kind 0"
        write("inquest/start_verdict.mcfunction",
              src.replace(needle, cleanup.strip() + "\n" + needle, 1))

    # 调查、真名与媒介都是阅历来源；真名同时生成可共享的残页。
    for q in LORDS:
        n = q["n"]
        for i in range(1, 6):
            rel = "inquest/clue/%d_%d.mcfunction" % (n, i)
            src = read(rel)
            needle = "tag @s add rpg.clue.%d.%d\n" % (n, i)
            if "scoreboard players add @s rpg_ex_xp 4" not in src:
                write(rel, src.replace(needle, needle + "scoreboard players add @s rpg_ex_xp 4\n", 1))
        rel = "inquest/reveal/%d.mcfunction" % n
        src = read(rel)
        if "inquest/give/page%d" % n not in src:
            write(rel, src.rstrip() + "\nscoreboard players add @s rpg_ex_xp 8\nfunction rpg:inquest/give/page%d" % n)
        rel = "inquest/offer/%d.mcfunction" % n
        src = read(rel)
        needle = "function rpg:inquest/consume_offer\n"
        if "scoreboard players add @a[distance=..8,gamemode=!spectator] rpg_ex_xp 6" not in src:
            write(rel, src.replace(needle, needle + "scoreboard players add @a[distance=..8,gamemode=!spectator] rpg_ex_xp 6\n", 1))

        rel = "inquest/anchor_bind/%d.mcfunction" % n
        src = read(rel).rstrip()
        init = """
scoreboard players set @s rpg_ex_stab 100
execute store result score @s rpg_ex_counter run random value 140..220
scoreboard players set @s rpg_ex_kind 0
scoreboard players set @s rpg_ex_ctime 0
scoreboard players set @s rpg_ex_ransom 0
scoreboard players set @s rpg_ex_slots 1
scoreboard players set @s rpg_ex_toolcd 0
execute if entity @a[distance=..10,gamemode=!spectator,scores={rpg_ex_lvl=5..}] run scoreboard players set @s rpg_ex_slots 2
"""
        if "rpg_ex_stab 100" not in src:
            write(rel, src + "\n" + init.strip())

    # 活动法阵：工具、冷却、反仪式、稳定度全部在本法阵上下文结算。
    write("inquest/anchor_tick.mcfunction", """\
scoreboard players set #bound_found rpg_ex_tmp 0
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run scoreboard players set #bound_found rpg_ex_tmp 1
execute if score #bound_found rpg_ex_tmp matches 0 run return run function rpg:inquest/anchor_orphan
scoreboard players remove @s rpg_totem 1
execute if score @s rpg_totem matches ..0 run return run function rpg:inquest/anchor_timeout
execute if score @s rpg_ex_toolcd matches 1.. run scoreboard players remove @s rpg_ex_toolcd 1
particle dust{color:[1.0,0.91,0.52],scale:0.7} ~ ~0.75 ~ 0.28 0.35 0.28 0.01 1 normal
execute if score @s rpg_ex_stage matches 2..3 run function rpg:inquest/tool/scan
execute if score @s rpg_ex_stage matches 2..3 run function rpg:inquest/counter/tick
execute if score @s rpg_ex_stab matches ..0 run return run function rpg:inquest/anchor_collapse
execute if score @s rpg_ex_ransom matches 1.. run return run function rpg:inquest/counter/mammon_wait
execute if score @s rpg_ex_stage matches 2 run return run function rpg:inquest/anchor_stage2
execute if score @s rpg_ex_stage matches 3 run return run function rpg:inquest/anchor_stage3
execute if score @s rpg_ex_stage matches 4 run return run function rpg:inquest/anchor_stage4
tag @s remove rpg.rite.anchor.active
""")

    # 真名残页可让队友代为守阵；疾行法阵和秘仪大师各再推进一刻。
    stage3 = ["scoreboard players set #channel rpg_ex_tmp 0"]
    for q in LORDS:
        n = q["n"]
        stage3 += [
            "execute if score @s rpg_dm_lord matches %(n)d if entity @a[tag=rpg.name.%(n)d,distance=..6,gamemode=!spectator] run scoreboard players set #channel rpg_ex_tmp 1" % q,
            "execute if score @s rpg_dm_lord matches %(n)d as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:%(n)d}] run scoreboard players set #channel rpg_ex_tmp 1" % q]
    stage3 += [
        "execute if score #channel rpg_ex_tmp matches 0 run scoreboard players set @s rpg_ex_time 100",
        "execute if score #channel rpg_ex_tmp matches 1 run scoreboard players remove @s rpg_ex_time 1",
        "execute if score #channel rpg_ex_tmp matches 1 if entity @s[tag=rpg.layout.haste] run scoreboard players remove @s rpg_ex_time 1",
        "execute if score #channel rpg_ex_tmp matches 1 if entity @a[distance=..6,gamemode=!spectator,scores={rpg_ex_path=3,rpg_ex_lvl=4..}] run scoreboard players remove @s rpg_ex_time 1",
        "execute if score @s rpg_ex_time matches 80 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 0.9",
        "execute if score @s rpg_ex_time matches 60 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 1.05",
        "execute if score @s rpg_ex_time matches 40 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 1.2",
        "execute if score @s rpg_ex_time matches 20 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 1.4",
        "execute if score #channel rpg_ex_tmp matches 1 run particle end_rod ~ ~0.8 ~ 0.45 0.35 0.45 0.025 3 normal",
        "execute if score @s rpg_ex_time matches ..0 run return run function rpg:inquest/start_verdict",
        "tag @s remove rpg.rite.anchor.active"]
    write("inquest/anchor_stage3.mcfunction", "\n".join(stage3))
    write("inquest/anchor_stage4.mcfunction", """\
scoreboard players remove @s rpg_ex_time 1
particle end_rod ~ ~0.9 ~ 0.9 0.55 0.9 0.05 5 force
particle soul_fire_flame ~ ~0.7 ~ 0.65 0.4 0.65 0.04 3 force
execute if score @s rpg_ex_time matches 200 run tellraw @a[distance=..14,gamemode=!spectator] %(again)s
execute if score @s rpg_ex_time matches ..0 run return run function rpg:inquest/outcome/banish
tag @s remove rpg.rite.anchor.active
""" % {"again": raw([txt("[裁决尚待] ", "#FFF2A8", True), txt("点击：", "gray"),
                           txt("消灭", "#FF6B5E", True, click="/trigger rpg_ex_choice set 1"), txt(" / "),
                           txt("放逐", "#FFF2A8", True, click="/trigger rpg_ex_choice set 2"), txt(" / "),
                           txt("封印", "#62D9E8", True, click="/trigger rpg_ex_choice set 3"), txt(" / "),
                           txt("契约", "#D596F2", True, click="/trigger rpg_ex_choice set 4")])})
    write("inquest/boss_stage4.mcfunction", """\
scoreboard players set @s rpg_ex_stage 4
scoreboard players set @s rpg_ex_time 300
data merge entity @s {Health:420f,CustomNameVisible:1b}
""")

    # 消灭路线恢复正常战斗；死亡探针负责掉落核心后继续原临死冲击。
    advent = read("taint/advent_tick.mcfunction").replace(
        "scores={rpg_ex_stage=2..}] run return 0",
        "scores={rpg_ex_stage=2..4}] run return 0")
    write("taint/advent_tick.mcfunction", advent)
    soul = read("taint/demon_soul.mcfunction")
    needle = "execute if score #ride rpg_fall matches 0 at @s run function rpg:taint/demon_boom"
    replacement = ("execute if score #ride rpg_fall matches 0 if entity @s[tag=rpg.outcome.eliminate] at @s run return run function rpg:inquest/outcome/eliminate_drop\n" + needle)
    if "outcome/eliminate_drop" not in soul:
        write("taint/demon_soul.mcfunction", soul.replace(needle, replacement, 1))

    # 修正 eliminate_boss 中的主体复制：先给 boss 临时标签，再拷给乘客。
    rel = "inquest/outcome/eliminate_boss.mcfunction"
    src = read(rel)
    old = "execute on passengers run scoreboard players operation @s rpg_dm_lord = @e[type=minecraft:vindicator,tag=rpg.rite.subject,limit=1] rpg_dm_lord"
    new = "tag @s add rpg.rite.subject\nexecute on passengers run scoreboard players operation @s rpg_dm_lord = @e[type=minecraft:vindicator,tag=rpg.rite.subject,limit=1] rpg_dm_lord\ntag @s remove rpg.rite.subject"
    write(rel, src.replace(old, new))

    # 浓缩圣水沿用原池逻辑，多洗一层魔化。
    aec = read("rite/aec.mcfunction").rstrip()
    if "16773320" not in aec:
        aec += "\nexecute if data entity @s {potion_contents:{custom_color:16773320}} run tag @s add rpg.holy_water\nexecute if data entity @s {potion_contents:{custom_color:16773320}} run tag @s add rpg.holy_water.strong"
        write("rite/aec.mcfunction", aec)
    pool = read("rite/pool_beat.mcfunction")
    needle = "execute as @a[distance=..4] run scoreboard players remove @s rpg_taint 1"
    if "rpg.holy_water.strong" not in pool:
        pool = pool.replace(needle, needle + "\nexecute if entity @s[tag=rpg.holy_water.strong] as @a[distance=..4] run scoreboard players remove @s rpg_taint 1", 1)
        write("rite/pool_beat.mcfunction", pool)


def build_tags_and_debug():
    write_data("rpg/tags/item/rite_media.json", {"values": [q["item"] for q in LORDS]})
    write("inquest/debug/reset_career.mcfunction", """\
scoreboard players set @s rpg_ex_xp 0
scoreboard players set @s rpg_ex_lvl 1
scoreboard players set @s rpg_ex_path 0
scoreboard players set @s rpg_ex_seen 0
tag @s remove rpg.ex.claim2
tag @s remove rpg.ex.claim3
tag @s remove rpg.ex.claim4
tag @s remove rpg.ex.claim5
tellraw @s %(msg)s
""" % {"msg": raw([txt("[驱魔师档案] ", "#FFF2A8", True), txt("职业阅历、路线与领取记录已重置。", "gray")])})


def validate_output():
    scoreboard = read("command/soreboard.mcfunction")
    for name, criterion in OBJECTIVES.items():
        if scoreboard.count("scoreboard objectives add %s %s" % (name, criterion)) != 1:
            raise RuntimeError("objective mismatch: " + name)
    for n in range(1, 8):
        if "function rpg:inquest/counter/start%d" % n not in read("inquest/counter/dispatch.mcfunction"):
            raise RuntimeError("counter route missing: %d" % n)
        if "scoreboard players add @s rpg_ex_xp 4" not in read("inquest/clue/%d_1.mcfunction" % n):
            raise RuntimeError("career clue reward missing: %d" % n)
        if "inquest/give/page%d" % n not in read("inquest/reveal/%d.mcfunction" % n):
            raise RuntimeError("true-name page missing: %d" % n)
        for kind in ("relic", "core"):
            if not os.path.isfile(path("inquest/give/%s%d.mcfunction" % (kind, n))):
                raise RuntimeError("verdict catalogue item missing: %s%d" % (kind, n))
        for kind in ("page", "relic", "core"):
            styled = read("inquest/give/%s%d.mcfunction" % (kind, n))
            if ('"text":"[驱魔]","italic":false' not in styled or
                    styled.count('"text":"+------------------+","italic":false') != 2):
                raise RuntimeError("exorcism item text style mismatch: %s%d" % (kind, n))
    for kind in ("nail", "bell", "incense", "lantern", "strong_water",
                 "chalk1", "chalk2", "chalk3"):
        styled = read("inquest/give/%s.mcfunction" % kind)
        if ('"text":"[驱魔]","italic":false' not in styled or
                styled.count('"text":"+------------------+","italic":false') != 2):
            raise RuntimeError("exorcism item text style mismatch: " + kind)
    if "scores={rpg_ex_stage=2..4}" not in read("taint/advent_tick.mcfunction"):
        raise RuntimeError("eliminate combat stage is still frozen")
    if "function rpg:inquest/start_verdict" not in read("inquest/anchor_stage3.mcfunction"):
        raise RuntimeError("verdict route missing")
    if read("inquest/start_verdict.mcfunction").count("/trigger rpg_ex_choice set ") != 4:
        raise RuntimeError("four verdict choices missing")
    if "rpg_sealed:1b" in read("command/index_player.mcfunction"):
        raise RuntimeError("sealed relic inventory scan is still on the per-tick index")
    if "rpg_seal_i matches 100.." not in read("inquest/player_tick.mcfunction"):
        raise RuntimeError("sealed relic low-frequency reconciliation missing")
    if "tag @a[tag=rpg.rite.chooser,distance=..14] add rpg.seal.carrier" not in read("inquest/outcome/seal_boss.mcfunction"):
        raise RuntimeError("sealed relic receiver is not indexed immediately")
    fail = read("inquest/fail.mcfunction")
    if "tag=rpg.counter.name" not in fail or "tag=rpg.counter.clone" not in fail:
        raise RuntimeError("counter-rite failure cleanup missing")
    for rel in ("inquest/anchor_orphan.mcfunction",
                "inquest/anchor_timeout.mcfunction",
                "inquest/start_verdict.mcfunction"):
        cleanup_src = read(rel)
        if "tag=rpg.counter.name" not in cleanup_src or "tag=rpg.counter.clone" not in cleanup_src:
            raise RuntimeError("counter-rite lifecycle cleanup missing: " + rel)
    place_dir = path("inquest/tool/place")
    placed = [name for name in os.listdir(place_dir) if name.endswith(".mcfunction")]
    if len(placed) != 16:
        raise RuntimeError("ritual ground display count mismatch: %d" % len(placed))
    if "tool/prop_tick" not in read("exorcism.mcfunction"):
        raise RuntimeError("ritual prop lifetime hook missing")
    for rel in ("inquest/tool/nail_item.mcfunction",
                "inquest/tool/chalk1_item.mcfunction",
                "inquest/tool/chalk2_item.mcfunction",
                "inquest/tool/chalk3_item.mcfunction",
                "inquest/tool/incense_item.mcfunction",
                "inquest/tool/bell_anchor.mcfunction",
                "inquest/choice/seal.mcfunction",
                "rite/light.mcfunction",
                "inquest/anchor_stage3.mcfunction"):
        if "tool/place/" not in read(rel):
            raise RuntimeError("ritual prop route missing: " + rel)
    for rel in ("inquest/fail.mcfunction",
                "inquest/anchor_success.mcfunction",
                "inquest/anchor_timeout.mcfunction",
                "inquest/anchor_orphan.mcfunction",
                "inquest/anchor_collapse.mcfunction",
                "inquest/outcome/eliminate.mcfunction",
                "inquest/outcome/seal.mcfunction",
                "inquest/outcome/pact.mcfunction"):
        if "tool/cleanup" not in read(rel):
            raise RuntimeError("ritual prop cleanup missing: " + rel)


def main():
    add_objectives()
    build_give_functions()
    build_career()
    build_player_runtime()
    build_stability()
    build_tool_runtime()
    build_counters()
    build_choices()
    build_tags_and_debug()
    patch_runtime()
    build_ritual_props()
    validate_output()
    print("exorcism expansion: 7 counter-rites, 4 verdicts, 5 career levels / 3 paths")
    print("exorcism expansion: pages, nail, bell, incense, lantern, 3 chalks, strong holy water")
    print("exorcism expansion: 16 ritual ground displays, rite-bound cleanup + timed lantern")


if __name__ == "__main__":
    main()
