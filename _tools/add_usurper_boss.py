# -*- coding: utf-8 -*-
"""篡夺者（达里奥·所罗门）Boss 的战斗外壳（docs/USURPER-DESIGN.md）。只用指令召唤，规格对齐教皇和路西法。

    python add_usurper_boss.py ../rpg

这里管：召唤、载体、两段血、死亡保护、普攻与出招调度、大招血线与时钟、切阶段、失败重置、清场、音乐。
外观在 add_usurper_model.py（一阶段附魔师，载体标签 rpg.usb 换装为 rpg.usm）。

一阶段（附魔师）的普攻、三招、七十二柱召役和两个大招都已实装（stage1()）；
二阶段（首席附魔师，篡夺圣灵）的连拳、天降、圣光突进、圣雷砸地、授权（圣卫与权柄线）、两个大招、
变身演出、破绽"有权无力"和击败结算在 stage2()。首席附魔师模型在 add_prime_enchanter_model.py，
白金重着色与帽顶王冠在 add_usurper_holy_look.py；变身时它的部件挪到这个载体上。
新约技能能打到他（载体带 rpg.demon.fly，只有新约技能选它），走固定伤害，二阶段多 25%。

血量每段一池，各 1000（原版卫道士最大生命上限 1024）。切段时补满；副手放隐形的死亡保护物品，
致命一击被它吃掉、载体剩 1 血，再由切段接手（同 add_lucifer_boss.py）。
两个阶段都不带 rpg.demon：他是人，七罪契约技能打不到他（设计稿第 9 节第 4 条）。
"""

import json
import os
import sys

import rpg_ui_style as ui
import add_usurper_fx_art as art         # 字形码位表（与字体同序）
import add_usurper_boss_art as bar_art   # 位图血条横幅
from display_mob import hook_tag, wf

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "usurper_boss")
B = "rpg:usurper_boss"
LOOK = "rpg:usurper"                 # add_usurper_model.py
O = "rpg_ub"
UNIT = "type=minecraft:vindicator,tag=rpg.usb"
SURV = "gamemode=!spectator,gamemode=!creative"

ARENA = 40
BAR_RANGE = 48
EMPTY_LIMIT = 1200                   # 战场里没人满 60 秒判负清场
STRIDE = 4                           # 每 4 刻读一次血
MAX = 1000
GUARD = 'minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]'
BASIC_GAP = 8                        # 普攻间隔（刻）
BASICS_PER_SKILL = 3
BASIC_RANGE = 25
CLIP_BUSY = {"attack": 21, "enchant": 84, "rise": 102}    # 动作长度（刻），这期间不再选招

# 篡夺白金（设计稿第 6 节，rpg_ui_style.WHITE_GOLD）：亮、中、深
WHITE_GOLD = ui.WHITE_GOLD
NAME_COLOR = "#B784D6"               # 一阶段附魔紫
NAME_COLOR2 = WHITE_GOLD[1]

STAGES = {
    # 段号: (名称, 大招血线, 大招时钟（刻）, 音乐, 音乐长度（刻）, 招式轮换)
    1: ("所罗门之裔", (625, 375), 900, "rpg:bgm.usurper1", 2287, ["seal", "infuse", "rewrite"]),
    2: ("篡夺圣灵", (667, 333), 1200, "rpg:bgm.usurper2", 1056, ["launch", "strike", "slam"]),
}
SKILL_NAMES = {
    "seal": ("所罗门封印", "enchant"), "infuse": ("附魔灌注", "enchant"), "rewrite": ("契约改写", "enchant"),
    "launch": ("天降", "enchant"), "strike": ("圣光突进", "attack"), "slam": ("圣雷砸地", "enchant"),
}
ULT_NAMES = {1: ("七十二柱环", "所罗门之钥"), 2: ("神力超载", "伪圣审判")}


def w(path, lines):
    wf(os.path.join(OUT, *path.split("/")) + ".mcfunction", lines)


def say(text, gloss=False, name=None, stage=1):
    """〖篡夺者〗 播报（ART-STYLE.md §12）。"""
    parts = [ui.comp("%s篡夺者%s" % ui.BRACKETS, NAME_COLOR if stage == 1 else NAME_COLOR2, True)]
    if gloss:
        parts.append(ui.comp(" " + ui.fraktur("The Usurper"), ui.BROADCAST_GLOSS))
    parts.append(ui.comp(ui.GAP, ui.BROADCAST_BODY))
    if name:
        parts.append(ui.comp(name, ui.BROADCAST_NAME))
    parts.append(ui.comp(text, ui.BROADCAST_BODY))
    return "tellraw @a[distance=..%d] %s" % (BAR_RANGE, ui.row(*parts))


def bar_title(stage, step=bar_art.STEPS):
    """血条名字是一整张位图横幅（原版条已隐藏），见 add_usurper_boss_art.py。"""
    return "bossbar set rpg:usurper_boss name %s" % json.dumps(
        {"text": bar_art.bar_text(stage, step), "font": bar_art.FONT}, ensure_ascii=True, separators=(",", ":"))


def build():
    w("load", [
        "scoreboard objectives add %s dummy" % O,
        "scoreboard objectives add rpg_ub_h dummy",      # 当前血量
        "scoreboard objectives add rpg_ub_c dummy",      # 本段大招时钟
        "scoreboard objectives add rpg_ub_b dummy",      # 普攻计时
        "scoreboard objectives add rpg_ub_n dummy",      # 普攻计数
        "scoreboard objectives add rpg_ub_k dummy",      # 招式轮换序号
        "scoreboard objectives add rpg_ub_busy dummy",   # 动作占用（刻）
        "scoreboard objectives add rpg_ub_sk dummy",     # 正在进行的招式
        "scoreboard objectives add rpg_ub_t dummy",      # 招式时间线（刻）
        "scoreboard objectives add rpg_ub_life dummy",   # 特效寿命（刻）
        "scoreboard objectives add rpg_ub_kd dummy",     # 特效种类
        "scoreboard objectives add rpg_ub_rw dummy",     # 契约改写剩余（玩家）
        "scoreboard objectives add rpg_ub_p1 dummy",     # 三档契约冷却上一刻的值（玩家）
        "scoreboard objectives add rpg_ub_p2 dummy",
        "scoreboard objectives add rpg_ub_p3 dummy",
        "scoreboard objectives add rpg_ub_l dummy",      # 二阶段：上次读到的血量 ×10
        "scoreboard objectives add rpg_ub_x dummy",      # 二阶段：破绽剩余（刻）
        "scoreboard objectives add rpg_ub_id dummy",     # 二阶段：圣卫与它的权柄线配对
        "scoreboard players set #two %s 2" % O,
        "scoreboard objectives add rpg_ub_s dummy",      # 横幅当前档位
        "bossbar add rpg:usurper_boss \"篡夺者\"",
        "# 粉色档的原版贴图已由教皇战改成全透明：只显示名字里的位图横幅。",
        "bossbar set rpg:usurper_boss color pink",
        "bossbar set rpg:usurper_boss style notched_20",
        "bossbar set rpg:usurper_boss visible false",
    ])

    # ---- 召唤
    w("summon", [
        "# 在执行位置开战。同一时间只允许一场。",
        "execute if score #fight %s matches 1 run return run tellraw @s %s" % (
            O, ui.row(ui.comp("〖篡夺者〗", NAME_COLOR, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                      ui.comp("已经有一场篡夺者战；先用 /function %s/clear 清场。" % B, ui.BROADCAST_BODY))),
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.usb.center\"]}",
        "function %s/altar_clear" % B,
        "summon minecraft:vindicator ~ ~1 ~ {Tags:[\"rpg.usb\",\"rpg.demon.fly\",\"rpg.usb.new\"],Silent:1b,PersistenceRequired:1b,NoAI:0b,"
        "CustomName:[{\"text\":\"[篡夺者]\",\"color\":\"%s\",\"bold\":true,\"italic\":false},{\"text\":\"达里奥·所罗门\",\"color\":\"%s\",\"bold\":false,\"italic\":false}],"
        "Health:%df,active_effects:[{id:\"invisibility\",duration:-1,amplifier:0,show_particles:0b}],"
        "attributes:[{id:\"max_health\",base:%df},{id:\"attack_damage\",base:8f},{id:\"armor\",base:8f},"
        "{id:\"follow_range\",base:48f},{id:\"knockback_resistance\",base:0.6f},{id:\"movement_speed\",base:0.3f}],"
        "drop_chances:{mainhand:0f,offhand:0f}}" % (NAME_COLOR, NAME_COLOR, MAX, MAX),
        "scoreboard players set @e[%s,tag=rpg.usb.new] %s 1" % (UNIT, O),
        "scoreboard players set @e[%s,tag=rpg.usb.new] rpg_ub_h %d" % (UNIT, MAX),
        "scoreboard players set @e[%s,tag=rpg.usb.new] rpg_ub_c 0" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.usb.new] rpg_ub_b 40" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.usb.new] rpg_ub_n 0" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.usb.new] rpg_ub_k 0" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.usb.new] rpg_ub_busy %d" % (UNIT, CLIP_BUSY["rise"]),
        "tag @e[%s,tag=rpg.usb.new] remove rpg.usb.new" % UNIT,
        "scoreboard players set #fight %s 1" % O,
        "scoreboard players set #stage %s 1" % O,
        "scoreboard players set #empty %s 0" % O,
        "scoreboard players set #tick %s 0" % O,
        bar_title(1),
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_ub_s %d" % (UNIT, bar_art.STEPS),
        "bossbar set rpg:usurper_boss color pink",
        "bossbar set rpg:usurper_boss max %d" % MAX,
        "bossbar set rpg:usurper_boss value %d" % MAX,
        "bossbar set rpg:usurper_boss visible true",
        "function %s/music/1" % B,
        "particle minecraft:enchant ~ ~1.5 ~ 1 1.5 1 1 160 force",
        "playsound minecraft:block.enchantment_table.use hostile @a[distance=..%d] ~ ~ ~ 1.2 0.6" % BAR_RANGE,
        say("所罗门封住了七十二柱，钥匙传到了我手里。", gloss=True),
    ])

    # ---- 每刻
    w("tick", [
        "execute unless score #fight %s matches 1 run return 0" % O,
        "execute as @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] at @s run function %s/arena" % B,
    ])
    w("arena", [
        "# 战场（as/at 战场中心）。",
        "scoreboard players add #tick %s 1" % O,
        "execute if entity @a[distance=..%d,%s] run scoreboard players set #empty %s 0" % (ARENA, SURV, O),
        "execute unless entity @a[distance=..%d,%s] run scoreboard players add #empty %s 1" % (ARENA, SURV, O),
        "execute if score #empty %s matches %d.. run return run function %s/lose" % (O, EMPTY_LIMIT, B),
        "execute unless entity @e[%s,distance=..%d] run return run function %s/lost_unit" % (UNIT, ARENA * 3, B),
        "bossbar set rpg:usurper_boss players @a[distance=..%d]" % BAR_RANGE,
        "execute as @e[%s,distance=..%d] at @s run function %s/unit" % (UNIT, ARENA * 3, B),
        "function %s/music/tick" % B,
    ])
    w("lost_unit", [
        "# 载体不见了：二阶段里被一击打穿时按胜利结算；否则清场。",
        "execute if score #stage %s matches 2.. run return run function %s/victory" % (O, B),
        "function %s/clear" % B,
    ])
    w("unit", [
        "# 载体每刻（as/at 载体）。",
        "execute if entity @s[tag=rpg.usb.end] run return run function %s/finale/tick" % B,
        "execute if entity @s[tag=!rpg.usb.hp] run return run function %s/hp_init" % B,
        "scoreboard players operation #m %s = #tick %s" % (O, O),
        "scoreboard players set #k %s %d" % (O, STRIDE),
        "scoreboard players operation #m %s %%= #k %s" % (O, O),
        "execute if score #m %s matches 0 run function %s/read_hp" % (O, B),
        "execute if score @s %s matches 1 if score @s rpg_ub_h matches ..1 run return run function %s/stage/end1" % (O, B),
        "execute if score @s %s matches 2 if score @s rpg_ub_h matches ..1 run return run function %s/stage/end2" % (O, B),
        "execute if entity @s[tag=rpg.usb.morph] run return run function %s/morph/tick" % B,
        "scoreboard players add @s rpg_ub_c 1",
        "execute if score @s rpg_ub_busy matches 1.. run return run scoreboard players remove @s rpg_ub_busy 1",
        "function %s/schedule" % B,
    ])
    w("hp_init", ["tag @s add rpg.usb.hp", "function %s/refill" % B])
    w("refill", [
        "# 补满本段血量，并补上副手的死亡保护（上一段的那件可能刚被吃掉）。",
        "attribute @s minecraft:max_health base set %d" % MAX,
        "data merge entity @s {Health:%df}" % MAX,
        "scoreboard players set @s rpg_ub_h %d" % MAX,
        "scoreboard players set @s rpg_ub_l %d" % (MAX * 10),
        "item replace entity @s weapon.offhand with %s" % GUARD,
    ])
    w("read_hp", [
        "execute if score @s %s matches 2 run function %s/s2/scale" % (O, B),
        "execute store result score @s rpg_ub_h run data get entity @s Health 1",
        "execute store result bossbar rpg:usurper_boss value run scoreboard players get @s rpg_ub_h",
        "# 横幅每 50 血一档，跨档才换图；变身期间停在空条",
        "execute if entity @s[tag=rpg.usb.morph] run return 0",
        "scoreboard players operation #s %s = @s rpg_ub_h" % O,
        "scoreboard players add #s %s 49" % O,
        "scoreboard players set #k %s %d" % (O, MAX // bar_art.STEPS),
        "scoreboard players operation #s %s /= #k %s" % (O, O),
        "execute if score #s %s matches %d.. run scoreboard players set #s %s %d" % (O, bar_art.STEPS + 1, O, bar_art.STEPS),
        "execute if score #s %s matches ..-1 run scoreboard players set #s %s 0" % (O, O),
        "execute unless score #s %s = @s rpg_ub_s run function %s/bar_name" % (O, B),
    ])
    names = ["scoreboard players operation @s rpg_ub_s = #s %s" % O]
    for st in STAGES:
        names += ["execute if score @s %s matches %d if score #s %s matches %d run return run %s" % (O, st, O, k, bar_title(st, k))
                  for k in range(bar_art.STEPS + 1)]
    w("bar_name", names)

    # ---- 出招调度：普攻每 8 刻，每三次普攻接一招；大招在选招时按血线或时钟插入
    w("schedule", [
        "execute unless entity @a[distance=..%d,%s] run return 0" % (BASIC_RANGE, SURV),
        "scoreboard players remove @s rpg_ub_b 1",
        "execute if score @s rpg_ub_b matches 1.. run return 0",
        "scoreboard players set @s rpg_ub_b %d" % BASIC_GAP,
        "execute if score @s rpg_ub_n matches %d.. run return run function %s/pick" % (BASICS_PER_SKILL, B),
        "scoreboard players add @s rpg_ub_n 1",
        "execute if score @s %s matches 1 run function %s/basic/1" % (O, B),
        "execute if score @s %s matches 2 run function %s/basic/2" % (O, B),
    ])
    pick = ["scoreboard players set @s rpg_ub_n 0", "scoreboard players set #ult %s 0" % O]
    for s, (_, ults, clock, *_r) in STAGES.items():
        for i, line in enumerate(ults, 1):
            pick.append("execute if score @s %s matches %d if score @s rpg_ub_h matches ..%d unless entity @s[tag=rpg.usb.u%d] "
                        "run scoreboard players set #ult %s %d" % (O, s, line, i, O, i))
        pick.append("execute if score @s %s matches %d if score #ult %s matches 0 if score @s rpg_ub_c matches %d.. "
                    "run scoreboard players set #ult %s 9" % (O, s, O, clock, O))
    pick.append("execute if score #ult %s matches 1.. run return run function %s/ult/pick" % (O, B))
    pick.append("execute if score @s %s matches 2 if entity @s[tag=rpg.usb.auth] run return run function %s/skill/summon" % (O, B))
    for s, (*_h, rotation) in STAGES.items():
        n = len(rotation)
        pick.append("execute if score @s %s matches %d run scoreboard players operation #r %s = @s rpg_ub_k" % (O, s, O))
        for i, sk in enumerate(rotation):
            pick.append("execute if score @s %s matches %d if score #r %s matches %d run function %s/skill/%s" % (O, s, O, i, B, sk))
        pick.append("execute if score @s %s matches %d run scoreboard players add @s rpg_ub_k 1" % (O, s))
        pick.append("execute if score @s %s matches %d if score @s rpg_ub_k matches %d.. run scoreboard players set @s rpg_ub_k 0" % (O, s, n))
    w("pick", pick)

    # ---- 招式与大招本体：一阶段 stage1()，二阶段 stage2()
    w("ult/pick", [
        "execute if score #ult %s matches 1 run tag @s add rpg.usb.u1" % O,
        "execute if score #ult %s matches 2 run tag @s add rpg.usb.u2" % O,
        "scoreboard players set @s rpg_ub_c 0",
        "# 两招轮流：血线 1 / 时钟到点且上一招是 2 → 第一招；否则第二招",
        "execute if score #ult %s matches 9 if entity @s[tag=rpg.usb.last1] run scoreboard players set #ult %s 2" % (O, O),
        "execute if score #ult %s matches 9 run scoreboard players set #ult %s 1" % (O, O),
        "execute if score @s %s matches 1 if score #ult %s matches 1 run function %s/ult/ring" % (O, O, B),
        "execute if score @s %s matches 1 if score #ult %s matches 2 run function %s/ult/key" % (O, O, B),
        "execute if score @s %s matches 2 if score #ult %s matches 1 run function %s/ult/overcharge" % (O, O, B),
        "execute if score @s %s matches 2 if score #ult %s matches 2 run function %s/ult/judgment" % (O, O, B),
        "execute if score #ult %s matches 1 run tag @s add rpg.usb.last1" % O,
        "execute if score #ult %s matches 2 run tag @s remove rpg.usb.last1" % O,
    ])
    # ---- 阶段切换
    w("stage/end1", [
        "# 一阶段打完：变身（篡夺圣灵）。无敌、站定，约 6 秒后进入二阶段。",
        "function %s/refill" % B,
        "tag @s add rpg.usb.morph",
        "# 收掉一阶段的招式、特效和召役",
        "scoreboard players set @s rpg_ub_sk 0",
        "attribute @s minecraft:armor base set 8",
        "kill @e[tag=rpg.usb.fx]",
        "execute as @e[tag=rpg.usb.unit] run function %s/clear_unit" % B,
        "execute as @a[tag=rpg.usb.rw] run function %s/rewrite/clear" % B,
        "scoreboard players set @s rpg_ub_c 0",
        "data merge entity @s {NoAI:1b,Invulnerable:1b}",
        "function %s/anim/enter/enchant" % LOOK,
        "bossbar set rpg:usurper_boss value %d" % MAX,
        bar_title(1, 0),
        say("把圣灵的权柄……交出来。", gloss=True, name="篡夺 · "),
        "# 致命一击被死亡保护挡下：原作不死图腾在他身前转一下再碎",
        "execute positioned ^ ^0.6 ^1.3 run " + disp("%s/totem" % FX, scale=12, color=0xFFFFFF, tags=("rpg.usb.totem",)),
    ] + born(None, "tspin") + [
        "particle minecraft:totem_of_undying ~ ~1.2 ~ 0.4 0.8 0.4 0.4 40",
        "playsound minecraft:item.totem.use hostile @a[distance=..%d] ~ ~ ~ 1 1" % BAR_RANGE,
    ])
    w("morph/tick", [
        "# 变身演出（as/at 载体，约 6 秒）：白金光柱降下，新约玩家身上牵出光线，书碎，光柱吞没，换成首席附魔师，王冠闪光",
        "scoreboard players add @s rpg_ub_c 1",
        "execute if score @s rpg_ub_c matches 1..100 run particle minecraft:end_rod ~ ~2 ~ 0.4 2 0.4 0.02 6",
        "execute if score @s rpg_ub_c matches 1 run function %s/morph/pillar" % B,
        "execute if score @s rpg_ub_c matches 28 as @e[tag=rpg.usb.totem] at @s run function %s/morph/totem_pop" % B,
        "execute if score @s rpg_ub_c matches 10..60 run scoreboard players operation #m %s = @s rpg_ub_c" % O,
        "scoreboard players set #k %s 10" % O,
        "execute if score @s rpg_ub_c matches 10..60 run scoreboard players operation #m %s %%= #k %s" % (O, O),
        "execute if score @s rpg_ub_c matches 10..60 if score #m %s matches 0 run function %s/morph/lines" % (O, B),
        "execute if score @s rpg_ub_c matches 60 run function %s/morph/shatter" % B,
        "execute if score @s rpg_ub_c matches 61 run function %s/morph/pages_fly" % B,
        "execute if score @s rpg_ub_c matches 70 run function %s/morph/engulf" % B,
        "execute if score @s rpg_ub_c matches 72 run function %s/look2/swap" % B,
        "execute if score @s rpg_ub_c matches 95 run function %s/morph/crown" % B,
        "execute if score @s rpg_ub_c matches 120.. run function %s/stage/begin2" % B,
    ])
    w("stage/begin2", [
        "tag @s remove rpg.usb.morph",
        "tag @s remove rpg.usb.u1",
        "tag @s remove rpg.usb.u2",
        "tag @s remove rpg.usb.last1",
        "data merge entity @s {NoAI:0b,Invulnerable:0b}",
        "scoreboard players set @s %s 2" % O,
        "scoreboard players set #stage %s 2" % O,
        "scoreboard players set @s rpg_ub_c 0",
        "scoreboard players set @s rpg_ub_n 0",
        "scoreboard players set @s rpg_ub_k 0",
        "scoreboard players set @s rpg_ub_b 20",
        "scoreboard players set @s rpg_ub_x 0",
        "scoreboard players set @s rpg_ub_sk 0",
        "execute store result score @s rpg_ub_l run data get entity @s Health 10",
        "# 第一件事是授权：召来圣卫",
        "tag @s add rpg.usb.auth",
        bar_title(2),
        "scoreboard players set @s rpg_ub_s %d" % bar_art.STEPS,
        "function %s/music/2" % B,
        "particle minecraft:flash{color:16774876} ~ ~1.5 ~ 0 0 0 0 1 force",
        "playsound minecraft:item.totem.use hostile @a[distance=..%d] ~ ~ ~ 1 0.8" % BAR_RANGE,
        say("权柄在我手里。现在，由我来命名真实。", gloss=True, name="第二阶段 · ", stage=2),
    ])
    w("stage/end2", [
        "# 二阶段打完：倒地（原作死亡动作），王冠碎裂，权柄归还，约 6 秒后胜利。",
        "function %s/refill" % B,
        "tag @s add rpg.usb.end",
        "scoreboard players set @s rpg_ub_c 0",
        "scoreboard players set @s rpg_ub_sk 0",
        "data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}",
        "function %s/altar_clear" % B,
        "kill @e[tag=rpg.usb.fx]",
        "execute as @e[tag=rpg.usb.guard] run function rpg:holy_guard/remove",
        "tag @s remove rpg.usb.exposed",
        "tag @s remove rpg.usb.guarded",
        "tag @s remove rpg.usb.auth",
        "tag @s remove rpg.usb.reauth",
        "tag @a remove rpg.usb.shit",
        "tag @a remove rpg.usb.dhit",
        "execute if entity @s[tag=rpg.usb.s2] run function rpg:prime_enchanter/anim/enter/death",
        "playsound minecraft:entity.evoker.death hostile @a[distance=..%d] ~ ~ ~ 1.2 0.6" % BAR_RANGE,
        "playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..%d] ~ ~ ~ 0.8 0.7" % BAR_RANGE,
        "bossbar set rpg:usurper_boss value 0",
        bar_title(2, 0),
        say("……权柄，从来就不是能偷来的东西。", gloss=True, stage=2),
    ])
    w("finale/tick", [
        "scoreboard players add @s rpg_ub_c 1",
        "execute if score @s rpg_ub_c matches 1..90 run particle minecraft:end_rod ~ ~1.5 ~ 0.5 1 0.5 0.05 3",
        "execute if score @s rpg_ub_c matches 20 if entity @s[tag=rpg.usb.s2] run function %s/finale/crown" % B,
        "execute if score @s rpg_ub_c matches 21 run function %s/finale/shards_fly" % B,
        "execute if score @s rpg_ub_c matches 40 run function %s/finale/return" % B,
        "execute if score @s rpg_ub_c matches 118.. run function %s/victory" % B,
    ])

    # ---- 结算、判负、清场
    quote = ui.row(ui.comp("〖约翰福音 10:10〗", ui.BROADCAST_HOLY, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                   ui.comp("盗贼来，无非要偷窃，杀害，毁坏。", ui.BROADCAST_NAME))
    w("victory", [
        "execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run particle minecraft:flash{color:16774876} ~ ~2 ~ 0 0 0 0 1 force",
        "execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run playsound minecraft:block.beacon.deactivate hostile @a[distance=..%d] ~ ~ ~ 1.2 0.8" % BAR_RANGE,
        "execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run tellraw @a[distance=..%d] %s" % (BAR_RANGE, quote),
        "function %s/clear" % B,
    ])
    w("lose", [
        "execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run %s" % say("没有人来阻止我。").replace(
            "tellraw @a[distance=..%d]" % BAR_RANGE, "tellraw @a[distance=..%d]" % (BAR_RANGE * 2)),
        "function %s/clear" % B,
    ])
    w("clear", [
        "# 清除篡夺者战的全部实体。模型部件随载体一起清掉；圣坛的屏障方块先拆。",
        "function %s/altar_clear" % B,
        "tag @a remove rpg.usb.shit",
        "tag @a remove rpg.usb.dhit",
        "tag @a remove rpg.usb.hit",
        "tag @a remove rpg.usb.safe",
        "execute as @e[%s] run function %s/clear_unit" % (UNIT, B),
        "kill @e[type=minecraft:marker,tag=rpg.usb.center]",
        "kill @e[tag=rpg.usb.fx]",
        "execute as @e[tag=rpg.usb.unit] run function %s/clear_unit" % B,
        "execute as @a[tag=rpg.usb.rw] run function %s/rewrite/clear" % B,
        "bossbar set rpg:usurper_boss visible false",
        "bossbar set rpg:usurper_boss players",
    ] + ["stopsound @a record %s" % m for m in sorted({v[3] for v in STAGES.values()})] + [
        "scoreboard players set #fight %s 0" % O,
        "scoreboard players set #stage %s 0" % O,
    ])
    w("clear_unit", ["execute on passengers run kill @s", "tp @s ~ -256 ~", "kill @s"])

    # ---- 音乐：唱片机音量，放完循环
    music = ["scoreboard players remove #bgm %s 1" % O]
    for s, v in STAGES.items():
        music.append("execute if score #bgm %s matches ..0 if score #stage %s matches %d run function %s/music/%d" % (O, O, s, B, s))
        w("music/%d" % s, ["stopsound @a[distance=..%d] record %s" % (BAR_RANGE, m)
                           for m in sorted({x[3] for x in STAGES.values()})] + [
            "execute as @a[distance=..%d] at @s run playsound %s record @s ~ ~ ~ 1 1" % (BAR_RANGE, v[3]),
            "scoreboard players set #bgm %s %d" % (O, v[4]),
        ])
    w("music/tick", music)

    # ---- 调试
    w("debug/stage2", [
        "# 召唤后直接打到一阶段底线，走正常的变身进入二阶段。",
        "function %s/summon" % B,
        "tag @e[%s,limit=1,sort=nearest] add rpg.usb.hp" % UNIT,
        "execute as @e[%s,limit=1,sort=nearest] run function %s/refill" % (UNIT, B),
        "execute as @e[%s,limit=1,sort=nearest] run data merge entity @s {Health:1f}" % UNIT,
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_ub_h 1" % UNIT,
    ])


# =====================================================================================
# 一阶段：所罗门之裔（附魔师）的普攻、三招、召役与两个大招（设计稿第 4、6 节）。
# 特效素材取自原作（add_usurper_fx_art.py）：附魔台符文、灵魂图腾法阵、由它叠成的六芒星、唤魔者尖牙，
# 以及通用特效贴图（像素冲击环、爆环、星芒、神光、六边形、漩涡、光晕盘、裂纹、弧光、附魔光束）；
# 书页弹用附魔师模型自己的书页。特效实体都带 rpg.usb.fx 和寿命，到期自动清除；形变交给客户端插值。
# =====================================================================================
FX = "rpg:usurper_fx"
FONT = "rpg:usurper_fx"
PURPLE = 0xB784D6
PURPLE_HEX = "#B784D6"
LAVENDER = "#E8D5FF"                                   # 亮紫：星芒、爆光
DEEP_HEX = "#5B2C6F"                                   # 暗紫：光晕、裂纹
WARN_HEX = "#C04A3C"                                   # 反噬
ID = "[0f,0f,0f,1f]"
SKILL_ID = {"seal": 1, "infuse": 2, "rewrite": 3, "ring": 4, "key": 5, "stagger": 9}
SEAL_R, SEAL_DMG, SEAL_DELAY, SEAL_LOCK = 3, 10, 30, 160
INFUSE_TICKS, INFUSE_RANGE, INFUSE_STAGGER = 120, 20, 40
REWRITE_TICKS, REWRITE_TAINT = 200, 5
BOLT_SPEED, BOLT_LIFE, BOLT_DMG, SWEEP_DMG, SWEEP_RANGE = 0.9, 30, 6, 8, 3.5
WAVE_LINES = (1000, 750, 500, 250)
UNIT_CAP = 4
RING_R, RING_N, RING_SEG, RING_WIND, RING_GAP, RING_DMG = 10, 72, 7, 30, 20, 12
KEY_R, KEY_SAFE_R, KEY_SAFE_D, KEY_DELAY, KEY_DMG, KEY_KNEEL = 14, 2.5, 11, 80, 26, 60
SERVANT = "tag=rpg.usb.unit"
ARMOR = 8

# 七柱罪仆名册，与 check_demon_minions.py 的 LORDS 一致
LORD_SPIRITS = [
    ("lucifer", ["bael", "agares", "vassago", "samigina", "marbas"]),
    ("leviathan", ["valefor", "amon", "barbatos", "paimon", "buer"]),
    ("abaddon", ["gusion", "sitri", "beleth", "leraje", "eligos"]),
    ("beelzebub", ["zepar", "botis", "bathin", "sallos", "purson"]),
    ("samael", ["marax", "ipos", "aim", "naberius", "glasya_labolas"]),
    ("belial", ["bune", "ronove", "berith", "astaroth", "forneus"]),
    ("mammon", ["foras", "asmoday", "gaap", "furfur", "marchosias"]),
]


def color_int(hexstr):
    return int(hexstr.lstrip("#"), 16)


def lit(n):
    return ui.pillar(n)["lit"]


# ---------------------------------------------------------------------------
# 特效引擎（与教皇、路西法战同一套载体选择，display-render-facts）：
#   发光体 = text_display 位图字形（不受光照，文字颜色染色，默认朝向相机）；
#   地面贴花与实物 = item_display（朝上的面全亮），custom_model_data 颜色染色。
# 每个特效召出时记下寿命 rpg_ub_life 与种类 rpg_ub_kd；fx/tick 只在寿命走到预定的刻
# 换一次帧或发一次 data merge，形变交给客户端插值。
# ---------------------------------------------------------------------------
def gscale(name, blocks):
    """Scale that makes a glyph `blocks` wide (one glyph pixel is 0.025 block at scale 1)."""
    return round(blocks / (art.glyph_table()[name][1] * 0.025), 4)


def sc(s):
    return "scale:[%gf,%gf,%gf]" % (s if isinstance(s, tuple) else (s, s, s))


def flat_sc(s):
    return "scale:[%gf,1f,%gf]" % (s, s)


TW = gscale("star", 0.7)
RAY_W, RAY_H = gscale("ray", 1.6), gscale("ray", 4.2)
BOLT_W = 2.4                                            # 闪电字形 8 像素宽的线居中在 32 像素格里：宽 0.6 格
BOLT_K = gscale("bolt", BOLT_W)
BOLT_H = BOLT_K * 4                                     # 竖着拉长 4 倍：约 9.6 格高
SLASH_K = gscale("slash", 2.2)
# 种类：名称 -> dict(life, frames=(字形或物品, 名称, 帧数, 每帧刻数), steps=[(寿命走到几时, 插值刻数, 变换片段)], extra=[每刻指令])
KINDS = {
    "spin": dict(extra=["tp @s ~ ~ ~ ~3 ~"]),
    "spinr": dict(extra=["tp @s ~ ~ ~ ~-2 ~"]),
    "fang": dict(life=24, extra=["execute if score @s rpg_ub_life matches 22 run tp @s ~ ~1.3 ~",
                                 "execute if score @s rpg_ub_life matches 4 run tp @s ~ ~-1.3 ~"]),
    "pop": dict(life=10, frames=("glyph", "pop", 10, 1)),
    "burst": dict(life=16, frames=("glyph", "burst", 8, 2)),
    "shock": dict(life=16, frames=("item", "shock", 8, 2)),
    "twinkle": dict(life=10, steps=[(9, 3, sc(TW)), (4, 4, sc(0.01))]),
    "ray": dict(life=16, steps=[(15, 4, sc((RAY_W, RAY_H, RAY_W))), (6, 6, sc((0.01, RAY_H, 0.01)))]),
    "raylong": dict(life=92, steps=[(91, 8, sc((RAY_W, RAY_H, RAY_W))), (6, 6, sc((0.01, RAY_H, 0.01)))]),
    "sweep": dict(life=8, steps=[(7, 3, flat_sc(4.5)), (3, 3, flat_sc(5.5))]),
    "sbeam": dict(life=10, steps=[(4, 4, "scale:[0.01f,0.01f,%gf]" % RING_R)]),
    # 二阶段
    "spark": dict(life=8, frames=("glyph", "spark", 8, 1)),
    "sparkl": dict(life=60, frames=("glyph", "spark", 15, 4)),
    "bolt": dict(life=10, frames=("glyph", "bolt", 4, 2), steps=[(3, 3, "scale:[0.01f,%gf,0.01f]" % BOLT_H)]),
    "slashfx": dict(life=8, steps=[(7, 2, sc(SLASH_K * 1.25)), (3, 3, sc(0.01))]),
    "sq": dict(life=8, frames=("item", "sq", 8, 1)),
    "rise": dict(life=136, steps=[(135, 16, "translation:[0f,0f,0f]"), (14, 10, "translation:[0f,-2.4f,0f]")]),
    "tspin": dict(life=30, extra=["tp @s ~ ~ ~ ~24 ~"]),
    "pillar": dict(life=125, steps=[(124, 10, "scale:[1.4f,1.4f,40f]"), (10, 8, "scale:[0.01f,0.01f,40f]")]),
}
KIND_ID = dict((n, i + 1) for i, n in enumerate(KINDS))


def born(life, kind=None):
    """Everything just summoned (rpg.usb.fxnew): its life and kind; then it is no longer new."""
    if kind and life is None:
        life = KINDS[kind]["life"]
    return ["scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life %d" % life,
            "scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd %d" % (KIND_ID[kind] if kind else 0),
            "tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew"]


def _tags(tags):
    return ",".join('"%s"' % x for x in ("rpg.usb.fx", "rpg.usb.fxnew") + tuple(tags))


def disp(model, pos="~ ~ ~", scale=1.0, color=PURPLE, tags=(), billboard=None, trans=(0, 0, 0), tp=1, yaw=None, lrot=None):
    """A solid effect item_display (page, fang, beam), full bright, tinted through custom_model_data colour 0.
    Born with rpg.usb.fxnew: follow it with born()."""
    s = scale if isinstance(scale, tuple) else (scale, scale, scale)
    bb = ',billboard:"%s"' % billboard if billboard else ""
    if yaw is not None:
        bb += ",Rotation:[%sf,0f]" % yaw
    return ('summon minecraft:item_display %s {Tags:[%s],item:{id:"minecraft:paper",count:1,components:'
            '{"minecraft:item_model":"%s","minecraft:custom_model_data":{colors:[%d]}}},brightness:{sky:15,block:15},'
            'teleport_duration:%d,interpolation_duration:3,view_range:2f,transformation:{translation:[%sf,%sf,%sf],left_rotation:%s,'
            'scale:[%sf,%sf,%sf],right_rotation:%s}%s}' % (
                pos, _tags(tags), model, color, tp, trans[0], trans[1], trans[2], lrot or ID, s[0], s[1], s[2], ID, bb))


def marker(pos, *tags):
    return "summon minecraft:marker %s {Tags:[%s]}" % (pos, _tags(tags))


def decal(name, size, color, pos="~ ~0.05 ~", kind=None, life=None, tags=(), yaw=None):
    """A ground decal (up-facing plane, `size` blocks across), born at once."""
    return [disp("%s/%s" % (FX, name), pos=pos, scale=(size, 1, size), color=color_int(color) if isinstance(color, str) else color,
                 tags=tags, yaw=yaw)] + born(life, kind)


def glyph(name, blocks, color, pos="~ ~ ~", frame=0, kind=None, life=None, tags=(), billboard="center", trans=(0, 0, 0),
          start=None, born_now=True, tpd=1):
    """A glowing sprite: one text_display glyph from font rpg:usurper_fx, tinted by the text colour."""
    k = gscale(name, blocks)
    s = start if start is not None else (k, k, k)
    if not isinstance(s, tuple):
        s = (s, s, s)
    line = ('summon minecraft:text_display %s {Tags:[%s],text:{text:"%s",font:"%s",color:"%s"},background:0,'
            'billboard:"%s",brightness:{sky:15,block:15},teleport_duration:%d,interpolation_duration:3,view_range:2f,'
            'transformation:{translation:[%sf,%sf,%sf],left_rotation:%s,scale:[%gf,%gf,%gf],right_rotation:%s}}'
            % (pos, _tags(tags), art.glyph_text(name, frame), FONT, color, billboard, tpd, trans[0], trans[1], trans[2], ID,
               s[0], s[1], s[2], ID))
    return [line] + (born(life, kind) if born_now else [])


def twinkle(pos, color=LAVENDER, frame=1):
    return glyph("star", 0.7, color, pos=pos, frame=frame, kind="twinkle", start=0.01)


def ray(pos, color, long=False, tags=()):
    return glyph("ray", 1.6, color, pos=pos, billboard="vertical", kind="raylong" if long else "ray",
                 start=(RAY_W, 0.01, RAY_W), trans=(0, 2.1, 0), tags=tags)


def morph(selector, scale, ticks=4, decal_=False):
    """Interpolated rescale of displays that already exist (not on their first tick)."""
    return ("execute as @e[%s] run data merge entity @s {start_interpolation:0,interpolation_duration:%d,"
            "transformation:{%s}}" % (selector, ticks, flat_sc(scale) if decal_ else sc(scale)))


def hit(selector, dmg):
    return "execute as @a[%s,%s] run damage @s %d minecraft:magic by @e[%s,limit=1]" % (selector, SURV, dmg, UNIT)


def every(n, score="@s rpg_ub_t"):
    """#m = score mod n (use with `if score #m rpg_ub matches 0`)."""
    who, obj = score.split()
    return ["scoreboard players operation #m %s = %s %s" % (O, who, obj),
            "scoreboard players set #k %s %d" % (O, n),
            "scoreboard players operation #m %s %%= #k %s" % (O, O)]


def build_fx():
    w("fx/tick", [
        "# 每个特效实体每刻（as/at 它）。",
        "scoreboard players remove @s rpg_ub_life 1",
        "execute if score @s rpg_ub_life matches ..0 run return run kill @s",
        "execute if entity @s[tag=rpg.usb.bolt] run return run function %s/fx/bolt" % B,
        "execute if score @s rpg_ub_kd matches 1.. run function %s/fx/kind" % B,
    ])
    w("fx/kind", ["execute if score @s rpg_ub_kd matches %d run return run function %s/fx/k/%s" % (i, B, n)
                  for n, i in KIND_ID.items()])
    for name, k in KINDS.items():
        body = list(k.get("extra", []))
        for at_, ticks, frag in k.get("steps", []):
            body.append("execute if score @s rpg_ub_life matches %d run data merge entity @s "
                        "{start_interpolation:0,interpolation_duration:%d,transformation:{%s}}" % (at_, ticks, frag))
        if "frames" in k:
            how, seq, count, step = k["frames"]
            for i in range(1, count):
                at_ = k["life"] - i * step
                if how == "glyph":
                    body.append("execute if score @s rpg_ub_life matches %d run data modify entity @s text.text set value \"%s\""
                                % (at_, art.glyph_text(seq, i)))
                else:
                    body.append("execute if score @s rpg_ub_life matches %d run data modify entity @s "
                                "item.components.\"minecraft:item_model\" set value \"%s/%s_%d\"" % (at_, FX, seq, i))
        w("fx/k/%s" % name, body)


def stage1():
    import math
    build_fx()
    lock_lines = lambda sel: [
        "scoreboard players set @a[%s,%s,scores={rpg_pact_cd=..%d}] rpg_pact_cd %d" % (sel, SURV, SEAL_LOCK, SEAL_LOCK),
        "scoreboard players set @a[%s,%s,scores={rpg_pact_cd2=..%d}] rpg_pact_cd2 %d" % (sel, SURV, SEAL_LOCK, SEAL_LOCK),
        "scoreboard players set @a[%s,%s,scores={rpg_pact_cd3=..%d}] rpg_pact_cd3 %d" % (sel, SURV, SEAL_LOCK, SEAL_LOCK),
        # 封印设上的冷却不算“用了契约技能”（契约改写只罚玩家自己出手）
        "execute as @a[%s,tag=rpg.usb.rw] run function %s/rewrite/sync" % (sel, B),
    ]

    # ---- 书页弹：飞行、拖尾星芒、命中爆环
    w("fx/bolt", [
        "# 书页弹：每刻前进，碰到人就打，撞墙就散；每 3 刻在身后留一颗星芒",
        "tp @s ^ ^ ^%s" % BOLT_SPEED,
        "execute positioned ~ ~-1 ~ if entity @a[distance=..1.2,%s] run return run function %s/fx/bolt_hit" % (SURV, B),
        "execute unless block ~ ~ ~ #minecraft:replaceable run return run function %s/fx/bolt_pop" % B,
    ] + every(3, "@s rpg_ub_life") + [
        "execute if score #m %s matches 0 positioned ^ ^ ^-0.6 run function %s/fx/bolt_trail" % (O, B),
        "particle minecraft:enchant ~ ~ ~ 0.1 0.1 0.1 0.6 2",
    ])
    w("fx/bolt_trail", twinkle("~ ~ ~"))
    w("fx/bolt_hit", [
        "execute positioned ~ ~-1 ~ run " + hit("distance=..1.2", BOLT_DMG),
        "function %s/fx/bolt_pop" % B,
    ])
    w("fx/bolt_pop", glyph("pop", 1.4, LAVENDER, kind="pop") + twinkle("~0.3 ~0.2 ~", frame=2) + twinkle("~-0.3 ~-0.2 ~0.2", frame=0) + [
        "particle minecraft:enchant ~ ~ ~ 0.3 0.3 0.3 1 16",
        "playsound minecraft:item.book.page_turn hostile @a[distance=..16] ~ ~ ~ 0.8 1.4",
        "kill @s",
    ])

    # ---- 普攻：书页弹；贴身时书页横扫
    w("basic/1", [
        "# 一阶段普攻（as/at 载体）：远处射书页弹，贴身就横扫",
        "function %s/anim/enter/attack" % LOOK,
        "scoreboard players set @s rpg_ub_busy %d" % CLIP_BUSY["attack"],
        "execute if entity @a[distance=..%s,%s] run return run function %s/basic/sweep" % (SWEEP_RANGE, SURV, B),
        "execute facing entity @p[distance=..%d,%s] eyes positioned ^ ^1.6 ^0.8 run %s" % (
            BASIC_RANGE, SURV, disp("rpg:usurper/paper1", scale=8, color=0xF4E9FF, tags=("rpg.usb.bolt",),
                                     lrot="[0f,0.70710677f,0f,0.70710677f]")),     # 书页本是 YZ 平面：转 90° 正对飞行方向
        "execute as @e[tag=rpg.usb.fxnew] at @s run tp @s ~ ~ ~ facing entity @p[distance=..%d,%s] eyes" % (BASIC_RANGE + 2, SURV),
    ] + born(BOLT_LIFE) + [
        "execute facing entity @p[distance=..%d,%s] eyes positioned ^ ^1.6 ^0.8 run function %s/basic/flash" % (BASIC_RANGE, SURV, B),
    ])
    w("basic/flash", glyph("pop", 0.9, PURPLE_HEX, kind="pop"))
    w("basic/sweep", [
        "# 书页横扫：身前一道原作的弧光（贴在胸口高度，朝他面向的方向）",
        "execute positioned ^ ^ ^1.5 run " + hit("distance=..2.4", SWEEP_DMG),
        "execute positioned ^ ^1.1 ^1.2 run %s" % disp("%s/crescent" % FX, scale=(1, 1, 1), color=color_int(LAVENDER)),
        "execute as @e[tag=rpg.usb.fxnew] positioned as @s run tp @s ~ ~ ~ ~ 0",
    ] + born(None, "sweep") + [
        "particle minecraft:enchant ^ ^1 ^1.5 1 0.3 1 1 24",
        "playsound minecraft:item.book.page_turn hostile @a[distance=..16] ~ ~ ~ 1 0.8",
    ])

    # ---- 七十二柱召役：血线 100/75/50/25 各召一波，每波 2 名，场上最多 4 名
    one = ["# 从七柱 35 名罪仆里随机召一名（at 召唤点），记进篡夺者的召役；脚下是那一柱颜色的漩涡与法阵",
           "execute store result score #r %s run random value 0..34" % O]
    for li, (lord, spirits) in enumerate(LORD_SPIRITS):
        for si, sp in enumerate(spirits):
            one.append("execute if score #r %s matches %d run function rpg:minion/summon/%s/%s" % (O, li * 5 + si, lord, sp))
    one.append("tag @e[tag=rpg.demon.minion,tag=!rpg.usb.unit,distance=..3,limit=1,sort=nearest] add rpg.usb.unit")
    for li in range(7):
        one.append("execute if score #r %s matches %d..%d run function %s/wave/fx%d" % (O, li * 5, li * 5 + 4, B, li + 1))
        w("wave/fx%d" % (li + 1), ["# %s的颜色" % ui.pillar(li + 1)["who"]]
          + decal("swirl", 4, lit(li + 1), pos="~ ~0.03 ~", kind="spin", life=34)
          + decal("sigil", 3, lit(li + 1), pos="~ ~0.07 ~", kind="spinr", life=34)
          + decal("shock_0", 5, lit(li + 1), pos="~ ~0.11 ~", kind="shock")
          + ray("~ ~ ~", lit(li + 1)))
    one += [
        "particle minecraft:enchant ~ ~0.5 ~ 1 0.3 1 1 30",
    ]
    w("wave/one", one)
    w("wave/spawn", [
        "# 一波（as/at 载体）：场上不足 4 名才召，两侧各一名",
        "function %s/anim/enter/enchant" % LOOK,
        "scoreboard players set @s rpg_ub_busy 40",
        "execute store result score #n %s if entity @e[%s]" % (O, SERVANT),
        "execute if score #n %s matches ..%d positioned ^3.5 ^ ^1 run function %s/wave/one" % (O, UNIT_CAP - 1, B),
        "execute store result score #n %s if entity @e[%s]" % (O, SERVANT),
        "execute if score #n %s matches ..%d positioned ^-3.5 ^ ^1 run function %s/wave/one" % (O, UNIT_CAP - 1, B),
        say("七十二柱，听候所罗门之名。", name="七十二柱召役 · "),
    ])
    waves = ["# 召役血线（as/at 载体，空闲时）"]
    for i, line in enumerate(WAVE_LINES):
        waves.append("execute if score @s rpg_ub_h matches ..%d unless entity @s[tag=rpg.usb.w%d] run return run function %s/wave/at%d"
                     % (line, i, B, i))
        w("wave/at%d" % i, ["tag @s add rpg.usb.w%d" % i, "function %s/wave/spawn" % B])
    w("wave/check", waves)

    # ---- 招式时间线：rpg_ub_sk 记招式，rpg_ub_t 每刻 +1，sk/<招式> 按时刻推进
    def start(name, busy):
        return ["scoreboard players set @s rpg_ub_sk %d" % SKILL_ID[name], "scoreboard players set @s rpg_ub_t 0",
                "scoreboard players set @s rpg_ub_busy %d" % busy]
    w("sk/tick", ["scoreboard players add @s rpg_ub_t 1"] + [
        "execute if score @s rpg_ub_sk matches %d run return run function %s/sk/%s" % (i, B, n) for n, i in SKILL_ID.items()])
    w("sk/end", ["scoreboard players set @s rpg_ub_sk 0", "data merge entity @s {NoAI:0b,NoGravity:0b,Invulnerable:0b}"])

    # 所罗门封印：最近两名玩家脚下六芒星，1.5 秒后闭合
    w("skill/seal", start("seal", SEAL_DELAY + 10) + [
        "function %s/anim/enter/attack" % LOOK,
        "playsound rpg:usurper.prepare hostile @a[distance=..32] ~ ~ ~ 1 1",
        say("跪进所罗门的封印里。", name="所罗门封印 · "),
        "execute at @a[distance=..%d,%s,sort=nearest,limit=2] run function %s/seal/place" % (BASIC_RANGE, SURV, B),
    ])
    place = [marker("~ ~ ~", "rpg.usb.seal")] + born(SEAL_DELAY + 6)
    place += decal("glow", SEAL_R * 2 + 1.5, DEEP_HEX, pos="~ ~0.03 ~", life=SEAL_DELAY + 6, tags=("rpg.usb.sealv",))
    place += decal("hexagram", SEAL_R * 2 + 0.5, PURPLE, pos="~ ~0.06 ~", kind="spin", life=SEAL_DELAY + 6, tags=("rpg.usb.sealv",))
    place += decal("hexagon", SEAL_R * 2 + 1.6, PURPLE, pos="~ ~0.09 ~", kind="spinr", life=SEAL_DELAY + 6, tags=("rpg.usb.sealv",))
    for k in range(6):
        a = math.radians(60 * k + 30)
        place += glyph("rune", 0.6, LAVENDER, pos="~%.2f ~0.9 ~%.2f" % (SEAL_R * math.cos(a), SEAL_R * math.sin(a)),
                       frame=(k * 5) % 14, life=SEAL_DELAY + 1, tags=("rpg.usb.sealv",))
    place += [
        "particle minecraft:enchant ~ ~0.3 ~ %d 0.1 %d 0.5 30" % (SEAL_R, SEAL_R),
        "playsound minecraft:block.enchantment_table.use hostile @a[distance=..24] ~ ~ ~ 1 0.6",
    ]
    w("seal/place", place)
    w("sk/seal", [
        "execute if score @s rpg_ub_t matches %d as @e[type=minecraft:marker,tag=rpg.usb.seal] at @s run function %s/seal/close"
        % (SEAL_DELAY, B),
        "execute if score @s rpg_ub_t matches %d.. run function %s/sk/end" % (SEAL_DELAY + 1, B),
    ])
    close = ["# 封印闭合（as/at 封印中心）：圈内受伤，契约技能封住 8 秒；法阵收拢、冲击环炸开、圈边钻出唤魔者尖牙",
             hit("distance=..%s" % SEAL_R, SEAL_DMG)] + lock_lines("distance=..%s" % SEAL_R)
    for k in range(6):
        a = math.radians(60 * k + 30)
        close += [disp("%s/fang" % FX, pos="~%.2f ~-1.3 ~%.2f" % (SEAL_R * math.cos(a), SEAL_R * math.sin(a)), yaw=60 * k,
                       scale=1.6, color=0xFFFFFF, tags=("rpg.usb.fang",), tp=3)]
    close += born(None, "fang")
    close += [morph("tag=rpg.usb.sealv,distance=..1", 0.6, 5, decal_=True)]
    close += decal("shock_0", SEAL_R * 3, LAVENDER, pos="~ ~0.12 ~", kind="shock")
    close += decal("cracks", SEAL_R * 2, DEEP_HEX, pos="~ ~0.04 ~", life=40)
    close += glyph("burst", 3.2, LAVENDER, pos="~ ~1 ~", kind="burst")
    close += ray("~ ~ ~", PURPLE_HEX)
    close += twinkle("~1 ~1.4 ~0.5", frame=2) + twinkle("~-0.8 ~0.8 ~-0.6", frame=1) + twinkle("~0.2 ~2 ~-1", frame=0)
    close += [
        "particle minecraft:enchant ~ ~0.5 ~ %d 0.3 %d 1.5 60" % (SEAL_R, SEAL_R),
        "playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..24] ~ ~ ~ 1 0.8",
        "playsound rpg:usurper.close hostile @a[distance=..24] ~ ~ ~ 1 0.7",
        "kill @s",
    ]
    w("seal/close", close)

    # 附魔灌注：对最近的罪仆射附魔光束 6 秒；先杀掉它光束就断，他硬直 2 秒
    w("skill/infuse", [
        "# 附魔灌注（as/at 载体）。没有罪仆在近处就改用封印。",
        "execute unless entity @e[%s,distance=..%d] run return run function %s/skill/seal" % (SERVANT, INFUSE_RANGE, B),
        "tag @e[%s,distance=..%d,sort=nearest,limit=1] add rpg.usb.infused" % (SERVANT, INFUSE_RANGE),
    ] + start("infuse", INFUSE_TICKS) + [
        "data merge entity @s {NoAI:1b}",
        "function %s/anim/enter/enchant" % LOOK,
        "execute as @e[tag=rpg.usb.infused] run effect give @s minecraft:resistance %d 1 true" % (INFUSE_TICKS // 20 + 1),
        "execute as @e[tag=rpg.usb.infused] run effect give @s minecraft:speed %d 1 true" % (INFUSE_TICKS // 20 + 1),
        "execute as @e[tag=rpg.usb.infused] at @s run function %s/infuse/runes" % B,
        "# 原作附魔光束：滚动的云纹光柱，从他胸前连到罪仆，每 2 刻按距离重新拉长",
        disp("%s/beam" % FX, pos="~ ~1.5 ~", scale=(0.3, 0.3, 0.01), tags=("rpg.usb.ibeam", "rpg.usb.ifx"), tp=2),
    ] + born(INFUSE_TICKS + 5)
      + decal("swirl", 3.5, PURPLE, pos="~ ~0.04 ~", kind="spin", life=INFUSE_TICKS + 5, tags=("rpg.usb.ifx",))
      + glyph("pop", 1.2, LAVENDER, pos="~ ~1.6 ~", kind="pop") + [
        "playsound rpg:usurper.beam hostile @a[distance=..32] ~ ~ ~ 1 1",
        say("把七十二柱的力，灌给我的仆从。", name="附魔灌注 · "),
    ])
    runes = []
    for r, tr in ((3, (0.7, -0.5, 0)), (7, (-0.7, -0.2, 0)), (11, (0, 0.4, 0))):
        runes += glyph("rune", 0.55, LAVENDER, frame=r, tags=("rpg.usb.irune", "rpg.usb.ifx"), trans=tr, born_now=False)
    w("infuse/runes", ["# 被灌注的罪仆身上绕三枚原作符文（骑在它身上）"] + runes + [
        "execute as @e[tag=rpg.usb.fxnew,tag=rpg.usb.irune] run ride @s mount @e[tag=rpg.usb.infused,limit=1,sort=nearest]",
    ] + born(INFUSE_TICKS + 20))
    w("infuse/beam", [
        "# 光束（as 被灌注的罪仆，at 他胸前并朝向它）：量出距离，拉长到那里",
        "scoreboard players set #d %s 0" % O,
        "function %s/infuse/step" % B,
        "execute as @e[tag=rpg.usb.ibeam,limit=1] run tp @s ~ ~ ~ ~ ~",
        "execute as @e[tag=rpg.usb.ibeam,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:2}",
        "execute as @e[tag=rpg.usb.ibeam,limit=1] store result entity @s transformation.scale[2] float 1 run scoreboard players get #d %s" % O,
        "execute as @e[tag=rpg.usb.ibeam,limit=1] store result entity @s transformation.translation[2] float 0.5 run scoreboard players get #d %s" % O,
    ])
    w("infuse/step", [
        "scoreboard players add #d %s 1" % O,
        "execute if entity @s[distance=..1.2] run return 0",
        "execute positioned ~ ~-1.4 ~ if entity @s[distance=..1.2] run return 0",
        "execute if score #d %s matches ..%d positioned ^ ^ ^1 run function %s/infuse/step" % (O, INFUSE_RANGE + 4, B),
    ])
    beam = ["execute if score @s rpg_ub_t matches %d.. run return run function %s/infuse/end" % (INFUSE_TICKS, B),
            "execute unless entity @e[tag=rpg.usb.infused] run return run function %s/infuse/broken" % B] + every(2) + [
        "execute if score #m %s matches 0 as @e[tag=rpg.usb.infused,limit=1] positioned ~ ~1.5 ~ facing entity @s eyes "
        "run function %s/infuse/beam" % (O, B)]
    beam += every(6) + ["execute if score #m %s matches 0 at @e[tag=rpg.usb.infused,limit=1] run function %s/infuse/spark" % (O, B)]
    beam.append("execute if score @s rpg_ub_t matches 20 run playsound rpg:usurper.beam_loop hostile @a[distance=..32] ~ ~ ~ 0.8 1")
    beam.append("execute if score @s rpg_ub_t matches 60 run playsound rpg:usurper.beam_loop hostile @a[distance=..32] ~ ~ ~ 0.8 1")
    w("sk/infuse", beam)
    w("infuse/spark", twinkle("~0.4 ~1.8 ~", frame=1) + ["particle minecraft:enchant ~ ~1 ~ 0.3 0.6 0.3 1 6"])
    w("infuse/end", [
        "tag @e[tag=rpg.usb.infused] remove rpg.usb.infused",
        "kill @e[tag=rpg.usb.ifx]",
        "playsound rpg:usurper.chime hostile @a[distance=..24] ~ ~ ~ 1 1",
        "function %s/sk/end" % B,
    ] + glyph("pop", 1.2, LAVENDER, pos="~ ~1.6 ~", kind="pop"))
    w("infuse/broken", [
        "# 被灌注的罪仆先倒下：光束断开，他硬直 2 秒",
        "kill @e[tag=rpg.usb.ifx]",
    ] + start("stagger", INFUSE_STAGGER) + [
        "data merge entity @s {NoAI:1b}",
    ] + glyph("burst", 2.6, LAVENDER, pos="~ ~1.6 ~", kind="burst")
      + decal("shock_0", 5, PURPLE, pos="~ ~0.1 ~", kind="shock") + [
        "particle minecraft:enchant ~ ~1.5 ~ 0.5 0.8 0.5 2 40",
        "playsound minecraft:block.glass.break hostile @a[distance=..24] ~ ~ ~ 1 0.6",
        say("……断了？", name=""),
    ])
    w("sk/stagger", every(8) + [
        "execute if score #m %s matches 0 run function %s/stagger_star" % (O, B),
        "execute if score @s rpg_ub_t matches %d.. run function %s/sk/end" % (INFUSE_STAGGER, B),
    ])
    w("stagger_star", twinkle("~0.3 ~2.5 ~", frame=2) + twinkle("~-0.3 ~2.3 ~0.2", frame=0))

    # 契约改写：签了七罪契约的玩家，10 秒内每用一次契约技能魔化 +5
    w("skill/rewrite", [
        "# 契约改写（as/at 载体）。没人签契约就改用封印。",
        "execute unless entity @a[distance=..%d,%s,scores={rpg_pact=1..7}] run return run function %s/skill/seal" % (BASIC_RANGE, SURV, B),
    ] + start("rewrite", 30) + [
        "function %s/anim/enter/enchant" % LOOK,
        "execute as @a[distance=..%d,%s,scores={rpg_pact=1..7}] at @s run function %s/rewrite/mark" % (BASIC_RANGE, SURV, B),
        say("你们的契约，我替你们重写一遍。", name="契约改写 · "),
    ] + glyph("pop", 1.2, LAVENDER, pos="~ ~1.8 ~", kind="pop"))
    w("sk/rewrite", ["execute if score @s rpg_ub_t matches 20.. run function %s/sk/end" % B])
    w("rewrite/mark", [
        "tag @s add rpg.usb.rw",
        "scoreboard players set @s rpg_ub_rw %d" % REWRITE_TICKS,
        "function %s/rewrite/sync" % B,
    ] + glyph("rune", 0.9, LAVENDER, pos="~ ~2.5 ~", frame=6, life=24)
      + glyph("pop", 1.4, PURPLE_HEX, pos="~ ~2.5 ~", kind="pop")
      + decal("ring", 2.6, PURPLE, pos="~ ~0.05 ~", life=24) + [
        "particle minecraft:enchant ~ ~2 ~ 0.4 0.4 0.4 1 24",
        "playsound minecraft:block.enchantment_table.use hostile @s ~ ~ ~ 1 0.5",
    ])
    w("rewrite/sync", [
        "scoreboard players operation @s rpg_ub_p1 = @s rpg_pact_cd",
        "scoreboard players operation @s rpg_ub_p2 = @s rpg_pact_cd2",
        "scoreboard players operation @s rpg_ub_p3 = @s rpg_pact_cd3",
    ])
    w("rewrite/tick", [
        "# 被改写的玩家（as 玩家）：任一契约冷却被重新设高，就是刚用了契约技能",
        "scoreboard players remove @s rpg_ub_rw 1",
        "execute if score @s rpg_pact_cd > @s rpg_ub_p1 run function %s/rewrite/backlash" % B,
        "execute if score @s rpg_pact_cd2 > @s rpg_ub_p2 run function %s/rewrite/backlash" % B,
        "execute if score @s rpg_pact_cd3 > @s rpg_ub_p3 run function %s/rewrite/backlash" % B,
        "function %s/rewrite/sync" % B,
    ] + every(20, "@s rpg_ub_rw") + [
        "execute if score #m %s matches 0 at @s run function %s/rewrite/mote" % (O, B),
        "execute if score @s rpg_ub_rw matches ..0 run function %s/rewrite/clear" % B,
    ])
    w("rewrite/mote", glyph("rune", 0.5, PURPLE_HEX, pos="~ ~2.4 ~", frame=11, life=12) + [
        "particle %s ~ ~2.3 ~ 0.3 0.05 0.3 0 3" % ui.dust(PURPLE_HEX, 0.9)])
    w("rewrite/backlash", [
        "scoreboard players add @s rpg_taint %d" % REWRITE_TAINT,
        "execute at @s run function %s/rewrite/backlash_fx" % B,
    ])
    w("rewrite/backlash_fx", glyph("burst", 1.8, WARN_HEX, pos="~ ~1.2 ~", kind="burst") + [
        "particle minecraft:enchant ~ ~1 ~ 0.4 0.6 0.4 1.5 30",
        "playsound minecraft:block.enchantment_table.use hostile @s ~ ~ ~ 1 1.6",
    ])
    w("rewrite/clear", ["tag @s remove rpg.usb.rw", "scoreboard players reset @s rpg_ub_rw"])

    # ---- 大招：七十二柱环
    ring = ["# 七十二柱环（as/at 载体）：七十二枚原作符文绕身一圈（字形，暗色），七段依次亮起、朝圈心射光；已经射过的扇区安全"]
    for i in range(RING_N):
        a = 2 * math.pi * i / RING_N
        seg = i * RING_SEG // RING_N
        ring += glyph("rune", 0.75, ui.pillar(seg + 1)["deep"], pos="~%.2f ~1.6 ~%.2f" % (RING_R * math.cos(a), RING_R * math.sin(a)),
                      frame=i % 14, tags=("rpg.usb.ring", "rpg.usb.rs%d" % seg), born_now=False)
    ring_len = RING_WIND + RING_SEG * RING_GAP
    w("ult/ring", start("ring", ring_len + 20) + [
        "data merge entity @s {NoAI:1b}",
        "function %s/anim/enter/enchant" % LOOK,
        say("", gloss=True, name="七十二柱环"),
    ] + ring + born(ring_len + 30)
      + decal("ring", RING_R * 2, PURPLE, pos="~ ~0.04 ~", life=ring_len + 30, tags=("rpg.usb.ringv",))
      + decal("glow", RING_R * 2 + 2, DEEP_HEX, pos="~ ~0.02 ~", life=ring_len + 30, tags=("rpg.usb.ringv",))
      + decal("swirl", 5, PURPLE, pos="~ ~0.07 ~", kind="spin", life=ring_len + 30, tags=("rpg.usb.ringv",))
      + glyph("burst", 3, LAVENDER, pos="~ ~1.6 ~", kind="burst") + [
        "playsound minecraft:block.enchantment_table.use hostile @a[distance=..32] ~ ~ ~ 1.4 0.5",
        "playsound rpg:usurper.spell hostile @a[distance=..32] ~ ~ ~ 1.2 0.8",
    ])
    sk_ring = []
    for seg in range(RING_SEG):
        t = RING_WIND + seg * RING_GAP
        col = lit(seg + 1)
        # 扇区中线方向 (cos a, sin a)；Minecraft 偏航角的朝向是 (-sin y, cos y)，所以 y = a - 90°
        mid = (seg + 0.5) * 360.0 / RING_SEG
        yaw = (mid - 90) % 360
        sk_ring.append("execute if score @s rpg_ub_t matches %d run function %s/ring/light%d" % (t - 12, B, seg))
        sk_ring.append("execute if score @s rpg_ub_t matches %d run function %s/ring/fire%d" % (t, B, seg))
        k_lit = gscale("rune", 1.25)
        w("ring/light%d" % seg, [
            "# 第 %d 段（%s）亮起：符文换亮色、放大，预警 0.6 秒" % (seg + 1, ui.pillar(seg + 1)["who"]),
            "execute as @e[tag=rpg.usb.rs%d] run data modify entity @s text.color set value \"%s\"" % (seg, col),
            "execute as @e[tag=rpg.usb.rs%d] run data merge entity @s {start_interpolation:0,interpolation_duration:6,"
            "transformation:{scale:[%gf,%gf,%gf]}}" % (seg, k_lit, k_lit, k_lit),
            "execute rotated %.1f 0 positioned ^ ^ ^%d run function %s/ring/warn%d" % (yaw, RING_R, B, seg),
            "playsound rpg:usurper.chime hostile @a[distance=..32] ~ ~ ~ 1 %.2f" % (0.7 + 0.1 * seg),
        ])
        w("ring/warn%d" % seg, ray("~ ~ ~", col) + twinkle("~ ~2.2 ~", col, 2) + [
            "particle %s ~ ~1.6 ~ 1.5 0.5 1.5 0 16 force" % ui.pillar_dust(seg + 1, 1.6)])
        fire = ["# 第 %d 段射出：一道原作光束从圈上射向圈心，这一扇区里的人受伤" % (seg + 1)]
        fire += ["execute positioned ~ ~1.4 ~ run %s" % disp("%s/beam" % FX, scale=(0.5, 0.5, RING_R), color=color_int(col),
                                                             trans=(0, 0, RING_R / 2.0), yaw=yaw)] + born(None, "sbeam")
        fire += ["execute rotated %.1f 0 positioned ^ ^ ^%g run function %s/ring/blast%d" % (yaw, RING_R * 0.55, B, seg)]
        w("ring/blast%d" % seg, decal("shock_0", 7, col, pos="~ ~0.1 ~", kind="shock")
          + glyph("pop", 2.2, col, pos="~ ~1.4 ~", kind="pop"))
        # 扇区（约 51°）用一串沿中线的圆近似，一直铺到战场边
        for dist, rad in ((2.5, 2.0), (5.5, 2.8), (8.5, 3.6), (12, 4.6), (17, 6.2), (23, 8.2)):
            fire.append("execute rotated %.1f 0 positioned ^ ^ ^%s run tag @a[distance=..%s,%s] add rpg.usb.hit" % (yaw, dist, rad, SURV))
        fire += [
            "execute as @a[tag=rpg.usb.hit,distance=..%d] run damage @s %d minecraft:magic by @e[%s,limit=1]" % (ARENA, RING_DMG, UNIT),
            "tag @a[tag=rpg.usb.hit] remove rpg.usb.hit",
            "kill @e[tag=rpg.usb.rs%d]" % seg,
            "playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..32] ~ ~ ~ 1 %.2f" % (0.8 + 0.08 * seg),
        ]
        w("ring/fire%d" % seg, fire)
    sk_ring.append("execute if score @s rpg_ub_t matches %d.. run function %s/ring/done" % (ring_len + 10, B))
    w("sk/ring", sk_ring)
    w("ring/done", ["kill @e[tag=rpg.usb.ringv]", "function %s/sk/end" % B])

    # ---- 大招：所罗门之钥
    safes = []
    for k in range(6):
        a = math.radians(90 + 60 * k)
        x, z = KEY_SAFE_D * math.cos(a), KEY_SAFE_D * math.sin(a)
        p = "~%.2f ~ ~%.2f" % (x, z)
        safes += [marker(p, "rpg.usb.safe")] + born(KEY_DELAY + 12)
        safes += decal("sigil", KEY_SAFE_R * 2, WHITE_GOLD[0], pos="~%.2f ~0.12 ~%.2f" % (x, z), kind="spin", life=KEY_DELAY + 12,
                       tags=("rpg.usb.keyv",))
        safes += decal("ring", KEY_SAFE_R * 2 + 0.4, WHITE_GOLD[1], pos="~%.2f ~0.15 ~%.2f" % (x, z), life=KEY_DELAY + 12,
                       tags=("rpg.usb.keyv",))
        safes += ray(p, WHITE_GOLD[0], long=True)
    w("ult/key", start("key", KEY_DELAY + KEY_KNEEL + 10) + [
        "# 所罗门之钥（as/at 载体）：脚下巨大的六芒星，六个角上各一个白金安全圈（光柱标出）；4 秒后爆开，之后他跪地 3 秒、护甲归零",
        "data merge entity @s {NoAI:1b}",
        "function %s/anim/enter/enchant" % LOOK,
        say("", gloss=True, name="所罗门之钥"),
    ] + decal("glow", KEY_R * 2 + 2, DEEP_HEX, pos="~ ~0.02 ~", life=KEY_DELAY + 12, tags=("rpg.usb.keyv",))
      + decal("hexagram", KEY_R * 2, PURPLE, pos="~ ~0.05 ~", life=KEY_DELAY + 12, tags=("rpg.usb.keyv", "rpg.usb.keyhex"))
      + decal("hexagon", KEY_R * 2 + 2, PURPLE, pos="~ ~0.08 ~", kind="spinr", life=KEY_DELAY + 12, tags=("rpg.usb.keyv",))
      + decal("swirl", 6, LAVENDER, pos="~ ~0.1 ~", kind="spin", life=KEY_DELAY + 12, tags=("rpg.usb.keyv",))
      + safes + [
        "playsound minecraft:block.end_portal.spawn hostile @a[distance=..40] ~ ~ ~ 0.8 1.4",
        "playsound rpg:usurper.prepare hostile @a[distance=..40] ~ ~ ~ 1.2 0.7",
    ])
    w("sk/key", every(10) + [
        "execute if score @s rpg_ub_t matches ..%d if score #m %s matches 0 run particle %s ~ ~0.3 ~ %d 0.1 %d 0 40 force"
        % (KEY_DELAY, O, ui.dust(PURPLE_HEX, 1.5), KEY_R // 2, KEY_R // 2),
        "execute if score @s rpg_ub_t matches ..%d if score #m %s matches 5 run function %s/key/mote" % (KEY_DELAY - 10, O, B),
        "execute if score @s rpg_ub_t matches %d run %s" % (KEY_DELAY - 20, morph("tag=rpg.usb.keyhex", KEY_R * 2 + 2, 20, decal_=True)),
        "execute if score @s rpg_ub_t matches %d run function %s/key/burst" % (KEY_DELAY, B),
        "execute if score @s rpg_ub_t matches %d..%d if score #m %s matches 0 run function %s/stagger_star" % (KEY_DELAY + 1, KEY_DELAY + KEY_KNEEL, O, B),
        "execute if score @s rpg_ub_t matches %d run function %s/key/rise" % (KEY_DELAY + KEY_KNEEL, B),
        "execute if score @s rpg_ub_t matches %d.. run function %s/sk/end" % (KEY_DELAY + KEY_KNEEL + 1, B),
    ])
    w("key/mote", ["# 六芒星上冒起的星芒"] + twinkle("~4 ~0.6 ~3", PURPLE_HEX, 1) + twinkle("~-5 ~0.6 ~-2", PURPLE_HEX, 2)
      + twinkle("~1 ~0.6 ~-6", PURPLE_HEX, 0))
    burst = [
        "# 爆开（as/at 载体）：圈内、安全圈外的人受伤；他跪地，护甲归零",
        "execute as @e[type=minecraft:marker,tag=rpg.usb.safe] at @s run tag @a[distance=..%s] add rpg.usb.safe" % KEY_SAFE_R,
        hit("distance=..%d,tag=!rpg.usb.safe" % ARENA, KEY_DMG),     # 站远也躲不掉，只有安全圈
        "tag @a remove rpg.usb.safe",
        "kill @e[tag=rpg.usb.keyv]",
        "kill @e[type=minecraft:marker,tag=rpg.usb.safe]",
        "particle minecraft:flash{color:%d} ~ ~1 ~ 0 0 0 0 1 force" % PURPLE,
    ] + decal("shock_0", KEY_R * 2 + 4, LAVENDER, pos="~ ~0.12 ~", kind="shock") \
      + decal("cracks", 9, DEEP_HEX, pos="~ ~0.05 ~", life=60) \
      + glyph("burst", 7, LAVENDER, pos="~ ~2 ~", kind="burst") \
      + glyph("pop", 3, PURPLE_HEX, pos="~ ~1 ~", kind="pop")
    for k in range(8):
        a = math.radians(45 * k + 20)
        burst += twinkle("~%.1f ~%.1f ~%.1f" % (6 * math.cos(a), 0.8 + (k % 3) * 0.6, 6 * math.sin(a)), LAVENDER, k % 3)
    burst += [
        "particle minecraft:enchant ~ ~1 ~ %d 0.5 %d 2 200 force" % (KEY_R // 2, KEY_R // 2),
        "playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1.2 0.7",
        "playsound rpg:usurper.close hostile @a[distance=..40] ~ ~ ~ 1.4 0.6",
        "attribute @s minecraft:armor base set 0",
        say("……", name=""),
    ]
    w("key/burst", burst)
    w("key/rise", ["attribute @s minecraft:armor base set %d" % ARMOR, "function %s/anim/enter/rise" % LOOK])


# =====================================================================================
# 二阶段：篡夺圣灵（首席附魔师，设计稿第 4、6 节）。
# 模型：add_prime_enchanter_model.py（rpg:prime_enchanter，11 段原作动作）；冰电改白金、帽顶王冠在
# add_usurper_holy_look.py。变身时把首席附魔师的部件挪到篡夺者的载体上（look2/swap），载体打上
# rpg.usb.s2 与 rpg.prime_enchanter，动作由它自己的运行时播放，这里只调 anim/enter/<clip>。
# 出手时刻取自 prime_enchanter_ref/sockets.json 的事件帧（连拳 15/28/79、砸地 110，前冲 30，
# 天降隐身 23–43、落地 44，雷霆砸地 53，召唤举拳 12）。
# 特效素材：原作电弧、直闪电、弧光、方形冲击环（SM_SquareDonut 序列）、虚空风暴闪电网、
# 地卜师石柱（圣坛）、不死图腾、商人王冠（add_usurper_fx_art.py）。
# =====================================================================================
PE = "rpg:prime_enchanter"
WG_L, WG_M, WG_D = ui.WHITE_GOLD
WG = color_int(WG_M)
WGL = color_int(WG_L)
S2_ID = {"fist": 10, "launch": 11, "strike": 12, "slam": 13, "summon": 14, "over": 15, "judge": 16}
SKILL_ID.update(S2_ID)
PE_K = 1.15 / 16                      # 首席附魔师模型单位 -> 格（sockets.json：[-x,y,-z] × 1.15/16）
HEAD = "execute on passengers if entity @s[tag=rpg.prime_enchanter.p.head] run "
GUARDS = "tag=rpg.usb.guard"

FIST_RANGE, FIST_DMG, FIST_SLAM_DMG, FIST_SLAM_R = 4.5, 6, 10, 3
FIST_HITS, FIST_SLAM, FIST_LEN = (15, 28, 79), 110, 138
LAUNCH_MARK, LAUNCH_UP, LAUNCH_DOWN, LAUNCH_HIT, LAUNCH_LEN = 20, 23, 43, 44, 79
LAUNCH_R, LAUNCH_DMG = 4, 14
STRIKE_GO, STRIKE_STEPS, STRIKE_STEP, STRIKE_DMG, STRIKE_LEN = 26, 11, 1.1, 8, 50
SLAM_HIT, SLAM_SPEED, SLAM_R, SLAM_DMG = 53, 0.35, 20, 10
SLAM_TICKS = int(SLAM_R / SLAM_SPEED)                  # 57 刻扩到 20 格
SLAM_LEN = SLAM_HIT + SLAM_TICKS + 2
AUTH_AT, AUTH_LEN = 12, 45
WEAK_GUARDS, WEAK_ULT = 120, 80                        # 圣卫全倒 6 秒、大招后 4 秒
OVER_LEN, OVER_END, OVER_WAVES, OVER_WARN, OVER_DMG = 140, 120, (40, 65, 90, 115), 12, 10
ALTARS = ((6, 6), (-7, 6), (6, -7), (-7, -7))          # 圣坛 2×2，对齐方块角
JUDGE_OFF, JUDGE_T0, JUDGE_GAP, JUDGE_TELE, JUDGE_LEN, JUDGE_DMG = (0, -24, 24, -48, 48), 30, 10, 14, 20, 16
CROWN_DIM, CROWN_FLICK = 0x3C3428, 0x8A7240


def anim2(clip):
    return "function %s/anim/enter/%s" % (PE, clip)


def start2(name, busy):
    return ["scoreboard players set @s rpg_ub_sk %d" % SKILL_ID[name], "scoreboard players set @s rpg_ub_t 0",
            "scoreboard players set @s rpg_ub_busy %d" % busy]


def face(r=BASIC_RANGE):
    return "execute facing entity @p[distance=..%s,%s] feet run tp @s ~ ~ ~ ~ 0" % (r, SURV)


def crown(colour):
    return HEAD + "data modify entity @s item.components.\"minecraft:custom_model_data\" set value {colors:[%d]}" % colour


def sock(x, y, z):
    return "^%.2f ^%.2f ^%.2f" % (-x * PE_K, y * PE_K, -z * PE_K)


def spark(pos, colour=WG_L, size=0.9, frame=0, kind="spark"):
    return glyph("spark", size, colour, pos=pos, frame=frame, kind=kind)


def bolt(pos="~ ~ ~", colour=WG_L):
    return glyph("bolt", BOLT_W, colour, pos=pos, kind="bolt", billboard="vertical", start=(BOLT_K, BOLT_H, BOLT_K),
                 trans=(0, BOLT_W * 2, 0))


def tick_at(t, fn):
    return "execute if score @s rpg_ub_t matches %d run function %s/%s" % (t, B, fn)


def stage2():
    import math

    # ---- 伤害：圣卫在场 -50%，破绽 +50%（每 4 刻读血时把这段的伤害退回或补上，同教皇外壳）
    w("s2/scale", [
        "# 二阶段读血前（as 载体）：Health×10 和上次比，少了就按状态退回一半或再扣一半",
        "execute store result score #hp %s run data get entity @s Health 10" % O,
        "scoreboard players operation #lost %s = @s rpg_ub_l" % O,
        "scoreboard players operation #lost %s -= #hp %s" % (O, O),
        "execute if score #lost %s matches 1.. run function %s/s2/hurt" % (O, B),
        "execute store result score @s rpg_ub_l run data get entity @s Health 10",
    ])
    w("s2/hurt", [
        "# 二阶段没有原作原声（首席附魔师没有可用原件）：受击用原版唤魔者的声音压低",
        "playsound minecraft:entity.evoker.hurt hostile @a[distance=..32] ~ ~ ~ 1 0.7",
        "playsound minecraft:block.amethyst_block.hit hostile @a[distance=..32] ~ ~ ~ 0.6 0.8",
        "# 致命一击可能刚吃掉副手的死亡保护：补回去，下次照样挡",
        "item replace entity @s weapon.offhand with %s" % GUARD,
        "scoreboard players operation #lost %s /= #two %s" % (O, O),
        "execute if entity @s[tag=rpg.usb.exposed] run return run function %s/s2/extra" % B,
        "execute if entity @e[%s,distance=..%d] run function %s/s2/refund" % (GUARDS, ARENA * 3, B),
    ])
    w("s2/refund", [
        "# 有权无力：命令有人执行，他难以撼动",
        "scoreboard players operation #hp %s += #lost %s" % (O, O),
        "execute store result entity @s Health float 0.1 run scoreboard players get #hp %s" % O,
    ])
    w("s2/extra", [
        "# 破绽：权柄没有执行者，伤害加一半（至少留 1 血，交给切段判定）",
        "scoreboard players operation #hp %s -= #lost %s" % (O, O),
        "execute if score #hp %s matches ..10 run scoreboard players set #hp %s 10" % (O, O),
        "execute store result entity @s Health float 0.1 run scoreboard players get #hp %s" % O,
    ])

    # ---- 每刻（as/at 载体）：权柄线、圣卫是否全倒、破绽
    w("s2/tick", every(2, "#tick %s" % O) + [
        "execute if score #m %s matches 0 as @e[%s,distance=..%d] at @s run function %s/auth/line" % (O, GUARDS, ARENA * 2, B),
        "execute if score #m %s matches 0 as @e[tag=rpg.usb.abeam] run function %s/auth/check" % (O, B),
        "execute if entity @s[tag=rpg.usb.guarded] unless entity @e[%s,distance=..%d] run function %s/auth/fall" % (GUARDS, ARENA * 3, B),
        "execute if entity @s[tag=rpg.usb.exposed] run function %s/weak/tick" % B,
    ] + every(160, "#tick %s" % O) + [
        "execute if score #m %s matches 0 if score @s rpg_ub_busy matches ..0 run playsound minecraft:entity.evoker.ambient "
        "hostile @a[distance=..32] ~ ~ ~ 1 0.7" % O,
    ])

    # ---- 普攻：连拳（贴身才出；远了就继续走过去）
    w("basic/2", [
        "# 二阶段普攻（as/at 载体）：连拳三下，再跃起双拳砸地",
        "execute unless entity @a[distance=..%s,%s] run return 0" % (FIST_RANGE, SURV),
    ] + start2("fist", FIST_LEN) + ["data merge entity @s {NoAI:1b}", face(FIST_RANGE + 1), anim2("fury_fist")])
    w("sk/fist", [tick_at(t, "fist/punch") for t in FIST_HITS] + [
        tick_at(FIST_SLAM - 12, "fist/leap"),
        tick_at(FIST_SLAM, "fist/slam"),
        "execute if score @s rpg_ub_t matches %d.. run function %s/sk/end" % (FIST_LEN, B),
    ])
    w("fist/punch", [
        face(6),
        "execute at @s if block ^ ^0.5 ^0.6 #minecraft:replaceable if block ^ ^1.5 ^0.6 #minecraft:replaceable run tp @s ^ ^ ^0.6",
        "execute at @s positioned ^ ^ ^1.6 run " + hit("distance=..1.8", FIST_DMG),
        "execute at @s positioned ^ ^1.3 ^1.5 run function %s/fist/punch_fx" % B,
        "playsound minecraft:entity.player.attack.strong hostile @a[distance=..24] ~ ~ ~ 1 0.7",
        "playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..24] ~ ~ ~ 0.4 1.8",
    ])
    w("fist/punch_fx", glyph("slash", 2.2, WG_M, kind="slashfx") + spark("~0.3 ~0.2 ~", frame=3)
      + glyph("pop", 1.0, WG_L, kind="pop") + ["particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.3 12"])
    w("fist/leap", ["execute at @s positioned %s run function %s/fist/charge" % (sock(-1.5, 25, -11), B)])
    w("fist/charge", spark("~ ~ ~", frame=5) + spark("~0.3 ~0.3 ~", frame=9)
      + ["particle minecraft:electric_spark ~ ~ ~ 0.2 0.2 0.2 0.4 10"])
    w("fist/slam", [
        "# 双拳砸地（at 载体）：3 格内 10",
        hit("distance=..%d" % FIST_SLAM_R, FIST_SLAM_DMG),
    ] + decal("sq_0", FIST_SLAM_R * 2 + 1, WG_L, pos="~ ~0.1 ~", kind="sq")
      + decal("shock_0", FIST_SLAM_R * 2 + 2, WG_M, pos="~ ~0.13 ~", kind="shock")
      + decal("cracks", 4, WG_D, pos="~ ~0.05 ~", life=40)
      + glyph("burst", 2.6, WG_L, pos="~ ~0.8 ~", kind="burst")
      + spark("~1 ~0.4 ~", frame=1) + spark("~-1 ~0.4 ~0.3", frame=6) + [
        "particle minecraft:electric_spark ~ ~0.3 ~ 1.2 0.2 1.2 0.5 40",
        "playsound minecraft:item.mace.smash_ground_heavy hostile @a[distance=..32] ~ ~ ~ 1 0.9",
    ])

    # ---- 天降：消失（原作动作 23–43 刻部件自己藏起），从目标头顶砸下；落点白金光柱标 1.2 秒
    w("skill/launch", start2("launch", LAUNCH_LEN + 2) + [
        "data merge entity @s {NoAI:1b}", face(), anim2("launch"),
        "playsound minecraft:entity.breeze.jump hostile @a[distance=..32] ~ ~ ~ 1.2 0.6",
        say("……从天上。", name="天降 · ", stage=2),
    ])
    w("sk/launch", [
        "execute if score @s rpg_ub_t matches %d at @r[distance=..%d,%s] run function %s/launch/mark" % (LAUNCH_MARK, BASIC_RANGE, SURV, B),
        "execute if score @s rpg_ub_t matches %d unless entity @e[type=minecraft:marker,tag=rpg.usb.land] run function %s/launch/mark" % (LAUNCH_MARK, B),
        "execute if score @s rpg_ub_t matches %d run data merge entity @s {Invulnerable:1b,NoGravity:1b}" % LAUNCH_UP,
        "execute if score @s rpg_ub_t matches %d at @s run tp @s ~ ~14 ~" % LAUNCH_UP,
        "execute if score @s rpg_ub_t matches %d at @e[type=minecraft:marker,tag=rpg.usb.land,limit=1] run tp @s ~ ~ ~" % LAUNCH_DOWN,
        "execute if score @s rpg_ub_t matches %d at @s run function %s/launch/land" % (LAUNCH_HIT, B),
        "execute if score @s rpg_ub_t matches %d.. run function %s/sk/end" % (LAUNCH_LEN, B),
    ])
    w("launch/mark", [
        "# 落点（at 目标脚下）：白金光柱、法阵、光环",
        marker("~ ~ ~", "rpg.usb.land")] + born(LAUNCH_HIT - LAUNCH_MARK + 6)
      + decal("glow", LAUNCH_R * 2 + 1, WG_D, pos="~ ~0.03 ~", life=30, tags=("rpg.usb.landv",))
      + decal("sigil", LAUNCH_R * 2 - 1, WG_L, pos="~ ~0.07 ~", kind="spin", life=30, tags=("rpg.usb.landv",))
      + decal("ring", LAUNCH_R * 2, WG_M, pos="~ ~0.1 ~", life=30, tags=("rpg.usb.landv",))
      + ray("~ ~ ~", WG_L, long=True, tags=("rpg.usb.landv",)) + [
        "playsound minecraft:block.beacon.activate hostile @a[distance=..32] ~ ~ ~ 1 1.6",
    ])
    w("launch/land", [
        "# 砸地（at 落点）：4 格内 14；方形冲击环是原作 SM_SquareDonut 的序列",
        "data merge entity @s {Invulnerable:0b,NoGravity:0b}",
        hit("distance=..%d" % LAUNCH_R, LAUNCH_DMG),
        "kill @e[tag=rpg.usb.landv]",
        "kill @e[type=minecraft:marker,tag=rpg.usb.land]",
    ] + decal("sq_0", LAUNCH_R * 2 + 2, WG_L, pos="~ ~0.1 ~", kind="sq")
      + decal("shock_0", LAUNCH_R * 2 + 4, WG_M, pos="~ ~0.13 ~", kind="shock")
      + decal("cracks", 6, WG_D, pos="~ ~0.05 ~", life=40)
      + glyph("burst", 4, WG_L, pos="~ ~1 ~", kind="burst") + glyph("pop", 2, WG_M, pos="~ ~0.5 ~", kind="pop")
      + spark("~1.5 ~0.5 ~", frame=2) + spark("~-1.4 ~0.6 ~0.8", frame=7) + spark("~0.2 ~0.4 ~-1.6", frame=12) + [
        "particle minecraft:flash{color:%d} ~ ~1 ~ 0 0 0 0 1 force" % WGL,
        "particle minecraft:electric_spark ~ ~0.3 ~ 2 0.2 2 0.6 60",
        "playsound minecraft:item.mace.smash_ground_heavy hostile @a[distance=..40] ~ ~ ~ 1.4 0.7",
        "playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..40] ~ ~ ~ 1 1",
    ])

    # ---- 圣光突进：朝目标直线冲 12 格，沿途每 2 格炸开一团白金光（每次突进每人只挨一下）
    w("skill/strike", start2("strike", STRIKE_LEN + 2) + [
        "data merge entity @s {NoAI:1b}", face(), anim2("forward_strike"),
        "# 地上先画出冲锋线",
        "execute positioned ~ ~0.08 ~ run " + disp("%s/beam" % FX, scale=(1.4, 0.02, 13), color=WGL, trans=(0, 0, 6.5)),
        "execute as @e[tag=rpg.usb.fxnew] positioned as @s rotated as @e[%s,limit=1,sort=nearest] run tp @s ~ ~ ~ ~ 0" % UNIT,
    ] + born(STRIKE_GO + 4) + [
        "playsound minecraft:entity.breeze.charge hostile @a[distance=..32] ~ ~ ~ 1 0.8",
        say("让开。", name="圣光突进 · ", stage=2),
    ])
    w("sk/strike", every(2) + [
        "execute if score @s rpg_ub_t matches %d..%d at @s if block ^ ^0.5 ^%s #minecraft:replaceable if block ^ ^1.5 ^%s "
        "#minecraft:replaceable run tp @s ^ ^ ^%s" % (STRIKE_GO, STRIKE_GO + STRIKE_STEPS - 1, STRIKE_STEP, STRIKE_STEP, STRIKE_STEP),
        "execute if score @s rpg_ub_t matches %d..%d if score #m %s matches 1 at @s run function %s/strike/burst"
        % (STRIKE_GO + 1, STRIKE_GO + STRIKE_STEPS, O, B),
        "execute if score @s rpg_ub_t matches %d run tag @a remove rpg.usb.dhit" % (STRIKE_GO + STRIKE_STEPS + 1),
        "execute if score @s rpg_ub_t matches %d.. run function %s/sk/end" % (STRIKE_LEN, B),
    ])
    w("strike/burst", ["execute as @a[distance=..2.2,%s,tag=!rpg.usb.dhit] run function %s/strike/hit" % (SURV, B)]
      + glyph("burst", 2, WG_L, pos="~ ~1 ~", kind="burst") + glyph("slash", 2.4, WG_M, pos="~ ~1.3 ~", kind="slashfx")
      + decal("shock_0", 3.5, WG_M, pos="~ ~0.1 ~", kind="shock") + spark("~ ~1.8 ~", frame=4) + [
        "particle minecraft:electric_spark ~ ~1 ~ 0.6 0.6 0.6 0.4 14",
        "playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..24] ~ ~ ~ 0.6 1.6",
    ])
    w("strike/hit", ["damage @s %d minecraft:magic by @e[%s,limit=1]" % (STRIKE_DMG, UNIT), "tag @s add rpg.usb.dhit"])

    # ---- 圣雷砸地：拳套蓄力，跃起砸地，一道贴地慢慢扩张到 20 格的电环；只打脚踩地面的人（跳起来躲）
    w("skill/slam", start2("slam", SLAM_LEN) + [
        "data merge entity @s {NoAI:1b}", face(), anim2("lightning_slam"),
        "playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1 1.8",
        say("雷霆在我手里。", name="圣雷砸地 · ", stage=2),
    ])
    hits = []
    for t in range(SLAM_HIT + 1, SLAM_HIT + SLAM_TICKS + 1):
        r = SLAM_SPEED * (t - SLAM_HIT)
        hits.append("execute if score @s rpg_ub_t matches %d at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] "
                    "as @a[distance=%.2f..%.2f,%s,tag=!rpg.usb.shit] if predicate %s/on_ground run function %s/slam/hit"
                    % (t, max(0, r - 0.7), r + 0.7, SURV, B, B))
    w("sk/slam", every(4) + [
        "execute if score @s rpg_ub_t matches ..38 if score #m %s matches 0 at @s positioned %s run function %s/slam/charge"
        % (O, sock(-1.5, 25, -11), B),
        tick_at(SLAM_HIT, "slam/burst"),
        "execute if score @s rpg_ub_t matches %d run %s" % (SLAM_HIT + 1, morph("tag=rpg.usb.sring", SLAM_R * 2, SLAM_TICKS, decal_=True)),
    ] + ["execute if score @s rpg_ub_t matches %d as @e[tag=rpg.usb.ss%d] at @s rotated %d 0 run tp @s ^ ^ ^%d"
         % (SLAM_HIT + 1, k, k * 30, SLAM_R) for k in range(12)] + hits + [
        "execute if score @s rpg_ub_t matches %d.. run tag @a remove rpg.usb.shit" % SLAM_LEN,
        "execute if score @s rpg_ub_t matches %d.. run function %s/sk/end" % (SLAM_LEN, B),
    ])
    w("slam/charge", spark("~ ~ ~", frame=8) + ["particle minecraft:electric_spark ~ ~ ~ 0.2 0.2 0.2 0.3 6"])
    burst = [marker("~ ~ ~", "rpg.usb.slamc")] + born(SLAM_TICKS + 6)
    burst += decal("ring", 1, WG_L, pos="~ ~0.15 ~", life=SLAM_TICKS + 2, tags=("rpg.usb.sring",))
    burst += decal("storm", 9, WG_M, pos="~ ~0.06 ~", kind="spin", life=40)
    burst += decal("sq_0", 6, WG_L, pos="~ ~0.1 ~", kind="sq") + decal("cracks", 5, WG_D, pos="~ ~0.04 ~", life=50)
    burst += glyph("burst", 3, WG_L, pos="~ ~0.8 ~", kind="burst")
    for k in range(12):
        burst += glyph("spark", 1.1, WG_L, pos="~ ~0.5 ~", frame=k, kind="sparkl", tags=("rpg.usb.ss%d" % k,), tpd=SLAM_TICKS)
    burst += [
        "particle minecraft:flash{color:%d} ~ ~0.5 ~ 0 0 0 0 1 force" % WGL,
        "particle minecraft:electric_spark ~ ~0.3 ~ 1.5 0.1 1.5 0.8 50",
        "playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..48] ~ ~ ~ 0.8 1.4",
        "playsound minecraft:item.mace.smash_ground_heavy hostile @a[distance=..40] ~ ~ ~ 1.2 0.8",
    ]
    w("slam/burst", burst)
    w("slam/hit", ["damage @s %d minecraft:magic by @e[%s,limit=1]" % (SLAM_DMG, UNIT), "tag @s add rpg.usb.shit",
                   "execute at @s run function %s/slam/zap" % B])
    w("slam/zap", spark("~ ~0.6 ~", frame=3) + ["particle minecraft:electric_spark ~ ~0.5 ~ 0.3 0.4 0.3 0.4 12",
                                                 "playsound minecraft:entity.lightning_bolt.impact hostile @s ~ ~ ~ 0.6 1.8"])
    wj = os.path.join(DP, "data", "rpg", "predicate", "usurper_boss", "on_ground.json")
    os.makedirs(os.path.dirname(wj), exist_ok=True)
    with open(wj, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"flags": {"is_on_ground": True}}}, fh)

    # ---- 授权：召两名圣卫，各连一道白金权柄线（原作直闪电）；圣卫在场他减伤一半，全倒后 6 秒破绽，之后重新授权
    w("skill/summon", ["tag @s remove rpg.usb.auth"] + start2("summon", AUTH_LEN + 2) + [
        "data merge entity @s {NoAI:1b}", anim2("summon"),
        "playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1.2 1.2",
        say("起来，替我执行。", name="授权 · ", stage=2),
    ])
    w("sk/summon", [
        "execute if score @s rpg_ub_t matches %d at @s positioned ^3.5 ^ ^1 run function %s/auth/one1" % (AUTH_AT, B),
        "execute if score @s rpg_ub_t matches %d at @s positioned ^-3.5 ^ ^1 run function %s/auth/one2" % (AUTH_AT, B),
        "execute if score @s rpg_ub_t matches %d.. run function %s/sk/end" % (AUTH_LEN, B),
    ])
    for n in (1, 2):
        w("auth/one%d" % n, [
            "# 第 %d 名圣卫（as 载体，at 落点）" % n,
            "function rpg:holy_guard/summon",
            "tag @e[type=minecraft:vindicator,tag=rpg.hg,tag=!rpg.usb.guard,distance=..2,limit=1,sort=nearest] add rpg.usb.gnew",
            "tag @e[tag=rpg.usb.gnew] add rpg.usb.unit",
            "tag @e[tag=rpg.usb.gnew] add rpg.usb.guard",
            "scoreboard players set @e[tag=rpg.usb.gnew] rpg_ub_id %d" % n,
            "tag @e[tag=rpg.usb.gnew] remove rpg.usb.gnew",
            "tag @s add rpg.usb.guarded",
            "execute at @s positioned ~ ~1.6 ~ run " + disp("%s/bolt_beam" % FX, scale=(0.7, 0.7, 0.01), color=WGL,
                                                         tags=("rpg.usb.abeam",), tp=2),
            "scoreboard players set @e[tag=rpg.usb.fxnew,tag=rpg.usb.abeam] rpg_ub_id %d" % n,
        ] + born(24000) + decal("sq_0", 3, WG_L, pos="~ ~0.1 ~", kind="sq")
          + decal("sigil", 2.6, WG_M, pos="~ ~0.06 ~", kind="spin", life=30) + ray("~ ~ ~", WG_L) + [
            "particle minecraft:end_rod ~ ~1 ~ 0.4 1 0.4 0.05 20",
            "playsound minecraft:block.beacon.activate hostile @a[distance=..32] ~ ~ ~ 1 1.4",
        ])
    w("auth/line", [
        "# 权柄线（as/at 圣卫）：从他胸前拉到这名圣卫",
        "scoreboard players operation #id %s = @s rpg_ub_id" % O,
        "execute at @e[%s,limit=1,sort=nearest] positioned ~ ~1.6 ~ facing entity @s eyes run function %s/auth/beam" % (UNIT, B),
    ])
    w("auth/beam", [
        "scoreboard players set #d %s 0" % O,
        "function %s/infuse/step" % B,
        "execute as @e[tag=rpg.usb.abeam] if score @s rpg_ub_id = #id %s run function %s/auth/set" % (O, B),
    ])
    w("auth/set", [
        "tp @s ~ ~ ~ ~ ~",
        "data merge entity @s {start_interpolation:0,interpolation_duration:2}",
        "execute store result entity @s transformation.scale[2] float 1 run scoreboard players get #d %s" % O,
        "execute store result entity @s transformation.translation[2] float 0.5 run scoreboard players get #d %s" % O,
    ])
    w("auth/check", [
        "# 权柄线（as 线）：它的圣卫倒下了就断",
        "scoreboard players operation #id %s = @s rpg_ub_id" % O,
        "scoreboard players set #n %s 0" % O,
        "execute as @e[%s] if score @s rpg_ub_id = #id %s run scoreboard players set #n %s 1" % (GUARDS, O, O),
        "execute if score #n %s matches 0 at @s run function %s/auth/snap" % (O, B),
    ])
    w("auth/snap", glyph("burst", 1.6, WG_L, kind="burst") + [
        "playsound minecraft:block.glass.break hostile @a[distance=..24] ~ ~ ~ 1 1.4", "kill @s"])
    w("auth/fall", [
        "# 圣卫全倒（as 载体）：命令没人执行了，6 秒破绽，之后重新授权",
        "tag @s remove rpg.usb.guarded",
        "tag @s add rpg.usb.reauth",
        "scoreboard players set @s rpg_ub_x %d" % WEAK_GUARDS,
        "function %s/weak/start" % B,
        say("……没有人执行我的命令？", name="有权无力 · ", stage=2),
    ])
    w("weak/start", [
        "# 破绽开始（as 载体；rpg_ub_x 已设好时长）：王冠暗下",
        "tag @s add rpg.usb.exposed",
        crown(CROWN_DIM),
        "execute at @s positioned ~ ~2.7 ~ run function %s/weak/burst" % B,
    ])
    w("weak/burst", glyph("burst", 1.8, WG_D, kind="burst") + spark("~0.3 ~0.2 ~", WG_M, frame=10) + [
        "playsound minecraft:block.beacon.deactivate hostile @a[distance=..32] ~ ~ ~ 1 1.4"])
    w("weak/tick", ["scoreboard players remove @s rpg_ub_x 1"] + every(4, "@s rpg_ub_x") + [
        "# 王冠暗下，裂纹一闪一闪",
        "execute if score #m %s matches 0 run %s" % (O, crown(CROWN_DIM)),
        "execute if score #m %s matches 2 run %s" % (O, crown(CROWN_FLICK)),
    ] + every(8, "@s rpg_ub_x") + [
        "execute if score #m %s matches 0 at @s run function %s/weak/mote" % (O, B),
        "execute if score @s rpg_ub_x matches ..0 run function %s/weak/end" % B,
    ])
    w("weak/mote", spark("~0.3 ~2.8 ~", WG_D, 0.7, frame=13) + twinkle("~-0.3 ~2.5 ~0.2", WG_M, 1) + [
        "particle minecraft:wax_off ~ ~2.6 ~ 0.3 0.2 0.3 0 3"])
    w("weak/end", [
        "tag @s remove rpg.usb.exposed",
        crown(0xFFFFFF),
        "execute if entity @s[tag=rpg.usb.reauth] run tag @s add rpg.usb.auth",
        "tag @s remove rpg.usb.reauth",
    ])
    w("weak/ult", ["# 大招结束后 4 秒破绽", "scoreboard players set @s rpg_ub_x %d" % WEAK_ULT, "function %s/weak/start" % B])

    # ---- 大招：神力超载（浮在中心蓄力 6 秒，免疫伤害；四座白金圣坛升起，站上去躲电光）
    w("altar_clear", [
        "# 圣坛的屏障方块（任何结束路径都要先拆，再清实体）",
        "execute at @e[type=minecraft:marker,tag=rpg.usb.altar] run fill ~ ~ ~ ~1 ~1 ~1 minecraft:air replace minecraft:barrier",
        "kill @e[type=minecraft:marker,tag=rpg.usb.altar]",
    ])
    over = start2("over", OVER_LEN + 2) + [
        "# 神力超载（as/at 载体）",
        "data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:1b}",
        "execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run tp @s ~ ~3 ~",
        anim2("overcharge"),
        say("", gloss=True, name="神力超载", stage=2),
        "playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 1.4 0.6",
        "playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..48] ~ ~ ~ 0.6 1.6",
    ]
    for dx, dz in ALTARS:
        over.append("execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~%d ~ ~%d positioned over "
                    "motion_blocking_no_leaves align xyz run function %s/over/altar" % (dx, dz, B))
    over.append("execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run function %s/over/field" % B)
    w("ult/overcharge", over)
    w("over/field", decal("glow", 18, WG_D, pos="~ ~0.03 ~", life=OVER_END, tags=("rpg.usb.overv",))
      + decal("storm", 14, WG_M, pos="~ ~0.06 ~", kind="spin", life=OVER_END, tags=("rpg.usb.overv",))
      + decal("hexagon", 20, WG_L, pos="~ ~0.09 ~", kind="spinr", life=OVER_END, tags=("rpg.usb.overv",)))
    w("over/altar", [
        "# 一座圣坛（at 2×2 的方块角）：原作地卜师石柱，白金，从地下升起；16 刻后铺屏障方块，人能站上去",
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.usb.altar\"]}",
        "execute positioned ~1 ~ ~1 run " + disp("%s/pillar" % FX, scale=(26.7, 7.4, 26.7), color=0xFFFFFF, trans=(0, -2.4, 0)),
    ] + born(None, "rise") + decal("sigil", 3.2, WG_L, pos="~1 ~0.05 ~1", kind="spin", life=OVER_END)
      + ray("~1 ~2 ~1", WG_L, long=True) + [
        "particle minecraft:end_rod ~1 ~1 ~1 0.5 1 0.5 0.05 20",
        "playsound minecraft:block.stone.place hostile @a[distance=..32] ~ ~ ~ 1 0.5",
    ])
    sk_over = [
        "# 铺屏障前，站在圣坛脚下 2×2 里的人先托到坛顶，免得卡进方块",
        "execute if score @s rpg_ub_t matches 16 as @e[type=minecraft:marker,tag=rpg.usb.altar] at @s as @a[dx=1,dy=1,dz=1] "
        "run tp @s ~1 ~2.05 ~1",
        "execute if score @s rpg_ub_t matches 16 at @e[type=minecraft:marker,tag=rpg.usb.altar] run fill ~ ~ ~ ~1 ~1 ~1 "
        "minecraft:barrier replace minecraft:air",
        "execute if score @s rpg_ub_t matches 66 run " + anim2("overcharge"),
    ]
    for i, t in enumerate(OVER_WAVES):
        sk_over.append(tick_at(t - OVER_WARN, "over/warn"))
        sk_over.append(tick_at(t, "over/strike%d" % i))
        strike = [
            "# 第 %d 波电光（as/at 载体）：圣坛顶上的人安全，其余人都挨" % (i + 1),
            "execute as @e[type=minecraft:marker,tag=rpg.usb.altar] at @s positioned ~0.1 ~1.95 ~0.1 run tag @a[dx=0.8,dy=0,dz=0.8] add rpg.usb.safe",      # 体积选到 d+1：只罩住坛顶
            "execute as @a[distance=..%d,%s,tag=!rpg.usb.safe] at @s run function %s/over/zap" % (ARENA, SURV, B),
            "tag @a remove rpg.usb.safe",
            "execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run function %s/over/sweep" % B,
        ]
        for k in range(6):
            a = math.radians(60 * k + 37 * i)
            d = 7 + (k * 5 + i * 3) % 9
            strike.append("execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~%.1f ~ ~%.1f positioned over "
                          "motion_blocking_no_leaves run function %s/over/bolt" % (d * math.cos(a), d * math.sin(a), B))
        w("over/strike%d" % i, strike)
    sk_over += [tick_at(OVER_END, "over/end"),
                "execute if score @s rpg_ub_t matches %d.. run function %s/sk/end" % (OVER_LEN, B)]
    w("sk/over", sk_over)
    w("over/warn", [
        "execute as @a[distance=..%d,%s] at @s run function %s/over/warn_at" % (ARENA, SURV, B),
        "execute at @s positioned %s run function %s/slam/charge" % (sock(-1.6, 34, -3), B),
        "playsound minecraft:block.beacon.ambient hostile @a[distance=..48] ~ ~ ~ 1.4 1.8",
    ])
    w("over/warn_at", decal("storm", 3, WG_M, pos="~ ~0.08 ~", life=OVER_WARN) + spark("~ ~2.6 ~", frame=11))
    w("over/zap", ["damage @s %d minecraft:magic by @e[%s,limit=1]" % (OVER_DMG, UNIT), "function %s/over/bolt" % B])
    w("over/bolt", bolt() + decal("shock_0", 2.6, WG_L, pos="~ ~0.1 ~", kind="shock") + spark("~ ~0.5 ~", frame=6) + [
        "particle minecraft:electric_spark ~ ~0.4 ~ 0.4 0.3 0.4 0.4 12"])
    w("over/sweep", decal("shock_0", ARENA, WG_L, pos="~ ~0.14 ~", kind="shock") + [
        "particle minecraft:flash{color:%d} ~ ~3 ~ 0 0 0 0 1 force" % WGL,
        "playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..48] ~ ~ ~ 0.9 1.3",
    ])
    w("over/end", [
        "# 收势（as 载体）：圣坛撤下，他落地，4 秒破绽",
        "function %s/altar_clear" % B,
        "kill @e[tag=rpg.usb.overv]",
        "execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run tp @s ~ ~ ~",
        "data merge entity @s {Invulnerable:0b,NoGravity:0b}",
        "function %s/weak/ult" % B,
        "execute at @s run function %s/over/land" % B,
    ])
    w("over/land", decal("sq_0", 6, WG_L, pos="~ ~0.1 ~", kind="sq") + glyph("burst", 2.4, WG_M, pos="~ ~1 ~", kind="burst") + [
        "playsound minecraft:item.mace.smash_ground hostile @a[distance=..32] ~ ~ ~ 1 0.8"])

    # ---- 大招：伪圣审判（模仿新约的创世净光：从身前向外依次扫出 5 道白金光束，先细线后变粗）
    w("ult/judgment", start2("judge", JUDGE_T0 + JUDGE_GAP * 4 + 22) + [
        "# 伪圣审判（as/at 载体）",
        "data merge entity @s {NoAI:1b}", face(), anim2("summon"),
        "execute at @s run " + marker("~ ~ ~", "rpg.usb.jdir"),
        "execute as @e[tag=rpg.usb.fxnew] at @s rotated as @e[%s,limit=1,sort=nearest] run tp @s ~ ~ ~ ~ 0" % UNIT,
    ] + born(JUDGE_T0 + JUDGE_GAP * 4 + 30)
      + decal("glow", 7, WG_D, pos="~ ~0.03 ~", life=JUDGE_T0 + JUDGE_GAP * 4 + 16)
      + decal("swirl", 5, WG_L, pos="~ ~0.06 ~", kind="spin", life=JUDGE_T0 + JUDGE_GAP * 4 + 16) + [
        say("", gloss=True, name="伪圣审判", stage=2),
        "playsound minecraft:block.beacon.activate hostile @a[distance=..48] ~ ~ ~ 1.4 0.7",
    ])
    sk_j = [tick_at(JUDGE_T0 - 10, "judge/pose")]
    for k, off in enumerate(JUDGE_OFF):
        t = JUDGE_T0 + JUDGE_GAP * k
        sel = "execute as @e[type=minecraft:marker,tag=rpg.usb.jdir,limit=1] at @s rotated ~%d 0" % off
        sk_j += [tick_at(t - JUDGE_TELE, "judge/tele%d" % k), tick_at(t, "judge/fire%d" % k),
                 "execute if score @s rpg_ub_t matches %d run %s" % (t + 8, morph("tag=rpg.usb.jb%d" % k, (0.01, 0.01, JUDGE_LEN), 4))]
        w("judge/tele%d" % k, ["%s positioned ~ ~1.5 ~ run function %s/judge/beam%d" % (sel, B, k)])
        w("judge/beam%d" % k, [
            "# 第 %d 道光束：先是一条细线（as 方向标记，at 起点，朝光束方向）" % (k + 1),
            disp("%s/beam" % FX, scale=(0.06, 0.06, JUDGE_LEN), color=WGL, trans=(0, 0, JUDGE_LEN / 2.0),
                 tags=("rpg.usb.jb%d" % k,)),
            "execute as @e[tag=rpg.usb.fxnew] run tp @s ~ ~ ~ ~ ~",
        ] + born(JUDGE_TELE + 14) + twinkle("^ ^ ^%d" % JUDGE_LEN, WG_L, k % 3) + [
            "playsound minecraft:block.beacon.ambient hostile @a[distance=..40] ~ ~ ~ 1 2",
        ])
        fire = ["# 第 %d 道光束变粗：线上 1.6 格内 16" % (k + 1),
                morph("tag=rpg.usb.jb%d" % k, (1.4, 1.4, JUDGE_LEN), 2)]
        d = 1.5
        while d <= JUDGE_LEN:
            fire.append("%s positioned ^ ^ ^%s run tag @a[distance=..1.6,%s] add rpg.usb.hit" % (sel, d, SURV))
            d += 1.5
        fire += [
            "execute as @a[tag=rpg.usb.hit,distance=..%d] run damage @s %d minecraft:magic by @e[%s,limit=1]" % (ARENA, JUDGE_DMG, UNIT),
            "tag @a[tag=rpg.usb.hit] remove rpg.usb.hit",
        ] + ["%s positioned ^ ^1.5 ^%d run function %s/judge/spark" % (sel, dd, B) for dd in (6, 12, 18)] + [
            "%s positioned ^ ^1.5 ^1 run function %s/judge/flash" % (sel, B),
            "playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..40] ~ ~ ~ 1 1.2",
            "playsound minecraft:block.beacon.deactivate hostile @a[distance=..40] ~ ~ ~ 0.8 1.8",
        ]
        w("judge/fire%d" % k, fire)
    w("judge/pose", [anim2("forward_strike")])
    w("judge/spark", spark("~ ~ ~", frame=7) + ["particle minecraft:end_rod ~ ~ ~ 0.3 0.3 0.3 0.05 4"])
    w("judge/flash", glyph("pop", 1.6, WG_L, kind="pop"))
    j_end = JUDGE_T0 + JUDGE_GAP * 4 + 16
    sk_j += [tick_at(j_end, "weak/ult"), "execute if score @s rpg_ub_t matches %d.. run function %s/sk/end" % (j_end + 4, B)]
    w("sk/judge", sk_j)

    # ---- 变身：篡夺圣灵（约 6 秒）。天降白金光柱；签了新约的玩家身上牵出白金光线；书碎；光柱吞没；换成首席附魔师
    w("morph/pillar", [
        "execute positioned ~ ~ ~ run " + disp("%s/beam" % FX, scale=(0.01, 0.01, 40), color=WGL, trans=(0, 0, 20), tags=("rpg.usb.mpil",)),
        "execute as @e[tag=rpg.usb.fxnew] run tp @s ~ ~ ~ ~ -90",
    ] + born(None, "pillar") + decal("glow", 10, WG_D, pos="~ ~0.03 ~", life=120)
      + decal("ring", 8, WG_L, pos="~ ~0.06 ~", life=120) + decal("storm", 7, WG_M, pos="~ ~0.09 ~", kind="spin", life=120) + [
        "playsound minecraft:block.beacon.power_select hostile @a[distance=..%d] ~ ~ ~ 1.4 0.6" % BAR_RANGE,
        "playsound minecraft:block.beacon.activate hostile @a[distance=..%d] ~ ~ ~ 1.2 0.8" % BAR_RANGE,
    ])
    w("morph/lines", ["execute as @a[distance=..%d,%s,scores={rpg_lt_divine=2}] at @s positioned ~ ~1.2 ~ facing entity "
                      "@e[%s,limit=1,sort=nearest] eyes run function %s/morph/line" % (BAR_RANGE, SURV, UNIT, B)])
    w("morph/line", [
        "# 一道白金光线（as 签了新约的玩家，at 其胸前，朝向他）：只是演出，不扣权柄",
        "scoreboard players set #d %s 0" % O,
        "function %s/morph/step" % B,
        disp("%s/bolt_beam" % FX, scale=(0.6, 0.6, 0.01), color=WGL, tags=("rpg.usb.mline",)),
        "execute as @e[tag=rpg.usb.fxnew,tag=rpg.usb.mline] run tp @s ~ ~ ~ ~ ~",
        "execute as @e[tag=rpg.usb.fxnew,tag=rpg.usb.mline] store result entity @s transformation.scale[2] float 1 run scoreboard players get #d %s" % O,
        "execute as @e[tag=rpg.usb.fxnew,tag=rpg.usb.mline] store result entity @s transformation.translation[2] float 0.5 run scoreboard players get #d %s" % O,
    ] + born(11) + twinkle("~ ~0.6 ~", WG_L, 2))
    w("morph/step", [
        "scoreboard players add #d %s 1" % O,
        "execute if entity @e[%s,distance=..1.4] run return 0" % UNIT,
        "execute positioned ~ ~-1.6 ~ if entity @e[%s,distance=..1.4] run return 0" % UNIT,
        "execute if score #d %s matches ..%d positioned ^ ^ ^1 run function %s/morph/step" % (O, BAR_RANGE, B),
    ])
    pages = ["# 附魔书碎裂：书页四散（附魔师模型自己的书页）"]
    pages += glyph("burst", 3, LAVENDER, pos="~ ~2.6 ~", kind="burst") + glyph("pop", 2, WG_L, pos="~ ~2.6 ~", kind="pop")
    for k in range(8):
        pages += [disp("rpg:usurper/paper1", pos="~ ~2.5 ~", scale=6, color=0xF4E9FF, tags=("rpg.usb.page%d" % k,), tp=20,
                       lrot="[0f,0.70710677f,0f,0.70710677f]")] + born(34)
    pages += ["playsound minecraft:block.glass.break hostile @a[distance=..%d] ~ ~ ~ 1.2 0.7" % BAR_RANGE,
              "playsound rpg:usurper.close hostile @a[distance=..%d] ~ ~ ~ 1.4 0.6" % BAR_RANGE]
    w("morph/shatter", pages)
    w("morph/pages_fly", ["execute as @e[tag=rpg.usb.page%d] at @s rotated %d -25 run tp @s ^ ^ ^5 ~ ~" % (k, k * 45)
                          for k in range(8)])
    w("morph/engulf", glyph("burst", 6, WG_L, pos="~ ~1.5 ~", kind="burst") + decal("shock_0", 14, WG_L, pos="~ ~0.12 ~", kind="shock")
      + ray("~ ~ ~", WG_L, long=True) + [
        "particle minecraft:flash{color:%d} ~ ~1.5 ~ 0 0 0 0 1 force" % WGL,
        "particle minecraft:end_rod ~ ~1.5 ~ 0.6 1.5 0.6 0.2 80 force",
        "playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..%d] ~ ~ ~ 1 0.8" % BAR_RANGE,
        "playsound minecraft:item.totem.use hostile @a[distance=..%d] ~ ~ ~ 1 0.6" % BAR_RANGE,
    ])
    w("morph/crown", glyph("pop", 1.6, WG_L, pos="~ ~2.9 ~", kind="pop") + twinkle("~0.4 ~3 ~", WG_L, 0)
      + twinkle("~-0.4 ~3.1 ~0.2", WG_L, 1) + twinkle("~0.1 ~3.3 ~-0.3", WG_M, 2) + [
        "playsound rpg:usurper.chime hostile @a[distance=..%d] ~ ~ ~ 1.2 1.4" % BAR_RANGE])
    w("morph/totem_pop", glyph("burst", 1.6, "#F3D34A", pos="~ ~0.6 ~", kind="burst") + [
        "particle minecraft:totem_of_undying ~ ~0.6 ~ 0.3 0.4 0.3 0.6 60",
        "playsound minecraft:block.glass.break hostile @a[distance=..%d] ~ ~ ~ 1 1.2" % BAR_RANGE,
        "kill @s"])
    w("look2/swap", [
        "# 换成首席附魔师（as/at 载体）：收掉附魔师的部件，把首席附魔师的部件挪到这个载体上",
        "execute on passengers if entity @s[tag=rpg.usm.part] run kill @s",
        "tag @s remove rpg.usm",
        "tag @s add rpg.usb.s2",
        "tag @s add rpg.prime_enchanter",
        "function %s/summon" % PE,
        "execute as @e[type=minecraft:vindicator,tag=rpg.prime_enchanter,tag=!rpg.usb,distance=..1,limit=1] run function %s/look2/take" % B,
        anim2("appear"),
    ])
    w("look2/take", ["execute on passengers run function %s/look2/move" % B, "tp @s ~ -256 ~", "kill @s"])
    w("look2/move", ["ride @s dismount", "ride @s mount @e[%s,tag=rpg.usb.s2,limit=1,sort=nearest]" % UNIT])

    # ---- 击败结算：倒地，王冠碎裂，权柄归还
    shards = ["# 王冠碎裂（as/at 载体）：头部换成不带王冠的那份，碎片四散",
              HEAD + "data modify entity @s item.components.\"minecraft:item_model\" set value \"rpg:usurper_fx/pe_head_bare\""]
    shards += glyph("burst", 2.5, WG_L, pos="~ ~2.5 ~", kind="burst") + glyph("pop", 1.4, WG_M, pos="~ ~2.5 ~", kind="pop")
    for k in range(6):
        shards += [disp("%s/crown" % FX, pos="~ ~2.5 ~", scale=3, color=0xFFFFFF, tags=("rpg.usb.shard%d" % k,), tp=20)] + born(30)
    shards += ["particle minecraft:end_rod ~ ~2.5 ~ 0.3 0.3 0.3 0.15 30",
               "playsound minecraft:block.glass.break hostile @a[distance=..%d] ~ ~ ~ 1.4 0.6" % BAR_RANGE,
               "playsound minecraft:block.beacon.deactivate hostile @a[distance=..%d] ~ ~ ~ 1.2 0.8" % BAR_RANGE]
    w("finale/crown", shards)
    w("finale/shards_fly", ["execute as @e[tag=rpg.usb.shard%d] at @s rotated %d -30 run tp @s ^ ^ ^3.5 ~120 ~" % (k, k * 60)
                            for k in range(6)])
    back = ui.row(ui.comp("[权柄] ", ui.CYAN, True), ui.comp("被篡夺的权柄归还；你的权柄完整度已补满。", ui.CYAN_LIGHT))
    w("finale/return", [
        "# 权柄归还：签了新约的玩家，白金光线连回去，权柄补满",
        "execute as @a[distance=..%d,%s,scores={rpg_lt_divine=2}] at @s positioned ~ ~1.2 ~ facing entity "
        "@e[%s,limit=1,sort=nearest] eyes run function %s/morph/line" % (BAR_RANGE, SURV, UNIT, B),
        "scoreboard players set @a[distance=..%d,scores={rpg_lt_divine=2}] rpg_lt_auth 100" % BAR_RANGE,
        "tellraw @a[distance=..%d,scores={rpg_lt_divine=2}] %s" % (BAR_RANGE, back),
        "execute as @a[distance=..%d,%s] at @s run function %s/finale/glint" % (BAR_RANGE, SURV, B),
    ])
    w("finale/glint", twinkle("~0.3 ~2 ~", WG_L, 0) + twinkle("~-0.3 ~1.6 ~0.2", WG_L, 2))

    # ---- 新约技能打到他（设计稿第 9 节第 3 条）：固定伤害，没有斩杀线；二阶段多 25%
    for kind, base in (("new", 120), ("old", 100), ("field", 80), ("judgment", 100)):
        w("divine/%s" % kind, [
            "# 新约技能打到篡夺者：固定 %d，二阶段 %d（玩家承受的是力，克制他偷来的权）；不走百分比和斩杀线" % (base, base * 5 // 4),
            "tag @s add rpg.divine.hit",
            "# 神圣之光无视无敌：他无敌的时候（变身、超载、天降半空、倒地）不吃",
            "execute if data entity @s {Invulnerable:1b} run return 0",
            "scoreboard players set @s rpg_lt_max %d" % (base * 100),
            "execute if score #stage %s matches 2 run scoreboard players set @s rpg_lt_max %d" % (O, base * 125),
            "function rpg:divine/damage/apply_score",
            "particle minecraft:enchanted_hit ~ ~1.5 ~ 0.5 1 0.5 0.1 16 normal",
        ])


DIVINE_MARK = "# 篡夺者（add_usurper_boss.py）"


def hook_divine():
    """The covenant skills select rpg.demon / .minion / .fly; the Usurper carries rpg.demon.fly (nothing else
    selects it), and the four damage entry points send him to fixed damage first."""
    for rel, kind in (("divine/damage/new_target", "new"), ("divine/damage/old_target", "old"),
                      ("divine/damage/field_target", "field"), ("divine/judgment/strike", "judgment")):
        path = os.path.join(FUNC, *rel.split("/")) + ".mcfunction"
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
        if DIVINE_MARK in lines:
            continue
        i = 0
        while i < len(lines) and lines[i].startswith("#"):
            i += 1
        lines[i:i] = [DIVINE_MARK, "execute if entity @s[tag=rpg.usb] run return run function %s/divine/%s" % (B, kind)]
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines))


def wire_stage2():
    stage2()
    unit = os.path.join(OUT, "unit.mcfunction")
    with open(unit, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    i = lines.index("execute if score @s rpg_ub_busy matches 1.. run return run scoreboard players remove @s rpg_ub_busy 1")
    lines[i:i] = ["execute if score @s %s matches 2 run function %s/s2/tick" % (O, B)]
    wf(unit, lines)
    hook_divine()


def wire_stage1():
    """Stage 1 replaces the framework placeholders; its per-tick hooks join unit / arena."""
    stage1()
    unit = os.path.join(OUT, "unit.mcfunction")
    with open(unit, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    i = lines.index("execute if score @s rpg_ub_busy matches 1.. run return run scoreboard players remove @s rpg_ub_busy 1")
    lines[i:i] = [
        "execute if score @s rpg_ub_sk matches 1.. run function %s/sk/tick" % B,
        "execute if score @s %s matches 1 if score @s rpg_ub_busy matches ..0 run function %s/wave/check" % (O, B),
    ]
    wf(unit, lines)
    arena = os.path.join(OUT, "arena.mcfunction")
    with open(arena, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    lines += [
        "execute as @e[tag=rpg.usb.fx,distance=..%d] at @s run function %s/fx/tick" % (ARENA * 3, B),
        "execute as @a[tag=rpg.usb.rw] run function %s/rewrite/tick" % B,
    ]
    wf(arena, lines)


def main():
    build()
    wire_stage1()
    wire_stage2()
    hook_tag(DP, "load", "%s/load" % B, False)
    hook_tag(DP, "tick", "%s/tick" % B, True)
    count = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("usurper_boss: %d functions; two stages of %d HP, both stages live" % (count, MAX))


if __name__ == "__main__":
    main()
