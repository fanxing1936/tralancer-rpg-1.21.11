# -*- coding: utf-8 -*-
"""最终 Boss 路西法（docs/LUCIFER-BOSS-DESIGN.md）。只用指令召唤，规格对齐教皇战。

这里只管战斗的外壳：召唤、载体、血量分段、出招调度、大招血线、阶段切换、
血条、音乐、失败重置和清场。招式本身复用 add_lucifer_fight.py 的时间线
（rpg:lucifer_fight/ 下的一阶段 p1/ 与二阶段招式），外观复用两套 GPT 模型。

和七罪恶魔领主路西法是两个 Boss：载体挂 rpg.lub，不挂 rpg.advent，
所以不走十分钟寿命、驱魔系统和罪证。为了让两套外观认出它，载体带 rpg_dm_lord=1。

血量每段一池，各 1000：原版卫道士的最大生命上限是 1024，装不下几段的总和。
切阶段时补满。副手放一件隐形的、带死亡保护组件的物品，致命一击会被它吃掉、
载体剩 1 血，再由阶段切换接手；所以一刀打过头也不会真的死，也不会跨段。

读载体血量要序列化它身上的全部乘客（二阶段有 102 个部件），所以每 4 刻读一次。
"""

import os
import sys

import json

import add_lucifer_boss_art as art
import rpg_ui_style as ui
from display_mob import hook_tag, wf

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "lucifer_boss")
B = "rpg:lucifer_boss"
FIGHT = "rpg:lucifer_fight"
O = "rpg_lub"

ARENA = 40
BAR_RANGE = 48
EMPTY_LIMIT = 1200          # 战场里没人满 60 秒判负清场
STRIDE = 4
CAST_RANGE = 16
CAST_CD = 70

STAGES = {
    # 段号: (名称, 本段血量, 本段底线, 大招血线（本段内）, 大招时钟, 音乐, 音乐长度, 血条颜色)
    1: ("晨星之蛇", 1000, 1, (625, 375), 900, "boss2", 1876, "green"),
    2: ("知善恶树", 1000, 1, (667, 333), 1200, "boss1", 2943, "green"),
}
MAX = 1000
GUARD = ('minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]')
FINALE_TICKS = 60
UNIT = "type=minecraft:vindicator,tag=rpg.lub"
SURV = "gamemode=!spectator,gamemode=!creative"


def w(path, lines):
    wf(os.path.join(OUT, *path.split("/")) + ".mcfunction", lines)


def say(text, gloss=False, name=None):
    """〖路西法〗 播报（ART-STYLE.md §12）。"""
    parts = [ui.comp("%s路西法%s" % ui.BRACKETS, ui.pillar_mid(1), True)]
    if gloss:
        parts.append(ui.comp(" " + ui.fraktur("Lucifer"), ui.BROADCAST_GLOSS))
    parts.append(ui.comp(ui.GAP, ui.BROADCAST_BODY))
    if name:
        parts.append(ui.comp(name, ui.BROADCAST_NAME))
    parts.append(ui.comp(text, ui.BROADCAST_BODY))
    return "tellraw @a[distance=..%d] %s" % (BAR_RANGE, ui.row(*parts))


def bar_name(stage, step=art.STEPS):
    """血条名字是一整张位图横幅（原版条已隐藏），见 add_lucifer_boss_art.py。"""
    return "bossbar set rpg:lucifer_boss name %s" % json.dumps(
        {"text": art.bar_text(stage, step), "font": art.FONT}, ensure_ascii=True, separators=(",", ":"))


def build():
    w("load", [
        "scoreboard objectives add %s dummy" % O,
        "scoreboard objectives add rpg_lub_h dummy",
        "scoreboard objectives add rpg_lub_c dummy",
        "scoreboard objectives add rpg_lub_s dummy",
        "bossbar add rpg:lucifer_boss \"路西法\"",
        "# 粉色档的原版贴图已由教皇战改成全透明：只显示名字里的位图横幅。",
        "bossbar set rpg:lucifer_boss color pink",
        "bossbar set rpg:lucifer_boss style notched_10",
        "bossbar set rpg:lucifer_boss visible false",
    ])

    # ---- 召唤
    w("summon", [
        "# 在执行位置开战。同一时间只允许一场。",
        "execute if score #fight %s matches 1 run return run tellraw @s %s" % (
            O, ui.row(ui.comp("〖路西法〗", ui.pillar_mid(1), True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                      ui.comp("已经有一场路西法战；先用 /function %s/clear 清场。" % B, ui.BROADCAST_BODY))),
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.lub.center\"]}",
        "summon minecraft:vindicator ~ ~1 ~ {Tags:[\"rpg.lub\",\"rpg.demon\",\"rpg.lub.new\"],Silent:1b,PersistenceRequired:1b,"
        "CustomName:[{\"text\":\"[最终]\",\"color\":\"%s\",\"bold\":true,\"italic\":false},{\"text\":\"路西法\",\"color\":\"%s\",\"bold\":false,\"italic\":false}],"
        "Health:%df,active_effects:[{id:\"invisibility\",duration:-1,amplifier:0,show_particles:0b},{id:\"speed\",duration:-1,amplifier:1,show_particles:0b}],"
        "attributes:[{id:\"max_health\",base:%df},{id:\"attack_damage\",base:11f},{id:\"attack_knockback\",base:2f},{id:\"armor\",base:8f},"
        "{id:\"follow_range\",base:48f},{id:\"knockback_resistance\",base:0.5f}],drop_chances:{mainhand:0f,offhand:0f}}"
        % (ui.pillar(1)["lit"], ui.pillar(1)["lit"], MAX, MAX),
        "scoreboard players set @e[%s,tag=rpg.lub.new] rpg_lub_h %d" % (UNIT, MAX),
        "scoreboard players set @e[%s,tag=rpg.lub.new] rpg_dm_lord 1" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.lub.new] %s 1" % (UNIT, O),
        "scoreboard players set @e[%s,tag=rpg.lub.new] rpg_lub_c 0" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.lub.new] rpg_dm_cd 60" % UNIT,
        "tag @e[%s,tag=rpg.lub.new] remove rpg.lub.new" % UNIT,
        "scoreboard players set #fight %s 1" % O,
        "scoreboard players set #stage %s 1" % O,
        "scoreboard players set #empty %s 0" % O,
        "scoreboard players set #tick %s 0" % O,
        bar_name(1),
        "bossbar set rpg:lucifer_boss max %d" % STAGES[1][1],
        "bossbar set rpg:lucifer_boss value %d" % STAGES[1][1],
        "bossbar set rpg:lucifer_boss visible true",
        "function %s/music/1" % B,
        "particle %s ~ ~1 ~ 1 1.5 1 0.05 80 force" % ui.pillar_transition(1, 2.6),
        "playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..%d] ~ ~ ~ 1.2 0.5" % BAR_RANGE,
        say("我是晨星，是早晨之子。你们的神给了我光，又把我摔下天来。", gloss=True),
    ])

    # ---- 每刻
    w("tick", [
        "execute unless score #fight %s matches 1 run return 0" % O,
        "execute as @e[type=minecraft:marker,tag=rpg.lub.center,limit=1] at @s run function %s/arena" % B,
    ])
    w("arena", [
        "# 战场（as/at 战场中心）。",
        "scoreboard players add #tick %s 1" % O,
        "execute if entity @a[distance=..%d,%s] run scoreboard players set #empty %s 0" % (ARENA, SURV, O),
        "execute unless entity @a[distance=..%d,%s] run scoreboard players add #empty %s 1" % (ARENA, SURV, O),
        "execute if score #empty %s matches %d.. run return run function %s/lose" % (O, EMPTY_LIMIT, B),
        "execute unless entity @e[%s,distance=..%d] run return run function %s/lost_unit" % (UNIT, ARENA * 3, B),
        "bossbar set rpg:lucifer_boss players @a[distance=..%d]" % BAR_RANGE,
        "execute as @e[%s,distance=..%d] at @s run function %s/unit" % (UNIT, ARENA * 3, B),
        "function %s/music/tick" % B,
    ])
    w("lost_unit", [
        "# 载体不见了：二阶段里被一击打穿底线时也会这样，按胜利结算；否则清场。",
        "execute if score #stage %s matches 2.. run return run function %s/victory" % (O, B),
        "function %s/clear" % B,
    ])

    stage_checks = []
    for s, (name, hp, floor, ults, clock, _, _, _) in STAGES.items():
        stage_checks.append("execute if score @s %s matches %d if score @s rpg_lub_h matches ..%d run return run function %s/stage/end%d"
                            % (O, s, floor, B, s))
    w("unit", [
        "# 载体每刻（as/at 载体）。",
        "execute if entity @s[tag=rpg.lub.end] run return run function %s/finale/tick" % B,
        "# 召唤 NBT 里的 Health 先于属性生效、被原版上限截断；到载体的第一刻再补满（同 inquest/init_health）。",
        "execute if entity @s[tag=!rpg.lub.hp] run return run function %s/hp_init" % B,
        "execute if score #tick %s matches 0 run function %s/read_hp" % (O, B),
        "scoreboard players operation #m %s = #tick %s" % (O, O),
        "scoreboard players set #k %s %d" % (O, STRIDE),
        "scoreboard players operation #m %s %%= #k %s" % (O, O),
        "execute if score #m %s matches 0 run function %s/read_hp" % (O, B),
    ] + stage_checks + [
        "function %s/tick" % FIGHT,
        "scoreboard players add @s rpg_lub_c 1",
        "function %s/schedule" % B,
    ])
    w("hp_init", [
        "tag @s add rpg.lub.hp",
        "function %s/refill" % B,
    ])
    w("refill", [
        "# 补满本段血量，并补上副手的死亡保护（上一段的那件可能刚被吃掉）。",
        "attribute @s minecraft:max_health base set %d" % MAX,
        "data merge entity @s {Health:%df}" % MAX,
        "scoreboard players set @s rpg_lub_h %d" % MAX,
        "item replace entity @s weapon.offhand with %s" % GUARD,
    ])
    w("read_hp", [
        "execute store result score @s rpg_lub_h run data get entity @s Health 1",
        "function %s/bar" % B,
    ])
    bar = []
    for s, (_, hp, floor, *_rest) in STAGES.items():
        bar += ["execute if score @s %s matches %d run scoreboard players operation #v %s = @s rpg_lub_h" % (O, s, O),
                ]
    w("bar", bar + [
        "execute if score #v %s matches ..-1 run scoreboard players set #v %s 0" % (O, O),
        "execute store result bossbar rpg:lucifer_boss value run scoreboard players get #v %s" % O,
        "# 横幅每 50 血一档，跨档才换图。",
        "scoreboard players operation #s %s = #v %s" % (O, O),
        "scoreboard players add #s %s 49" % O,
        "scoreboard players set #k %s %d" % (O, MAX // art.STEPS),
        "scoreboard players operation #s %s /= #k %s" % (O, O),
        "execute if score #s %s matches %d.. run scoreboard players set #s %s %d" % (O, art.STEPS + 1, O, art.STEPS),
        "execute unless score #s %s = @s rpg_lub_s run function %s/bar_name" % (O, B),
    ])
    names = ["scoreboard players operation @s rpg_lub_s = #s %s" % O]
    for s in STAGES:
        names += ["execute if score @s %s matches %d if score #s %s matches %d run return run %s" % (O, s, O, k, bar_name(s, k))
                  for k in range(art.STEPS + 1)]
    w("bar_name", names)

    # ---- 出招调度：复用领主的冷却节奏；空闲且冷却走完才出手，大招只在选招时插入。
    w("schedule", [
        "execute unless score @s rpg_l2_st matches 2 run return 0",
        "execute if entity @s[tag=rpg.lu2f.morph] run return 0",
        "scoreboard players add @s rpg_dm_cd 0",
        "execute if score @s rpg_dm_cd matches 1.. run return run scoreboard players remove @s rpg_dm_cd 1",
        "execute if entity @a[distance=..%d,%s] run function %s/cast" % (CAST_RANGE, SURV, B),
    ])
    cast = ["scoreboard players set @s rpg_dm_cd %d" % CAST_CD, "scoreboard players set #ult %s 0" % O]
    for s, (name, hp, floor, ults, clock, *_r) in STAGES.items():
        for i, line in enumerate(ults, 1):
            cast.append("execute if score @s %s matches %d if score @s rpg_lub_h matches ..%d unless entity @s[tag=rpg.lub.u%d] run scoreboard players set #ult %s %d"
                        % (O, s, floor + line, i, O, i))
        cast.append("execute if score @s %s matches %d if score #ult %s matches 0 if score @s rpg_lub_c matches %d.. run scoreboard players set #ult %s 9"
                    % (O, s, O, clock, O))
    cast += [
        "execute if score #ult %s matches 1.. run return run function %s/ult" % (O, B),
        "tag @s add rpg.dm.cast",
        "execute if entity @s[tag=rpg.lu.phase2] run function %s/cast" % FIGHT,
        "execute unless entity @s[tag=rpg.lu.phase2] run function %s/p1/cast" % FIGHT,
        "tag @s remove rpg.dm.cast",
    ]
    w("cast", cast)
    w("ult", [
        "execute if score #ult %s matches 1 run tag @s add rpg.lub.u1" % O,
        "execute if score #ult %s matches 2 run tag @s add rpg.lub.u2" % O,
        "scoreboard players set @s rpg_lub_c 0",
        "scoreboard players set @s rpg_dm_cd %d" % CAST_CD,
        "execute if entity @s[tag=rpg.lu.phase2] run function %s/ult/warn" % FIGHT,
        "execute unless entity @s[tag=rpg.lu.phase2] run function %s/p1/ult/warn" % FIGHT,
    ])

    # ---- 阶段切换
    w("stage/end1", [
        "# 蛇 → 树：钳在底线，大招标记与时钟归零，交给已做好的变身演出。",
        "function %s/refill" % B,
        "scoreboard players set @s %s 2" % O,
        "scoreboard players set #stage %s 2" % O,
        "tag @s remove rpg.lub.u1",
        "tag @s remove rpg.lub.u2",
        "scoreboard players set @s rpg_lub_c 0",
        "tag @s add rpg.lub",
        "function %s/morph/start" % FIGHT,
        bar_name(2),
        "bossbar set rpg:lucifer_boss max %d" % STAGES[2][1],
        "bossbar set rpg:lucifer_boss value %d" % STAGES[2][1],
        "function %s/music/2" % B,
        say("晨星落了下来，落回那棵树上。", gloss=True, name="第二阶段 · "),
    ])
    w("stage/end2", [
        "# 树倒下：古龙（三阶段）还没做，暂时在这里结算。",
        "function %s/refill" % B,
        "tag @s add rpg.lub.end",
        "scoreboard players set @s %s 9" % O,
        "scoreboard players set #stage %s 9" % O,
        "scoreboard players set @s rpg_lub_c 0",
        "function %s/cancel" % FIGHT,
        "function %s/hold" % FIGHT,
        "effect give @s minecraft:resistance 10 4 true",
        "function rpg:lucifer_p2/play/jungleabomination_death",
        "bossbar set rpg:lucifer_boss value 0",
        say("……树根断了。可蛇不会死在树上。", gloss=True),
    ])
    w("finale/tick", [
        "scoreboard players add @s rpg_lub_c 1",
        "execute if score @s rpg_lub_c matches %d.. run function %s/victory" % (FINALE_TICKS, B),
    ])

    # ---- 结算、判负、清场
    quote = ui.row(ui.comp("〖启示录 20:2〗", ui.BROADCAST_HOLY, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                   ui.comp("他捉住那龙，就是古蛇，又叫魔鬼，也叫撒但，把它捆绑一千年。", ui.BROADCAST_NAME))
    w("victory", [
        "execute at @e[type=minecraft:marker,tag=rpg.lub.center,limit=1] run particle %s ~ ~2 ~ 3 2 3 0.1 120 force" % ui.pillar_transition(1, 3),
        "execute at @e[type=minecraft:marker,tag=rpg.lub.center,limit=1] run playsound minecraft:entity.wither.death hostile @a[distance=..%d] ~ ~ ~ 1 1.3" % BAR_RANGE,
        "execute at @e[type=minecraft:marker,tag=rpg.lub.center,limit=1] run tellraw @a[distance=..%d] %s" % (BAR_RANGE, quote),
        "execute at @e[type=minecraft:marker,tag=rpg.lub.center,limit=1] run scoreboard players set @a[distance=..%d] rpg_taint 0" % BAR_RANGE,
        "function %s/clear" % B,
    ])
    w("lose", [
        "execute at @e[type=minecraft:marker,tag=rpg.lub.center,limit=1] run %s" % say("没有人留下来看晨星。").replace(
            "tellraw @a[distance=..%d]" % BAR_RANGE, "tellraw @a[distance=..%d]" % (BAR_RANGE * 2)),
        "function %s/clear" % B,
    ])
    w("clear", [
        "# 清除最终 Boss 的全部实体。模型部件随载体一起清掉；特效按寿命、罪仆按主人自行消失。",
        "execute as @e[%s] run function %s/clear_unit" % (UNIT, B),
        "kill @e[type=minecraft:marker,tag=rpg.lub.center]",
        "bossbar set rpg:lucifer_boss visible false",
        "bossbar set rpg:lucifer_boss players",
    ] + ["stopsound @a record minecraft:%s" % m for m in sorted({v[5] for v in STAGES.values()})] + [
        "scoreboard players set #fight %s 0" % O,
        "scoreboard players set #stage %s 0" % O,
    ])
    w("clear_unit", [
        "execute on passengers run kill @s",
        "tp @s ~ -256 ~",
        "kill @s",
    ])

    # ---- 音乐：唱片机音量，放完循环
    music = ["scoreboard players remove #bgm %s 1" % O]
    for s, v in STAGES.items():
        music.append("execute if score #bgm %s matches ..0 if score #stage %s matches %d run function %s/music/%d" % (O, O, s, B, s))
        w("music/%d" % s, ["stopsound @a[distance=..%d] record minecraft:%s" % (BAR_RANGE, m)
                           for m in sorted({x[5] for x in STAGES.values()})] + [
            "execute as @a[distance=..%d] at @s run playsound minecraft:%s record @s ~ ~ ~ 1 1" % (BAR_RANGE, v[5]),
            "scoreboard players set #bgm %s %d" % (O, v[6]),
        ])
    w("music/tick", music)

    # ---- 调试
    w("debug/stage2", [
        "# 召唤后直接打到一阶段底线，走正常的变身演出进入二阶段。",
        "function %s/summon" % B,
        "# 先补满（含死亡保护），再把血量压到底线，下一次读血就走正常的变身。",
        "tag @e[%s,limit=1,sort=nearest] add rpg.lub.hp" % UNIT,
        "execute as @e[%s,limit=1,sort=nearest] run function %s/refill" % (UNIT, B),
        "execute as @e[%s,limit=1,sort=nearest] run data merge entity @s {Health:1f}" % UNIT,
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_lub_h 1" % UNIT,
    ])


MARK = "# 最终 Boss 路西法（add_lucifer_boss.py）"


def _path(rel):
    return os.path.join(FUNC, *rel.split("/")) + ".mcfunction"


def insert_after(rel, anchor, new):
    path = _path(rel)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    if MARK in lines:
        return
    if anchor not in lines:
        raise AssertionError("%s: anchor line missing: %s" % (rel, anchor))
    i = lines.index(anchor) + 1
    lines[i:i] = [MARK, new]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))


def prepend(rel, new):
    path = _path(rel)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    if MARK in lines:
        return
    i = 0
    while i < len(lines) and lines[i].startswith("#"):
        i += 1
    lines[i:i] = [MARK, new]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))


def hook():
    # 一阶段外观只给带 rpg.advent 的领主换装，这里给最终 Boss 加一条换装入口。
    insert_after("lucifer_lord/tick",
                 "execute as @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.lu,tag=!rpg.lu.phase2,scores={rpg_dm_lord=1}] at @s run function rpg:lucifer_lord/dress",
                 "execute as @e[type=minecraft:vindicator,tag=rpg.lub,tag=!rpg.lu,tag=!rpg.lu.phase2] at @s run function rpg:lucifer_lord/dress")
    # 新约技能按最大生命百分比结算；Boss 血池大，改走末影之心那套固定伤害。
    for rel, target in (("divine/damage/new_target", "new_target"), ("divine/damage/old_target", "old_target"),
                        ("divine/damage/field_target", "field_target"), ("divine/judgment/strike", "judgment_target")):
        prepend(rel, "execute if entity @s[tag=rpg.lub] run return run function rpg:pope_fight/heart/%s" % target)
    hook_tag(DP, "load", "%s/load" % B, False)
    hook_tag(DP, "tick", "%s/tick" % B, True)


def main():
    build()
    hook()
    count = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("lucifer_boss: %d functions; HP pool %d (%s)" % (
        count, MAX, ", ".join("%s %d" % (v[0], v[1]) for v in STAGES.values())))


if __name__ == "__main__":
    main()
