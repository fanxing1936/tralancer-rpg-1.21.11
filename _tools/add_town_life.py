# -*- coding: utf-8 -*-
"""城镇的日常：镇上的人、福利、每日循环、支线、声望（《开局参与感》策划书第二、五节）。

- 一个「现实日」= 服务器运行满 24 小时（1 728 000 刻；数据包读不到现实时钟）。#day 每 86400 秒加一。
- 镇上的人：神父（教堂门口）、村长（村长家门口）、吟游诗人（酒馆门口，没有酒馆就在天使像旁）、守夜人（墓地）、
  三位镇民（天使像四周）、两名站岗的圣卫、铁匠（已有的铁匠商人，营火旁）、告示板（天使像另一侧）。
  外观由 add_town_models.py 挂在 #rpg:town_dress 上（地下城模型）；没有就是原版村民。
- 福利：新手大礼包（一次）、每日口粮（每现实日一次）、圣火庇护（两个游戏日或到第 2 阶：受伤降低、死亡不掉东西、在故乡复活）、租屋（声望 40）。
- 支线 9 条、每座镇各自的声望（rpg_rep_<镇号>）：20 口粮加一份 → 40 租屋 → 70 镇上的图纸 → 100 称号「守护者」。

python add_town_life.py ../rpg
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
L = "rpg:town/life"
O = "rpg_tl"
DO = "rpg_tl_do"
TW = "rpg_tw"
COUNT = [0]
TOWNS = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "town_ref", "towns.json"), encoding="utf-8"))
N = sorted(int(k) for k in TOWNS if not TOWNS[k].get("lm"))
DAY = 86400
GOLD = ui.BROADCAST_HOLY
NAME = ui.BROADCAST_NAME
BODY = ui.BROADCAST_BODY
GLOSS = ui.BROADCAST_GLOSS
CUR = 'minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}]'
MAT = lambda k: 'minecraft:paper[minecraft:custom_data~{rpg_mat:"%s"}]' % k
ROLE = {1: "priest", 2: "elder", 3: "bard", 4: "watchman", 5: "child", 6: "board", 7: "folk"}
QUESTS = {  # 编号: (名, 谁给, 一句话)
    1: ("铁匠的学徒", "告示板", "去营火旁熔铸或拆解一件武器"),
    2: ("神父的圣水", "神父", "带来一瓶水、两份糖（海盐）、一块木炭（圣火的灰）"),
    3: ("守夜人", "守夜人", "夜里走到墓地、刑台广场、教堂门口、营火四处"),
    4: ("发黑的麦子", "村长", "到粮仓里待一会儿，找出异味的来源"),
    5: ("失踪的孩子", "神父", "到镇外林子里找一个迷路的孩子"),
    6: ("吟游诗人", "吟游诗人", "在天使像、墓地、林中营地各听一段歌"),
    7: ("寄往邻镇的信", "村长", "把信交给另一座镇的村长"),
    8: ("收税官", "村长", "替教廷收税，还是替村民藏粮"),
    9: ("酒馆赌约", "吟游诗人", "三十秒内打中五个靶子"),
}


def J(c):
    return json.dumps(c, ensure_ascii=False, separators=(",", ":"))


def T(text, colour=BODY, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def fn(name, lines):
    path = os.path.join(FUNC, "town", "life", name + ".mcfunction")
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
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1)


def note(text, colour=BODY, who="@s"):
    return "tellraw %s %s" % (who, J(["", T("〖城镇〗", GOLD, True), T(ui.GAP + text, colour)]))


def card(model, head, lines, colour=NAME):
    """和营火工作台同一套卡片：左边一枚图标，右边标题与说明（add_bench.card）。"""
    return {"type": "minecraft:item", "item": {"id": "minecraft:paper", "count": 1, "components": {"minecraft:item_model": model}},
            "description": {"contents": ["", T(head + "\n", colour, True)] + [T(l + ("\n" if i < len(lines) - 1 else ""), BODY) for i, l in enumerate(lines)],
                            "width": 270},
            "show_decorations": False, "show_tooltip": False, "width": 16, "height": 16}


def dlg(title, gloss, body, actions, columns=2, prefix="城镇"):
    cards = [b for b in body if isinstance(b, dict) and "type" in b]
    text = [b for b in body if not (isinstance(b, dict) and "type" in b)]
    doc = {"type": "minecraft:multi_action", "title": ["", T(prefix + " · ", GOLD, True), T(title, NAME, True), T(" " + ui.fraktur(gloss), GLOSS)],
           "body": ([{"type": "minecraft:plain_message", "width": 300, "contents": ["", *text]}] if text else []) + cards,
           "actions": [{"label": T(l, c, True), "action": {"type": "minecraft:run_command", "command": "/trigger %s set %d" % (DO, v)}} for l, c, v in actions],
           "columns": columns, "exit_action": {"label": T("离开", BODY)}, "can_close_with_escape": True, "pause": False, "after_action": "close"}
    return "dialog show @s " + J(ui.darken(doc))


SCROLL = ('minecraft:paper[minecraft:custom_name=%s,minecraft:lore=[%s,%s,%s,%s],minecraft:custom_data={rpg_home:1b},minecraft:item_model="rpg:town/home_scroll",'
          'minecraft:consumable={consume_seconds:1234567.0f,animation:"none",sound:"minecraft:intentionally_empty",has_consume_particles:false},minecraft:max_stack_size=16]'
          % (J(["", T("[城镇]", GOLD, True), T("余烬归途", "#FFFFFF")]), J(T("+------------------+", "#FFFFFF")), J(T("手持右键，站着念 5 秒，回到故乡", "gray")),
             J(T("挨打或走动会打断", "gray")), J(T("+------------------+", "#FFFFFF"))))


# 镇上发的吃食（用户 2026-11-28：NPC 给的物品要有数据包的命名与 lore）：仍是原版面包、熟牛肉，能吃；图标 rpg:town/<名>
ROT = "store result entity @s Rotation[0] float 1 run random value -180..179"


def food(base, name, lines, key):
    lore = [J(T("+------------------+", "#FFFFFF"))] + [J(T(x, "gray")) for x in lines] + [J(T("+------------------+", "#FFFFFF"))]
    return ('%s[minecraft:custom_name=%s,minecraft:lore=[%s],minecraft:custom_data={rpg_food:"%s"},minecraft:item_model="rpg:town/%s"]'
            % (base, J(["", T("[城镇]", GOLD, True), T(name, "#FFFFFF")]), ",".join(lore), key, key))


BREAD = food("minecraft:bread", "黑麦面包", ["教堂分给每户的口粮", "路上饿了就掰一块"], "rye_bread")
MEAT = food("minecraft:cooked_beef", "腌熏肉", ["熏房里挂了一冬的肉", "比面包顶饿"], "smoked_meat")


def scroll():
    fn("buy_scroll", ["execute store result score #m %s run clear @s %s 0" % (O, CUR),
                      "execute if score #m %s matches ..1 run return run " % O + note("一卷两枚货币。", ui.WARN),
                      "clear @s %s 2" % CUR, "give @s " + SCROLL, note("余烬归途到手。", GOLD)])
    wj("rpg/advancement/town/scroll.json", {"criteria": {"use": {"trigger": "minecraft:using_item", "conditions": {
        "item": {"predicates": {"minecraft:custom_data": "{rpg_home:1b}"}}}}}, "rewards": {"function": L + "/scroll_use"}})
    fn("scroll_use", ["advancement revoke @s only rpg:town/scroll",
                      "execute if entity @s[tag=rpg.tl.ch] run return 0",
                      "execute unless score @s rpg_tw_home matches 1.. run return run " + note("你还没有故乡。", ui.WARN),
                      "tag @s add rpg.tl.ch", "scoreboard players set @s rpg_tl_cht 5", "scoreboard players set @s rpg_tl_dmg 0",
                      "execute store result score @s rpg_tl_px run data get entity @s Pos[0] 4",
                      "execute store result score @s rpg_tl_pz run data get entity @s Pos[2] 4",
                      "playsound minecraft:block.campfire.crackle player @s ~ ~ ~ 1 0.8",
                      "title @s actionbar " + J(["", T("余烬归途：站着别动…… 5", GOLD)])])
    fn("scroll_tick", ["# 每秒（as/at 念着余烬归途的人）",
                       "execute store result score #x %s run data get entity @s Pos[0] 4" % O, "execute store result score #z %s run data get entity @s Pos[2] 4" % O,
                       "execute unless score #x %s = @s rpg_tl_px run return run function %s/scroll_stop" % (O, L),
                       "execute unless score #z %s = @s rpg_tl_pz run return run function %s/scroll_stop" % (O, L),
                       "execute if score @s rpg_tl_dmg matches 1.. run return run function %s/scroll_stop" % L,
                       "scoreboard players remove @s rpg_tl_cht 1",
                       "particle minecraft:small_flame ~ ~1 ~ 0.4 0.6 0.4 0.01 14", "particle minecraft:ash ~ ~1 ~ 0.4 0.6 0.4 0 10",
                       "title @s actionbar " + J(["", T("余烬归途：站着别动…… ", GOLD), {"score": {"name": "@s", "objective": "rpg_tl_cht"}, "color": GOLD}]),
                       "execute if score @s rpg_tl_cht matches ..0 run function %s/scroll_go" % L])
    fn("scroll_stop", ["tag @s remove rpg.tl.ch", "title @s actionbar " + J(["", T("余烬归途被打断了", ui.WARN)])])
    fn("scroll_go", ["tag @s remove rpg.tl.ch",
                     "execute store result storage rpg:town h.i int 1 run scoreboard players get @s rpg_tw_home",
                     "function %s/scroll_go_m with storage rpg:town h" % L])
    fn("scroll_go_m", ["$execute unless score #s$(i) rpg_tw matches 3 run return run " + note("故乡还没建起来，余烬没有地方可去。", ui.WARN),
                       "clear @s minecraft:paper[minecraft:custom_data~{rpg_home:1b}] 1",
                       "particle minecraft:flame ~ ~1 ~ 0.3 0.6 0.3 0.05 30",
                       "function rpg:town/home/arrive"])


def rep_obj(i):
    return "rpg_rep_%d" % i


# ============================================================================ 加载、每秒
def core():
    objs = ["%s dummy" % O, "%s trigger" % DO, "rpg_tl_d dummy", "rpg_tl_cht dummy", "rpg_tl_px dummy", "rpg_tl_pz dummy", "rpg_tl_dmg minecraft.custom:minecraft.damage_taken", "rpg_tl_gift dummy", "rpg_tl_born dummy", "rpg_tl_dc deathCount", "rpg_tl_ch dummy",
            "rpg_tl_fu dummy", "rpg_tl_t dummy", "rpg_tl_wt dummy", "rpg_tl_bd dummy", "rpg_tl_tax dummy", "rpg_tl_hit dummy"]
    objs += ["rpg_tl_q%d dummy" % k for k in QUESTS] + ["rpg_tl_qd%d dummy" % k for k in QUESTS] + ["%s dummy" % rep_obj(i) for i in N]
    fn("load", ["scoreboard objectives add " + o for o in objs] + ["scoreboard players set #day0 %s %d" % (O, DAY), "schedule function %s/sec 20t" % L])
    fn("sec", ["# 每秒：现实日计数、圣火庇护、死后还东西",
               "schedule function %s/sec 20t" % L,
               "scoreboard players add #sec %s 1" % O,
               "scoreboard players operation #day %s = #sec %s" % (O, O),
               "scoreboard players operation #day %s /= #day0 %s" % (O, O),
               "execute unless score #day %s = #lastday %s run function %s/newday" % (O, O, L),
               "execute store result score #gt %s run time query gametime" % O,
               "execute as @a[tag=rpg.tl.holy] run function %s/holy" % L,
               "execute as @a[tag=rpg.tl.kept] at @s unless entity @s[nbt={Health:0.0f}] run function %s/regive" % L,
               "execute as @a[tag=rpg.tl.ch] at @s run function %s/scroll_tick" % L,
               "execute as @a[scores={rpg_tl_q3=1..}] at @s run function %s/q/watch_tick" % L,
               "execute as @a[scores={rpg_tl_q4=1}] at @s run function %s/q/wheat_tick" % L,
               "execute as @a[scores={rpg_tl_q6=1..}] at @s run function %s/q/bard_tick" % L,
               "scoreboard players add #folkt %s 1" % O,
               "execute if score #folkt %s matches 30.. run function %s/folk_scan" % (O, L),
               "execute as @e[type=minecraft:interaction,tag=rpg.tl.target] run function %s/q/target_age" % L,
               "# 镇上的人不交易（用户 2026-11-28「右键都会打开交易面板」）：老存档里已有的村民改成无职业、清掉交易",
               "execute as @e[type=minecraft:villager,tag=rpg.tnpc,tag=!rpg.tl.notrade] run function %s/notrade" % L])
    fn("folk_scan", ["scoreboard players set #folkt %s 0" % O,
                      "execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c,tag=!rpg.tw.lm] at @s if entity @a[distance=..160] run function %s/folk_check" % L])
    fn("notrade", ["# 村民的身体是隐形的（外观是城镇模型），职业只决定交易：改成无职业，就不会再生成交易、不会弹交易面板",
                   "data merge entity @s {VillagerData:{profession:\"minecraft:none\"},Offers:{Recipes:[]}}",
                   "tag @s add rpg.tl.notrade"])
    fn("newday", ["# 新的现实日：#lastday 跟上；每个人的「今天」在用到时再比（rpg_tl_d、rpg_tl_qd*）",
                  "scoreboard players operation #lastday %s = #day %s" % (O, O),
                  "scoreboard players operation #day1 %s = #day %s" % (O, O), "scoreboard players add #day1 %s 1" % O,
                  "function #rpg:town_newday"])
    fn("tick", ["execute as @a[scores={rpg_tl_dc=1..}] at @s run function %s/died" % L,
                "execute as @a[scores={%s=1..}] at @s run function %s/do" % (DO, L),
                "execute as @e[type=minecraft:interaction,tag=rpg.tl.target] if data entity @s attack run function %s/q/target_hit" % L])
    hook_tag(DP, "load", L + "/load", False)
    hook_tag(DP, "tick", L + "/tick", True)
    tag_values("town_newday", [])


# ============================================================================ 圣火庇护（第一次到故乡起两个游戏日，或到原质第 2 阶为止）
def holy():
    fn("holy_start", ["# 圣火庇护开始（as 玩家）",
                      "execute store result score @s rpg_tl_born run time query gametime",
                      "tag @s add rpg.tl.holy",
                      note("教堂前的圣火护着你：受到的伤害降低，死去时东西不会掉，在故乡醒来。两个游戏日后，或到原质第 2 阶为止。", GOLD)])
    fn("holy", ["# 每秒（as 玩家）",
                "effect give @s minecraft:resistance 3 0 true",
                "scoreboard players operation #e %s = #gt %s" % (O, O), "scoreboard players operation #e %s -= @s rpg_tl_born" % O,
                "execute if score #e %s matches 48000.. run return run function %s/holy_end" % (O, L),
                "execute if score @s rpg_sef matches 2.. run function %s/holy_end" % L])
    badge = ('minecraft:paper[minecraft:custom_name=%s,minecraft:lore=[%s,%s,%s],minecraft:custom_data={rpg_badge:1b},minecraft:item_model="rpg:town/town_badge",minecraft:max_stack_size=1]'
             % (J(["", T("[城镇]", GOLD, True), T("镇民徽章", "#FFFFFF")]), J(T("+------------------+", "#FFFFFF")), J(T("你是这片大陆上一座城镇的人", "gray")), J(T("+------------------+", "#FFFFFF"))))
    pas = ('minecraft:paper[minecraft:custom_name=%s,minecraft:lore=[%s,%s,%s,%s],minecraft:custom_data={rpg_eden_pass:1b},minecraft:item_model="rpg:town/eden_pass",minecraft:max_stack_size=1]'
           % (J(["", T("[失乐园]", "#E0483C", True), T("失乐园通行符", "#FFFFFF")]), J(T("+------------------+", "#FFFFFF")), J(T("第一次进伊甸之门时生效", "gray")),
              J(T("二十分钟内受到的伤害降低", "gray")), J(T("+------------------+", "#FFFFFF"))))
    fn("holy_end", ["tag @s remove rpg.tl.holy", note("圣火庇护结束了。从今往后，路要自己走。")] + TT.say("PR21", "@s") + TT.say("PR22", "@s") + [
        "give @s " + badge, "give @s " + pas])
    # 死后还东西：死亡那一刻（下一刻）把脚边刚掉的物品收进 rpg:town keep.p<id>，复活后在身边放出来
    fn("died", ["scoreboard players set @s rpg_tl_dc 0",
                "execute unless entity @s[tag=rpg.tl.holy] run return 0",
                "execute store result storage rpg:town k.id int 1 run scoreboard players get @s rpg_fg_id",
                "execute as @e[type=minecraft:item,distance=..6] run function %s/keep with storage rpg:town k" % L,
                "tag @s add rpg.tl.kept"])
    fn("keep", ["$data modify storage rpg:town keep.p$(id) append from entity @s Item", "kill @s"])
    fn("regive", ["tag @s remove rpg.tl.kept",
                  "execute store result storage rpg:town k.id int 1 run scoreboard players get @s rpg_fg_id",
                  "scoreboard players set #n %s 0" % O,
                  "function %s/regive1 with storage rpg:town k" % L,
                  note("圣火替你收着的东西，都还给你了。", GOLD)])
    fn("regive1", ["$execute unless data storage rpg:town keep.p$(id)[0] run return 0",
                   'summon minecraft:item ~ ~0.5 ~ {Item:{id:"minecraft:stone",count:1},Tags:["rpg.tl.ri"],PickupDelay:0s}',
                   "$data modify entity @e[type=minecraft:item,tag=rpg.tl.ri,limit=1] Item set from storage rpg:town keep.p$(id)[0]",
                   "tag @e[type=minecraft:item,tag=rpg.tl.ri] remove rpg.tl.ri",
                   "$data remove storage rpg:town keep.p$(id)[0]",
                   "scoreboard players add #n %s 1" % O,
                   "$execute if score #n %s matches ..80 run function %s/regive1 {id:$(id)}" % (O, L)])


# ============================================================================ 镇上的人
def villager(role, name, gloss, prof, extra_tags=()):
    # 职业一律「无」：身体隐形、外观是城镇模型，职业只会让原版在重新载入后给他生成交易、右键弹交易面板（prof 参数保留不用）
    tags = ["rpg.tnpc", "rpg.tnpc." + role, "rpg.tl.new", "rpg.tl.notrade"] + list(extra_tags)
    return ("summon minecraft:villager ~ ~ ~ {Tags:%s,NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b,"
            "CustomNameVisible:0b,CustomName:%s,VillagerData:{type:\"minecraft:plains\",profession:\"minecraft:none\",level:1},Offers:{Recipes:[]}}"
            % (J(tags), J(T(ui.fraktur(gloss), "#404040")))) + "\n" + (
        "summon minecraft:text_display ~ ~ ~ {Tags:[\"rpg.tnpc.plate\",\"rpg.tl.pnew\"],billboard:\"center\",text:%s,"
        "transformation:{translation:[0f,0.62f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f]}}"
        % J(["", T(name, NAME, True), T("\n" + ui.fraktur(gloss), GLOSS)]))


def people():
    spawn = {
        "church": [("priest", "神父", "Father", "cleric", 0, 0)],
        "elder": [("elder", "村长", "Elder", "farmer", 0, 0)],
        "tavern": [("bard", "吟游诗人", "Bard", "nitwit", 0, 0)],
        "grave": [("watchman", "守夜人", "Watchman", "none", 0, -10)],
        "granary": [("folk", "农妇", "Farmwife", "farmer", 2, 1)],
        "plaza": [("folk", "少年", "Lad", "none", 5, 5)],
        "house": [("folk", "农夫", "Farmer", "farmer", 1, 1)],
    }
    out = ["# 一座镇建好了（#built = 镇号，执行位置任意）：在各个锚点放人"]
    for anchor, lst in spawn.items():
        if anchor == "house":
            out += ["execute as @e[type=minecraft:marker,tag=rpg.tw.at.house] if score @s %s_id = #built %s run tag @s add rpg.tl.pick" % (TW, TW),
                    "execute as @e[type=minecraft:marker,tag=rpg.tl.pick,limit=1,sort=random] at @s run function %s/ppl/house" % L,
                    "tag @e[type=minecraft:marker,tag=rpg.tl.pick] remove rpg.tl.pick"]
        else:
            out.append("execute as @e[type=minecraft:marker,tag=rpg.tw.at.%s] if score @s %s_id = #built %s at @s run function %s/ppl/%s" % (anchor, TW, TW, L, anchor))
        lines = []
        for role, name, gloss, prof, dx, dz in lst:
            lines += ["execute positioned ~%d ~ ~%d positioned over motion_blocking_no_leaves run function %s/ppl/one_%s_%s" % (dx, dz, L, role, gloss.lower())]
            fn("ppl/one_%s_%s" % (role, gloss.lower()), villager(role, name, gloss, prof, ["rpg.tnpc.%s" % gloss.lower()]).split("\n") + [
                "ride @e[type=minecraft:text_display,tag=rpg.tl.pnew,limit=1,sort=nearest] mount @e[type=minecraft:villager,tag=rpg.tl.new,limit=1,sort=nearest]",
                "tag @e[type=minecraft:text_display,tag=rpg.tl.pnew] remove rpg.tl.pnew",
                "scoreboard players operation @e[type=minecraft:villager,tag=rpg.tl.new] %s_id = #built %s" % (TW, TW),
                "execute as @e[type=minecraft:villager,tag=rpg.tl.new] %s" % ROT,        # 朝向四面八方
                "execute as @e[type=minecraft:villager,tag=rpg.tl.new] at @s run function #rpg:town_dress",
                "tag @e[type=minecraft:villager,tag=rpg.tl.new] remove rpg.tl.new"])
        fn("ppl/%s" % anchor, lines)
    # 没有酒馆的镇：吟游诗人站在天使像旁
    out.append("execute unless entity @e[type=minecraft:villager,tag=rpg.tnpc.bard,scores={%s_id=0}] as @e[type=minecraft:marker,tag=rpg.tw.at.plaza] if score @s %s_id = #built %s "
               "unless entity @e[type=minecraft:marker,tag=rpg.tw.at.tavern,distance=..400] at @s positioned ~-5 ~ ~5 run function %s/ppl/tavern" % (TW, TW, TW, L))
    # 铁匠（已有的铁匠商人）放在营火旁；告示板在天使像另一侧；两名站岗的圣卫
    out += ["execute as @e[type=minecraft:marker,tag=rpg.tw.at.bench] if score @s %s_id = #built %s at @s positioned ~-2 ~ ~1 run function rpg:merchant/spawn_smith" % (TW, TW),
            "execute as @e[type=minecraft:marker,tag=rpg.tw.at.bench] if score @s %s_id = #built %s at @s positioned ~-2 ~ ~1 as @e[type=minecraft:villager,tag=rpg.mer.smith,distance=..2] %s" % (TW, TW, ROT),
            "execute as @e[type=minecraft:marker,tag=rpg.tw.at.board] if score @s %s_id = #built %s at @s run function %s/ppl/board" % (TW, TW, L),
            "execute as @e[type=minecraft:marker,tag=rpg.tw.at.spawn] if score @s %s_id = #built %s at @s positioned ~9 ~ ~-1 run function %s/ppl/guard" % (TW, TW, L),
            "execute as @e[type=minecraft:marker,tag=rpg.tw.at.church] if score @s %s_id = #built %s at @s positioned ~-3 ~ ~1 run function %s/ppl/guard" % (TW, TW, L),
            "execute as @e[type=minecraft:marker,tag=rpg.tw.at.grave] if score @s %s_id = #built %s at @s run function %s/ppl/graves" % (TW, TW, L),
            "execute as @e[type=minecraft:marker,tag=rpg.tw.at.church] if score @s %s_id = #built %s at @s positioned ~2 ~ ~ run function rpg:town/prop {n:\"bell\"}" % (TW, TW)]
    graves = []
    for n, (dx, dz) in enumerate([(-6, -3), (-3, -3), (0, -3), (3, -3), (6, -3), (-6, 2), (-3, 2), (0, 2), (3, 2), (6, 2)]):
        graves.append("execute positioned ~%d 0 ~%d positioned over motion_blocking_no_leaves run function rpg:town/prop {n:\"grave_%s\"}" % (dx, dz, "ab"[n % 2]))
    fn("ppl/graves", graves)
    fn("ppl/board", ['summon minecraft:interaction ~ ~ ~ {Tags:["rpg.tnpc","rpg.tnpc.board","rpg.tl.new"],width:1.4f,height:2.2f,response:1b}',
                     "setblock ~ ~ ~ minecraft:lectern[facing=north]",
                     'summon minecraft:text_display ~ ~2.3 ~ {Tags:["rpg.tnpc.plate"],billboard:"center",text:%s}' % J(["", T("告示板", NAME, True), T("\n" + ui.fraktur("Notice Board"), GLOSS)]),
                     "scoreboard players operation @e[type=minecraft:interaction,tag=rpg.tl.new] %s_id = #built %s" % (TW, TW),
                     "tag @e[tag=rpg.tl.new] remove rpg.tl.new"])
    fn("ppl/guard", ["execute positioned over motion_blocking_no_leaves run function rpg:tower_guard/summon",
                     "execute as @e[type=minecraft:vindicator,tag=rpg.tg,tag=!rpg.tw.guard,distance=..1,limit=1] run function %s/ppl/guard_post" % L])
    fn("ppl/guard_post", ["data merge entity @s {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b}", "execute " + ROT, "tag @s add rpg.tw.guard", "tag @s add rpg.ally",
                          "scoreboard players operation @s %s_id = #built %s" % (TW, TW)])
    # 站岗的圣卫（镇上的、孤堡的）：圣卫的出招逻辑不看 NoAI，谁走近就打，打完还会把 NoAI 关掉。
    # 镇上的只对通缉中的恶魔信徒（rpg.dm.wanted）出手，孤堡的醒了（rpg.lm.awake）才出手；其余时候一动不动。
    fn("guard_ai", ["# 站岗的圣卫每刻（as/at 它）",
                    "execute if entity @s[tag=rpg.tw.guard] if entity @a[tag=rpg.dm.wanted,distance=..16,gamemode=!spectator] run tag @s add rpg.tw.fight",
                    "execute if entity @s[tag=rpg.lm.awake] run tag @s add rpg.tw.fight",
                    "execute if entity @s[tag=rpg.tw.guard,tag=rpg.tw.fight] unless score @s rpg_tg_st matches 1.. unless entity @a[tag=rpg.dm.wanted,distance=..24] run function %s/guard_calm" % L,
                    "execute if entity @s[tag=!rpg.tw.fight,nbt={NoAI:0b}] run data merge entity @s {NoAI:1b}"])
    fn("guard_calm", ["tag @s remove rpg.tw.fight", "data merge entity @s {NoAI:1b}"])
    for ai in ("tower_guard", "royal_guard"):
        q = os.path.join(FUNC, ai, "ai", "tick.mcfunction")
        if os.path.exists(q):
            s = io.open(q, encoding="utf-8").read()
            if L + "/guard_ai" not in s:
                head = ["execute if entity @s[tag=rpg.tw.guard] run function %s/guard_ai" % L,
                        "execute if entity @s[tag=rpg.lm.guard] run function %s/guard_ai" % L,
                        "execute if entity @s[tag=rpg.tw.guard,tag=!rpg.tw.fight] run return 0",
                        "execute if entity @s[tag=rpg.lm.guard,tag=!rpg.tw.fight] run return 0"]
                io.open(q, "w", encoding="utf-8", newline="\n").write("\n".join(head) + "\n" + s)
    fn("spawn_people", out)
    folk = [("farmwife", "granary"), ("farmer", "house"), ("lad", "plaza")]
    fn("folk_check", ["# 每 30 秒：附近有玩家的镇，农妇、农夫、少年缺谁补谁（as/at 镇中心标记）",
                      "scoreboard players operation #built %s = @s %s_id" % (TW, TW)] + [
        "execute unless entity @e[type=minecraft:villager,tag=rpg.tnpc.%s,distance=..200] run function %s/folk_add_%s" % (who, L, who) for who, _a in folk])
    for who, anchor in folk:
        if anchor == "house":
            body = ["execute as @e[type=minecraft:marker,tag=rpg.tw.at.house,distance=..200] if score @s %s_id = #built %s run tag @s add rpg.tl.pick" % (TW, TW),
                    "execute as @e[type=minecraft:marker,tag=rpg.tl.pick,limit=1,sort=random] at @s run function %s/ppl/house" % L,
                    "tag @e[type=minecraft:marker,tag=rpg.tl.pick] remove rpg.tl.pick"]
        else:
            body = ["execute as @e[type=minecraft:marker,tag=rpg.tw.at.%s,distance=..200] if score @s %s_id = #built %s at @s run function %s/ppl/%s" % (anchor, TW, TW, L, anchor)]
        fn("folk_add_%s" % who, body)
    tag_values("town_built", [L + "/spawn_people"])
    tag_values("town_dress", [])
    tag_values("town_arrive", [L + "/arrive"])
    fn("arrive", ["# 第一次到故乡（as 玩家）：圣火庇护开始，提示去找神父",
                  "execute if score @s rpg_tl_gift matches 1.. run return 0",
                  "execute unless entity @s[tag=rpg.tl.holy] unless score @s rpg_tl_born matches 1.. run function %s/holy_start" % L,
                  note("去教堂门口找神父报到，他那里有给新人的东西。", NAME)])
    # 对话入口
    wj("rpg/advancement/town/talk.json", {"criteria": {"t": {"trigger": "minecraft:player_interacted_with_entity", "conditions": {
        "entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": "{Tags:[\"rpg.tnpc\"]}"}}]}}},
        "rewards": {"function": L + "/talk"}})
    who = ["# 说话的是谁（as 那位）"]
    for v, r in ROLE.items():
        who.append("execute if entity @s[tag=rpg.tnpc.%s] run scoreboard players set #role %s %d" % (r, O, v))
    who += ["scoreboard players operation #t %s = @s %s_id" % (O, TW),
            "execute if entity @s[tag=rpg.tnpc.farmwife] run scoreboard players set #folk %s 1" % O,
            "execute if entity @s[tag=rpg.tnpc.farmer] run scoreboard players set #folk %s 2" % O,
            "execute if entity @s[tag=rpg.tnpc.lad] run scoreboard players set #folk %s 3" % O,
            "execute if entity @s[type=minecraft:villager] run rotate @s facing entity @p[distance=..8]"]
    fn("whoami", who)
    talk = ["# 右键了镇上的人或告示板（as/at 玩家）",
            "advancement revoke @s only rpg:town/talk",
            "scoreboard players set #role %s 0" % O, "scoreboard players set #folk %s 0" % O,
            "execute as @e[tag=rpg.tnpc,distance=..8,limit=1,sort=nearest] run function %s/whoami" % L,
            "execute if score #role %s matches 0 run return 0" % O,
            "scoreboard players operation @s rpg_tl_t = #t %s" % O,
            "scoreboard players enable @s %s" % DO]
    for v, r in ROLE.items():
        talk.append("execute if score #role %s matches %d run return run function %s/d/%s" % (O, v, L, r))
    fn("talk", talk)


# ============================================================================ 对话框
def dialogs():
    fn("d/priest", [dlg("神父", "Father", [T("「孩子，有什么事？」", NAME),
                                             card("rpg:town/welfare_pack", "报到", ["新人的一份：口粮、精血药水、驱魔圣水、器胚、残魂、铁锭、两卷余烬归途"], GOLD),
                                             card("rpg:town/ration", "每日口粮", ["每个现实日一次；原质第 3 阶以前多给器胚与残魂"], GOLD),
                                             card("rpg:town/holy_fire", "圣火庇护", ["第一次到故乡起两个游戏日，或到原质第 2 阶为止"], GOLD),
                                             card("rpg:town/home_scroll", "余烬归途", ["站着念 5 秒回故乡；两枚货币一卷"], GOLD),
                                             card("rpg:town/ev_granary", "驱魔委托", ["今晚的副本、神父的圣水、失踪的孩子"], GOLD)],
                                     [("报到", GOLD, 1), ("每日口粮", GOLD, 2), ("驱魔委托", GOLD, 3), ("神父的圣水", NAME, 4), ("失踪的孩子", NAME, 5), ("余烬归途", GOLD, 6)])])
    fn("d/elder", [dlg("村长", "Elder", [T("「镇子不大，但它是你的。」", NAME),
                                         card("rpg:town/town_badge", "声望", ["20 口粮加一份 · 40 租屋 · 70 镇上的图纸 · 100 守护者"], GOLD),
                                         card("rpg:town/letter", "寄往邻镇的信", ["把信交给另一座镇的村长"], NAME),
                                         card("rpg:town/wanted", "收税官 · 发黑的麦子", ["替教廷收税还是替村民藏粮；粮仓里的异味"], NAME)],
                       [("声望", GOLD, 11), ("租屋", GOLD, 12), ("寄往邻镇的信", NAME, 13), ("收税官", NAME, 14), ("发黑的麦子", NAME, 15), ("每日口粮", GOLD, 2)])])
    fn("d/bard", [dlg("吟游诗人", "Bard", [T("「想听歌？歌是碎的，得去各处拣。」\n", NAME), T("天使像、墓地、林中营地各有一段。也可以来比一比准头。", BODY)],
                      [("三首歌", GOLD, 21), ("酒馆赌约", NAME, 22)])])
    fn("d/watchman", [dlg("守夜人", "Watchman", [T("「夜里替我绕镇走一圈。」\n", NAME), T("墓地、刑台广场、教堂门口、营火，四处都走到。", BODY)],
                          [("守夜", GOLD, 31)], 1)])
    fn("d/board", ["function rpg:town/ev/board_text",
                   "function %s/d/board_m with storage rpg:town ev" % L])
    fn("d/board_m", ["$" + dlg("告示板", "Notice Board", [card("$(icon)", "今晚：$(name)", ["$(hint)"], GOLD),
                                                       card("rpg:town/tab_fuse", "铁匠的学徒", ["在营火工作台熔铸或拆解一件武器"], NAME),
                                                       card("rpg:town/wanted", "通缉令", ["在圣卫面前暴露的恶魔信徒；打倒他们领教廷的赏"], ui.RITUAL),
                                                       card("rpg:town/map_shard", "委托一览", ["神父、村长、吟游诗人、守夜人各有委托，每个现实日都能再做"], NAME)],
                               [("现在就开始", ui.WARN, 41), ("铁匠的学徒", NAME, 42), ("委托一览", NAME, 43), ("通缉令", ui.RITUAL, 44)])])
    folk = ["# 镇民：今天的风声（rpg:town/ev 按今晚的副本挑一句）",
            "function rpg:town/ev/rumor_one"]
    fn("d/folk", folk)
    fn("d/child", ["function %s/q/child_talk" % L])
    # 按钮
    do = ["# 对话框按钮（as/at 玩家）",
          "scoreboard players operation #do %s = @s %s" % (O, DO), "scoreboard players set @s %s 0" % DO, "scoreboard players enable @s %s" % DO,
          "scoreboard players operation #t %s = @s rpg_tl_t" % O]
    route = {1: "gift", 2: "ration", 6: "buy_scroll", 3: "rpg:town/ev/priest_info", 4: "q/holy", 5: "q/child", 11: "rep", 12: "rent", 13: "q/letter", 14: "q/tax",
             15: "q/wheat", 21: "q/bard", 22: "q/bet", 31: "q/watch", 41: "rpg:town/ev/start_now", 42: "q/smith", 43: "q/list", 44: "rpg:town/demon/wanted_list",
             141: "q/tax_church", 142: "q/tax_folk"}
    for v, f in route.items():
        do.append("execute if score #do %s matches %d run return run function %s" % (O, v, f if ":" in f else L + "/" + f))
    fn("do", do)


# ============================================================================ 福利
def welfare():
    give = lambda tbl, n=1: ["loot give @s loot %s" % tbl] * n
    fn("gift", ["# 报到：新手大礼包（一辈子一次）",
                "execute if score @s rpg_tl_gift matches 1.. run return run " + note("新人的那份你已经领过了。每天来领口粮吧。"),
                "scoreboard players set @s rpg_tl_gift 1"] + TT.say("PR01", "@s") + TT.say("PR02", "@s") + [
                "give @s %s 16" % BREAD, "give @s %s 8" % MEAT] + give("rpg:potion/blood", 2) + [
                "function rpg:alc/give/holy"] + give("rpg:forge/item/blank", 2) + give("rpg:forge/item/soul", 4) + [
                "loot give @s loot rpg:forge/item/forge_stone", "give @s " + SCROLL + " 2",
                "execute unless entity @s[tag=rpg.tl.holy] unless score @s rpg_tl_born matches 1.. run function %s/holy_start" % L] + TT.say("PR03", "@s") + [
                "execute store result score #r %s run scoreboard players get @s rpg_tl_t" % O,
                "scoreboard players operation @s rpg_tl_d = #day1 %s" % O,
                "function %s/rep_add {n:5}" % L,
                "playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6 1.2"])
    fn("ration", ["# 每日口粮：每个现实日一次；原质第 3 阶以前多给一份材料；声望 20 再加一份",
                  "execute if score @s rpg_tl_d = #day1 %s run return run function %s/ration_no" % (O, L),
                  "scoreboard players operation @s rpg_tl_d = #day1 %s" % O] + TT.say("PR05", "@s") + [
                  "give @s %s 8" % BREAD] + give("rpg:potion/blood") + [
                  "execute unless score @s rpg_sef matches 3.. run loot give @s loot rpg:forge/item/soul",
                  "execute unless score @s rpg_sef matches 3.. run loot give @s loot rpg:forge/item/blank",
                  "function %s/rep_get" % L,
                  "execute if score #rep %s matches 20.. run give @s %s 6" % (O, MEAT),
                  "playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.8 1"])
    fn("ration_no", TT.say("PR06", "@s"))
    # 声望（宏：#t 镇号）
    getl = ["# #rep ← 玩家在 #t 这座镇的声望"]
    addl = ["# 玩家在 #t 这座镇的声望 + $(n)（可以是负数：players add 不收负数，先放进 #rn）", "$scoreboard players set #rn %s $(n)" % O]
    for i in N:
        getl.append("execute if score #t %s matches %d run scoreboard players operation #rep %s = @s %s" % (O, i, O, rep_obj(i)))
        addl.append("execute if score #t %s matches %d run scoreboard players operation @s %s += #rn %s" % (O, i, rep_obj(i), O))
    fn("rep_get", ["scoreboard players set #rep %s 0" % O] + getl)
    fn("rep_add", addl + ["function %s/rep_get" % L, "function %s/rep_tier" % L])
    fn("rep_tier", ["# 到档的奖励（每档一次）",
                    "execute if score #rep %s matches 70.. unless entity @s[tag=rpg.tl.bp] run function %s/rep_bp" % (O, L),
                    "execute if score #rep %s matches 100.. unless entity @s[tag=rpg.tl.guardian] run function %s/rep_guard" % (O, L)])
    fn("rep_bp", ["tag @s add rpg.tl.bp"] + TT.say("EL05", "@s") + ["loot give @s loot rpg:world/bp_epic_any"])
    fn("rep_guard", ["tag @s add rpg.tl.guardian"] + TT.say("EL06", "@s") + ["function rpg:quest/title/get_guardian"])
    fn("rep", ["function %s/rep_get" % L, "function %s/rep_show with storage rpg:town r" % L])
    rs = ["execute store result storage rpg:town r.v int 1 run scoreboard players get #rep %s" % O]
    fn("rep_show_pre", rs)
    fn("rep", ["function %s/rep_get" % L] + rs + ["function %s/rep_show with storage rpg:town r" % L] + TT.say("EL03", "@s")[:0])
    fn("rep_show", ["$tellraw @s " + J(["", T("〖声望〗", GOLD, True), T(ui.GAP + "你在这座镇的声望：", BODY), T("$(v)", NAME, True),
                                        T("　（20 口粮加份 · 40 租屋 · 70 镇上的图纸 · 100 守护者）", ui.MUTED)])])
    fn("rent", ["# 租屋：声望 40 + 20 货币；复活点挪到租屋门口",
                "function %s/rep_get" % L,
                "execute if score #rep %s matches ..39 run return run " % O + note("声望到 40，村长才肯把屋子租给你。", ui.WARN),
                "execute store result score #m %s run clear @s %s 0" % (O, CUR),
                "execute if score #m %s matches ..19 run return run " % O + note("租金是 20 枚货币。", ui.WARN),
                "clear @s %s 20" % CUR] + TT.say("EL04", "@s") + [
                "execute as @e[type=minecraft:marker,tag=rpg.tw.at.rent] if score @s %s_id = #t %s at @s run spawnpoint @p[tag=rpg.tl.me] ~ ~ ~" % (TW, O),
                note("复活点挪到了你的屋子门口。", GOLD)])
    # 「me」标签：给 rent 用
    s = open(os.path.join(FUNC, "town", "life", "rent.mcfunction"), encoding="utf-8").read().split("\n")


# ============================================================================ 支线
def quests():
    q = lambda k: "rpg_tl_q%d" % k
    qd = lambda k: "rpg_tl_qd%d" % k
    done_today = lambda k: "execute if score @s %s = #day1 %s run return run " % (qd(k), O) + note("这件事今天已经做过了，明天再来。")
    finish = lambda k, rep=10: ["scoreboard players set @s %s 0" % q(k), "scoreboard players operation @s %s = #day1 %s" % (qd(k), O),
                                "function %s/rep_add {n:%d}" % (L, rep),
                                "tellraw @s " + J(["", T("〖委托完成〗", GOLD, True), T(ui.GAP + QUESTS[k][0], NAME, True)]),
                                "playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.3",
                                "function rpg:events/bt/town_quest"]
    accept = lambda k: ["scoreboard players set @s %s 1" % q(k), "tellraw @s " + J(["", T("〖委托〗", GOLD, True), T(ui.GAP + QUESTS[k][0], NAME, True),
                                                                                    T("　" + QUESTS[k][2], BODY)])]
    # 1 铁匠的学徒：熔铸 / 拆解（add_fusion 给 rpg_tl_fu 加分）
    fn("q/smith", [done_today(1),
                   "execute if score @s rpg_tl_q1 matches 1 if score @s rpg_tl_fu matches 1.. run return run function %s/q/smith_done" % L,
                   "execute if score @s rpg_tl_q1 matches 1 run return run " + note("还没熔过、拆过武器呢。营火工作台的「熔铸」「拆解」两页。"),
                   "scoreboard players set @s rpg_tl_fu 0"] + accept(1))
    fn("q/smith_done", finish(1) + ["loot give @s loot rpg:forge/item/blank", "loot give @s loot rpg:forge/item/forge_stone", "loot give @s loot rpg:forge/item/soul"])
    # 2 神父的圣水
    fn("q/holy", [done_today(2),
                  "execute if score @s rpg_tl_q2 matches 0 run return run function %s/q/holy_take" % L,
                  "execute store result score #a %s run clear @s minecraft:potion[minecraft:potion_contents={potion:\"minecraft:water\"}] 0" % O,
                  "execute store result score #b %s run clear @s minecraft:sugar 0" % O,
                  "execute store result score #c %s run clear @s minecraft:charcoal 0" % O,
                  "execute if score #a %s matches 1.. if score #b %s matches 2.. if score #c %s matches 1.. run return run function %s/q/holy_done" % (O, O, O, L),
                  note("要一瓶水、两份糖（当海盐）、一块木炭（圣火的灰）。")])
    fn("q/holy_take", TT.say("PR08", "@s") + accept(2))
    fn("q/holy_done", ["clear @s minecraft:potion[minecraft:potion_contents={potion:\"minecraft:water\"}] 1", "clear @s minecraft:sugar 2", "clear @s minecraft:charcoal 1"]
       + TT.say("PR20", "@s") + ["function rpg:alc/give/holy", "function rpg:alc/give/holy"] + finish(2))
    # 3 守夜人：夜里走到四处（位标记 1 墓地 2 广场 4 教堂 8 营火）
    fn("q/watch", [done_today(3),
                   "execute if score @s rpg_tl_q3 matches 16 run return run function %s/q/watch_done" % L,
                   "execute if score @s rpg_tl_q3 matches 1.. run return run " + note("四处还没走完：墓地、刑台广场、教堂门口、营火。"),
                   "scoreboard players set @s rpg_tl_wt 0"] + TT.say("WT01", "@s") + TT.say("WT02", "@s") + accept(3))
    wt = ["# 每秒（as/at 接了守夜的玩家）：只在夜里算",
          "execute store result score #tod %s run time query daytime" % O,
          "execute unless score #tod %s matches 13000..23000 run return 0" % O]
    for bit, anchor in ((1, "grave"), (2, "plaza"), (4, "church"), (8, "bench")):
        wt.append("execute if entity @e[type=minecraft:marker,tag=rpg.tw.at.%s,distance=..6] run function %s/q/watch_bit {b:%d}" % (anchor, L, bit))
    fn("q/watch_tick", wt)
    fn("q/watch_bit", ["$scoreboard players set #b %s $(b)" % O,
                       "scoreboard players operation #x %s = @s rpg_tl_wt" % O, "scoreboard players operation #x %s /= #b %s" % (O, O),
                       "scoreboard players operation #x %s %%= #2 rpg_tw" % O,
                       "execute if score #x %s matches 1 run return 0" % O,
                       "scoreboard players operation @s rpg_tl_wt += #b %s" % O,
                       "title @s actionbar " + J(["", T("守夜：这一处看过了", BODY)]),
                       "execute if score @s rpg_tl_wt matches 1 run function %s/q/watch_grave" % L,
                       "execute if score @s rpg_tl_wt matches 15 run scoreboard players set @s rpg_tl_q3 16",
                       "execute if score @s rpg_tl_wt matches 15 run " + note("四处都走过了，回去找守夜人。", GOLD)])
    fn("q/watch_grave", TT.say("WT03", "@s"))
    fn("q/watch_done", TT.say("WT04", "@s") + ["loot give @s loot rpg:world/currency", "loot give @s loot rpg:world/currency"] + finish(3))
    # 4 发黑的麦子：在粮仓里待满 5 秒
    fn("q/wheat", [done_today(4),
                   "execute if score @s rpg_tl_q4 matches 6.. run return run function %s/q/wheat_done" % L,
                   "execute if score @s rpg_tl_q4 matches 1.. run return run " + note("去粮仓里面看看，待一会儿。")] + TT.say("RB01", "@s", "村长") + accept(4))
    fn("q/wheat_tick", ["execute if entity @e[type=minecraft:marker,tag=rpg.tw.in.granary,distance=..12] run scoreboard players add #wq %s 1" % O,
                        "execute if entity @e[type=minecraft:marker,tag=rpg.tw.in.granary,distance=..12] run function %s/q/wheat_step" % L])
    fn("q/wheat_step", ["particle minecraft:dust{color:[0.35,0.42,0.12],scale:1.2} ~ ~1 ~ 2 1 2 0 20",
                        "playsound minecraft:entity.bee.loop hostile @s ~ ~ ~ 0.4 0.6",
                        "scoreboard players add @s rpg_tl_q4 1",
                        "execute if score @s rpg_tl_q4 matches 6 run " + note("麦袋从里面烂了，地上爬着一串苍蝇……回去告诉村长。", GOLD)])
    fn("q/wheat_done", TT.say("RB02", "@s", "村长") + ["give @s %s 12" % BREAD, "loot give @s loot rpg:forge/item/soul", "loot give @s loot rpg:forge/item/soul"] + finish(4))
    # 5 失踪的孩子：孩子在林中营地
    fn("q/child", [done_today(5),
                   "execute if score @s rpg_tl_q5 matches 2 run return run function %s/q/child_done" % L,
                   "execute if score @s rpg_tl_q5 matches 1 run return run " + note("孩子在镇外的林子里。往没有路的地方找。"),
                   "execute as @e[type=minecraft:marker,tag=rpg.tw.at.camp] if score @s %s_id = #t %s at @s unless entity @e[type=minecraft:villager,tag=rpg.tnpc.child,distance=..12] positioned ~3 ~ ~3 run function %s/q/child_spawn" % (TW, O, L)]
       + accept(5))
    fn("q/child_spawn", ["summon minecraft:villager ~ ~ ~ {Tags:[\"rpg.tnpc\",\"rpg.tnpc.child\"],Age:-2147483648,NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,CustomName:%s}" % J(T(ui.fraktur("Child"), "#404040")),
                         "scoreboard players operation @e[type=minecraft:villager,tag=rpg.tnpc.child,distance=..1] %s_id = #t %s" % (TW, O)])
    fn("q/child_talk", ["execute unless score @s rpg_tl_q5 matches 1 run return run " + "\n".join(TT.say("CH01", "@s"))] + TT.say("CH01", "@s") + TT.say("CH02", "@s") + TT.say("CH03", "@s") + [
        "scoreboard players set @s rpg_tl_q5 2", "tag @s add rpg.tl.camp",
        "execute as @e[type=minecraft:villager,tag=rpg.tnpc.child,distance=..8,limit=1,sort=nearest] at @s run function %s/q/child_gone" % L,
        note("孩子说他认得回家的路，先跑回去了。你记下了营地的位置。", GOLD)])
    fn("q/child_gone", ["particle minecraft:cloud ~ ~0.5 ~ 0.3 0.4 0.3 0.02 12", "tp @s ~ -400 ~"])
    fn("q/child_done", TT.say("CH04", "@s", "孩子") + finish(5, 15))
    # 6 吟游诗人：三段歌（位 1 天使像 2 墓地 4 营地）
    fn("q/bard", [done_today(6),
                  "execute if score @s rpg_tl_q6 matches 8 run return run function %s/q/bard_done" % L,
                  "execute if score @s rpg_tl_q6 matches 1.. run return run " + note("还没听全：天使像、墓地、林中营地。"),
                  "scoreboard players set @s rpg_tl_bd 0"] + accept(6))
    bt = ["# 每秒（as/at 接了三首歌的玩家）"]
    for bit, anchor, line in ((1, "spawn", "BD01"), (2, "grave", "BD02"), (4, "camp", "BD03")):
        bt.append("execute if entity @e[type=minecraft:marker,tag=rpg.tw.at.%s,distance=..8] run function %s/q/bard_bit_%d" % (anchor, L, bit))
        fn("q/bard_bit_%d" % bit, ["scoreboard players set #b %s %d" % (O, bit),
                                   "scoreboard players operation #x %s = @s rpg_tl_bd" % O, "scoreboard players operation #x %s /= #b %s" % (O, O),
                                   "scoreboard players operation #x %s %%= #2 rpg_tw" % O,
                                   "execute if score #x %s matches 1 run return 0" % O,
                                   "scoreboard players add @s rpg_tl_bd %d" % bit] + TT.say(line, "@s") + [
                                   "execute if score @s rpg_tl_bd matches 7 run scoreboard players set @s rpg_tl_q6 8",
                                   "execute if score @s rpg_tl_bd matches 7 run " + note("三段都听到了，回去唱给吟游诗人听。", GOLD)])
    fn("q/bard_tick", bt)
    fn("q/bard_done", finish(6, 10) + ["function rpg:quest/title/get_bard"])
    # 7 寄往邻镇的信
    letter = ('minecraft:paper[minecraft:custom_name=%s,minecraft:lore=[%s,%s,%s,%s],minecraft:custom_data={rpg_letter:1b,rpg_from:$(t)},minecraft:item_model="rpg:town/letter",minecraft:max_stack_size=1]'
              % (J(["", T("[城镇]", GOLD, True), T("寄往邻镇的信", "#FFFFFF")]), J(T("+------------------+", "#FFFFFF")), J(T("村长托你送的信，封口有蜡印", "gray")),
                 J(T("交给另一座镇的村长", "gray")), J(T("+------------------+", "#FFFFFF"))))
    fn("q/letter", ["execute if items entity @s container.* minecraft:paper[minecraft:custom_data~{rpg_letter:1b}] run return run function %s/q/letter_hand" % L,
                    done_today(7)] + TT.say("EL09", "@s") + [
                    "execute store result storage rpg:town q.t int 1 run scoreboard players get #t %s" % O,
                    "function %s/q/letter_give with storage rpg:town q" % L] + accept(7))
    fn("q/letter_give", ["$give @s " + letter])
    fn("q/letter_hand", ["# 手里有信：是别的镇来的才算送到",
                         ] + ["execute if score #t %s matches %d if items entity @s container.* minecraft:paper[minecraft:custom_data~{rpg_letter:1b,rpg_from:%d}] run return run " % (O, i, i) + note("信要送到另一座镇，交给那里的村长。") for i in N] + [
                         "clear @s minecraft:paper[minecraft:custom_data~{rpg_letter:1b}] 1",
                         "loot give @s loot rpg:world/currency", "loot give @s loot rpg:world/currency", "loot give @s loot rpg:world/currency",
                         "loot give @s loot rpg:world/bp_fragment"] + finish(7, 10))
    # 8 收税官
    fn("q/tax", [done_today(8)] + TT.say("EL10", "@s") + [
        dlg("收税官", "Tithe", [T("教廷的收税官又来了。镇上今年的麦子不多。", BODY)], [("替教廷收", ui.BROADCAST_HOLY, 141), ("替村民藏粮", ui.RITUAL, 142)])])
    fn("q/tax_church", ["execute if score @s rpg_tl_qd8 = #day1 %s run return 0" % O, "scoreboard players add @s rpg_tl_ch 10",
                        "loot give @s loot rpg:world/currency", "loot give @s loot rpg:world/currency", "loot give @s loot rpg:world/currency",
                        "function %s/rep_add {n:-5}" % L, note("教廷记下了你的名字。镇上有人不再跟你打招呼。", ui.BROADCAST_HOLY)] + finish(8, 0))
    fn("q/tax_folk", ["execute if score @s rpg_tl_qd8 = #day1 %s run return 0" % O, "scoreboard players remove @s rpg_tl_ch 10",
                      note("麦子藏进了地窖。镇上的人记住了你。", ui.RITUAL)] + finish(8, 15))
    # 9 酒馆赌约：30 秒内打中 5 个靶子（交互实体，左键）
    fn("q/bet", [done_today(9),
                 "execute if score @s rpg_tl_q9 matches 1 run return run " + note("靶子还立着，快打！"),
                 "scoreboard players set @s rpg_tl_hit 0", "scoreboard players set @s rpg_tl_q9 1",
                 "tag @s add rpg.tl.bet"] + ["execute positioned ^%d ^ ^%d positioned over motion_blocking_no_leaves run function %s/q/target" % (dx, dz, L)
                                            for dx, dz in ((-4, 6), (-2, 8), (0, 10), (2, 8), (4, 6))] + [
                 note("三十秒，五个靶子。左键打中它们。", GOLD)])
    fn("q/target", ['summon minecraft:interaction ~ ~ ~ {Tags:["rpg.tl.target"],width:0.8f,height:1.6f}',
                    'summon minecraft:block_display ~-0.3 ~ ~-0.3 {Tags:["rpg.tl.tdisp"],block_state:{Name:"minecraft:target"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.6f,1.4f,0.6f]}}',
                    "scoreboard players set @e[type=minecraft:interaction,tag=rpg.tl.target,distance=..0.5] %s 30" % O])
    fn("q/target_age", ["scoreboard players remove @s %s 1" % O, "execute if score @s %s matches ..0 at @s run function %s/q/target_die" % (O, L)])
    fn("q/target_die", ["kill @e[type=minecraft:block_display,tag=rpg.tl.tdisp,distance=..1]", "kill @s",
                        "execute unless entity @e[type=minecraft:interaction,tag=rpg.tl.target] as @a[tag=rpg.tl.bet] run function %s/q/bet_end" % L])
    fn("q/target_hit", ["execute at @s run particle minecraft:crit ~ ~1 ~ 0.2 0.4 0.2 0.2 12",
                        "execute at @s run playsound minecraft:block.note_block.bell player @a[distance=..12] ~ ~ ~ 1 1.6",
                        "execute at @s run scoreboard players add @p[tag=rpg.tl.bet] rpg_tl_hit 1",
                        "execute at @s run function %s/q/target_die" % L])
    fn("q/bet_end", ["tag @s remove rpg.tl.bet",
                     "execute if score @s rpg_tl_hit matches 5.. run return run function %s/q/bet_win" % L,
                     "scoreboard players set @s rpg_tl_q9 0", note("没打全。明天再来比。", ui.WARN), "scoreboard players operation @s rpg_tl_qd9 = #day1 %s" % O])
    fn("q/bet_win", ["loot give @s loot rpg:forge/rune_any"] + TT.say("TH03", "@s", "围观的少年") + finish(9, 8))
    # 一览
    lst = ["tellraw @s " + J(["", T("〖委托一览〗", GOLD, True), T(ui.GAP + "每个现实日每条都能再做一次", ui.MUTED)])]
    for k, (name, who, what) in QUESTS.items():
        lst.append("tellraw @s " + J(["", T("  " + name, NAME, True), T("　" + who + "　", GOLD), T(what, BODY)]))
    fn("q/list", lst)


def rent_me():
    p = os.path.join(FUNC, "town", "life", "rent.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    s = s.replace("clear @s %s 20\n" % CUR, "clear @s %s 20\ntag @s add rpg.tl.me\n" % CUR).rstrip("\n") + "\ntag @s remove rpg.tl.me\n"
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def titles_patch():
    """称号：add_quests 里加「守护者」「三首歌的听者」（图标由 Codex 画，放 world_ref/art/title_*.png）。"""
    for k, (name, why) in {"guardian": ("城镇的守护者", "一座城镇的声望到了 100"), "bard": ("三首歌的听者", "替吟游诗人拣齐了三首歌")}.items():
        p = os.path.join(FUNC, "quest", "title", "get_%s.mcfunction" % k)
        assert os.path.exists(p), "称号 %s 要先在 add_quests.TITLES 里登记" % k


def main():
    core()
    holy()
    people()
    dialogs()
    welfare()
    scroll()
    rent_me()
    quests()
    titles_patch()
    n = TT.install_vo(os.path.join(os.path.dirname(DP), "resourcepack"))
    print("town life: %d 个函数，配音 %d 句" % (COUNT[0], n))


if __name__ == "__main__":
    main()
