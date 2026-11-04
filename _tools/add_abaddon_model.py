# -*- coding: utf-8 -*-
"""亚巴顿 (Abaddon) -- the third of the seven lords, dressed as Minecraft
Dungeons' Wretched Wraith.

Only the look changes.  The lord is still the invisible vindicator that
rpg:taint/lord3 (and every other path that ends in `rpg_dm_lord 3`: the
seal escape, the debug summon) summons, with its tags, health, skills,
true-name inquest and exorcism untouched -- and with its standing black
smoke (opt_runtime_hotpaths.py) as it is.  Each tick, any such vindicator
not yet dressed gets the tag `rpg.ab` and six item_display parts mounted
beside its soul marker; the parts carry only `rpg.ab.*` tags, so no
`rpg.demon` / `devil` selector sees them.  They die with the lord: every
removal path either kills its passengers or leaves them riding nothing,
which the orphan sweep in display_mob.py catches.

The wiki shows no animation of the Wretched Wraith, and in Dungeons it is
the Tower Wraith's greater kin, so it plays the Tower Wraith's clips
(Mob.anim_from: tower_wraith.bbmodel, matched by bone name).  Its own
geometry is `_tools/abaddon_ref/abaddon.bbmodel` (see abaddon_geo.py): the
ice-crowned head with the pink gem, the frosted mantle, skeletal forearms
and the two ice fists.  The pink flecks, eyes, mouth and gem glow, after
the original emissive map.  Sounds are the Wretched Wraith set from
https://minecraft.wiki/w/Dungeons:Wretched_Wraith (abaddon_ref/sounds, see
SOURCES.md there).

Visibility as for 别西卜 and 利维坦: the carrier's invisibility is put back
after rpg:command/tick_end, and while the carrier glows (bound) the parts
glow.
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
MARK = "# 亚巴顿外观（add_abaddon_model.py）"


def snd(stem, n=None):
    if n is None:
        return ["WretchedWraith%s_soundwave.ogg" % stem]
    return ["WretchedWraith%s-%03d_soundwave.ogg" % (stem, i) for i in range(1, n + 1)]


MOB = Mob(
    key="abaddon", label="亚巴顿", generator="add_abaddon_model.py",
    bbmodel=os.path.join(HERE, "abaddon_ref", "abaddon.bbmodel"),
    anim_from=os.path.join(HERE, "tower_wraith_ref", "tower_wraith.bbmodel"),
    parts=[
        ("body", ["body"]),
        ("head", ["head", "crown", "crown_b", "eyes_glow", "gem"]),
        ("right_arm", ["right_arm"]),
        ("right_fist", ["right_fist"]),
        ("left_arm", ["left_arm"]),
        ("left_fist", ["left_fist"]),
    ],
    glow={"eyes_glow", "gem"},
    # the lord is a plain vindicator: seat 2.0 blocks; the boss stands near three tall
    seat=2.0, model_scale=0.55,
    tag="rpg.ab", score="rpg_ab",
    clips=[
        ("idle", 4, True),
        ("walk", 2, True),            # the forward glide
        ("cast", 1, False),           # arms up, thrust at 0.95 s
        ("spread", 1, False),         # arms flung wide, held 0.4..0.9 s
    ],
    sounds=dict(
        idle=(("亚巴顿：低吟", "Abaddon moans"), snd("Idle", 6), None),
        hurt=(("亚巴顿：受伤", "Abaddon hurts"), snd("Hurt", 3), None),
        death=(("亚巴顿：消散", "Abaddon fades"), snd("Death", 2), None),
        step=(("亚巴顿：踏冰", "Abaddon's ice crunches"), snd("WalkIce", 3), None),
        strike=(("亚巴顿：重击", "Abaddon strikes"), snd("BasicAttackFoley", 3), None),
        strike_vocal=(("亚巴顿：怒吼", "Abaddon roars"), snd("BasicAttackVocal", 3), None),
        bolt=(("亚巴顿：冰焰弹", "Abaddon hurls ghostfire"), snd("ProjectileAttackFoley", 3), None),
        bolt_vocal=(("亚巴顿：尖啸", "Abaddon shrieks"), snd("ProjectileAttackVocal", 3), None),
        circle=(("亚巴顿：冰焰环", "A ring of ghostfire"), snd("ProjectileCircleFoley", 3), None),
        circle_vocal=(("亚巴顿：咆哮", "Abaddon howls"), snd("ProjectileCircleVocal", 3), None),
        crown=(("亚巴顿：冰冠震鸣", "The ice crown rings"), snd("StunCrown", 2), None),
        summon=(("亚巴顿：召唤", "Abaddon summons"), snd("Summon", 1), None),
        intro=(("亚巴顿：现身", "Abaddon arrives"), snd("IntroVocal"), None),
        intro_foley=(("寒气骤起", "Frost rises"), snd("IntroFoley"), None),
    ),
    sound_dir=os.path.join(HERE, "abaddon_ref", "sounds"),
    cues={
        "walk": [(0.0, "step", 0.5, 1.0), (1.0, "step", 0.5, 1.0)],
        "cast": [(0.0, "bolt_vocal", 1.2, 1.0), (0.95, "bolt", 1.2, 1.0)],
        "spread": [(0.4, "circle", 1.2, 1.0)],
    },
    enter_cues={"spread": [("circle_vocal", 1.2, 1.0)]},
    hurt="hurt", death="death", ambient=("idle", 0.006),
)

# skill hook -> (clip, extra sound right away)
SKILLS = {
    "sk3_1": ("spread", "strike"),       # 收割：周身爆发
    "sk3_2": ("cast", "crown"),          # 沉眠
    "sk3_3": ("cast", "strike_vocal"),   # 深渊之口
    "sk3_4": ("spread", "crown"),        # 停摆
    "sk3_5": ("cast", "circle"),         # 死寂
    "ult3_warn": ("spread", "summon"),   # 终末收割蓄势
    "ult3": (None, "strike"),            # 终末收割
}


def dress(first):
    """As the undressed lord, at it: mount the parts and fling the arms wide."""
    lines = [
        "# 亚巴顿换装（as 降临者，at 其脚下）。只加 rpg.ab 标签与六个部件，不碰其他标签与数值。",
        "tag @s add rpg.ab",
        "tag @s add rpg.ab.dressing",
    ]
    for part, comp in first:
        lines.append(
            'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ab.part","rpg.ab.p.%s","rpg.ab.new"],'
            'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:abaddon/%s"}},'
            'item_display:"none",teleport_duration:2,interpolation_duration:2,'
            'view_range:1.5f,transformation:%s}' % (part, part, snbt_components(MOB, comp)))
    lines += [
        "execute as @e[type=minecraft:item_display,tag=rpg.ab.new,distance=..1] run "
        "ride @s mount @e[type=minecraft:vindicator,tag=rpg.ab.dressing,limit=1]",
        "tag @e[type=minecraft:item_display,tag=rpg.ab.new,distance=..1] remove rpg.ab.new",
        "tag @s remove rpg.ab.dressing",
        "function rpg:abaddon/anim/init",
        playsound(MOB, "intro_foley", 1.2, 1.0, 32),
        playsound(MOB, "intro", 1.2, 1.0, 48),
        "function rpg:abaddon/anim/enter/spread",
    ]
    wf(os.path.join(MOB.func, "dress.mcfunction"), lines)


def write_datapack(baked):
    first = baked["idle"]["frames"][0][1]
    dress([(p, first[p]) for p, _ in MOB.parts])
    lord = "type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.ab,scores={rpg_dm_lord=3}"
    write_rig_runtime(MOB, [
        "# 亚巴顿每刻入口。任何召唤路径落地的第三柱都在这里换装（含封印逃逸、调试召唤）。",
        "execute if entity @e[%s,limit=1] as @e[%s] at @s run function rpg:abaddon/dress" % (lord, lord),
        "execute if entity @e[type=minecraft:vindicator,tag=rpg.ab,limit=1] as @e[type=minecraft:vindicator,tag=rpg.ab] at @s run function rpg:abaddon/follow",
    ], follow_extra=[
        "# 被法阵束缚时载体发光：部件一起发光",
        "execute if predicate rpg:abaddon/glowing unless entity @s[tag=rpg.ab.glow] run function rpg:abaddon/glow_on",
        "execute unless predicate rpg:abaddon/glowing if entity @s[tag=rpg.ab.glow] run function rpg:abaddon/glow_off",
    ])
    pred = os.path.join(DP, "data", NS, "predicate", "abaddon")
    for name, effect in (("glowing", "minecraft:glowing"), ("invisible", "minecraft:invisibility")):
        wj(os.path.join(pred, name + ".json"), {
            "condition": "minecraft:entity_properties", "entity": "this",
            "predicate": {"effects": {effect: {}}}})
    for name, on in (("glow_on", True), ("glow_off", False)):
        wf(os.path.join(MOB.func, name + ".mcfunction"), [
            "tag @s %s rpg.ab.glow" % ("add" if on else "remove"),
            "execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {Glowing:%db}"
            % (1 if on else 0),
        ])
    # after rpg:command/tick_end, the last thing that clears the lord's invisibility
    wf(os.path.join(MOB.func, "tick_late.mcfunction"), [
        "# 亚巴顿的身体是模型：载体本身始终隐身（驱魔的显形只清隐身效果，没有逻辑读它）。",
        "execute as @e[type=minecraft:vindicator,tag=rpg.ab] unless predicate rpg:abaddon/invisible "
        "run effect give @s minecraft:invisibility infinite 0 true",
    ])
    hook_tag(DP, "tick", "rpg:abaddon/tick_late", False)

    for hook, (clip, extra) in SKILLS.items():
        lines = ["# %s 的外观与音效。由 add_abaddon_model.py 生成。" % hook]
        if clip:
            lines.append("function rpg:abaddon/anim/enter/%s" % clip)
        if extra:
            lines.append("execute at @s run " + playsound(MOB, extra, 1.2, 1.0, 32))
        wf(os.path.join(MOB.func, "skill", hook + ".mcfunction"), lines)
        append(hook, "execute if entity @s[tag=rpg.ab] run function rpg:abaddon/skill/%s" % hook)
    # dissipating after ten minutes: its passengers die with it, no orphan
    prepend("advent_gone", [
        "execute if entity @s[tag=rpg.ab] run " + playsound(MOB, "crown", 1.2, 0.7, 32),
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
