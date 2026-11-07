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

from display_mob import Mob, build, hook_tag, passenger, playsound, write_rig_runtime, wf

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

HERE = os.path.dirname(os.path.abspath(__file__))

# Carrier: an invisible vindicator.  Scale 1.15 gives a 0.69 x 2.24 block
# hitbox around the 35px-tall model.
CARRIER_SCALE = 1.15
MAX_HEALTH = 120
ARMOR = 12

SURVIVORS = "gamemode=!spectator,gamemode=!creative"
SHIELD_HITS = 6        # a hit from behind counts three
ATTACK_COOLDOWN = 40
CHARGE_COOLDOWN = 160
CHARGE_TICKS = 40
CHARGE_STEP = 0.5      # blocks per tick
ATTACK_DAMAGE = 8
CHARGE_DAMAGE = 10
# clip lengths in ticks, from the bbmodel
ATTACK_HIT, ATTACK_END = 16, 32
STOP_END = 40
COLLIDE_END = 32
STUN_END = COLLIDE_END + 30
BREAK_END = 26


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
    # extremes, the glaive hits at 0.8 s, the stomps at 0.3 / 0.65 / 1.0 s.
    # Several of them fight at once, so everything repeated is kept quiet.
    cues={
        "walk": [(0.0, "step", 0.2, 1.0), (0.4, "step", 0.2, 1.0)],
        "charge": [(0.0, "step", 0.3, 1.2), (0.3, "step", 0.3, 1.2)],
        "attack": [(0.0, "armour", 0.3, 1.0), (0.6, "swing", 0.5, 1.0)],
        "normal_stop": [(0.0, "stop", 1.0, 1.0)],
        "collide_stop": [(0.15, "collide", 1.0, 1.0)],
        "shield_break": [(0.0, "shield_break", 1.0, 1.0), (0.15, "shield_break_vocal", 1.0, 1.0),
                         (0.3, "step", 1.0, 0.8), (0.65, "step", 1.0, 0.8), (1.0, "step", 1.0, 0.8)],
    },
    enter_cues={"charge": [("charge", 1.0, 1.0)], "stun": [("stun", 1.0, 1.0)]},
    hurt="hurt", death="death", ambient=("idle", 0.002, 0.4), hurt_volume=0.4, death_volume=0.6,
)


def write_datapack(rest):
    # gold: the Holy See's colour
    name = ('[{"text":"圣卫","color":"#E3B04B","bold":true}]')
    attrs = ('[{id:"minecraft:max_health",base:%df},{id:"minecraft:armor",base:%df},'
             '{id:"minecraft:scale",base:%sf},{id:"minecraft:knockback_resistance",base:0.8f},'
             '{id:"minecraft:movement_speed",base:0.24f},{id:"minecraft:attack_damage",base:0f},'
             '{id:"minecraft:follow_range",base:32f}]' % (MAX_HEALTH, ARMOR, CARRIER_SCALE))
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
    ], follow_extra=["function rpg:tower_guard/ai/tick"])
    write_ai()


def write_ai():
    """Shield, glaive and charge.  rpg_tg_st is the guard's state: 0 free to
    act, 1 swinging, 2 charging, 3 braking, 4 crashed and stunned, 5 the
    shield breaking.  The carrier has no AI while it is committed to a move,
    so the charge keeps its line and the swing does not slide."""
    ai = os.path.join(MOB.func, "ai")
    fn = MOB.fn + "/ai"
    pause = "data merge entity @s {NoAI:1b}"
    resume = "data merge entity @s {NoAI:0b}"

    def enter(state):
        return ["scoreboard players set @s rpg_tg_st %d" % state,
                "scoreboard players set @s rpg_tg_ta 0"]

    def strike(amount):
        return ["tag @s add rpg.tg.self",
                "damage @a[distance=..2.2,%s,sort=nearest,limit=1] %d minecraft:mob_attack "
                "by @e[type=minecraft:vindicator,tag=rpg.tg.self,limit=1]" % (SURVIVORS, amount),
                "tag @s remove rpg.tg.self"]

    wf(os.path.join(ai, "load.mcfunction"), [
        "# 圣卫战斗计分板。由 add_tower_guard.py 生成。",
    ] + ["scoreboard objectives add %s dummy" % o
         for o in ("rpg_tg_st", "rpg_tg_ta", "rpg_tg_cd", "rpg_tg_cc", "rpg_tg_sh")])
    hook_tag(MOB.dp, "load", fn + "/load", False)

    wf(os.path.join(ai, "remove.mcfunction"), [
        "# 带着部件一起移除（as 载体）。",
        "execute on passengers run kill @s",
        "kill @s",
    ])
    wf(os.path.join(ai, "init.mcfunction"), [
        "# 新圣卫：盾满，冲锋冷却错开，免得一队人同时起步。",
        "scoreboard players set @s rpg_tg_st 0",
        "scoreboard players set @s rpg_tg_ta 0",
        "scoreboard players set @s rpg_tg_cd 0",
        "scoreboard players set @s rpg_tg_sh %d" % SHIELD_HITS,
        "execute store result score @s rpg_tg_cc run random value 40..120",
    ])
    wf(os.path.join(ai, "tick.mcfunction"), [
        "# 圣卫一刻的战斗（as、at 载体）。",
        "execute unless score @s rpg_tg_st matches 0.. run function %s/init" % fn,
        "execute if entity @s[tag=rpg.hurt,tag=!rpg.tg.broken] run function %s/shield_hit" % fn,
        "execute if score @s rpg_tg_st matches 1 run return run function %s/attack" % fn,
        "execute if score @s rpg_tg_st matches 2 run return run function %s/charge" % fn,
        "execute if score @s rpg_tg_st matches 3 run return run function %s/brake" % fn,
        "execute if score @s rpg_tg_st matches 4 run return run function %s/stun" % fn,
        "execute if score @s rpg_tg_st matches 5 run return run function %s/break_tick" % fn,
        "# 空闲：举盾挡下正面飞来的投射物。",
        "execute if entity @s[tag=!rpg.tg.broken] positioned ^ ^1.2 ^1.2 as "
        "@e[type=#minecraft:impact_projectiles,distance=..2.5] at @s run function %s/deflect" % fn,
        "scoreboard players remove @s[scores={rpg_tg_cd=1..}] rpg_tg_cd 1",
        "scoreboard players remove @s[scores={rpg_tg_cc=1..}] rpg_tg_cc 1",
        "execute if score @s rpg_tg_cd matches 0 if entity @a[distance=..3.2,%s] run return run function %s/attack_start"
        % (SURVIVORS, fn),
        "execute if score @s rpg_tg_cc matches 0 if entity @a[distance=6..16,%s] run function %s/charge_start"
        % (SURVIVORS, fn),
    ])

    wf(os.path.join(ai, "deflect.mcfunction"), [
        "# 盾面挡下一枚投射物（as、at 投射物）。",
        playsound(MOB, "block"),
        "particle minecraft:enchanted_hit ~ ~ ~ 0.2 0.2 0.2 0.1 8 normal",
        "kill @s",
    ])
    wf(os.path.join(ai, "shield_hit.mcfunction"), [
        "# 盾吃一下；从背后打算三下。",
        "scoreboard players remove @s rpg_tg_sh 1",
        "execute positioned ^ ^ ^-2 if entity @a[distance=..2.5,%s] run scoreboard players remove @s rpg_tg_sh 2"
        % SURVIVORS,
        "execute if score @s rpg_tg_sh matches ..0 run function %s/shield_break" % fn,
    ])
    wf(os.path.join(ai, "shield_break.mcfunction"), [
        "# 盾碎：此后不再格挡，护甲归零。",
        "tag @s add rpg.tg.broken",
        "attribute @s minecraft:armor base set 0",
        'execute on passengers if entity @s[tag=rpg.tg.p.shield] run data modify entity @s '
        'item.components."minecraft:item_model" set value "rpg:empty"',
        pause,
    ] + enter(5) + ["function %s/anim/enter/shield_break" % MOB.fn])
    wf(os.path.join(ai, "break_tick.mcfunction"), [
        "scoreboard players add @s rpg_tg_ta 1",
        "execute if score @s rpg_tg_ta matches %d.. run function %s/free" % (BREAK_END, fn),
    ])
    wf(os.path.join(ai, "free.mcfunction"), [
        "# 招式结束，回到自由状态。",
        "scoreboard players set @s rpg_tg_st 0",
        resume,
    ])

    wf(os.path.join(ai, "attack_start.mcfunction"), [
        "# 挥戟：转向最近的目标，定身出手。",
        pause,
        "execute facing entity @a[distance=..3.2,%s,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0" % SURVIVORS,
    ] + enter(1) + ["function %s/anim/enter/attack" % MOB.fn])
    wf(os.path.join(ai, "attack.mcfunction"), [
        "scoreboard players add @s rpg_tg_ta 1",
        "execute if score @s rpg_tg_ta matches %d positioned ^ ^ ^1.6 run function %s/attack_hit" % (ATTACK_HIT, fn),
        "execute if score @s rpg_tg_ta matches %d.. run function %s/attack_end" % (ATTACK_END, fn),
    ])
    wf(os.path.join(ai, "attack_hit.mcfunction"), ["# 戟刃落下：前方一人受击。"] + strike(ATTACK_DAMAGE))
    wf(os.path.join(ai, "attack_end.mcfunction"), [
        "scoreboard players set @s rpg_tg_cd %d" % ATTACK_COOLDOWN,
        "function %s/free" % fn,
    ])

    wf(os.path.join(ai, "charge_start.mcfunction"), [
        "# 冲锋：锁定此刻的方向，之后不再转向，所以可以侧身躲开，也可以引它撞墙。",
        pause,
        "execute facing entity @a[distance=6..16,%s,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0" % SURVIVORS,
    ] + enter(2) + ["function %s/anim/enter/charge" % MOB.fn])
    wf(os.path.join(ai, "charge.mcfunction"), [
        "# 直线推进；胸口以上被挡住算撞墙，只有脚下一格就迈上去。",
        "scoreboard players add @s rpg_tg_ta 1",
        "execute if score @s rpg_tg_ta matches %d.. run return run function %s/charge_stop" % (CHARGE_TICKS, fn),
        "execute positioned ^ ^ ^1 if entity @a[distance=..1.7,%s] run return run function %s/charge_hit"
        % (SURVIVORS, fn),
        "execute positioned ^ ^ ^0.9 unless block ~ ~1.2 ~ #minecraft:replaceable run return run function %s/charge_crash" % fn,
        "execute positioned ^ ^ ^0.9 unless block ~ ~0.2 ~ #minecraft:replaceable run return run tp @s ^ ^1 ^%s" % CHARGE_STEP,
        "tp @s ^ ^ ^%s" % CHARGE_STEP,
        "execute at @s if block ~ ~-0.1 ~ #minecraft:replaceable run tp @s ~ ~-0.5 ~",
    ])
    wf(os.path.join(ai, "charge_hit.mcfunction"),
       ["# 撞上目标：造成伤害后收势。", "execute positioned ^ ^ ^1 run function %s/charge_strike" % fn,
        "function %s/charge_stop" % fn])
    wf(os.path.join(ai, "charge_strike.mcfunction"), strike(CHARGE_DAMAGE))
    wf(os.path.join(ai, "charge_stop.mcfunction"),
       ["# 刹步。"] + enter(3) + ["function %s/anim/enter/normal_stop" % MOB.fn])
    wf(os.path.join(ai, "brake.mcfunction"), [
        "scoreboard players add @s rpg_tg_ta 1",
        "execute if score @s rpg_tg_ta matches %d.. run function %s/charge_end" % (STOP_END, fn),
    ])
    wf(os.path.join(ai, "charge_end.mcfunction"), [
        "scoreboard players set @s rpg_tg_cc %d" % CHARGE_COOLDOWN,
        "scoreboard players set @s rpg_tg_cd 20",
        "function %s/free" % fn,
    ])
    wf(os.path.join(ai, "charge_crash.mcfunction"), [
        "# 撞墙：卸下防御，这是输出窗口。",
        "attribute @s minecraft:armor base set 0",
    ] + enter(4) + ["function %s/anim/enter/collide_stop" % MOB.fn])
    wf(os.path.join(ai, "stun.mcfunction"), [
        "scoreboard players add @s rpg_tg_ta 1",
        "execute if score @s rpg_tg_ta matches %d run function %s/anim/enter/stun" % (COLLIDE_END, MOB.fn),
        "execute if score @s rpg_tg_ta matches %d.. run function %s/stun_end" % (STUN_END, fn),
    ])
    wf(os.path.join(ai, "stun_end.mcfunction"), [
        "execute if entity @s[tag=!rpg.tg.broken] run attribute @s minecraft:armor base set %d" % ARMOR,
        "function %s/anim/enter/idle" % MOB.fn,
        "function %s/charge_end" % fn,
    ])


def main():
    _, rest = build(MOB, RP, DP)
    write_datapack(rest)


if __name__ == "__main__":
    main()
