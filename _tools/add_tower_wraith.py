# -*- coding: utf-8 -*-
"""亚巴顿麾下的罪仆 dressed as Minecraft Dungeons' Tower Wraith -- the
hooded ghosts of the Tower, lesser kin of the Wretched Wraith whose look
亚巴顿 wears.

Only the look and voice change.  The servants stay the illagers
add_demon_minions.py summons (rpg.demon.minion.lord3: 古辛 the vanguard,
西迪 the hunter, 贝雷特 the ritualist, 列拉金 the hexer, 艾利欧格 the
executioner), with their health, AI, abilities, loot and lifetime
untouched.  Each tick any such servant not yet dressed gets the tag
`rpg.tw`, invisibility and its item_display parts.  As for 利维坦's
servants, no weapon is modelled: the servant's own vanilla mainhand item
is copied into the `weapon` part, drawn in `thirdperson_righthand` mode on
the model's right arm (Mob.held in display_mob.py), and the carrier's own
item model is set to `rpg:empty`.

All five share one model.  An illusioner cannot be dressed (its renderer
draws the body and four mirror copies even while invisible), so 列拉金,
the hexer, is summoned as a pillager (ROLE_OVERRIDES in
add_demon_minions.py); the selector still skips illusioners.

When a player comes within reach and the move is off cooldown, a clip
stands in for the illager's own swing or spell, which an invisible body
cannot show: crossbow carriers and the evoker raise their arms and cast at
range, everyone else claws in melee.

Source of truth is `_tools/tower_wraith_ref/tower_wraith.bbmodel`
(bootstrapped by tower_wraith_geo.py, posed and animated in Blockbench
after the wiki's animation renders); 亚巴顿 plays the same clips
(add_abaddon_model.py).  Texture and sounds from
https://minecraft.wiki/w/Dungeons:Tower_Wraith, see
tower_wraith_ref/SOURCES.md.
"""

import os
import sys

from display_mob import (Mob, NS, build, hook_tag, playsound, snbt_components,
                         wf, wj, write_rig_runtime)

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

HERE = os.path.dirname(os.path.abspath(__file__))


def snd(stem, n):
    return ["Sfx_mob_towerWraith%s-%03d_soundWave.ogg" % (stem, i) for i in range(1, n + 1)]


MOB = Mob(
    key="tower_wraith", label="幽魂罪仆", generator="add_tower_wraith.py",
    bbmodel=os.path.join(HERE, "tower_wraith_ref", "tower_wraith.bbmodel"),
    parts=[
        ("body", ["body"]),
        ("head", ["head", "eyes_glow"]),
        # its own part: the swept-back rest angle is past what an element may tilt
        ("brim", ["brim"]),
        ("banner", ["banner"]),
        ("right_arm", ["right_arm"]),
        ("left_arm", ["left_arm"]),
        ("weapon", ["right_arm"]),    # the carrier's own item, see Mob.held
    ],
    glow={"eyes_glow"},
    # vindicator, pillager and evoker share the illager seat: 2.0 blocks
    seat=2.0, model_scale=1.15,
    tag="rpg.tw", score="rpg_tw", carrier=None,
    clips=[
        ("idle", 4, True),
        ("walk", 2, True),            # the forward glide
        ("attack", 1, False),         # both claws come down at 0.45 s
        ("cast", 1, False),           # arms up, thrust at 0.95 s
    ],
    sounds=dict(
        idle=(("幽魂罪仆：低吟", "Wraith servant moans"), snd("Idle", 5), None),
        hurt=(("幽魂罪仆：受伤", "Wraith servant hurts"), snd("HurtVocal", 3), None),
        death=(("幽魂罪仆：消散", "Wraith servant fades"), snd("DeathVocal", 2) + snd("Death", 2), None),
        fly=(("幽魂罪仆：飘行", "Wraith servant glides"), snd("Fly", 5), None),
        attack_vocal=(("幽魂罪仆：嘶吼", "Wraith servant shrieks"), snd("AttackVocal", 2), None),
        attack=(("幽魂罪仆：爪击", "Wraith claws"), snd("Attack", 5), None),
        ember=(("幽魂罪仆：聚起冰焰", "Wraith gathers ghostfire"), snd("Ember", 5), None),
        appear=(("幽魂罪仆：现身", "Wraith servant appears"), snd("TeleportIn", 4), None),
    ),
    sound_dir=os.path.join(HERE, "tower_wraith_ref", "sounds"),
    cues={
        "walk": [(0.0, "fly", 0.4, 1.0)],
        "attack": [(0.25, "attack_vocal", 1.0, 1.0), (0.4, "attack", 1.0, 1.0)],
        "cast": [(0.0, "ember", 1.0, 1.0), (0.9, "attack_vocal", 1.0, 1.0)],
    },
    hurt="hurt", death="death", ambient=("idle", 0.006), held="weapon",
)

SERVANTS = "tag=rpg.demon.minion.lord3,tag=!rpg.tw,type=!minecraft:illusioner"
CAST_CD = 50                  # ticks between clips
CAST_RANGE = 12               # blocks, crossbow carriers and the evoker
SWING_RANGE = 3.2             # blocks, everyone else
CASTERS = "type=minecraft:pillager"
CASTERS_EV = "type=minecraft:evoker"


def write_datapack(baked):
    first = baked["idle"]["frames"][0][1]
    lines = [
        "# 亚巴顿麾下的罪仆换上塔中幽魂外观（as 罪仆，at 其脚下）。只加 rpg.tw 标签、隐身与部件，",
        "# 手上的物品不换，只把它的模型设成空的。",
        "tag @s add rpg.tw",
        "tag @s add rpg.tw.dressing",
        "effect give @s minecraft:invisibility infinite 0 true",
    ]
    for part, _ in MOB.parts:
        if part == MOB.held:
            lines.append(
                'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.tw.part","rpg.tw.p.%s","rpg.tw.new"],'
                'item_display:"thirdperson_righthand",teleport_duration:2,interpolation_duration:2,'
                'view_range:1f,transformation:%s}' % (part, snbt_components(MOB, first[part])))
            continue
        lines.append(
            'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.tw.part","rpg.tw.p.%s","rpg.tw.new"],'
            'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:tower_wraith/%s"}},'
            'item_display:"none",teleport_duration:2,interpolation_duration:2,'
            'view_range:1f,transformation:%s}' % (part, part, snbt_components(MOB, first[part])))
    lines += [
        "execute as @e[type=minecraft:item_display,tag=rpg.tw.new,distance=..1] run "
        "ride @s mount @e[tag=rpg.tw.dressing,limit=1]",
        "# 手里的原版物品复制到 weapon 部件上画出来，载体自己的那份只把模型设成空的",
        "item replace entity @e[type=minecraft:item_display,tag=rpg.tw.new,tag=rpg.tw.p.weapon,distance=..1,limit=1] "
        "contents from entity @s weapon.mainhand",
        'item modify entity @s weapon.mainhand {function:"minecraft:set_components",'
        'components:{"minecraft:item_model":"rpg:empty"}}',
        "tag @e[type=minecraft:item_display,tag=rpg.tw.new,distance=..1] remove rpg.tw.new",
        "tag @s remove rpg.tw.dressing",
        "scoreboard players set @s rpg_tw 0",
        "function rpg:tower_wraith/anim/init",
        "# 原作：塔中幽魂是瞬移现身的",
        playsound(MOB, "appear", 1.0, 1.0, 24),
    ]
    wf(os.path.join(MOB.func, "dress.mcfunction"), lines)
    wf(os.path.join(MOB.func, "strike.mcfunction"), [
        "# 有人进了距离：持弩的与司祭举臂施法，其余的双爪下劈。冷却借用 rpg_tw 的个体分数。",
        "scoreboard players set @s rpg_tw %d" % CAST_CD,
        "execute if entity @s[%s] run return run function rpg:tower_wraith/anim/enter/cast" % CASTERS,
        "execute if entity @s[%s] run return run function rpg:tower_wraith/anim/enter/cast" % CASTERS_EV,
        "function rpg:tower_wraith/anim/enter/attack",
    ])
    write_rig_runtime(MOB, [
        "# 幽魂罪仆每刻入口。任何途径召出的亚巴顿罪仆（手动、仪式二阶段）都在这里换装。",
        "execute if entity @e[%s,limit=1] as @e[%s] at @s run function rpg:tower_wraith/dress" % (SERVANTS, SERVANTS),
        "execute if entity @e[tag=rpg.tw,type=!minecraft:item_display,limit=1] "
        "as @e[tag=rpg.tw,type=!minecraft:item_display] at @s run function rpg:tower_wraith/follow",
    ], follow_extra=[
        "execute if score @s rpg_tw matches 1.. run scoreboard players remove @s rpg_tw 1",
        "execute if score @s rpg_tw matches ..0 unless score @s rpg_tw_anim matches 2..3 "
        "if entity @s[%s] "
        "if entity @a[distance=..%d,gamemode=!spectator,gamemode=!creative,limit=1] "
        "run function rpg:tower_wraith/strike" % (CASTERS, CAST_RANGE),
        "execute if score @s rpg_tw matches ..0 unless score @s rpg_tw_anim matches 2..3 "
        "if entity @s[%s] "
        "if entity @a[distance=..%d,gamemode=!spectator,gamemode=!creative,limit=1] "
        "run function rpg:tower_wraith/strike" % (CASTERS_EV, CAST_RANGE),
        "execute if score @s rpg_tw matches ..0 unless score @s rpg_tw_anim matches 2..3 "
        "unless entity @s[%s] unless entity @s[%s] "
        "if entity @a[distance=..%s,gamemode=!spectator,gamemode=!creative,limit=1] "
        "run function rpg:tower_wraith/strike" % (CASTERS, CASTERS_EV, SWING_RANGE),
    ])
    pred = os.path.join(DP, "data", NS, "predicate", "tower_wraith")
    wj(os.path.join(pred, "invisible.json"), {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"effects": {"minecraft:invisibility": {}}}})
    # the warden phase clears invisibility from whatever attacked something;
    # the servant's body is the model, so put it back after everything else
    wf(os.path.join(MOB.func, "tick_late.mcfunction"), [
        "# 幽魂罪仆的身体是模型：载体始终隐身。",
        "execute as @e[tag=rpg.tw,type=!minecraft:item_display] unless predicate rpg:tower_wraith/invisible "
        "run effect give @s minecraft:invisibility infinite 0 true",
    ])
    hook_tag(DP, "tick", "rpg:tower_wraith/tick_late", False)


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
