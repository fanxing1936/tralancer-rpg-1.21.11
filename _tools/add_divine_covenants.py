# -*- coding: utf-8 -*-
"""Build the Old/New divine covenants and the Daath transformation rite.

This runs after the original Kabbalah generator.  Ten filled Sephiroth award
the Old Covenant; placing the True Cross at Daath pulls every offering inward,
consumes the tree and upgrades the book to the New Covenant.
"""

import io
import json
import math
import os
import shutil
import sys

import rpg_ui_style as ui


DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
RP = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "../resourcepack")
HERE = os.path.dirname(os.path.abspath(__file__))
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement")
LOOT = os.path.join(DP, "data/rpg/loot_table")

OLD_CMD = 1110038
NEW_CMD = 1110039
CROSS_CMD = 1110001
OLD_COLOUR = ui.HOLY_DARK
OLD_LIGHT = ui.HOLY_LIGHT
NEW_COLOUR = ui.CYAN
NEW_LIGHT = ui.CYAN_LIGHT
USE = ('food={nutrition:0,saturation:0f,can_always_eat:1b},'
       'consumable={consume_seconds:100180f,animation:"block",'
       'sound:"minecraft:block.enchantment_table.use",'
       'has_consume_particles:false,on_consume_effects:[]}')


def pfunc(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep))


def read(rel):
    with io.open(pfunc(rel), encoding="utf-8") as handle:
        return handle.read()


def write(rel, content):
    target = pfunc(rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    content = "\n".join(line.rstrip() for line in content.splitlines())
    with io.open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content.rstrip("\n") + "\n")


def remove_function(rel):
    target = pfunc(rel)
    if os.path.isfile(target):
        os.remove(target)


def write_json(root, rel, value):
    target = os.path.join(root, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def comp(text, color="white", bold=False):
    return ui.comp(text, color, bold)


def row(*parts):
    return ui.row(*parts)


def lore(rows):
    return ui.lore(rows)


def covenant_profile(kind):
    if kind == 1:
        return {
            "title": "旧约", "colour": OLD_COLOUR, "light": OLD_LIGHT,
            "cmd": OLD_CMD, "flag": "rpg_divine_old",
            "origin": "十源质归位后，显于人间的上半部律法",
        }
    return {
        "title": "新约", "colour": NEW_COLOUR, "light": NEW_LIGHT,
        "cmd": NEW_CMD, "flag": "rpg_divine_new",
        "origin": "十源质与真·十字架归一后的权柄见证",
    }


def covenant_lore_rows(kind, signed):
    p = covenant_profile(kind)
    rows = [[comp(p["origin"], ui.GRAY)]]
    if signed:
        if kind == 1:
            rows.append([comp("长按右键动用契约之力（冷却 30 秒）", ui.GRAY)])
        else:
            rows.append([comp("长按右键施展净光；潜行长按展开敕界", ui.GRAY)])
            rows.append([comp("两种权能分别回响 20 / 30 秒", ui.DARK_GRAY)])
        rows.append([comp("在燃着的驱魔图腾旁长按则", ui.GRAY),
                     comp("解约", ui.RED, True)])
    else:
        rows.append([comp("长按右键与上帝立约", ui.GRAY)])

    # Mirror the seven-pillar contract's source/instruction -> powers hierarchy.
    rows.append([comp(ui.RULE_TEXT, ui.WHITE)])
    if kind == 1:
        rows += [
            [ui.label("恩赐"), comp("　每 20 秒获得 1 秒生命恢复 I", OLD_LIGHT)],
            [ui.label("力量"), comp("[十诫净界]", OLD_COLOUR, True)],
            [comp("　净化 10 格内所有恶魔，造成 20% 最大生命值伤害", ui.GRAY)],
            [comp("　生命不高于 25% 的恶魔直接斩杀", ui.GRAY)],
            [ui.label("律法"), comp("　每轮魔化结算抵消 2 点", OLD_LIGHT)],
        ]
    else:
        rows += [
            [ui.label("权柄"), comp("　魔化由权柄完整度取代", NEW_LIGHT)],
            [ui.label("力量"), comp("[创世净光]", NEW_COLOUR, True)],
            [comp("　对前方恶魔造成 25% 最大生命值伤害", ui.GRAY)],
            [comp("　并追加 15 点基础伤害与审判印记", ui.GRAY)],
            [ui.label("敕界"), comp("[伊甸敕界]", OLD_LIGHT, True)],
            [comp("　潜行长按展开 8 格敕界，造成 15% 最大生命值伤害", ui.GRAY)],
            [comp("　并追加 10 点伤害；净化、恢复并庇护范围内同伴", ui.GRAY)],
            [ui.label("神佑"), comp("　免疫失明与黑暗", NEW_LIGHT)],
            [ui.label("赦免"), comp("　可无副作用动用七罪契约之力", OLD_LIGHT)],
            [comp("　手持七罪契约书使用（冷却 15 秒）", ui.DARK_GRAY)],
        ]
    rows.append([comp(ui.RULE_TEXT, ui.WHITE)])
    if signed:
        rows.append([comp("契约已立 · 在燃着的驱魔图腾旁可断约", p["light"])])
    else:
        rows.append([comp("立约前不会消耗此书", ui.DARK_GRAY)])
    return rows


def covenant_name_value(kind, signed):
    p = covenant_profile(kind)
    prefix = "[已立约]" if signed else "[契约]"
    return ui.row_value(comp(prefix, p["colour"], True),
                        comp(p["title"], ui.WHITE))


def covenant_components(kind, signed=False):
    p = covenant_profile(kind)
    custom_data = {"rpg_divine_pact": True, p["flag"]: True}
    if signed:
        custom_data["rpg_divine_signed"] = True
    return {
        "minecraft:custom_name": covenant_name_value(kind, signed),
        "minecraft:lore": ui.lore_value(covenant_lore_rows(kind, signed)),
        "minecraft:custom_model_data": {"floats": [float(p["cmd"])]},
        "minecraft:enchantment_glint_override": True,
        "minecraft:max_stack_size": 1,
        "minecraft:food": {"nutrition": 0, "saturation": 0.0,
                           "can_always_eat": True},
        "minecraft:consumable": {
            "consume_seconds": 100180.0, "animation": "block",
            "sound": "minecraft:block.enchantment_table.use",
            "has_consume_particles": False, "on_consume_effects": [],
        },
        "minecraft:custom_data": custom_data,
    }


def covenant_item(kind, signed):
    p = covenant_profile(kind)
    flag = "%s:1b" % p["flag"]
    data = "{rpg_divine_pact:1b,%s%s}" % (
        flag, ",rpg_divine_signed:1b" if signed else "")
    return ("minecraft:enchanted_book[custom_name=" +
            json.dumps(covenant_name_value(kind, signed), ensure_ascii=False,
                       separators=(",", ":")) +
            ",lore=" + lore(covenant_lore_rows(kind, signed)) +
            ",custom_model_data={floats:[%d.0f]},enchantment_glint_override=true," % p["cmd"] +
            "max_stack_size=1," + USE + ",custom_data=" + data + "]")


def cross_item():
    lines = [
        [comp("生命之树的第十一件见证", ui.GRAY)],
        [comp("十源质归位后，站入 ", ui.GRAY), comp("[Daath]", NEW_COLOUR, True),
         comp(" 圆心长按右键", ui.GRAY)],
        [comp("十源质将汇入真·十字架，并显化", ui.GRAY),
         comp("『新约』", NEW_COLOUR, True)],
    ]
    return ("minecraft:iron_nugget[custom_name=" +
            ui.item_name("[秘仪]", "真·十字架", ui.RITUAL, ui.WHITE) +
            ",lore=" + lore(lines) +
            ",custom_model_data={floats:[%d.0f]},enchantment_glint_override=true," % CROSS_CMD +
            "max_stack_size=1," + USE +
            ",custom_data={rpg_kabbalah_use:1b,rpg_true_cross:1b}]")


def patch_objectives_and_tick():
    rel = "command/soreboard.mcfunction"
    names = ("rpg_lt_divine", "rpg_lt_div_cd", "rpg_lt_div_max", "rpg_lt_div_t", "rpg_lt_regen",
             "rpg_lt_auth", "rpg_lt_hp", "rpg_lt_max", "rpg_lt_owner",
             "rpg_lt_gather", "rpg_lt_claim", "rpg_lt_migrate")
    src = "\n".join(line for line in read(rel).splitlines()
                    if not any(name in line for name in names)).rstrip()
    src += "\n" + "\n".join("scoreboard objectives add %s dummy" % n for n in names)
    src += "\nscoreboard players set #three rpg_lt_max 3"
    src += "\nscoreboard players set #four rpg_lt_max 4"
    src += "\nscoreboard players set #five rpg_lt_max 5"
    src += "\nscoreboard players set #twenty rpg_lt_max 20"
    src += "\nscoreboard players set #hundred rpg_lt_max 100"
    write(rel, src)

    rel = "exorcism.mcfunction"
    src = "\n".join(line for line in read(rel).splitlines()
                    if "rpg:divine/player_tick" not in line and
                    "上位契约玩家状态" not in line and
                    "rpg:divine/gather/step" not in line and
                    "Daath 汇聚动画" not in line)
    anchor = "execute as @a at @s run function rpg:taint/taint"
    src = src.replace(anchor,
                      "# 上位契约玩家状态先于魔化与 HUD 结算。\n"
                      "execute as @a at @s run function rpg:divine/player_tick\n" + anchor)
    src += ("\n\n# Daath 汇聚动画：只有正在转化的生命之树才进入。\n"
            "execute if entity @e[type=minecraft:marker,tag=rpg.lt.gathering,limit=1] "
            "run function rpg:divine/gather/step\n")
    # The previous implementation's all-round New Covenant blessing is retired.
    src = "\n".join(line for line in src.splitlines()
                    if "function rpg:ritual/life_tree/covenant_tick" not in line and
                    "新约常驻祝福" not in line)
    write(rel, src)


def build_advancement_and_trigger():
    write_json(ADV, "divine/covenant.json", {
        "criteria": {"use": {"trigger": "minecraft:using_item", "conditions": {
            "item": {"predicates": {"minecraft:custom_data": "{rpg_divine_pact:1b}"}}}}},
        "rewards": {"function": "rpg:divine/trigger"},
    })
    write("divine/trigger.mcfunction", """advancement revoke @s only rpg:divine/covenant
execute if score @s rpg_lt_div_t matches 1.. run return 0
scoreboard players set @s rpg_lt_div_t 8
execute if score @s rpg_lt_divine matches 0 run return run function rpg:divine/sign
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_divine_signed:1b}] run return run function rpg:divine/reissue
execute if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,distance=..6,limit=1] run return run function rpg:divine/renounce
execute if score @s rpg_lt_div_cd matches 1.. run return run function rpg:divine/cooling
execute if score @s rpg_lt_divine matches 1 run return run function rpg:divine/invoke_old
execute if score @s rpg_lt_divine matches 2 run return run function rpg:divine/invoke_new
""")
    write("divine/sign.mcfunction", """execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_divine_old:1b}] run return run function rpg:divine/sign_old
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_divine_new:1b}] run return run function rpg:divine/sign_new
""")
    write("divine/sign_old.mcfunction", """scoreboard players set @s rpg_lt_divine 1
scoreboard players set @s rpg_lt_regen 0
tag @s add rpg.divine.old
tag @s remove rpg.divine.new
item replace entity @s weapon.mainhand with %s
function rpg:divine/sign_vfx_old
tellraw @s %s
    """ % (covenant_item(1, True), row(
        ui.comp("[旧约] ", OLD_COLOUR, True),
        ui.comp("律法刻入灵魂；你与上帝立下了旧约。", ui.GRAY,
                italic=True))))
    write("divine/sign_new.mcfunction", """execute if entity @s[tag=rpg.pact] run function rpg:pact/burn
scoreboard players set @s rpg_lt_divine 2
scoreboard players set @s rpg_lt_auth 100
scoreboard players set @s rpg_taint 0
tag @s remove rpg.taint.full
tag @s remove rpg.divine.old
tag @s add rpg.divine.new
item replace entity @s weapon.mainhand with %s
function rpg:divine/sign_vfx_new
tellraw @s %s
    """ % (covenant_item(2, True), row(
        ui.comp("[新约] ", NEW_COLOUR, True),
        ui.comp("权与力重新合一；新约取代了一切污染。", ui.GRAY,
                italic=True))))
    write("divine/sign_vfx_old.mcfunction", """title @s times 10 60 20
title @s title %s
title @s subtitle %s
particle minecraft:flash{color:16771162} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:end_rod ~ ~1 ~ 0.7 0.9 0.7 0.12 100 force
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.75 1.45
""" % (row(comp("契 约 已 立", OLD_COLOUR, True)),
         row(comp("人与上帝 · 律法见证", OLD_LIGHT))))
    write("divine/sign_vfx_new.mcfunction", """title @s times 10 60 20
title @s title %s
title @s subtitle %s
particle minecraft:flash{color:15594751} ~ ~1 ~ 0 0 0 0 1 force
particle end_rod ~ ~1 ~ 0.7 0.9 0.7 0.12 100 force
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.75 1.45
""" % (row(comp("契 约 已 立", NEW_COLOUR, True)),
         row(comp("人与上帝 · 权柄见证", NEW_LIGHT))))
    write("divine/reissue.mcfunction", """execute if score @s rpg_lt_divine matches 1 if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_divine_old:1b}] run item replace entity @s weapon.mainhand with %s
execute if score @s rpg_lt_divine matches 2 if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_divine_new:1b}] run item replace entity @s weapon.mainhand with %s
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.55 1.4
""" % (covenant_item(1, True), covenant_item(2, True)))
    write("divine/cooling.mcfunction",
          "playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.55 0.65")


def build_old_power():
    write("divine/invoke_old.mcfunction", """scoreboard players set @s rpg_lt_div_cd 600
scoreboard players set @s rpg_lt_div_max 600
tag @s add rpg.divine.cast
execute as @e[tag=rpg.demon,distance=..10] at @s run function rpg:divine/damage/old_target
execute as @e[tag=rpg.demon.minion,tag=!rpg.demon,distance=..10] at @s run function rpg:divine/damage/old_target
execute as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,distance=..10] at @s run function rpg:divine/damage/old_target
tag @s remove rpg.divine.cast
particle minecraft:flash{color:16771482} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:totem_of_undying ~ ~1 ~ 5 1 5 0.08 130 force
particle minecraft:end_rod ~ ~0.8 ~ 4.8 0.5 4.8 0.03 90 force
playsound minecraft:block.beacon.power_select master @a[distance=..24] ~ ~ ~ 1 1.35
function rpg:hud/m59
""")
    write("divine/damage/old_target.mcfunction", """execute if entity @s[tag=rpg.exorcism.bound] run return run function rpg:divine/ritual/old
execute store result score @s rpg_lt_hp run data get entity @s Health 100
execute store result score @s rpg_lt_max run attribute @s minecraft:max_health get 100
scoreboard players operation @s rpg_lt_max /= #four rpg_lt_max
execute unless score @s rpg_ex_stage matches 1 if score @s rpg_lt_hp <= @s rpg_lt_max run return run function rpg:divine/damage/execute
execute store result score @s rpg_lt_max run attribute @s minecraft:max_health get 100
scoreboard players operation @s rpg_lt_max /= #five rpg_lt_max
execute if score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_stage1
execute unless score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_score
particle minecraft:enchanted_hit ~ ~1 ~ 0.5 0.8 0.5 0.1 24 force
""")
    write("divine/damage/execute.mcfunction", """particle minecraft:flash{color:16777215} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:soul_fire_flame ~ ~1 ~ 0.5 0.8 0.5 0.05 36 force
playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..20] ~ ~ ~ 0.8 1.6
execute if entity @a[tag=rpg.divine.cast,limit=1] run damage @s 100000 rpg:divine_light by @a[tag=rpg.divine.cast,limit=1,sort=nearest]
execute unless entity @a[tag=rpg.divine.cast,limit=1] run damage @s 100000 rpg:divine_light
""")
    write("divine/damage/apply_score.mcfunction", """scoreboard players operation @s rpg_lt_max /= #hundred rpg_lt_max
execute store result storage rpg:divine damage.amount int 1 run scoreboard players get @s rpg_lt_max
execute if score @s rpg_lt_max matches 1.. run function rpg:divine/damage/macro with storage rpg:divine damage
""")
    write("divine/damage/apply_stage1.mcfunction", """# 调查阶段保留 25% 生命底线，伤害仍会真实显示。
execute store result score @s rpg_lt_hp run data get entity @s Health 100
scoreboard players remove @s rpg_lt_hp 17500
execute if score @s rpg_lt_max > @s rpg_lt_hp run scoreboard players operation @s rpg_lt_max = @s rpg_lt_hp
execute if score @s rpg_lt_max matches 1.. run function rpg:divine/damage/apply_score
""")
    write("divine/damage/macro.mcfunction", """$execute if entity @a[tag=rpg.divine.cast,limit=1] run damage @s $(amount) rpg:divine_light by @a[tag=rpg.divine.cast,limit=1,sort=nearest]
$execute unless entity @a[tag=rpg.divine.cast,limit=1] run damage @s $(amount) rpg:divine_light
""")


def build_new_power_and_borrow():
    beam = []
    for d in range(1, 21):
        beam.append("particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^%d 0.10 0.10 0.10 0.01 4 force" % d)
        if d % 2 == 0:
            beam.append("particle end_rod ^ ^1 ^%d 0.14 0.14 0.14 0.01 2 force" % d)
        beam.append("execute positioned ^ ^1 ^%d as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target" % d)
        beam.append("execute positioned ^ ^1 ^%d as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target" % d)
        beam.append("execute positioned ^ ^1 ^%d as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target" % d)

    field_ring = []
    for radius, count, scale in ((3.0, 24, 1.0), (6.0, 36, 1.25)):
        for index in range(count):
            angle = math.tau * index / count
            x = math.cos(angle) * radius
            z = math.sin(angle) * radius
            field_ring.append(
                "particle dust{color:[0.38,0.85,0.91],scale:%.2f} ~%.3f ~0.08 ~%.3f 0 0 0 0 1 force"
                % (scale, x, z))

    write("divine/invoke_new.mcfunction", """# 新约双式：常态为创世净光，潜行为伊甸敕界。
execute if entity @s[nbt={Pose:"CROUCHING"}] run return run function rpg:divine/invoke_new_field
function rpg:divine/invoke_new_beam
""")
    write("divine/invoke_new_beam.mcfunction", """scoreboard players set @s rpg_lt_div_cd 400
scoreboard players set @s rpg_lt_div_max 400
tag @s add rpg.divine.cast
tag @e[tag=rpg.divine.hit] remove rpg.divine.hit
%s
tag @e[tag=rpg.divine.hit] remove rpg.divine.hit
tag @s remove rpg.divine.cast
particle minecraft:flash{color:8641023} ^ ^1 ^1 0 0 0 0 1 force
playsound minecraft:block.beacon.activate master @a[distance=..32] ~ ~ ~ 1 1.65
function rpg:hud/m60
""" % "\n".join(beam))
    write("divine/damage/new_target.mcfunction", """tag @s add rpg.divine.hit
execute if entity @s[tag=rpg.exorcism.bound] run return run function rpg:divine/ritual/beam
execute store result score @s rpg_lt_max run attribute @s minecraft:max_health get 100
scoreboard players operation @s rpg_lt_max /= #four rpg_lt_max
scoreboard players add @s rpg_lt_max 1500
execute if score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_stage1
execute unless score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_score
effect give @s minecraft:glowing 8 0 true
effect give @s minecraft:weakness 6 0 true
particle minecraft:flash{color:8641023} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:end_rod ~ ~1 ~ 0.45 0.7 0.45 0.04 30 force
""")
    write("divine/invoke_new_field.mcfunction", """scoreboard players set @s rpg_lt_div_cd 600
scoreboard players set @s rpg_lt_div_max 600
tag @s add rpg.divine.cast
execute as @e[tag=rpg.demon,distance=..8] at @s run function rpg:divine/damage/field_target
execute as @e[tag=rpg.demon.minion,tag=!rpg.demon,distance=..8] at @s run function rpg:divine/damage/field_target
execute as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,distance=..8] at @s run function rpg:divine/damage/field_target
tag @s remove rpg.divine.cast
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:blindness
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:darkness
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:wither
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:poison
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:slowness
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:weakness
effect give @a[distance=..8,gamemode=!spectator] minecraft:regeneration 6 1 true
effect give @a[distance=..8,gamemode=!spectator] minecraft:resistance 6 0 true
effect give @a[distance=..8,gamemode=!spectator] minecraft:absorption 6 1 true
%s
particle minecraft:flash{color:6482395} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:totem_of_undying ~ ~0.8 ~ 5.5 0.5 5.5 0.05 120 force
playsound minecraft:block.beacon.power_select master @a[distance=..32] ~ ~ ~ 1 0.85
playsound minecraft:block.amethyst_block.resonate master @a[distance=..24] ~ ~ ~ 0.8 1.55
function rpg:hud/m61
""" % "\n".join(field_ring))
    write("divine/damage/field_target.mcfunction", """execute if entity @s[tag=rpg.exorcism.bound] run return run function rpg:divine/ritual/field
execute store result score @s rpg_lt_max run attribute @s minecraft:max_health get 100
scoreboard players operation @s rpg_lt_max *= #three rpg_lt_max
scoreboard players operation @s rpg_lt_max /= #twenty rpg_lt_max
scoreboard players add @s rpg_lt_max 1000
execute if score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_stage1
execute unless score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_score
effect give @s minecraft:slowness 8 2 true
effect give @s minecraft:weakness 8 1 true
effect give @s minecraft:glowing 8 0 true
particle minecraft:enchanted_hit ~ ~1 ~ 0.8 0.8 0.8 0.12 35 force
particle minecraft:end_rod ~ ~0.8 ~ 0.6 0.7 0.6 0.04 24 force
""")
    branches = "\n".join(
        "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:%d}] run function rpg:pact/p%d" % (n, n)
        for n in range(1, 8))
    write("divine/borrow.mcfunction", """execute if score @s rpg_lt_div_cd matches 1.. run return run function rpg:divine/cooling
scoreboard players set @s rpg_lt_div_cd 300
scoreboard players set @s rpg_lt_div_max 300
tag @s add rpg.pact.cast
%s
tag @s remove rpg.pact.cast
particle minecraft:end_rod ~ ~1 ~ 0.4 0.7 0.4 0.05 25
function rpg:hud/m62
""" % branches)

    # New Covenant intercepts every seven-pillar book before sign/invoke logic.
    rel = "pact/trigger.mcfunction"
    src = "\n".join(line for line in read(rel).splitlines()
                    if "rpg_lt_divine matches 2" not in line)
    hook = "advancement revoke @s only rpg:item/pact"
    injection = (hook + "\nexecute if score @s rpg_lt_divine matches 2 "
                 "run return run function rpg:divine/borrow")
    src = src.replace(hook, injection)
    write(rel, src)


def build_damage_type_and_ritual_compat():
    """Make percentage damage exact and meaningful in every exorcism phase."""
    write_json(DP, "data/rpg/damage_type/divine_light.json", {
        "message_id": "divine_light",
        "scaling": "never",
        "exhaustion": 0.0,
        "effects": "hurt",
    })
    for tag_name in (
            "bypasses_armor", "bypasses_resistance",
            "bypasses_invulnerability", "bypasses_enchantments",
            "bypasses_shield"):
        write_json(DP, "data/minecraft/tags/damage_type/%s.json" % tag_name, {
            "replace": False,
            "values": ["rpg:divine_light"],
        })

    # Stage one is a real 700-health fight, while its 25% floor preserves the
    # investigation/true-name route instead of allowing a premature kill.
    rel = "inquest/stage1.mcfunction"
    src = read(rel)
    old_guard = ("data merge entity @s {Health:420f}\n"
                 "effect give @s minecraft:resistance 2 4 true")
    new_guard = ("# 调查阶段允许真实伤害；175 HP（700 的 25%）为仪式保护线。\n"
                 "execute store result score @s rpg_ex_hp run data get entity @s Health 100\n"
                 "execute if score @s rpg_ex_hp matches ..17499 run data merge entity @s {Health:175f}\n"
                 "effect give @s minecraft:resistance 2 0 true")
    if old_guard in src:
        src = src.replace(old_guard, new_guard, 1)
    write(rel, src)

    def ritual_route(name, amount, xp, colour, particle_colour, pitch):
        write("divine/ritual/%s.mcfunction" % name, """# 绑定阶段的神圣伤害转化为法阵稳定度，不再被 420 HP 回填吞没。
tag @s add rpg.divine.ritual_subject
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.divine.ritual_subject,limit=1,sort=nearest] rpg_rite_id run function rpg:divine/ritual/%s_apply
tag @s remove rpg.divine.ritual_subject
particle minecraft:flash{color:%d} ~ ~1 ~ 0 0 0 0 1 force
""" % (name, particle_colour))
        write("divine/ritual/%s_apply.mcfunction" % name, """scoreboard players add @s rpg_ex_stab %d
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
execute at @s run particle dust{color:%s,scale:1.1} ~ ~0.18 ~ 0.8 0.08 0.8 0.04 28 force
execute at @s run particle minecraft:end_rod ~ ~0.25 ~ 0.7 0.12 0.7 0.03 18 force
execute at @s run playsound minecraft:block.amethyst_block.resonate master @a[distance=..24] ~ ~ ~ 0.75 %.2f
execute at @s as @a[tag=rpg.divine.cast,distance=..24,sort=nearest,limit=1] run scoreboard players add @s rpg_ex_xp %d
""" % (amount, colour, pitch, xp))

    ritual_route("old", 20, 3, "[0.83,0.69,0.22]", 16771482, 1.15)
    ritual_route("beam", 25, 4, "[0.38,0.85,0.91]", 8641023, 1.55)
    ritual_route("field", 15, 2, "[0.91,0.96,1.0]", 6482395, 1.35)


def build_player_tick_hud_and_renounce():
    write("divine/player_tick.mcfunction", """scoreboard players add @s rpg_lt_divine 0
scoreboard players add @s rpg_lt_div_cd 0
scoreboard players add @s rpg_lt_div_max 0
scoreboard players add @s rpg_lt_div_t 0
scoreboard players add @s rpg_lt_regen 0
scoreboard players add @s rpg_lt_auth 0
scoreboard players add @s rpg_lt_claim 0
scoreboard players add @s rpg_lt_migrate 0
execute if score @s rpg_lt_div_cd matches 1.. if score @s rpg_lt_div_max matches ..0 if score @s rpg_lt_divine matches 1 run scoreboard players set @s rpg_lt_div_max 600
execute if score @s rpg_lt_div_cd matches 1.. if score @s rpg_lt_div_max matches ..0 if score @s rpg_lt_divine matches 2 run scoreboard players set @s rpg_lt_div_max 400
execute if score @s rpg_lt_div_cd matches 1.. run scoreboard players remove @s rpg_lt_div_cd 1
execute unless score @s rpg_lt_div_cd matches 1.. run scoreboard players set @s rpg_lt_div_max 0
execute if score @s rpg_lt_div_t matches 1.. run scoreboard players remove @s rpg_lt_div_t 1
execute if score @s rpg_lt_divine matches 1 run function rpg:divine/old_tick
execute if score @s rpg_lt_divine matches 2 run function rpg:divine/new_tick
execute if score @s rpg_lt_migrate matches 0 if score @s rpg_lt_covenant matches 1.. run function rpg:divine/migrate_legacy
""")
    write("divine/old_tick.mcfunction", """scoreboard players add @s rpg_lt_regen 1
execute if score @s rpg_lt_regen matches 400.. run effect give @s minecraft:regeneration 1 0 true
execute if score @s rpg_lt_regen matches 400.. run scoreboard players set @s rpg_lt_regen 0
""")
    write("divine/new_tick.mcfunction", """scoreboard players set @s rpg_lt_auth 100
scoreboard players set @s rpg_taint 0
tag @s remove rpg.taint.full
effect clear @s minecraft:blindness
effect clear @s minecraft:darkness
""")
    write("divine/migrate_legacy.mcfunction", """scoreboard players set @s rpg_lt_migrate 1
scoreboard players set @s rpg_lt_covenant 0
clear @s minecraft:enchanted_book[minecraft:custom_data~{rpg_new_covenant:1b}]
loot give @s loot rpg:ritual/life_tree/old_covenant
scoreboard players set @s rpg_lt_claim 1
tellraw @s %s
""" % row(comp("[秘仪] ", ui.RITUAL, True),
              comp("先前的生命之树见证已重铸为", ui.GRAY),
              comp("『旧约』", OLD_COLOUR, True), comp("。", ui.GRAY)))
    write("divine/renounce.mcfunction", """execute if score @s rpg_lt_divine matches 1 run item replace entity @s weapon.mainhand with %s
execute if score @s rpg_lt_divine matches 2 run item replace entity @s weapon.mainhand with %s
title @s times 10 60 20
execute if score @s rpg_lt_divine matches 1 run title @s title %s
execute if score @s rpg_lt_divine matches 1 run title @s subtitle %s
execute if score @s rpg_lt_divine matches 2 run title @s title %s
execute if score @s rpg_lt_divine matches 2 run title @s subtitle %s
scoreboard players set @s rpg_lt_divine 0
scoreboard players set @s rpg_lt_div_cd 0
scoreboard players set @s rpg_lt_div_max 0
scoreboard players set @s rpg_lt_auth 0
tag @s remove rpg.divine.old
tag @s remove rpg.divine.new
kill @e[type=minecraft:item_display,tag=rpg.totem.lit,distance=..6,limit=1,sort=nearest]
particle minecraft:flash{color:16777215} ~ ~1 ~ 0 0 0 0 1
particle minecraft:end_rod ~ ~1 ~ 0.6 0.8 0.6 0.15 90
playsound minecraft:block.beacon.deactivate master @s ~ ~ ~ 1 0.7
""" % (covenant_item(1, False), covenant_item(2, False),
         row(comp("契 约 已 断", OLD_COLOUR, True)),
         row(comp("律法归于沉寂", ui.GRAY)),
         row(comp("契 约 已 断", NEW_COLOUR, True)),
         row(comp("权柄归于沉寂", ui.GRAY))))

    # Old Covenant removes two points after each normal two-second taint batch.
    rel = "taint/step.mcfunction"
    src = "\n".join(line for line in read(rel).splitlines()
                    if "旧约以律法抵消" not in line and
                    "rpg_lt_divine matches 1 run scoreboard players remove @s rpg_taint" not in line)
    anchor = "execute if entity @s[scores={rpg_taint=..-1}] run scoreboard players set @s rpg_taint 0"
    add = ("# 旧约以律法抵消每次结算中的两点魔化。\n"
           "execute if score @s rpg_lt_divine matches 1 run scoreboard players remove @s rpg_taint 2\n" + anchor)
    src = src.replace(anchor, add)
    write(rel, src)

    rel = "hud/status.mcfunction"
    status_lines = []
    for line in read(rel).splitlines():
        if "function rpg:hud/authority" in line or "function rpg:hud/divine_bar" in line:
            continue
        if "function rpg:hud/holy" in line:
            line = "execute unless score @s rpg_lt_divine matches 2 if entity @s[scores={rpg_holy=1..}] run function rpg:hud/holy"
        if "function rpg:hud/taint" in line:
            line = "execute unless score @s rpg_lt_divine matches 2 if entity @s[scores={rpg_taint=1..}] run function rpg:hud/taint"
            status_lines.append(line)
            status_lines.append("execute if score @s rpg_lt_divine matches 2 run function rpg:hud/authority")
            continue
        status_lines.append(line)
        if "function rpg:hud/pbar" in line:
            status_lines.append("execute if score @s rpg_lt_div_cd matches 1.. run function rpg:hud/divine_bar")
    write(rel, "\n".join(status_lines))
    authority_lines = [
        "scoreboard players set @s rpg_hud_on 1",
        "scoreboard players operation @s rpg_hud_p = @s rpg_lt_auth",
        "scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud",
        "scoreboard players operation @s rpg_hud_p /= #taint_max rpg_hud",
        "execute if score @s rpg_hud_p matches ..0 run scoreboard players set @s rpg_hud_p 0",
        "execute if score @s rpg_hud_p matches 10.. run scoreboard players set @s rpg_hud_p 10",
    ]
    for filled in range(11):
        parts = [comp("权柄 ", ui.DARK_GRAY)]
        if filled:
            parts.append(comp("▰" * filled, NEW_COLOUR))
        if 10 - filled:
            parts.append(comp("▱" * (10 - filled), ui.DARK_GRAY))
        parts += [comp("  完整度 ", NEW_LIGHT),
                  {"score": {"name": "@s", "objective": "rpg_lt_auth"},
                   "color": NEW_LIGHT, "italic": False},
                  comp("/100", ui.DARK_GRAY)]
        authority_lines.append(
            "execute if score @s rpg_hud_p matches %d run data modify storage rpg:hud a set value '%s'"
            % (filled, row(*parts)))
    write("hud/authority.mcfunction", "\n".join(authority_lines))

    def mini_bar(label_text, colour, filled):
        parts = [comp("　│　上位 ", ui.DARK_GRAY),
                 comp(label_text + " ", colour, True)]
        if filled:
            parts.append(comp("▰" * filled, colour))
        if 5 - filled:
            parts.append(comp("▱" * (5 - filled), ui.DARK_GRAY))
        return row(*parts)

    labels = (
        ("hud/divine_old.mcfunction", "旧约 · 十诫净界", OLD_COLOUR),
        ("hud/divine_beam.mcfunction", "新约 · 创世净光", NEW_COLOUR),
        ("hud/divine_field.mcfunction", "新约 · 伊甸敕界", OLD_LIGHT),
        ("hud/divine_borrow.mcfunction", "新约 · 赦免", NEW_COLOUR),
    )
    for rel_name, label_text, colour in labels:
        bar_lines = ["# 上位契约冷却：固定五格，与七罪契约同一视觉语法。"]
        for filled in range(6):
            bar_lines.append(
                "execute if score @s rpg_hud_p matches %d run data modify storage rpg:hud d set value '%s'"
                % (filled, mini_bar(label_text, colour, filled)))
        write(rel_name, "\n".join(bar_lines))
    write("hud/divine_bar.mcfunction", """scoreboard players set @s rpg_hud_on 1
scoreboard players operation @s rpg_hud_p = @s rpg_lt_div_max
scoreboard players operation @s rpg_hud_p -= @s rpg_lt_div_cd
scoreboard players operation @s rpg_hud_p *= #hud_mini rpg_hud
scoreboard players operation @s rpg_hud_p /= @s rpg_lt_div_max
execute if score @s rpg_lt_divine matches 1 run return run function rpg:hud/divine_old
execute if score @s rpg_lt_div_max matches 300 run return run function rpg:hud/divine_borrow
execute if score @s rpg_lt_div_max matches 600 run return run function rpg:hud/divine_field
function rpg:hud/divine_beam
""")

    messages = {
        59: row(comp("[十诫净界]", OLD_COLOUR, True),
                comp("　律法涤尽十方罪影", OLD_LIGHT), comp(" ✦", ui.WHITE)),
        60: row(comp("[创世净光]", NEW_COLOUR, True),
                comp("　权柄化作前路之光", NEW_LIGHT), comp(" ✦", ui.WHITE)),
        61: row(comp("[伊甸敕界]", OLD_LIGHT, True),
                comp("　伊甸在脚下重开", NEW_LIGHT), comp(" ✦", ui.WHITE)),
        62: row(comp("[赦免]", NEW_COLOUR, True),
                comp("　柱中之力未留下魔化", ui.GRAY), comp(" ✦", OLD_LIGHT)),
    }
    msg_src = "\n".join(
        line for line in read("hud/msg.mcfunction").splitlines()
        if not any("rpg_hud_m=%d" % message_id in line for message_id in messages))
    for message_id, message in messages.items():
        write("hud/m%d.mcfunction" % message_id,
              "scoreboard players set @s rpg_hud_m %d\nscoreboard players set @s rpg_hud_mt 40"
              % message_id)
        msg_src += ("\nexecute if entity @s[scores={rpg_hud_m=%d}] run title @s actionbar %s"
                    % (message_id, message))
    write("hud/msg.mcfunction", msg_src)

    # Keep the player panel consistent with the one-line HUD.
    rel = "panel/open.mcfunction"
    lines = read(rel).splitlines()
    out = []
    for line in lines:
        if "驱魔等级 " in line and "权柄完整度 " in line:
            continue
        if "驱魔等级 " in line and "侵蚀 " in line:
            raw = line[line.find("tellraw @s "):]
            out.append("execute unless score @s rpg_lt_divine matches 2 run " + raw)
            authority_header = row(
                comp("驱魔等级 ", ui.GRAY),
                {"score": {"name": "@s", "objective": "rpg_ex_lvl"}, "color": ui.HOLY_LIGHT, "italic": False},
                comp("　阅历 ", ui.GRAY),
                {"score": {"name": "@s", "objective": "rpg_ex_xp"}, "color": ui.HOLY, "italic": False},
                comp("　权柄完整度 ", NEW_COLOUR),
                {"score": {"name": "@s", "objective": "rpg_lt_auth"}, "color": NEW_LIGHT, "italic": False},
                comp("/100", ui.DARK_GRAY))
            out.append("execute if score @s rpg_lt_divine matches 2 run tellraw @s " + authority_header)
        elif "[契约·权柄]" in line:
            continue
        elif "[契约·侵蚀]" in line:
            raw = line[line.find("tellraw @s "):]
            out.append("execute unless score @s rpg_lt_divine matches 2 run " + raw)
            authority_button = raw.replace("[契约·侵蚀]", "[契约·权柄]")
            authority_button = authority_button.replace(
                '"text":"[契约·权柄]","color":"#D596F2"',
                '"text":"[契约·权柄]","color":"%s"' % NEW_COLOUR)
            out.append("execute if score @s rpg_lt_divine matches 2 run " + authority_button)
        else:
            out.append(line)
    write(rel, "\n".join(out))

    rel = "panel/pact.mcfunction"
    panel_lines = []
    base_header = None
    for line in read(rel).splitlines():
        if "上位契约：" in line or "权柄完整度：" in line or "契约与权柄" in line:
            continue
        if "契约与侵蚀" in line:
            base_header = line[line.find("tellraw @s "):]
            continue
        if "当前侵蚀：" in line:
            pos = line.find("tellraw @s ")
            line = line[pos:] if pos >= 0 else line
            line = "execute unless score @s rpg_lt_divine matches 2 run " + line
        panel_lines.append(line)
    if base_header is None:
        base_header = "tellraw @s " + row(comp("+-------- 契约与侵蚀 --------+", ui.RITUAL, True))
    new_header = "tellraw @s " + row(comp("+-------- 契约与权柄 --------+", NEW_COLOUR, True))
    divine_lines = [
        "execute unless score @s rpg_lt_divine matches 2 run " + base_header,
        "execute if score @s rpg_lt_divine matches 2 run " + new_header,
        "execute if score @s rpg_lt_divine matches 1 run tellraw @s " +
        row(comp("上位契约：", ui.GRAY), comp("旧约 · 律法", OLD_COLOUR, True)),
        "execute if score @s rpg_lt_divine matches 2 run tellraw @s " +
        row(comp("上位契约：", ui.GRAY), comp("新约 · 权柄", NEW_COLOUR, True)),
        "execute if score @s rpg_lt_divine matches 0 run tellraw @s " +
        row(comp("上位契约：无", ui.DARK_GRAY)),
        "execute if score @s rpg_lt_divine matches 2 run tellraw @s " +
        row(comp("权柄完整度：", NEW_COLOUR),
            {"score": {"name": "@s", "objective": "rpg_lt_auth"},
             "color": NEW_LIGHT, "italic": False},
            comp(" / 100", ui.DARK_GRAY)),
    ]
    # The section header belongs at the top, before either meter.
    panel_lines = divine_lines + panel_lines
    write(rel, "\n".join(panel_lines))


def build_tree_rewards_and_cross():
    # Loot, /give, sign, reissue and renounce all share this exact source.
    old_components = covenant_components(1, False)
    new_components = covenant_components(2, False)
    write_json(LOOT, "ritual/life_tree/old_covenant.json", {
        "type": "minecraft:generic", "pools": [{"rolls": 1, "entries": [{
            "type": "minecraft:item", "name": "minecraft:enchanted_book", "functions": [{
                "function": "minecraft:set_components", "components": old_components}]}]}]})
    write_json(LOOT, "ritual/life_tree/new_covenant.json", {
        "type": "minecraft:generic", "pools": [{"rolls": 1, "entries": [{
            "type": "minecraft:item", "name": "minecraft:enchanted_book", "functions": [{
                "function": "minecraft:set_components", "components": new_components}]}]}]})
    write("ritual/life_tree/give_old_covenant.mcfunction", "loot give @s loot rpg:ritual/life_tree/old_covenant")
    write("ritual/life_tree/give_new_covenant.mcfunction", "loot give @s loot rpg:ritual/life_tree/new_covenant")
    write("ritual/life_tree/complete.mcfunction", """tag @s add rpg.lt.complete
execute as @a[tag=rpg.kabbalah.user,distance=..5,sort=nearest,limit=1] unless score @s rpg_lt_claim matches 1.. run function rpg:ritual/life_tree/give_old_covenant
scoreboard players set @a[tag=rpg.kabbalah.user,distance=..5,sort=nearest,limit=1] rpg_lt_claim 1
particle minecraft:flash{color:13145394} ~ ~0.18 ~ 0 0 0 0 1 force
particle minecraft:totem_of_undying ~ ~0.35 ~ 2.2 0.35 4.6 0.10 140 force
playsound minecraft:ui.toast.challenge_complete master @a[distance=..32] ~ ~ ~ 1.0 0.82
tellraw @a[distance=..24,gamemode=!spectator] %s
""" % row(comp("[旧约] ", OLD_COLOUR, True),
           comp("十源质归位，律法的上半部显于人间；", ui.GRAY),
           comp("Daath 节点", NEW_COLOUR, True),
           comp("仍等待最后的见证。", ui.GRAY)))

    # Add True Cross routing at the hidden node before the generic failure text.
    rel = "ritual/life_tree/input.mcfunction"
    src = "\n".join(line for line in read(rel).splitlines()
                    if "rpg_true_cross:1b" not in line)
    needle = "tag @s add rpg.kabbalah.user"
    route = (needle + "\nexecute if items entity @s weapon.mainhand minecraft:iron_nugget"
             "[minecraft:custom_data~{rpg_true_cross:1b}] at @s as @e[type=minecraft:marker,"
             "tag=rpg.ritual.life_tree,tag=rpg.lt.complete,tag=!rpg.lt.gathering,distance=..12,"
             "sort=nearest,limit=1] at @s positioned ^0.000 ^0.06 ^-1.580 "
             "if entity @a[tag=rpg.kabbalah.user,distance=..0.68,limit=1] "
             "run return run function rpg:divine/gather/start")
    src = src.replace(needle, route)
    write(rel, src)

    write("divine/gather/start.mcfunction", """tag @s add rpg.lt.gathering
scoreboard players set @s rpg_lt_gather 0
scoreboard players add #next rpg_lt_owner 1
scoreboard players operation @s rpg_lt_owner = #next rpg_lt_owner
scoreboard players operation @a[tag=rpg.kabbalah.user,distance=..1,limit=1] rpg_lt_owner = #next rpg_lt_owner
clear @a[tag=rpg.kabbalah.user,distance=..1,limit=1] minecraft:iron_nugget[minecraft:custom_data~{rpg_true_cross:1b}] 1
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.ritual.life_tree.cross"],item:{id:"minecraft:iron_nugget",count:1,components:{"minecraft:custom_model_data":{floats:[1110001.0f]},"minecraft:enchantment_glint_override":1b}},item_display:"ground",view_range:0.8f,brightness:{block:15,sky:15},transformation:{translation:[0f,0.04f,0f],scale:[1.0f,1.0f,1.0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
particle minecraft:flash{color:16777215} ~ ~0.2 ~ 0 0 0 0 1 force
playsound minecraft:block.beacon.activate master @a[distance=..24] ~ ~ ~ 1 1.55
tellraw @a[tag=rpg.kabbalah.user,distance=..1,limit=1] %s
tag @a[tag=rpg.kabbalah.user,distance=..1] remove rpg.kabbalah.user
""" % row(comp("[秘仪] ", ui.RITUAL, True),
           comp("真·十字架在", ui.GRAY), comp("Daath 节点", NEW_COLOUR, True),
           comp("承接禁忌知识；十源质开始汇聚……", ui.GRAY)))
    write("divine/gather/step.mcfunction", """execute as @e[type=minecraft:marker,tag=rpg.lt.gathering] at @s run function rpg:divine/gather/one
""")
    write("divine/gather/one.mcfunction", """scoreboard players add @s rpg_lt_gather 1
execute as @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.prop,distance=..8] at @s facing entity @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.cross,distance=..8,limit=1,sort=nearest] feet run tp @s ^ ^ ^0.22
execute as @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.prop,distance=..8] at @s run particle minecraft:end_rod ~ ~0.08 ~ 0.08 0.03 0.08 0.01 2 force
execute positioned ^0 ^0.12 ^-1.58 run particle dust{color:[0.75,0.90,1.0],scale:1.4} ~ ~ ~ 0.25 0.05 0.25 0.02 8 force
execute if score @s rpg_lt_gather matches 24.. run return run function rpg:divine/gather/finish
""")
    write("divine/gather/finish.mcfunction", """execute as @a if score @s rpg_lt_owner = @e[type=minecraft:marker,tag=rpg.lt.gathering,distance=..1,limit=1] rpg_lt_owner run function rpg:divine/gather/reward
kill @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.prop,distance=..8]
kill @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.cross,distance=..8]
particle minecraft:flash{color:8641023} ~ ~0.4 ~ 0 0 0 0 1 force
particle minecraft:end_rod ~ ~0.4 ~ 2.2 0.5 4.5 0.12 180 force
particle minecraft:totem_of_undying ~ ~0.4 ~ 2.0 0.4 4.2 0.10 120 force
playsound minecraft:ui.toast.challenge_complete master @a[distance=..32] ~ ~ ~ 1 1.25
tellraw @a[distance=..24,gamemode=!spectator] %s
kill @s
""" % row(comp("[新约] ", NEW_COLOUR, True),
           comp("十源质与真·十字架归于一体；生命之树收束为", ui.GRAY),
           comp("『新约』", NEW_LIGHT, True), comp("。", ui.GRAY)))
    write("divine/gather/reward.mcfunction", """clear @s minecraft:enchanted_book[minecraft:custom_data~{rpg_divine_old:1b}]
execute if score @s rpg_lt_divine matches 1 run scoreboard players set @s rpg_lt_divine 0
tag @s remove rpg.divine.old
loot give @s loot rpg:ritual/life_tree/new_covenant
""")

    # Administrative clearing must also remove an in-progress Daath cross.
    rel = "ritual/life_tree/clear.mcfunction"
    src = "\n".join(line for line in read(rel).splitlines()
                    if "tag=rpg.ritual.life_tree.cross" not in line)
    needle = "kill @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..12]"
    src = src.replace(needle,
                      "execute as @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..12] at @s run kill @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.cross,distance=..8]\n" + needle)
    write(rel, src)
    rel = "ritual/life_tree/clear_all.mcfunction"
    src = "\n".join(line for line in read(rel).splitlines()
                    if "tag=rpg.ritual.life_tree.cross" not in line)
    src = "kill @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.cross]\n" + src
    write(rel, src)


def patch_catalog():
    rel = "ritual/life_tree/give/all.mcfunction"
    src = "\n".join(line for line in read(rel).splitlines() if "rpg_true_cross" not in line)
    src += "\ngive @s %s 1" % cross_item()
    write(rel, src)
    rel = "command/give/extra.mcfunction"
    lines = read(rel).splitlines()
    cleaned = []
    inside = False
    for line in lines:
        if line == "# == DIVINE COVENANT RITE ==":
            inside = True
            continue
        if line == "# == END DIVINE COVENANT RITE ==":
            inside = False
            continue
        if not inside and "rpg_true_cross" not in line:
            cleaned.append(line)
    src = "\n".join(cleaned)
    src += ("\n\n# == DIVINE COVENANT RITE ==\n"
            "give @a %s 1\n"
            "give @a %s 1\n"
            "give @a %s 1\n"
            "# == END DIVINE COVENANT RITE ==" %
            (covenant_item(1, False), covenant_item(2, False), cross_item()))
    write(rel, src)


def build_models_and_assets():
    src_dir = os.path.join(HERE, "assets", "divine_covenant")
    tex_dir = os.path.join(RP, "assets", "rpg", "textures", "item")
    model_dir = os.path.join(RP, "assets", "rpg", "models", "item")
    os.makedirs(tex_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    for name in ("old_covenant", "new_covenant", "true_cross"):
        shutil.copyfile(os.path.join(src_dir, name + ".png"), os.path.join(tex_dir, name + ".png"))
        write_json(model_dir, name + ".json", {
            "parent": "item/generated", "textures": {"layer0": "rpg:item/" + name}})

    path = os.path.join(RP, "assets", "minecraft", "items", "enchanted_book.json")
    with io.open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    entries = [e for e in data["model"]["entries"] if e.get("threshold") not in (OLD_CMD, NEW_CMD)]
    entries += [
        {"threshold": OLD_CMD, "model": {"type": "minecraft:model", "model": "rpg:item/old_covenant"}},
        {"threshold": NEW_CMD, "model": {"type": "minecraft:model", "model": "rpg:item/new_covenant"}},
    ]
    data["model"]["entries"] = sorted(entries, key=lambda e: e["threshold"])
    write_json(os.path.dirname(path), os.path.basename(path), data)

    path = os.path.join(RP, "assets", "minecraft", "items", "iron_nugget.json")
    data = {"model": {"type": "minecraft:range_dispatch", "property": "minecraft:custom_model_data",
                      "index": 0, "fallback": {"type": "minecraft:model", "model": "minecraft:item/iron_nugget"},
                      "entries": [{"threshold": CROSS_CMD, "model": {"type": "minecraft:model", "model": "rpg:item/true_cross"}}]}}
    write_json(os.path.dirname(path), os.path.basename(path), data)


def main():
    # Remove files emitted by the retired direct-New/single-VFX prototypes so
    # incremental generator runs are as clean as a full rebuild.
    remove_function("divine/sign_vfx.mcfunction")
    remove_function("ritual/life_tree/covenant_tick.mcfunction")
    patch_objectives_and_tick()
    build_advancement_and_trigger()
    build_old_power()
    build_new_power_and_borrow()
    build_damage_type_and_ritual_compat()
    build_player_tick_hud_and_renounce()
    build_tree_rewards_and_cross()
    patch_catalog()
    build_models_and_assets()
    print("divine covenants: Old Covenant / Daath True Cross / New Covenant")


if __name__ == "__main__":
    main()
