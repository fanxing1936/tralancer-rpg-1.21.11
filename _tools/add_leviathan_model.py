# -*- coding: utf-8 -*-
"""利维坦 (Leviathan) -- the second of the seven lords, dressed as Minecraft
Dungeons' Necromancer.

Only the look changes.  The lord is still the invisible vindicator that
rpg:taint/lord2 (and every other path that ends in `rpg_dm_lord 2`: the
seal escape, the debug summon) summons, with its tags, health, skills,
true-name inquest and exorcism untouched.  Each tick, any such vindicator
not yet dressed gets the tag `rpg.lv` and seven item_display parts
mounted beside its soul marker; the parts carry only `rpg.lv.*` tags, so
no `rpg.demon` / `devil` selector sees them.  They die with the lord: every
removal path either kills its passengers or leaves them riding nothing,
which the orphan sweep in display_mob.py catches.

The Necromancer is the Nameless One's recolour, so the rig, poses and
clips are 别西卜's (add_beelzebub.py); only the atlas and the staff head
(a glowing cube in a fork) differ.  Source of truth is
`_tools/leviathan_ref/leviathan.bbmodel` (see leviathan_geo.py).  Sounds
are the Necromancer set from https://minecraft.wiki/w/Dungeons:Necromancer
(leviathan_ref/sounds, see SOURCES.md there).

Visibility as for 别西卜: the carrier's invisibility is put back after
rpg:command/tick_end, and while the carrier glows (bound) the parts glow.
"""

import io
import os
import sys

from display_mob import (Mob, build, hook_tag, playsound, snbt_components,
                         write_rig_runtime, wf, wj, NS)

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

HERE = os.path.dirname(os.path.abspath(__file__))
TAINT = os.path.join(DP, "data", NS, "function", "taint")
MARK = "# 利维坦外观（add_leviathan_model.py）"


def snd(stem, n, fmt="Sfx_mob_Necromancer%s-%03d_soundWave.ogg", start=1):
    return [fmt % (stem, i) for i in range(start, start + n)]


MOB = Mob(
    key="leviathan", label="利维坦", generator="add_leviathan_model.py",
    bbmodel=os.path.join(HERE, "leviathan_ref", "leviathan.bbmodel"),
    parts=[
        ("body", ["body", "belt", "skirt", "right_pauldron", "left_pauldron"]),
        ("head", ["head", "eyes_glow", "crown"]),
        ("right_arm", ["right_arm"]),
        ("left_arm", ["left_arm"]),
        ("staff", ["staff"]),
        # its own part: the corner-on tilt is two axes, and it spins
        ("gem", ["gem"]),
        ("cape", ["cape"]),
    ],
    glow={"eyes_glow", "gem"},
    # the lord is a plain vindicator: seat 2.0 blocks
    seat=2.0, model_scale=1.1,
    tag="rpg.lv", score="rpg_lv",
    clips=[
        ("idle", 4, True),
        ("walk", 2, True),            # the hover-glide
        ("cast", 1, False),           # staff raised, thrust at 0.65 s
        ("summon", 1, False),         # arms up, slam at 1.0 s
        ("rise", 2, False),           # coming up out of the ground on arrival
    ],
    sounds=dict(
        idle=(("利维坦：低语", "Leviathan murmurs"), snd("Idle", 3), None),
        hurt=(("利维坦：受伤", "Leviathan hurts"), snd("Hurt", 4), None),
        death=(("利维坦：消亡", "Leviathan dies"), snd("Death", 2), None),
        step=(("利维坦：脚步", "Leviathan steps"), snd("Step", 4), None),
        laugh=(("利维坦：骨笑", "Leviathan laughs"), snd("BoneyLaugh", 2), None),
        spell=(("利维坦：咒弹", "Leviathan hurls a spell"), snd("Spell", 2), None),
        prepare=(("利维坦：蓄咒", "Leviathan prepares a summoning"),
                 snd("PrepareSummon", 1, start=2) + ["Sfx_mob_evokerPrepareSummon-001_soundWave.ogg"], None),
        cast=(("利维坦：施法", "Leviathan casts"),
              ["Sfx_multi_evokerCastSpell-%03d_soundWave.ogg" % i for i in (1, 2)], None),
        summoned=(("深渊里有骨头爬起", "Bones rise"),
                  ["Sfx_mob_skeletonNecromancerSummoned-%03d_soundWave.ogg" % i for i in (1, 2, 3)], None),
        impact=(("利维坦：咒弹命中", "Spell hits"),
                ["Sfx_item_necromancerArrowImpactNormal-%03d.ogg" % i for i in (1, 2, 3, 4)], None),
    ),
    sound_dir=os.path.join(HERE, "leviathan_ref", "sounds"),
    cues={
        "walk": [(0.0, "step", 0.5, 1.0), (0.8, "step", 0.5, 1.0)],
        "cast": [(0.0, "cast", 1.0, 1.0), (0.65, "spell", 1.0, 1.0)],
        "summon": [(1.0, "summoned", 1.0, 0.8)],
        "rise": [(1.6, "laugh", 1.2, 0.9)],
    },
    enter_cues={"summon": [("prepare", 1.0, 1.0)], "rise": [("summoned", 1.2, 0.7)]},
    hurt="hurt", death="death", ambient=("idle", 0.006),
)

# skill hook -> (clip, extra sound right away)
SKILLS = {
    "sk2_1": ("cast", "impact"),         # 沉锚：锚落处涌起漩涡
    "sk2_2": ("cast", "laugh"),          # 溺没
    "sk2_3": ("summon", None),           # 嫉羡
    "sk2_4": ("summon", "laugh"),        # 逆潮
    "sk2_5": ("cast", "impact"),         # 海渊重压
    "ult2_warn": ("summon", None),       # 妒海沉城蓄势
    "ult2": (None, "impact"),            # 妒海沉城
}


def dress(first):
    """As the undressed lord, at it: mount the parts in the rise pose."""
    lines = [
        "# 利维坦换装（as 降临者，at 其脚下）。只加 rpg.lv 标签与七个部件，不碰其他标签与数值。",
        "tag @s add rpg.lv",
        "tag @s add rpg.lv.dressing",
    ]
    for part, comp in first:
        lines.append(
            'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lv.part","rpg.lv.p.%s","rpg.lv.new"],'
            'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:leviathan/%s"}},'
            'item_display:"none",teleport_duration:2,interpolation_duration:2,'
            'view_range:1.5f,transformation:%s}' % (part, part, snbt_components(MOB, comp)))
    lines += [
        "execute as @e[type=minecraft:item_display,tag=rpg.lv.new,distance=..1] run "
        "ride @s mount @e[type=minecraft:vindicator,tag=rpg.lv.dressing,limit=1]",
        "tag @e[type=minecraft:item_display,tag=rpg.lv.new,distance=..1] remove rpg.lv.new",
        "tag @s remove rpg.lv.dressing",
        "function rpg:leviathan/anim/init",
        playsound(MOB, "prepare", 1.2, 0.8, 32),
        playsound(MOB, "laugh", 1.2, 0.8, 48),
        "function rpg:leviathan/anim/enter/rise",
    ]
    wf(os.path.join(MOB.func, "dress.mcfunction"), lines)


def write_datapack(baked):
    first = baked["rise"]["frames"][0][1]
    dress([(p, first[p]) for p, _ in MOB.parts])
    lord = "type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.lv,scores={rpg_dm_lord=2}"
    write_rig_runtime(MOB, [
        "# 利维坦每刻入口。任何召唤路径落地的第二柱都在这里换装（含封印逃逸、调试召唤）。",
        "execute if entity @e[%s,limit=1] as @e[%s] at @s run function rpg:leviathan/dress" % (lord, lord),
        "execute if entity @e[type=minecraft:vindicator,tag=rpg.lv,limit=1] as @e[type=minecraft:vindicator,tag=rpg.lv] at @s run function rpg:leviathan/follow",
    ], follow_extra=[
        "# 被法阵束缚时载体发光：部件一起发光",
        "execute if predicate rpg:leviathan/glowing unless entity @s[tag=rpg.lv.glow] run function rpg:leviathan/glow_on",
        "execute unless predicate rpg:leviathan/glowing if entity @s[tag=rpg.lv.glow] run function rpg:leviathan/glow_off",
    ])
    pred = os.path.join(DP, "data", NS, "predicate", "leviathan")
    for name, effect in (("glowing", "minecraft:glowing"), ("invisible", "minecraft:invisibility")):
        wj(os.path.join(pred, name + ".json"), {
            "condition": "minecraft:entity_properties", "entity": "this",
            "predicate": {"effects": {effect: {}}}})
    for name, on in (("glow_on", True), ("glow_off", False)):
        wf(os.path.join(MOB.func, name + ".mcfunction"), [
            "tag @s %s rpg.lv.glow" % ("add" if on else "remove"),
            "execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {Glowing:%db}"
            % (1 if on else 0),
        ])
    # after rpg:command/tick_end, the last thing that clears the lord's invisibility
    wf(os.path.join(MOB.func, "tick_late.mcfunction"), [
        "# 利维坦的身体是模型：载体本身始终隐身（驱魔的显形只清隐身效果，没有逻辑读它）。",
        "execute as @e[type=minecraft:vindicator,tag=rpg.lv] unless predicate rpg:leviathan/invisible "
        "run effect give @s minecraft:invisibility infinite 0 true",
    ])
    hook_tag(DP, "tick", "rpg:leviathan/tick_late", False)

    for hook, (clip, extra) in SKILLS.items():
        lines = ["# %s 的外观与音效。由 add_leviathan_model.py 生成。" % hook]
        if clip:
            lines.append("function rpg:leviathan/anim/enter/%s" % clip)
        if extra:
            lines.append("execute at @s run " + playsound(MOB, extra, 1.2, 1.0, 32))
        wf(os.path.join(MOB.func, "skill", hook + ".mcfunction"), lines)
        append(hook, "execute if entity @s[tag=rpg.lv] run function rpg:leviathan/skill/%s" % hook)
    # dissipating after ten minutes: its passengers die with it, no orphan
    prepend("advent_gone", [
        "execute if entity @s[tag=rpg.lv] run " + playsound(MOB, "laugh", 1.2, 0.7, 32),
    ])


def _read(name):
    path = os.path.join(TAINT, name + ".mcfunction")
    with io.open(path, encoding="utf-8") as fh:
        return path, fh.read().rstrip("\n").split("\n")


def append(name, line):
    path, lines = _read(name)
    if MARK in lines:
        return
    wf(path, lines + [MARK, line])


def prepend(name, new):
    """After the leading comment block."""
    path, lines = _read(name)
    if MARK in lines:
        return
    i = 0
    while i < len(lines) and lines[i].startswith("#"):
        i += 1
    wf(path, lines[:i] + [MARK] + new + lines[i:])


def main():
    baked, _ = build(MOB, RP, DP)
    if os.path.isdir(TAINT):
        write_datapack(baked)


if __name__ == "__main__":
    main()
