# -*- coding: utf-8 -*-
"""米迦勒战的大招（每段三个）、二阶段的「六翼燃尽」与特效。"""
from michael_boss_lib import *          # noqa: F401,F403
from michael_boss_lib import fx, w, art

WHO_ROUNDS, WHO_FIRST, WHO_GAP, WHO_WARN, WHO_LEN = 3, 40, 40, 20, 30
SANCTUS_WAVES = (20, 50, 80, 88)
TRUMPET_N, TRUMPET_FIRST, TRUMPET_GAP = 7, 20, 20
BONES_FROM, BONES_LAPS_T, BONES_R, BONES_OFF = 30, 120, 10, 4
STAR_FIRST, STAR_GAP = 20, 50
BURN_FIRST, BURN_GAP = 24, 24


def window_end(t):
    """Close a big move: show the solid window, then hand back after it."""
    return [at(t, "function %s/solid/on" % B), at(t, "scoreboard players set @s rpg_mk_so %d" % SOLID_WIN),
            at(t, anim("idle")),
            "execute if score @s rpg_mk_t matches %d.. run function %s/sk/end" % (t + SOLID_WIN, B)]


def ults1():
    # ---- 谁似神？回到中心插下脊骨，骨刺沿八条放射线破土，每轮转 22.5°，共三轮
    end = WHO_FIRST + WHO_GAP * (WHO_ROUNDS - 1) + 16
    w("ult/who", start("who", end + SOLID_WIN + 2) + ["data merge entity @s {NoAI:1b}", "tp @s @e[%s]" % CENTER,
                                                       "execute at @s run function %s/who/begin" % B])
    w("who/begin", [face(ARENA), anim("mighty"),
                    say("谁似神？", gloss="Quis ut Deus", name="谁似神？ · "),
                    "playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 1.4 0.6"]
      + fx.decal("sigil", 12, PEACH_I, pos="~ ~0.06 ~", kind="spins", life=end) + fx.decal("glow", 10, PEACH_I, pos="~ ~0.05 ~", life=end)
      + light_pillar(PEACH_I) + mglyph("halo", 4.4, pos="~ ~2.2 ~", kind="haloloop", life=end) + wingburst("~ ~1.8 ~", 8))
    wh = []
    for k in range(WHO_ROUNDS):
        t_hit = WHO_FIRST + WHO_GAP * k
        wh += [at(t_hit - WHO_WARN, "function %s/who/warn%d" % (B, k)), at(t_hit, "function %s/who/strike%d" % (B, k)),
               at(t_hit, anim("slash1"))]
        yaws = [45 * i + 22.5 * k for i in range(8)]
        w("who/warn%d" % k, ["# 第 %d 轮预警（as/at 他）：八条裂线" % (k + 1)]
          + [x for y in yaws for x in ["execute rotated %s 0 positioned ~ ~0.05 ~ run %s" % (y, s) for s in
                                        beam(PEACH_I, (0.9, 0.02, WHO_LEN), (0, 0, WHO_LEN / 2.0))] + fx.born(WHO_WARN)]
          + ["playsound minecraft:block.bone_block.hit hostile @a[distance=..48] ~ ~ ~ 1 0.7"])
        w("who/strike%d" % k, ["# 第 %d 轮骨刺（as/at 他）" % (k + 1)]
          + ["execute rotated %s 0 run function %s/who/line" % (y, B) for y in yaws]
          + hurt_tagged(WHO_DMG)
          + ["playsound minecraft:block.bone_block.break hostile @a[distance=..48] ~ ~ ~ 2 0.5",
             "playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..48] ~ ~ ~ 1.4 0.6"])
    w("who/line", ["# 一条骨刺线（as/at 他，朝这条线）：沿线判定、几节骨刺、一路碎骨"]
      + ["execute positioned ~ ~0.6 ~ positioned ^ ^ ^1.5 run function %s/line/thin" % B][0:0]
      + line("thin", int(WHO_LEN / 1.5)) + [x for d in (5, 11, 17, 24) for x in ["execute positioned ^ ^ ^%d run %s" % (d, s) for s in SPIKE]]
      + ["particle minecraft:block{block_state:\"minecraft:bone_block\"} ^ ^0.4 ^%d 0.3 0.3 0.3 0 4" % d for d in range(3, WHO_LEN, 3)])
    w("sk/who", wh + [at(end - 6, anim("horn"))] + window_end(end))

    # ---- 圣哉三唱：三道齐膝高的焰墙从他身上依次向外扩散（第三道一前一后两圈）；焰墙到脚下时跳过去
    last = SANCTUS_WAVES[-1] + 60
    w("ult/sanctus", start("sanctus", last + SOLID_WIN + 2) + ["data merge entity @s {NoAI:1b}", "tp @s @e[%s]" % CENTER,
                                                                "execute at @s run %s" % face(ARENA), anim("gong")]
      + say_s("圣哉，圣哉，圣哉。", gloss="Isaiah 6:3", name="圣哉三唱 · ")
      + ["playsound minecraft:block.bell.resonate hostile @a[distance=..48] ~ ~ ~ 1.6 0.8"]
      + ["execute at @s run " + c if c.startswith("summon") else c for c in
         mglyph("halo", 4.6, pos="~ ~2.2 ~", kind="haloloop", life=last) + fx.decal("sigil", 9, PEACH_I, pos="~ ~0.06 ~", kind="spins", life=last)])
    sc_ = []
    for i, t in enumerate(SANCTUS_WAVES, 1):
        sc_ += [at(t, "function %s/sanctus/wave" % B), at(t, "scoreboard players set #wid %s %d" % (O, i)),
                at(t, "execute as @e[tag=rpg.mkb.wavenew] run scoreboard players operation @s rpg_mk_r = #wid %s" % O),
                at(t, "tag @e[tag=rpg.mkb.wavenew] remove rpg.mkb.wavenew"),
                at(t - 2, anim("gong")),
                at(t, "playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 1.4 %.1f" % (0.6 + 0.15 * i))]
    w("sk/sanctus", sc_ + [at(last, "function %s/sanctus/clear" % B)] + window_end(last))
    w("sanctus/wave", ["# 一道焰墙（as/at 他）：一个圆心标记，带波号；地上一圈往外长的火环",
                       'summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.wave","rpg.mkb.wavenew"]}',
                       "scoreboard players set @e[tag=rpg.mkb.wavenew] rpg_mk_life 61",
                       "scoreboard players set @e[tag=rpg.mkb.wavenew] rpg_mk_kd 0"]
      + mdecal("ring_t", 2, pos="~ ~0.08 ~", kind="ringgrow") + mdecal("glow_f", 3, pos="~ ~0.07 ~", kind="ringm")
      + impact("~ ~1.5 ~", False, 5)
      + ["execute rotated %d 0 run function %s/sanctus/%s" % (a, B, "flame" if a % 36 == 0 else "spoke") for a in range(0, 360, 12)])
    w("sanctus/flame", fx.glyph("fire", 2.6, "white", pos="~ ~ ~", billboard="vertical", trans=(0, 1.0, 0), tags=("rpg.mkb.spoke",),
                                born_now=False, view=4)
      + ["execute as @e[tag=%s] run tp @s ~ ~ ~ ~ 0" % NEW] + fx.born(60, "fireloop"))
    w("sanctus/spoke", ['summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.spoke"]}',
                        "execute as @e[tag=%s] run tp @s ~ ~ ~ ~ 0" % NEW] + fx.born(60))
    w("fx/spoke", ["tp @s ^ ^ ^0.508", "execute at @s run particle minecraft:flame ~ ~0.45 ~ 0.05 0.25 0.05 0 1",
                   "execute if score @s rpg_mk_kd matches 1.. run function %s/fx/kind" % B])
    w("fx/wave", [
        "# 焰墙往外走（as/at 圆心）：半径 = (61 - 生命) × 0.508；两侧各 0.7 格内、脚着地、这道墙还没烧过的人挨一下",
        "scoreboard players set #lo %s 61" % O,
        "scoreboard players operation #lo %s -= @s rpg_mk_life" % O,
        "scoreboard players set #k %s 508" % O,
        "scoreboard players operation #lo %s *= #k %s" % (O, O),
        "scoreboard players operation #hi %s = #lo %s" % (O, O),
        "scoreboard players remove #lo %s 700" % O,
        "scoreboard players add #hi %s 700" % O,
        "execute if score #lo %s matches ..-1 run scoreboard players set #lo %s 0" % (O, O),
        "execute store result storage %s wave.lo double 0.001 run scoreboard players get #lo %s" % (B, O),
        "execute store result storage %s wave.hi double 0.001 run scoreboard players get #hi %s" % (B, O),
        "execute store result storage %s wave.id int 1 run scoreboard players get @s rpg_mk_r" % B,
        "function %s/sanctus/band with storage %s wave" % (B, B),
    ])
    w("sanctus/band", ["$execute as @a[distance=$(lo)..$(hi),%s,tag=!rpg.mkb.sw$(id)] if predicate rpg:michael_boss/grounded "
                       "run function %s/sanctus/burn {id:$(id)}" % (SURV, B)])
    w("sanctus/burn", ["$tag @s add rpg.mkb.sw$(id)",
                       "damage @s %d minecraft:in_fire by @e[%s,limit=1]" % (SANCTUS_DMG, UNIT),
                       "particle minecraft:flame ~ ~0.5 ~ 0.3 0.3 0.3 0.05 10"])
    w("sanctus/clear", ["tag @a remove rpg.mkb.sw%d" % i for i in range(1, len(SANCTUS_WAVES) + 1)])

    # ---- 第七号角：飞到中心上空吹号 7 秒，每秒一道天火落在你（被看见时）或你 1 秒前的位置；最后一秒三道
    end = TRUMPET_FIRST + TRUMPET_GAP * TRUMPET_N + 10
    w("ult/trumpet", start("trumpet", end + SOLID_WIN + 2) + [
        "data merge entity @s {NoAI:1b,NoGravity:1b}", "tag @s add rpg.mkb.air", "tp @s @e[%s]" % CENTER, anim("rise")]
      + say_s("第七位天使吹号。", gloss="Revelation 11:15", name="第七号角 · ")
      + ["playsound minecraft:entity.phantom.flap hostile @a[distance=..48] ~ ~ ~ 1.6 0.6"]
      + ["execute at @e[%s] run %s" % (CENTER, c) if c.startswith("summon") else c for c in
         mdecal("seal_trumpet", 14, pos="~ ~9 ~", kind="spins", life=end) + mglyph("halo", 4.4, pos="~ ~7.4 ~", kind="haloloop", life=end)])
    tr = [span(2, 9, "tp @s ~ ~0.5 ~")]
    for k in range(TRUMPET_N):
        t = TRUMPET_FIRST + TRUMPET_GAP * k
        tr += [at(t - 2, anim("horn")), at(t, "playsound minecraft:item.goat_horn.sound.%d hostile @a[distance=..64] ~ ~ ~ 2 1" % (k % 8))]
        if k < TRUMPET_N - 1:
            tr += [x for x in (at(t, c) for c in aimed("function %s/trumpet/mark" % B))]
        else:
            tr += [x for x in (at(t, c) for c in aimed("function %s/trumpet/last" % B))]
    tr += [at(end, "tp @s @e[%s]" % CENTER), at(end, "data merge entity @s {NoGravity:0b}"), at(end, "tag @s remove rpg.mkb.air"),
           at(end, anim("land"))]
    w("sk/trumpet", tr + window_end(end + 2))
    w("trumpet/mark", ["# 天火落点（at 瞄准点）：亮 1 秒", fx.marker("~ ~ ~", "rpg.mkb.trump")] + fx.born(20)
      + fx.decal("ring", 5, FIRE_I, pos="~ ~0.06 ~", life=19) + fx.decal("glow", 5, CORAL_I, pos="~ ~0.05 ~", life=19)
      + mdecal("firering", 4.4, pos="~ ~0.07 ~", life=19))
    w("trumpet/last", ["function %s/trumpet/mark" % B, "execute positioned ^4 ^ ^ run function %s/trumpet/mark" % B,
                       "execute positioned ^-4 ^ ^ run function %s/trumpet/mark" % B])
    w("fx/trump", ["execute if score @s rpg_mk_life matches 1 run function %s/trumpet/hit" % B])
    w("trumpet/hit", ["# 天火落下（as/at 落点）：2.5 格内 %d" % TRUMPET_DMG,
                      "execute as @a[distance=..2.5,%s] run damage @s %d minecraft:in_fire by @e[%s,limit=1]" % (SURV, TRUMPET_DMG, UNIT)]
      + light_pillar(FIRE_I) + fx.decal("shock_0", 6, FIRE_I, pos="~ ~0.1 ~", kind="shock")
      + mglyph("column", 1.0, pos="~ ~ ~", kind="columnloop", life=14, billboard="vertical", start=(7.5, 15, 7.5), trans=(0, 5.8, 0))
      + impact("~ ~1 ~", True, 4.5) + fx.decal("cracks", 4, 0x2A2020, pos="~ ~0.04 ~", life=80)
      + ["particle minecraft:flame ~ ~0.4 ~ 1 0.2 1 0.05 24",
         "playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..48] ~ ~ ~ 0.6 1.4",
         "playsound minecraft:item.firecharge.use hostile @a[distance=..32] ~ ~ ~ 1.2 0.6"])


def ults2():
    # ---- 骨中之骨：两根肋骨沿两条交叉的圆弧绕场飞两圈；他在两条弧线的交点之间来回突进
    lap_end = BONES_FROM + BONES_LAPS_T
    end = lap_end + 10
    w("ult/bones", start("bones", end + SOLID_WIN + 2) + ["data merge entity @s {NoAI:1b}", "tp @s @e[%s]" % CENTER,
                                                          "execute at @s run function %s/bones/begin" % B])
    w("bones/begin", [face(ARENA), anim("showoff"),
                      say("骨中之骨。", gloss="Genesis 2:23", name="骨中之骨 · ", stage=2),
                      "playsound minecraft:entity.phantom.flap hostile @a[distance=..48] ~ ~ ~ 1.6 0.8"]
      + ['execute on passengers if entity @s[tag=rpg.mkm.p.%s] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"' % p
         for p in ("rib", "rib_attack")]
      + ["execute rotated 90 0 positioned ^ ^ ^%d run function %s/bones/orbit {side:\"a\"}" % (BONES_OFF, B),
         "execute rotated -90 0 positioned ^ ^ ^%d run function %s/bones/orbit {side:\"b\"}" % (BONES_OFF, B),
         'summon minecraft:marker ~ ~ ~%.2f {Tags:["rpg.mkb.fx","rpg.mkb.bp1"]}' % math.sqrt(BONES_R ** 2 - BONES_OFF ** 2),
         'summon minecraft:marker ~ ~ ~-%.2f {Tags:["rpg.mkb.fx","rpg.mkb.bp2"]}' % math.sqrt(BONES_R ** 2 - BONES_OFF ** 2),
         "scoreboard players set @e[tag=rpg.mkb.bp1] rpg_mk_life %d" % (end + 4),
         "scoreboard players set @e[tag=rpg.mkb.bp2] rpg_mk_life %d" % (end + 4),
         "scoreboard players set @e[tag=rpg.mkb.bp1] rpg_mk_kd 0", "scoreboard players set @e[tag=rpg.mkb.bp2] rpg_mk_kd 0"])
    w("bones/orbit", [
        "# 一条圆弧（at 圆心）：地上亮一圈，圆心标记带一根飞行的肋骨",
        "$summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.mkb.fx\",\"rpg.mkb.orb\",\"rpg.mkb.orb$(side)\"]}",
        "$scoreboard players set @e[tag=rpg.mkb.orb$(side)] rpg_mk_life %d" % (lap_end + 2),
        "$scoreboard players set @e[tag=rpg.mkb.orb$(side)] rpg_mk_kd 0",
    ] + fx.decal("ring", BONES_R * 2 + 1, FIRE_D, pos="~ ~0.06 ~", life=lap_end) + [
        '$summon minecraft:item_display ~ ~1.2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.rib","rpg.mkb.rib$(side)"],'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_boss/rib"}},item_display:"none",'
        'brightness:{sky:15,block:15},teleport_duration:1,view_range:3f,transformation:{translation:[0f,0f,0f],'
        'left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}',
        "$scoreboard players set @e[tag=rpg.mkb.rib$(side)] rpg_mk_life %d" % (lap_end + 2),
        "$scoreboard players set @e[tag=rpg.mkb.rib$(side)] rpg_mk_kd 0",
    ])
    w("fx/orb", [
        "# 圆心标记（as/at）：绕着转，带着肋骨走",
        "execute if score @s rpg_mk_life matches ..%d if entity @s[tag=rpg.mkb.orba] run tp @s ~ ~ ~ ~6 0" % BONES_LAPS_T,
        "execute if score @s rpg_mk_life matches ..%d if entity @s[tag=rpg.mkb.orbb] run tp @s ~ ~ ~ ~-6 0" % BONES_LAPS_T,
        "execute if entity @s[tag=rpg.mkb.orba] at @s positioned ^ ^1.2 ^%d as @e[tag=rpg.mkb.riba] run tp @s ~ ~ ~ ~25 0" % BONES_R,
        "execute if entity @s[tag=rpg.mkb.orbb] at @s positioned ^ ^1.2 ^%d as @e[tag=rpg.mkb.ribb] run tp @s ~ ~ ~ ~-25 0" % BONES_R,
        "execute if score @s rpg_mk_life matches ..%d if entity @s[tag=rpg.mkb.orba] at @s positioned ^ ^ ^%d run function %s/bones/cut"
        % (BONES_LAPS_T, BONES_R, B),
    ] + every(2, "@s rpg_mk_life") + [
        "execute if score #m %s matches 0 at @s positioned ^ ^1.2 ^%d run function %s/bones/trail" % (O, BONES_R, B),
        "execute if score @s rpg_mk_life matches ..%d if entity @s[tag=rpg.mkb.orbb] at @s positioned ^ ^ ^%d run function %s/bones/cut"
        % (BONES_LAPS_T, BONES_R, B),
    ])
    w("bones/trail", mglyph("tongue", 1.6, pos="~ ~ ~", kind="tongue"))
    w("bones/cut", ["# 飞行的肋骨（at 它）：1.4 格内 %d" % BONES_DMG,
                    "execute as @a[distance=..1.6,%s] run damage @s %d minecraft:mob_attack by @e[%s,limit=1]" % (SURV, BONES_DMG, UNIT),
                    "particle minecraft:flame ~ ~1.2 ~ 0.2 0.2 0.2 0.01 2",
                    "particle %s ~ ~1.2 ~ 0.2 0.2 0.2 0 1" % FIRE_DUST])
    bn = [at(BONES_FROM - 4, "tp @s @e[tag=rpg.mkb.bp1,limit=1]"),
          at(BONES_FROM - 4, "playsound minecraft:item.trident.throw hostile @a[distance=..48] ~ ~ ~ 1.4 0.6")]
    for i, t in enumerate((40, 70, 100, 130)):
        target = "rpg.mkb.bp2" if i % 2 == 0 else "rpg.mkb.bp1"
        bn += [at(t - 6, "execute facing entity @e[tag=%s,limit=1] feet run tp @s ~ ~ ~ ~ 0" % target),
               at(t - 6, "execute positioned ~ ~0.05 ~ run function %s/bones/warn" % B),
               at(t, anim("roll_f")),
               span(t, t + 9, "function %s/bones/step" % B),
               at(t + 10, anim("rib_slash4")),
               at(t + 10, "function %s/bones/hit" % B)]
    bn += [at(lap_end, "function %s/bones/catch" % B)]
    w("sk/bones", bn + window_end(end))
    w("bones/warn", beam(FIRE_D, (0.7, 0.02, 18.4), (0, 0, 9.2)) + fx.born(8))
    w("bones/step", [ground("tp @s ^ ^ ^1.84", "^ ^ ^1.84"), "execute at @s run tag @a[distance=..1.5,%s] add rpg.mkb.hit" % SURV,
                     "execute at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.02 4"])
    w("bones/hit", hurt_tagged(BONES_DASH, flame=True) + fx.slash("^ ^1.2 ^1", FIRE, size=3.0, roll=30) + impact("^ ^1.2 ^1", True, 3))
    w("bones/catch", ["# 接回肋骨（as/at 他）", "kill @e[tag=rpg.mkb.rib]", "kill @e[tag=rpg.mkb.orb]",
                      "function %s/weapon/rib" % LOOK, anim("rib_slash5"),
                      "particle minecraft:flame ~ ~1.2 ~ 0.5 0.6 0.5 0.05 16"] + wingburst("~ ~1.7 ~", 6) + impact("~ ~1.3 ~", True, 4) + [
                      "playsound minecraft:item.trident.return hostile @a[distance=..48] ~ ~ ~ 1.4 0.8"])

    # ---- 炽天使：六翼全开，6 格外的整个场地一圈一圈烧起来；他在中心不停连斩
    dur = 120
    w("ult/seraph", start("seraph", dur + 12 + SOLID_WIN + 2) + ["data merge entity @s {NoAI:1b}", "tp @s @e[%s]" % CENTER,
                                                                  "execute at @s run %s" % face(ARENA), anim("twirl")]
      + say_s("我们是燃烧者。", gloss="Seraphim", name="炽天使 · ") + ["function %s/vfx/seraph" % B]
      + ["execute at @s run " + c if c.startswith("summon") else c for c in
         mglyph("halo", 0.5, pos="~ ~2.4 ~", kind="haloin", life=dur + 10, view=5) + wingburst("~ ~1.8 ~", 11)]
      + ["execute at @s run " + c if c.startswith("summon") else c for c in
         fx.decal("glow", 12, PEACH_I, pos="~ ~0.05 ~", life=dur + 10) + fx.decal("ring", 12.4, WHITE_I, pos="~ ~0.07 ~", life=dur + 10)])
    se = [at(80, anim("twirl"))]
    se += ["execute if score @s rpg_mk_t matches 10..%d run function %s/seraph/tick" % (dur + 10, B)]
    se += [at(dur + 12, "function %s/seraph/out" % B)]
    w("sk/seraph", se + window_end(dur + 14))
    w("seraph/tick", every(20) + [
        "execute if score #m %s matches 0 as @a[distance=6..%d,%s] run damage @s %d minecraft:in_fire by @e[%s,limit=1]"
        % (O, ARENA + 4, SURV, SERAPH_FIRE, UNIT),
    ] + every(10) + [
        "execute if score #m %s matches 0 run %s" % (O, fx.disp("%s/ring_t" % MNS, pos="~ ~0.1 ~", scale=(12, 1, 12), color=0xFFFFFF)),
        "execute if score #m %s matches 0 run %s" % (O, fx.born(kind="seraphring")[0]),
        "execute if score #m %s matches 0 run %s" % (O, fx.born(kind="seraphring")[1]),
        "execute if score #m %s matches 0 run %s" % (O, fx.born(kind="seraphring")[2]),
        "execute if score #m %s matches 0 run particle minecraft:flame ~ ~0.4 ~ 16 0.3 16 0.02 80" % O,
        "execute if score #m %s matches 5 run particle %s ~ ~0.8 ~ 14 0.4 14 0 40" % (O, FIRE_DUST),
    ] + every(12) + [
        "execute if score #m %s matches 0 run function %s/seraph/slash" % (O, B),
    ] + every(20) + [
        "execute if score #m %s matches 0 run function %s/seraph/flames" % (O, B),
        "execute if score #m %s matches 10 rotated 30 0 run function %s/seraph/flames" % (O, B),
    ])
    w("seraph/flames", ["# 场上一簇簇圣焰（as/at 他）：内外两圈各六簇"]
      + [x for a in range(0, 360, 60) for d in (10, 17) for x in flame_at("^%.2f ^ ^%.2f" % (d * math.sin(math.radians(a + d * 3)), d * math.cos(math.radians(a + d * 3))), 2.6, 22)])
    w("seraph/slash", ["execute store result score #r %s run random value 1..6" % O]
      + ["execute if score #r %s matches %d run %s" % (O, i, anim("rib_slash%d" % i)) for i in range(1, 7)]
      + [face(6), "tag @a[distance=..3.5,%s] add rpg.mkb.hit" % SURV] + hurt_tagged(RIB_DMG, flame=True)
      + fx.slash("^ ^1.3 ^1.5", FIRE, size=2.4))
    w("seraph/out", ["# 火灭（as/at 他）"] + smoke_puff("~ ~1 ~", 5) + ["particle minecraft:large_smoke ~ ~0.5 ~ 14 0.3 14 0.02 60",
                     "playsound minecraft:block.fire.extinguish hostile @a[distance=..48] ~ ~ ~ 1.4 0.6"])

    # ---- 三分之一的星辰：升空；场地分三个 120° 扇区，你所在的扇区先亮红，三轮顺时针；最后一颗大星砸在中心
    big_warn = STAR_FIRST + STAR_GAP * 3
    big_hit = big_warn + 20
    end = big_hit + 6
    w("ult/stars", start("stars", end + SOLID_WIN + 2) + [
        "data merge entity @s {NoAI:1b,NoGravity:1b}", "tag @s add rpg.mkb.air", "tp @s @e[%s]" % CENTER, anim("rise")]
      + say_s("三分之一的星辰，从天上坠落。", gloss="Revelation 12:4", name="三分之一的星辰 · ")
      + ["function %s/stars/which" % B])
    which = ["# 你在哪个扇区（as 他）：扇区 j = 方位 [120j, 120j+120)",
             "scoreboard players set #sec %s 0" % O,
             "tag @a remove rpg.mkb.aim",
             "execute at @e[%s] run tag @p[distance=..%d,%s] add rpg.mkb.aim" % (CENTER, ARENA, SURV)]
    for j in range(3):
        which.append("execute at @e[%s] rotated %d 0 positioned ^ ^ ^100 if entity @a[tag=rpg.mkb.aim,distance=..100] at @e[%s] rotated %d 0 "
                     "positioned ^ ^ ^100 if entity @a[tag=rpg.mkb.aim,distance=..100] run scoreboard players set #sec %s %d"
                     % (CENTER, 120 * j + 90, CENTER, 120 * j + 30, O, j))
    which.append("tag @a remove rpg.mkb.aim")
    which.append("scoreboard players operation @s rpg_mk_r = #sec %s" % O)
    w("stars/which", which)
    st = [span(2, 11, "tp @s ~ ~0.5 ~")]
    for k in range(3):
        tw, th = STAR_FIRST + STAR_GAP * k, STAR_FIRST + STAR_GAP * k + 30
        for j in range(3):
            # 第 k 轮亮的是 (起始扇区 + k) % 3
            cond = "execute if score @s rpg_mk_r matches %d" % ((j - k) % 3)
            st += [at(tw, "%s at @e[%s] run function %s/stars/warn%d" % (cond, CENTER, B, j)),
                   span(tw + 12, th - 2, "%s at @e[%s] run function %s/stars/meteor%d" % (cond, CENTER, B, j)),
                   at(th, "%s at @e[%s] run function %s/stars/hit%d" % (cond, CENTER, B, j))]
        st.append(at(tw, anim("horn")))
    for j in range(3):
        a0 = 120 * j
        w("stars/warn%d" % j, ["# 扇区 %d 亮红（at 中心）" % j]
          + ["execute rotated %d 0 positioned ~ ~0.05 ~ run %s" % (a, s) for a in (a0, a0 + 120) for s in beam(FIRE_I, (0.4, 0.02, 30), (0, 0, 15))]
          + fx.born(30)
          + [fx.disp("%s/wedge" % MNS, pos="~ ~0.06 ~", scale=(62, 1, 62), color=0xFFFFFF, view=6),
             # 展示实体的模型朝向和生物相反：贴图朝南展开的扇形，偏航 φ 时朝 φ+180 的方向展开
             "tp @e[tag=%s,limit=1] ~ ~0.06 ~ %d 0" % (NEW, a0 + 60 + 180)] + fx.born(30)
          + ["playsound minecraft:block.note_block.bass hostile @a[distance=..48] ~ ~ ~ 1.4 0.5"])
        w("stars/meteor%d" % j, ["# 一颗流星（at 中心）：扇区里随机一点",
                                 "execute store result storage %s star.a int 1 run random value %d..%d" % (B, a0 + 5, a0 + 115),
                                 "execute store result storage %s star.d int 1 run random value 3..30" % B,
                                 "function %s/stars/fall with storage %s star" % (B, B)])
        hit = ["# 扇区 %d 落下（at 中心）：扇区里的人各 %d" % (j, STAR_DMG)]
        hit.append("execute rotated %d 0 positioned ^ ^ ^100 as @a[distance=..100,%s] at @e[%s] rotated %d 0 positioned ^ ^ ^100 "
                   "if entity @s[distance=..100] run damage @s %d minecraft:in_fire by @e[%s,limit=1]"
                   % (a0 + 90, SURV, CENTER, a0 + 30, STAR_DMG, UNIT))
        hit += ["playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1.2 0.8"]
        w("stars/hit%d" % j, hit)
    w("stars/fall", ["$execute rotated $(a) 0 positioned ^ ^ ^$(d) positioned over motion_blocking_no_leaves run function %s/stars/one" % B])
    w("stars/one", fx.glyph("meteor", 3.2, "white", pos="~ ~14 ~", billboard="vertical", trans=(0, 1.0, 0), tags=("rpg.mkb.meteor",),
                            born_now=False, tpd=0, view=4) + fx.born(14, "meteorloop"))
    w("fx/meteor", ["execute if score @s rpg_mk_life matches 13 run data merge entity @s {teleport_duration:10}",
                    "execute if score @s rpg_mk_life matches 13 run tp @s ~ ~-13.6 ~",
                    "execute if score @s rpg_mk_life matches 3..12 run particle minecraft:flame ~ ~0.4 ~ 0.1 0.3 0.1 0.02 2",
                    "execute if score @s rpg_mk_life matches 2 run function %s/stars/land" % B,
                    "execute if score @s rpg_mk_life matches 2 run particle minecraft:flame ~ ~0.2 ~ 0.6 0.1 0.6 0.05 10",
                    "function %s/fx/kind" % B])
    w("stars/land", mglyph("burstf", 2.6, pos="~ ~0.6 ~", kind="burstf"))
    st += [at(big_warn, "execute at @e[%s] run function %s/stars/bigwarn" % (CENTER, B)),
           at(big_warn, say("……最后一颗。", stage=2)),
           at(big_hit, "execute at @e[%s] run function %s/stars/bighit" % (CENTER, B)),
           at(end, "tp @s @e[%s]" % CENTER), at(end, "data merge entity @s {NoGravity:0b}"), at(end, "tag @s remove rpg.mkb.air"),
           at(end, anim("land"))]
    w("sk/stars", st + window_end(end + 2))
    w("stars/bigwarn", ["# 大星预警（at 中心）：5 格"] + fx.decal("ring", 10, FIRE_I, pos="~ ~0.06 ~", life=20)
      + fx.decal("glow", 10, FIRE_D, pos="~ ~0.05 ~", life=20) + mdecal("firering", 9, pos="~ ~0.07 ~", life=20)
      + fx.glyph("meteor", 11, "white", pos="~ ~24 ~", billboard="vertical", trans=(0, 3.0, 0), tags=("rpg.mkb.bigstar",),
                 born_now=False, tpd=0, view=8) + fx.born(22, "meteorloop") + ["playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 1.4 0.5"])
    w("fx/bigstar", ["execute if score @s rpg_mk_life matches 20 run data merge entity @s {teleport_duration:18}",
                     "execute if score @s rpg_mk_life matches 20 run tp @s ~ ~-22 ~",
                     "particle minecraft:flame ~ ~1 ~ 0.6 0.6 0.6 0.03 6", "function %s/fx/kind" % B])
    w("stars/bighit", ["# 大星砸地（at 中心）：5 格内 %d" % STAR_BIG,
                       "execute as @a[distance=..5,%s] run damage @s %d minecraft:in_fire by @e[%s,limit=1]" % (SURV, STAR_BIG, UNIT)]
      + fx.decal("shock_0", 14, FIRE_I, pos="~ ~0.1 ~", kind="shock") + fx.decal("cracks", 9, 0x1A1010, pos="~ ~0.04 ~", life=100)
      + impact("~ ~1.5 ~", True, 10) + godray("~ ~ ~", True) + wingburst("~ ~2 ~", 12) + feathers_out("~ ~1.4 ~", 8)
      + wave("minecraft:flame", 32, 0.6, y=0.4) + [
        "particle minecraft:flash{color:%d} ~ ~1 ~ 0 0 0 0 1 force" % FIRE_I,
        "playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1.6 0.5"])

    # ---- 六翼燃尽（二阶段血量 150，只一次）：四周变白，他升空扑击六次，每扑一次烧掉一片翼；最后无翼落地跪倒
    last = BURN_FIRST + BURN_GAP * 6
    w("ult/burn", start("burn", last + 64) + [
        "tag @s add rpg.mkb.burnt", "data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:1b}", "tag @s add rpg.mkb.air",
        "tp @s @e[%s]" % CENTER, anim("rise"),
    ] + full_title("flash", 0, (2, 6, 20)) + [
        "execute as @e[tag=rpg.mkb.pillar] at @s run %s" % light_pillar(WHITE_I)[0],
        say("谁似神？", gloss="Quis ut Deus", name="六翼燃尽 · ", stage=2),
        "playsound minecraft:block.beacon.activate hostile @a[distance=..48] ~ ~ ~ 2 0.5",
        "playsound minecraft:entity.phantom.flap hostile @a[distance=..48] ~ ~ ~ 2 0.4",
    ] + fx.born(kind="pillarfade"))
    bu = [span(2, 12, "tp @s ~ ~0.5 ~")]
    for k in range(6):
        t = BURN_FIRST + BURN_GAP * k
        bu += [at(t, c) for c in aimed("function %s/burn/mark" % B)]
        bu += [at(t + 12, "execute at @e[tag=rpg.mkb.burnto,limit=1] run tp @s ~ ~5 ~"),
               at(t + 12, anim("roll_f")),
               at(t + 16, "execute at @e[tag=rpg.mkb.burnto,limit=1] run tp @s ~ ~ ~"),
               at(t + 16, anim("land")),
               at(t + 17, "function %s/burn/hit" % B),
               at(t + 17, "function %s/wings/burn/%d" % (LOOK, k + 1)),
               at(t + 20, "tp @s ~ ~4 ~")]
    bu += [at(last, "tp @s @e[%s]" % CENTER), at(last, "data merge entity @s {NoGravity:0b,Invulnerable:0b}"),
           at(last, "tag @s remove rpg.mkb.air"), at(last + 2, anim("kneel")),
           at(last + 2, "attribute @s minecraft:armor base set 0"),
           at(last + 2, "function %s/solid/on" % B), at(last + 2, "scoreboard players set @s rpg_mk_so 60"),
           at(last + 6, say("……", stage=2)),
           "execute if score @s rpg_mk_t matches %d.. run function %s/sk/end" % (last + 62, B)]
    w("sk/burn", bu)
    w("burn/mark", ["# 扑击落点（at 瞄准点）", "kill @e[tag=rpg.mkb.burnto]", fx.marker("~ ~ ~", "rpg.mkb.burnto")] + fx.born(20)
      + fx.decal("ring", 6, WHITE_I, pos="~ ~0.06 ~", life=17) + fx.decal("glow", 6, FIRE_I, pos="~ ~0.05 ~", life=17)
      + fx.decal("sigil", 5.5, PEACH_I, pos="~ ~0.07 ~", kind="spinf", life=17)
      + ["playsound minecraft:block.note_block.bell hostile @a[distance=..48] ~ ~ ~ 1.2 1.8"])
    w("burn/hit", ["# 扑下（as/at 他）：3 格内 %d；一片翼化作火羽散开" % BURN_DMG, "tag @a[distance=..3,%s] add rpg.mkb.hit" % SURV]
      + hurt_tagged(BURN_DMG) + fx.decal("shock_0", 7, WHITE_I, pos="~ ~0.1 ~", kind="shock")
      + wingburst("~ ~1.8 ~", 8) + feathers_out("~ ~1.8 ~", 8) + impact("~ ~1.2 ~", True, 5)
      + fx.decal("cracks", 5, 0x2A2020, pos="~ ~0.04 ~", life=80) + [
        "particle minecraft:flame ~ ~1.6 ~ 0.8 0.6 0.8 0.08 40",
        "particle minecraft:end_rod ~ ~1.6 ~ 0.8 0.6 0.8 0.08 20",
        "particle minecraft:flash{color:%d} ~ ~1.5 ~ 0 0 0 0 1 force" % FIRE_I,
        "playsound minecraft:entity.phantom.flap hostile @a[distance=..48] ~ ~ ~ 1.6 0.6",
        "playsound minecraft:item.firecharge.use hostile @a[distance=..48] ~ ~ ~ 1.4 0.6"])


def vfx():
    w("vfx/intro", ["# 登场（as/at 战场中心）：天光、灵光环"]
      + light_pillar(PEACH_I) + fx.decal("ring", 2, PEACH_I, pos="~ ~0.08 ~", kind="ringx")
      + fx.decal("sigil", 9, PEACH_I, pos="~ ~0.06 ~", kind="spinf", life=40) + wingburst("~ ~2 ~", 9)
      + [x for k in range(4) for x in mglyph("dove", 1.4, pos="^%.1f ^1.5 ^%.1f" % (2 * math.cos(k * 1.57), 2 * math.sin(k * 1.57)),
                                              kind="doverise", life=50)]
      + wave("minecraft:end_rod", 20, 0.3, y=1.2) + ["particle minecraft:flash{color:%d} ~ ~1.5 ~ 0 0 0 0 1 force" % PEACH_I])
    w("vfx/blink", ["# 守望者传送（at 它）：一团黑烟，一只眼睛睁开；不用末影人的紫色粒子（用户 2026-11-21）"] + smoke_puff("~ ~1.4 ~", 2.6)
      + mglyph("eye", 1.6, pos="~ ~2.6 ~", kind="eyeopen") + [
                    "particle minecraft:large_smoke ~ ~1.4 ~ 0.3 0.8 0.3 0.02 10",
                    "particle minecraft:flame ~ ~2.4 ~ 0.3 0.3 0.3 0.01 4",
                    "playsound minecraft:entity.enderman.teleport hostile @a[distance=..32] ~ ~ ~ 1 0.8"])
    w("vfx/wings", ["# 六翼全展（as/at 他）"] + wave("minecraft:end_rod", 16, 0.25, y=1.8) + wingburst("~ ~1.8 ~", 8)
      + ["particle %s ^ ^1.8 ^-0.6 1.6 0.8 0.3 0 20" % WHITE_DUST,
         "playsound minecraft:entity.phantom.flap hostile @a[distance=..40] ~ ~ ~ 1.6 0.7"])
    w("vfx/seraph", ["# 六翼燃起（as/at 他）"] + wave("minecraft:flame", 24, 0.3, y=1.6) + wingburst("~ ~1.8 ~", 9)
      + feathers_out("~ ~1.8 ~", 8) + godray("~ ~ ~", True)
      + fx.decal("ring", 2, FIRE_I, pos="~ ~0.08 ~", kind="ringm")
      + ["particle minecraft:flame ^ ^1.7 ^-0.6 1.6 0.8 0.3 0.04 40",
         "particle minecraft:flash{color:%d} ~ ~1.6 ~ 0 0 0 0 1 force" % FIRE_I,
         "playsound minecraft:entity.blaze.shoot hostile @a[distance=..40] ~ ~ ~ 1.4 0.6",
         "playsound minecraft:item.firecharge.use hostile @a[distance=..40] ~ ~ ~ 1.2 0.5"])
    # ---- 死亡（用户 2026-11-21「米迦勒没有死亡特效」）。finale/tick 的时间线：76 光环降下、地上圣印转起来；
    # 78..98 六翼一片片烧掉（每片一团火羽）；108 天光聚拢；124 一闪散开（全屏白光、光柱、白鸽、羽毛、冲击环）；
    # 136 余光落下；200 结算。载体意外死掉时 ghost/tick 在他最后的位置补放同一套。
    w("vfx/death/halo", ["# 光环降下（at 他）：头顶的光环长出来，脚下的炽天使圣印慢慢转，一圈白光向外推"]
      + mglyph("halo", 0.5, pos="~ ~3.3 ~", kind="halodeath")
      + fx.decal("sigil", 7, PEACH_I, pos="~ ~0.06 ~", kind="spins", life=124)
      + fx.decal("glow", 6, PEACH_I, pos="~ ~0.05 ~", life=124)
      + fx.decal("ring", 2, PEACH_I, pos="~ ~0.08 ~", kind="ringgrow")
      + wave("minecraft:end_rod", 16, 0.12, y=0.3)
      + ["playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 1.2 0.6",
         "playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..48] ~ ~ ~ 1 0.5"])
    w("vfx/death/wing", ["# 烧掉一片翼（as/at 他）：背后一团火、几根火羽"]
      + mglyph("fburn", 2.2, pos="^ ^1.9 ^-0.5", kind="fburn") + feathers_out("^ ^1.9 ^-0.5", 2)
      + ["particle minecraft:flame ^ ^1.9 ^-0.5 0.7 0.5 0.2 0.04 14",
         "particle minecraft:white_ash ^ ^1.9 ^-0.5 0.9 0.6 0.3 0 12",
         "playsound minecraft:item.firecharge.use hostile @a[distance=..40] ~ ~ ~ 0.8 0.7"])
    w("vfx/death/gather", ["# 天光聚拢（at 他）：一道天光落下，光点往他身上收"]
      + godray("~ ~ ~") + mglyph("column", 3.2, pos="~ ~1.6 ~", kind="columnloop", billboard="vertical")
      + [x for k in range(6) for x in mglyph("star", 0.9, pos="^%.1f ^%.1f ^%.1f" % (
          2.2 * math.cos(k * 1.05), 1.0 + 0.4 * (k % 3), 2.2 * math.sin(k * 1.05)), kind="twinkle", start=0.01)]
      + ["particle minecraft:end_rod ~%.2f ~1.2 ~%.2f %.3f 0 %.3f 0.18 0 force" % (
          3.6 * math.cos(a), 3.6 * math.sin(a), -math.cos(a), -math.sin(a)) for a in [k * math.pi / 12 for k in range(24)]]
      + ["playsound minecraft:block.beacon.ambient hostile @a[distance=..48] ~ ~ ~ 1.6 1.4",
         "playsound minecraft:block.bell.resonate hostile @a[distance=..48] ~ ~ ~ 1 1.2"])
    w("vfx/death", ["# 散开（as/at 他）：一闪，光柱、白鸽升起、羽毛四散，冲击环推开"]
      + light_pillar(PEACH_I) + godray("~ ~ ~")
      + fx.decal("ring", 2, PEACH_I, pos="~ ~0.06 ~", kind="ringx")
      + fx.decal("shock_0", 9, PEACH_I, pos="~ ~0.1 ~", kind="shock")
      + wingburst("~ ~1.8 ~", 11) + impact("~ ~1.4 ~", False, 7) + feathers_out("~ ~1.6 ~", 8)
      + [x for k in range(8) for x in mglyph("dove", 1.6, pos="^%.1f ^%.1f ^%.1f" % (
          1.6 * math.cos(k * 0.785), 0.8 + 0.25 * k, 1.6 * math.sin(k * 0.785)), kind="doverise")]
      + wave("minecraft:end_rod", 32, 0.32, y=1.0) + wave("minecraft:white_ash", 24, 0.2, y=0.4)
      + ["particle minecraft:flash{color:%d} ~ ~1.2 ~ 0 0 0 0 1 force" % WHITE_I,
         "particle minecraft:end_rod ~ ~1.4 ~ 0.4 0.8 0.4 0.25 60 force",
         "playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..48] ~ ~ ~ 1.6 0.6",
         "playsound minecraft:block.beacon.deactivate hostile @a[distance=..48] ~ ~ ~ 1.4 0.8",
         "playsound minecraft:entity.phantom.flap hostile @a[distance=..48] ~ ~ ~ 1.6 0.6"])
    w("vfx/death/after", ["# 余光（at 他原来站的地方）：再推开一圈淡光，光点从天上慢慢落下"]
      + fx.decal("ring", 2, WHITE_I, pos="~ ~0.07 ~", kind="ringx")
      + [x for k in range(3) for x in mglyph("dove", 1.2, pos="^%.1f ^2.4 ^%.1f" % (
          1.0 * math.cos(k * 2.09 + 0.5), 1.0 * math.sin(k * 2.09 + 0.5)), kind="doverise")]
      + ["particle minecraft:end_rod ~ ~5 ~ 3 1 3 0.01 40",
         "playsound minecraft:block.bell.resonate hostile @a[distance=..48] ~ ~ ~ 0.8 0.8"])
