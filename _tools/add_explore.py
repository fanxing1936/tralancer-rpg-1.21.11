# -*- coding: utf-8 -*-
"""探索与见闻（用户 2026-11-27：「初见演出、怪物情报、武器熟练都制作出来；探索地图是和打怪同等重要的事情，也应该有一些奖励」）。

- 群系：每进一个群系，屏幕中央一行「火山 · 危险 V · 建议第 6 阶」（策划书「进群系时提醒」，只提醒不拦）。
  第一次进：初见演出（大标题 + 一句旁白 + 一声和弦），记入见闻录，给阅历、探索点和材料；十九个走遍得称号「破碎大陆的旅人」。
- 城镇：第一次走进一座镇也记一笔、给奖励。
- 里程：每走一千格（步行、疾跑、骑马、坐船、游泳、滑翔都算）给探索点和阅历。
- 探索点到 50 / 150 / 300 / 500 / 800 / 1200 各给一份奖励（图纸碎片、符文、史诗图纸、符石、传说图纸……），和打怪的掉落同一档次。
- 怪物情报：同一种怪杀满 25 只，解锁它的弱点和掉落；之后打它 +5%。
- 武器熟练：长剑、战斧、重锤、长弓、劲弩各自记命中次数，200 / 800 / 2000 三级，每级 +3%；重锤一级起破甲（目标护甲 −3）。
- 见闻录：面板「旅程」页的按钮，三页：群系与城镇、怪物情报、武器熟练。

python add_explore.py ../rpg
"""
import io
import json
import os
import sys

import rpg_ui_style as ui
import town_text as TT
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
X = "rpg:explore"
COUNT = [0]
BODY = ui.BROADCAST_BODY
NAME = ui.BROADCAST_NAME
GOLD = ui.BROADCAST_HOLY
GLOSS = ui.BROADCAST_GLOSS
DANGER = {1: ("I", ui.READY, 1), 2: ("II", "#E8D27A", 2), 3: ("III", "#FFA15C", 4), 4: ("IV", ui.WARN, 5), 5: ("V", ui.PASSION, 6)}
GROUPS = [  # (键, 名, 英文, 危险, 群系)
    ("plains", "平原", "Plains", 1, ["plains"]),
    ("forest", "森林", "Forest", 1, ["forest"]),
    ("wildfield", "原野", "Wildfield", 1, ["wildfield"]),
    ("lavender", "雾月花森林", "Mistmoon Wood", 1, ["lavender_forest"]),
    ("golden", "丰饶森林", "Golden Wood", 1, ["golden_forest"]),
    ("desert", "沙漠", "Desert", 2, ["desert"]),
    ("snowfield", "雪原", "Snowfield", 2, ["snowfield"]),
    ("taiga", "云杉木森林", "Geyser Taiga", 2, ["geyser_taiga"]),
    ("mesa", "平顶山沙漠", "Mesa Valley", 3, ["mesa_valley"]),
    ("eroded", "侵蚀沙漠", "Eroded Desert", 3, ["eroded_desert"]),
    ("ashwood", "焦木林", "Ashwood", 3, ["ashwood"]),
    ("stone", "石林", "Stone Forest", 3, ["stone_forest"]),
    ("warped", "诡异高原", "Warped Plateau", 4, ["warped_plateau"]),
    ("glacier", "巨大冰原", "Glacier Spires", 4, ["glacier_spires"]),
    ("alpine", "高山", "Alpine", 4, ["alpine", "alpine_slope", "alpine_rock", "alpine_cliff"]),
    ("volcano", "火山", "Volcano", 5, ["volcano"]),
    ("war", "战争前线", "War Front", 5, ["war_front"]),
    ("cliffs", "海岸断崖", "Sea Cliffs", 2, ["sea_cliffs"]),
    ("sea", "海与河", "Seas and Rivers", 1, ["ocean", "deep_ocean", "frozen_ocean", "river", "frozen_river", "beach", "snowy_beach"]),
]
MOBS = [  # (类型, 名, 弱点, 掉落)
    ("zombie", "僵尸", "怕火；亡灵，圣器与「亡灵杀手」克它", "腐肉、残魂"), ("husk", "尸壳", "同僵尸；不怕太阳", "腐肉、残魂"),
    ("drowned", "溺尸", "离了水就慢；亡灵", "腐肉、铜锭、三叉戟（少见）"), ("skeleton", "骷髅", "近身打，它拉不开弓；亡灵", "骨头、箭"),
    ("stray", "流浪者", "同骷髅；箭带迟缓，别站远", "骨头、迟缓之箭"), ("bogged", "沼骸", "同骷髅；箭带剧毒", "骨头、剧毒之箭"),
    ("spider", "蜘蛛", "白天不主动打人；节肢，「节肢杀手」克它", "线、蜘蛛眼"), ("cave_spider", "洞穴蜘蛛", "血薄；被咬会中毒，带牛奶", "线、蜘蛛眼"),
    ("creeper", "苦力怕", "听到嘶声就后撤；被雷劈会变强", "火药"), ("enderman", "末影人", "怕水；别直视它", "末影珍珠"),
    ("witch", "女巫", "会给自己喝药，先打断；怕近身", "药材、玻璃瓶"), ("pillager", "掠夺者", "弩手，拉近距离", "箭、弩"),
    ("vindicator", "卫道士", "斧子很疼，用盾挡", "绿宝石"), ("evoker", "唤魔者", "先杀它，再处理尖牙和恼鬼", "不死图腾"),
    ("ravager", "劫掠兽", "咆哮前会停一下，绕到侧面", "鞍"), ("phantom", "幻翼", "睡觉就不来了；不死生物", "幻翼膜"),
    ("slime", "史莱姆", "大的会分裂，一次清干净", "黏液球"), ("silverfish", "蠹虫", "成群出现，范围攻击", "无"),
    ("blaze", "烈焰人", "怕雪球；远程别硬拼", "烈焰棒"), ("wither_skeleton", "凋灵骷髅", "攻击带凋零，保持血量", "煤炭、凋灵骷髅头（少见）"),
    ("magma_cube", "岩浆怪", "同史莱姆；不怕火", "岩浆膏"), ("ghast", "恶魂", "把火球打回去", "恶魂之泪、火药"),
    ("piglin_brute", "猪灵蛮兵", "血厚，别贪刀", "金斧"), ("hoglin", "疣猪兽", "怕诡异菌", "猪排、皮革"),
    ("guardian", "守卫者", "激光要蓄一会儿，躲到柱子后面", "海晶碎片"), ("breeze", "旋风人", "会弹开弹射物，近身打", "旋风棒"),
]
INTEL_AT = 25
CLASSES = [  # (键, 名, 判定, 近战/远程)
    ("sword", "长剑", "#minecraft:swords", "melee"), ("axe", "战斧", "#minecraft:axes", "melee"), ("mace", "重锤", "minecraft:mace", "melee"),
    ("bow", "长弓", "minecraft:bow", "ranged"), ("crossbow", "劲弩", "minecraft:crossbow", "ranged"),
]
MASTERY = (200, 800, 2000)
MILESTONES = [(50, ["loot give @s loot rpg:world/bp_fragment"] * 3 + ["loot give @s loot rpg:world/currency"] * 3, "图纸碎片 ×3、货币 ×3"),
              (150, ["loot give @s loot rpg:forge/rune_any", "loot give @s loot rpg:forge/item/forge_stone"], "符文 ×1、锻石 ×1"),
              (300, ["loot give @s loot rpg:world/bp_epic_any"], "史诗图纸 ×1"),
              (500, ["loot give @s loot rpg:forge/stone_any"] + ["loot give @s loot rpg:world/currency"] * 6, "符石 ×1、货币 ×6"),
              (800, ["loot give @s loot rpg:forge/rune_any", "loot give @s loot rpg:forge/stone_any", "loot give @s loot rpg:world/bp_epic_any"], "符文、符石、史诗图纸"),
              (1200, ["loot give @s loot rpg:world/bp_legend_any"], "传说图纸 ×1")]
STATS = ["walk_one_cm", "sprint_one_cm", "horse_one_cm", "boat_one_cm", "swim_one_cm", "aviate_one_cm", "walk_on_water_one_cm", "walk_under_water_one_cm"]


def J(c):
    return json.dumps(c, ensure_ascii=False, separators=(",", ":"))


def T(text, colour=BODY, bold=False, italic=False):
    return {"text": text, "color": colour, "bold": bold, "italic": italic}


def fn(name, lines):
    path = os.path.join(FUNC, "explore", name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT[0] += 1


def wj(rel, doc):
    path = os.path.join(DP, "data", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)


def read(rel):
    return io.open(os.path.join(FUNC, rel + ".mcfunction"), encoding="utf-8").read()


def write(rel, s):
    io.open(os.path.join(FUNC, rel + ".mcfunction"), "w", encoding="utf-8", newline="\n").write(s)


def note(tagname, text, colour=GOLD, who="@s"):
    return "tellraw %s %s" % (who, J(["", T("〖%s〗" % tagname, colour, True), T(ui.GAP + text, BODY)]))


def points(n, found=False):
    return ["scoreboard players add @s rpg_x_pt %d" % n, "scoreboard players add @s rpg_ex_xp %d" % n, "function %s/milestone" % X] + (
        ["function rpg:events/bt/explore"] if found else [])


# ============================================================================ 群系
def biomes():
    objs = ["rpg_xb dummy", "rpg_x_pt dummy", "rpg_x_cd dummy", "rpg_xb_n dummy", "rpg_xt_n dummy", "rpg_xd dummy", "rpg_x_do trigger"]
    objs += ["rpg_xs_%d minecraft.custom:minecraft.%s" % (n, s) for n, s in enumerate(STATS)]
    objs += ["rpg_kl_%s minecraft.killed:minecraft.%s" % (m[0], m[0]) for m in MOBS]
    objs += ["rpg_ms_%s dummy" % c[0] for c in CLASSES]
    fn("load", ["scoreboard objectives add " + o for o in objs] + ["schedule function %s/sec 20t" % X])
    hook_tag(DP, "load", X + "/load", False)
    for n, (k, zh, en, d, bl) in enumerate(GROUPS, 1):
        wj("rpg/tags/worldgen/biome/ex/%s.json" % k, {"values": ["rpg:" + b for b in bl]})
    sec = ["# 每秒（rpg:explore/load 起的循环）", "schedule function %s/sec 20t" % X,
           "execute as @a[gamemode=!spectator] at @s run function %s/each" % X]
    fn("sec", sec)
    each = ["# 每秒（as/at 玩家）",
            "execute if score @s rpg_x_cd matches 1.. run scoreboard players remove @s rpg_x_cd 1",
            "execute if dimension minecraft:overworld run function %s/biome" % X,
            "function %s/dist" % X,
            "function %s/intel_check" % X,
            "function %s/mastery_check" % X,
            "execute if score @s rpg_x_do matches 1.. run function %s/do" % X]
    fn("each", each)
    bio = ["scoreboard players set #b rpg_xb 0"]
    for n, (k, *_r) in enumerate(GROUPS, 1):
        bio.append("execute if biome ~ ~ ~ #rpg:ex/%s run scoreboard players set #b rpg_xb %d" % (k, n))
    bio += ["execute if score #b rpg_xb = @s rpg_xb run return 0",
            "scoreboard players operation @s rpg_xb = #b rpg_xb",
            "execute if score #b rpg_xb matches 0 run return 0"]
    bio += ["execute if score #b rpg_xb matches %d run return run function %s/b/%s" % (n, X, k) for n, (k, *_r) in enumerate(GROUPS, 1)]
    fn("biome", bio)
    for n, (k, zh, en, d, bl) in enumerate(GROUPS, 1):
        dn, col, tier = DANGER[d]
        rec = "建议第 %d 阶" % tier if tier > 1 else "新手也能走"
        fn("b/%s" % k, ["execute unless entity @s[tag=rpg.xb.%s] run return run function %s/first/%s" % (k, X, k),
                        "execute if score @s rpg_x_cd matches 1.. run return 0",
                        "scoreboard players set @s rpg_x_cd 8",
                        "title @s times 5 35 12",
                        "title @s title " + J(["", T(zh, NAME, True)]),
                        "title @s subtitle " + J(["", T("危险 " + dn, col, True), T(" · " + rec + "  ", BODY), T(ui.fraktur(en), GLOSS)])])
        line = TT.LINES["EX%02d" % n]
        reward = d * 10
        first = ["# 初见：%s" % zh, "tag @s add rpg.xb.%s" % k, "scoreboard players add @s rpg_xb_n 1", "scoreboard players set @s rpg_x_cd 12",
                 "title @s times 15 70 25",
                 "title @s title " + J(["", T(zh, NAME, True)]),
                 "title @s subtitle " + J(["", T("初见 · ", GOLD, True), T("危险 " + dn, col, True), T(" · " + rec + "  ", BODY), T(ui.fraktur(en), GLOSS)]),
                 "tellraw @s " + J(["", dict(T("　「%s」" % line["zh"], ui.MUTED, italic=True), hover_event={"action": "show_text", "value": T(line["en"], GLOSS)})]),
                 "playsound minecraft:block.amethyst_block.resonate ambient @s ~ ~ ~ 1 0.7",
                 "playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 0.8 0.84",
                 "playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 0.6 1.12",
                 "playsound minecraft:block.note_block.bell ambient @s ~ ~ ~ 0.5 0.63"]
        if TT.has_vo("EX%02d" % n):
            first.append("playsound rpg:vo.town.ex%02d voice @s ~ ~ ~ 1 1" % n)
        first += points(reward, True) + ["loot give @s loot rpg:world/currency"] * d + ["loot give @s loot rpg:forge/item/soul"] * d + [
            note("见闻录", "%s 记入见闻录　阅历 +%d　探索点 +%d" % (zh, reward, reward)),
            "execute if score @s rpg_xb_n matches %d.. run function rpg:quest/title/get_traveler" % len(GROUPS)]
        fn("first/%s" % k, first)


# ============================================================================ 城镇、里程、里程碑
def travel():
    towns = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "town_ref", "towns.json"), encoding="utf-8"))
    tv = ["# 走进一座镇（as 玩家，#w = 镇号）：第一次来就记一笔"]
    for i in sorted(int(k) for k in towns):
        t = towns[str(i)]
        tv.append("execute if score #w rpg_tw matches %d unless entity @s[tag=rpg.xt.%d] run function %s/t/%d" % (i, i, X, i))
        if t.get("lm"):
            fn("t/%d" % i, ["tag @s add rpg.xt.%d" % i] + points(25, True) + ["loot give @s loot rpg:world/currency"] * 3 + ["loot give @s loot rpg:world/bp_fragment"] * 2 + [
                note("见闻录", "发现地标：%s　阅历 +25　探索点 +25" % t["zh"])])
            continue
        fn("t/%d" % i, ["tag @s add rpg.xt.%d" % i, "scoreboard players add @s rpg_xt_n 1"] + points(15, True) + ["loot give @s loot rpg:world/currency"] * 2 + [
            note("见闻录", "第一次来到%s　阅历 +15　探索点 +15" % t["zh"])])
    fn("town_visit", tv)
    s = read("town/where")
    a = "execute if score #w rpg_tw matches 0 run return 0\n"
    assert a in s
    if "explore/town_visit" not in s:
        write("town/where", s.replace(a, a + "function %s/town_visit\n" % X))
    d = ["# 里程：各种移动的厘米数加起来，每满 1000 格给一份"]
    for n, _s in enumerate(STATS):
        d += ["scoreboard players operation @s rpg_xd += @s rpg_xs_%d" % n, "scoreboard players set @s rpg_xs_%d 0" % n]
    d += ["execute if score @s rpg_xd matches 100000.. run function %s/km" % X]
    fn("dist", d)
    fn("km", ["scoreboard players remove @s rpg_xd 100000"] + points(5) + ["title @s actionbar " + J(["", T("又走了一千格　", BODY), T("探索点 +5", GOLD)])])
    ms = ["# 探索点到档（as 玩家）"]
    for n, (at, give, what) in enumerate(MILESTONES):
        ms.append("execute if score @s rpg_x_pt matches %d.. unless entity @s[tag=rpg.xm.%d] run function %s/m/%d" % (at, n, X, n))
        fn("m/%d" % n, ["tag @s add rpg.xm.%d" % n] + give + [note("见闻录", "探索点到了 %d：%s" % (at, what)),
                                                             "playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6 1.1"])
    fn("milestone", ms)


# ============================================================================ 怪物情报、武器熟练
def combat():
    ic = ["# 情报解锁（as 玩家）"]
    for k, zh, weak, drop in MOBS:
        ic.append("execute if score @s rpg_kl_%s matches %d.. unless entity @s[tag=rpg.in.%s] run function %s/in/%s" % (k, INTEL_AT, k, X, k))
        fn("in/%s" % k, ["tag @s add rpg.in.%s" % k] + points(5) + [
            "tellraw @s " + J(["", T("〖怪物情报〗", ui.WARN, True), T(ui.GAP + zh, NAME, True), T("　弱点：" + weak + "　掉落：" + drop, BODY), T("　此后打它 +5%", GOLD)])])
    fn("intel_check", ic)
    mc = ["# 熟练升级（as 玩家）"]
    for k, zh, _sel, _kind in CLASSES:
        for lv, at in enumerate(MASTERY, 1):
            mc.append("execute if score @s rpg_ms_%s matches %d.. unless entity @s[tag=rpg.ms.%s%d] run function %s/ms/%s%d" % (k, at, k, lv, X, k, lv))
            extra = "（重锤：命中的目标护甲 −3）" if k == "mace" and lv == 1 else ""
            fn("ms/%s%d" % (k, lv), ["tag @s add rpg.ms.%s%d" % (k, lv),
                                     "tellraw @s " + J(["", T("〖武器熟练〗", GOLD, True), T(ui.GAP + "%s熟练到了 %d 级：%s伤害 +%d%%%s" % (zh, lv, zh, 3 * lv, extra), BODY)]),
                                     "playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.5 1.4"])
    fn("mastery_check", mc)
    # 挂到锻造的命中钩子上（as 受击者，攻击者 rpg.fg.atk）
    A = "@a[tag=rpg.fg.atk,limit=1]"
    for rel, kind in (("forge/hit/melee", "melee"), ("forge/hit/ranged", "ranged")):
        s = read(rel)
        if "见闻录（add_explore.py）" in s:
            continue
        add = ["# 见闻录（add_explore.py）：怪物情报 +5%、武器熟练"]
        for k, *_r in MOBS:
            add.append("execute if entity @s[type=minecraft:%s] if entity @a[tag=rpg.fg.atk,tag=rpg.in.%s] run scoreboard players add #pct rpg_fg 5" % (k, k))
        for k, zh, sel, ck in CLASSES:
            if ck != kind:
                continue
            add.append("execute if items entity %s weapon.mainhand %s run scoreboard players add @a[tag=rpg.fg.atk] rpg_ms_%s 1" % (A, sel, k))
            for lv in (1, 2, 3):
                add.append("execute if items entity %s weapon.mainhand %s if entity @a[tag=rpg.fg.atk,tag=rpg.ms.%s%d] run scoreboard players add #pct rpg_fg 3" % (A, sel, k, lv))
            if k == "mace":
                add.append("execute if items entity %s weapon.mainhand %s if entity @a[tag=rpg.fg.atk,tag=rpg.ms.mace1] run attribute @s minecraft:armor modifier add rpg:mastery_mace -3 add_value" % (A, sel))
        write(rel, s.rstrip("\n") + "\n" + "\n".join(add) + "\n")


# ============================================================================ 见闻录
def book():
    def head(active):
        acts = [{"label": T(("◆ " if v == active else "") + n, GOLD if v == active else BODY, v == active),
                 "action": {"type": "minecraft:run_command", "command": "/trigger rpg_x_do set %d" % v}} for v, n in ((1, "群系与城镇"), (2, "怪物情报"), (3, "武器熟练"))]
        acts.append({"label": T("‹ 旅程", BODY), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set 22"}})
        return ["data modify storage rpg:panel ui set value " + J(ui.darken({"title": ["", T("旅程 · ", GOLD, True), T("见闻录", NAME, True), T(" " + ui.fraktur("Travel Journal"), GLOSS)],
                                                                             "body": [""], "actions": acts})),
                "data modify storage rpg:panel ui.tab set value 5"]

    def app(comp, cond=""):
        line = "data modify storage rpg:panel ui.body append value " + J(ui.darken(comp))
        if cond:
            line = "execute %s run " % cond + line
        return ("$" + line) if "$(" in line else line

    stats = ["execute store result storage rpg:explore k.%s int 1 run scoreboard players get @s %s" % (n, o) for n, o in
             (("pt", "rpg_x_pt"), ("bn", "rpg_xb_n"), ("tn", "rpg_xt_n"))] + [
            "execute store result storage rpg:explore k.%s int 1 run scoreboard players get @s rpg_kl_%s" % (m[0], m[0]) for m in MOBS] + [
            "execute store result storage rpg:explore k.ms_%s int 1 run scoreboard players get @s rpg_ms_%s" % (c[0], c[0]) for c in CLASSES]
    nxt = ["data modify storage rpg:explore k.nx set value \"都拿到了\""]
    for n, (at, _g, what) in reversed(list(enumerate(MILESTONES))):
        nxt.append("execute unless entity @s[tag=rpg.xm.%d] run data modify storage rpg:explore k.nx set value \"%d 点：%s\"" % (n, at, what))
    fn("stats", stats + nxt)
    # 第 1 页
    p1 = head(1) + [app(T("探索点 ", BODY)), app(T("$(pt)", GOLD, True)), app(T("　下一份：$(nx)\n", BODY)),
                    app(T("群系 $(bn) / %d　　城镇 $(tn) / 20\n\n" % len(GROUPS), BODY))]
    for k, zh, en, d, _b in GROUPS:
        dn, col, tier = DANGER[d]
        p1.append(app(T("✓ " + zh, NAME, True), "if entity @s[tag=rpg.xb.%s]" % k))
        p1.append(app(T("？ ？？？", ui.MUTED), "unless entity @s[tag=rpg.xb.%s]" % k))
        p1.append(app(T("　危险 %s\n" % dn, col)))
    fn("page1_m", p1 + ["function rpg:panel/ui/show"])
    p2 = head(2) + [app(T("同一种怪杀满 %d 只，解锁弱点与掉落，此后打它 +5%%。\n\n" % INTEL_AT, BODY))]
    for k, zh, weak, drop in MOBS:
        p2.append(app(T(zh, NAME, True), "if entity @s[tag=rpg.in.%s]" % k))
        p2.append(app(T("　%s\n　　掉落：%s\n" % (weak, drop), BODY), "if entity @s[tag=rpg.in.%s]" % k))
        p2.append(app(T("？？？", ui.MUTED), "unless entity @s[tag=rpg.in.%s]" % k))
        p2.append(app(T("　已杀 $(%s) / %d\n" % (k, INTEL_AT), ui.MUTED), "unless entity @s[tag=rpg.in.%s]" % k))
    fn("page2_m", p2 + ["function rpg:panel/ui/show"])
    p3 = head(3) + [app(T("同一类武器命中越多，越顺手：%d / %d / %d 次各升一级，每级伤害 +3%%。\n\n" % MASTERY, BODY))]
    for k, zh, _s, _kd in CLASSES:
        p3.append(app(T(zh + "　", NAME, True)))
        for lv in (3, 2, 1):
            p3.append(app(T("%d 级" % lv, GOLD, True), "if entity @s[tag=rpg.ms.%s%d] unless entity @s[tag=rpg.ms.%s%d]" % (k, lv, k, lv + 1) if lv < 3 else "if entity @s[tag=rpg.ms.%s3]" % k))
        p3.append(app(T("未入门", ui.MUTED), "unless entity @s[tag=rpg.ms.%s1]" % k))
        p3.append(app(T("　命中 $(ms_%s)%s\n" % (k, "　（破甲）" if k == "mace" else ""), BODY)))
    fn("page3_m", p3 + ["function rpg:panel/ui/show"])
    acts = [{"label": T(n, GOLD, True), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_x_do set %d" % v}} for v, n in ((1, "群系与城镇"), (2, "怪物情报"), (3, "武器熟练"))]
    acts.append({"label": T("‹ 旅程", BODY), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set 22"}})
    show = {"type": "minecraft:multi_action", "title": ["", T("见闻录", NAME, True), T(" " + ui.fraktur("Travel Journal"), GLOSS)],
            "body": [{"type": "minecraft:plain_message", "width": 320, "contents": "@C@"}], "actions": acts, "columns": 4,
            "can_close_with_escape": True, "pause": False, "after_action": "close"}
    fn("show", ["$dialog show @s " + J(show).replace('"@C@"', "$(c)")])
    for v in (1, 2, 3):
        fn("page%d" % v, ["scoreboard players enable @s rpg_x_do", "function %s/stats" % X, "function %s/page%d_m with storage rpg:explore k" % (X, v)])
    fn("book", ["function %s/page1" % X])
    fn("do", ["scoreboard players operation #do rpg_xb = @s rpg_x_do", "scoreboard players set @s rpg_x_do 0",
              "execute if score #do rpg_xb matches 1 run function %s/page1" % X,
              "execute if score #do rpg_xb matches 2 run function %s/page2" % X,
              "execute if score #do rpg_xb matches 3 run function %s/page3" % X])
    # 面板：旅程页加「见闻录」按钮，rpg_panel 24 打开
    s = read("panel/tick")
    end = "execute if score @s rpg_panel matches 1.. run scoreboard players set @s rpg_panel 0"
    if "explore/book" not in s:
        write("panel/tick", s.replace(end, "execute if score @s rpg_panel matches 24 run function %s/book\n" % X + end))
    s = read("events/jr/body")
    a = "data modify storage rpg:panel ui.tab set value 5"
    if "rpg_panel set 24" not in s:
        btn = {"label": T("见闻录", ui.BROADCAST_HOLY, True), "tooltip": T("群系、城镇、怪物情报、武器熟练", BODY),
               "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set 24"}}
        write("events/jr/body", s.replace(a, "data modify storage rpg:panel ui.actions append value " + J(btn) + "\n" + a))


# ============================================================================ 危险等级：距离 × 群系（策划书「主世界的去处」），失乐园的圈层标题
PL_RINGS = [(160, "伊甸门廊", "Eden Porch", "建议第 2–3 阶", ui.READY), (240, "泥沼", "The Mire", "建议第 4–5 阶", "#FFA15C"),
            (560, "血泽", "The Blood Marsh", "建议第 6–7 阶", ui.WARN), (100000, "灰烬边境", "The Ash March", "建议第 8 阶起", ui.PASSION)]
SCALE = {3: (0.25, 0.15), 4: (0.6, 0.35), 5: (1.0, 0.6)}


def danger():
    towns = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "town_ref", "towns.json"), encoding="utf-8"))
    s = read("panel/tick")
    end = "execute if score @s rpg_panel matches 1.. run scoreboard players set @s rpg_panel 0"
    if "rpg:pl/enter_ok" not in s:
        write("panel/tick", s.replace(end, "execute if score @s rpg_panel matches 25 run function rpg:pl/enter_ok\n" + end))
    each = read("explore/each")
    each += "execute if dimension rpg:paradise_lost run function %s/pl_ring\nexecute unless dimension rpg:paradise_lost run scoreboard players set @s rpg_x_pr 0\n" % X
    write("explore/each", each)
    load = read("explore/load")
    write("explore/load", load + "scoreboard objectives add rpg_x_pr dummy\n")
    ring = ["# 失乐园里换圈（as/at 玩家）", "scoreboard players set #r rpg_xb 4"]
    for n, (r, *_x) in reversed(list(enumerate(PL_RINGS[:3], 1))):
        ring.append("execute positioned 0 83 0 if entity @s[distance=..%d] run scoreboard players set #r rpg_xb %d" % (r, n))
    ring += ["execute if score #r rpg_xb = @s rpg_x_pr run return 0", "scoreboard players operation @s rpg_x_pr = #r rpg_xb"]
    for n, (r, zh, en, rec, col) in enumerate(PL_RINGS, 1):
        ring.append("execute if score #r rpg_xb matches %d run return run function %s/pl/%d" % (n, X, n))
        fn("pl/%d" % n, ["title @s times 5 40 12", "title @s title " + J(["", T(zh, NAME, True)]),
                         "title @s subtitle " + J(["", T(rec, col, True), T("  " + ui.fraktur(en), GLOSS)])])
    fn("pl_ring", ring)
    # 怪物第一次被看见（as/at 怪）：离最近的城镇多远 × 群系危险，取较高者
    mob = ["# 主世界的怪第一次出现（as/at 它）：近郊弱化、不出精英；深处精英多；危险 III–V 的群系加强",
           "tag @s add rpg.ow.s",
           "execute if data entity @s CustomName run return 0",
           "scoreboard players set #lv rpg_xb 1"]
    for k, zh, en, d, _b in GROUPS:
        if d >= 2:
            mob.append("execute if biome ~ ~ ~ #rpg:ex/%s run scoreboard players set #lv rpg_xb %d" % (k, d))
    mob += ["execute store result score #mx rpg_xb run data get entity @s Pos[0]", "execute store result score #mz rpg_xb run data get entity @s Pos[2]",
            "scoreboard players set #best rpg_xb 2147483647"]
    for i in sorted(int(k) for k in towns if not towns[k].get("lm")):
        mob.append("execute if score #s%d rpg_tw matches 3 run function %s/d2 {i:%d}" % (i, X, i))
    mob += ["execute if score #best rpg_xb matches ..360000 if score #lv rpg_xb matches ..2 run return run function %s/weak" % X,
            "execute if score #best rpg_xb matches 4000001.. run tag @s add rpg.ow.deep"]
    for d, (hp, dmg) in SCALE.items():
        mob.append("execute if score #lv rpg_xb matches %d run function %s/lv%d" % (d, X, d))
        fn("lv%d" % d, ["tag @s add rpg.ow.lv%d" % d,
                        "attribute @s minecraft:max_health modifier add rpg:ow_danger %s add_multiplied_base" % hp,
                        "attribute @s minecraft:attack_damage modifier add rpg:ow_danger %s add_multiplied_base" % dmg,
                        "data modify entity @s Health set value 1024f"])
    fn("mob", mob)
    fn("d2", ["scoreboard players operation #dx rpg_xb = #mx rpg_xb", "$scoreboard players operation #dx rpg_xb -= #x$(i) rpg_tw",
              "scoreboard players operation #dz rpg_xb = #mz rpg_xb", "$scoreboard players operation #dz rpg_xb -= #z$(i) rpg_tw",
              "scoreboard players operation #dx rpg_xb *= #dx rpg_xb", "scoreboard players operation #dz rpg_xb *= #dz rpg_xb",
              "scoreboard players operation #dx rpg_xb += #dz rpg_xb", "scoreboard players operation #best rpg_xb < #dx rpg_xb"])
    fn("weak", ["tag @s add rpg.ow.weak",
                "attribute @s minecraft:max_health modifier add rpg:ow_danger -0.3 add_multiplied_base",
                "attribute @s minecraft:attack_damage modifier add rpg:ow_danger -0.3 add_multiplied_base",
                "data modify entity @s Health set value 1024f"])
    sec = read("explore/sec")
    write("explore/sec", sec + "execute in minecraft:overworld as @e[type=#rpg:elite_pool,tag=!rpg.ow.s,tag=!rpg.tw.ev] at @s run function %s/mob\n" % X)
    # 精英：近郊不出、深处翻倍（elite/roll 开头先给怪定级）
    s = read("elite/roll")
    if "explore/mob" not in s:
        s = ("execute unless entity @s[tag=rpg.ow.s] if dimension minecraft:overworld run function %s/mob\n"
             "execute if entity @s[tag=rpg.ow.weak] run return 0\n" % X) + s
        a = "execute if score #nt rpg_el matches 1.. run return 0\n"
        assert a in s
        s = s.replace(a, a + "execute if entity @s[tag=rpg.ow.deep] run scoreboard players operation #p rpg_el *= #2 rpg_el\n", 1)
        write("elite/roll", s)


def journey():
    """旅程页加「故乡与见闻」一节；面板「下一步」加城镇的几条提示（低于原有提示的优先级）。"""
    towns = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "town_ref", "towns.json"), encoding="utf-8"))
    s = read("events/jr/open")
    a = "function rpg:events/jr/body with storage rpg:events v"
    if "rpg_tw_home" not in s:
        add = ['data modify storage rpg:events v merge value {home:"（还没有）",fac:"教廷",rep:0,bn:0,tn:0,pt:0}',
               'execute if entity @s[tag=rpg.dm] run data modify storage rpg:events v.fac set value "恶魔"']
        for k in sorted(towns, key=int):
            t = towns[k]
            if t.get("lm"):
                continue
            add.append('execute if score @s rpg_tw_home matches %s run data modify storage rpg:events v.home set value "%s"' % (k, t["zh"]))
            add.append("execute if score @s rpg_tw_home matches %s store result storage rpg:events v.rep int 1 run scoreboard players get @s rpg_rep_%s" % (k, k))
        add += ["execute store result storage rpg:events v.bn int 1 run scoreboard players get @s rpg_xb_n",
                "execute store result storage rpg:events v.tn int 1 run scoreboard players get @s rpg_xt_n",
                "execute store result storage rpg:events v.pt int 1 run scoreboard players get @s rpg_x_pt"]
        write("events/jr/open", s.replace(a, "\n".join(add) + "\n" + a))
    s = read("events/jr/body")
    a = 'data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"支线\\n"'
    if "$(home)" not in s:
        i = s.index(a)
        line = ("$data modify storage rpg:panel ui.body append value " + J({"text": "", "extra": [
            T("故乡　", ui.BROADCAST_BODY, True), T("$(home)", NAME, True), T("　声望 $(rep)　阵营 $(fac)\n", ui.BROADCAST_BODY),
            T("见闻　", ui.BROADCAST_BODY, True), T("群系 $(bn) / %d　城镇 $(tn) / 20　探索点 $(pt)\n\n" % len(GROUPS), ui.BROADCAST_BODY)]}) + "\n")
        write("events/jr/body", s[:i] + line + s[i:])
    s = read("panel/v2/tree")
    a = 'data modify storage rpg:panel nx set value ""\n'
    if "rpg_tl_gift" not in s:
        hints = [("if score @s rpg_tw_home matches 1.. unless score @s rpg_tl_gift matches 1..", "回故乡的教堂，找神父报到，领新人的那份。"),
                 ("if score @s rpg_tl_gift matches 1.. if score @s rpg_xb_n matches ..2", "出门走走：第一次走进一个群系，见闻录都有奖励。"),
                 ("if score @s rpg_tl_gift matches 1.. unless score @s rpg_tl_fu matches 1..", "告示板上有委托；入夜后，镇上会有一场全村副本。")]
        add = "".join("execute %s run data modify storage rpg:panel nx set value %s\n" % (c, J(t)) for c, t in hints)
        write("panel/v2/tree", s.replace(a, a + add, 1))


def main():
    biomes()
    travel()
    combat()
    book()
    danger()
    journey()
    assert os.path.exists(os.path.join(FUNC, "quest", "title", "get_traveler.mcfunction")), "add_quests.TITLES 里要有 traveler"
    print("explore: %d 个函数" % COUNT[0])


if __name__ == "__main__":
    main()
