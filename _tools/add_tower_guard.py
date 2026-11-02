# -*- coding: utf-8 -*-
"""圣卫 (Holy Guard) -- the Minecraft Dungeons tower guard as a
display-entity mob.  In the setting it is the Pope's own legion: the armed
hand of the Holy See, which the hero ends up defying, so it is hostile.
Internal ids keep the tower_guard / rpg_tg names.

Source of truth is the Blockbench project
`_tools/tower_guard_ref/tower_guard.bbmodel`.  The shared pipeline in
display_mob.py turns it into the atlas, one Java item model per display
part (item definitions under `assets/rpg/items/tower_guard/`, used through
the `item_model` component) and the baked animation clips.  This script
adds the carrier: the summon function (an invisible vindicator carrying
the parts as passengers) and the per-tick entry.

Glow: the original `_S` layers mark the eyes and the glaive blade.

Sounds: the Dungeons tower guard set from
https://minecraft.wiki/w/Dungeons:Tower_Guard (tower_guard_ref/sounds,
see SOURCES.md there).  `block` is registered for the projectile
deflection, which the gameplay pass still has to wire up.
"""

import os
import sys

from display_mob import Mob, build, passenger, write_rig_runtime, wf

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

HERE = os.path.dirname(os.path.abspath(__file__))

# Carrier: an invisible vindicator.  Scale 1.15 gives a 0.69 x 2.24 block
# hitbox around the 35px-tall model.
CARRIER_SCALE = 1.15
MAX_HEALTH = 120


def snd(stem, n, fmt="%02d"):
    return ["S1_sfx_towerGuard_%s_%s.ogg" % (stem, fmt % i) for i in range(1, n + 1)]


MOB = Mob(
    key="tower_guard", label="圣卫", generator="add_tower_guard.py",
    bbmodel=os.path.join(HERE, "tower_guard_ref", "tower_guard.bbmodel"),
    parts=[
        ("body", ["body", "belt", "chin_guard"]),
        ("head", ["head", "helmet", "neck_guard", "eyes_glow"]),
        ("right_arm", ["right_arm", "right_pauldron"]),
        ("left_arm", ["left_arm", "left_pauldron"]),
        ("shield", ["shield"]),
        ("spear", ["spear", "spear_glow"]),
        ("cape", ["cape"]),
        ("right_leg", ["right_leg"]),
        ("left_leg", ["left_leg"]),
    ],
    glow={"eyes_glow", "spear_glow"},
    # vindicator passenger seat: 2.0 x scale, measured on a 1.21.11 server
    # (display Pos y - carrier Pos y = 2.3 at scale 1.15)
    seat=2.0 * CARRIER_SCALE,
    tag="rpg.tg", score="rpg_tg",
    # clip -> (ticks between samples, loops).  The order is the clip id in
    # the `rpg_tg_anim` score; idle (0) and walk (1) are the locomotion pair
    # picked from the carrier's movement.  A clip that does not loop falls
    # back to idle when it ends.
    clips=[
        ("idle", 4, True),
        ("walk", 2, True),
        ("attack", 1, False),         # glaive swing; the hit lands at 0.8 s
        ("charge", 2, True),          # the run itself; gameplay decides how long
        ("normal_stop", 2, False),
        ("collide_stop", 1, False),
        ("shield_break", 1, False),   # angry stomp
        ("stun", 2, True),
    ],
    sounds=dict(
        idle=(("圣卫：低声祷念", "Holy Guard mutters"), snd("idle", 7), None),
        hurt=(("圣卫：受伤", "Holy Guard hurts"), snd("hurt", 4), None),
        death=(("圣卫：倒下", "Holy Guard dies"), snd("death", 4), None),
        swing=(("圣卫：挥戟", "Glaive swings"), snd("basicAttack_swing", 3), None),
        armour=(("圣卫：甲胄铿锵", "Armor clanks"), snd("basicAttack_armour", 3), None),
        block=(("圣卫：盾挡", "Holy Guard blocks"), snd("block", 5), None),
        shield_break=(("圣卫：盾牌碎裂", "Shield breaks"), snd("shieldBreak", 3, "%03d"), None),
        shield_break_vocal=(("圣卫：怒吼", "Holy Guard roars"), snd("shieldBreak_vocal", 5), None),
        charge=(("圣卫：冲锋", "Holy Guard charges"), snd("chargeAttack_start", 4), None),
        stop=(("圣卫：刹步", "Holy Guard halts"), snd("chargeAttack_stop_normal", 3), None),
        collide=(("圣卫：撞击", "Holy Guard collides"), snd("chargeAttack_stop_collide", 4), None),
        step=(("圣卫：脚步", "Heavy footsteps"), snd("step", 8), None),
        stun=(("圣卫：眩晕", "Holy Guard is stunned"), snd("stun", 3), None),
    ),
    sound_dir=os.path.join(HERE, "tower_guard_ref", "sounds"),
    # on the baked frames, read off the clips' keys: feet land on the leg
    # extremes, the glaive hits at 0.8 s, the stomps at 0.3 / 0.65 / 1.0 s
    cues={
        "walk": [(0.0, "step", 0.6, 1.0), (0.4, "step", 0.6, 1.0)],
        "charge": [(0.0, "step", 0.8, 1.2), (0.3, "step", 0.8, 1.2)],
        "attack": [(0.0, "armour", 0.8, 1.0), (0.6, "swing", 1.0, 1.0)],
        "normal_stop": [(0.0, "stop", 1.0, 1.0)],
        "collide_stop": [(0.15, "collide", 1.0, 1.0)],
        "shield_break": [(0.0, "shield_break", 1.0, 1.0), (0.15, "shield_break_vocal", 1.0, 1.0),
                         (0.3, "step", 1.0, 0.8), (0.65, "step", 1.0, 0.8), (1.0, "step", 1.0, 0.8)],
    },
    enter_cues={"charge": [("charge", 1.0, 1.0)], "stun": [("stun", 1.0, 1.0)]},
    hurt="hurt", death="death", ambient=("idle", 0.008),
)


def write_datapack(rest):
    # gold: the Holy See's colour
    name = ('[{"text":"圣卫","color":"#E3B04B","bold":true}]')
    attrs = ('[{id:"minecraft:max_health",base:%df},{id:"minecraft:armor",base:12f},'
             '{id:"minecraft:scale",base:%sf},{id:"minecraft:knockback_resistance",base:0.8f},'
             '{id:"minecraft:movement_speed",base:0.24f},{id:"minecraft:attack_damage",base:0f},'
             '{id:"minecraft:follow_range",base:32f}]' % (MAX_HEALTH, CARRIER_SCALE))
    passengers = ",".join(passenger(MOB, p, m) for p, m in rest)
    wf(os.path.join(MOB.func, "summon.mcfunction"), [
        "# 圣卫：教皇直属的军团，借神之名行压迫的武装。",
        "# 隐形卫道士承载九个展示实体部件。由 _tools/add_tower_guard.py 生成。",
        "summon minecraft:vindicator ~ ~ ~ {Tags:[\"rpg.tg\"],Silent:1b,PersistenceRequired:1b,"
        "CanPickUpLoot:0b,Health:%df,CustomName:%s,"
        "active_effects:[{id:\"minecraft:invisibility\",duration:-1,amplifier:0,show_particles:0b}],"
        "attributes:%s,Passengers:[%s]}" % (MAX_HEALTH, name, attrs, passengers),
    ])
    write_rig_runtime(MOB, [
        "# 圣卫每刻入口：场上没有圣卫就只剩这两条带类型的存在性判定。",
        "execute if entity @e[type=minecraft:vindicator,tag=rpg.tg,limit=1] as @e[type=minecraft:vindicator,tag=rpg.tg] at @s run function rpg:tower_guard/follow",
    ])


def main():
    _, rest = build(MOB, RP, DP)
    write_datapack(rest)


if __name__ == "__main__":
    main()
