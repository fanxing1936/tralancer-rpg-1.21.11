# -*- coding: utf-8 -*-
"""七柱真名调查与四阶段驱魔仪式。

这个生成器故意在 ``opt_runtime_hotpaths.py`` 之后运行：它接入的是最终版
``advent_tick``、``rite/beat`` 与恶魔招式入口，避免后续热路径重写把仪式守卫
覆盖掉。所有调查进度属于玩家；所有仪式状态属于恶魔与其唯一绑定的图腾，
因此多人同时调查、同时开阵不会互相借进度。
"""

import io
import json
import os
import sys


DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")

MAX_HP = 700
SUPPRESS_HP = 420
FAIL_HP = 560
CHANNEL_TICKS = 100
BANISH_TICKS = 40
ANCHOR_TICKS = 800

LORDS = [
    dict(n=1, who="路西法", colour="#00491C", item="minecraft:feather",
         medium="羽毛 · 谦卑之羽", weakness="傲慢无法承受自愿的低伏",
          clues=["蛇矛总从高处落下，力量依赖俯视。",
                 "高踞并非威严，而是不能低头的枷锁。",
                 "以一枚轻羽代替王冠，能使傲慢接受宣判。",
                 "失坠会折断他人的高度，却暴露王冠对低处的恐惧。",
                 "王座只会排斥靠近者，因为傲慢无法容纳平视。"]),
    dict(n=2, who="利维坦", colour="#1B4F72", item="minecraft:prismarine_crystals",
         medium="海晶砂 · 无主之潮", weakness="嫉妒惧怕不属于任何人的馈赠",
          clues=["沉锚牵动的不是海水，而是占有欲。",
                 "溺没会夺走呼吸，嫉羡会夺走恩赐。",
                 "无主的海晶能让深潮失去可嫉妒的对象。",
                 "逆潮不断重写远近，因为嫉妒从不接受平等的位置。",
                 "海渊重压源于比较，而非真正的深度。"]),
    dict(n=3, who="亚巴顿", colour="#6A6A70", item="minecraft:clock",
         medium="时钟 · 不眠之钟", weakness="怠惰畏惧持续前行的时间",
          clues=["收割只偏爱已经停滞的灵魂。",
                 "沉眠与深渊之口都在迫使万物静止。",
                 "仍在走动的时钟可以钉住无底坑的门。",
                 "停摆是怠惰最纯粹的愿望：让时间替它放弃。",
                 "死寂吞没行动之前，总会先吞掉声音。"]),
    dict(n=4, who="别西卜", colour="#5A6B1E", item="minecraft:poisonous_potato",
         medium="毒马铃薯 · 腐宴残食", weakness="暴食无法吞下已经腐败的宴席",
          clues=["余烬不是火，而是吃剩后扬起的灰。",
                 "吞噬与蝇群都从永不满足的胃中孵化。",
                 "把腐败食物献回宴席，万蝇之王会拒绝进食。",
                 "腐宴把宾客也算作菜肴，却惧怕已经坏死的食物。",
                 "饥啮只追逐最近的血肉，证明饥饿从未拥有选择。"]),
    dict(n=5, who="萨麦尔", colour="#7B241C", item="minecraft:snowball",
         medium="雪球 · 熄怒之雪", weakness="暴怒会被不还手的寒意冷却",
          clues=["毒雾先灼热血液，怒斩随后追逐沸腾。",
                 "死亡低语会回应继续攻击的人。",
                 "一团没有杀意的雪，足以让怒火失去回声。",
                 "血猎循伤而至，怒火只能追逐已经流出的血。",
                 "怒潮把众人推远，暴露了暴怒无法承受接近。"]),
    dict(n=6, who="贝利尔", colour="#5B2C6F", item="minecraft:amethyst_shard",
         medium="紫水晶碎片 · 清醒之镜", weakness="色欲惧怕不被幻象改写的映照",
          clues=["朝拜强迫身体低头，却不能证明心已屈服。",
                 "迷乱与献身都依靠被篡改的感官。",
                 "清醒的紫晶会把诱惑照回施术者自己。",
                 "顾盼只能强迫目光，无法让真实意志转向。",
                 "欲障遮住真形，因此最惧怕清醒的映照。"]),
    dict(n=7, who="玛门", colour="#B7950B", item="minecraft:gold_ingot",
         medium="金锭 · 自愿之金", weakness="贪婪无法夺走主动舍弃之物",
          clues=["点金给每条命标价，夺财则拒绝无主之物。",
                 "重金一击的力量来自被迫支付的代价。",
                 "自愿投入的一锭金，不属于玛门的账本。",
                 "复利需要债主承认债务，自愿舍弃便无利可生。",
                 "金牢困住的是占有者，而非被主动放下的黄金。"]),
]

OBJECTIVES = (["rpg_ex_stage", "rpg_ex_time", "rpg_ex_hp",
               "rpg_ex_tmp", "rpg_rite_id"] +
              ["rpg_case%d" % q["n"] for q in LORDS])


def wf(rel, text):
    path = os.path.join(FUNC, rel)
    parent = os.path.dirname(path)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.rstrip("\n") + "\n")


def read(rel):
    with io.open(os.path.join(FUNC, rel), encoding="utf-8") as f:
        return f.read()


def write(rel, text):
    with io.open(os.path.join(FUNC, rel), "w", encoding="utf-8", newline="\n") as f:
        f.write(text.rstrip("\n") + "\n")


def raw(parts):
    return json.dumps([""] + parts, ensure_ascii=False,
                      separators=(",", ":"))


def text(value, colour="white", bold=False, italic=False):
    out = {"text": value, "color": colour}
    if bold:
        out["bold"] = True
    if italic:
        out["italic"] = True
    return out


def patch_once(rel, needle, insert, before=False):
    src = read(rel)
    if insert.strip() in src:
        return
    if needle not in src:
        raise RuntimeError("patch anchor missing in %s: %s" % (rel, needle))
    replacement = insert + needle if before else needle + insert
    write(rel, src.replace(needle, replacement, 1))


def add_objectives():
    rel = "command/soreboard.mcfunction"
    src = read(rel).rstrip("\n")
    added = []
    for objective in OBJECTIVES:
        if ("scoreboard objectives add %s " % objective) not in src:
            src += "\nscoreboard objectives add %s dummy" % objective
            added.append(objective)
    write(rel, src)
    return added


def build_clues():
    for q in LORDS:
        n = q["n"]
        for i, clue in enumerate(q["clues"], 1):
            progress = raw([
                text("[罪证] ", "#DAA520", True),
                text(q["who"] + " · ", q["colour"], True),
                text(clue, "gray"),
                text("　进度 ", "dark_gray"),
                {"score": {"name": "@s", "objective": "rpg_case%d" % n},
                 "color": "white"},
                text("/3", "dark_gray")])
            body = """\
execute if entity @s[tag=rpg.name.%(n)d] run return 0
execute if entity @s[tag=rpg.clue.%(n)d.%(i)d] run return 0
tag @s add rpg.clue.%(n)d.%(i)d
function rpg:inquest/recount/%(n)d
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s %(progress)s
execute if score @s rpg_case%(n)d matches 3.. run function rpg:inquest/reveal/%(n)d
""" % dict(n=n, i=i, progress=progress)
            wf("inquest/clue/%d_%d.mcfunction" % (n, i), body)

        recount = [
            "# 罪证标签才是事实来源；分数只是显示缓存，不能继承旧测试残值。",
            "scoreboard players set @s rpg_case%d 0" % n]
        for i in range(1, 6):
            recount.append(
                "execute if entity @s[tag=rpg.clue.%d.%d] run scoreboard players add @s rpg_case%d 1"
                % (n, i, n))
        wf("inquest/recount/%d.mcfunction" % n, "\n".join(recount))

        reveal = raw([
            text("[真名确证] ", "#FFF2A8", True),
            text(q["who"], q["colour"], True),
            text("　弱点媒介：", "gray"),
            text(q["medium"], "white", True),
            text("。", "gray")])
        subtitle = raw([text("弱点 · " + q["weakness"], q["colour"], True)])
        wf("inquest/reveal/%d.mcfunction" % n, """\
tag @s add rpg.name.%(n)d
scoreboard players set @s rpg_case%(n)d 3
title @s times 10 70 20
title @s title %(title)s
title @s subtitle %(subtitle)s
tellraw @s %(reveal)s
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.35
""" % dict(n=n,
             title=raw([text("真　名　确　证", "#FFF2A8", True)]),
             subtitle=subtitle, reveal=reveal))

        wf("inquest/reminder/%d.mcfunction" % n,
           "tellraw @s " + raw([
               text("[调查档案] ", "#DAA520", True),
               text(q["who"], q["colour"], True),
               text("的真名已确证；向燃烧图腾投入", "gray"),
               text(q["medium"], "white", True),
               text("。", "gray")]))

    reset = [
        "# 仅供玩家主动重新测试调查；绝不在加载或战斗中自动调用。"]
    for q in LORDS:
        n = q["n"]
        reset.append("tag @s remove rpg.name.%d" % n)
        for i in range(1, 6):
            reset.append("tag @s remove rpg.clue.%d.%d" % (n, i))
        reset.append("scoreboard players set @s rpg_case%d 0" % n)
    reset += [
        "tellraw @s " + raw([
            text("[调查档案] ", "#DAA520", True),
            text("已清空你的七柱真名与罪证；下一次见证将从 1 / 3 开始。", "gray")]),
        "playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.0"]
    wf("inquest/reset_self.mcfunction", "\n".join(reset))


def build_boss_functions():
    wf("inquest/boss_tick.mcfunction", """\
# 只收七柱降临者；无名者仍沿用原来的直接战斗处置。
execute unless score @s rpg_dm_lord matches 1..7 run return 0
execute unless entity @s[tag=rpg.health700] run function rpg:inquest/init_health
execute unless entity @s[tag=rpg.inquest.intro] run function rpg:inquest/intro
scoreboard players add @s rpg_ex_stage 0
execute store result score @s rpg_ex_hp run data get entity @s Health 1
execute if entity @s[scores={rpg_ex_stage=0,rpg_ex_hp=..420}] run function rpg:inquest/suppress
execute if entity @s[scores={rpg_ex_stage=1}] run function rpg:inquest/stage1
execute if entity @s[scores={rpg_ex_stage=2..4}] run function rpg:inquest/bound_tick
""")

    wf("inquest/init_health.mcfunction", """\
attribute @s minecraft:max_health base set 700
data merge entity @s {Health:700f}
tag @s add rpg.health700
""")

    intro_lines = [
        "tag @s add rpg.inquest.intro",
        "tellraw @a[distance=..24,gamemode=!spectator] " + raw([
            text("[驱魔调查] ", "#DAA520", True),
            text("携带圣器见证五种招式中的任意三种；重复招式不会生成新罪证。", "gray")])]
    for q in LORDS:
        intro_lines.append(
            "execute if score @s rpg_dm_lord matches %(n)d as "
            "@a[tag=rpg.name.%(n)d,distance=..24,gamemode=!spectator] run "
            "function rpg:inquest/reminder/%(n)d" % q)
    wf("inquest/intro.mcfunction", "\n".join(intro_lines))

    wf("inquest/suppress.mcfunction", """\
scoreboard players set @s rpg_ex_stage 1
data merge entity @s {Health:420f}
effect give @s minecraft:resistance 2 4 true
title @a[distance=..18,gamemode=!spectator] times 10 50 15
title @a[distance=..18,gamemode=!spectator] title %(title)s
title @a[distance=..18,gamemode=!spectator] subtitle %(subtitle)s
tellraw @a[distance=..18,gamemode=!spectator] %(message)s
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..28] ~ ~ ~ 1 0.55
""" % dict(
        title=raw([text("Ⅰ · 镇　压", "#DAA520", True)]),
        subtitle=raw([text("肉身已伏 · 真名与法阵缺一不可", "gray")]),
        message=raw([text("[镇压] ", "#DAA520", True),
                     text("恶魔被锁在 420 / 700 生命；完成调查并点燃驱魔图腾。", "gray")])) )

    stage1 = [
        "data merge entity @s {Health:420f}",
        "effect give @s minecraft:resistance 2 4 true",
        "particle dust{color:[0.95,0.82,0.32],scale:0.8} ~ ~1 ~ 0.35 0.7 0.35 0.01 1 normal"]
    for q in LORDS:
        stage1.append(
            "execute if score @s rpg_dm_lord matches %(n)d "
            "if entity @a[tag=rpg.name.%(n)d,distance=..10,gamemode=!spectator] "
            "if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,"
            "tag=!rpg.totem.inv,tag=!rpg.rite.anchor,distance=..8,limit=1] "
            "run return run function rpg:inquest/bind/%(n)d" % q)
    wf("inquest/stage1.mcfunction", "\n".join(stage1))

    wf("inquest/bound_tick.mcfunction", """\
data merge entity @s {Health:420f,CustomNameVisible:1b}
effect give @s minecraft:resistance 2 4 true
effect give @s minecraft:slowness 2 255 true
effect give @s minecraft:glowing 2 0 true
effect clear @s minecraft:invisibility
particle enchant ~ ~1 ~ 0.55 0.9 0.55 0.04 2 normal
scoreboard players set #anchor_found rpg_ex_tmp 0
tag @s add rpg.rite.subject
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.rite.subject,limit=1] rpg_rite_id run scoreboard players set #anchor_found rpg_ex_tmp 1
tag @s remove rpg.rite.subject
execute if score #anchor_found rpg_ex_tmp matches 0 run function rpg:inquest/fail
""")

    wf("inquest/fail.mcfunction", """\
scoreboard players set @s rpg_ex_stage 0
scoreboard players set @s rpg_ex_time 0
data merge entity @s {Health:560f,CustomNameVisible:0b}
tag @s remove rpg.exorcism.bound
tag @s remove rpg.exorcism.visible
effect clear @s minecraft:resistance
effect clear @s minecraft:slowness
effect clear @s minecraft:glowing
tellraw @a[distance=..18,gamemode=!spectator] %(message)s
playsound minecraft:block.beacon.deactivate hostile @a[distance=..24] ~ ~ ~ 1 0.65
""" % {"message": raw([text("[仪式中断] ", "dark_red", True),
                             text("法阵失去约束，恶魔恢复至 560 生命。", "gray")])})

    for q in LORDS:
        n = q["n"]
        wf("inquest/bind/%d.mcfunction" % n, """\
scoreboard players add #rite_next rpg_rite_id 1
scoreboard players operation @s rpg_rite_id = #rite_next rpg_rite_id
scoreboard players set @s rpg_ex_stage 2
tag @s add rpg.exorcism.bound
tag @s add rpg.exorcism.visible
tag @s add rpg.rite.subject
execute as @e[type=minecraft:item_display,tag=rpg.totem.lit,tag=!rpg.totem.inv,tag=!rpg.rite.anchor,distance=..8,limit=1,sort=nearest] at @s run function rpg:inquest/anchor_bind/%(n)d
tag @s remove rpg.rite.subject
title @a[distance=..18,gamemode=!spectator] times 10 60 15
title @a[distance=..18,gamemode=!spectator] title %(title)s
title @a[distance=..18,gamemode=!spectator] subtitle %(subtitle)s
tellraw @a[distance=..18,gamemode=!spectator] %(message)s
playsound minecraft:block.beacon.power_select player @a[distance=..24] ~ ~ ~ 1 1.25
""" % dict(
            n=n,
            title=raw([text("Ⅱ · 显　形", q["colour"], True)]),
            subtitle=raw([text(q["who"] + " · 真名已被法阵承认", "white")]),
            message=raw([text("[显形] ", q["colour"], True),
                         text("向图腾投入弱点媒介：", "gray"),
                         text(q["medium"], "white", True)])))

        wf("inquest/anchor_bind/%d.mcfunction" % n, """\
tag @s add rpg.rite.anchor
scoreboard players operation @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.rite.subject,limit=1] rpg_rite_id
scoreboard players set @s rpg_dm_lord %(n)d
scoreboard players set @s rpg_ex_stage 2
scoreboard players set @s rpg_ex_time 0
scoreboard players set @s rpg_totem %(life)d
particle flash{color:16777200} ~ ~0.8 ~ 0 0 0 0 1 force
particle end_rod ~ ~0.7 ~ 0.7 0.5 0.7 0.06 45 normal
""" % {"n": n, "life": ANCHOR_TICKS})

        wf("inquest/boss_stage3/%d.mcfunction" % n, """\
scoreboard players set @s rpg_ex_stage 3
scoreboard players set @s rpg_ex_time %(ticks)d
data merge entity @s {Health:420f,CustomNameVisible:1b}
""" % {"ticks": CHANNEL_TICKS})

        wf("inquest/offer/%d.mcfunction" % n, """\
function rpg:inquest/consume_offer
scoreboard players set @s rpg_ex_stage 3
scoreboard players set @s rpg_ex_time %(ticks)d
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/boss_stage3/%(n)d
tag @s remove rpg.rite.anchor.active
title @a[distance=..12,gamemode=!spectator] times 10 60 15
title @a[distance=..12,gamemode=!spectator] title %(title)s
title @a[distance=..12,gamemode=!spectator] subtitle %(subtitle)s
tellraw @a[distance=..16,gamemode=!spectator] %(message)s
playsound minecraft:block.enchantment_table.use player @a[distance=..20] ~ ~ ~ 1 0.7
""" % dict(
            ticks=CHANNEL_TICKS, n=n,
            title=raw([text("Ⅲ · 宣　判", "#FFF2A8", True)]),
            subtitle=raw([text("真名：" + q["who"], q["colour"], True)]),
            message=raw([text("[宣判] ", "#FFF2A8", True),
                         text(q["who"] + "，" + q["weakness"] + "。", q["colour"]),
                         text(" 知晓真名者须守阵五秒；燃烧图腾本身提供圣性。", "gray")])))

        wf("inquest/scan/%d.mcfunction" % n, """\
execute as @e[type=minecraft:item,distance=..4] if items entity @s contents %(item)s run tag @s add rpg.rite.offer
execute if entity @e[type=minecraft:item,tag=rpg.rite.offer,distance=..4,limit=1] run return run function rpg:inquest/offer/%(n)d
tag @s remove rpg.rite.anchor.active
""" % {"item": q["item"], "n": n})

    wf("inquest/consume_offer.mcfunction", """\
execute store result score #offer_count rpg_ex_tmp run data get entity @e[type=minecraft:item,tag=rpg.rite.offer,limit=1] Item.count 1
scoreboard players remove #offer_count rpg_ex_tmp 1
execute if score #offer_count rpg_ex_tmp matches 1.. store result entity @e[type=minecraft:item,tag=rpg.rite.offer,limit=1] Item.count int 1 run scoreboard players get #offer_count rpg_ex_tmp
execute if score #offer_count rpg_ex_tmp matches ..0 run kill @e[type=minecraft:item,tag=rpg.rite.offer,limit=1]
tag @e[type=minecraft:item,tag=rpg.rite.offer] remove rpg.rite.offer
""")

    wf("inquest/boss_stage4.mcfunction", """\
scoreboard players set @s rpg_ex_stage 4
scoreboard players set @s rpg_ex_time 40
data merge entity @s {Health:420f,CustomNameVisible:1b}
""")

    wf("inquest/boss_success.mcfunction", """\
execute on passengers run kill @s
particle sculk_soul ~ ~1 ~ 1.2 1.4 1.2 0.16 90 force
particle end_rod ~ ~1 ~ 1.4 1.2 1.4 0.12 120 force
particle flash{color:16777200} ~ ~1 ~ 0 0 0 0 1 force
playsound minecraft:entity.wither.death hostile @a[distance=..40] ~ ~ ~ 1 1.45
experience add @a[distance=..10,gamemode=!spectator] 80 points
scoreboard players remove @a[distance=..10,gamemode=!spectator] rpg_taint 10
scoreboard players set @a[distance=..10,gamemode=!spectator,scores={rpg_taint=..-1}] rpg_taint 0
tellraw @a[distance=..24,gamemode=!spectator] %(message)s
kill @s
""" % {"message": raw([text("[驱魔完成] ", "#FFF2A8", True),
                             text("真名已宣、罪性已断，恶魔被逐离此世。", "white")])})


def build_anchor_functions():
    wf("inquest/anchor_tick.mcfunction", """\
scoreboard players set #bound_found rpg_ex_tmp 0
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run scoreboard players set #bound_found rpg_ex_tmp 1
execute if score #bound_found rpg_ex_tmp matches 0 run return run function rpg:inquest/anchor_orphan
scoreboard players remove @s rpg_totem 1
execute if score @s rpg_totem matches ..0 run return run function rpg:inquest/anchor_timeout
particle dust{color:[1.0,0.91,0.52],scale:0.7} ~ ~0.75 ~ 0.28 0.35 0.28 0.01 1 normal
execute if score @s rpg_ex_stage matches 2 run return run function rpg:inquest/anchor_stage2
execute if score @s rpg_ex_stage matches 3 run return run function rpg:inquest/anchor_stage3
execute if score @s rpg_ex_stage matches 4 run return run function rpg:inquest/anchor_stage4
tag @s remove rpg.rite.anchor.active
""")

    stage2 = []
    for q in LORDS:
        stage2.append(
            "execute if score @s rpg_dm_lord matches %(n)d "
            "run return run function rpg:inquest/scan/%(n)d" % q)
    stage2 += [
        "execute if score @s rpg_totem matches 700 run playsound minecraft:block.beacon.ambient player @a[distance=..16] ~ ~ ~ 0.6 1.5",
        "tag @s remove rpg.rite.anchor.active"]
    wf("inquest/anchor_stage2.mcfunction", "\n".join(stage2))

    stage3 = ["scoreboard players set #channel rpg_ex_tmp 0"]
    for q in LORDS:
        stage3.append(
            "execute if score @s rpg_dm_lord matches %(n)d if entity "
            "@a[tag=rpg.name.%(n)d,distance=..6,gamemode=!spectator] "
            "run scoreboard players set #channel rpg_ex_tmp 1" % q)
    stage3 += [
        "execute if score #channel rpg_ex_tmp matches 0 run scoreboard players set @s rpg_ex_time %d" % CHANNEL_TICKS,
        "execute if score #channel rpg_ex_tmp matches 1 run scoreboard players remove @s rpg_ex_time 1",
        "execute if score @s rpg_ex_time matches 80 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 0.9",
        "execute if score @s rpg_ex_time matches 60 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 1.05",
        "execute if score @s rpg_ex_time matches 40 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 1.2",
        "execute if score @s rpg_ex_time matches 20 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 1.4",
        "execute if score #channel rpg_ex_tmp matches 1 run particle end_rod ~ ~0.8 ~ 0.45 0.35 0.45 0.025 3 normal",
        "execute if score @s rpg_ex_time matches ..0 run return run function rpg:inquest/start_banish",
        "tag @s remove rpg.rite.anchor.active"]
    wf("inquest/anchor_stage3.mcfunction", "\n".join(stage3))

    wf("inquest/start_banish.mcfunction", """\
tag @s add rpg.rite.anchor.active
scoreboard players set @s rpg_ex_stage 4
scoreboard players set @s rpg_ex_time 40
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/boss_stage4
title @a[distance=..14,gamemode=!spectator] times 5 35 15
title @a[distance=..14,gamemode=!spectator] title %(title)s
title @a[distance=..14,gamemode=!spectator] subtitle %(subtitle)s
playsound minecraft:block.end_portal.spawn player @a[distance=..28] ~ ~ ~ 0.8 1.5
tag @s remove rpg.rite.anchor.active
""" % dict(
        title=raw([text("Ⅳ · 逐　离", "#FFF2A8", True)]),
        subtitle=raw([text("法阵闭合 · 此世拒绝其名", "white")])) )

    wf("inquest/anchor_stage4.mcfunction", """\
scoreboard players remove @s rpg_ex_time 1
particle end_rod ~ ~0.9 ~ 0.9 0.55 0.9 0.05 8 force
particle soul_fire_flame ~ ~0.7 ~ 0.65 0.4 0.65 0.04 5 force
execute if score @s rpg_ex_time matches 20 run particle flash{color:16777200} ~ ~0.8 ~ 0 0 0 0 1 force
execute if score @s rpg_ex_time matches ..0 run return run function rpg:inquest/anchor_success
tag @s remove rpg.rite.anchor.active
""")

    wf("inquest/anchor_success.mcfunction", """\
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/boss_success
particle explosion ~ ~0.7 ~ 0.3 0.25 0.3 0 2 force
particle end_rod ~ ~0.8 ~ 1.3 0.8 1.3 0.14 100 force
playsound minecraft:block.beacon.deactivate player @a[distance=..24] ~ ~ ~ 1 1.7
kill @s
""")

    wf("inquest/anchor_timeout.mcfunction", """\
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/fail
tellraw @a[distance=..18,gamemode=!spectator] %(message)s
particle large_smoke ~ ~0.7 ~ 0.7 0.5 0.7 0.08 35 normal
kill @s
""" % {"message": raw([text("[法阵熄灭] ", "dark_red", True),
                             text("未能在时限内完成宣判。", "gray")])})

    wf("inquest/anchor_orphan.mcfunction", """\
tag @s remove rpg.rite.anchor.active
particle smoke ~ ~0.7 ~ 0.4 0.3 0.4 0.05 12 normal
kill @s
""")


def patch_runtime():
    patch_once(
        "taint/advent_tick.mcfunction",
        "execute if entity @s[tag=!rpg.advent.timed] run function rpg:taint/advent_arm\n",
        "function rpg:inquest/boss_tick\n"
        "execute if entity @s[scores={rpg_ex_stage=2..}] run return 0\n")

    patch_once(
        "rite/beat.mcfunction",
        "# 一支图腾一拍。净化与反转两套节拍，从这里分开。\n",
        "execute if entity @s[tag=rpg.rite.anchor] run return run function rpg:inquest/anchor_tick\n")

    patch_once(
        "command/tick_end.mcfunction",
        "execute as @a[tag=rpg.holy] run function rpg:command/holy_effects\n",
        "# 显形阶段在 tick 尾再次清除烟幕续上的隐身；这里只扫正在举行仪式的七柱。\n"
        "execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.visible] run effect clear @s minecraft:invisibility\n")

    for q in LORDS:
        for i in range(1, 6):
            rel = "taint/sk%d_%d.mcfunction" % (q["n"], i)
            hook = ("# 携圣器亲历这一招，记下一份不可重复的罪证。\n"
                    "execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] "
                    "run function rpg:inquest/clue/%d_%d\n" % (q["n"], i))
            src = read(rel)
            if ("function rpg:inquest/clue/%d_%d" % (q["n"], i)) not in src:
                write(rel, hook + src)


def validate_output():
    for n in range(1, 8):
        lord = read("taint/lord%d.mcfunction" % n)
        if "Health:700f" not in lord or "base:700f" not in lord:
            raise RuntimeError("lord%d did not inherit 700 health" % n)
        for i in range(1, 6):
            skill = read("taint/sk%d_%d.mcfunction" % (n, i))
            if skill.count("function rpg:inquest/clue/%d_%d" % (n, i)) != 1:
                raise RuntimeError("clue hook mismatch: %d/%d" % (n, i))
        recount = read("inquest/recount/%d.mcfunction" % n)
        if recount.count("run scoreboard players add @s rpg_case%d 1" % n) != 5:
            raise RuntimeError("clue recount mismatch: %d" % n)
    reset = read("inquest/reset_self.mcfunction")
    if reset.count("tag @s remove rpg.name.") != 7 or reset.count("tag @s remove rpg.clue.") != 35:
        raise RuntimeError("inquest reset coverage mismatch")
    beat = read("rite/beat.mcfunction")
    advent = read("taint/advent_tick.mcfunction")
    if beat.count("function rpg:inquest/anchor_tick") != 1:
        raise RuntimeError("anchor tick route missing or duplicated")
    if advent.count("function rpg:inquest/boss_tick") != 1:
        raise RuntimeError("boss tick route missing or duplicated")


def main():
    added = add_objectives()
    build_clues()
    build_boss_functions()
    build_anchor_functions()
    patch_runtime()
    validate_output()
    print("true-name rite: 7 lords, 35 unique clues (any 3), 4 ritual stages, hp=%d" % MAX_HP)
    print("true-name rite: objectives +%d; multiplayer anchor ids enabled" % len(added))


if __name__ == "__main__":
    main()
