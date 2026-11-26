# -*- coding: utf-8 -*-
"""达阿特的影子：召唤、每刻、血量、伤害、调度、夺械、切段、结局（docs/DAATH-DESIGN.md §4）。"""
import json
import os

import add_daath_art as art
import daath_spec as S
from daath_lib import *  # noqa: F401,F403
from daath_lib import (B, CENTER, FLOOR, R, DIM, DP, DUST, DUST_D, GUARD, LOOK, ME, NEAR, O, SIL, SLOTS, UNIT, WHITE, anim, at, beam, burst, every, face, fx, light_pillar,
                       line, lines_at, msg, ring, ripple, shards, shock, snd, span, step, title, txt, ui, w, wave, wj)

# 招式编号
SK = {n: i + 1 for i, n in enumerate([
    "chain", "shoot", "guard", "step", "grab", "steal", "drink", "dodge", "lance", "blast", "blade", "bind", "shell", "puppet", "seal",
    "follow", "douse", "swap", "pact", "stun", "reflect", "ten", "ask", "clash", "shatter", "riposte", "arrive"])}
GAP1, GAP2 = 16, 10
# 玩家技能编号 → 影版
ECHO = {"lance": (1, 2, 13), "blast": (3, 11, 15, 22), "blade": (4, 14), "bind": (10, 16), "step": (12, 21), "shell": (5, 6, 7, 17, 18, 19),
        "puppet": (8, 23, 24), "seal": (9, 25, 26, 31, 32, 33, 34, 35, 36)}
ECHO_ID = {n: i + 1 for i, n in enumerate(ECHO)}
BGM = {1: ("rpg:bgm.daath1", 2498), 2: ("rpg:bgm.daath2", 1523)}


def start(name, *lines):
    """开始一招：记编号、归零计时、定住。"""
    return ["scoreboard players set @s rpg_dt_sk %d" % SK[name], "scoreboard players set @s rpg_dt_t 0", "data merge entity @s {NoAI:1b}"] + list(lines)


def bar_text(stage, step):
    return json.dumps({"text": art.bar_text(stage, step), "font": art.FONT}, ensure_ascii=True, separators=(",", ":"))


def build():
    # ------------------------------------------------------------ 召唤
    w("unit/summon", ["# 影子从倒影里站起来（as/at 挑战者）",
                      "execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1,sort=nearest] positioned ~ ~ ~-7 run summon minecraft:vindicator ~ ~ ~ "
                      "{Tags:[\"rpg.el.seen\",\"rpg.dtb\",\"rpg.dtwear\",\"rpg.dt.new\"],Silent:1b,PersistenceRequired:1b,NoAI:1b,Invulnerable:1b,Rotation:[0f,0f],"
                      "active_effects:[{id:\"minecraft:invisibility\",duration:-1,amplifier:0,show_particles:0b}],"
                      "attributes:[{id:\"minecraft:attack_damage\",base:0d},{id:\"minecraft:armor\",base:0d},{id:\"minecraft:follow_range\",base:64d},"
                      "{id:\"minecraft:knockback_resistance\",base:1d},{id:\"minecraft:movement_speed\",base:0.34d}],equipment:{mainhand:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"rpg:empty\"}}},"
                      "drop_chances:{mainhand:0f,offhand:0f}}",
                      "tag @s add rpg.dt.me",
                      "execute as @e[%s,tag=rpg.dt.new,distance=..80,limit=1,sort=nearest] at @s run function %s/unit/init" % (UNIT, B),
                      "tag @s remove rpg.dt.me"])
    zero = ["rpg_dt_sk", "rpg_dt_t", "rpg_dt_cl", "rpg_dt_far", "rpg_dt_still", "rpg_dt_mel", "rpg_dt_melt", "rpg_dt_same", "rpg_dt_ek", "rpg_dt_et", "rpg_dt_eid", "rpg_dt_esm",
            "rpg_dt_ult", "rpg_dt_lit", "rpg_dt_blade", "rpg_dt_sw", "rpg_dt_sa", "rpg_dt_shell", "rpg_dt_tries", "rpg_dt_die", "rpg_dt_dsp", "rpg_dt_orb", "rpg_dt_bgm", "rpg_dt_say"]
    w("unit/init", ["# as/at 影子；挑战者带 rpg.dt.me", "tag @s remove rpg.dt.new",
                    "scoreboard players operation @s %s = %s %s" % (O, ME, O), "scoreboard players operation @s rpg_dt_sid = %s rpg_dt_sid" % ME,
                    "scoreboard players set @s rpg_dt_st 1"] + ["scoreboard players set @s %s 0" % z for z in zero] + [
        "scoreboard players set @s rpg_dt_scd 400", "scoreboard players set @s rpg_dt_gcd 120", "scoreboard players set @s rpg_dt_gap 30",
        "scoreboard players set @s rpg_dt_slot -1",
        "# 每段生命 = 挑战者的近战面板 ×60，900 到 3000；手里不是武器就 1200（虚拟血池，不受原版 1024 上限管）",
        "scoreboard players set @s rpg_dt_mx 1200",
        "execute if items entity %s weapon.mainhand #rpg:daath/weapon store result score @s rpg_dt_mx run attribute %s minecraft:attack_damage get 60" % (ME, ME),
        "execute if score @s rpg_dt_mx matches ..899 run scoreboard players set @s rpg_dt_mx 900",
        "execute if score @s rpg_dt_mx matches 3001.. run scoreboard players set @s rpg_dt_mx 3000",
        "function %s/unit/refill" % B,
        "function %s/dress" % LOOK, "function %s/wear/all" % LOOK, "function %s/look/dark" % LOOK,
        "function %s/weapon/pick" % B] + start("arrive") + [anim("revive"),
        "function %s/bar/open" % B, "function %s/music/1" % B] + line("S01") +
      ["execute if score %s rpg_dt_n matches 1.. run function %s/say_n02" % (ME, B)])
    n2 = [{"text": "〖", "color": "#7C8593", "bold": True, "italic": False}, ui.comp("影", SIL, True), ui.comp("〗", "#7C8593", True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
          ui.comp("这是第 ", ui.BROADCAST_NAME), {"score": {"name": "#n", "objective": O}, "color": WHITE, "bold": True}, ui.comp(" 次。", ui.BROADCAST_NAME)]
    w("say_n02", ["scoreboard players operation #n %s = %s rpg_dt_n" % (O, ME), "scoreboard players add #n %s 1" % O, "tellraw %s %s" % (ME, ui.row(*n2))])
    w("unit/refill", ["# 补满本段：血记在 rpg_dt_h（十分之一点）；载体自己的血永远顶在 1024，只用来量挨了多少",
                      "scoreboard players operation @s rpg_dt_h = @s rpg_dt_mx", "scoreboard players operation @s rpg_dt_h *= #10 %s" % O, "function %s/unit/top" % B])
    w("unit/top", ["attribute @s minecraft:max_health base set 1024", "data modify entity @s Health set value 1024f",
                   "execute unless items entity @s weapon.offhand *[minecraft:death_protection] run item replace entity @s weapon.offhand with %s" % GUARD])

    # ------------------------------------------------------------ 每刻
    w("unit/tick", ["# 影子每刻（as/at 影子）", "tag @s add rpg.dt.it",
                    "tag @p[tag=rpg.dt.in,distance=..90] add rpg.dt.me",
                    "execute if entity %s run function %s/unit/run" % (ME, B),
                    "tag @a remove rpg.dt.me", "tag @e[type=minecraft:vindicator,tag=rpg.dt.it] remove rpg.dt.it"])
    w("unit/run", ["# 有挑战者在场才动",
                   "scoreboard players add @s rpg_dt_orb 1",
                   "execute if entity @s[y=64.4,dy=60,tag=!rpg.dt.hid] run tp @s ~ %d ~" % FLOOR,
                   "execute unless entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..26] run function %s/unit/home" % B,
                   "execute if entity @s[tag=rpg.dt.end] run return run function %s/end/tick" % B,
                   "function %s/unit/light" % B,
                   "function %s/unit/hp" % B,
                   "function %s/music/tick" % B,
                   "execute if score %s rpg_dt_ph matches 4.. run return run function %s/unit/idle" % (ME, B),
                   "execute if entity @s[tag=rpg.dt.morph] run return run function %s/morph/tick" % B,
                   "execute if entity @s[tag=rpg.dt.desp] run return run function %s/despair/tick" % B,
                   "execute if score @s rpg_dt_h matches ..15 if score @s rpg_dt_st matches 1 run return run function %s/stage/end1" % B,
                   "execute if score @s rpg_dt_h matches ..15 if score @s rpg_dt_st matches 2 run return run function %s/stage/end2" % B,
                   "function %s/mind/watch" % B,
                   "function %s/steal/clock" % B,
                   "execute if score @s rpg_dt_blade matches 1.. run function %s/unit/blade" % B,
                   "execute if score @s rpg_dt_sk matches 1.. run return run function %s/sk/tick" % B,
                   "function %s/schedule" % B])
    w("unit/room", [face(), "execute facing entity %s feet rotated ~ 0 positioned ^ ^ ^-0.2 if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..%d] run tp @s ~ ~ ~" % (ME, R - 1)])
    w("unit/idle", ["data merge entity @s {NoAI:1b}", face()])
    w("unit/home", ["# 掉出场地：回到中心", "execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..140,limit=1,sort=nearest] run tp @s ~ ~ ~"])
    w("unit/blade", ["scoreboard players remove @s rpg_dt_blade 1", "execute on passengers if entity @s[tag=rpg.dtm.p.weapon_r] run particle minecraft:smoke ~ ~ ~ 0.2 0.3 0.2 0.01 1",
                     "particle %s ^-0.4 ^1.1 ^0.6 0.2 0.3 0.2 0 1" % DUST_D])
    # 光：在灯下 = 显形
    w("unit/light", ["# 灯下显形（as/at 影子）",
                     "execute if entity @s[tag=!rpg.dt.lit] if entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..6.2] run function %s/unit/lit_on" % B,
                     "execute if entity @s[tag=rpg.dt.lit] unless entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..6.6] run function %s/unit/lit_off" % B,
                     "execute if entity @s[tag=rpg.dt.lit] run particle minecraft:end_rod ~ ~1 ~ 0.35 0.7 0.35 0.01 1",
                     "execute if score @s rpg_dt_st matches 1 if entity @s[tag=!rpg.dt.lit] run particle %s ~ ~0.9 ~ 0.35 0.6 0.35 0.01 1" % "minecraft:smoke",
                     "execute if score @s rpg_dt_sw matches 1.. run particle %s ^-0.4 ^1.2 ^0.5 0.15 0.2 0.15 0 1" % DUST,
                     "execute if score @s rpg_dt_sa matches 1.. run particle minecraft:wax_off ~ ~1 ~ 0.4 0.6 0.4 0 1"])
    w("unit/lit_on", ["tag @s add rpg.dt.lit", "function %s/look/lit" % LOOK] + burst(size=2.0, color=WHITE) + [
        snd("block.amethyst_block.resonate", 1.2, 1.4), snd("block.sculk_shrieker.shriek", 0.4, 1.8), "particle minecraft:flash{color:16774826} ~ ~1.2 ~ 0 0 0 0 1"])
    w("unit/lit_off", ["tag @s remove rpg.dt.lit", "execute if score @s rpg_dt_st matches 1 run function %s/look/dark" % LOOK, snd("block.candle.extinguish", 0.8, 0.6)])

    # ------------------------------------------------------------ 血量：每 2 刻读一次，按状态折算
    w("unit/hp", ["# 读血与折算（十分之一点）", "scoreboard players operation #m %s = @s rpg_dt_orb" % O, "scoreboard players set #k %s 2" % O, "scoreboard players operation #m %s %%= #k %s" % (O, O),
                  "execute unless score #m %s matches 0 run return 0" % O,
                  "execute store result score #h %s run data get entity @s Health 10" % O,
                  "scoreboard players set #d %s 10240" % O, "scoreboard players operation #d %s -= #h %s" % (O, O),
                  "execute unless score #d %s matches 1.. run return run function %s/bar/set" % (O, B),
                  "function %s/unit/top" % B, "function %s/unit/struck" % B, "function %s/bar/set" % B])
    w("unit/struck", ["# 挨了一下：#d 是原始伤害（十分之一点）。每下最多按本段生命的 1.2% 算，再按明暗、夺甲折算",
                      "execute if entity @s[tag=rpg.dt.morph] run return 0", "execute if entity @s[tag=rpg.dt.desp] run return 0",
                      "scoreboard players operation #cap %s = @s rpg_dt_mx" % O, "scoreboard players operation #cap %s *= #12 %s" % (O, O), "scoreboard players operation #cap %s /= #100 %s" % (O, O),
                      "execute if score #d %s > #cap %s run scoreboard players operation #d %s = #cap %s" % (O, O, O, O),
                      "execute if entity @s[tag=rpg.dt.seek] run tag @s add rpg.dt.found",
                      "execute if entity @s[tag=rpg.dt.window] run function %s/clash/win" % B,
                      "execute if score @s rpg_dt_shell matches 1.. run return run function %s/shell/hit" % B,
                      "scoreboard players set #pc %s 100" % O,
                      "execute if entity @s[tag=!rpg.dt.lit] if score @s rpg_dt_st matches 1 run scoreboard players set #pc %s 60" % O,
                      "execute if entity @s[tag=!rpg.dt.lit] if score @s rpg_dt_st matches 2 run scoreboard players set #pc %s 75" % O,
                      "execute if entity @s[tag=rpg.dt.lit] run scoreboard players set #pc %s 150" % O,
                      "execute if score @s rpg_dt_sk matches %d run scoreboard players set #pc %s 150" % (SK["stun"], O),
                      "# 夺了盔甲：受到的伤害 −20%", "execute if score @s rpg_dt_sa matches 1.. run scoreboard players operation #pc %s *= #8 %s" % (O, O),
                      "execute if score @s rpg_dt_sa matches 1.. run scoreboard players operation #pc %s /= #10 %s" % (O, O),
                      "# 同一招用太多：减半", "execute if entity @s[tag=rpg.dt.loop] run scoreboard players set #k %s 2" % O,
                      "execute if entity @s[tag=rpg.dt.loop] run scoreboard players operation #pc %s /= #k %s" % (O, O),
                      "execute if score @s rpg_dt_sk matches %d if entity %s run function %s/guard/struck" % (SK["guard"], ME, B),
                      "scoreboard players operation #e %s = #d %s" % (O, O), "scoreboard players operation #e %s *= #pc %s" % (O, O), "scoreboard players operation #e %s /= #100 %s" % (O, O),
                      "scoreboard players operation @s rpg_dt_h -= #e %s" % O,
                      "execute if score @s rpg_dt_h matches ..10 run scoreboard players set @s rpg_dt_h 10",
                      "# 计数：近战第几下、是不是一直同一格武器",
                      "execute if entity @a[tag=rpg.dt.me,distance=..5.5] run function %s/mind/melee" % B,
                      "execute if entity @s[tag=rpg.dt.lit] if score #d %s matches 10.. run function %s/steal/pry" % (O, B),
                      snd("block.glass.hit", 0.5, 0.8, 24), "particle %s ~ ~1.1 ~ 0.25 0.4 0.25 0 4" % DUST,
                      "execute if entity @s[tag=rpg.dt.drk] run function %s/drink/hit" % B])

    # ------------------------------------------------------------ 打挑战者：#pc = 最大生命的百分之几（as 挑战者）
    w("hurt/me", ["# 影子打中挑战者（as 挑战者；#pc 百分比）：最大生命 ×#pc%，会死就不扣、判负",
                  "execute unless score @s rpg_dt_ph matches 3 run return 0",
                  "execute store result score #a %s run attribute @s minecraft:max_health get 10" % O,
                  "scoreboard players operation #a %s *= #pc %s" % (O, O),
                  "execute if entity @e[type=minecraft:vindicator,tag=rpg.dt.it,scores={rpg_dt_sw=1..}] run scoreboard players operation #a %s *= #12 %s" % (O, O),
                  "execute if entity @e[type=minecraft:vindicator,tag=rpg.dt.it,scores={rpg_dt_sw=1..}] run scoreboard players operation #a %s /= #10 %s" % (O, O),
                  "execute if entity @e[type=minecraft:vindicator,tag=rpg.dt.it,scores={rpg_dt_blade=1..}] run scoreboard players operation #a %s *= #13 %s" % (O, O),
                  "execute if entity @e[type=minecraft:vindicator,tag=rpg.dt.it,scores={rpg_dt_blade=1..}] run scoreboard players operation #a %s /= #10 %s" % (O, O),
                  "scoreboard players operation #a %s /= #100 %s" % (O, O),
                  "execute store result score #hp %s run data get entity @s Health 10" % O,
                  "execute store result score #ab %s run data get entity @s AbsorptionAmount 10" % O,
                  "scoreboard players operation #hp %s += #ab %s" % (O, O),
                  "execute if score #a %s >= #hp %s run return run function %s/hurt/fail" % (O, O, B),
                  "execute store result storage rpg:daath t.d double 0.1 run scoreboard players get #a %s" % O,
                  "function %s/hurt/m with storage rpg:daath t" % B])
    w("hurt/m", ["$damage @s $(d) rpg:daath by @e[type=minecraft:vindicator,tag=rpg.dt.it,limit=1]"])
    w("hurt/fail", ["# 判负：不会真的死（as 挑战者）", "scoreboard players set @s rpg_dt_ph 5", "scoreboard players set @s rpg_dt_pt 0",
                    "execute as @e[type=minecraft:vindicator,tag=rpg.dt.it,limit=1] at @s run function %s/hurt/fail_it" % B])
    w("hurt/fail_it", ["function %s/sk/end" % B, "data merge entity @s {NoAI:1b,Invulnerable:1b}", anim("hero"),
                       "execute at %s run tp @s ^ ^ ^1.2 facing entity %s feet" % (ME, ME)] + line("S21") + [snd("block.conduit.deactivate", 1, 0.5)])
    w("hurt/all", ["# 打中带 rpg.dt.hit 的挑战者：#pc 由调用者设", "execute as @a[tag=rpg.dt.hit] at @s run function %s/hurt/me" % B, "tag @a remove rpg.dt.hit"])

    # ------------------------------------------------------------ 记住你：眼睛
    w("mind/watch", ["# 每刻记：远近、站着不动、刚放的技能、刚喝的药（as/at 影子）",
                     "execute if entity @a[tag=rpg.dt.me,distance=..8] run scoreboard players set @s rpg_dt_far 0",
                     "execute unless entity @a[tag=rpg.dt.me,distance=..8] run scoreboard players add @s rpg_dt_far 1",
                     "execute if score @s rpg_dt_melt matches 1.. run scoreboard players remove @s rpg_dt_melt 1",
                     "execute if score @s rpg_dt_melt matches 0 run scoreboard players set @s rpg_dt_mel 0",
                     "execute if score @s rpg_dt_scd matches 1.. run scoreboard players remove @s rpg_dt_scd 1",
                     "execute if score @s rpg_dt_gcd matches 1.. run scoreboard players remove @s rpg_dt_gcd 1",
                     "execute if score @s rpg_dt_et matches 1.. run scoreboard players remove @s rpg_dt_et 1",
                     "execute if score %s rpg_dt_cast matches 1.. run function %s/mind/cast" % (ME, B),
                     "execute if score %s rpg_dt_drk matches 1.. run function %s/mind/drank" % (ME, B)] + every(10, "rpg_dt_orb") + [
        "execute if score #m %s matches 0 run function %s/mind/still" % (O, B)])
    w("mind/still", ["execute store result score #x %s run data get entity %s Pos[0] 4" % (O, ME), "execute store result score #z %s run data get entity %s Pos[2] 4" % (O, ME),
                     "execute if score #x %s = @s rpg_dt_px if score #z %s = @s rpg_dt_pz run scoreboard players add @s rpg_dt_still 10" % (O, O),
                     "execute unless score #x %s = @s rpg_dt_px run scoreboard players set @s rpg_dt_still 0" % O,
                     "execute unless score #z %s = @s rpg_dt_pz run scoreboard players set @s rpg_dt_still 0" % O,
                     "scoreboard players operation @s rpg_dt_px = #x %s" % O, "scoreboard players operation @s rpg_dt_pz = #z %s" % O])
    w("mind/melee", ["scoreboard players add @s rpg_dt_mel 1", "scoreboard players set @s rpg_dt_melt 70",
                     "execute store result score #s %s run data get entity %s SelectedItemSlot" % (O, ME),
                     "execute if score #s %s = @s rpg_dt_slot run scoreboard players add @s rpg_dt_same 1" % O,
                     "execute unless score #s %s = @s rpg_dt_slot run function %s/mind/fresh" % (O, B),
                     "scoreboard players operation @s rpg_dt_slot = #s %s" % O,
                     "execute if score @s rpg_dt_same matches 22.. if entity @s[tag=!rpg.dt.loop] run function %s/mind/loop" % B])
    w("mind/fresh", ["# 换招了", "scoreboard players set @s rpg_dt_same 0", "execute if entity @s[tag=rpg.dt.loop] run function %s/mind/unloop" % B])
    w("mind/loop_say", ["# 这句半分钟最多说一次", "scoreboard players operation @s rpg_dt_say = @s rpg_dt_orb", "scoreboard players add @s rpg_dt_say 600"] + line("S04"))
    w("mind/loop", ["tag @s add rpg.dt.loop", "execute unless score @s rpg_dt_say > @s rpg_dt_orb run function %s/mind/loop_say" % B] + ["function %s/eye/loop" % B, snd("block.beacon.deactivate", 0.8, 0.7)])
    w("mind/unloop", ["tag @s remove rpg.dt.loop", "function %s/eye/off" % B, snd("block.glass.break", 0.8, 1.2)])
    echo = ["# 挑战者放了技能（#e 编号）：两秒半后还一记影版", "scoreboard players operation #e %s = %s rpg_dt_cast" % (O, ME), "scoreboard players set %s rpg_dt_cast 0" % ME,
            "execute if score #e %s = @s rpg_dt_eid run scoreboard players add @s rpg_dt_esm 1" % O,
            "execute unless score #e %s = @s rpg_dt_eid run scoreboard players set @s rpg_dt_esm 1" % O,
            "execute unless score #e %s = @s rpg_dt_eid run function %s/mind/fresh" % (O, B),
            "scoreboard players operation @s rpg_dt_eid = #e %s" % O,
            "execute if score @s rpg_dt_esm matches 3.. if entity @s[tag=!rpg.dt.loop] run function %s/mind/loop" % B,
            "execute if score @s rpg_dt_ek matches 1.. run return 0"]
    for n, ids in ECHO.items():
        for k in ids:
            echo.append("execute if score #e %s matches %d run scoreboard players set @s rpg_dt_ek %d" % (O, k, ECHO_ID[n]))
    echo += ["execute if score @s rpg_dt_ek matches 1.. run scoreboard players set @s rpg_dt_et 50",
             "execute if score @s rpg_dt_ek matches 1.. run function %s/eye/skill" % B]
    w("mind/cast", echo)
    w("mind/drank", ["scoreboard players set %s rpg_dt_drk 0" % ME, "tag @s add rpg.dt.want_drink", "function %s/eye/bottle" % B])
    # 眼睛：头顶的位图字（Codex 的图来了以后换成 rpg:daath_vfx）
    for name, glyph, col in (("blade", "⚔", WHITE), ("step", "»", WHITE), ("bottle", "⚗", WHITE), ("shield", "⛨", WHITE), ("loop", "↻", "#FF5A62"), ("skill", "✦", "#FFF2A8"), ("hand", "✋", "#FFF2A8")):
        w("eye/" + name, ["kill @e[type=minecraft:text_display,tag=rpg.dt.eye,distance=..6]",
                          "summon minecraft:text_display ~ ~2.75 ~ {Tags:[\"rpg.dt.fx\",\"rpg.dt.eye\",\"rpg.dt.eyenew\"],text:%s,background:0,billboard:\"center\",see_through:0b,"
                          "brightness:{sky:15,block:15},teleport_duration:2,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.6f,2.6f,2.6f],right_rotation:[0f,0f,0f,1f]}}"
                          % ui.row(ui.comp(art.mark(name), col) if art.mark(name) is None else dict(text=art.mark(name), font=art.VFX_FONT, color="#FFFFFF")) if art.mark(name) else
                          "summon minecraft:text_display ~ ~2.75 ~ {Tags:[\"rpg.dt.fx\",\"rpg.dt.eye\",\"rpg.dt.eyenew\"],text:%s,background:0,billboard:\"center\","
                          "brightness:{sky:15,block:15},teleport_duration:2,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.6f,2.6f,2.6f],right_rotation:[0f,0f,0f,1f]}}" % ui.row(ui.comp(glyph, col, True)),
                          "scoreboard players set @e[type=minecraft:text_display,tag=rpg.dt.eyenew] rpg_dt_life %d" % (100000 if name == "loop" else 60),
                          "scoreboard players set @e[type=minecraft:text_display,tag=rpg.dt.eyenew] rpg_dt_kd 0",
                          "tag @e[type=minecraft:text_display,tag=rpg.dt.eyenew] remove rpg.dt.eyenew",
                          snd("block.sculk_sensor.clicking", 0.8, 0.8, 24)] +
          seq("eye", 1.9, "~ ~2.75 ~") +
          (["execute unless entity @s[tag=rpg.dt.told] run function %s/eye/told" % B] if name != "loop" else []))
    w("eye/told", ["tag @s add rpg.dt.told"] + line("S03"))
    w("eye/off", ["kill @e[type=minecraft:text_display,tag=rpg.dt.eye,distance=..6]"])
    w("eye/follow", ["execute positioned ~ ~2.75 ~ run tp @e[type=minecraft:text_display,tag=rpg.dt.eye,distance=..8] ~ ~ ~"])

    # ------------------------------------------------------------ 调度
    w("schedule", ["# 空着手：走近，等间隔，选下一招（as/at 影子）",
                   "function %s/eye/follow" % B,
                   "scoreboard players remove @s rpg_dt_gap 1",
                   "# 贴得太近就停住、退半步",
                   "execute if entity @a[tag=rpg.dt.me,distance=..1.5] run function %s/unit/room" % B,
                   "execute if score @s rpg_dt_gap matches 1.. if entity @a[tag=rpg.dt.me,distance=..1.9] run return run data merge entity @s {NoAI:1b}",
                   "execute if score @s rpg_dt_gap matches 1.. run return run data merge entity @s {NoAI:0b}",
                   "execute if score @s rpg_dt_st matches 1 run scoreboard players set @s rpg_dt_gap %d" % GAP1,
                   "execute if score @s rpg_dt_st matches 2 run scoreboard players set @s rpg_dt_gap %d" % GAP2,
                   "function %s/pick" % B])
    pick = ["# 选招：大招血线 → 影版技能 → 它记住的事 → 夺械 → 连招", face()]
    for st, ths in ((1, (650, 350)), (2, (700, 400, 200))):
        for i, th in enumerate(ths, 1):
            pick.append("execute if score @s rpg_dt_st matches %d if score @s rpg_dt_bar matches ..%d unless entity @s[tag=rpg.dt.u%d] run return run function %s/ult/%d_%d" % (st, th // 50, i, B, st, i))
    pick += ["execute if score @s rpg_dt_ek matches 1.. if score @s rpg_dt_et matches 0 run return run function %s/echo/cast" % B,
             "execute if entity @s[tag=rpg.dt.want_drink] run return run function %s/skill/drink" % B,
             "execute if score @s rpg_dt_far matches 80.. run return run function %s/skill/step" % B,
             "execute if score @s rpg_dt_still matches 60.. if entity @a[tag=rpg.dt.me,distance=..9] run return run function %s/skill/grab" % B,
             "execute if score @s rpg_dt_mel matches 5.. if score @s rpg_dt_gcd matches 0 run return run function %s/skill/guard" % B,
             "execute if score @s rpg_dt_scd matches 0 if entity @a[tag=rpg.dt.me,distance=..9] run return run function %s/skill/steal" % B,
             "execute store result score #r %s run random value 1..100" % O,
             "execute if score @s rpg_dt_st matches 1 if score #r %s matches 1..14 run return run function %s/skill/dodge" % (O, B)]
    for i, n in enumerate(("follow", "douse", "swap", "pact")):
        cond = " if entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..40]" if n == "douse" else ""
        pick.append("execute if score @s rpg_dt_st matches 2 if score #r %s matches %d..%d%s run return run function %s/skill/%s" % (O, 1 + i * 12, 12 + i * 12, cond, B, n))
    pick += ["function %s/skill/chain" % B]
    w("pick", pick)
    w("sk/tick", ["scoreboard players add @s rpg_dt_t 1", "function %s/eye/follow" % B] +
      ["execute if score @s rpg_dt_sk matches %d run return run function %s/sk/%s" % (i, B, n) for n, i in SK.items()])
    w("sk/end", ["# 一招结束", "scoreboard players set @s rpg_dt_sk 0", "scoreboard players set @s rpg_dt_t 0", "tag @s remove rpg.dt.drk", "tag @s remove rpg.dt.hid",
                 "data merge entity @s {NoAI:0b,NoGravity:0b,Invulnerable:0b}", "tag @a remove rpg.dt.hit"])
    w("sk/arrive", [span(1, 40, "particle %s ~ ~0.1 ~ 0.7 0.05 0.7 0 8" % DUST_D), at(6, snd("entity.generic.splash", 1, 0.5)), at(50, anim("hero"))] +
      ["execute if score @s rpg_dt_t matches 60.. run data merge entity @s {Invulnerable:0b}", "execute if score @s rpg_dt_t matches 64.. run function %s/sk/end" % B])
    w("sk/stun", ["# 眩晕：#rpg_dt_gcd 借来记多久", span(1, 400, "particle minecraft:crit ~ ~2.1 ~ 0.3 0.1 0.3 0.1 1"),
                  "scoreboard players remove @s rpg_dt_i 1", "execute if score @s rpg_dt_i matches ..0 run function %s/sk/end" % B])
    w("stun", ["# 眩晕（#s 刻）：夺走的东西立刻掉还", "scoreboard players operation @s rpg_dt_i = #s %s" % O] + start("stun") + [
        anim("stun"), "execute if score @s rpg_dt_sw matches 1.. run function %s/steal/lose_w" % B, "execute if score @s rpg_dt_sa matches 1.. run function %s/steal/lose_a" % B,
        snd("block.glass.break", 1.2, 0.6), snd("entity.zombie.attack_iron_door", 0.6, 0.6)] + shards(8))

    # ------------------------------------------------------------ 武器：从整个背包里抽
    w("weapon/pick", ["# 抽一把武器拿在手里，#c 类别记进 rpg_dt_wc（as 影子）",
                      "execute if score @s rpg_dt_sw matches 1.. run return run function %s/weapon/stolen" % B,
                      "execute store result storage rpg:daath t.n int 1 run scoreboard players get @s %s" % O,
                      "function %s/weapon/len with storage rpg:daath t" % B,
                      "execute if score #len %s matches ..0 run return run function %s/weapon/none" % (O, B),
                      "scoreboard players remove #len %s 1" % O,
                      "execute store result storage rpg:daath t.max int 1 run scoreboard players get #len %s" % O,
                      "function %s/weapon/roll with storage rpg:daath t" % B,
                      "function %s/weapon/take with storage rpg:daath t" % B,
                      "function %s/weapon/hold" % B])
    w("weapon/len", ["$execute store result score #len %s run data get storage rpg:daath s$(n).arms" % O])
    w("weapon/roll", ["$execute store result storage rpg:daath t.i int 1 run random value 0..$(max)"])
    w("weapon/take", ["$data modify storage rpg:daath t.cur set from storage rpg:daath s$(n).arms[$(i)]"])
    w("weapon/stolen", ["# 夺来的那把：之后只用它", "execute store result storage rpg:daath t.id int 1 run scoreboard players get %s rpg_fg_id" % ME,
                        "function %s/weapon/stolen_m with storage rpg:daath t" % B, "function %s/weapon/hold" % B])
    w("weapon/stolen_m", ["$data modify storage rpg:daath t.cur set from storage rpg:daath st.p$(id).w"])
    w("weapon/none", ["scoreboard players set @s rpg_dt_wc 0", "execute on passengers if entity @s[tag=rpg.dtm.p.weapon_r] run data remove entity @s item",
                      "execute on passengers if entity @s[tag=rpg.dtm.p.weapon_l] run data remove entity @s item"])
    w("weapon/hold", ["execute store result score @s rpg_dt_wc run data get storage rpg:daath t.cur.c",
                      "execute on passengers if entity @s[tag=rpg.dtm.p.weapon_r] run data modify entity @s item set from storage rpg:daath t.cur.item",
                      "execute if score @s rpg_dt_wc matches 6 on passengers if entity @s[tag=rpg.dtm.p.weapon_l] run data modify entity @s item set from storage rpg:daath t.cur.item",
                      "execute unless score @s rpg_dt_wc matches 6 on passengers if entity @s[tag=rpg.dtm.p.weapon_l] run data remove entity @s item",
                      "particle minecraft:smoke ^-0.4 ^1.1 ^0.4 0.1 0.2 0.1 0.01 4"])

    # ------------------------------------------------------------ 夺械
    w("steal/clock", ["# 夺走的东西 40 秒后自己还", "execute if score @s rpg_dt_sw matches 1.. run scoreboard players remove @s rpg_dt_sw 1",
                      "execute if score @s rpg_dt_sw matches 1 run function %s/steal/lose_w" % B,
                      "execute if score @s rpg_dt_sa matches 1.. run scoreboard players remove @s rpg_dt_sa 1",
                      "execute if score @s rpg_dt_sa matches 1 run function %s/steal/lose_a" % B])
    w("steal/pry", ["# 灯下打中它：四下还一件", "execute if score @s rpg_dt_sw matches ..0 if score @s rpg_dt_sa matches ..0 run return 0",
                    "scoreboard players add @s rpg_dt_sp 1", "particle minecraft:crit ~ ~1.3 ~ 0.3 0.3 0.3 0.3 8",
                    "execute if score @s rpg_dt_sp matches 4.. if score @s rpg_dt_sw matches 1.. run return run function %s/steal/lose_w" % B,
                    "execute if score @s rpg_dt_sp matches 4.. if score @s rpg_dt_sa matches 1.. run function %s/steal/lose_a" % B])
    for k, zh, sc_ in (("w", "武器", "rpg_dt_sw"), ("a", "盔甲", "rpg_dt_sa")):
        w("steal/lose_%s" % k, ["# 还%s（as/at 影子）" % zh, "scoreboard players set @s %s 0" % sc_, "scoreboard players set @s rpg_dt_sp 0",
                                "execute as %s run function %s/steal/give_one_%s" % (ME, B, k)] + line("S23", 2) + burst("~ ~1.2 ~", 1.8, "#FFF2A8") + [
            snd("item.armor.equip_chain", 1.2, 1.2), snd("block.amethyst_block.chime", 1, 1.2)] +
          (["function %s/weapon/pick" % B] if k == "w" else ["function %s/wear/all" % LOOK, "execute if entity @s[tag=!rpg.dt.lit] if score @s rpg_dt_st matches 1 run function %s/look/dark" % LOOK]))
        w("steal/give_one_%s" % k, ["execute store result storage rpg:daath t.id int 1 run scoreboard players get @s rpg_fg_id", "function %s/steal/give_%s with storage rpg:daath t" % (B, k),
                                    msg([txt("%s回到你手里。" % zh, SIL)])])
    w("steal/take", ["# 夺到了（as/at 影子；挑战者 rpg.dt.me）：先夺武器，武器已夺或空手就夺盔甲",
                     "execute store result storage rpg:daath t.id int 1 run scoreboard players get %s rpg_fg_id" % ME,
                     "execute if score @s rpg_dt_sw matches ..0 if items entity %s weapon.mainhand #rpg:daath/weapon run return run function %s/steal/take_w" % (ME, B),
                     "execute if score @s rpg_dt_sa matches ..0 run function %s/steal/take_a" % B])
    w("steal/take_w", ["scoreboard players set @s rpg_dt_sw 800", "scoreboard players set @s rpg_dt_sp 0",
                       "execute store result score #s %s run data get entity %s SelectedItemSlot" % (O, ME),
                       "execute store result storage rpg:daath t.hs int 1 run scoreboard players get #s %s" % O,
                       "execute as %s at @s run function %s/snap/all_one" % (ME, B),
                       "function %s/steal/store_w with storage rpg:daath t" % B,
                       "item replace entity %s weapon.mainhand with minecraft:air" % ME, "scoreboard players set %s rpg_dt_got 1" % ME,
                       "function %s/weapon/stolen" % B] + line("S22") + [msg([txt("它夺走了你的武器：伤害 +20%。灯下打中它四下，或让它眩晕，就能拿回来。", "#FF5A62")], ME),
                                                                             snd("rpg:daath.execute", 1.2, 0.9), snd("entity.item.break", 1, 0.6)])
    w("snap/all_one", ["# 主手那把存进 t.e（as/at 挑战者）", "summon minecraft:item_display ~ ~ ~ {Tags:[\"rpg.dt.tmp\"]}",
                       "data modify storage rpg:daath t.keep set from storage rpg:daath t.n", "data modify storage rpg:daath t.n set value 0", "data modify storage rpg:daath s0.arms set value []",
                       "function %s/snap/one {s:\"weapon.mainhand\"}" % B, "kill @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4]"])
    w("steal/store_w", ["$data modify storage rpg:daath st.p$(id).w set from storage rpg:daath t.e", "$data modify storage rpg:daath st.p$(id).w.slot set value \"hotbar.$(hs)\""])
    ta = ["# 夺一件盔甲：有哪件抽哪件", "scoreboard players set #r %s 0" % O, "execute store result score #o %s run random value 0..3" % O, "scoreboard players set #f %s 0" % O]
    sl = [("chest", "armor.chest"), ("head", "armor.head"), ("legs", "armor.legs"), ("feet", "armor.feet")]
    for rot in range(4):
        for k in range(4):
            nm, slot = sl[(rot + k) % 4]
            ta.append("execute if score #o %s matches %d if score #f %s matches 0 if items entity %s %s * run function %s/steal/take_%s" % (O, rot, O, ME, slot, B, nm))
    w("steal/take_a", ta)
    for nm, slot in sl:
        w("steal/take_%s" % nm, ["scoreboard players set #f %s 1" % O, "scoreboard players set @s rpg_dt_sa 800", "scoreboard players set @s rpg_dt_sp 0",
                                 "execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:[\"rpg.dt.ret\"]}",
                                 "item replace entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] contents from entity %s %s" % (ME, slot),
                                 "data modify storage rpg:daath t.e set value {slot:\"%s\"}" % slot,
                                 "data modify storage rpg:daath t.e.item set from entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] item",
                                 "kill @e[type=minecraft:item_display,tag=rpg.dt.ret]", "function %s/steal/store_a with storage rpg:daath t" % B,
                                 "item replace entity %s %s with minecraft:air" % (ME, slot), "scoreboard players set %s rpg_dt_got 1" % ME,
                                 "execute on passengers if entity @s[tag=rpg.dtm.s.%s] run data merge entity @s {brightness:{block:15,sky:15}}" % nm] + line("S22") + [
            msg([txt("它夺走了你的盔甲：受到的伤害 −20%。灯下打中它四下，或让它眩晕，就能拿回来。", "#FF5A62")], ME), snd("rpg:daath.execute", 1.2, 0.8), snd("item.armor.equip_netherite", 1, 0.6)])
    w("steal/store_a", ["$data modify storage rpg:daath st.p$(id).a set from storage rpg:daath t.e"])

    # ------------------------------------------------------------ 血条
    open_ = ["# as 影子"]
    for n in range(1, SLOTS + 1):
        open_.append("execute if score @s %s matches %d run bossbar set rpg:daath_%d visible true" % (O, n, n))
        open_.append("execute if score @s %s matches %d run bossbar set rpg:daath_%d players %s" % (O, n, n, ME))
        open_.append("execute if score @s %s matches %d run bossbar set rpg:daath_%d max 20" % (O, n, n))
    w("bar/open", open_ + ["scoreboard players set @s rpg_dt_bar -1", "function %s/bar/set" % B])
    w("bar/set", ["# 档位：每段 20 档", "scoreboard players operation #s %s = @s rpg_dt_h" % O, "scoreboard players operation #k %s = @s rpg_dt_mx" % O,
                  "scoreboard players set #20 %s 20" % O, "scoreboard players operation #s %s *= #20 %s" % (O, O), "scoreboard players operation #k %s *= #10 %s" % (O, O),
                  "scoreboard players operation #j %s = #k %s" % (O, O), "scoreboard players remove #j %s 1" % O, "scoreboard players operation #s %s += #j %s" % (O, O),
                  "scoreboard players operation #s %s /= #k %s" % (O, O),
                  "execute if score #s %s matches 21.. run scoreboard players set #s %s 20" % (O, O), "execute if score #s %s matches ..0 run scoreboard players set #s %s 0" % (O, O),
                  "execute if score #s %s = @s rpg_dt_bar run return 0" % O, "scoreboard players operation @s rpg_dt_bar = #s %s" % O,
                  "execute store result storage rpg:daath t.n int 1 run scoreboard players get @s %s" % O, "execute store result storage rpg:daath t.v int 1 run scoreboard players get #s %s" % O,
                  "execute store result storage rpg:daath t.st int 1 run scoreboard players get @s rpg_dt_st", "function %s/bar/m with storage rpg:daath t" % B])
    w("bar/m", ["$bossbar set rpg:daath_$(n) value $(v)", "$data modify storage rpg:daath t.tx set from storage rpg:daath_bar b$(st)_$(v)", "function %s/bar/m2 with storage rpg:daath t" % B])
    w("bar/m2", ["$bossbar set rpg:daath_$(n) name {\"text\":\"$(tx)\",\"font\":\"%s\"}" % art.FONT])
    w("bar/load", ["data modify storage rpg:daath_bar b%d_%d set value \"%s\"" % (st, k, art.bar_text(st, k)) for st in (1, 2) for k in range(21)])

    # ------------------------------------------------------------ 音乐
    for st, (ev, ln) in BGM.items():
        w("music/%d" % st, ["stopsound %s record" % ME, "execute as %s at @s run playsound %s record @s ~ ~ ~ 1 1 1" % (ME, ev), "scoreboard players set @s rpg_dt_bgm %d" % ln])
    w("music/tick", ["execute if entity @s[tag=rpg.dt.mute] run return 0", "scoreboard players remove @s rpg_dt_bgm 1", "execute if score @s rpg_dt_bgm matches 1.. run return 0",
                     "execute if score @s rpg_dt_st matches 1 run function %s/music/1" % B, "execute if score @s rpg_dt_st matches 2 run function %s/music/2" % B])

    # ------------------------------------------------------------ 一段打空：面具
    w("stage/end1", ["# 一段打空：跪下，面具裂开（as/at 影子）", "function %s/sk/end" % B, "function %s/unit/refill" % B, "tag @s add rpg.dt.morph", "scoreboard players set @s rpg_dt_t 0",
                     "data merge entity @s {NoAI:1b,Invulnerable:1b}", "execute if score @s rpg_dt_sw matches 1.. run function %s/steal/lose_w" % B, "execute if score @s rpg_dt_sa matches 1.. run function %s/steal/lose_a" % B,
                     "function %s/eye/off" % B, "kill @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=..60]", "tag @s remove rpg.dt.loop", "function %s/lamp/all_out" % B, anim("kneel"), face(), snd("block.glass.break", 1.4, 0.5)])
    m = ["scoreboard players add @s rpg_dt_t 1"] + lines_at(20, "S08")
    for t in range(30, 100, 10):
        m.append(at(t, "function %s/morph/flake" % B))
    m += [at(60, "execute on passengers if entity @s[tag=rpg.dtm.s.feet] run data merge entity @s {brightness:{block:15,sky:15}}"),
          at(60, "execute on passengers if entity @s[tag=rpg.dtm.s.legs] run data merge entity @s {brightness:{block:15,sky:15}}"),
          at(78, "execute on passengers if entity @s[tag=rpg.dtm.s.chest] run data merge entity @s {brightness:{block:15,sky:15}}"),
          at(92, "execute on passengers if entity @s[tag=rpg.dtm.s.head] run data merge entity @s {brightness:{block:15,sky:15}}"),
          at(100, "function %s/face/on" % LOOK), at(100, "function %s/look/lit" % LOOK), at(100, "function %s/morph/crack" % B)] + lines_at(112, "S09", 2) + [
        at(112, anim("hero")), "execute if score @s rpg_dt_t matches 140.. run function %s/stage/begin2" % B]
    w("morph/tick", m)
    w("morph/flake", shards(6, 0.6, 0.5) + [snd("block.glass.step", 1, 0.7), "particle %s ~ ~1 ~ 0.4 0.7 0.4 0 12" % DUST_D])
    w("morph/crack", burst("~ ~1.6 ~", 3.6, WHITE) + shards(14, 1.5, 0.4) + dec("crack_mirror", 6, life=60) + light_pillar(WHITE) + [
        "particle minecraft:flash{color:16777215} ~ ~1.6 ~ 0 0 0 0 1 force", snd("block.glass.break", 2, 0.7), snd("rpg:daath.splinter", 1.6, 0.9), "effect give %s minecraft:blindness 1 0 true" % ME])
    w("stage/begin2", ["tag @s remove rpg.dt.morph", "tag @s remove rpg.dt.u1", "tag @s remove rpg.dt.u2", "tag @s remove rpg.dt.u3", "scoreboard players set @s rpg_dt_st 2",
                       "scoreboard players set @s rpg_dt_bar -1", "function %s/unit/refill" % B, "function %s/bar/set" % B, "function %s/music/2" % B, "scoreboard players set @s rpg_dt_gap 20",
                       "scoreboard players set @s rpg_dt_scd 200", "attribute @s minecraft:movement_speed base set 0.39", "function %s/sk/end" % B,
                       "function %s/say_deaths" % B] + ["title %s times 5 35 12" % ME, "title %s subtitle %s" % (ME, ui.row(ui.comp(ui.fraktur("Facie ad Faciem"), ui.BROADCAST_GLOSS))),
                                                         "title %s title %s" % (ME, ui.row(ui.comp("面对面", WHITE, True)))])
    who2 = [ui.comp("〖", "#7C8593", True), {"selector": ME, "color": WHITE, "bold": True, "italic": False}, ui.comp("〗", "#7C8593", True), ui.comp(ui.GAP, ui.BROADCAST_BODY)]
    w("say_deaths", ["execute unless score %s rpg_dt_de matches 1.. run return 0" % ME] + line("S10", 2) + [
        "tellraw %s %s" % (ME, ui.row(*(who2 + [ui.comp("你死过 ", ui.BROADCAST_NAME), {"score": {"name": ME, "objective": "rpg_dt_de"}, "color": WHITE, "bold": True}, ui.comp(" 次。", ui.BROADCAST_NAME)])))])

    # ------------------------------------------------------------ 二段打空 → 绝境 → 结局
    w("stage/end2", ["# 二段打空：绝境没过就进绝境，过了就跪下", "function %s/sk/end" % B, "execute if entity @s[tag=rpg.dt.despdone] run return run function %s/end/begin" % B, "function %s/despair/begin" % B])


def hooks():
    """接到别的模块上：技能施放、喝药。"""
    p = os.path.join(DP, "data", "rpg", "function", "force", "cast.mcfunction")
    import io
    s = io.open(p, encoding="utf-8").read()
    key = "rpg_dt_cast"
    if key not in s:
        i = s.index("execute if score #k rpg_fo matches 1 run return run")
        s = s[:i] + "# 达阿特：影子记住这一招（add_daath.py）\nexecute if score @s rpg_dt matches 1.. run scoreboard players operation @s rpg_dt_cast = #k rpg_fo\n" + s[i:]
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    # 深渊里魔化不结算：不会在场地里降临（试炼只有你和影子）
    p = os.path.join(DP, "data", "rpg", "function", "taint", "step.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg_dt matches" not in s:
        io.open(p, "w", encoding="utf-8").write("execute if score @s rpg_dt matches 1.. run return 0" + chr(10) + s)
    wj(os.path.join(DP, "data", "rpg", "advancement", "daath", "drink.json"), {
        "criteria": {"d": {"trigger": "minecraft:consume_item"}},
        "rewards": {"function": B + "/hook/drank"}})
    w("hook/drank", ["advancement revoke @s only rpg:daath/drink", "execute if score @s %s matches 1.. run scoreboard players set @s rpg_dt_drk 1" % O])
