# -*- coding: utf-8 -*-
"""圣卫的另外两种（用户 2026-11-14：圣卫一共三种）。

    python add_holy_guards.py ../resourcepack ../rpg

  塔卫（add_tower_guard.py，rpg.tg）     盾 + 长戟 + 冲锋，原样不动
  重盾 royal_guard（rpg.rg）            原作皇家卫兵：巨盾挡正面（正面来的伤害退回七成、投射物挡下），
                                        贴身一锤砸地；砸完盾放下、喘一口气，这是输出窗口
  术士 end_illager（rpg.ei）            原作「终末灾厄村民」：只在回响虚空结尾的预渲染动画里出现，本体没有它的
                                        模型；开发者说它像唤魔者，所以用原作唤魔者的网格和动作，袍子按动画改成褐色、
                                        去掉兜帽（dungeons_models.py）。保持距离放圣光弹，被贴身就瞬移走，
                                        隔一阵给附近的圣卫回血

三种都打 rpg.hg：rpg:holy_guard/summon 随机召一种（教皇战、篡夺者的授权都走它）。
模型从本体提取（<key>_dungeons_ref/，dungeons_models.py）；声音用原版事件。
"""

import os
import sys

import add_usurper_fx_art as fxart
import dungeons_variant
from display_mob import Mob, build, hook_tag, passenger, playsound, wf, write_rig_runtime

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"
HERE = os.path.dirname(os.path.abspath(__file__))
SURV = "gamemode=!spectator,gamemode=!creative"
GOLD = "#E3B04B"             # 圣卫的名字色（教皇的军团）
HOLY_LIGHT = "#FFF2A8"


def ev(zh, en, *ids):
    return ((zh, en), list(ids), {"type": "event"})


def mob(key, label, tag, score, scale, clips, sounds, cues):
    m = Mob(key=key, label=label, generator="add_holy_guards.py",
            bbmodel=os.path.join(HERE, key + "_dungeons_ref", key + ".bbmodel"), parts=[], glow=(),
            seat=2.0 * scale, tag=tag, score=score, clips=clips, sounds=sounds,
            sound_dir=os.path.join(HERE, "dungeons_sounds"), cues=cues,
            hurt="hurt", death="death", ambient=("idle", 0.002, 0.5), hurt_volume=0.5, death_volume=0.7)
    if not dungeons_variant.apply(m):
        raise SystemExit("%s: the extracted model is missing (python dungeons_models.py %s)" % (key, key))
    return m


# ---------------------------------------------------------------------------------------------
# 重盾：原作皇家卫兵
# ---------------------------------------------------------------------------------------------
RG_SCALE, RG_HEALTH, RG_ARMOR, RG_SPEED = 1.15, 160, 16, 0.2
RG_REACH, RG_HIT, RG_END, RG_REST, RG_CD, RG_DMG, RG_SLAM_R = 3.0, 12, 37, 24, 50, 9, 2.6
RG_REFUND = 7                 # 正面来的伤害退回 7/10
RG = mob("royal_guard", "圣卫·重盾", "rpg.rg", "rpg_rg", RG_SCALE,
         clips=[("idle", 4, True), ("walk", 2, True), ("attack", 1, False), ("stun", 2, True)],
         sounds=dict(
             idle=ev("重盾：低声祷念", "Shield Guard mutters", "minecraft:entity.vindicator.ambient"),
             hurt=ev("重盾：受伤", "Shield Guard hurts", "minecraft:entity.vindicator.hurt"),
             death=ev("重盾：倒下", "Shield Guard dies", "minecraft:entity.vindicator.death"),
             block=ev("重盾：盾挡", "Shield Guard blocks", "minecraft:item.shield.block"),
             slam=ev("重盾：砸地", "Mace slams", "minecraft:item.mace.smash_ground"),
             step=ev("重盾：脚步", "Heavy footsteps", "minecraft:entity.iron_golem.step"),
         ),
         cues={"walk": [(0.0, "step", 0.25, 0.9), (0.4, "step", 0.25, 0.9)]})


def royal_guard(rest):
    m, fn = RG, RG.fn
    ai = os.path.join(m.func, "ai")
    attrs = ('[{id:"minecraft:max_health",base:%df},{id:"minecraft:armor",base:%df},{id:"minecraft:scale",base:%sf},'
             '{id:"minecraft:knockback_resistance",base:1f},{id:"minecraft:movement_speed",base:%sf},'
             '{id:"minecraft:attack_damage",base:0f},{id:"minecraft:follow_range",base:32f}]'
             % (RG_HEALTH, RG_ARMOR, RG_SCALE, RG_SPEED))
    wf(os.path.join(m.func, "summon.mcfunction"), [
        "# 圣卫·重盾：原作皇家卫兵。隐形卫道士承载展示实体部件。由 _tools/add_holy_guards.py 生成。",
        "summon minecraft:vindicator ~ ~ ~ {Tags:[\"rpg.rg\",\"rpg.hg\"],Silent:1b,PersistenceRequired:1b,CanPickUpLoot:0b,"
        "Health:%df,CustomName:[{\"text\":\"圣卫·重盾\",\"color\":\"%s\",\"bold\":true}],"
        "active_effects:[{id:\"minecraft:invisibility\",duration:-1,amplifier:0,show_particles:0b}],attributes:%s,Passengers:[%s]}"
        % (RG_HEALTH, GOLD, attrs, ",".join(passenger(m, p, c) for p, c in rest)),
    ])
    write_rig_runtime(m, [
        "# 重盾每刻入口。",
        "execute if entity @e[type=minecraft:vindicator,tag=rpg.rg,limit=1] as @e[type=minecraft:vindicator,tag=rpg.rg] at @s run function %s/follow" % fn,
    ], follow_extra=["function %s/ai/tick" % fn])
    pause, resume = "data merge entity @s {NoAI:1b}", "data merge entity @s {NoAI:0b}"

    def enter(state):
        return ["scoreboard players set @s rpg_rg_st %d" % state, "scoreboard players set @s rpg_rg_ta 0"]

    wf(os.path.join(ai, "load.mcfunction"), ["# 重盾计分板。由 add_holy_guards.py 生成。"] + [
        "scoreboard objectives add %s dummy" % o for o in ("rpg_rg_st", "rpg_rg_ta", "rpg_rg_cd", "rpg_rg_v")] + [
        "scoreboard players set #ten rpg_rg_v 10", "scoreboard players set #keep rpg_rg_v %d" % RG_REFUND])
    hook_tag(m.dp, "load", fn + "/ai/load", False)
    wf(os.path.join(ai, "remove.mcfunction"), ["# 带着部件一起移除（as 载体）。", "execute on passengers run kill @s", "kill @s"])
    wf(os.path.join(ai, "init.mcfunction"), [
        "scoreboard players set @s rpg_rg_st 0", "scoreboard players set @s rpg_rg_ta 0",
        "execute store result score @s rpg_rg_cd run random value 10..40",
    ])
    wf(os.path.join(ai, "tick.mcfunction"), [
        "# 重盾一刻（as/at 载体）。0 举盾自由，1 砸锤，2 放盾喘息。",
        "execute unless score @s rpg_rg_st matches 0.. run function %s/ai/init" % fn,
        "execute if entity @s[tag=rpg.hurt] unless score @s rpg_rg_st matches 2 run function %s/ai/guard" % fn,
        "execute if score @s rpg_rg_st matches 1 run return run function %s/ai/attack" % fn,
        "execute if score @s rpg_rg_st matches 2 run return run function %s/ai/rest" % fn,
        "# 举盾：正面飞来的投射物挡下",
        "execute positioned ^ ^1.2 ^1.2 as @e[type=#minecraft:impact_projectiles,distance=..2.5] at @s run function %s/ai/deflect" % fn,
        "scoreboard players remove @s[scores={rpg_rg_cd=1..}] rpg_rg_cd 1",
        "execute if score @s rpg_rg_cd matches 0 if entity @a[distance=..%s,%s] run function %s/ai/attack_start" % (RG_REACH, SURV, fn),
    ])
    wf(os.path.join(ai, "deflect.mcfunction"), [
        "# 巨盾挡下一枚投射物（as/at 投射物）。",
        playsound(m, "block"), "particle minecraft:enchanted_hit ~ ~ ~ 0.2 0.2 0.2 0.1 8 normal", "kill @s"])
    wf(os.path.join(ai, "guard.mcfunction"), [
        "# 挨了一下（as 载体）：打的人在盾面前方，就把这一下退回七成（同教皇外壳）；从背后或侧面打照吃",
        "execute positioned ^ ^ ^1.8 unless entity @a[distance=..2.6,%s] run return 0" % SURV,
        "scoreboard players operation #lost rpg_rg_v = @s damage_timing",
        "scoreboard players operation #lost rpg_rg_v -= @s damage_action",
        "execute if score #lost rpg_rg_v matches ..0 run return 0",
        "scoreboard players operation #lost rpg_rg_v *= #keep rpg_rg_v",
        "scoreboard players operation #lost rpg_rg_v /= #ten rpg_rg_v",
        "scoreboard players operation #hp rpg_rg_v = @s damage_action",
        "scoreboard players operation #hp rpg_rg_v += #lost rpg_rg_v",
        "execute store result entity @s Health float 1 run scoreboard players get #hp rpg_rg_v",
        "scoreboard players operation @s damage_timing = #hp rpg_rg_v",
        "scoreboard players operation @s damage_action = #hp rpg_rg_v",
        playsound(m, "block", 0.8, 0.9),
        "particle minecraft:enchanted_hit ^ ^1.2 ^0.8 0.3 0.4 0.3 0.1 10 normal",
    ])
    wf(os.path.join(ai, "attack_start.mcfunction"), [
        "# 砸锤：转向最近的人，定身出手",
        pause,
        "execute facing entity @a[distance=..%s,%s,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0" % (RG_REACH + 1, SURV),
    ] + enter(1) + ["function %s/anim/enter/attack" % fn])
    wf(os.path.join(ai, "attack.mcfunction"), [
        "scoreboard players add @s rpg_rg_ta 1",
        "execute if score @s rpg_rg_ta matches %d positioned ^ ^ ^1.6 run function %s/ai/slam" % (RG_HIT, fn),
        "execute if score @s rpg_rg_ta matches %d.. run function %s/ai/rest_start" % (RG_END, fn),
    ])
    wf(os.path.join(ai, "slam.mcfunction"), [
        "# 锤落地（at 落点）：一圈人受伤",
        "tag @s add rpg.rg.self",
        "execute as @a[distance=..%s,%s] run damage @s %d minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.rg.self,limit=1]"
        % (RG_SLAM_R, SURV, RG_DMG),
        "tag @s remove rpg.rg.self",
        playsound(m, "slam", 1.0, 0.9),
        "particle minecraft:dust_pillar{block_state:\"minecraft:gold_block\"} ~ ~0.1 ~ 1.2 0.1 1.2 0 30 normal",
        "particle minecraft:end_rod ~ ~0.3 ~ 1 0.1 1 0.04 12 normal",
    ])
    wf(os.path.join(ai, "rest_start.mcfunction"),
       ["# 砸完放下盾喘一口气：这时候盾不挡"] + enter(2) + ["function %s/anim/enter/stun" % fn])
    wf(os.path.join(ai, "rest.mcfunction"), [
        "scoreboard players add @s rpg_rg_ta 1",
        "execute if score @s rpg_rg_ta matches %d.. run function %s/ai/free" % (RG_REST, fn),
    ])
    wf(os.path.join(ai, "free.mcfunction"), [
        "scoreboard players set @s rpg_rg_st 0", "scoreboard players set @s rpg_rg_cd %d" % RG_CD,
        "function %s/anim/enter/idle" % fn, resume,
    ])


# ---------------------------------------------------------------------------------------------
# 术士：原作「终末灾厄村民」（唤魔者网格，褐袍）
# ---------------------------------------------------------------------------------------------
EI_SCALE, EI_HEALTH, EI_ARMOR, EI_SPEED = 1.1, 70, 2, 0.3
EI_CAST_AT, EI_CAST_END, EI_CAST_CD, EI_NEAR, EI_FAR = 30, 62, 70, 5, 20
EI_BOLT_SPEED, EI_BOLT_LIFE, EI_BOLT_DMG = 0.7, 40, 6
EI_BLINK_R, EI_BLINK_D, EI_BLINK_CD = 4, 8, 100
EI_HEAL_AT, EI_HEAL_END, EI_HEAL_CD, EI_HEAL_R = 40, 73, 240, 12
EI = mob("end_illager", "圣卫·术士", "rpg.ei", "rpg_ei", EI_SCALE,
         clips=[("idle", 4, True), ("walk", 2, True), ("cast", 1, False), ("strong", 1, False), ("summon", 1, False),
                ("rise", 2, False), ("hurt", 1, False), ("stun", 2, True)],
         sounds=dict(
             idle=ev("术士：低语", "Robed Guard murmurs", "minecraft:entity.evoker.ambient"),
             hurt=ev("术士：受伤", "Robed Guard hurts", "minecraft:entity.evoker.hurt"),
             death=ev("术士：倒下", "Robed Guard dies", "minecraft:entity.evoker.death"),
             prepare=ev("术士：蓄咒", "Robed Guard gathers a spell", "minecraft:entity.evoker.prepare_attack"),
             cast=ev("术士：施咒", "Robed Guard casts", "minecraft:entity.evoker.cast_spell"),
             blink=ev("术士：瞬移", "Robed Guard blinks", "minecraft:entity.enderman.teleport"),
             heal=ev("术士：祝圣", "Robed Guard blesses", "minecraft:block.beacon.power_select"),
         ),
         cues={"cast": [(0.1, "prepare", 1.0, 1.1)], "strong": [(0.2, "prepare", 1.0, 0.8)]})


def end_illager(rest):
    m, fn = EI, EI.fn
    ai = os.path.join(m.func, "ai")
    attrs = ('[{id:"minecraft:max_health",base:%df},{id:"minecraft:armor",base:%df},{id:"minecraft:scale",base:%sf},'
             '{id:"minecraft:movement_speed",base:%sf},{id:"minecraft:attack_damage",base:0f},{id:"minecraft:follow_range",base:32f}]'
             % (EI_HEALTH, EI_ARMOR, EI_SCALE, EI_SPEED))
    wf(os.path.join(m.func, "summon.mcfunction"), [
        "# 圣卫·术士：原作终末灾厄村民（唤魔者网格，褐袍）。由 _tools/add_holy_guards.py 生成。",
        "summon minecraft:vindicator ~ ~ ~ {Tags:[\"rpg.ei\",\"rpg.hg\"],Silent:1b,PersistenceRequired:1b,CanPickUpLoot:0b,"
        "Health:%df,CustomName:[{\"text\":\"圣卫·术士\",\"color\":\"%s\",\"bold\":true}],"
        "active_effects:[{id:\"minecraft:invisibility\",duration:-1,amplifier:0,show_particles:0b}],attributes:%s,Passengers:[%s]}"
        % (EI_HEALTH, GOLD, attrs, ",".join(passenger(m, p, c) for p, c in rest)),
    ])
    write_rig_runtime(m, [
        "# 术士每刻入口；圣光弹不跟载体走，单独推进。",
        "execute if entity @e[type=minecraft:vindicator,tag=rpg.ei,limit=1] as @e[type=minecraft:vindicator,tag=rpg.ei] at @s run function %s/follow" % fn,
        "execute if entity @e[type=minecraft:text_display,tag=rpg.ei.bolt,limit=1] as @e[type=minecraft:text_display,tag=rpg.ei.bolt] at @s run function %s/ai/bolt" % fn,
    ], follow_extra=["function %s/ai/tick" % fn])
    pause, resume = "data merge entity @s {NoAI:1b}", "data merge entity @s {NoAI:0b}"

    def enter(state):
        return ["scoreboard players set @s rpg_ei_st %d" % state, "scoreboard players set @s rpg_ei_ta 0"]

    wf(os.path.join(ai, "load.mcfunction"), ["# 术士计分板。由 add_holy_guards.py 生成。"] + [
        "scoreboard objectives add %s dummy" % o for o in ("rpg_ei_st", "rpg_ei_ta", "rpg_ei_cd", "rpg_ei_bc", "rpg_ei_hc", "rpg_ei_life")])
    hook_tag(m.dp, "load", fn + "/ai/load", False)
    wf(os.path.join(ai, "remove.mcfunction"), ["# 带着部件一起移除（as 载体）。", "execute on passengers run kill @s", "kill @s"])
    wf(os.path.join(ai, "init.mcfunction"), [
        "scoreboard players set @s rpg_ei_st 0", "scoreboard players set @s rpg_ei_ta 0", "scoreboard players set @s rpg_ei_bc 0",
        "execute store result score @s rpg_ei_cd run random value 20..60",
        "execute store result score @s rpg_ei_hc run random value 80..160",
    ])
    wf(os.path.join(ai, "tick.mcfunction"), [
        "# 术士一刻（as/at 载体）。0 自由，1 放圣光弹，2 祝圣同伴。",
        "execute unless score @s rpg_ei_st matches 0.. run function %s/ai/init" % fn,
        "execute if score @s rpg_ei_st matches 1 run return run function %s/ai/cast" % fn,
        "execute if score @s rpg_ei_st matches 2 run return run function %s/ai/heal" % fn,
        "scoreboard players remove @s[scores={rpg_ei_cd=1..}] rpg_ei_cd 1",
        "scoreboard players remove @s[scores={rpg_ei_bc=1..}] rpg_ei_bc 1",
        "scoreboard players remove @s[scores={rpg_ei_hc=1..}] rpg_ei_hc 1",
        "execute if score @s rpg_ei_bc matches 0 if entity @a[distance=..%d,%s] run return run function %s/ai/blink" % (EI_BLINK_R, SURV, fn),
        "execute if score @s rpg_ei_hc matches 0 if entity @e[type=minecraft:vindicator,tag=rpg.hg,tag=!rpg.ei,distance=..%d] run return run function %s/ai/heal_start" % (EI_HEAL_R, fn),
        "execute if score @s rpg_ei_cd matches 0 if entity @a[distance=%d..%d,%s] run function %s/ai/cast_start" % (EI_NEAR, EI_FAR, SURV, fn),
        "execute if entity @s[tag=rpg.hurt] run function %s/anim/enter/hurt" % fn,
    ])
    wf(os.path.join(ai, "cast_start.mcfunction"), [
        "# 圣光弹：转向最近的人，定身念咒",
        pause,
        "execute facing entity @a[distance=..%d,%s,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0" % (EI_FAR + 2, SURV),
    ] + enter(1) + ["function %s/anim/enter/cast" % fn])
    wf(os.path.join(ai, "cast.mcfunction"), [
        "scoreboard players add @s rpg_ei_ta 1",
        "execute if score @s rpg_ei_ta matches %d positioned ^ ^1.7 ^0.8 run function %s/ai/fire" % (EI_CAST_AT, fn),
        "execute if score @s rpg_ei_ta matches %d.. run function %s/ai/free" % (EI_CAST_END, fn),
    ])
    bolt = ('summon minecraft:text_display ~ ~ ~ {Tags:["rpg.ei.bolt","rpg.ei.bnew"],text:{text:"%s",font:"%s",color:"%s"},'
            'background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,view_range:2f,'
            'transformation:{translation:[0f,-0.2f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.4f,1.4f,1.4f],right_rotation:[0f,0f,0f,1f]}}'
            % (fxart.glyph_text("star", 1), "rpg:" + fxart.FONT_NAME, HOLY_LIGHT))
    wf(os.path.join(ai, "fire.mcfunction"), [
        "# 放出一枚圣光弹（at 手前），朝最近的人的眼睛直飞",
        bolt,
        "execute as @e[type=minecraft:text_display,tag=rpg.ei.bnew] at @s run tp @s ~ ~ ~ facing entity @a[distance=..%d,%s,sort=nearest,limit=1] eyes" % (EI_FAR + 4, SURV),
        "scoreboard players set @e[type=minecraft:text_display,tag=rpg.ei.bnew] rpg_ei_life %d" % EI_BOLT_LIFE,
        "tag @e[type=minecraft:text_display,tag=rpg.ei.bnew] remove rpg.ei.bnew",
        playsound(m, "cast", 1.0, 1.2),
        "particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.05 10 normal",
    ])
    wf(os.path.join(ai, "bolt.mcfunction"), [
        "# 圣光弹（as/at 弹）：前进，碰到人就打，撞墙或飞够了就散",
        "scoreboard players remove @s rpg_ei_life 1",
        "execute if score @s rpg_ei_life matches ..0 run return run function %s/ai/bolt_pop" % fn,
        "tp @s ^ ^ ^%s" % EI_BOLT_SPEED,
        "execute positioned ~ ~-1 ~ if entity @a[distance=..1.1,%s] run return run function %s/ai/bolt_hit" % (SURV, fn),
        "execute unless block ~ ~ ~ #minecraft:replaceable run return run function %s/ai/bolt_pop" % fn,
        "particle minecraft:dust{color:[1.0,0.95,0.66],scale:1.0} ~ ~ ~ 0.05 0.05 0.05 0 2 normal",
        "particle minecraft:end_rod ~ ~ ~ 0 0 0 0.01 1 normal",
    ])
    wf(os.path.join(ai, "bolt_hit.mcfunction"), [
        "execute positioned ~ ~-1 ~ as @a[distance=..1.1,%s] run damage @s %d minecraft:magic by @e[type=minecraft:vindicator,tag=rpg.ei,limit=1,sort=nearest]"
        % (SURV, EI_BOLT_DMG),
        "function %s/ai/bolt_pop" % fn,
    ])
    wf(os.path.join(ai, "bolt_pop.mcfunction"), [
        "particle minecraft:flash{color:16774824} ~ ~ ~ 0 0 0 0 1 normal",
        "particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.08 12 normal",
        "playsound minecraft:block.amethyst_block.break hostile @a[distance=..16] ~ ~ ~ 0.8 1.6",
        "kill @s",
    ])
    wf(os.path.join(ai, "blink.mcfunction"), [
        "# 被贴身：背向最近的人瞬移 %d 格，落在地面上" % EI_BLINK_D,
        "scoreboard players set @s rpg_ei_bc %d" % EI_BLINK_CD,
        "particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40 normal",
        playsound(m, "blink", 1.0, 1.0),
        "execute facing entity @a[distance=..%d,%s,sort=nearest,limit=1] feet rotated ~ 0 positioned ^ ^ ^-%d "
        "positioned over motion_blocking_no_leaves if block ~ ~1 ~ #minecraft:replaceable run tp @s ~ ~ ~ ~180 0"
        % (EI_BLINK_R + 1, SURV, EI_BLINK_D),
        "execute at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40 normal",
        "function %s/anim/enter/rise" % fn,
    ])
    wf(os.path.join(ai, "heal_start.mcfunction"), [
        "# 祝圣：双手高举，给 %d 格内的圣卫回血" % EI_HEAL_R, pause,
    ] + enter(2) + ["function %s/anim/enter/strong" % fn])
    wf(os.path.join(ai, "heal.mcfunction"), [
        "scoreboard players add @s rpg_ei_ta 1",
        "execute if score @s rpg_ei_ta matches %d run function %s/ai/bless" % (EI_HEAL_AT, fn),
        "execute if score @s rpg_ei_ta matches %d.. run function %s/ai/free" % (EI_HEAL_END, fn),
    ])
    wf(os.path.join(ai, "bless.mcfunction"), [
        "execute as @e[type=minecraft:vindicator,tag=rpg.hg,distance=..%d] run effect give @s minecraft:regeneration 5 1 true" % EI_HEAL_R,
        "execute as @e[type=minecraft:vindicator,tag=rpg.hg,distance=..%d] at @s run particle minecraft:happy_villager ~ ~1.4 ~ 0.4 0.6 0.4 0 10 normal" % EI_HEAL_R,
        "particle minecraft:end_rod ~ ~2.4 ~ 0.6 0.4 0.6 0.05 24 normal",
        playsound(m, "heal", 1.0, 1.4),
    ])
    wf(os.path.join(ai, "free.mcfunction"), [
        "scoreboard players set @s rpg_ei_st 0", "scoreboard players set @s rpg_ei_cd %d" % EI_CAST_CD,
        "execute if score @s rpg_ei_hc matches ..0 run scoreboard players set @s rpg_ei_hc %d" % EI_HEAL_CD, resume,
    ])


def holy_guard_common():
    func = os.path.join(DP, "data", "rpg", "function", "holy_guard")
    wf(os.path.join(func, "summon.mcfunction"), [
        "# 随机召一名圣卫（塔卫、重盾、术士三选一），带 rpg.hg。由 add_holy_guards.py 生成。",
        "execute store result score #r rpg_rg_v run random value 0..2",
        "execute if score #r rpg_rg_v matches 0 run return run function rpg:tower_guard/summon",
        "execute if score #r rpg_rg_v matches 1 run return run function rpg:royal_guard/summon",
        "function rpg:end_illager/summon",
    ])
    wf(os.path.join(func, "remove.mcfunction"), ["# 移除一名圣卫（as 载体），三种通用。",
                                                 "execute on passengers run kill @s", "kill @s"])


def main():
    for m, write in ((RG, royal_guard), (EI, end_illager)):
        _, rest = build(m, RP, DP)
        write(rest)
    holy_guard_common()
    print("holy guards: royal_guard %d parts, end_illager %d parts; rpg:holy_guard/summon picks one of three"
          % (len(RG.parts), len(EI.parts)))


if __name__ == "__main__":
    main()
