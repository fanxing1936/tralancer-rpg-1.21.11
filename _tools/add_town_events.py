# -*- coding: utf-8 -*-
"""三场全村副本（《开局参与感》策划书第三节）：别西卜降临（驱魔）、空缺者事件（战斗）、女巫处刑（世界观）。

- 每座镇每个现实日从三场里随机一场（和昨天不同）。当天第一个游戏内夜晚、镇上有人时开始；告示板上也能「现在就开始」。
  一天打完就没了。同一时间全大陆只跑一场（多人服各镇轮流）。
- 镇上 96 格内的玩家都算参与，怪的数量和血量按人数加。失败也给一半奖励。
- 白天的「风声」：镇民按今晚的副本说闲话（RB/RH/RW 台词）。
- 女巫那场救下的人就是边缘者；听完她讲，林中营地向你敞开（恶魔阵营的入口，add_demon.py）。

python add_town_events.py ../rpg
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
E = "rpg:town/ev"
O = "rpg_te"
TW = "rpg_tw"
COUNT = [0]
TOWNS = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "town_ref", "towns.json"), encoding="utf-8"))
N = sorted(int(k) for k in TOWNS if not TOWNS[k].get("lm"))
IN = "@a[tag=rpg.tw.in]"
GOLD = ui.BROADCAST_HOLY
NAME = ui.BROADCAST_NAME
BODY = ui.BROADCAST_BODY
EV = {1: ("别西卜降临", "The Lord of Flies", "粮仓", "#B5D957"), 2: ("空缺者事件", "The Hollow", "墓地与镇口", "#A8B4C0"), 3: ("女巫处刑", "The Burning", "广场刑台", "#D97AD9")}
HINT = {1: "粮仓里的麦子发黑了。神父说今晚要做一场驱魔。", 2: "墓地的土是松的。夜里有人看见没有脸的人。", 3: "审判官进了城，广场上搭起了刑台。明早要烧女巫。"}
RUMOR = {1: ["RB01", "RB02", "RB03", "RB04"], 2: ["RH01", "RH02", "RH03", "RH04"], 3: ["RW01", "RW02", "RW03", "RW04"]}
LIMIT = 900   # 秒
GLYPH = {1: "\ue7d0", 2: "\ue7d1", 3: "\ue7d2"}     # add_town_art.py 的 rpg:town_icons


def J(c):
    return json.dumps(c, ensure_ascii=False, separators=(",", ":"))


def T(text, colour=BODY, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def fn(name, lines):
    path = os.path.join(FUNC, "town", "ev", name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT[0] += 1


def wj(rel, doc):
    path = os.path.join(DP, "data", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)


def tag_values(name, values):
    path = os.path.join(DP, "data", "rpg", "tags", "function", name + ".json")
    doc = json.load(io.open(path, encoding="utf-8")) if os.path.exists(path) else {"values": []}
    for v in values:
        if v not in doc["values"]:
            doc["values"].append(v)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1)


def tag(text, colour=GOLD, who=IN):
    return "tellraw %s %s" % (who, J(["", T("〖副本〗", colour, True), T(ui.GAP + text, BODY)]))


def at_anchor(anchor, cmd):
    """在当前副本那座镇的某个锚点上执行。"""
    if cmd.startswith("positioned "):
        cmd = "execute " + cmd
    return "execute as @e[type=minecraft:marker,tag=rpg.tw.at.%s] if score @s %s_id = #run %s at @s run %s" % (anchor, TW, O, cmd)


def at_in(anchor, cmd):
    if cmd.startswith("positioned "):
        cmd = "execute " + cmd
    return "execute as @e[type=minecraft:marker,tag=rpg.tw.in.%s] if score @s %s_id = #run %s at @s run %s" % (anchor, TW, O, cmd)


# ============================================================================ 调度
def core():
    fn("load", ["scoreboard objectives add %s dummy" % O, "scoreboard objectives add rpg_te_seen dummy",
                "bossbar add rpg:town_ev \"\"", "bossbar set rpg:town_ev color yellow", "bossbar set rpg:town_ev style notched_10",
                "scoreboard players set #run %s 0" % O, "schedule function %s/sec 20t" % E, "schedule function %s/quick 5t" % E])
    roll = ["# 新的现实日：每座镇抽今晚的副本（和昨天不同），状态清零"]
    for i in N:
        roll += ["scoreboard players operation #evp%d %s = #ev%d %s" % (i, O, i, O),
                 "execute store result score #ev%d %s run random value 1..3" % (i, O),
                 "execute if score #ev%d %s = #evp%d %s run scoreboard players add #ev%d %s 1" % (i, O, i, O, i, O),
                 "execute if score #ev%d %s matches 4 run scoreboard players set #ev%d %s 1" % (i, O, i, O),
                 "scoreboard players set #es%d %s 0" % (i, O)]
    fn("newday", roll)
    tag_values("town_newday", [E + "/newday"])
    sec = ["# 每秒：开场判断、进行中的副本、白天的风声",
           "schedule function %s/sec 20t" % E,
           "execute store result score #tod %s run time query daytime" % O,
           "execute if score #run %s matches 1.. run return run function %s/step" % (O, E),
           "execute if score #tod %s matches 13000..13100 run function %s/night" % (O, E),
           "scoreboard players add #rumor %s 1" % O,
           "execute if score #rumor %s matches 70.. if score #tod %s matches 1000..12000 run function %s/rumors" % (O, O, E)]
    fn("sec", sec)
    # 入夜：有人在镇上、今天还没打过的镇开场
    night = ["# 入夜（as 服务器）：第一座有人在、今天还没打过的镇开场"]
    for i in N:
        night.append("execute if score #run %s matches 0 if score #es%d %s matches 0 in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] if score @s %s_id matches %d at @s if entity @a[distance=..80,gamemode=!spectator] run function %s/begin {t:%d}"
                     % (O, i, O, TW, i, E, i))
    fn("night", night)
    # 开场（宏 t）
    fn("begin", ["$scoreboard players set #run %s $(t)" % O,
                 "$scoreboard players operation #kind %s = #ev$(t) %s" % (O, O),
                 "$scoreboard players set #es$(t) %s 1" % O,
                 "execute if score #kind %s matches 0 run scoreboard players set #kind %s 1" % (O, O),
                 "scoreboard players set #ph %s 0" % O, "scoreboard players set #et %s 0" % O, "scoreboard players set #tt %s 0" % O,
                 "tag @a remove rpg.tw.in",
                 "execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] if score @s %s_id = #run %s at @s run function %s/begin_at" % (TW, O, E),
                 "execute store result score #np %s if entity @a[tag=rpg.tw.in]" % O,
                 "execute if score #np %s matches 0 run scoreboard players set #np %s 1" % (O, O),
                 "bossbar set rpg:town_ev players @a[tag=rpg.tw.in]", "bossbar set rpg:town_ev visible true",
                 "execute if score #kind %s matches 1 run function %s/g/start" % (O, E),
                 "execute if score #kind %s matches 2 run function %s/h/start" % (O, E),
                 "execute if score #kind %s matches 3 run function %s/w/start" % (O, E)])
    fn("begin_at", ["scoreboard players set @s %s_ev 1" % TW, "tag @a[distance=..96,gamemode=!spectator] add rpg.tw.in",
                    "playsound minecraft:block.bell.use ambient @a[distance=..120] ~ ~ ~ 3 0.7",
                    "playsound minecraft:block.bell.resonate ambient @a[distance=..120] ~ ~ ~ 2 0.7"])
    for k, (name, en, where, col) in EV.items():
        fn("title%d" % k, ["title @a[tag=rpg.tw.in] times 10 60 20",
                           "title @a[tag=rpg.tw.in] title " + J(["", T(name, col, True)]),
                           "title @a[tag=rpg.tw.in] subtitle " + J(["", T(where + "　", BODY), T(ui.fraktur(en), ui.BROADCAST_GLOSS)]),
                           "bossbar set rpg:town_ev name " + J(["", {"text": GLYPH[k], "font": "rpg:town_icons", "color": "white"}, T(" " + name, col, True)])])
    step = ["# 进行中（每秒）：参与者跟着走；超时就失败",
            "scoreboard players add #et %s 1" % O,
            "execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] if score @s %s_id = #run %s at @s run tag @a[distance=..110,gamemode=!spectator] add rpg.tw.in" % (TW, O),
            "bossbar set rpg:town_ev players @a[tag=rpg.tw.in]",
            "execute if score #et %s matches %d.. run return run function %s/fail" % (O, LIMIT, E),
            "execute if score #kind %s matches 1 run function %s/g/step" % (O, E),
            "execute if score #kind %s matches 2 run function %s/h/step" % (O, E),
            "execute if score #kind %s matches 3 run function %s/w/step" % (O, E)]
    fn("step", step)
    fn("quick", ["schedule function %s/quick 5t" % E,
                 "execute if score #run %s matches 1.. if score #kind %s matches 2 run function %s/h/quick" % (O, O, E)])
    # 结束
    fn("win", ["# 成功：全额奖励",
               tag("副本完成。", GOLD),
               "execute as @a[tag=rpg.tw.in] run function %s/reward_%s" % (E, "full"),
               "function %s/stop" % E])
    fn("fail", ["# 失败：一半奖励，镇子第二天自己修好",
                tag("这一夜没守住……失败也有一半的收获。", ui.WARN)] + TT.say("EL07", IN) + [
                "execute as @a[tag=rpg.tw.in] run function %s/reward_half" % E,
                "function %s/stop" % E])
    rew = lambda half: ["# 奖励（as 参与者）：#kind 1 驱魔 2 战斗 3 世界观",
                        "scoreboard players operation #t rpg_tl = #run %s" % O,
                        "function rpg:town/life/rep_add {n:%d}" % (8 if half else 20),
                        "function rpg:events/bt/town_event",
                        "loot give @s loot rpg:world/currency", "loot give @s loot rpg:forge/item/soul", "loot give @s loot rpg:forge/item/soul"] + ([] if half else [
                        "loot give @s loot rpg:world/currency", "loot give @s loot rpg:forge/item/soul",
                        "execute if score #kind %s matches 1 run function rpg:alc/give/holy" % O,
                        "execute if score #kind %s matches 1 run loot give @s loot rpg:potion/blank_rite" % O,
                        "execute if score #kind %s matches 2 run loot give @s loot rpg:loot/loot" % O,
                        "execute if score #kind %s matches 2 run loot give @s loot rpg:forge/item/forge_stone" % O,
                        "execute if score #kind %s matches 3 run loot give @s loot rpg:world/sin_shard_%d" % (O, 6),
                        "execute if score #kind %s matches 3 if entity @s[tag=rpg.dm] run loot give @s loot rpg:world/sin_shard_6" % O,
                        "execute if score #kind %s matches 3 if entity @s[tag=rpg.dm] run loot give @s loot rpg:world/currency" % O])
    fn("reward_full", rew(False))
    fn("reward_half", rew(True))
    fn("stop", ["# 收场：怪、道具、标记都清掉；安全区恢复",
                "execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] if score @s %s_id = #run %s run scoreboard players set @s %s_ev 0" % (TW, O, TW),
                "execute in minecraft:overworld as @e[tag=rpg.tw.ev] run function %s/remove" % E,
                "bossbar set rpg:town_ev visible false",
                "tag @a remove rpg.tw.in", "tag @a remove rpg.te.cut",
                "scoreboard players set #run %s 0" % O])
    fn("remove", ["execute on passengers run kill @s", "tp @s ~ -400 ~", "kill @s"])
    # 告示板 / 神父 / 镇民 用的
    bt = ["# 告示板上今晚的副本（as 玩家，#t = 镇号）→ rpg:town ev.name / ev.hint", "scoreboard players set #k %s 0" % O]
    for i in N:
        bt.append("execute if score #t rpg_tl matches %d run scoreboard players operation #k %s = #ev%d %s" % (i, O, i, O))
        bt.append("execute if score #t rpg_tl matches %d if score #es%d %s matches 1.. run scoreboard players set #k %s 9" % (i, i, O, O))
    for k, (name, *_r) in EV.items():
        bt.append('execute if score #k %s matches %d run data modify storage rpg:town ev set value {name:"%s",hint:"%s",icon:"rpg:town/%s"}' % (O, k, name, HINT[k], ("ev_granary", "ev_hollow", "ev_witch")[k - 1]))
    bt.append('execute if score #k %s matches 0 run data modify storage rpg:town ev set value {name:"（还没定）",hint:"今天的风声还没传开。",icon:"rpg:town/holy_fire"}' % O)
    bt.append('execute if score #k %s matches 9 run data modify storage rpg:town ev set value {name:"今天的已经过去了",hint:"明天还会有事。",icon:"rpg:town/holy_fire"}' % O)
    fn("board_text", bt)
    fn("priest_info", ["function %s/board_text" % E, "function %s/priest_info_m with storage rpg:town ev" % E] + TT.say("PR07", "@s"))
    fn("priest_info_m", ["$tellraw @s " + J(["", T("〖驱魔委托〗", GOLD, True), T(ui.GAP + "今晚：", BODY), T("$(name)", NAME, True), T("　$(hint)", BODY)])])
    sn = ["# 告示板「现在就开始」（as 玩家，#t = 镇号）",
          "execute if score #run %s matches 1.. run return run tellraw @s %s" % (O, J(["", T("〖副本〗", GOLD, True), T(ui.GAP + "别处的副本还没打完，稍等。", BODY)]))]
    for i in N:
        sn.append("execute if score #t rpg_tl matches %d if score #es%d %s matches 1.. run return run tellraw @s %s" % (i, i, O, J(["", T("〖副本〗", GOLD, True), T(ui.GAP + "今天的已经打过了。", BODY)])))
        sn.append("execute if score #t rpg_tl matches %d if score #ev%d %s matches 0 run execute store result score #ev%d %s run random value 1..3" % (i, i, O, i, O))
        sn.append("execute if score #t rpg_tl matches %d run return run function %s/begin {t:%d}" % (i, E, i))
    fn("start_now", sn)
    ro = ["# 镇民（as 被点的镇民 or 玩家，#t 镇号）说一句今天的风声", "scoreboard players set #k %s 0" % O]
    for i in N:
        ro.append("execute if score #t rpg_tl matches %d run scoreboard players operation #k %s = #ev%d %s" % (i, O, i, O))
    # 谁说话就说谁的台词（用户 2026-11-28：「少年说农夫的台词」）：台词表里每句都有说话人（农妇 / 农夫 / 少年）
    who = {"farmwife": 1, "farmer": 2, "youth": 3}
    ro += ["execute if entity @s[type=minecraft:villager] run scoreboard players set #folk rpg_tl 0",
           "execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.farmwife] run scoreboard players set #folk rpg_tl 1",
           "execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.farmer] run scoreboard players set #folk rpg_tl 2",
           "execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.lad] run scoreboard players set #folk rpg_tl 3"]
    calm = {2: ["TH05"]}                                   # 没有副本时的闲话：只有农夫有
    for k, ids in list(RUMOR.items()) + [(0, None)]:
        for f in (1, 2, 3):
            mine = [p for p in ids if TT.LINES[p]["speaker"] == [s for s, v in who.items() if v == f][0]] if ids else calm.get(f, [])
            if not mine:
                continue
            sub = "r/k%d_f%d" % (k, f)
            body = ["execute store result score #r %s run random value 0..%d" % (O, len(mine) - 1)]
            for n, pid in enumerate(mine):
                body.append("execute if score #r %s matches %d run return run function %s/r/%s" % (O, n, E, pid.lower()))
                fn("r/%s" % pid.lower(), TT.say(pid, "@a[distance=..16]"))
            fn(sub, body)
            ro.append("execute if score #k %s matches %d if score #folk rpg_tl matches %d run return run function %s/%s" % (O, k, f, E, sub))
    fn("rumor_one", ro)
    rum = ["# 白天的风声：每 70 秒，有人在的镇上，镇民说一句", "scoreboard players set #rumor %s 0" % O]
    rum.append("execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] at @s if entity @a[distance=..120,gamemode=!spectator] run function %s/rumor_at" % E)
    fn("rumors", rum)
    fn("rumor_at", ["scoreboard players operation #t rpg_tl = @s %s_id" % TW,
                    "execute as @a[distance=..120,gamemode=!spectator,limit=1,sort=random] at @s as @e[type=minecraft:villager,tag=rpg.tnpc.folk,distance=..16,limit=1,sort=nearest] at @s run function %s/rumor_one" % E])
    hook_tag(DP, "load", E + "/load", False)


# ============================================================================ 1 别西卜降临（粮仓）
def granary():
    G = E + "/g"
    traces = [(-6, -5, "PR10", "苍蝇团"), (5, -3, "PR11", "腐烂的麦袋"), (0, 6, "PR12", "地上的印记")]
    start = ["function %s/title1" % E] + TT.say("PR09", IN) + [tag("跟着神父去粮仓：找出三处痕迹（右键）。"),
             "bossbar set rpg:town_ev max 3", "bossbar set rpg:town_ev value 0", "scoreboard players set #ph %s 1" % O, "scoreboard players set #found %s 0" % O]
    for n, (dx, dz, line, name) in enumerate(traces):
        start.append(at_in("granary", "positioned ~%d ~ ~%d run function %s/trace {n:%d}" % (dx, dz, G, n + 1)))
        fn("g/t%d" % (n + 1), TT.say(line, IN) + ["scoreboard players add #found %s 1" % O,
                                                  "execute store result bossbar rpg:town_ev value run scoreboard players get #found %s" % O,
                                                  tag("找到了：%s（%s / 3）" % (name, "%d" % (n + 1)))])
    fn("g/start", start)
    fn("g/trace", ['execute positioned ~1 ~ ~1 run function rpg:town/prop {n:"crate_pile"}', '$summon minecraft:interaction ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.trace","rpg.te.tr$(n)"],width:1.2f,height:1.4f,response:1b}',
                   'summon minecraft:item_display ~ ~0.4 ~ {Tags:["rpg.tw.ev"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:town/fx_flies"}},billboard:"center"}'])
    wj("rpg/advancement/town/trace.json", {"criteria": {"t": {"trigger": "minecraft:player_interacted_with_entity", "conditions": {
        "entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": "{Tags:[\"rpg.te.trace\"]}"}}]}}},
        "rewards": {"function": G + "/touch"}})
    fn("g/touch", ["advancement revoke @s only rpg:town/trace"] +
       ["execute as @e[type=minecraft:interaction,tag=rpg.te.tr%d,distance=..6] at @s run function %s/found {n:%d}" % (n, G, n) for n in (1, 2, 3)] +
       ["execute as @e[type=minecraft:interaction,tag=rpg.te.circle,distance=..6] run function %s/totem" % G])
    fn("g/found", ["$scoreboard players set #tn %s $(n)" % O] + ["execute if score #tn %s matches %d run function %s/t%d" % (O, n, G, n) for n in (1, 2, 3)] + [ "particle minecraft:dust{color:[0.35,0.42,0.12],scale:1.4} ~ ~0.8 ~ 0.5 0.5 0.5 0 30",
                   "kill @e[type=minecraft:item_display,tag=rpg.tw.ev,distance=..1.5]", "kill @s",
                   "execute if score #found %s matches 3 run function %s/named" % (O, G)])
    fn("g/named", TT.say("PR13", IN) + TT.say("PR14", IN) + [
        "execute as @a[tag=rpg.tw.in] run function rpg:alc/give/totem", "execute as @a[tag=rpg.tw.in] run function rpg:alc/give/holy",
        tag("在粮仓门口立图腾（拿着驱魔图腾右键法阵），再扔驱魔圣水点燃它。"),
        at_anchor("granary", 'summon minecraft:interaction ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.circle","rpg.te.trace"],width:3f,height:0.6f,response:1b}'),
        at_anchor("granary", 'summon minecraft:marker ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.cm"]}'),
        "scoreboard players set #ph %s 2" % O, "scoreboard players set #totem %s 0" % O])
    fn("g/totem", ["# 右键法阵（as 法阵；@p 是右键的人）",
                   "execute if score #totem %s matches 1 run return 0" % O,
                   "execute unless items entity @p[tag=rpg.tw.in,distance=..6] weapon.mainhand minecraft:totem_of_undying run return run tellraw @p %s" % J(["", T("〖副本〗", GOLD, True), T(ui.GAP + "拿着驱魔图腾右键法阵。", BODY)]),
                   "item modify entity @p[tag=rpg.tw.in,distance=..6] weapon.mainhand {function:\"minecraft:set_count\",count:-1,add:true}",
                   "scoreboard players set #totem %s 1" % O,
                   "execute at @s run summon minecraft:item_display ~ ~1 ~ {Tags:[\"rpg.tw.ev\"],item:{id:\"minecraft:totem_of_undying\",count:1},billboard:\"vertical\"}",
                   "execute at @s run playsound minecraft:block.wood.place player @a[distance=..16] ~ ~ ~ 1 0.8",
                   tag("图腾立起来了。现在扔驱魔圣水点燃它。")])
    # 第二阶：等圣水
    fn("g/step", ["execute if score #ph %s matches 2 if score #totem %s matches 1 as @e[type=minecraft:marker,tag=rpg.te.cm] at @s if entity @e[type=minecraft:area_effect_cloud,tag=rpg.holy_water,distance=..5] run function %s/lit" % (O, O, G),
                  "execute if score #ph %s matches 3 run function %s/hold" % (O, G),
                  "execute if score #ph %s matches 4 run function %s/kneel_wait" % (O, G)])
    fn("g/lit", TT.say("PR15", IN) + [
        "scoreboard players set #ph %s 3" % O, "scoreboard players set #tt %s 0" % O, "scoreboard players set #stab %s 100" % O,
        "bossbar set rpg:town_ev max 100", "bossbar set rpg:town_ev value 100",
        "bossbar set rpg:town_ev name " + J(["", T("别西卜降临", EV[1][3], True), T("　法阵稳定度", BODY)]),
        "particle minecraft:end_rod ~ ~0.3 ~ 2 0.1 2 0.02 60",
        "playsound minecraft:block.beacon.activate block @a[distance=..32] ~ ~ ~ 1 0.8",
        tag("法阵亮了。守住它两分钟：别让蝇群扑到圣火上（站在法阵里能稳住它）。"),
        at_in("granary", "function %s/avatar" % G)])
    fn("g/avatar", ["# 别西卜的化身：已有的别西卜模型，挂在一只弱化的卫道士上",
                    'summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.av"],PersistenceRequired:1b,CustomName:%s,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:60},{id:"minecraft:attack_damage",base:5},{id:"minecraft:movement_speed",base:0.22}],Health:60f}' % J(T("别西卜的化身", "#B5D957", True)),
                    "execute as @e[type=minecraft:vindicator,tag=rpg.te.av,distance=..1] at @s run function rpg:beelzebub/dress",
                    "execute as @e[type=minecraft:vindicator,tag=rpg.te.av,distance=..1] run function %s/avatar_hp" % G])
    fn("g/avatar_hp", ["scoreboard players operation #hp %s = #np %s" % (O, O), "scoreboard players operation #hp %s *= #30 %s" % (O, O), "scoreboard players add #hp %s 60" % O,
                       "execute store result storage rpg:town hp.v int 1 run scoreboard players get #hp %s" % O,
                       "function %s/set_hp with storage rpg:town hp" % E])
    fn("set_hp", ["$attribute @s minecraft:max_health base set $(v)", "$data modify entity @s Health set value $(v)f"])
    fn("g/hold", ["# 守阵（每秒）：蝇群靠近法阵就掉稳定度，有人站在法阵里回一点",
                  "scoreboard players add #tt %s 1" % O,
                  "execute as @e[type=minecraft:marker,tag=rpg.te.cm] at @s store result score #near %s if entity @e[tag=rpg.te.fly,distance=..4]" % O,
                  "scoreboard players operation #stab %s -= #near %s" % (O, O),
                  "execute as @e[type=minecraft:marker,tag=rpg.te.cm] at @s if entity @a[tag=rpg.tw.in,distance=..3] run scoreboard players add #stab %s 1" % O,
                  "execute if score #stab %s matches 101.. run scoreboard players set #stab %s 100" % (O, O),
                  "execute store result bossbar rpg:town_ev value run scoreboard players get #stab %s" % O,
                  "execute as @e[type=minecraft:marker,tag=rpg.te.cm] at @s run particle minecraft:dust{color:[1.0,0.85,0.35],scale:1.0} ~ ~0.2 ~ 1.6 0.05 1.6 0 14",
                  "scoreboard players operation #m %s = #tt %s" % (O, O), "scoreboard players operation #m %s %%= #12 %s" % (O, O),
                  "execute if score #m %s matches 0 run function %s/flies" % (O, G),
                  "execute if score #tt %s matches 60 run function %s/half" % (O, G),
                  "execute if score #stab %s matches ..0 run return run function %s/fail" % (O, E),
                  "execute if score #tt %s matches 120.. run function %s/kneel" % (O, G)])
    fn("g/half", TT.say("PR16", IN))
    fn("g/flies", ["# 一波蝇群（2 + 人数）", "scoreboard players operation #k %s = #np %s" % (O, O), "scoreboard players add #k %s 2" % O,
                   at_in("granary", "function %s/fly_n" % G)])
    fn("g/fly_n", ['summon minecraft:silverfish ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.fly"],PersistenceRequired:1b,CustomName:%s}' % J(T("蝇群", "#B5D957")),
                   "particle minecraft:dust{color:[0.2,0.25,0.08],scale:1.2} ~ ~0.5 ~ 0.6 0.4 0.6 0 16",
                   "scoreboard players remove #k %s 1" % O, "execute if score #k %s matches 1.. run function %s/fly_n" % (O, G)])
    fn("g/kneel", TT.say("PR17", IN) + [
        "scoreboard players set #ph %s 4" % O,
        "execute as @e[tag=rpg.te.fly] run function %s/remove" % E,
        "execute as @e[type=minecraft:vindicator,tag=rpg.te.av] run data merge entity @s {NoAI:1b,Invulnerable:1b}",
        "execute as @a[tag=rpg.tw.in] run function %s/verdict" % G])
    acts = [("消灭", ui.VERDICTS["消灭"], 1), ("放逐", ui.VERDICTS["放逐"], 2), ("封印", ui.VERDICTS["封印"], 3)]
    def vd(extra):
        a = acts + ([("悄悄放走", ui.RITUAL, 4)] if extra else [])
        doc = {"type": "minecraft:multi_action", "title": ["", T("驱魔 · ", GOLD, True), T("裁决", NAME, True), T(" " + ui.fraktur("Verdict"), ui.BROADCAST_GLOSS)],
               "body": [{"type": "minecraft:plain_message", "width": 280, "contents": ["", T("别西卜的化身跪在法阵里。由你来裁决。", BODY)]}],
               "actions": [{"label": T(l, c, True), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_te_v set %d" % v}} for l, c, v in a],
               "columns": 2, "can_close_with_escape": False, "pause": False, "after_action": "close"}
        return "dialog show @s " + J(ui.darken(doc))
    fn("g/verdict", ["scoreboard players enable @s rpg_te_v", "execute if entity @s[tag=rpg.dm] run return run " + vd(True), vd(False)])
    fn("g/kneel_wait", ["scoreboard players add #tt %s 1" % O,
                        "execute as @a[tag=rpg.tw.in,scores={rpg_te_v=1..}] run function %s/judged" % G,
                        "execute if score #tt %s matches 160.. run function %s/judge_default" % (O, G)])
    fn("g/judge_default", ["scoreboard players set @p[tag=rpg.tw.in] rpg_te_v 3", "execute as @p[tag=rpg.tw.in] run function %s/judged" % G])
    fn("g/judged", ["scoreboard players operation #v %s = @s rpg_te_v" % O, "scoreboard players set @s rpg_te_v 0",
                    "scoreboard players add @a[tag=rpg.tw.in] rpg_ex_rites 1",
                    "execute if score #v %s matches 1 run tellraw @a[tag=rpg.tw.in] %s" % (O, J(["", T("〖裁决〗", ui.VERDICTS["消灭"], True), T(ui.GAP + "化身在圣火里烧尽了。", BODY)])),
                    "execute if score #v %s matches 2 run tellraw @a[tag=rpg.tw.in] %s" % (O, J(["", T("〖裁决〗", ui.VERDICTS["放逐"], True), T(ui.GAP + "化身被逐回了深渊。", BODY)])),
                    "execute if score #v %s matches 3 run tellraw @a[tag=rpg.tw.in] %s" % (O, J(["", T("〖裁决〗", ui.VERDICTS["封印"], True), T(ui.GAP + "化身被封进了图腾里。", BODY)])),
                    "execute if score #v %s matches 4 run tellraw @s %s" % (O, J(["", T("〖裁决〗", ui.RITUAL, True), T(ui.GAP + "你悄悄松开了法阵的一角。它看了你一眼，化成蝇群散了。别人只看见它消失。", BODY)])),
                    "execute if score #v %s matches 4 run scoreboard players add @s rpg_dm_rep 10" % O,
                    "execute as @e[type=minecraft:vindicator,tag=rpg.te.av] at @s run particle minecraft:large_smoke ~ ~1 ~ 0.4 0.8 0.4 0.02 40"] + TT.say("PR18", IN) + [
                    "function %s/win" % E])
    wj("rpg/advancement/town/v_dummy.json", {"criteria": {"i": {"trigger": "minecraft:impossible"}}})


# ============================================================================ 2 空缺者事件（墓地 → 镇口）
def hollow():
    H = E + "/h"
    fn("h/start", ["function %s/title2" % E] + TT.say("HO01", IN) + [
        tag("空心人从墓地出来了。看着它们，它们就不动；一转身，它就近了一点。别让它们走到天使像。"),
        "scoreboard players set #ph %s 1" % O, "scoreboard players set #wave %s 0" % O, "scoreboard players set #reach %s 0" % O,
        "bossbar set rpg:town_ev max 3", "bossbar set rpg:town_ev value 0", "function %s/wave" % H])
    fn("h/wave", ["scoreboard players add #wave %s 1" % O,
                  "execute store result bossbar rpg:town_ev value run scoreboard players get #wave %s" % O,
                  "bossbar set rpg:town_ev name " + J(["", T("空缺者事件", EV[2][3], True), T("　三波防守", BODY)]),
                  "scoreboard players operation #k %s = #np %s" % (O, O),
                  "execute if score #wave %s matches 1 run scoreboard players operation #k %s *= #2 %s" % (O, O, O),
                  "execute if score #wave %s matches 2.. run scoreboard players operation #k %s *= #3 %s" % (O, O, O),
                  "scoreboard players add #k %s 3" % O,
                  "execute if score #wave %s matches 2 run scoreboard players add #k %s 2" % (O, O),
                  "execute if score #wave %s matches 3 run scoreboard players add #k %s 4" % (O, O),
                  at_anchor("grave", "function %s/spawn_n" % H),
                  "execute if score #wave %s matches 2 run function %s/drag" % (O, H),
                  "execute if score #wave %s matches 3 run function %s/giant" % (O, H),
                  "execute if score #wave %s matches 1 run " % O + tag("第一波。", EV[2][3]),
                  "execute if score #wave %s matches 2 run " % O + tag("第二波：它们开始抓人了。", EV[2][3]),
                  "execute if score #wave %s matches 3 run " % O + tag("第三波。最后那个……在变大。", EV[2][3])])
    fn("h/spawn_n", ["execute store result score #rx %s run random value -6..6" % O, "execute store result score #rz %s run random value -5..5" % O,
                     "execute store result storage rpg:town hv.x int 1 run scoreboard players get #rx %s" % O,
                     "execute store result storage rpg:town hv.z int 1 run scoreboard players get #rz %s" % O,
                     "function %s/spawn_one with storage rpg:town hv" % H,
                     "scoreboard players remove #k %s 1" % O, "execute if score #k %s matches 1.. run function %s/spawn_n" % (O, H)])
    fn("h/spawn_one", ["$execute positioned ~$(x) ~ ~$(z) positioned over motion_blocking_no_leaves run function %s/hollow_at" % H])
    fn("h/hollow_at", ['summon minecraft:zombie ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.hol"],PersistenceRequired:1b,CanPickUpLoot:0b,CustomName:%s,attributes:[{id:"minecraft:max_health",base:26},{id:"minecraft:movement_speed",base:0.26},{id:"minecraft:follow_range",base:48}],Health:26f}' % J(T("空心人", "#A8B4C0")),
                       "particle minecraft:block{block_state:\"minecraft:dirt\"} ~ ~0.3 ~ 0.4 0.2 0.4 0.1 24",
                       "playsound minecraft:block.rooted_dirt.break hostile @a[distance=..24] ~ ~ ~ 1 0.6",
                       "execute as @e[type=minecraft:zombie,tag=rpg.te.hol,distance=..1] at @s run function #rpg:town_dress"])
    fn("h/giant", TT.say("HO03", IN) + [at_anchor("grave", 'summon minecraft:zombie ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.hol","rpg.te.big"],PersistenceRequired:1b,CanPickUpLoot:0b,CustomName:%s,attributes:[{id:"minecraft:max_health",base:160},{id:"minecraft:scale",base:1.8},{id:"minecraft:attack_damage",base:9},{id:"minecraft:movement_speed",base:0.24},{id:"minecraft:knockback_resistance",base:0.8}],Health:160f}' % J(T("显形的空缺者", "#C8D2DC", True))),
        at_anchor("grave", "execute as @e[type=minecraft:zombie,tag=rpg.te.big,distance=..2] at @s run function #rpg:town_dress"),
        "execute as @e[type=minecraft:zombie,tag=rpg.te.big] run function %s/big_hp" % H])
    fn("h/big_hp", ["scoreboard players operation #hp %s = #np %s" % (O, O), "scoreboard players operation #hp %s *= #50 %s" % (O, O), "scoreboard players add #hp %s 110" % O,
                    "execute store result storage rpg:town hp.v int 1 run scoreboard players get #hp %s" % O,
                    "function %s/set_hp with storage rpg:town hp" % E])
    fn("h/drag", TT.say("HO02", IN) + ["execute in minecraft:overworld as @e[type=minecraft:villager,tag=rpg.tnpc.folk,limit=1,sort=random] if score @s %s_id = #run %s run function %s/taken" % (TW, O, H)])
    fn("h/taken", ["tag @s add rpg.te.taken", "data merge entity @s {Invulnerable:1b}",
                   "execute store result score #ox %s run data get entity @s Pos[0]" % O, "execute store result score #oz %s run data get entity @s Pos[2]" % O,
                   at_anchor("grave", "tp @e[type=minecraft:villager,tag=rpg.te.taken] ^ ^ ^-14"),
                   at_anchor("grave", "execute as @e[type=minecraft:villager,tag=rpg.te.taken] at @s run tp @s ~ ~ ~ ~ ~"),
                   tag("有人被拖走了！到墓地那边把人救回来（走到他身边）。", ui.WARN)])
    fn("h/step", ["# 每秒：救人、清点",
                  "execute as @e[type=minecraft:villager,tag=rpg.te.taken] at @s if entity @a[tag=rpg.tw.in,distance=..3] run function %s/rescued" % H,
                  "execute as @e[type=minecraft:villager,tag=rpg.te.taken] at @s run particle minecraft:soul ~ ~1 ~ 0.3 0.4 0.3 0.01 4",
                  "execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] if score @s %s_id = #run %s at @s as @e[tag=rpg.te.hol,distance=..5] run function %s/reached" % (TW, O, H),
                  "execute if score #reach %s matches 6.. run return run function %s/fail" % (O, E),
                  "execute store result score #left %s if entity @e[tag=rpg.te.hol]" % O,
                  "execute if score #left %s matches 0 if score #wave %s matches ..2 run return run function %s/wave" % (O, O, H),
                  "execute if score #left %s matches 0 if score #wave %s matches 3 run function %s/dawn" % (O, O, H)])
    fn("h/reached", ["scoreboard players add #reach %s 1" % O, "function %s/remove" % E,
                     tag("一个空心人走到了天使像下……（%s）" % "再有几个，镇子就守不住了", ui.WARN)])
    fn("h/rescued", ["tag @s remove rpg.te.taken", "tag @s add rpg.te.saved"] + TT.say("TH01", "@a[distance=..12]") + TT.say("TH02", "@a[distance=..12]") + [
        "execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.at.spawn] if score @s %s_id = #run %s at @s run tp @e[type=minecraft:villager,tag=rpg.te.saved] ~3 ~ ~2" % (TW, O),
        "tag @e[type=minecraft:villager,tag=rpg.te.saved] remove rpg.te.saved"])
    fn("h/dawn", TT.say("HO04", IN) + ["execute if score #tod %s matches 13000..23000 run time set 23500" % O, "function %s/win" % E])
    # 「看着就不动」：每 5 刻，沿每个参与者的视线取样，视线上的空心人冻住，其余的走
    fn("h/quick", ["tag @e[tag=rpg.te.hol] remove rpg.te.seen",
                   "execute as @a[tag=rpg.tw.in] at @s anchored eyes run function %s/look" % H,
                   "execute as @e[tag=rpg.te.hol,tag=rpg.te.seen,tag=!rpg.te.big] run data modify entity @s NoAI set value 1b",
                   "execute as @e[tag=rpg.te.hol,tag=!rpg.te.seen] run data modify entity @s NoAI set value 0b"])
    fn("h/look", ["execute positioned ^ ^ ^%d run tag @e[tag=rpg.te.hol,distance=..%s] add rpg.te.seen" % (d, "1.6" if d < 10 else "2.6") for d in range(2, 34, 3)])


# ============================================================================ 3 女巫处刑（劫法场）
def witch():
    W = E + "/w"
    fn("w/start", ["function %s/title3" % E] + TT.say("IQ01", IN) + TT.say("IQ02", IN) + [
        "scoreboard players set #ph %s 1" % O, "scoreboard players set #tt %s 0" % O,
        "bossbar set rpg:town_ev max 4", "bossbar set rpg:town_ev value 1",
        at_anchor("plaza", "execute facing entity @e[type=minecraft:marker,tag=rpg.tw.in.center,limit=1,sort=nearest] feet rotated ~ 0 run function %s/stage" % W),
        tag("刑台上绑着一个人。去刑台后面的巷子，有人在等你。")])
    fn("w/stage", ["# 刑台（广场中间，地下城的吊笼与柴堆模型由 add_town_models 挂上）：女巫、审判官、两名圣卫、兜帽人",
                   'summon minecraft:villager ~ ~ ~ {Tags:["rpg.tw.ev","rpg.tnpc","rpg.tnpc.witch","rpg.te.witch"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:%s,VillagerData:{type:"minecraft:swamp",profession:"minecraft:none",level:1}}' % J(T("女巫", "#B48AD8", True)),
                   "execute as @e[type=minecraft:villager,tag=rpg.te.witch,distance=..1] at @s run function #rpg:town_dress",
                   "execute positioned ~ ~ ~1 run function rpg:town/prop {n:\"pyre\"}",
                   "execute positioned ~ ~ ~ run function rpg:town/prop {n:\"cage\"}",
                   'summon minecraft:vindicator ~3 ~ ~ {Tags:["rpg.te.inq.new"],PersistenceRequired:1b,CanPickUpLoot:0b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:90},{id:"minecraft:armor",base:10},{id:"minecraft:attack_damage",base:7}],Health:90f}',
                   "execute as @e[type=minecraft:vindicator,tag=rpg.te.inq.new,limit=1] at @s run function %s/inq" % W,
                   "execute positioned ~-4 ~ ~3 run function rpg:tower_guard/summon", "execute positioned ~4 ~ ~-3 run function rpg:tower_guard/summon",
                   "execute as @e[tag=rpg.tg,distance=..8,tag=!rpg.tw.guard] run function %s/guard" % W,
                   "execute positioned ^ ^ ^-10 positioned over motion_blocking_no_leaves run function %s/hood" % W])
    fn("w/inq", ["tag @s remove rpg.te.inq.new", "tag @s add rpg.tw.ev", "tag @s add rpg.te.inq", "tag @s add rpg.te.g",
                 "data merge entity @s {CustomName:%s,NoAI:1b}" % J(T("审判官", "#B8902F", True)), "function #rpg:town_dress"])
    fn("w/guard", ["tag @s add rpg.tw.ev", "tag @s add rpg.te.g", "data merge entity @s {NoAI:1b}"])
    fn("w/hood", ['summon minecraft:villager ~ ~ ~ {Tags:["rpg.tw.ev","rpg.tnpc","rpg.tnpc.hood","rpg.te.hood"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:%s,VillagerData:{type:"minecraft:swamp",profession:"minecraft:none",level:1}}' % J(T("兜帽人", ui.RITUAL, True)),
                  "execute as @e[type=minecraft:villager,tag=rpg.te.hood,distance=..1] at @s run function #rpg:town_dress"])
    # 右键兜帽人 / 女巫：rpg:town/talk 走 rpg.tnpc 的路由，这里给 talk 加两个角色
    fn("w/hood_talk", ["execute unless score #run %s matches 1.. run return 0" % O,
                       "execute unless score #kind %s matches 3 run return 0" % O,
                       "execute unless score #ph %s matches 1 run return 0" % O] + TT.say("EW01", IN) + TT.say("EW02", IN) + TT.say("EW04", IN) + [
                       "execute if score #np %s matches 1 run function %s/solo" % (O, W),
                       "scoreboard players set #ph %s 2" % O, "bossbar set rpg:town_ev value 2",
                       "execute as @e[tag=rpg.te.g] run data merge entity @s {NoAI:0b}"] + TT.say("EW06", IN) + TT.say("EW07", IN) + [
                       tag("火起来了。去刑台割断绳子（右键女巫，站在她身边三秒）。圣卫只打晕，别杀。"),
                       at_anchor("plaza", "positioned ~8 ~ ~8 positioned over motion_blocking_no_leaves run setblock ~ ~ ~ minecraft:fire"),
                       at_anchor("plaza", "execute as @e[tag=rpg.tg,tag=rpg.te.g,distance=..20,limit=1] run tp @s ~8 ~ ~8")])
    fn("w/solo", TT.say("EW05", IN))
    fn("w/witch_talk", ["execute unless score #run %s matches 1.. run return 0" % O,
                        "execute if score #ph %s matches 2 run tag @s add rpg.te.cut" % O,
                        "execute if score #ph %s matches 2 run title @s actionbar %s" % (O, J(["", T("割绳子……站着别动", BODY)]))])
    fn("w/step", ["# 每秒",
                  "execute if score #ph %s matches 2 run function %s/cutting" % (O, W),
                  "execute if score #ph %s matches 2..3 run function %s/stun" % (O, W),
                  "execute if score #ph %s matches 3 run function %s/escort" % (O, W),
                  "execute if score #ph %s matches 4 run function %s/story" % (O, W)])
    fn("w/cutting", ["execute as @a[tag=rpg.te.cut] at @s unless entity @e[tag=rpg.te.witch,distance=..3] run tag @s remove rpg.te.cut",
                     "execute if entity @a[tag=rpg.te.cut] run scoreboard players add #cut %s 1" % O,
                     "execute if score #cut %s matches 3.. run function %s/freed" % (O, W)])
    fn("w/freed", TT.say("EW08", IN) + TT.say("IQ03", IN) + [
        "tag @a remove rpg.te.cut", "scoreboard players set #ph %s 3" % O, "scoreboard players set #tt %s 0" % O, "bossbar set rpg:town_ev value 3",
        "execute as @e[tag=rpg.te.inq] run data merge entity @s {NoAI:0b}",
        tag("护送她到镇外林子里的营地。她走得慢，挡住后面追来的人。")])
    fn("w/stun", ["# 圣卫只打晕：血量低到三成就跪下（不再动、不再挨打）",
                  "execute as @e[tag=rpg.te.g,tag=!rpg.te.down] store result score #h %s run data get entity @s Health" % O,
                  "execute as @e[tag=rpg.te.g,tag=!rpg.te.down] run function %s/stun_one" % W])
    fn("w/stun_one", ["execute store result score #h %s run data get entity @s Health" % O,
                      "execute if score #h %s matches ..30 run function %s/down" % (O, W)])
    fn("w/down", ["tag @s add rpg.te.down", "data merge entity @s {NoAI:1b,Invulnerable:1b}",
                  "execute at @s run particle minecraft:crit ~ ~1.5 ~ 0.3 0.3 0.3 0.1 12",
                  "execute if entity @s[tag=rpg.te.inq] run function %s/inq_down" % W])
    fn("w/inq_down", TT.say("IQ08", IN))
    fn("w/escort", ["# 她跟着最近的参与者走（每秒一格多），到营地就停",
                    "scoreboard players add #tt %s 1" % O,
                    "execute if score #tt %s matches 20 run function %s/l_iq04" % (O, W),
                    "execute if score #tt %s matches 40 run function %s/l_ew09" % (O, W),
                    "execute if score #tt %s matches 70 run function %s/l_iq05" % (O, W),

                    "execute as @e[tag=rpg.te.witch] at @s run particle minecraft:dust{color:[0.6,0.4,0.8],scale:1} ~ ~1 ~ 0.2 0.5 0.2 0 4",
                    "execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.at.camp] if score @s %s_id = #run %s at @s if entity @e[tag=rpg.te.witch,distance=..10] run function %s/arrive" % (TW, O, W)])
    # 护送：她自己跟着最近的参与者走（用户 2026-11-28：「女巫不会自主移动」）。每刻一小步，离人三格内就站住，太远（24 格外）就等。
    fn("w/follow_tick", ["execute unless score #run %s matches 1.. run return 0" % O, "execute unless score #kind %s matches 3 run return 0" % O,
                         "execute unless score #ph %s matches 3 run return 0" % O,
                         "execute as @e[type=minecraft:villager,tag=rpg.te.witch] at @s run function %s/follow" % W])
    fn("w/follow", ["execute if entity @a[tag=rpg.tw.in,distance=..3,gamemode=!spectator] run return run tp @s ~ ~ ~ facing entity @p[tag=rpg.tw.in] feet",
                    "execute unless entity @a[tag=rpg.tw.in,distance=..24,gamemode=!spectator] run return 0",
                    "execute facing entity @p[tag=rpg.tw.in] feet rotated ~ 0 positioned ^ ^ ^0.17 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~ ~ 0"])
    hook_tag(DP, "tick", W + "/follow_tick", False)
    fn("w/l_iq04", TT.say("IQ04", IN))
    fn("w/l_ew09", TT.say("EW09", IN) + TT.say("EW10", IN))
    fn("w/l_iq05", TT.say("IQ05", IN))
    fn("w/arrive", TT.say("EW11", IN) + [
        "scoreboard players set #ph %s 4" % O, "scoreboard players set #tt %s 0" % O, "bossbar set rpg:town_ev value 4",
        "execute as @e[tag=rpg.te.g] run function %s/remove" % E,
        tag("到了。坐下来听她讲。")])
    story = ["EW12", "WI01", "WI02", "WI03", "WI04", "WI05", "WI06", "WI07", "WI08", "WI09", "WI10", "EW13"]
    st = ["scoreboard players add #tt %s 1" % O]
    for n, pid in enumerate(story):
        st.append("execute if score #tt %s matches %d run function %s/s_%s" % (O, 2 + n * 6, W, pid.lower()))
        extra = []
        if pid == "WI09":
            extra = ["execute as @a[tag=rpg.tw.in] run loot give @s loot rpg:world/sin_shard_6"]
        if pid == "WI10":
            extra = ["tag @a[tag=rpg.tw.in] add rpg.tl.camp", "tag @a[tag=rpg.tw.in] add rpg.tl.witch"]
        fn("w/s_%s" % pid.lower(), TT.say(pid, IN) + extra)
    st.append("execute if score #tt %s matches %d run function %s/win" % (O, 2 + len(story) * 6, E))
    fn("w/story", st)


def talk_routes():
    """给 rpg:town/life/talk 补兜帽人、女巫的右键。"""
    p = os.path.join(FUNC, "town", "life", "whoami.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg.tnpc.hood" not in s:
        s += "execute if entity @s[tag=rpg.tnpc.hood] run scoreboard players set #role rpg_tl 8\nexecute if entity @s[tag=rpg.tnpc.witch] run scoreboard players set #role rpg_tl 9\n"
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    p = os.path.join(FUNC, "town", "life", "talk.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "w/hood_talk" not in s:
        s += ("execute if score #role rpg_tl matches 8 if score #run %s matches 1.. if score #kind %s matches 3 run return run function %s/w/hood_talk\n"
              "execute if score #role rpg_tl matches 9 if score #run %s matches 1.. run return run function %s/w/witch_talk\n"
              "execute if score #role rpg_tl matches 9 run return run function rpg:town/demon/witch_talk\n") % (O, O, E, O, E)
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    p = os.path.join(FUNC, "town", "life", "load.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg_te_v" not in s:
        s += "scoreboard objectives add rpg_te_v trigger\n"
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def consts():
    p = os.path.join(FUNC, "town", "ev", "load.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    s += "\n".join("scoreboard players set #%d %s %d" % (v, O, v) for v in (2, 3, 12, 30, 50)) + "\n"
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def main():
    core()
    granary()
    hollow()
    witch()
    talk_routes()
    consts()
    print("town events: %d 个函数" % COUNT[0])


if __name__ == "__main__":
    main()
