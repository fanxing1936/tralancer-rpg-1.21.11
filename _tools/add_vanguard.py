# -*- coding: utf-8 -*-
"""别西卜麾下的罪仆 dressed as Minecraft Dungeons' Vanguard -- the skeleton
guard of the Nameless One, whose look 别西卜 wears.

Only the look and voice change.  The servants stay the illagers
add_demon_minions.py summons (rpg.demon.minion.lord4: 桀派 the vanguard,
布提斯 the hunter, 巴钦 the ritualist, 塞列欧斯 the hexer, 布松 the
executioner), with their
health, AI, abilities, loot and lifetime untouched.  Each tick any such
servant not yet dressed gets the tag `rpg.vg`, invisibility, eight
item_display parts, and its held item's model set to `rpg:empty`: the
item stays (so its damage and the crossbow's loading still work) but
draws nothing where the model's hands are not.

An illusioner cannot be dressed: its renderer draws the body, and four
mirror copies, even while invisible.  So 塞列欧斯, the hexer, is summoned as
a pillager (ROLE_OVERRIDES in add_demon_minions.py), and the selector
still skips illusioners in case one carries the tag.

The shield takes the first hit, as in Dungeons: on the first hurt it
shatters (its part is removed, the `break` clip and sound play).  It is
only the look -- health is not changed.  Melee: when a player is within
reach and the swing is off cooldown, the `attack` clip plays; it stands
in for the vindicator's own swing, which an invisible body cannot show.

Source of truth is `_tools/vanguard_ref/vanguard.bbmodel` (bootstrapped by
vanguard_geo.py, posed and animated in Blockbench).  Textures and sounds
from https://minecraft.wiki/w/Dungeons:Vanguard and its equipment pages,
see vanguard_ref/SOURCES.md.
"""

import os
import sys

from display_mob import (Mob, NS, build, hook_tag, playsound, snbt_components,
                         wf, wj, write_rig_runtime)

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

HERE = os.path.dirname(os.path.abspath(__file__))


def snd(stem, n):
    return ["Sfx_mob_vanguard%s-%03d_soundWave.ogg" % (stem, i) for i in range(1, n + 1)]


MOB = Mob(
    key="vanguard", label="先锋罪仆", generator="add_vanguard.py",
    bbmodel=os.path.join(HERE, "vanguard_ref", "vanguard.bbmodel"),
    parts=[
        ("body", ["body", "cuirass", "loincloth"]),
        ("head", ["head", "helmet"]),
        ("right_arm", ["right_arm"]),
        ("left_arm", ["left_arm"]),
        ("shield", ["shield"]),
        ("glaive", ["glaive"]),
        ("right_leg", ["right_leg"]),
        ("left_leg", ["left_leg"]),
    ],
    glow=(),
    # vindicator, pillager and evoker share the illager seat: 2.0 blocks
    seat=2.0,
    tag="rpg.vg", score="rpg_vg", carrier=None,
    clips=[
        ("idle", 4, True),
        ("walk", 2, True),
        ("attack", 1, False),         # thrust lands at 0.45 s
        ("break", 1, False),          # the shield shatters, a stagger back
    ],
    sounds=dict(
        idle=(("先锋罪仆：嘶鸣", "Vanguard rattles"), snd("Idle", 3), None),
        hurt=(("先锋罪仆：受伤", "Vanguard hurts"), snd("Hurt", 4), None),
        death=(("先锋罪仆：散架", "Vanguard dies"), snd("Death", 3), None),
        shield_break=(("先锋罪仆：盾牌碎裂", "Vanguard's shield breaks"), snd("ShieldBreak", 3), None),
        spear=(("先锋罪仆：长戟突刺", "Glaive thrusts"), snd("Spear", 1), None),
        step=(("先锋罪仆：脚步", "Vanguard steps"), snd("Step", 4), None),
    ),
    sound_dir=os.path.join(HERE, "vanguard_ref", "sounds"),
    cues={
        "walk": [(0.0, "step", 0.5, 1.0), (0.5, "step", 0.5, 1.0)],
        "attack": [(0.4, "spear", 1.0, 1.0)],
    },
    enter_cues={"break": [("shield_break", 1.0, 1.0)]},
    hurt="hurt", death="death", ambient=("idle", 0.006),
    on_hurt=["execute if entity @s[tag=!rpg.vg.broken] run function rpg:vanguard/shield_break"],
)

SERVANTS = "tag=rpg.demon.minion.lord4,tag=!rpg.vg,type=!minecraft:illusioner"
SWING_CD = 24                 # ticks between attack clips


def write_datapack(baked):
    first = baked["idle"]["frames"][0][1]
    lines = [
        "# 别西卜麾下的罪仆换上先锋外观（as 罪仆，at 其脚下）。只加 rpg.vg 标签、隐身与部件，",
        "# 手上的物品不换，只把它的模型设成空的。",
        "tag @s add rpg.vg",
        "tag @s add rpg.vg.dressing",
        "effect give @s minecraft:invisibility infinite 0 true",
        'item modify entity @s weapon.mainhand {function:"minecraft:set_components",'
        'components:{"minecraft:item_model":"rpg:empty"}}',
    ]
    for part, _ in MOB.parts:
        lines.append(
            'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vg.part","rpg.vg.p.%s","rpg.vg.new"],'
            'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:vanguard/%s"}},'
            'item_display:"none",teleport_duration:2,interpolation_duration:2,'
            'view_range:1f,transformation:%s}' % (part, part, snbt_components(MOB, first[part])))
    lines += [
        "execute as @e[type=minecraft:item_display,tag=rpg.vg.new,distance=..1] run "
        "ride @s mount @e[tag=rpg.vg.dressing,limit=1]",
        "tag @e[type=minecraft:item_display,tag=rpg.vg.new,distance=..1] remove rpg.vg.new",
        "tag @s remove rpg.vg.dressing",
        "scoreboard players set @s rpg_vg 0",
        "function rpg:vanguard/anim/init",
        "# 原作：先锋现身时会嘶鸣一声",
        playsound(MOB, "idle", 1.0, 1.0, 24),
    ]
    wf(os.path.join(MOB.func, "dress.mcfunction"), lines)
    wf(os.path.join(MOB.func, "shield_break.mcfunction"), [
        "# 第一下打在盾上：盾碎，部件移除（只是外观，血量照常扣）。",
        "tag @s add rpg.vg.broken",
        "execute on passengers if entity @s[tag=rpg.vg.p.shield] run kill @s",
        "execute at @s run particle block{block_state:\"minecraft:spruce_planks\"} ~ ~1.2 ~ 0.4 0.5 0.4 0.1 24",
        "function rpg:vanguard/anim/enter/break",
    ])
    wf(os.path.join(MOB.func, "strike.mcfunction"), [
        "# 有人进了长戟的距离：刺一下。冷却借用 rpg_vg 的个体分数。",
        "scoreboard players set @s rpg_vg %d" % SWING_CD,
        "function rpg:vanguard/anim/enter/attack",
    ])
    write_rig_runtime(MOB, [
        "# 先锋罪仆每刻入口。任何途径召出的别西卜罪仆（手动、仪式二阶段）都在这里换装。",
        "execute if entity @e[%s,limit=1] as @e[%s] at @s run function rpg:vanguard/dress" % (SERVANTS, SERVANTS),
        "execute if entity @e[tag=rpg.vg,type=!minecraft:item_display,limit=1] "
        "as @e[tag=rpg.vg,type=!minecraft:item_display] at @s run function rpg:vanguard/follow",
    ], follow_extra=[
        "execute if score @s rpg_vg matches 1.. run scoreboard players remove @s rpg_vg 1",
        "execute if score @s rpg_vg matches ..0 unless score @s rpg_vg_anim matches 2..3 "
        "if entity @a[distance=..3.2,gamemode=!spectator,gamemode=!creative,limit=1] "
        "run function rpg:vanguard/strike",
    ])
    pred = os.path.join(DP, "data", NS, "predicate", "vanguard")
    wj(os.path.join(pred, "invisible.json"), {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"effects": {"minecraft:invisibility": {}}}})
    # the warden phase clears invisibility from whatever attacked something;
    # the servant's body is the model, so put it back after everything else
    wf(os.path.join(MOB.func, "tick_late.mcfunction"), [
        "# 先锋罪仆的身体是模型：载体始终隐身。",
        "execute as @e[tag=rpg.vg,type=!minecraft:item_display] unless predicate rpg:vanguard/invisible "
        "run effect give @s minecraft:invisibility infinite 0 true",
    ])
    hook_tag(DP, "tick", "rpg:vanguard/tick_late", False)


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
