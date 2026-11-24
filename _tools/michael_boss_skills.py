# -*- coding: utf-8 -*-
"""米迦勒战的招式：普攻、一阶段与二阶段的技能、守望者、注视、圣焰叠层、骨柱。"""
from michael_boss_lib import *          # noqa: F401,F403
from michael_boss_lib import fx, w, art

EYE_FONT = mart.FONT
# 注视的三圈眼睛：(半径, 个数, 出现的刻, 半睁的刻, 高度, 大小)。眼睛是 Codex 画的六帧睁眼（字形 32 像素高，
# 所以大小是旧版 16 像素字形的一半）：0 闭、1 眼缝、2 半睁、3 全睁、4 爆亮、5 全睁收势
GAZE_RINGS = ((6, 8, 4, 50, 2.6, 2.6), (14, 14, 16, 53, 3.4, 3.6), (24, 20, 28, 56, 4.6, 4.6))
GAZE_OPEN, GAZE_END = 60, 82


def eye_json(frame):
    return '{text:"%s",font:"%s",color:"white"}' % (mart.glyph_text("eye", frame), EYE_FONT)


def skills1():
    # ---- 普攻：脊骨三连（原作长柄连招）。5 格内：两下各 7，第三下 270° 横扫 10（背后 90° 没有）
    w("basic/spine", [
        "scoreboard players add @s rpg_mk_n 1",
        face(MELEE1 + 1),
        "execute if score @s rpg_mk_cb matches 0 run function %s/skill/slash1" % B,
        "execute if score @s rpg_mk_cb matches 1 run function %s/skill/slash2" % B,
        "execute if score @s rpg_mk_cb matches 2 run function %s/skill/sweep" % B,
        "scoreboard players add @s rpg_mk_cb 1",
        "execute if score @s rpg_mk_cb matches 3.. run scoreboard players set @s rpg_mk_cb 0",
    ])
    for name, hit, busy in (("slash1", 7, 16), ("slash2", 9, 21), ("sweep", 8, 19)):
        w("skill/%s" % name, start(name, busy) + ["data merge entity @s {NoAI:1b}", anim(name)])
        w("sk/%s" % name, [at(hit, "function %s/strike/%s" % (B, "sweep" if name == "sweep" else "slash")),
                           "execute if score @s rpg_mk_t matches %d.. run function %s/sk/end" % (busy - 1, B)])
    w("strike/slash", ["# 脊骨一挥（as/at 他）：身前 2.6 格那一点 2.4 格内", tag_near(2.4, "^ ^ ^2.6")] + hurt_tagged(SLASH_DMG)
      + fx.slash("^ ^1.4 ^2", PEACH, size=3.4, roll=-28) + mglyph("star", 1.4, pos="^0.6 ^1.9 ^2.4", kind="twinkle", start=0.01, frame=2)
      + ["particle minecraft:sweep_attack ^ ^1.2 ^2.2 0.5 0.2 0.5 0 2",
                                                 "particle %s ^ ^1.3 ^2.4 0.6 0.3 0.6 0 6" % WHITE_DUST])
    w("strike/sweep", [
        "# 横扫（as/at 他）：5 格内，背后那一块除外",
        "tag @a[distance=..%s,%s] add rpg.mkb.hit" % (MELEE1, SURV),
        "execute positioned ^ ^ ^-2.8 run tag @a[distance=..2.3,tag=rpg.mkb.hit] remove rpg.mkb.hit",
    ] + hurt_tagged(SWEEP_DMG) + flat_glyph("arcw", 11, pos="~ ~0.9 ~", kind="arcwfx")
      + fx.decal("ring", 2, PEACH_I, pos="~ ~0.1 ~", kind="ringm")
      + ["particle minecraft:sweep_attack ~ ~1.1 ~ 2.2 0.3 2.2 0 8",
         "particle %s ~ ~1 ~ 2.5 0.4 2.5 0 20" % WHITE_DUST,
         "playsound minecraft:entity.player.attack.sweep hostile @a[distance=..24] ~ ~ ~ 1.2 0.7"])

    # ---- 守望者降临：召来两只守望者（同时最多一阶段 2、二阶段 3）；满了就换下一招
    full1, full2 = WATCH_MAX[1], WATCH_MAX[2]
    w("skill/watch", [
        "execute if score @s %s matches 1 if score #w %s matches %d.. run return run function %s/skill/quis" % (O, O, full1, B),
        "execute if score @s %s matches 2 if score #w %s matches %d.. run return run function %s/skill/dash" % (O, O, full2, B),
    ] + start("watch", 34) + ["data merge entity @s {NoAI:1b}", face(),
                              "execute if score @s %s matches 1 run %s" % (O, anim("mighty")),
                              "execute if score @s %s matches 2 run %s" % (O, anim("hero"))]
      + say_s("守望的圣者，从天而降。", gloss="Daniel 4:13", name="守望者降临 · "))
    w("sk/watch", [
        at(10, "execute at @e[%s] run function %s/watch/spawn" % (CENTER, B)),
        at(10, "execute store result score #w %s if entity @e[%s]" % (O, WATCH)),
        at(11, "execute if score @s %s matches 1 if score #w %s matches ..%d at @e[%s] run function %s/watch/spawn" % (O, O, full1 - 1, CENTER, B)),
        at(11, "execute if score @s %s matches 2 if score #w %s matches ..%d at @e[%s] run function %s/watch/spawn" % (O, O, full2 - 1, CENTER, B)),
        "execute if score @s rpg_mk_t matches 33.. run function %s/sk/end" % B,
    ])
    w("watch/spawn", [
        "execute if score #pro %s matches 1 run return 0" % O,   # 序章里的米迦勒不召守望者
        "# 一只守望者从场地边缘传送进来（at 中心）：随机方向 14 格外的地面",
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.mkb.wspot\"]}",
        "execute as @e[type=minecraft:marker,tag=rpg.mkb.wspot] store result entity @s Rotation[0] float 1 run random value 0..359",
        "execute as @e[type=minecraft:marker,tag=rpg.mkb.wspot] at @s rotated as @s positioned ^ ^ ^14 positioned over motion_blocking_no_leaves run function %s/watch/summon" % B,
        "kill @e[type=minecraft:marker,tag=rpg.mkb.wspot]",
    ])
    w("watch/summon", [
        'summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.mkw","rpg.mkb.w","rpg.mkb.wnew"],NoAI:1b,Silent:1b,PersistenceRequired:1b,'
        'DeathLootTable:"minecraft:empty",CustomName:{"text":"守望者","color":"%s","italic":false},Health:%df,'
        'active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}],'
        'attributes:[{id:"max_health",base:%df},{id:"knockback_resistance",base:0.6f}],drop_chances:{mainhand:0f,offhand:0f}}'
        % (FIRE, WATCH_HP, WATCH_HP),
        "execute as @e[%s,tag=rpg.mkb.wnew] store result score @s rpg_mk_wt run random value 0..18" % WATCH,
        "scoreboard players set @e[%s,tag=rpg.mkb.wnew] rpg_mk_ws 2" % WATCH,
        "execute as @e[%s,tag=rpg.mkb.wnew] at @s run %s" % (WATCH, face(ARENA * 2)),
        "tag @e[%s,tag=rpg.mkb.wnew] remove rpg.mkb.wnew" % WATCH,
        "function %s/vfx/blink" % B,
    ])
    w("watch/tick", [
        "# 守望者每刻（as/at 它）：照原作，传送到你身边、挥臂或双臂下砸；挨打会传送走（watch/hurt）",
        "scoreboard players add @s rpg_mk_wt 1",
    ] + every(4, "@s rpg_mk_wt") + [
        "execute if score #m %s matches 0 unless score @s rpg_mk_ws matches 3..4 run %s" % (O, face(ARENA)),
        "execute if score @s rpg_mk_ws matches 0 if score @s rpg_mk_wt matches 30.. unless entity @a[distance=..3.2,%s] run return run function %s/watch/blink" % (SURV, B),
        "execute if score @s rpg_mk_ws matches 0 if score @s rpg_mk_wt matches 30.. run return run function %s/watch/attack" % B,
        "execute if score @s rpg_mk_ws matches 1 if score @s rpg_mk_wt matches 8.. run return run function %s/watch/arrive" % B,
        "execute if score @s rpg_mk_ws matches 2 if score @s rpg_mk_wt matches 10.. run function %s/watch/ready" % B,
        "execute if score @s rpg_mk_ws matches 3 if score @s rpg_mk_wt matches 8 run function %s/watch/strike" % B,
        "execute if score @s rpg_mk_ws matches 3 if score @s rpg_mk_wt matches 24.. run function %s/watch/rest" % B,
        "execute if score @s rpg_mk_ws matches 4 if score @s rpg_mk_wt matches 14 run function %s/watch/heavyhit" % B,
        "execute if score @s rpg_mk_ws matches 4 if score @s rpg_mk_wt matches 32.. run function %s/watch/rest" % B,
    ])
    w("watch/blink", ["# 传送出去（as/at 它）", "scoreboard players set @s rpg_mk_ws 1", "scoreboard players set @s rpg_mk_wt 0",
                      wanim("tp_out"), "particle minecraft:large_smoke ~ ~1.4 ~ 0.3 0.8 0.3 0.02 8"])
    w("watch/arrive", [
        "# 出现在最近那人身边（as 它）：四个方向里挑一个能站的",
        "scoreboard players set @s rpg_mk_ws 2", "scoreboard players set @s rpg_mk_wt 0",
        "execute store result score #r %s run random value 0..3" % O,
    ] + [ground("tp @s ~ ~ ~", "^ ^ ^2.4").replace("execute positioned", "execute if score #r %s matches %d at @p[distance=..%d,%s] rotated ~%d 0 positioned"
                                                   % (O, k, ARENA * 2, SURV, 90 * k), 1) for k in range(4)] + [
        "execute at @s run %s" % face(ARENA),
        wanim("tp_in"),
        "execute at @s run function %s/vfx/blink" % B,
    ])
    w("watch/ready", ["scoreboard players set @s rpg_mk_ws 0", "scoreboard players set @s rpg_mk_wt 22"])
    w("watch/attack", [
        "scoreboard players set @s rpg_mk_wt 0",
        "scoreboard players set @s rpg_mk_ws 3",
        "execute if predicate rpg:michael_boss/heavy run scoreboard players set @s rpg_mk_ws 4",
        "execute if score @s rpg_mk_ws matches 3 run " + wanim("attack"),
        "execute if score @s rpg_mk_ws matches 4 run " + wanim("heavy"),
    ])
    w("watch/strike", ["# 挥臂（as/at 它）", tag_near(1.8, "^ ^ ^1.6"),
                       "execute as @a[tag=rpg.mkb.hit] run damage @s %d minecraft:mob_attack by @e[%s,limit=1,sort=nearest]" % (WATCH_HIT, WATCH),
                       "tag @a remove rpg.mkb.hit", "particle minecraft:sweep_attack ^ ^1.4 ^1.4 0.3 0.2 0.3 0 1"])
    w("watch/heavyhit", ["# 双臂下砸（as/at 它）", tag_near(2.4, "^ ^ ^1.8"),
                         "execute as @a[tag=rpg.mkb.hit] run damage @s %d minecraft:mob_attack by @e[%s,limit=1,sort=nearest]" % (WATCH_HEAVY, WATCH),
                         "tag @a remove rpg.mkb.hit"]
      + fx.decal("shock_0", 3.6, FIRE_I, pos="^ ^0.1 ^1.8", kind="shock") + impact("^ ^0.6 ^1.8", True, 2.4)
      + ["particle minecraft:block{block_state:\"minecraft:obsidian\"} ^ ^0.2 ^1.8 0.5 0.1 0.5 0 12",
         "playsound minecraft:entity.iron_golem.attack hostile @a[distance=..24] ~ ~ ~ 1 0.6"])
    w("watch/rest", ["scoreboard players set @s rpg_mk_ws 0", "execute store result score @s rpg_mk_wt run random value 0..12",
                     wanim("idle")])
    w("watch/hurt", [
        "# 玩家打到了守望者（as 玩家）：三成机会，它传送走",
        "advancement revoke @s only rpg:michael_boss/hit_watch",
        "execute as @e[%s,distance=..8,limit=1,sort=nearest] unless score @s rpg_mk_ws matches 1..2 if predicate rpg:michael_boss/flee at @s run function %s/watch/flee" % (WATCH, B),
    ])
    w("watch/flee", [
        "# 受击传送（as/at 它）：往后 6 格",
        "function %s/vfx/blink" % B,
        ground("tp @s ~ ~ ~", "^ ^ ^-6"),
        "scoreboard players set @s rpg_mk_ws 2", "scoreboard players set @s rpg_mk_wt 0",
        wanim("tp_in"),
        "execute at @s run function %s/vfx/blink" % B,
    ])
    w("watch/die", ["# 收场时守望者散去（as 它）", "execute at @s run particle minecraft:ash ~ ~1.5 ~ 0.4 1 0.4 0 40"]
      + ["execute at @s run " + c if c.startswith("summon") else c for c in smoke_puff("~ ~1.6 ~", 3.2)] + [
                    "execute at @s run particle minecraft:flame ~ ~2.4 ~ 0.3 0.3 0.3 0.02 8",
                    "function %s/clear_unit" % B])

    # ---- 谁似神（骨刺）：举脊骨蓄力 1 秒，地上一条 16 格的裂线，骨刺一节一节往前冒
    w("skill/quis", start("quis", 44) + ["data merge entity @s {NoAI:1b}", face(), anim("mighty")]
      + ["execute positioned ~ ~0.05 ~ run %s" % s for s in beam(PEACH_I, (0.9, 0.02, 16), (0, 0, 8), tags=("rpg.mkb.quiswarn",))]
      + fx.born(22) + say_s("谁似神？", name="骨刺 · ")
      + ["playsound minecraft:block.bone_block.hit hostile @a[distance=..24] ~ ~ ~ 1 0.6"])
    w("sk/quis", [
        span(1, 16, face()),
        span(1, 16, "execute as @e[tag=rpg.mkb.quiswarn,distance=..2] positioned as @s rotated as @e[%s,limit=1] run tp @s ~ ~ ~ ~ ~" % UNIT),
        span(1, 18, "particle %s ^ ^2.4 ^0.3 0.15 0.4 0.15 0 2" % WHITE_DUST),
        at(20, anim("slash1")),
        at(1, "function %s/quis/charge" % B),
        at(21, "function %s/quis/slam" % B),
        at(22, "execute rotated ~ 0 run function %s/quis/walker" % B),
        "execute if score @s rpg_mk_t matches 42.. run function %s/sk/end" % B,
    ])
    w("quis/charge", ["# 举脊骨蓄力（as/at 他）：身后一圈光环，脚下圣印"]
      + mglyph("halo", 3.2, pos="~ ~2.6 ~", kind="haloloop", life=22) + fx.decal("sigil", 4, PEACH_I, pos="~ ~0.07 ~", kind="spinf", life=24))
    w("quis/slam", ["# 下劈（as/at 他）"] + impact("^ ^0.5 ^2", False, 3.2) + fx.decal("shock_0", 4, PEACH_I, pos="^ ^0.1 ^2", kind="shock"))
    w("quis/walker", ["# 骨刺的行走点（at 起点，朝这条线）：每刻往前 1 格，破土一节", fx.marker("~ ~ ~", "rpg.mkb.walker"),
                      "execute as @e[tag=%s] run tp @s ~ ~ ~ ~ 0" % NEW] + fx.born(17)
      + ["playsound minecraft:block.bone_block.break hostile @a[distance=..32] ~ ~ ~ 1.2 0.5",
         "playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..32] ~ ~ ~ 0.8 0.8"])
    w("fx/walker", [
        "# 骨刺（as/at 行走点）：生命到 17 以下才动（骨柱的那一条先等预警）",
        "execute if score @s rpg_mk_life matches ..17 run function %s/walker/step" % B,
    ])
    w("walker/step", ["tp @s ^ ^ ^1", "execute at @s run function %s/walker/burst" % B])
    w("walker/burst", SPIKE + [
        "tag @a[distance=..1.3,%s] add rpg.mkb.hit" % SURV,
        "execute as @a[tag=rpg.mkb.hit] run damage @s %d minecraft:mob_attack by @e[%s,limit=1]" % (QUIS_DMG, UNIT),
        "tag @a remove rpg.mkb.hit",
    ])

    # ---- 羽刃：振翼射出扇形五片燃烧的羽毛
    w("skill/feather", start("feather", 30) + ["data merge entity @s {NoAI:1b}", face(), anim("showoff"),
                                                "playsound minecraft:entity.phantom.flap hostile @a[distance=..24] ~ ~ ~ 1.4 0.8"]
      + say_s("羽毛也是刃。", name="羽刃 · "))
    w("sk/feather", [at(6, "execute rotated ~%d 0 positioned ^ ^1.4 ^1 run function %s/feather/one" % (y, B)) for y in (-30, -15, 0, 15, 30)]
      + ["execute if score @s rpg_mk_t matches 29.. run function %s/sk/end" % B])
    w("feather/one", [
        "# 一片燃烧的羽毛（at 起点，朝飞行方向）",
        'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.feather"],'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_boss/feather"}},item_display:"none",'
        'brightness:{sky:15,block:15},teleport_duration:1,view_range:2f,transformation:{translation:[0f,0f,0f],'
        'left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[1.2f,1.2f,1.2f],right_rotation:[0f,0f,0f,1f]}}',
        "tp @e[tag=%s,limit=1] ~ ~ ~ ~ 0" % NEW,
    ] + fx.born(30))
    w("fx/feather", [
        "# 飞行的羽毛（as/at 它）：每刻 0.9 格；碰到人就扎上去",
        "tp @s ^ ^ ^0.9",
        "execute at @s run particle minecraft:flame ~ ~ ~ 0.05 0.05 0.05 0.01 1",
    ] + every(4, "@s rpg_mk_life") + [
        "execute if score #m %s matches 0 at @s run function %s/feather/trail" % (O, B),
        "execute at @s if entity @a[distance=..1.1,%s] run function %s/feather/hit" % (SURV, B),
    ])
    w("feather/trail", mglyph("tongue", 0.9, pos="~ ~ ~", kind="tongue"))
    w("feather/hit", [tag_near(1.1)] + hurt_tagged(FEATHER_DMG) + mglyph("fburn", 1.6, pos="~ ~ ~", kind="fburn")
      + impact("~ ~ ~", True, 2.0) + [
        "particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.05 6", "kill @s"])

    # ---- 天降：振翼升空，圈跟着你走 1.5 秒后锁定，俯冲砸下
    w("skill/dive", start("dive", 60) + ["data merge entity @s {NoAI:1b,NoGravity:1b}", "tag @s add rpg.mkb.air", anim("rise"),
                                          "playsound minecraft:entity.phantom.flap hostile @a[distance=..32] ~ ~ ~ 1.6 0.6"]
      + aimed("function %s/dive/mark" % B) + say_s("我从高处来。", name="天降 · ") + wingburst("~ ~1.8 ~", 7)
      + feathers_out("~ ~1.2 ~", 4))
    w("dive/mark", ["# 落点（at 瞄准点）：一圈圣焰，先跟着走", fx.marker("~ ~ ~", "rpg.mkb.diveto")] + fx.born(40)
      + fx.decal("ring", 6, FIRE_I, pos="~ ~0.06 ~", life=36, tags=("rpg.mkb.divering",))
      + fx.decal("glow", 6, CORAL_I, pos="~ ~0.05 ~", life=36, tags=("rpg.mkb.divering",))
      + fx.decal("sigil", 5, PEACH_I, pos="~ ~0.07 ~", kind="spinf", life=36, tags=("rpg.mkb.divering",)))
    w("sk/dive", [
        span(2, 12, "tp @s ~ ~0.55 ~"),
        span(2, 28, "execute if score #w %s matches 1.. as @e[tag=rpg.mkb.diveto] at @p[distance=..%d,%s] run tp @s ~ ~ ~" % (O, ARENA, SURV)),
        span(2, 28, "execute if score #w %s matches ..0 as @e[tag=rpg.mkb.diveto] at @e[%s] run tp @s ~ ~ ~" % (O, LAG)),
        span(2, 28, "execute as @e[tag=rpg.mkb.divering] at @e[tag=rpg.mkb.diveto,limit=1] run tp @s ~ ~0.06 ~"),
        at(28, "playsound minecraft:block.note_block.bell hostile @a[distance=..32] ~ ~ ~ 1 1.6"),
        at(34, "execute at @e[tag=rpg.mkb.diveto,limit=1] run tp @s ~ ~ ~"),
        at(34, "data merge entity @s {NoGravity:0b}"),
        at(34, anim("land")),
        at(35, "function %s/dive/hit" % B),
        "execute if score @s rpg_mk_t matches 58.. run function %s/sk/end" % B,
    ])
    w("dive/hit", [
        "# 砸下（as/at 他）：3 格内 %d，3～6 格冲击波 %d" % (DIVE_DMG, DIVE_EDGE),
        "kill @e[tag=rpg.mkb.diveto]", "kill @e[tag=rpg.mkb.divering]",
        "tag @a[distance=..3,%s] add rpg.mkb.hit" % SURV,
    ] + hurt_tagged(DIVE_DMG) + ["tag @a[distance=3..6,%s] add rpg.mkb.hit" % SURV] + hurt_tagged(DIVE_EDGE)
      + fx.decal("shock_0", 12, PEACH_I, pos="~ ~0.1 ~", kind="shock") + fx.decal("cracks", 6, 0x2A2020, pos="~ ~0.04 ~", life=80)
      + impact("~ ~1.2 ~", False, 6) + godray("~ ~ ~") + feathers_out("~ ~1.6 ~", 8)
      + wave("minecraft:flame", 24, 0.4, y=0.3) + wave(WHITE_DUST, 16, 0.3, y=0.8) + [
        "particle minecraft:flash{color:%d} ~ ~1 ~ 0 0 0 0 1 force" % PEACH_I,
        "playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1 0.8",
        "playsound minecraft:entity.phantom.flap hostile @a[distance=..40] ~ ~ ~ 1.4 0.5",
    ])

    # ---- 六翼掩面：六翼合拢 2 秒（伤害减八成），然后猛然展开，6 格内羽刃 8；展开后显形 1.5 秒
    w("skill/fold", start("fold", 64) + ["data merge entity @s {NoAI:1b}", anim("fold"), "tag @s add rpg.mkb.fold"]
      + say_s("用两个翅膀遮脸。", gloss="Isaiah 6:2", name="六翼掩面 · "))
    w("sk/fold", [
        span(1, 38, "particle minecraft:end_rod ~ ~1.3 ~ 0.4 0.7 0.4 0.01 1"),
        at(2, "function %s/fold/close" % B),
        at(30, "playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1 1.4"),
        at(40, "function %s/fold/open" % B),
        "execute if score @s rpg_mk_t matches 62.. run function %s/sk/end" % B,
    ])
    w("fold/close", ["# 合拢（as/at 他）：背后的光环与脚下圣印"] + mglyph("halo", 4.2, pos="~ ~1.7 ~", kind="haloloop", life=38)
      + fx.decal("sigil", 4.5, PEACH_I, pos="~ ~0.07 ~", kind="spinf", life=38) + fx.decal("glow", 4, PEACH_I, pos="~ ~0.06 ~", life=38))
    w("fold/open", ["# 六翼展开（as/at 他）：6 格内羽刃，击退；然后显形", "tag @s remove rpg.mkb.fold", anim("hero"),
                    "tag @a[distance=..6,%s] add rpg.mkb.hit" % SURV] + hurt_tagged(FOLD_DMG)
      + fx.decal("ring", 2, PEACH_I, pos="~ ~0.08 ~", kind="ringx") + wave("minecraft:end_rod", 24, 0.5, y=1.2)
      + wingburst("~ ~1.7 ~", 9) + feathers_out("~ ~1.5 ~", 8) + impact("~ ~1.4 ~", False, 5)
      + wave("minecraft:flame", 16, 0.35, y=1.6) + solid(30) + [
        "playsound minecraft:entity.phantom.flap hostile @a[distance=..40] ~ ~ ~ 2 0.5",
        "playsound minecraft:item.trident.riptide_3 hostile @a[distance=..40] ~ ~ ~ 1 1.2"])

    # ---- 注视（用户指定）：眼睛一圈一圈向外铺满场地，半睁，全睁：全屏伤害，每只守望者 +6，背对他减半
    gz = [span(1, GAZE_OPEN, "particle minecraft:end_rod ~ ~2 ~ 1.2 1 1.2 0.02 2")]
    for k, (r, n, t_out, t_half, h, size) in enumerate(GAZE_RINGS, 1):
        gz += [at(t_out, "function %s/gaze/ring%d" % (B, k)),
               at(t_out + 1, "execute as @e[tag=rpg.mkb.eye%d] at @s run tp @s ^ ^%s ^%d" % (k, round(h - 2.4, 2), r)),
               at(t_out, "playsound minecraft:entity.elder_guardian.ambient hostile @a[distance=..48] ~ ~ ~ 1 %.1f" % (1.6 - 0.2 * k)),
               at(t_half - 3, "execute as @e[tag=rpg.mkb.eye%d] run data modify entity @s text set value %s" % (k, eye_json(1))),
               at(t_half, "execute as @e[tag=rpg.mkb.eye%d] run data modify entity @s text set value %s" % (k, eye_json(2))),
               at(t_out, "function %s/gaze/floor%d" % (B, k))]
        w("gaze/floor%d" % k, ["# 第 %d 圈的地面红环（as/at 他）" % k] + mdecal("ring_r", 2 * r + 1, pos="~ ~0.07 ~", life=GAZE_END + 4 - t_out))
        eyes = []
        for i in range(n):
            yaw = round(360.0 * i / n + (k * 7), 1)
            eyes.append('summon minecraft:text_display ~ ~2.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.eye","rpg.mkb.eye%d"],'
                        'Rotation:[%sf,0f],text:%s,background:0,billboard:"center",brightness:{sky:15,block:15},'
                        'teleport_duration:10,view_range:4f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],'
                        'scale:[%sf,%sf,%sf],right_rotation:[0f,0f,0f,1f]}}' % (k, yaw, eye_json(0), size, size, size))
        w("gaze/ring%d" % k, ["# 第 %d 圈眼睛（as/at 他）：%d 只闭着的眼睛，下一刻飞到 %d 格外" % (k, n, r)] + eyes + fx.born(GAZE_END + 4))
    gz += [at(1, "function %s/gaze/seal" % B),
           at(50, say("不可直视。")),
           at(GAZE_OPEN, "execute as @e[tag=rpg.mkb.eye] run data modify entity @s text set value %s" % eye_json(3)),
           at(GAZE_OPEN + 1, "execute as @e[tag=rpg.mkb.eye] run data modify entity @s text set value %s" % eye_json(4)),
           at(GAZE_OPEN + 5, "execute as @e[tag=rpg.mkb.eye] run data modify entity @s text set value %s" % eye_json(5)),
           at(GAZE_OPEN, "function %s/gaze/burst" % B)]
    for t_, line in ((20, full_title("vig", 0, (6, 30, 0))), (38, full_title("vig", 1, (0, 30, 0))), (52, full_title("vig", 2, (0, 12, 0))),
                     (GAZE_OPEN + 2, full_title("flash", 1, (0, 3, 0))), (GAZE_OPEN + 4, full_title("flash", 2, (0, 3, 0))),
                     (GAZE_OPEN + 6, full_title("flash", 3, (0, 2, 12)))):
        gz += [at(t_, "title @a[distance=..%d] clear" % (ARENA + 8))] + [at(t_, c) for c in line]
    w("gaze/seal", ["# 他脚下的眼印与身后的守望之眼（as/at 他）"]
      + mdecal("seal_eye", 9, pos="~ ~0.08 ~", kind="spins", life=GAZE_END + 2) + fx.decal("glow", 8, FIRE_I, pos="~ ~0.06 ~", life=GAZE_END + 2)
      + mglyph("gaze", 3.4, pos="~ ~3.6 ~", kind="gazeloop", life=GAZE_END))
    gz += [
           at(GAZE_OPEN + 12, "execute as @e[tag=rpg.mkb.eye] at @s run function %s/gaze/fade" % B),
           "execute if score @s rpg_mk_t matches %d.. run function %s/sk/end" % (GAZE_END, B)]
    w("skill/gaze", start("gaze", GAZE_END + 2) + ["data merge entity @s {NoAI:1b}", face(), anim("hero"),
                                                   "playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..48] ~ ~ ~ 1 0.8"]
      + say_s("众目都看着你。", name="注视 · ") + ["function %s/vfx/wings" % B])
    w("sk/gaze", gz)
    burst = [
        "# 全睁（as/at 他）：全屏一闪，黑暗，场上所有人挨一下；背对他的减半；每只活着的守望者 +%d" % GAZE_PER,
        "tag @a remove rpg.mkb.away",
        "execute as @a[distance=..%d,%s] at @s rotated ~ 0 positioned ^ ^ ^100 unless entity @e[%s,distance=..100] run tag @s add rpg.mkb.away"
        % (ARENA + 4, SURV, UNIT),
        "execute store result score #w %s if entity @e[%s]" % (O, WATCH),
    ]
    for k in range(WATCH_MAX[2] + 1):
        full = GAZE_BASE + GAZE_PER * k
        burst += ["execute if score #w %s matches %d%s as @a[distance=..%d,%s,tag=!rpg.mkb.away] run damage @s %d minecraft:mob_attack by @e[%s,limit=1]"
                  % (O, k, ".." if k == WATCH_MAX[2] else "", ARENA + 4, SURV, full, UNIT),
                  "execute if score #w %s matches %d%s as @a[distance=..%d,%s,tag=rpg.mkb.away] run damage @s %d minecraft:mob_attack by @e[%s,limit=1]"
                  % (O, k, ".." if k == WATCH_MAX[2] else "", ARENA + 4, SURV, full // 2, UNIT)]
    burst += [
    ] + full_title("flash", 0, (0, 3, 0)) + wingburst("~ ~1.8 ~", 10) + godray("~ ~ ~", True) + impact("~ ~2 ~", True, 7) + [
        "execute as @e[tag=rpg.mkb.eye] at @s run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.04 4",
        "effect give @a[distance=..%d,%s] minecraft:darkness 2 0 true" % (ARENA + 4, SURV),
        "execute as @e[tag=rpg.mkb.eye] at @s run particle minecraft:flash{color:%d} ~ ~ ~ 0 0 0 0 1 force" % FIRE_I,
        "particle minecraft:flash{color:%d} ~ ~2 ~ 0 0 0 0 1 force" % PEACH_I,
        "playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..48] ~ ~ ~ 2 0.6",
        "playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 2 0.5",
        "tag @a remove rpg.mkb.away",
    ]
    w("gaze/burst", burst)
    w("gaze/fade", ["# 眼睛散去（as/at 它）", "particle minecraft:end_rod ~ ~ ~ 0.3 0.3 0.3 0.02 3", "kill @s"])


def skills2():
    # ---- 普攻：双肋连斩（原作双匕首六段，每次随机两段），3.5 格内各 5；带圣焰
    w("basic/rib", ["scoreboard players add @s rpg_mk_n 1", face(MELEE2 + 1), "function %s/skill/rslash" % B])
    w("skill/rslash", start("rslash", 12) + ["data merge entity @s {NoAI:1b}",
                                              "execute store result score #r %s run random value 1..6" % O]
      + ["execute if score #r %s matches %d run %s" % (O, i, anim("rib_slash%d" % i)) for i in range(1, 7)])
    w("sk/rslash", [
        at(3, "function %s/strike/rib" % B),
        at(6, "execute store result score #r %s run random value 1..6" % O),
    ] + [at(6, "execute if score #r %s matches %d run %s" % (O, i, anim("rib_slash%d" % i))) for i in range(1, 7)] + [
        at(8, "function %s/strike/rib" % B),
        "execute if score @s rpg_mk_t matches 11.. run function %s/sk/end" % B,
    ])
    w("strike/rib", ["# 肋骨一斩（as/at 他）", tag_near(1.9, "^ ^ ^1.9")] + hurt_tagged(RIB_DMG, flame=True)
      + ["execute if score #r %s matches 1..3 run %s" % (O, c) if c.startswith("summon") else c for c in fx.slash("^ ^1.3 ^1.5", CORAL, size=2.6, roll=-35)]
      + ["execute if score #r %s matches 4..6 run %s" % (O, c) if c.startswith("summon") else c for c in fx.slash("^ ^1.3 ^1.5", CORAL, size=2.6, roll=145)]
      + ["particle minecraft:flame ^ ^1.2 ^1.6 0.3 0.2 0.3 0.02 4"])

    # ---- 圣焰（被动）：命中叠一层；叠满 3 层 0.5 秒后炸开 10 并持续烧 3 秒；5 秒没被打中清零
    w("flame/add", [
        "# 叠一层圣焰（as 玩家）",
        "tag @s add rpg.mkb.flamed",
        "scoreboard players add @s rpg_mk_fl 1",
        "scoreboard players set @s rpg_mk_ft 100",
    ] + ["execute at @s run " + c if c.startswith("summon") else c for c in mglyph("drop", 1.0, pos="~ ~2.3 ~", kind="drop")] + [
        "execute if score @s rpg_mk_fl matches 3.. unless score @s rpg_mk_fu matches 1.. run function %s/flame/kindle" % B,
        "execute if score @s rpg_mk_fl matches 1 run title @s actionbar [{\"text\":\"圣焰 \",\"color\":\"%s\"},{\"text\":\"● ○ ○\",\"color\":\"%s\"}]" % (CORAL, FIRE),
        "execute if score @s rpg_mk_fl matches 2 run title @s actionbar [{\"text\":\"圣焰 \",\"color\":\"%s\"},{\"text\":\"● ● ○\",\"color\":\"%s\"}]" % (CORAL, FIRE),
    ])
    w("flame/kindle", ["# 点燃（as 玩家）：0.5 秒的引信", "scoreboard players set @s rpg_mk_fl 0", "scoreboard players set @s rpg_mk_fu 10",
                       "title @s actionbar [{\"text\":\"圣焰 \",\"color\":\"%s\"},{\"text\":\"● ● ●\",\"color\":\"%s\",\"bold\":true}]" % (CORAL, FIRE),
                       "playsound minecraft:item.firecharge.use hostile @a[distance=..24] ~ ~ ~ 1 0.8"])
    w("flame/tick", [
        "# 身上有圣焰（as/at 玩家）",
        "scoreboard players remove @s rpg_mk_ft 1",
        "execute if score @s rpg_mk_ft matches ..0 run scoreboard players set @s rpg_mk_fl 0",
        "execute if score @s rpg_mk_fl matches 1.. run particle minecraft:small_flame ~ ~1 ~ 0.3 0.5 0.3 0.01 1",
        "execute if score @s rpg_mk_fl matches 2.. run particle minecraft:flame ~ ~1.2 ~ 0.3 0.5 0.3 0.01 1",
        "execute if score @s rpg_mk_fu matches 1.. run scoreboard players remove @s rpg_mk_fu 1",
        "execute if score @s rpg_mk_fu matches 1.. run particle minecraft:flame ~ ~1 ~ 0.4 0.6 0.4 0.03 4",
        "execute if score @s rpg_mk_fu matches 0 run function %s/flame/burst" % B,
        "execute if score @s rpg_mk_r matches 1.. run function %s/flame/burn" % B,
        "execute unless score @s rpg_mk_fl matches 1.. unless score @s rpg_mk_fu matches 1.. unless score @s rpg_mk_r matches 1.. run function %s/flame/out" % B,
    ])
    w("flame/burst", ["# 圣焰炸开（as/at 玩家）", "scoreboard players reset @s rpg_mk_fu", "scoreboard players set @s rpg_mk_r 60",
                      "damage @s %d minecraft:in_fire by @e[%s,limit=1]" % (FLAME_DMG, UNIT),
                      "particle minecraft:flash{color:%d} ~ ~1 ~ 0 0 0 0 1 force" % FIRE_I,
                      "particle minecraft:flame ~ ~1 ~ 0.4 0.6 0.4 0.08 30"] + impact("~ ~1 ~", True, 3)
      + mglyph("fire", 2.2, pos="~ ~0.9 ~", kind="fireloop", life=14, billboard="vertical") + [
                      "playsound minecraft:entity.blaze.shoot hostile @a[distance=..24] ~ ~ ~ 1.2 0.6"])
    w("flame/burn", ["# 余烬（as/at 玩家）：3 秒，每秒 1", "scoreboard players remove @s rpg_mk_r 1"] + every(20, "@s rpg_mk_r") + [
        "execute if score #m %s matches 0 run damage @s 1 minecraft:on_fire" % O,
        "particle minecraft:flame ~ ~0.8 ~ 0.3 0.5 0.3 0.01 2"])
    w("flame/out", ["tag @s remove rpg.mkb.flamed", "scoreboard players reset @s rpg_mk_fl", "scoreboard players reset @s rpg_mk_fu",
                    "scoreboard players reset @s rpg_mk_r", "scoreboard players reset @s rpg_mk_ft"])

    # ---- 炽翼突进：展翼贴地冲刺 12 格，身后留下一条烧 3 秒的火路
    w("skill/dash", start("dash", 40) + ["data merge entity @s {NoAI:1b}", face()]
      + ["execute positioned ~ ~0.05 ~ run %s" % s for s in beam(FIRE_D, (0.8, 0.02, 12), (0, 0, 6), tags=("rpg.mkb.dashwarn",))]
      + fx.born(16) + say_s("烧尽。", name="炽翼突进 · ") + wingburst("~ ~1.7 ~", 6))
    w("sk/dash", [
        span(1, 13, face()),
        span(1, 13, "execute as @e[tag=rpg.mkb.dashwarn,distance=..2] positioned as @s rotated as @e[%s,limit=1] run tp @s ~ ~ ~ ~ ~" % UNIT),
        at(16, anim("roll_f")),
        at(16, "playsound minecraft:entity.phantom.flap hostile @a[distance=..32] ~ ~ ~ 1.6 0.8"),
        span(16, 21, "function %s/dash/step" % B),
        at(22, "function %s/dash/hit" % B),
        "execute if score @s rpg_mk_t matches 38.. run function %s/sk/end" % B,
    ])
    w("dash/step", [
        "# 冲两格（as/at 他）：沿途碰到的记下，身后留火",
        ground("tp @s ^ ^ ^1", "^ ^ ^1"),
        "execute at @s run function %s/dash/fire" % B,
        "execute at @s run tag @a[distance=..1.5,%s] add rpg.mkb.hit" % SURV,
        "execute at @s run " + ground("tp @s ^ ^ ^1", "^ ^ ^1"),
        "execute at @s run function %s/dash/fire" % B,
        "execute at @s run tag @a[distance=..1.5,%s] add rpg.mkb.hit" % SURV,
        "execute at @s run particle minecraft:flame ~ ~1 ~ 0.4 0.6 0.4 0.03 6",
    ])
    w("dash/fire", [fx.marker("~ ~ ~", "rpg.mkb.trail")] + fx.born(60) + mdecal("embers", 2, pos="~ ~0.06 ~", life=60)
      + fire_block("~ ~ ~", 60))
    w("dash/hit", hurt_tagged(DASH_DMG, flame=True) + fx.slash("^ ^1.2 ^1", FIRE, size=3.0) + impact("^ ^1.2 ^1", True, 3))
    w("fx/trail", ["# 火路（as/at 标记）：每 10 刻烧一下站在上面的人"] + every(3, "@s rpg_mk_life") + [
        "execute if score #m %s matches 0 run particle minecraft:flame ~ ~0.2 ~ 0.3 0.05 0.3 0.01 2" % O,
        "execute if score @s rpg_mk_life matches 50 run function %s/trail/burn" % B,
        "execute if score @s rpg_mk_life matches 30 run function %s/trail/burn" % B,
        "execute if score @s rpg_mk_life matches 10 run function %s/trail/burn" % B,
    ])
    w("trail/burn", ["execute as @a[distance=..1.1,%s] run damage @s %d minecraft:in_fire" % (SURV, TRAIL_DMG)])

    # ---- 十字斩：脚下亮一个 X，0.8 秒后两道斩痕交叉斩下
    w("skill/cross", start("cross", 36) + ["data merge entity @s {NoAI:1b}", face(), anim("rib_slash5")]
      + aimed("execute rotated as @e[%s,limit=1] rotated ~45 0 run function %s/cross/mark" % (UNIT, B)))
    w("cross/mark", ["# 十字（at 瞄准点）", fx.marker("~ ~ ~", "rpg.mkb.cross"), "execute as @e[tag=%s] run tp @s ~ ~ ~ ~ 0" % NEW]
      + fx.born(20)
      + ["execute positioned ^ ^0.05 ^-4.5 run %s" % s for s in beam(FIRE_D, (0.5, 0.02, 9), (0, 0, 4.5))] + fx.born(18)
      + ["execute rotated ~90 0 positioned ^ ^0.05 ^-4.5 run %s" % s for s in beam(FIRE_D, (0.5, 0.02, 9), (0, 0, 4.5))] + fx.born(18)
      + [fx.disp("%s/xmark" % MNS, pos="~ ~0.07 ~", scale=(6.8, 1, 6.8), color=0xFFFFFF), "tp @e[tag=%s,limit=1] ~ ~0.07 ~ ~45 0" % NEW]
      + fx.born(18) + ["playsound minecraft:block.note_block.hat hostile @a[distance=..24] ~ ~ ~ 1 1.2"])
    w("sk/cross", [
        at(17, anim("rib_slash6")),
        at(18, "execute as @e[tag=rpg.mkb.cross] at @s run function %s/cross/strike" % B),
        "execute if score @s rpg_mk_t matches 35.. run function %s/sk/end" % B,
    ])
    w("cross/strike", [
        "# 两道斩痕斩下（as/at 十字）",
        "execute positioned ^ ^0.6 ^-4.5 run function %s/cross/line" % B,
        "execute rotated ~90 0 positioned ^ ^0.6 ^-4.5 run function %s/cross/line" % B,
    ] + hurt_tagged(CROSS_DMG, flame=True)
      + ["execute positioned ^ ^0.08 ^-4.5 run %s" % s for s in beam(FIRE_I, (0.5, 0.04, 9), (0, 0, 4.5))] + fx.born(kind="crossfade")
      + ["execute rotated ~90 0 positioned ^ ^0.08 ^-4.5 run %s" % s for s in beam(FIRE_I, (0.5, 0.04, 9), (0, 0, 4.5))] + fx.born(kind="crossfade")
      + mglyph("xslash", 7, pos="~ ~1.2 ~", kind="xslash") + impact("~ ~1 ~", True, 4)
      + fx.decal("cracks", 5, 0x2A2020, pos="~ ~0.05 ~", life=60) + [
        "particle minecraft:flame ~ ~0.5 ~ 2 0.2 2 0.03 20",
        "playsound minecraft:entity.player.attack.sweep hostile @a[distance=..24] ~ ~ ~ 1.2 1.4",
        "kill @s"])
    w("cross/line", line("thin", 7))

    # ---- 天火羽雨：八个落点亮圈，1 秒后燃烧的羽毛落下
    w("skill/rain", start("rain", 44) + ["data merge entity @s {NoAI:1b}", face(), anim("showoff"),
                                          "playsound minecraft:entity.phantom.flap hostile @a[distance=..32] ~ ~ ~ 1.6 1.2"]
      + say_s("羽毛落下来了。", name="天火羽雨 · "))
    spots = ((0, 0), (2.6, 1.0), (-2.2, 2.0), (1.0, -2.6), (-2.6, -1.6), (4.2, -0.6), (-0.6, 4.2), (3.2, 3.6))
    w("rain/spots", ["execute positioned ~%s ~ ~%s run function %s/rain/one" % (dx, dz, B) for dx, dz in spots])
    w("sk/rain", aimed("function %s/rain/spots" % B)[0:0] + [
        at(4, "execute if score #w %s matches 1.. at @p[distance=..%d,%s] run function %s/rain/spots" % (O, ARENA, SURV, B)),
        at(4, "execute if score #w %s matches ..0 at @e[%s] run function %s/rain/spots" % (O, LAG, B)),
        "execute if score @s rpg_mk_t matches 43.. run function %s/sk/end" % B,
    ])
    w("rain/one", ["# 一片落羽（at 落点）", fx.marker("~ ~ ~", "rpg.mkb.rainf")] + fx.born(22)
      + fx.decal("ring", 3, FIRE_I, pos="~ ~0.06 ~", life=21) + mdecal("firering", 2.6, pos="~ ~0.07 ~", life=21) + [
        'summon minecraft:item_display ~ ~9 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.rainfeather"],'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_boss/feather"}},item_display:"none",'
        'brightness:{sky:15,block:15},teleport_duration:0,view_range:2f,transformation:{translation:[0f,0f,0f],'
        'left_rotation:[0f,0f,0.9238795f,0.3826834f],scale:[1.6f,1.6f,1.6f],right_rotation:[0f,0f,0f,1f]}}',
    ] + fx.born(24))
    w("fx/rainfeather", ["execute if score @s rpg_mk_life matches 14 run data merge entity @s {teleport_duration:12}",
                         "execute if score @s rpg_mk_life matches 14 run tp @s ~ ~-8.4 ~",
                         "execute if score @s rpg_mk_life matches 3..13 run particle minecraft:flame ~ ~0.3 ~ 0.05 0.2 0.05 0.01 1"])
    w("fx/rainf", ["execute if score @s rpg_mk_life matches 1 run function %s/rain/hit" % B])
    w("rain/hit", impact("~ ~0.6 ~", True, 2.6) + mglyph("fburn", 1.6, pos="~ ~0.8 ~", kind="fburn") + [
                   "execute as @a[distance=..1.5,%s] run damage @s %d minecraft:in_fire by @e[%s,limit=1]" % (SURV, RAIN_DMG, UNIT),
                   "particle minecraft:flame ~ ~0.3 ~ 0.6 0.1 0.6 0.04 12",
                   "playsound minecraft:item.firecharge.use hostile @a[distance=..24] ~ ~ ~ 0.8 1.2"])

    # ---- 骨柱：二阶段每 15 秒自己放一次骨刺，朝离它最近的人
    w("pillar/clock", ["# 骨柱（as/at 骨柱，二阶段）"] + every(300, "#tick %s" % O) + [
        "execute if score #m %s matches 0 positioned ~ ~-2.3 ~ facing entity @p[distance=..%d,%s] feet rotated ~ 0 run function %s/pillar/cast"
        % (O, ARENA, SURV, B)])
    w("pillar/cast", ["# 骨柱放骨刺（at 柱脚，朝目标）：先亮 1 秒裂线"]
      + ["execute positioned ~ ~0.05 ~ run %s" % s for s in beam(PEACH_I, (0.9, 0.02, 18), (0, 0, 9))] + fx.born(20)
      + [fx.marker("~ ~ ~", "rpg.mkb.walker"), "execute as @e[tag=%s] run tp @s ~ ~ ~ ~ 0" % NEW] + fx.born(37)
      + godray("~ ~ ~") + ["particle minecraft:end_rod ~ ~2.5 ~ 0.3 1.2 0.3 0.03 16",
         "playsound minecraft:block.bone_block.hit hostile @a[distance=..40] ~ ~ ~ 1.4 0.5"])
