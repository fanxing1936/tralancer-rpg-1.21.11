# -*- coding: utf-8 -*-
"""利维坦麾下的罪仆 dressed as Minecraft Dungeons' Sunken Skeleton -- the
drowned crossbowmen of the sunken ruins, for the lord who wears the
Necromancer's look.

Only the look and voice change.  The servants stay the illagers
add_demon_minions.py summons (rpg.demon.minion.lord2: 华利弗 the vanguard,
亚蒙 the hunter, 巴巴托斯 the ritualist, 派蒙 the hexer, 布耶尔 the
executioner), with their health, AI, abilities, loot and lifetime
untouched.  Each tick any such servant not yet dressed gets the tag
`rpg.sk`, invisibility and seven item_display parts.  No weapon is
modelled: the servant's own vanilla mainhand item (sword, crossbow, book,
axe) is copied into the `weapon` part, drawn in `thirdperson_righthand`
mode on the model's right arm (Mob.held in display_mob.py).  The carrier's
own item stays, so its damage and the crossbow's loading still work, but
its model is set to `rpg:empty` so it is not drawn twice.

All five share one model.  An illusioner cannot be
dressed (its renderer draws the body and four mirror copies even while
invisible), so 派蒙, the hexer, is summoned as a pillager (ROLE_OVERRIDES
in add_demon_minions.py); the selector still skips illusioners.

When a player comes within reach and the move is off cooldown, a clip
stands in for the illager's own swing or shot, which an invisible body
cannot show: crossbow carriers (pillagers) raise and fire at range,
everyone else swings in melee.

Source of truth is `_tools/sunken_skeleton_ref/sunken_skeleton.bbmodel`
(bootstrapped by sunken_skeleton_geo.py, posed and animated in
Blockbench).  Texture and sounds from
https://minecraft.wiki/w/Dungeons:Sunken_Skeleton, see
sunken_skeleton_ref/SOURCES.md.
"""

import os
import sys

from display_mob import (Mob, NS, build, hook_tag, playsound, snbt_components,
                         wf, wj, write_rig_runtime)

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

HERE = os.path.dirname(os.path.abspath(__file__))


def snd(stem, n):
    return ["D5_sfx_mob_sunkenSkeleton%s-%03d.ogg" % (stem, i) for i in range(1, n + 1)]


MOB = Mob(
    key="sunken_skeleton", label="沉没罪仆", generator="add_sunken_skeleton.py",
    bbmodel=os.path.join(HERE, "sunken_skeleton_ref", "sunken_skeleton.bbmodel"),
    parts=[
        ("body", ["body"]),
        ("head", ["head", "coral", "sprig"]),
        ("right_arm", ["right_arm"]),
        ("left_arm", ["left_arm"]),
        ("weapon", ["right_arm"]),    # the carrier's own item, see Mob.held
        ("right_leg", ["right_leg"]),
        ("left_leg", ["left_leg"]),
    ],
    glow=(),
    # vindicator, pillager and evoker share the illager seat: 2.0 blocks
    seat=2.0,
    tag="rpg.sk", score="rpg_sk", carrier=None,
    clips=[
        ("idle", 4, True),
        ("walk", 2, True),
        ("attack", 1, False),         # overhead swing, lands at 0.4 s
        ("shoot", 1, False),          # crossbow raised, fires at 0.6 s
    ],
    sounds=dict(
        idle=(("沉没罪仆：咯咯作响", "Sunken servant rattles"), snd("Idle", 3), None),
        hurt=(("沉没罪仆：受伤", "Sunken servant hurts"), snd("Hurt", 4), None),
        death=(("沉没罪仆：散架", "Sunken servant dies"), snd("Death", 3), None),
        step=(("沉没罪仆：湿漉的脚步", "Sunken servant steps"), snd("Step", 4), None),
        load=(("沉没罪仆：上弦", "Crossbow loads"), snd("CrossbowLoad", 4), None),
        shoot=(("沉没罪仆：放箭", "Crossbow fires"), snd("CrossbowShoot", 3), None),
        impact=(("弩箭命中", "Bolt hits"), snd("CrossbowImpact", 4), None),
        novelty=(("沉没罪仆：怪笑", "Sunken servant cackles"), snd("Novelty", 2), None),
    ),
    sound_dir=os.path.join(HERE, "sunken_skeleton_ref", "sounds"),
    cues={
        "walk": [(0.0, "step", 0.5, 1.0), (0.5, "step", 0.5, 1.0)],
        "shoot": [(0.0, "load", 0.9, 1.0), (0.6, "shoot", 1.0, 1.0), (0.75, "impact", 0.6, 1.0)],
    },
    hurt="hurt", death="death", ambient=("idle", 0.006), held="weapon",
)

SERVANTS = "tag=rpg.demon.minion.lord2,tag=!rpg.sk,type=!minecraft:illusioner"
SHOT_CD = 40                  # ticks between clips
SHOT_RANGE = 12               # blocks, crossbow carriers
SWING_RANGE = 3.2             # blocks, everyone else


def write_datapack(baked):
    first = baked["idle"]["frames"][0][1]
    lines = [
        "# 利维坦麾下的罪仆换上沉没骷髅外观（as 罪仆，at 其脚下）。只加 rpg.sk 标签、隐身与部件，",
        "# 手上的物品不换，只把它的模型设成空的。",
        "tag @s add rpg.sk",
        "tag @s add rpg.sk.dressing",
        "effect give @s minecraft:invisibility infinite 0 true",
    ]
    for part, _ in MOB.parts:
        if part == MOB.held:
            lines.append(
                'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.%s","rpg.sk.new"],'
                'item_display:"thirdperson_righthand",teleport_duration:2,interpolation_duration:2,'
                'view_range:1f,transformation:%s}' % (part, snbt_components(MOB, first[part])))
            continue
        lines.append(
            'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.sk.part","rpg.sk.p.%s","rpg.sk.new"],'
            'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:sunken_skeleton/%s"}},'
            'item_display:"none",teleport_duration:2,interpolation_duration:2,'
            'view_range:1f,transformation:%s}' % (part, part, snbt_components(MOB, first[part])))
    lines += [
        "execute as @e[type=minecraft:item_display,tag=rpg.sk.new,distance=..1] run "
        "ride @s mount @e[tag=rpg.sk.dressing,limit=1]",
        "# 手里的原版物品复制到 weapon 部件上画出来，载体自己的那份只把模型设成空的",
        "item replace entity @e[type=minecraft:item_display,tag=rpg.sk.new,tag=rpg.sk.p.weapon,distance=..1,limit=1] "
        "contents from entity @s weapon.mainhand",
        'item modify entity @s weapon.mainhand {function:"minecraft:set_components",'
        'components:{"minecraft:item_model":"rpg:empty"}}',
        "tag @e[type=minecraft:item_display,tag=rpg.sk.new,distance=..1] remove rpg.sk.new",
        "tag @s remove rpg.sk.dressing",
        "scoreboard players set @s rpg_sk 0",
        "function rpg:sunken_skeleton/anim/init",
        "# 原作：沉没骷髅现身时会怪笑一声",
        playsound(MOB, "novelty", 1.0, 1.0, 24),
    ]
    wf(os.path.join(MOB.func, "dress.mcfunction"), lines)
    wf(os.path.join(MOB.func, "strike.mcfunction"), [
        "# 有人进了距离：持弩的举弩放箭，其余的挥一下。冷却借用 rpg_sk 的个体分数。",
        "scoreboard players set @s rpg_sk %d" % SHOT_CD,
        "execute if entity @s[type=minecraft:pillager] run return run function rpg:sunken_skeleton/anim/enter/shoot",
        "function rpg:sunken_skeleton/anim/enter/attack",
    ])
    write_rig_runtime(MOB, [
        "# 沉没罪仆每刻入口。任何途径召出的利维坦罪仆（手动、仪式二阶段）都在这里换装。",
        "execute if entity @e[%s,limit=1] as @e[%s] at @s run function rpg:sunken_skeleton/dress" % (SERVANTS, SERVANTS),
        "execute if entity @e[tag=rpg.sk,type=!minecraft:item_display,limit=1] "
        "as @e[tag=rpg.sk,type=!minecraft:item_display] at @s run function rpg:sunken_skeleton/follow",
    ], follow_extra=[
        "execute if score @s rpg_sk matches 1.. run scoreboard players remove @s rpg_sk 1",
        "execute if score @s rpg_sk matches ..0 unless score @s rpg_sk_anim matches 2..3 "
        "if entity @s[type=minecraft:pillager] "
        "if entity @a[distance=..%d,gamemode=!spectator,gamemode=!creative,limit=1] "
        "run function rpg:sunken_skeleton/strike" % SHOT_RANGE,
        "execute if score @s rpg_sk matches ..0 unless score @s rpg_sk_anim matches 2..3 "
        "unless entity @s[type=minecraft:pillager] "
        "if entity @a[distance=..%s,gamemode=!spectator,gamemode=!creative,limit=1] "
        "run function rpg:sunken_skeleton/strike" % SWING_RANGE,
    ])
    pred = os.path.join(DP, "data", NS, "predicate", "sunken_skeleton")
    wj(os.path.join(pred, "invisible.json"), {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"effects": {"minecraft:invisibility": {}}}})
    # the warden phase clears invisibility from whatever attacked something;
    # the servant's body is the model, so put it back after everything else
    wf(os.path.join(MOB.func, "tick_late.mcfunction"), [
        "# 沉没罪仆的身体是模型：载体始终隐身。",
        "execute as @e[tag=rpg.sk,type=!minecraft:item_display] unless predicate rpg:sunken_skeleton/invisible "
        "run effect give @s minecraft:invisibility infinite 0 true",
    ])
    hook_tag(DP, "tick", "rpg:sunken_skeleton/tick_late", False)


def write_empty_model():
    """rpg:empty -- an item model that draws nothing (held items under a rig)."""
    wj(os.path.join(RP, "assets", NS, "items", "empty.json"), {"model": {"type": "minecraft:empty"}})


def main():
    baked, _ = build(MOB, RP, DP)
    write_empty_model()
    if os.path.isdir(os.path.join(DP, "data", NS, "function", "minion")):
        write_datapack(baked)


if __name__ == "__main__":
    main()
