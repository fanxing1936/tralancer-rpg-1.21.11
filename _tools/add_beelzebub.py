# -*- coding: utf-8 -*-
"""别西卜 (Beelzebub) -- the fourth of the seven lords, dressed as Minecraft
Dungeons' Nameless One.

Only the look changes.  The lord is still the invisible vindicator that
rpg:taint/lord4 (and every other path that ends in `rpg_dm_lord 4`)
summons, with its tags, health, skills, true-name inquest and exorcism
untouched.  Each tick, any such vindicator not yet dressed gets the tag
`rpg.bz` and seven item_display parts mounted beside its soul marker; the
parts carry only `rpg.bz.*` tags, so no `rpg.demon` / `devil` selector
sees them.  They die with the lord: every removal path either kills its
passengers or leaves them riding nothing, which the orphan sweep in
display_mob.py catches.

Source of truth is `_tools/beelzebub_ref/beelzebub.bbmodel` (bootstrapped
by beelzebub_geo.py, posed and animated in Blockbench).  Sounds are the
Nameless One set from https://minecraft.wiki/w/Dungeons:Nameless_One
(beelzebub_ref/sounds, see SOURCES.md there).  Approach, Death, Distant
and WakeUp are stereo in the original, so the game plays them without
distance falloff; they are kept for the arena-wide moments.

Visibility: the exorcism reveals the lord by clearing invisibility (the
bind, the rite's visible phase, the judgment strike).  Nothing reads that
effect back, it is only what players see.  With the model the lord is
always visible, so the carrier's invisibility is put back after
rpg:command/tick_end (the last thing that clears it), and while the
carrier glows (bound) the parts glow too.
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
MARK = "# 别西卜外观（add_beelzebub.py）"


def snd(stem, n=None, kind="mob"):
    if n is None:
        return ["Sfx_%s_nameless%s-001_soundWave.ogg" % (kind, stem)]
    return ["Sfx_%s_nameless%s-%03d_soundWave.ogg" % (kind, stem, i) for i in range(1, n + 1)]


MOB = Mob(
    key="beelzebub", label="别西卜", generator="add_beelzebub.py",
    bbmodel=os.path.join(HERE, "beelzebub_ref", "beelzebub.bbmodel"),
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
    tag="rpg.bz", score="rpg_bz",
    clips=[
        ("idle", 4, True),
        ("walk", 2, True),            # the hover-glide
        ("cast", 1, False),           # staff raised, thrust at 0.65 s
        ("summon", 1, False),         # arms up, slam at 1.0 s
        ("rise", 2, False),           # coming up out of the ground on arrival
    ],
    sounds=dict(
        approach=(("别西卜：逼近", "Beelzebub approaches"), snd("Approach"), None),
        cast=(("别西卜：施法", "Beelzebub casts"), snd("Cast", 3), None),
        death=(("别西卜：消亡", "Beelzebub dies"), snd("Death"), None),
        distant=(("远处的低语", "Distant whispers"), snd("Distant", 4), None),
        fly=(("别西卜：飘行", "Beelzebub glides"), snd("Fly", 4), None),
        hurt=(("别西卜：受伤", "Beelzebub hurts"), snd("Hurt", 4), None),
        load=(("别西卜：蓄力", "Beelzebub gathers power"), snd("Load", 2), None),
        load_long=(("别西卜：长咒", "Beelzebub chants"), snd("LoadLongSpell"), None),
        poff=(("别西卜：消散", "Beelzebub vanishes"), snd("Poff"), None),
        spell=(("别西卜：咒弹", "Beelzebub hurls a spell"), snd("SpellFat"), None),
        teleport_in=(("别西卜：显现", "Beelzebub appears"), snd("TeleportIn", 4, "multi"), None),
        teleport_out=(("别西卜：遁去", "Beelzebub teleports"), snd("TeleportOut", 2), None),
        wake=(("别西卜：苏醒", "Beelzebub awakens"), snd("WakeUp", 3), None),
        idle=(("别西卜：低语", "Beelzebub murmurs"), snd("Idle", 3, "multi"), None),
        laugh=(("别西卜：冷笑", "Beelzebub laughs"), snd("LaughShort", 3, "multi"), None),
        laugh_long=(("别西卜：狂笑", "Beelzebub cackles"), snd("LaughLong", 3, "multi"), None),
    ),
    sound_dir=os.path.join(HERE, "beelzebub_ref", "sounds"),
    cues={
        "walk": [(0.0, "fly", 0.4, 1.0)],
        "cast": [(0.0, "cast", 1.0, 1.0)],
        "summon": [(1.0, "poff", 1.0, 0.8)],
        "rise": [(1.6, "laugh_long", 1.2, 1.0)],
    },
    enter_cues={"summon": [("load_long", 1.0, 1.0)], "rise": [("wake", 1.0, 1.0)]},
    hurt="hurt", death="death", ambient=("idle", 0.006),
)

# skill hook -> (clip, extra sound right away)
SKILLS = {
    "sk4_1": ("cast", "spell"),          # 余烬：前方喷灰
    "sk4_2": ("cast", "laugh"),          # 吞噬
    "sk4_3": ("summon", "fly"),          # 蝇群
    "sk4_4": ("summon", "laugh_long"),   # 腐宴
    "sk4_5": ("cast", "teleport_out"),   # 饥啮：扑向最近的人
    "ult4_warn": ("summon", None),       # 罪约蓄势（30 刻）
    "ult4": (None, "spell"),             # 万蝇饕宴
}


def dress(first):
    """As the undressed lord, at it: mount the parts in the rise pose."""
    lines = [
        "# 别西卜换装（as 降临者，at 其脚下）。只加 rpg.bz 标签与七个部件，不碰其他标签与数值。",
        "tag @s add rpg.bz",
        "tag @s add rpg.bz.dressing",
    ]
    for part, comp in first:
        lines.append(
            'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.bz.part","rpg.bz.p.%s","rpg.bz.new"],'
            'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:beelzebub/%s"}},'
            'item_display:"none",teleport_duration:2,interpolation_duration:2,'
            'view_range:1.5f,transformation:%s}' % (part, part, snbt_components(MOB, comp)))
    lines += [
        "execute as @e[type=minecraft:item_display,tag=rpg.bz.new,distance=..1] run "
        "ride @s mount @e[type=minecraft:vindicator,tag=rpg.bz.dressing,limit=1]",
        "tag @e[type=minecraft:item_display,tag=rpg.bz.new,distance=..1] remove rpg.bz.new",
        "tag @s remove rpg.bz.dressing",
        "function rpg:beelzebub/anim/init",
        playsound(MOB, "teleport_in", 1.2, 1.0, 32),
        playsound(MOB, "approach", 1.0, 1.0, 48),
        "function rpg:beelzebub/anim/enter/rise",
    ]
    wf(os.path.join(MOB.func, "dress.mcfunction"), lines)


def write_datapack(baked):
    first = baked["rise"]["frames"][0][1]
    dress([(p, first[p]) for p, _ in MOB.parts])
    lord = "type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.bz,scores={rpg_dm_lord=4}"
    write_rig_runtime(MOB, [
        "# 别西卜每刻入口。任何召唤路径落地的第四柱都在这里换装（含封印逃逸、调试召唤）。",
        "execute if entity @e[%s,limit=1] as @e[%s] at @s run function rpg:beelzebub/dress" % (lord, lord),
        "execute if entity @e[type=minecraft:vindicator,tag=rpg.bz,limit=1] as @e[type=minecraft:vindicator,tag=rpg.bz] at @s run function rpg:beelzebub/follow",
    ], follow_extra=[
        "execute if predicate rpg:beelzebub/distant run "
        "playsound rpg:beelzebub.distant hostile @a[distance=20..64] ~ ~ ~ 0.8 1",
        "# 被法阵束缚时载体发光：部件一起发光",
        "execute if predicate rpg:beelzebub/glowing unless entity @s[tag=rpg.bz.glow] run function rpg:beelzebub/glow_on",
        "execute unless predicate rpg:beelzebub/glowing if entity @s[tag=rpg.bz.glow] run function rpg:beelzebub/glow_off",
    ])
    pred = os.path.join(DP, "data", NS, "predicate", "beelzebub")
    wj(os.path.join(pred, "distant.json"), {"condition": "minecraft:random_chance", "chance": 0.003})
    for name, effect in (("glowing", "minecraft:glowing"), ("invisible", "minecraft:invisibility")):
        wj(os.path.join(pred, name + ".json"), {
            "condition": "minecraft:entity_properties", "entity": "this",
            "predicate": {"effects": {effect: {}}}})
    for name, on in (("glow_on", True), ("glow_off", False)):
        wf(os.path.join(MOB.func, name + ".mcfunction"), [
            "tag @s %s rpg.bz.glow" % ("add" if on else "remove"),
            "execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {Glowing:%db}"
            % (1 if on else 0),
        ])
    # after rpg:command/tick_end, the last thing that clears the lord's invisibility
    wf(os.path.join(MOB.func, "tick_late.mcfunction"), [
        "# 别西卜的身体是模型：载体本身始终隐身（驱魔的显形只清隐身效果，没有逻辑读它）。",
        "execute as @e[type=minecraft:vindicator,tag=rpg.bz] unless predicate rpg:beelzebub/invisible "
        "run effect give @s minecraft:invisibility infinite 0 true",
    ])
    hook_tag(DP, "tick", "rpg:beelzebub/tick_late", False)

    for hook, (clip, extra) in SKILLS.items():
        lines = ["# %s 的外观与音效。由 add_beelzebub.py 生成。" % hook]
        if clip:
            lines.append("function rpg:beelzebub/anim/enter/%s" % clip)
        if extra:
            lines.append("execute at @s run " + playsound(MOB, extra, 1.2, 1.0, 32))
        wf(os.path.join(MOB.func, "skill", hook + ".mcfunction"), lines)
        append(hook, "execute if entity @s[tag=rpg.bz] run function rpg:beelzebub/skill/%s" % hook)
    # dissipating after ten minutes: its passengers die with it, no orphan
    prepend("advent_gone", [
        "execute if entity @s[tag=rpg.bz] run " + playsound(MOB, "poff", 1.2, 1.0, 32),
        "execute if entity @s[tag=rpg.bz] run " + playsound(MOB, "teleport_out", 1.2, 0.8, 32),
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
