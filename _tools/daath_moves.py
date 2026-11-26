# -*- coding: utf-8 -*-
"""达阿特的影子：连招、弓弩、格反、影步、抓取、夺械、喝药、闪避、影版技能、二段招式（docs/DAATH-DESIGN.md §4.3～4.8）。"""
import json
import os

import daath_spec as S
from daath_lib import dummy
from daath_frame import ECHO, ECHO_ID, SK, start
from daath_lib import *  # noqa: F401,F403
from daath_lib import (B, DUST, DUST_D, LIGHTC, LOOK, ME, MID, NEAR, NEW, O, R, REF, SIL, SIL_I, UNIT, WHITE, WHITE_I, along, anim, at, beam, burst, every, face, fx, light_pillar,
                       line, lines_at, msg, ring, ripple, shards, shock, snd, span, step, txt, w, wave)

HITS = json.load(open(os.path.join(REF, "hits.json"), encoding="utf-8"))
SHAPES = {n: i + 1 for i, n in enumerate(("jab", "arc", "wide", "spin", "line", "smash"))}
CLS = {n: v[0] for n, v in S.CLASSES.items()}
LINE_LEN = {"sword": 4, "dagger": 4, "spear": 6, "glaive": 6}


def tag_near(r, pos="~ ~ ~"):
    return "execute positioned %s run tag @a[distance=..%s,%s] add rpg.dt.hit" % (pos, r, NEAR)


def hit(pc):
    return ["execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc %s %d" % (O, pc), "execute if entity @a[tag=rpg.dt.hit] run function %s/hurt/all" % B]


def slashes(size, n=1, spread=0, pos="^ ^1.2 ^1.4", color=SIL):
    return seq("slash", size * 0.78, pos.replace("^1.4", "^0.9").replace("^1.8", "^1.0").replace("^1.6", "^1.0"))


def end_at(t):
    return "execute if score @s rpg_dt_t matches %d.. run function %s/sk/end" % (t, B)


def chain():
    # ---------------- 连招：每一下重新抽武器、抽动作
    w("skill/chain", ["# 一套连招：2 到 6 下", "execute store result score @s rpg_dt_cl run random value 2..4",
                      "execute if score @s rpg_dt_st matches 2 run execute store result score @s rpg_dt_cl run random value 3..6",
                      "function %s/weapon/pick" % B,
                      "execute if score @s rpg_dt_wc matches 8..9 run return run function %s/skill/shoot" % B] + start("chain") + [
        "scoreboard players set @s rpg_dt_ht 999", "scoreboard players set @s rpg_dt_ln 10", face(), anim("guard")] + fx.twinkle("^-0.4 ^1.6 ^0.5", WHITE) + [
        snd("item.trident.riptide_1", 0.5, 1.7, 24)])
    w("sk/chain", ["# 起手十刻，之后一下接一下",
                   "execute if score @s rpg_dt_t < @s rpg_dt_ht run function %s/chain/close" % B,
                   "execute if score @s rpg_dt_t = @s rpg_dt_ht run function %s/chain/strike" % B,
                   "execute if score @s rpg_dt_t >= @s rpg_dt_ln run function %s/chain/next" % B])
    w("chain/close", ["# 出手前：盯着你、贴上来", "execute if score @s rpg_dt_t matches 1.. run " + face(),
                      "execute unless entity @a[tag=rpg.dt.me,distance=..2.1] at @s run " + step(0.36)])
    w("chain/next", ["execute unless score @s rpg_dt_cl matches 1.. run return run function %s/chain/done" % B, "scoreboard players remove @s rpg_dt_cl 1",
                     "execute if entity @a[tag=rpg.dt.me,distance=..9] run function %s/weapon/pick_melee" % B,
                     "execute unless entity @a[tag=rpg.dt.me,distance=..9] run return run function %s/chain/done" % B,
                     "scoreboard players set @s rpg_dt_t 0", face()] +
      ["execute if score @s rpg_dt_wc matches %d run function %s/hit/c_%s" % (i, B, n) for n, i in CLS.items() if n not in ("bow", "crossbow")])
    w("chain/done", ["function %s/sk/end" % B, anim("idle"), "execute if score @s rpg_dt_st matches 1 run scoreboard players set @s rpg_dt_gap 20", "execute if score @s rpg_dt_st matches 2 run scoreboard players set @s rpg_dt_gap 13"])
    w("weapon/pick_melee", ["# 连招里不抽弓弩：最多重抽三次", "function %s/weapon/pick" % B] + ["execute if score @s rpg_dt_wc matches 8..9 run function %s/weapon/pick" % B] * 3 + [
        "execute if score @s rpg_dt_wc matches 8..9 run function %s/weapon/none" % B])
    for cls in CLS:
        hs = [h for h in S.H if h[2] == cls]
        if not hs:
            continue
        w("hit/c_%s" % cls, ["execute store result score #r %s run random value 0..%d" % (O, len(hs) - 1)] +
          ["execute if score #r %s matches %d run return run function %s/hit/%s" % (O, i, B, h[0]) for i, h in enumerate(hs)])
        for nm, _src, _c, sh, pc, _lg in hs:
            ht, ln = HITS[nm]
            end = max(ht + 5, min(ln, ht + 10))
            w("hit/%s" % nm, ["scoreboard players set @s rpg_dt_ht %d" % max(ht, 3), "scoreboard players set @s rpg_dt_ln %d" % end, "scoreboard players set @s rpg_dt_pc %d" % pc,
                              "scoreboard players set @s rpg_dt_sh %d" % SHAPES[sh], anim(nm)])
    w("chain/strike", ["# 出手（as/at 影子）：按形状判"] +
      ["execute if score @s rpg_dt_sh matches %d run function %s/shape/%s" % (i, B, n) for n, i in SHAPES.items()] + [
        "execute if entity @a[tag=rpg.dt.hit] run scoreboard players operation #pc %s = @s rpg_dt_pc" % O, "execute if entity @a[tag=rpg.dt.hit] run function %s/hurt/all" % B,
        "execute if score @s rpg_dt_blade matches 1.. run particle minecraft:smoke ^ ^1 ^1.6 0.6 0.4 0.6 0.02 10"])
    w("shape/jab", [tag_near(1.7, "^ ^ ^1.5")] + slashes(1.8, pos="^ ^1.2 ^1.2") + [snd("entity.player.attack.sweep", 0.6, 1.5, 24)])
    w("shape/arc", [tag_near(2.3, "^ ^ ^1.7")] + slashes(2.6) + ["particle %s ^ ^1.1 ^1.8 0.7 0.1 0.7 0 5" % DUST, snd("entity.player.attack.sweep", 0.8, 1.0, 24)])
    w("shape/wide", [tag_near(3.2, "^ ^ ^1.3")] + slashes(3.6) + slashes(2.6, pos="^0.8 ^1.0 ^1.2", color=MID) + ["particle %s ^ ^1.1 ^1.8 1.2 0.1 1.2 0 10" % DUST, snd("entity.player.attack.sweep", 1.0, 0.8, 32)] + ripple())
    w("shape/spin", [tag_near(3.7)] + seq("axe", 4.6, "^ ^1.1 ^") + slashes(3.0, pos="^ ^1.1 ^1.6") +
      ripple() + wave("minecraft:cloud", 16, 0.22) + [snd("entity.player.attack.sweep", 1.2, 0.7, 32), snd("item.trident.throw", 0.7, 0.7, 32)])
    for ln in (4, 6):
        w("shape/line_%d" % ln, ["execute positioned ^ ^ ^%.1f run tag @a[distance=..1.25,%s] add rpg.dt.hit" % (d, NEAR) for d in [1.0 + 1.1 * i for i in range(int(ln / 1.1))]] +
          ["execute positioned ^ ^1.25 ^0.8 run %s" % c for c in beam(SIL_I, (0.14, 0.14, float(ln)), (0, 0, ln / 2.0))] + fx.born(kind="stabfade") + seq("thrust", ln * 0.7, "^ ^1.25 ^%.1f" % (ln * 0.5)) +
          along(DUST, ln, 0.8, 1.2, 0.08, 1) + [snd("item.trident.throw", 0.8, 1.4, 28)])
    w("shape/line", ["execute if score @s rpg_dt_wc matches 4..5 run return run function %s/shape/line_6" % B, "function %s/shape/line_4" % B])
    w("shape/smash", [tag_near(2.9, "^ ^ ^1.9")] + ["execute positioned ^ ^ ^1.9 run function %s/shape/quake" % B])
    w("shape/quake", dec("crack_mirror", 5.5, life=50) + fx.decal("rpg:daath_fx/smash_0", 6, WHITE, pos="~ ~0.08 ~", kind="ksmash") + wave("minecraft:cloud", 18, 0.28) + [
        "particle minecraft:block{block_state:\"minecraft:black_stained_glass\"} ~ ~0.2 ~ 1 0.1 1 0.1 24", snd("entity.player.attack.strong", 1.2, 0.6, 32), snd("block.glass.break", 0.8, 0.6, 32)])
    # ---------------- 弓弩
    w("skill/shoot", ["# 弓弩：弓一发满弦，弩三连；太近先退"] + start("shoot") + [face(), "execute if entity @a[tag=rpg.dt.me,distance=..4] run function %s/shoot/back" % B,
                      "execute if score @s rpg_dt_wc matches 8 run " + anim("bow_draw"), "execute if score @s rpg_dt_wc matches 9 run " + anim("xbow_load"),
                      "execute if score @s rpg_dt_wc matches 8 run " + snd("item.crossbow.loading_start", 0.8, 0.8), "execute if score @s rpg_dt_wc matches 9 run " + snd("item.crossbow.loading_middle", 0.8, 1)])
    w("shoot/back", [anim("roll_b"), "execute positioned ^ ^ ^-5 if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..%d] run tp @s ~ ~ ~" % (R - 1), snd("entity.player.attack.nodamage", 0.8, 0.8)])
    w("sk/shoot", [span(1, 17, face()), at(6, "execute if score @s rpg_dt_wc matches 8 run " + anim("bow_draw")),
                   "execute if score @s rpg_dt_t matches 10..17 positioned ^ ^1.4 ^0.6 run particle %s ~ ~ ~ 0.05 0.05 0.05 0 2" % DUST] +
      ["execute if score @s rpg_dt_t matches 18 if score @s rpg_dt_wc matches 8 run function %s/shoot/bow" % B] +
      ["execute if score @s rpg_dt_t matches %d if score @s rpg_dt_wc matches 9 run function %s/shoot/bolt" % (t, B) for t in (16, 22, 28)] + [
        span(19, 27, "execute if score @s rpg_dt_wc matches 9 run " + face()), end_at(38)])
    for nm, pc, sp, sz, cl in (("bow", 14, 1.5, 1.0, "bow"), ("bolt", 6, 1.2, 0.7, "xbow")):
        w("shoot/" + nm, [anim(cl), "execute positioned ^ ^1.35 ^0.8 facing entity %s eyes run summon minecraft:item_display ~ ~ ~ {Tags:[\"rpg.dt.shot\",\"rpg.dt.snew\"],item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"rpg:usurper_fx/beam\",\"minecraft:custom_model_data\":{colors:[%d]}}},brightness:{sky:15,block:15},teleport_duration:1,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[%gf,%gf,%gf],right_rotation:[0f,0f,0f,1f]}}" % (ME, SIL_I, 0.1 * sz, 0.1 * sz, 1.4 * sz),
                         "execute as @e[type=minecraft:item_display,tag=rpg.dt.snew,distance=..4] at @s facing entity %s eyes run rotate @s ~ ~" % ME,
                         "scoreboard players set @e[type=minecraft:item_display,tag=rpg.dt.snew,distance=..4] rpg_dt_life 34", "scoreboard players set @e[type=minecraft:item_display,tag=rpg.dt.snew,distance=..4] rpg_dt_pc %d" % pc,
                         "scoreboard players operation @e[type=minecraft:item_display,tag=rpg.dt.snew,distance=..4] %s = @s %s" % (O, O),
                         "tag @e[type=minecraft:item_display,tag=rpg.dt.snew,distance=..4] remove rpg.dt.snew", snd("rpg:daath.shot", 1.2, 1.0 if nm == "bolt" else 0.8)])
    w("shot/tick", ["# 飞行的箭（as/at 箭）：每刻 1.2 格，分两步查", "scoreboard players remove @s rpg_dt_life 1", "execute if score @s rpg_dt_life matches ..0 run return run kill @s",
                    "execute positioned ^ ^ ^0.6 if entity @a[tag=rpg.dt.in,distance=..1.9,gamemode=!spectator,gamemode=!creative] positioned ~ ~-0.9 ~ if entity @a[tag=rpg.dt.in,distance=..1.15] run return run function %s/shot/land" % B,
                    "execute positioned ^ ^ ^1.2 positioned ~ ~-0.9 ~ if entity @a[tag=rpg.dt.in,distance=..1.15,gamemode=!spectator,gamemode=!creative] run return run function %s/shot/land" % B,
                    "tp @s ^ ^ ^1.2", "particle %s ~ ~ ~ 0.05 0.05 0.05 0 1" % DUST])
    w("shot/land", ["tag @p[tag=rpg.dt.in,distance=..4] add rpg.dt.hit", "scoreboard players operation #pc %s = @s rpg_dt_pc" % O,
                    "execute as @e[%s,distance=..70,limit=1,sort=nearest] run tag @s add rpg.dt.it" % UNIT, "function %s/hurt/all" % B, "tag @e[%s] remove rpg.dt.it" % UNIT,
                    "particle %s ~ ~ ~ 0.2 0.2 0.2 0 8" % DUST, snd("rpg:daath.impact", 1, 1, 24), "kill @s"])


def skills():
    # ---------------- 格反
    w("skill/guard", start("guard") + [face(), anim("guard"), "scoreboard players set @s rpg_dt_mel 0", "scoreboard players set @s rpg_dt_gcd 160", "function %s/eye/blade" % B,
                                       snd("item.armor.equip_chain", 1, 0.8)])
    w("guard/go", ["tag @s remove rpg.dt.rip"] + start("riposte"))
    w("sk/guard", ["execute if entity @s[tag=rpg.dt.rip] run return run function %s/guard/go" % B] + every(4) + ["execute if score #m %s matches 0 run particle minecraft:end_rod ^ ^1.4 ^0.6 0.25 0.35 0.1 0.01 2" % O, end_at(30)])
    w("guard/mark", seq("eye", 1.6, "~ ~ ~"))
    w("guard/struck", ["# 格反中被打到：从正面就还手（as 影子）", "execute at @s positioned ^ ^ ^2 unless entity @a[tag=rpg.dt.me,distance=..3.2] run return 0",
                       "scoreboard players set #pc %s 0" % O, "tag @s add rpg.dt.rip"])
    w("sk/riposte", [at(1, face()), at(1, anim("ka3")), at(7, "function %s/guard/counter" % B), end_at(22)])
    w("guard/counter", [tag_near(2.6, "^ ^ ^1.8")] + hit(12) + slashes(3.4, color=WHITE) + burst("^ ^1.3 ^1", 2.2, WHITE) + shards(8) + [snd("item.shield.block", 1.2, 1.4), snd("block.glass.break", 1, 1.0)])
    # ---------------- 影步：从你自己的影子里钻出来
    w("skill/step", start("step") + ["scoreboard players set @s rpg_dt_far 0", "function %s/eye/step" % B, anim("vanish"), snd("rpg:daath.splinter", 1, 1)])
    w("sk/step", [span(1, 12, "particle %s ~ ~0.6 ~ 0.4 0.6 0.4 0.02 5" % "minecraft:squid_ink"), span(8, 20, "execute at %s run particle %s ~ ~0.05 ~ 0.6 0.02 0.6 0 8" % (ME, DUST_D)),
                  at(14, "function %s/step/out" % B), at(15, anim("sw3")), at(19, "function %s/step/stab" % B), end_at(34)])
    w("step/out", ["execute at %s rotated ~ 0 run tp @s ^ ^ ^-1.6 ~ 0" % ME] + ["execute at @s run function %s/step/fx" % B])
    w("step/fx", seq("ink", 3.6, "~ ~1.5 ~", "vertical") + seq("splash", 2.2, "~ ~0.7 ~", "vertical") + ripple() + [
        "particle minecraft:squid_ink ~ ~0.4 ~ 0.3 0.6 0.3 0.05 16", snd("rpg:daath.flash1", 1.2, 1), snd("entity.generic.splash", 0.8, 0.6)])
    w("step/stab", [face(), tag_near(2.2, "^ ^ ^1.5")] + hit(10) + slashes(2.8, color=WHITE) + [snd("entity.player.attack.sweep", 1, 0.8)])
    # ---------------- 抓取：破架
    w("skill/grab", start("grab") + ["scoreboard players set @s rpg_dt_still 0", "function %s/eye/shield" % B, face(), anim("throw"), snd("entity.warden.sonic_charge", 0.5, 1.6)])
    w("sk/grab", [span(1, 12, face()), span(6, 14, "execute unless entity @a[tag=rpg.dt.me,distance=..1.5] at @s run " + step(0.6)), at(16, "function %s/grab/take" % B), end_at(34)])
    w("grab/take", [tag_near(2.0, "^ ^ ^1.2"), "execute as @a[tag=rpg.dt.hit] at @s run tp @s ~ ~0.3 ~", "execute as @a[tag=rpg.dt.hit] run effect give @s minecraft:levitation 1 6 true",
                    "execute if entity @a[tag=rpg.dt.hit] run " + snd("entity.player.attack.knockback", 1.2, 0.6)] + hit(14) + wave("minecraft:cloud", 12, 0.2))
    # ---------------- 夺械
    w("skill/steal", start("steal") + ["execute store result score @s rpg_dt_scd run random value 500..700", "function %s/eye/hand" % B, face(), anim("cast"), "tag @s add rpg.dt.aim",
                                       snd("entity.evoker.prepare_wololo", 0.8, 0.7)])
    w("sk/steal", [span(1, 14, face()), at(14, "function %s/steal/lane" % B),
                   span(1, 20, "particle %s ^-0.4 ^1.3 ^0.8 0.1 0.1 0.1 0 3" % DUST_D), at(24, anim("throw")), at(26, "function %s/steal/reach" % B), end_at(46)])
    w("steal/lane", ["execute positioned ~ ~0.06 ~ run %s" % c for c in beam(0x7C8593, (1.6, 0.02, 8.0), (0, 0, 4.0))] + fx.born(14) + [snd("block.conduit.ambient.short", 1, 0.6)])
    w("steal/reach", ["# 一条 8 格的影子手；灯下夺不到", "execute positioned ~ ~0.06 ~ run %s" % beam(0x1A1D24, (1.4, 0.05, 8.0), (0, 0, 4.0))[0], "execute positioned ~ ~0.06 ~ run %s" % beam(0, (1, 1, 1), (0, 0, 0))[1]] + fx.born(kind="stabfade") +
      ["execute positioned ^ ^ ^%.1f run tag @a[distance=..1.3,%s] add rpg.dt.hit" % (1 + 1.2 * i, NEAR) for i in range(7)] + [
          "execute as @a[tag=rpg.dt.hit] at @s if entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..6] run tag @s remove rpg.dt.hit",
          "execute if entity @a[tag=rpg.dt.hit] run function %s/steal/caught" % B, "tag @a remove rpg.dt.hit", snd("item.trident.throw", 1, 0.5)])
    w("steal/caught", ["function %s/steal/take" % B, "execute at %s run function %s/steal/fx" % (ME, B), "execute as %s run effect give @s minecraft:slowness 1 2 true" % ME])
    w("steal/fx", seq("grab", 2.6, "~ ~1.2 ~") + ["particle minecraft:squid_ink ~ ~1.1 ~ 0.3 0.4 0.3 0.05 20", snd("rpg:daath.execute", 1.2, 1.1)])
    # ---------------- 喝药
    w("skill/drink", ["tag @s remove rpg.dt.want_drink"] + start("drink") + ["tag @s add rpg.dt.drk", "scoreboard players set @s rpg_dt_i 0", anim("drink")])
    w("sk/drink", every(5) + ["execute if score #m %s matches 0 run %s" % (O, snd("entity.generic.drink", 0.8, 0.8, 24)), span(1, 30, "particle minecraft:witch ~ ~1.6 ~ 0.15 0.2 0.15 0 1"),
                              at(34, "function %s/drink/heal" % B), end_at(40)])
    w("drink/heal", ["scoreboard players operation #h %s = @s rpg_dt_mx" % O, "scoreboard players set #k %s 60" % O, "scoreboard players operation #h %s *= #k %s" % (O, O), "scoreboard players operation #h %s /= #100 %s" % (O, O),
                     "scoreboard players operation #h %s += @s rpg_dt_h" % O, "scoreboard players operation #k %s = @s rpg_dt_mx" % O, "scoreboard players operation #k %s *= #10 %s" % (O, O),
                     "execute if score #h %s > #k %s run scoreboard players operation #h %s = #k %s" % (O, O, O, O),
                     "scoreboard players operation @s rpg_dt_h = #h %s" % O,
                     "particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 6", snd("entity.witch.drink", 1, 0.8)])
    w("drink/hit", ["scoreboard players add @s rpg_dt_i 1", "execute if score @s rpg_dt_i matches 3.. run function %s/drink/stop" % B])
    w("drink/stop", ["tag @s remove rpg.dt.drk", "scoreboard players set #s %s 24" % O, "function %s/stun" % B])
    # ---------------- 闪避
    w("skill/dodge", start("dodge") + [snd("rpg:daath.flash2", 0.7, 1.2, 32), face(), "execute store result score @s rpg_dt_i run random value 0..2", "execute if score @s rpg_dt_i matches 0 run " + anim("roll_l"), "execute if score @s rpg_dt_i matches 1 run " + anim("roll_r"),
                                       "execute if score @s rpg_dt_i matches 2 run " + anim("roll_f"), snd("entity.player.attack.nodamage", 0.8, 1.0)])
    for k, vec in ((0, "^0.45 ^ ^0.12"), (1, "^-0.45 ^ ^0.12"), (2, "^ ^ ^0.5")):
        w("dodge/%d" % k, ["execute positioned %s if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..%d] run tp @s ~ ~ ~" % (vec, R - 1)])
    w("sk/dodge", [span(1, 8, "execute if score @s rpg_dt_i matches %d run function %s/dodge/%d" % (k, B, k)) for k in range(3)] + ["particle minecraft:smoke ~ ~0.6 ~ 0.3 0.4 0.3 0.01 2", end_at(13)])


def echoes():
    """影版技能：八种。"""
    w("echo/cast", ["# 还一记影版", "scoreboard players operation #e %s = @s rpg_dt_ek" % O, "scoreboard players set @s rpg_dt_ek 0",
                    "execute unless entity @s[tag=rpg.dt.echoed] run function %s/echo/say" % B] +
      ["execute if score #e %s matches %d run return run function %s/skill/%s" % (O, i, B, n) for n, i in ECHO_ID.items()])
    w("echo/say", ["tag @s add rpg.dt.echoed"] + line("S05"))
    # 影矛：16 格直线
    w("skill/lance", start("lance") + [face(), anim("mighty"), snd("entity.illusioner.prepare_mirror", 1, 1.2)])
    w("sk/lance", [span(1, 8, face()), at(9, "function %s/lance/warn" % B), at(25, anim("sp3")), at(26, "function %s/lance/go" % B), end_at(44)])
    w("lance/warn", ["execute positioned ~ ~0.06 ~ run %s" % c for c in beam(0x7C8593, (1.4, 0.02, 16.0), (0, 0, 8.0))] + fx.born(18) + [snd("block.beacon.ambient", 1, 1.6)])
    w("lance/go", ["execute positioned ^ ^ ^%.1f run tag @a[distance=..1.4,%s] add rpg.dt.hit" % (1 + 1.4 * i, NEAR) for i in range(12)] + hit(12) +
      ["execute positioned ^ ^1.2 ^0.8 run %s" % c for c in beam(0xAAB4C3, (0.5, 0.5, 16.0), (0, 0, 8.0))] + fx.born(kind="linefade") +
      ["execute positioned ^ ^1.2 ^0.8 run %s" % c for c in beam(0x0B0C10, (0.3, 0.3, 16.0), (0, 0, 8.0))] + fx.born(kind="linefade") + along(DUST, 16, 1.2, 1.2, 0.2, 2) + [snd("entity.warden.sonic_boom", 0.6, 1.4), snd("item.trident.thunder", 0.4, 1.6)])
    # 影爆：五格
    w("skill/blast", start("blast") + [anim("updraft")] + fx.decal("sigil", 10, MID, pos="~ ~0.06 ~", life=26, kind="spinf") + fx.decal("ring", 10, SIL, life=24) + [snd("block.respawn_anchor.charge", 1, 0.6)])
    w("sk/blast", [span(1, 20, "particle minecraft:squid_ink ~ ~0.3 ~ 2.2 0.1 2.2 0.02 4"), at(22, "function %s/blast/go" % B), end_at(46)])
    w("blast/go", [tag_near(5.1)] + hit(14) + burst("~ ~1.2 ~", 5, SIL) + shock(SIL, 11) + fx.decal("ring", 1, WHITE, kind="ringx") + wave("minecraft:squid_ink", 24, 0.5) + shards(10, 0.8, 1.6) + [
        "particle minecraft:flash{color:11187395} ~ ~1 ~ 0 0 0 0 1 force", snd("rpg:daath.flash3", 1.4, 0.9), snd("block.glass.break", 1.2, 0.8)])
    # 影刃：八秒
    w("skill/blade", start("blade") + [anim("shake"), "scoreboard players set @s rpg_dt_blade 160", snd("item.firecharge.use", 1, 0.6)])
    w("sk/blade", [span(1, 18, "particle minecraft:smoke ^-0.4 ^1.2 ^0.4 0.2 0.4 0.2 0.02 4"), end_at(20)])
    # 影链：抓住一秒半
    w("skill/bind", start("bind") + [face(), anim("cast"), snd("block.chain.place", 1.2, 0.6)] + ["execute at %s run function %s/bind/mark" % (ME, B)])
    w("bind/mark", ["summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.dt.fx\",\"rpg.dt.bm\"]}", "scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.bm,distance=..0.5] rpg_dt_life 24",
                    "scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.bm,distance=..0.5] rpg_dt_kd 0"] + fx.decal("hexagram", 4.4, MID, life=20, kind="spinf"))
    w("sk/bind", [at(18, "function %s/bind/go" % B), end_at(40)])
    w("bind/go", ["# 圈画在 18 刻前你站的地方：走开就没事", "execute at @e[type=minecraft:marker,tag=rpg.dt.bm,distance=..50,limit=1,sort=nearest] run tag @a[distance=..2.2,%s] add rpg.dt.hit" % NEAR,
                  "execute as @a[tag=rpg.dt.hit] run effect give @s minecraft:slowness 2 9 true", "execute as @a[tag=rpg.dt.hit] at @s run function %s/bind/fx" % B] + hit(7))
    w("bind/fx", fx.glyph("d_chain", 2.2, WHITE, pos="~ ~1 ~", kind="kchain", billboard="vertical") + fx.glyph("d_chain", 2.2, WHITE, pos="~0.5 ~1.4 ~0.3", kind="kchain", billboard="vertical") + ["particle minecraft:squid_ink ~ ~1 ~ 0.4 0.8 0.4 0.02 16", snd("block.chain.break", 1.2, 0.6)])
    # 影壳：护盾，打破就眩晕
    w("skill/shell", start("shell") + [anim("kneel"), "scoreboard players operation @s rpg_dt_shell = @s rpg_dt_mx", "scoreboard players set #k %s 80" % O, "scoreboard players operation @s rpg_dt_shell *= #k %s" % O,
                                       "scoreboard players operation @s rpg_dt_shell /= #100 %s" % O, snd("block.beacon.power_select", 1, 0.7)] + fx.decal("hexagon", 4, SIL, life=60, kind="spinf"))
    w("sk/shell", ["particle %s ~ ~1 ~ 0.6 0.8 0.6 0 3" % DUST, "execute if score @s rpg_dt_t matches 80.. run function %s/shell/out" % B])
    w("shell/hit", ["# 护盾挨打：#d 十分之一点", "scoreboard players operation @s rpg_dt_shell -= #d %s" % O, snd("block.glass.hit", 1, 1.2, 24), "execute if score @s rpg_dt_shell matches ..0 run function %s/shell/burst" % B])
    w("shell/burst", ["scoreboard players set @s rpg_dt_shell 0", "scoreboard players set #s %s 40" % O, "function %s/stun" % B] + burst("~ ~1.2 ~", 3, WHITE))
    w("shell/out", ["scoreboard players set @s rpg_dt_shell 0", "function %s/sk/end" % B, anim("idle")])
    # 影傀：一个没穿盔甲的小影子
    w("skill/puppet", start("puppet") + [anim("gong"), snd("entity.illusioner.cast_spell", 1, 0.8)])
    w("sk/puppet", [at(10, "function %s/puppet/call" % B), end_at(24)])
    w("puppet/call", ["execute if entity @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=..60] run return 0",
                      "execute positioned ^2 ^ ^1 run summon minecraft:zombie ~ ~ ~ {Tags:[\"rpg.el.seen\",\"rpg.dt.minion\"],PersistenceRequired:1b,IsBaby:0b,Silent:1b,Health:60f,DeathLootTable:\"minecraft:empty\",attributes:[{id:\"minecraft:max_health\",base:60d},{id:\"minecraft:attack_damage\",base:0d},{id:\"minecraft:movement_speed\",base:0.3d},{id:\"minecraft:scale\",base:0.8d}],active_effects:[{id:\"minecraft:invisibility\",duration:-1,show_particles:0b}],equipment:{mainhand:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"rpg:empty\"}}},drop_chances:{mainhand:0f}}"]+ ["execute at @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=..8,limit=1] positioned ~ ~2 ~ run %s" % ln for ln in dummy(("rpg.dt.fx", "rpg.dt.pp"))] + ["scoreboard players set @e[type=minecraft:item_display,tag=rpg.dt.pp,distance=..12] rpg_dt_life 420", "scoreboard players set @e[type=minecraft:item_display,tag=rpg.dt.pp,distance=..12] rpg_dt_kd 0",
                      "scoreboard players set @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=..6] rpg_dt_life 400"])
    # 影印：全场，站到灯下可免
    w("skill/seal", start("seal") + [anim("mighty"), snd("block.end_portal.spawn", 0.6, 1.2)] + ["execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..40,limit=1] run function %s/seal/mark" % B])
    w("seal/mark", dec("seal_daath_lit", 14, pos="~ ~0.08 ~", life=64, kind="spinf") + fx.decal("ring", 28, MID, pos="~ ~0.07 ~", life=64) + fx.decal("ring", 45, SIL, pos="~ ~0.06 ~", life=64))
    w("sk/seal", [span(1, 58, "particle minecraft:squid_ink ~ ~0.4 ~ 9 0.1 9 0.02 8"), at(60, "function %s/seal/go" % B), end_at(84)])
    w("seal/go", ["# 站在亮着的灯下就没事", "execute as %s at @s unless entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..6] run tag @s add rpg.dt.hit" % ME] + hit(16) +
      ["particle minecraft:flash{color:11187395} ~ ~2 ~ 0 0 0 0 1 force", snd("entity.warden.sonic_boom", 1, 0.8)] + fx.decal("ring", 1, WHITE, kind="ringw"))


def stage2():
    # 影随
    w("skill/follow", start("follow") + [face(), anim("roll_f"), snd("entity.player.attack.nodamage", 0.8, 0.8)])
    w("sk/follow", [span(1, 9, "execute unless entity @a[tag=rpg.dt.me,distance=..1.6] at @s run " + step(0.62)), span(1, 6, face()), at(11, anim("sw3")), at(14, "function %s/follow/cut" % B), end_at(26)])
    w("follow/cut", [face(), tag_near(2.4, "^ ^ ^1.6")] + hit(10) + slashes(3.0, color=WHITE) + [snd("entity.player.attack.sweep", 1, 0.9)])
    # 熄灯
    w("skill/douse", start("douse") + ["tag @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..60,limit=1,sort=nearest] add rpg.dt.goal", anim("walk")])
    w("sk/douse", ["execute unless entity @e[type=minecraft:marker,tag=rpg.dt.goal,distance=..60] run return run function %s/sk/end" % B,
                   "execute facing entity @e[type=minecraft:marker,tag=rpg.dt.goal,distance=..60,limit=1] feet rotated ~ 0 run rotate @s ~ ~",
                   "execute unless entity @e[type=minecraft:marker,tag=rpg.dt.goal,distance=..1.2] at @s run " + step(0.3),
                   "execute if entity @e[type=minecraft:marker,tag=rpg.dt.goal,distance=..1.2] run return run function %s/douse/cut" % B, end_at(100)])
    w("douse/cut", [anim("ax3")] + slashes(3.6, color=DARK) + ["execute as @e[type=minecraft:marker,tag=rpg.dt.goal,distance=..3] at @s run function %s/douse/out" % B, snd("block.candle.extinguish", 1.2, 0.5), "function %s/sk/end" % B, "scoreboard players set @s rpg_dt_gap 14"])
    w("douse/out", ["execute as @e[type=minecraft:interaction,tag=rpg.dt.lamp,distance=..8,limit=1,sort=nearest] at @s run function %s/lamp/out" % B, "function %s/lamp/pool_out" % B])
    # 换位
    w("skill/swap", start("swap") + [anim("land"), snd("rpg:daath.mirror", 1.2, 1)] + burst("~ ~1.2 ~", 2.2, WHITE))
    w("sk/swap", [at(8, "function %s/swap/go" % B), at(28, "function %s/swap/boom" % B), end_at(40)])
    w("swap/go", ["# 互换位置；你原来的地方留下一记影爆", "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.dt.fx\",\"rpg.dt.sw1\"]}", "scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.sw1,distance=..1] rpg_dt_life 60", "scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.sw1,distance=..1] rpg_dt_kd 0",
                  "execute at %s run tp @s ~ ~ ~" % ME, "execute at @e[type=minecraft:marker,tag=rpg.dt.sw1,distance=..60,limit=1] run tp %s ~ ~ ~" % ME,
                  "execute at %s run function %s/swap/mark" % (ME, B), snd("entity.enderman.teleport", 1, 0.6), "execute at %s run playsound minecraft:block.glass.break hostile %s ~ ~ ~ 0.8 1.4" % (ME, ME)])
    w("swap/mark", fx.decal("ring", 6, SIL, life=20, tags=("rpg.dt.swr",)) + dec("crack_mirror", 5, life=24) + ripple())
    w("swap/boom", ["execute at @e[tag=rpg.dt.sw1,distance=..60,limit=1] run function %s/swap/hit" % B, "kill @e[type=minecraft:marker,tag=rpg.dt.sw1,distance=..60]"])
    w("swap/hit", ["tag @a[distance=..3.1,%s] add rpg.dt.hit" % NEAR] + hit(12) + burst("~ ~1 ~", 3.4, SIL) + shock(SIL, 7) + [snd("entity.generic.explode", 0.7, 1.3), snd("block.glass.break", 1, 0.8)])
    # 契约之影：你签的那一柱
    w("skill/pact", start("pact") + [face(), anim("shake"), snd("entity.evoker.prepare_attack", 1, 0.7)])
    warn, go = [], []
    for i in range(3):
        warn.append("execute positioned ^%d ^ ^%d run function %s/pact/mark" % ((-5, 0, 5)[i], (6, 4, 6)[i], B))
        go.append("execute positioned ^%d ^ ^%d run function %s/pact/pillar" % ((-5, 0, 5)[i], (6, 4, 6)[i], B))
    w("sk/pact", [at(1, face())] + [at(8, c) for c in warn] + [at(28, c) for c in go] + [end_at(48)])
    w("pact/mark", fx.decal("hexagram", 5, SIL, life=22, kind="spinf") + fx.decal("ring", 5, MID, life=22))
    pl = ["execute if entity @a[distance=..2.5,%s] run tag @a[distance=..2.5,%s] add rpg.dt.hit" % (NEAR, NEAR)] + hit(12)
    for i in range(1, 8):
        pl.append("execute if score %s rpg_pact matches %d run particle %s ~ ~2 ~ 0.6 1.6 0.6 0 40 force" % (ME, i, ui.pillar_transition(i, 2)))
    w("pact/pillar", pl + ["execute unless score %s rpg_pact matches 1..7 run particle %s ~ ~2 ~ 0.6 1.6 0.6 0 40 force" % (ME, DUST)] + light_pillar(SIL) + shock(MID, 6) + [snd("entity.lightning_bolt.impact", 0.6, 0.8)])


def minion():
    w("minion/gone", ["kill @e[type=minecraft:item_display,tag=rpg.dt.pp,distance=..16]", "particle minecraft:smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 16", "function %s/unit/vanish" % B])
    w("minion/tick", ["# 影傀（as/at）：贴身打 5%", "scoreboard players remove @s rpg_dt_life 1", "execute if score @s rpg_dt_life matches ..0 run return run function %s/minion/gone" % B,
                      "execute positioned ~ ~2 ~ rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rpg.dt.pp,distance=..16] ~ ~ ~ ~ ~",
                      "particle minecraft:smoke ~ ~0.8 ~ 0.2 0.4 0.2 0.005 2", "execute if score @s rpg_dt_gcd matches 1.. run return run scoreboard players remove @s rpg_dt_gcd 1",
                      "execute unless entity @a[tag=rpg.dt.in,distance=..1.8] run return 0", "scoreboard players set @s rpg_dt_gcd 24", "tag @p[tag=rpg.dt.in,distance=..1.8] add rpg.dt.hit",
                      "scoreboard players set #pc %s 5" % O, "execute as @e[%s,distance=..70,limit=1,sort=nearest] run tag @s add rpg.dt.it" % UNIT, "function %s/hurt/all" % B, "tag @e[%s] remove rpg.dt.it" % UNIT,
                      snd("entity.player.attack.sweep", 0.5, 1.4, 16)])


def build():
    chain()
    skills()
    echoes()
    stage2()
    minion()
    for n in ("chain", "shoot", "guard", "step", "grab", "steal", "drink", "dodge", "lance", "blast", "blade", "bind", "shell", "puppet", "seal", "follow", "douse", "swap", "pact"):
        w("debug/skill/%s" % n, ["# 调试：自己那个影子立刻出这一招（as/at 玩家）", "execute as @e[%s,distance=..80,limit=1,sort=nearest] at @s rotated ~ 0 run function %s/debug/as_%s" % (UNIT, B, n)])
        w("debug/as_%s" % n, ["tag @s add rpg.dt.it", "tag @p[tag=rpg.dt.in,distance=..90] add rpg.dt.me", "function %s/sk/end" % B, "function %s/skill/%s" % (B, n), "tag @a remove rpg.dt.me", "tag @s remove rpg.dt.it"])
