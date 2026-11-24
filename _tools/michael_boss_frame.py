# -*- coding: utf-8 -*-
"""米迦勒战的框架：召唤、每刻、血量、显形、调度、伤害结算、切段、结算、清场、音乐、调试。"""
import os

from michael_boss_lib import *          # noqa: F401,F403
from michael_boss_lib import fx, w, ui, art, json, wj, DP


def build():
    w("load", [
        "scoreboard objectives add %s dummy" % O,
    ] + ["scoreboard objectives add %s dummy" % s for s in (
        "rpg_mk_h", "rpg_mk_c", "rpg_mk_b", "rpg_mk_n", "rpg_mk_k", "rpg_mk_cb", "rpg_mk_busy", "rpg_mk_sk", "rpg_mk_t",
        "rpg_mk_life", "rpg_mk_kd", "rpg_mk_s", "rpg_mk_dd0", "rpg_mk_v", "rpg_mk_ur", "rpg_mk_so", "rpg_mk_fl", "rpg_mk_ft",
        "rpg_mk_fu", "rpg_mk_wt", "rpg_mk_ws", "rpg_mk_r")] + [
        "scoreboard objectives add rpg_mk_dd minecraft.custom:minecraft.damage_dealt",
        "bossbar add %s \"米迦勒\"" % BAR,
        "# 粉色档的原版贴图已由教皇战改成全透明：只显示名字里的位图横幅。",
        "bossbar set %s color pink" % BAR,
        "bossbar set %s style notched_20" % BAR,
        "bossbar set %s visible false" % BAR,
        "scoreboard players set #two %s 2" % O,
        "scoreboard players set #ten %s 10" % O,
    ])

    w("summon", [
        "# 在执行位置开战。同一时间只允许一场。",
        "execute if score #fight %s matches 1 run return run tellraw @s %s" % (
            O, ui.row(ui.comp("〖米迦勒〗", PEACH, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                      ui.comp("已经有一场米迦勒战；先用 /function %s/clear 清场。" % B, ui.BROADCAST_BODY))),
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.mkb.center\"]}",
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.mkb.lag\"]}",
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.mkb.last\"]}",
        "summon minecraft:vindicator ~ ~ ~ {Tags:[\"rpg.mkb\",\"rpg.mkwear\",\"rpg.mkb.new\"],Silent:1b,PersistenceRequired:1b,"
        "DeathLootTable:\"minecraft:empty\",CustomName:{\"text\":\"米迦勒\",\"color\":\"%s\",\"bold\":true,\"italic\":false},"
        "Health:%df,active_effects:[{id:\"invisibility\",duration:-1,amplifier:0,show_particles:0b}],"
        "attributes:[{id:\"max_health\",base:%df},{id:\"attack_damage\",base:1f},{id:\"armor\",base:%df},"
        "{id:\"follow_range\",base:48f},{id:\"knockback_resistance\",base:1f},{id:\"movement_speed\",base:%gf}],"
        "drop_chances:{mainhand:0f,offhand:0f}}" % (PEACH, MAX, MAX, ARMOR1, SPEED1),
        "scoreboard players set @e[%s,tag=rpg.mkb.new] %s 1" % (UNIT, O),
        "scoreboard players set @e[%s,tag=rpg.mkb.new] rpg_mk_h %d" % (UNIT, MAX),
    ] + ["scoreboard players set @e[%s,tag=rpg.mkb.new] %s 0" % (UNIT, s)
         for s in ("rpg_mk_c", "rpg_mk_n", "rpg_mk_k", "rpg_mk_cb", "rpg_mk_sk", "rpg_mk_so", "rpg_mk_ur")] + [
        "scoreboard players set @e[%s,tag=rpg.mkb.new] rpg_mk_b 40" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.mkb.new] rpg_mk_busy 40" % UNIT,
        "tag @e[%s,tag=rpg.mkb.new] add rpg.mkb.intro" % UNIT,
        "tag @e[%s,tag=rpg.mkb.new] remove rpg.mkb.new" % UNIT,
        "scoreboard players set #fight %s 1" % O,
        "scoreboard players set #stage %s 1" % O,
        "scoreboard players set #empty %s 0" % O,
        "scoreboard players set #tick %s 0" % O,
        "scoreboard players set #w %s 0" % O,
        "execute as @a run scoreboard players operation @s rpg_mk_dd0 = @s rpg_mk_dd",
        "scoreboard players reset @a rpg_mk_fl",
        bar_title(1),
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_mk_s %d" % (UNIT, art.STEPS),
        "bossbar set %s max %d" % (BAR, MAX),
        "bossbar set %s value %d" % (BAR, MAX),
        "bossbar set %s visible true" % BAR,
        # 序章模式（#pro rpg_mk = 1，由 rpg:prologue 打开）：开场、配乐与播报交给序章的过场与字幕
        "execute unless score #pro %s matches 1 run function %s/music/1" % (O, B),
        "execute unless score #pro %s matches 1 run function %s/vfx/intro" % (O, B),
        "playsound minecraft:block.beacon.activate hostile @a[distance=..%d] ~ ~ ~ 2 0.6" % BAR_RANGE,
        "playsound minecraft:entity.phantom.flap hostile @a[distance=..%d] ~ ~ ~ 2 0.5" % BAR_RANGE,
        say("在天上就有了争战。你身上有拂晓之星的气味。", gloss="Quis ut Deus"),
    ])

    w("tick", [
        "execute unless score #fight %s matches 1 run return 0" % O,
        "execute as @e[%s] at @s run function %s/arena" % (CENTER, B),
    ])
    w("arena", [
        "# 战场（as/at 战场中心）。",
        "scoreboard players add #tick %s 1" % O,
        "execute if score #ghost %s matches 1.. run return run function %s/ghost/tick" % (O, B),
        "execute if entity @a[distance=..%d,%s] run scoreboard players set #empty %s 0" % (ARENA, SURV, O),
        "execute unless entity @a[distance=..%d,%s] run scoreboard players add #empty %s 1" % (ARENA, SURV, O),
        "execute if score #empty %s matches %d.. run return run function %s/lose" % (O, EMPTY_LIMIT, B),
        "execute unless entity @e[%s,distance=..%d] run return run function %s/lost_unit" % (UNIT, ARENA * 3, B),
        "bossbar set %s players @a[distance=..%d]" % (BAR, BAR_RANGE),
        "# 守望者：数一数；还有活着的，场上的人就「被看见」（发光）",
        "execute store result score #w %s if entity @e[%s,distance=..%d]" % (O, WATCH, ARENA * 2),
    ] + every(10, "#tick %s" % O) + [
        "execute if score #m %s matches 0 if score #w %s matches 1.. run effect give @a[distance=..%d,%s] minecraft:glowing 1 0 true" % (O, O, ARENA, SURV),
    ] + every(20, "#tick %s" % O) + [
        "# 守望者全死时，落点招式瞄的是这个标记：每秒挪到玩家那里一次（约 1 秒前的位置）",
        "execute if score #m %s matches 0 as @e[%s] at @p[distance=..%d,%s] run tp @s ~ ~ ~" % (O, LAG, ARENA, SURV),
        "execute as @e[%s,distance=..%d] at @s run function %s/unit" % (UNIT, ARENA * 3, B),
        "execute as @e[%s,distance=..%d] at @s run function %s/watch/tick" % (WATCH, ARENA * 2, B),
        "execute as @e[tag=rpg.mkb.fx,distance=..%d] at @s run function %s/fx/tick" % (ARENA * 3, B),
        "execute as @a[tag=rpg.mkb.flamed] at @s run function %s/flame/tick" % B,
        "execute if score #stage %s matches 2 as @e[tag=rpg.mkb.pillar] at @s run function %s/pillar/clock" % (O, B),
        "execute as @a[tag=rpg.mkb.pend] run function %s/hit/settle" % B,
        "execute as @a run scoreboard players operation @s rpg_mk_dd0 = @s rpg_mk_dd",
        "function %s/music/tick" % B,
    ])
    w("lost_unit", [
        "# 载体不见了：二阶段里（比如被一下打穿了死亡保护）在他最后的位置补放死亡特效再结算；否则清场。",
        "execute if score #stage %s matches 2.. run return run function %s/ghost/start" % (O, B),
        "function %s/clear" % B,
    ])
    w("unit", [
        "# 载体每刻（as/at 载体）。",
        "execute if entity @s[tag=rpg.mkb.end] run return run function %s/finale/tick" % B,
        "execute if entity @s[tag=!rpg.mkb.hp] run return run function %s/hp_init" % B,
        "# 保险：离场地中心太远或掉到下面就拉回中心；升空的招式除外",
        "execute unless entity @s[tag=rpg.mkb.air] at @e[%s] unless entity @s[distance=..36] run function %s/safety/back" % (CENTER, B),
        "execute unless entity @s[tag=rpg.mkb.air] at @e[%s] positioned ~-48 ~-80 ~-48 if entity @s[dx=96,dy=72,dz=96] run function %s/safety/back" % (CENTER, B),
        "scoreboard players operation #m %s = #tick %s" % (O, O),
        "scoreboard players set #k %s %d" % (O, STRIDE),
        "scoreboard players operation #m %s %%= #k %s" % (O, O),
        "execute if score #m %s matches 0 run function %s/read_hp" % (O, B),
        "execute if score #m %s matches 0 if score #pro %s matches 1 run function #rpg:michael_boss/prologue_hp" % (O, O),
        "execute if score @s %s matches 1 if score @s rpg_mk_h matches ..1 unless score #pro %s matches 1 run return run function %s/stage/end1" % (O, O, B),
        "execute if score @s %s matches 2 if score @s rpg_mk_h matches ..1 run return run function %s/stage/end2" % (O, B),
        "execute if entity @s[tag=rpg.mkb.morph] run return run function %s/morph/tick" % B,
        "execute if score @s rpg_mk_so matches 1.. run function %s/solid/tick" % B,
        "execute unless entity @s[tag=rpg.mkb.solid] run function %s/aura" % B,
        "scoreboard players add @s rpg_mk_c 1",
        "execute if score @s rpg_mk_sk matches 1.. run function %s/sk/tick" % B,
        "execute if score @s rpg_mk_busy matches 1.. run return run scoreboard players remove @s rpg_mk_busy 1",
        "function %s/schedule" % B,
    ])
    w("aura", ["# 灵体常驻（as/at 他）：身边慢慢上飘的白色灵光；二阶段六翼边缘飘火星"] + every(5, "#tick %s" % O) + [
        "execute if score #m %s matches 0 run particle minecraft:end_rod ~ ~1.2 ~ 0.5 0.8 0.5 0.01 1" % O,
        "execute if score #m %s matches 2 run particle minecraft:white_ash ~ ~1.4 ~ 0.6 0.8 0.6 0 3" % O,
        "execute if score @s %s matches 2 if score #m %s matches 1 run particle minecraft:flame ^ ^1.6 ^-0.6 0.9 0.5 0.2 0.01 2" % (O, O),
        "execute if score @s %s matches 2 if score #m %s matches 3 run particle %s ^ ^1.4 ^-0.5 0.8 0.6 0.2 0 2" % (O, O, FIRE_DUST),
    ])
    w("hp_init", ["tag @s add rpg.mkb.hp", "function %s/refill" % B,
                  "execute if entity @s[tag=rpg.mkb.intro] run %s" % anim("hero"),
                  "execute if score #pro %s matches 1 run function %s/look/solid" % (O, LOOK),
                  "tag @s remove rpg.mkb.intro"])
    w("safety/back", ["# 拉回场地中心（as 他）", "tp @s @e[%s]" % CENTER,
                      "execute at @s run particle %s ~ ~1 ~ 0.4 0.7 0.4 0 20" % WHITE_DUST,
                      "execute at @s run playsound minecraft:entity.phantom.flap hostile @a[distance=..32] ~ ~ ~ 1 0.6"])
    w("refill", [
        "# 补满本段血量，并补上副手的死亡保护（上一段的那件可能刚被吃掉）。",
        "attribute @s minecraft:max_health base set %d" % MAX,
        "data merge entity @s {Health:%df}" % MAX,
        "scoreboard players set @s rpg_mk_h %d" % MAX,
        "item replace entity @s weapon.offhand with %s" % GUARD_ITEM,
    ])
    step = MAX // art.STEPS
    w("read_hp", [
        "tp @e[%s] @s" % LAST,
        "execute store result score @s rpg_mk_h run data get entity @s Health 1",
        "execute store result bossbar %s value run scoreboard players get @s rpg_mk_h" % BAR,
        "execute if entity @s[tag=rpg.mkb.morph] run return 0",
        "scoreboard players operation #s %s = @s rpg_mk_h" % O,
        "scoreboard players add #s %s %d" % (O, step - 1),
        "scoreboard players set #k %s %d" % (O, step),
        "scoreboard players operation #s %s /= #k %s" % (O, O),
        "execute if score #s %s matches %d.. run scoreboard players set #s %s %d" % (O, art.STEPS + 1, O, art.STEPS),
        "execute if score #s %s matches ..-1 run scoreboard players set #s %s 0" % (O, O),
        "execute unless score #s %s = @s rpg_mk_s run function %s/bar_name" % (O, B),
    ])
    names = ["scoreboard players operation @s rpg_mk_s = #s %s" % O]
    for st in STAGES:
        names += ["execute if score @s %s matches %d if score #s %s matches %d run return run %s" % (O, st, O, k, bar_title(st, k))
                  for k in range(art.STEPS + 1)]
    w("bar_name", names)

    # ---- 显形：破绽时模型变实、灵光熄灭、可被击退，受到的伤害多一半（hit/unit）
    w("solid/on", ["# 显形（as/at 他）", "tag @s add rpg.mkb.solid", "function %s/look/solid" % LOOK,
                   "attribute @s minecraft:knockback_resistance base set 0",
                   "particle minecraft:flash{color:%d} ~ ~1.2 ~ 0 0 0 0 1 force" % PEACH_I,
                   "particle %s ~ ~1.2 ~ 0.5 0.8 0.5 0 16" % WHITE_DUST,
                   "playsound minecraft:block.beacon.deactivate hostile @a[distance=..32] ~ ~ ~ 1 1.4"])
    w("solid/tick", ["scoreboard players remove @s rpg_mk_so 1",
                     "execute if score @s rpg_mk_so matches ..0 run function %s/solid/off" % B])
    w("solid/off", ["# 恢复灵体（as 他）", "tag @s remove rpg.mkb.solid", "scoreboard players set @s rpg_mk_so 0",
                    "execute unless entity @s[tag=rpg.mkb.end] unless score #pro %s matches 1 run function %s/look/spirit" % (O, LOOK),
                    "attribute @s minecraft:knockback_resistance base set 1",
                    "execute at @s run particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.7 0.4 0.03 10"])

    # ---- 调度：普攻（一阶段每 10 刻，二阶段每 7 刻），每三次普攻接一招；大招按血线或时钟插入
    w("schedule", [
        "execute unless entity @a[distance=..%d,%s] run return 0" % (BASIC_RANGE, SURV),
        "scoreboard players remove @s rpg_mk_b 1",
        "execute if score @s rpg_mk_b matches 1.. run return 0",
        "execute if score @s %s matches 1 run scoreboard players set @s rpg_mk_b %d" % (O, GAP1),
        "execute if score @s %s matches 2 run scoreboard players set @s rpg_mk_b %d" % (O, GAP2),
        "execute if score @s rpg_mk_n matches %d.. run return run function %s/pick" % (BASICS_PER_SKILL, B),
        "execute if score @s %s matches 1 if entity @a[distance=..%s,%s] run return run function %s/basic/spine" % (O, MELEE1, SURV, B),
        "execute if score @s %s matches 2 if entity @a[distance=..%s,%s] run return run function %s/basic/rib" % (O, MELEE2, SURV, B),
        "# 拉开了：远处不出普攻，走近；太远就直接出招",
        "execute unless entity @a[distance=..%d,%s] run function %s/pick" % (FAR, SURV, B),
    ])
    pick = ["scoreboard players set @s rpg_mk_n 0", "scoreboard players set #ult %s 0" % O,
            "# 二阶段血量到 %d：只放一次的六翼燃尽" % BURN_AT,
            "execute if score @s %s matches 2 if score @s rpg_mk_h matches ..%d unless entity @s[tag=rpg.mkb.burnt] run return run function %s/ult/burn"
            % (O, BURN_AT, B)]
    for s, (_, _, ults, clock, *_r) in STAGES.items():
        for i, ln in enumerate(ults, 1):
            pick.append("execute if score @s %s matches %d if score @s rpg_mk_h matches ..%d unless entity @s[tag=rpg.mkb.u%d] "
                        "run scoreboard players set #ult %s %d" % (O, s, ln, i, O, i))
        pick.append("execute if score @s %s matches %d if score #ult %s matches 0 if score @s rpg_mk_c matches %d.. "
                    "run scoreboard players set #ult %s 9" % (O, s, O, clock, O))
    pick.append("execute if score #ult %s matches 1.. run return run function %s/ult/pick" % (O, B))
    pick.append("# 被拉开到 %d 格外：一阶段天降，二阶段炽翼突进" % FAR)
    pick.append("execute if score @s %s matches 1 unless entity @a[distance=..%d,%s] run return run function %s/skill/dive" % (O, FAR, SURV, B))
    pick.append("execute if score @s %s matches 2 unless entity @a[distance=..%d,%s] run return run function %s/skill/dash" % (O, FAR, SURV, B))
    for s, (*_h, rotation) in STAGES.items():
        n = len(rotation)
        pick.append("execute if score @s %s matches %d run scoreboard players operation #r %s = @s rpg_mk_k" % (O, s, O))
        for i, sk in enumerate(rotation):
            pick.append("execute if score @s %s matches %d if score #r %s matches %d run function %s/skill/%s" % (O, s, O, i, B, sk))
        pick.append("execute if score @s %s matches %d run scoreboard players add @s rpg_mk_k 1" % (O, s))
        pick.append("execute if score @s %s matches %d if score @s rpg_mk_k matches %d.. run scoreboard players set @s rpg_mk_k 0" % (O, s, n))
    w("pick", pick)

    upick = [
        "scoreboard players set @s rpg_mk_c 0",
        "execute if score #ult %s matches 9 run scoreboard players add @s rpg_mk_ur 1" % O,
        "execute if score #ult %s matches 9 if score @s rpg_mk_ur matches 4.. run scoreboard players set @s rpg_mk_ur 1" % O,
        "execute if score #ult %s matches 9 run scoreboard players operation #ult %s = @s rpg_mk_ur" % (O, O),
        "scoreboard players operation @s rpg_mk_ur = #ult %s" % O,
    ]
    for k in (1, 2, 3):
        upick.append("execute if score #ult %s matches %d run tag @s add rpg.mkb.u%d" % (O, k, k))
    for s, names_ in ULTS.items():
        for k, n in enumerate(names_, 1):
            upick.append("execute if score @s %s matches %d if score #ult %s matches %d run function %s/ult/%s" % (O, s, O, k, B, n))
    w("ult/pick", upick)

    w("sk/tick", ["scoreboard players add @s rpg_mk_t 1"] + [
        "execute if score @s rpg_mk_sk matches %d run return run function %s/sk/%s" % (i, B, n) for n, i in SKILL_ID.items()])
    w("sk/end", [
        "scoreboard players set @s rpg_mk_sk 0",
        "scoreboard players set @s rpg_mk_busy 0",
        "tag @s remove rpg.mkb.fold",
        "tag @s remove rpg.mkb.air",
        "data merge entity @s {NoAI:0b,NoGravity:0b,Invulnerable:0b}",
        "execute if score @s %s matches 1 run attribute @s minecraft:armor base set %d" % (O, ARMOR1),
        "execute if score @s %s matches 2 run attribute @s minecraft:armor base set %d" % (O, ARMOR2),
    ])

    # ---- 线判定：从这里沿当前朝向每 1.5 格查一次
    for kind, r in (("thin", 1.1), ("path", 1.4)):
        w("line/%s" % kind, [
            "tag @a[distance=..%s,%s] add rpg.mkb.hit" % (r, SURV),
            "scoreboard players remove #d %s 1" % O,
            "execute if score #d %s matches 1.. positioned ^ ^ ^1.5 run function %s/line/%s" % (O, B, kind),
        ])

    # ---- 打到他（as 玩家）：显形多扣一半，六翼掩面退回八成，被看见退回三成
    adv = os.path.join(DP, "data", "rpg", "advancement", "michael_boss")
    for name, tag, fn in (("hit", "rpg.mkb", "hit/player"), ("hit_watch", "rpg.mkb.w", "watch/hurt")):
        wj(os.path.join(adv, name + ".json"), {
            "criteria": {"hit": {"trigger": "minecraft:player_hurt_entity", "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this",
                 "predicate": {"type": "minecraft:vindicator", "nbt": "{Tags:[\"%s\"]}" % tag}}]}}},
            "rewards": {"function": "%s/%s" % (B, fn)}})
    pred = os.path.join(DP, "data", "rpg", "predicate", "michael_boss")
    wj(os.path.join(pred, "flee.json"), {"condition": "minecraft:random_chance", "chance": 0.3})
    wj(os.path.join(pred, "heavy.json"), {"condition": "minecraft:random_chance", "chance": 0.3})
    wj(os.path.join(pred, "grounded.json"),
       {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"flags": {"is_on_ground": True}}})
    w("hit/player", [
        "# 玩家打到了米迦勒（as 玩家）。原版在这之后才记伤害统计，所以这里只判定怎么算，下一刻再按增量结算。",
        "advancement revoke @s only rpg:michael_boss/hit",
        "scoreboard players set @s rpg_mk_v 0",
        "tag @s add rpg.mkb.att",
        "execute as @e[%s,distance=..24,limit=1,sort=nearest] at @s run function %s/hit/unit" % (UNIT, B),
        "tag @s remove rpg.mkb.att",
        "execute if score @s rpg_mk_v matches 1.. run tag @s add rpg.mkb.pend",
    ])
    w("hit/unit", [
        "# 他被打到（as/at 他；攻击者带 rpg.mkb.att）",
        "execute if entity @s[tag=rpg.mkb.end] run return 0",
        "execute if entity @s[tag=rpg.mkb.morph] run return 0",
        "execute if entity @s[tag=rpg.mkb.solid] run return run scoreboard players set @a[tag=rpg.mkb.att] rpg_mk_v 3",
        "execute if entity @s[tag=rpg.mkb.fold] run return run function %s/hit/fold" % B,
        "execute if score #w %s matches 1.. run scoreboard players set @a[tag=rpg.mkb.att] rpg_mk_v 4" % O,
    ])
    w("hit/fold", ["# 六翼合拢：这一下大半被翼挡住（as/at 他）",
                   "scoreboard players set @a[tag=rpg.mkb.att] rpg_mk_v 5",
                   "particle minecraft:end_rod ~ ~1.4 ~ 0.6 0.8 0.6 0.05 6",
                   "playsound minecraft:entity.phantom.flap hostile @a[distance=..24] ~ ~ ~ 0.8 1.6"])
    w("hit/settle", [
        "# 结算上一刻那一下（as 玩家）：增量 = 统计 - 上一刻的基准",
        "tag @s remove rpg.mkb.pend",
        "scoreboard players operation #dd %s = @s rpg_mk_dd" % O,
        "scoreboard players operation #dd %s -= @s rpg_mk_dd0" % O,
        "execute if score #dd %s matches ..0 run return 0" % O,
        "execute if score @s rpg_mk_v matches 3 as @e[%s,distance=..24,limit=1,sort=nearest] run function %s/hit/extra" % (UNIT, B),
        "execute if score @s rpg_mk_v matches 4 run scoreboard players set #f %s 3" % O,
        "execute if score @s rpg_mk_v matches 5 run scoreboard players set #f %s 8" % O,
        "execute if score @s rpg_mk_v matches 4..5 as @e[%s,distance=..24,limit=1,sort=nearest] run function %s/hit/refund" % (UNIT, B),
    ])
    w("hit/refund", [
        "# 退回这一下的 #f 成（as 他）",
        "scoreboard players operation #dd %s *= #f %s" % (O, O),
        "scoreboard players operation #dd %s /= #ten %s" % (O, O),
        "execute store result score #h %s run data get entity @s Health 10" % O,
        "scoreboard players operation #h %s += #dd %s" % (O, O),
        "execute if score #h %s matches %d.. run scoreboard players set #h %s %d" % (O, MAX * 10, O, MAX * 10),
        "execute store result entity @s Health float 0.1 run scoreboard players get #h %s" % O,
    ])
    w("hit/extra", [
        "# 显形中：这一下再多扣一半（as 他）",
        "execute store result score #h %s run data get entity @s Health 10" % O,
        "scoreboard players operation #dd %s /= #two %s" % (O, O),
        "scoreboard players operation #h %s -= #dd %s" % (O, O),
        "execute if score #h %s matches ..10 run scoreboard players set #h %s 10" % (O, O),
        "execute store result entity @s Health float 0.1 run scoreboard players get #h %s" % O,
        "execute at @s run particle minecraft:damage_indicator ~ ~1.4 ~ 0.3 0.3 0.3 0.2 6",
    ])

    # ---- 阶段切换：骨中之骨
    w("stage/end1", [
        "# 一阶段打完：骨中之骨。无敌、站定，约 6 秒后进入二阶段。",
        "function %s/refill" % B,
        "function %s/sk/end" % B,
        "function %s/solid/off" % B,
        "tag @s add rpg.mkb.morph",
        "scoreboard players set @s rpg_mk_c 0",
        "kill @e[tag=rpg.mkb.fx]",
        "data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}",
        "tp @s @e[%s]" % CENTER,
        "execute at @s run %s" % face(ARENA),
        "execute at @s run tp @s ^ ^ ^2",
        anim("kneel"),
        "bossbar set %s value %d" % (BAR, MAX),
        bar_title(1, 0),
    ])
    w("morph/tick", [
        "scoreboard players add @s rpg_mk_c 1",
        at_c(14, "execute at @e[%s] run function %s/pillar/plant" % (CENTER, B)),
        at_c(16, say("……", gloss="The Seraph", stage=2)),
        "execute if score @s rpg_mk_c matches 14..40 run particle minecraft:white_ash ~ ~1 ~ 0.5 0.6 0.5 0 3",
        at_c(40, "function %s/weapon/rib" % LOOK),
        at_c(40, anim("hero")),
        at_c(40, "function %s/vfx/seraph" % B),
        at_c(46, say("骨中之骨，肉中之肉。", gloss="Genesis 2:23", name="第二阶段 · ", stage=2)),
        at_c(110, "function %s/stage/begin2" % B),
    ])
    w("pillar/plant", [
        "# 脊骨插进场地中心（at 中心）：一根比人高的骨柱，立到战斗结束",
        'summon minecraft:item_display ~ ~2.3 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.pillar"],'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_boss/spine"}},item_display:"none",'
        'brightness:{sky:15,block:13},view_range:4f,transformation:{translation:[0f,0f,0f],'
        'left_rotation:[0f,0f,-0.9238795f,0.3826834f],scale:[4.5f,4.5f,4.5f],right_rotation:[0f,0f,0f,1f]}}',
    ] + fx.born(30000) + light_pillar(PEACH_I) + fx.decal("cracks", 5, 0x2A2020, pos="~ ~0.04 ~", life=30000)
      + fx.decal("shock_0", 8, PEACH_I, pos="~ ~0.1 ~", kind="shock") + impact("~ ~1.5 ~", False, 7)
      + fx.decal("sigil", 7, PEACH_I, pos="~ ~0.06 ~", kind="spins", life=30000) + [
        "particle minecraft:block{block_state:\"minecraft:bone_block\"} ~ ~0.5 ~ 0.8 0.3 0.8 0 40",
        "particle minecraft:flash{color:%d} ~ ~2 ~ 0 0 0 0 1 force" % PEACH_I,
        "playsound minecraft:block.bone_block.break hostile @a[distance=..48] ~ ~ ~ 2 0.5",
        "playsound minecraft:item.trident.hit_ground hostile @a[distance=..48] ~ ~ ~ 1.5 0.6",
    ])
    w("stage/begin2", [
        "tag @s remove rpg.mkb.morph",
        "tag @s remove rpg.mkb.u1",
        "tag @s remove rpg.mkb.u2",
        "tag @s remove rpg.mkb.u3",
        "scoreboard players set @s rpg_mk_ur 0",
        "data merge entity @s {NoAI:0b,Invulnerable:0b}",
        "attribute @s minecraft:armor base set %d" % ARMOR2,
        "attribute @s minecraft:movement_speed base set %g" % SPEED2,
        "scoreboard players set @s %s 2" % O,
        "scoreboard players set #stage %s 2" % O,
    ] + ["scoreboard players set @s %s 0" % s for s in ("rpg_mk_c", "rpg_mk_n", "rpg_mk_k", "rpg_mk_cb", "rpg_mk_sk")] + [
        "scoreboard players set @s rpg_mk_b 14",
        bar_title(2),
        "scoreboard players set @s rpg_mk_s %d" % art.STEPS,
        "function %s/music/2" % B,
    ])

    w("stage/end2", [
        "# 二阶段打完：两根肋骨落下，他跪在骨柱前，灵体一层层变淡、散去，留下三根实心的骨头。",
        "function %s/refill" % B,
        "function %s/sk/end" % B,
        "function %s/solid/off" % B,
        "tag @s add rpg.mkb.end",
        "scoreboard players set @s rpg_mk_c 0",
        "data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}",
        "kill @e[tag=rpg.mkb.fx,tag=!rpg.mkb.pillar]",
        "execute as @e[%s] run function %s/watch/die" % (WATCH, B),
        "execute at @e[%s] facing entity @s feet run tp @s ^ ^ ^1.8 ~ 0" % CENTER,
        "execute at @s facing entity @e[%s] feet run tp @s ~ ~ ~ ~ 0" % CENTER,
        anim("kneel"),
        "playsound minecraft:block.beacon.deactivate hostile @a[distance=..%d] ~ ~ ~ 1.4 0.6" % BAR_RANGE,
        "bossbar set %s value 0" % BAR,
        bar_title(2, 0),
    ])
    w("finale/tick", [
        "# 死亡（as/at 他）：肋骨落下、跪下、倒地，一层层变淡、散成白光，然后结算",
        "scoreboard players add @s rpg_mk_c 1",
        at_c(8, "function %s/finale/drop" % B),
        at_c(30, say("……", stage=2)),
        at_c(44, anim("fall")),
        at_c(68, anim("down")),
        at_c(70, say("……主责备你吧。", stage=2)),
        # 死亡特效（用户 2026-11-21「米迦勒没有死亡特效」：原来散开 16 刻后就结算清场，特效还没长出来就被收掉了）：
        # 光环降下、六翼一片片烧掉，天光聚拢，一闪散成白光与白鸽，最后余光落下；结算挪到 200 刻，等特效放完
        at_c(76, "function %s/vfx/death/halo" % B),
    ] + [at_c(78 + 4 * k, "function %s/wings/burn/%d" % (LOOK, k + 1)) for k in range(6)] + [
        at_c(78 + 4 * k, "function %s/vfx/death/wing" % B) for k in range(6)] + [
        at_c(100, "function %s/look/fade" % LOOK),
        "execute if score @s rpg_mk_c matches 70..130 run particle minecraft:end_rod ~ ~0.8 ~ 0.6 0.4 0.6 0.02 2",
        "execute if score @s rpg_mk_c matches 100..130 run particle minecraft:white_ash ~ ~0.8 ~ 0.7 0.4 0.7 0.02 6",
        at_c(108, "function %s/vfx/death/gather" % B),
        at_c(124, "function %s/vfx/death" % B),
    ] + [at_c(124 + 2 * k, c) for k, times in enumerate(((0, 3, 0), (0, 3, 0), (0, 3, 0), (0, 2, 14)))
         for c in full_title("flash", k, times)] + [
        at_c(128, "execute on passengers run kill @s"),
        at_c(136, "function %s/vfx/death/after" % B),
        "execute if score @s rpg_mk_c matches 130..190 run particle minecraft:end_rod ~ ~6 ~ 2.5 1.5 2.5 0 1",
        "execute if score @s rpg_mk_c matches 200.. run function %s/victory" % B,
    ])
    rib = ('summon minecraft:item_display ~ ~0.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.bones"],'
           'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_boss/rib"}},item_display:"none",'
           'brightness:{sky:15,block:12},view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0.9238795f,0.3826834f],'
           'scale:[1.4f,1.4f,1.4f],right_rotation:[0f,0f,0f,1f]}}')
    w("finale/drop", [
        "# 两根肋骨从手里落下，插在他身前（as/at 他）；手里的换成空模型",
    ] + ['execute on passengers if entity @s[tag=rpg.mkm.p.%s] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"' % p
         for p in ("rib", "rib_attack")] + [
        "execute positioned ^0.5 ^ ^1 run " + rib,
        "execute positioned ^-0.5 ^ ^1.2 run " + rib,
    ] + fx.born(30000) + [
        "playsound minecraft:block.bone_block.place hostile @a[distance=..24] ~ ~ ~ 1 0.8",
        "particle minecraft:block{block_state:\"minecraft:bone_block\"} ^ ^0.3 ^1 0.3 0.1 0.3 0 10",
    ])

    quote = ui.row(ui.comp("〖犹大书 1:9〗", ui.BROADCAST_HOLY, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                   ui.comp("天使长米迦勒……尚且不敢用毁谤的话罪责他，只说：主责备你吧！", ui.BROADCAST_NAME))
    got = ui.row(ui.comp("〖米迦勒〗", PEACH, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                 ui.comp("灵走了，骨留下来。你拾起了米迦勒脊骨与米迦勒肋骨。", ui.BROADCAST_BODY))
    w("victory", [
        "execute at @e[%s] run particle minecraft:flash{color:%d} ~ ~2 ~ 0 0 0 0 1 force" % (CENTER, PEACH_I),
        "execute at @e[%s] run particle minecraft:end_rod ~ ~4 ~ 3 3 3 0.02 60 force" % CENTER,
        "execute at @e[%s] run playsound minecraft:block.bell.resonate hostile @a[distance=..%d] ~ ~ ~ 1 0.6" % (CENTER, BAR_RANGE),
        "execute at @e[%s] run tellraw @a[distance=..%d] %s" % (CENTER, BAR_RANGE, quote),
        "# 掉落（第 9 节第 5 条）：在场的人各得米迦勒脊骨、米迦勒肋骨一把",
        "execute at @e[%s] as @a[distance=..%d,gamemode=!spectator] run function rpg:command/give/michael" % (CENTER, ARENA + 8),
        "execute at @e[%s] run tellraw @a[distance=..%d,gamemode=!spectator] %s" % (CENTER, ARENA + 8, got),
        "function %s/clear" % B,
    ])
    w("lose", [
        "execute at @e[%s] run %s" % (CENTER, say("审判已定。").replace(
            "tellraw @a[distance=..%d]" % BAR_RANGE, "tellraw @a[distance=..%d]" % (BAR_RANGE * 2))),
        "function %s/clear" % B,
    ])
    w("clear", [
        "# 清除米迦勒战的全部实体：载体与部件、守望者、骨柱与特效；血条与音乐一起收掉。",
        "tag @a remove rpg.mkb.hit",
        "tag @a remove rpg.mkb.att",
        "tag @a remove rpg.mkb.pend",
        "scoreboard players reset @a rpg_mk_fl",
        "scoreboard players reset @a rpg_mk_fu",
        "scoreboard players reset @a rpg_mk_r",
        "tag @a remove rpg.mkb.flamed",
        "execute as @e[%s] run function %s/clear_unit" % (UNIT, B),
        "execute as @e[%s] run function %s/clear_unit" % (WATCH, B),
        "kill @e[type=minecraft:marker,tag=rpg.mkb.center]",
        "kill @e[type=minecraft:marker,tag=rpg.mkb.lag]",
        "kill @e[type=minecraft:marker,tag=rpg.mkb.last]",
        "scoreboard players set #ghost %s 0" % O,
        "kill @e[tag=rpg.mkb.fx]",
        "bossbar set %s visible false" % BAR,
        "bossbar set %s players" % BAR,
    ] + ["stopsound @a record %s" % m for m in sorted({v[4] for v in STAGES.values()})] + [
        "scoreboard players set #fight %s 0" % O,
        "scoreboard players set #stage %s 0" % O,
    ])
    w("ghost/start", [
        "# 载体没走完结尾就死了（as/at 战场中心）：收掉没了坐骑的部件和守望者，在最后的位置放死亡特效",
        "tag @e[tag=rpg.mkm.part] add rpg.mkb.orph",
        "execute as @e[tag=rpg.mkm] on passengers run tag @s remove rpg.mkb.orph",
        "kill @e[tag=rpg.mkb.orph]",
        "execute as @e[%s] run function %s/watch/die" % (WATCH, B),
        "kill @e[tag=rpg.mkb.fx,tag=!rpg.mkb.pillar]",
        "bossbar set %s value 0" % BAR,
        "scoreboard players set #ghost %s 1" % O,
    ])
    w("ghost/tick", [
        "# 补放的死亡特效（as 战场中心），在最后的位置：聚光、一闪散开、余光，然后结算",
        "scoreboard players add #ghost %s 1" % O,
        "execute if score #ghost %s matches 2 at @e[%s] run function %s/vfx/death/halo" % (O, LAST, B),
        "execute if score #ghost %s matches 4 at @e[%s] run function %s/vfx/death/gather" % (O, LAST, B),
        "execute if score #ghost %s matches 20 at @e[%s] run function %s/vfx/death" % (O, LAST, B),
    ] + ["execute if score #ghost %s matches %d run %s" % (O, 20 + 2 * k, c)
         for k, times in enumerate(((0, 3, 0), (0, 3, 0), (0, 3, 0), (0, 2, 14))) for c in full_title("flash", k, times)] + [
        "execute if score #ghost %s matches 46 at @e[%s] run function %s/vfx/death/after" % (O, LAST, B),
        "execute if score #ghost %s matches 26..86 at @e[%s] run particle minecraft:end_rod ~ ~6 ~ 2.5 1.5 2.5 0 1" % (O, LAST),
        "execute as @e[tag=rpg.mkb.fx,distance=..%d] at @s run function %s/fx/tick" % (ARENA * 3, B),
        "execute if score #ghost %s matches 112.. run function %s/victory" % (O, B),
    ])
    w("clear_unit", ["execute on passengers run kill @s", "tp @s ~ -256 ~", "kill @s"])

    music = ["execute if score #pro %s matches 1 run return 0" % O, "scoreboard players remove #bgm %s 1" % O]
    for s, v in STAGES.items():
        music.append("execute if score #bgm %s matches ..0 if score #stage %s matches %d run function %s/music/%d" % (O, O, s, B, s))
        w("music/%d" % s, ["stopsound @a[distance=..%d] record %s" % (BAR_RANGE, m)
                           for m in sorted({x[4] for x in STAGES.values()})] + [
            "stopsound @a[distance=..%d] music" % BAR_RANGE,
            "execute as @a[distance=..%d] at @s run playsound %s record @s ~ ~ ~ 1 1" % (BAR_RANGE, v[4]),
            "scoreboard players set #bgm %s %d" % (O, v[5]),
        ])
    w("music/tick", music)

    w("debug/stage2", [
        "# 召唤后直接打到一阶段底线，走正常的骨中之骨进入二阶段。",
        "function %s/summon" % B,
        "tag @e[%s,limit=1,sort=nearest] add rpg.mkb.hp" % UNIT,
        "execute as @e[%s,limit=1,sort=nearest] run function %s/refill" % (UNIT, B),
        "execute as @e[%s,limit=1,sort=nearest] run data merge entity @s {Health:1f}" % UNIT,
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_mk_h 1" % UNIT,
    ])
    w("debug/ult", [
        "# 调试：下一次选招就放大招（按本段的轮换）。",
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_mk_c 99999" % UNIT,
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_mk_n %d" % (UNIT, BASICS_PER_SKILL),
    ])
    for sk in ("watch", "quis", "feather", "gaze", "dive", "fold", "dash", "cross", "rain", "spine", "rib"):
        where = "basic" if sk in ("spine", "rib") else "skill"
        w("debug/skill/%s" % sk, ["# 调试：最近的米迦勒立刻出这一招。",
                                  "execute as @e[%s,limit=1,sort=nearest] at @s run function %s/%s/%s" % (UNIT, B, where, sk)])
    for u in ULTS[1] + ULTS[2] + ["burn"]:
        w("debug/ult/%s" % u, ["# 调试：最近的米迦勒立刻放这个大招。",
                               "execute as @e[%s,limit=1,sort=nearest] at @s run function %s/ult/%s" % (UNIT, B, u)])
