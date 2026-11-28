# -*- coding: utf-8 -*-
"""随机事件、每日悬赏与面板「旅程」页（策划书第五步，用户 2026-11-23/24）。

    python add_events.py ../rpg

事件（每 10 分钟掷一次，全服同时最多一个；只在主世界、只挑走完新手的玩家）：
  1 罪潮之夜  夜里、原质 ≥ 3：10 分钟内精英出现率 ×3、杀怪残魂再掷一次；其间打倒 3 名首领 → 源质「基础」。
  2 坠星      原质 ≥ 4：附近砸下陨星，3 名精英守着；守卫都倒下 → 星辰残片与钻石；守卫 10% → 源质「光辉」。
  3 罪仆巡逻  原质 ≥ 5：某一柱 3 名罪仆游荡；全倒下 → 该柱罪印碎片 ×2、25% 未立约契约书。
  4 寻宝者    任意：背着钱袋的兔子 30 秒内逃走；打死 → 货币、原料一袋、30% 图纸碎片。
  5 空缺者显现 附近村子里有空缺者：让它显形 60 秒、报坐标。
  （迷途商人随商人一起在最后一步做；受伤的圣卫要先把圣卫做成友方，见策划书。）
播报沿用驱魔裁决的格式：〖事件・名〗+ 花体英文 + 灰色正文。
悬赏：每天（游戏日）3 条，打怪类按组记、精英按击杀记、上交类在领取时清点；完成给货币、精英徽记、阅历；
  三条都领了再给铸造之石；累计 21 条 → 源质「王国」。
旅程页：主面板「旅程」按钮 → rpg:panel/ui/show（与原质页同一个渲染）；当前事件、悬赏（可领取）、配方书。
"""
import io
import json
import os
import sys

import rpg_ui_style as ui
import world_loot_spec as W
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
LOOT = os.path.join(DP, "data", "rpg", "loot_table")
P = "rpg:events"
O = "rpg_ev"
COUNT = 0
HERE = os.path.dirname(os.path.abspath(__file__))

EVENTS = {  # id: (名, 英文, 颜色, 持续刻)
    1: ("罪潮之夜", "Tide of Sin", ui.mix(ui.BROADCAST_VOID, ui.WARN, 0.4), 12000),
    2: ("坠星", "Falling Star", ui.HOLY_LIGHT, 6000),
    3: ("罪仆巡逻", "Goetic Patrol", ui.BROADCAST_VOID, 9600),
    4: ("寻宝者", "Treasure Rabbit", ui.HOLY, 600),
    5: ("空缺者显现", "The Vacant", ui.CYAN, 1200),
}
# 悬赏：id → (文字, 种类, 目标, 键)
BOUNTIES = {
    1: ("击杀亡灵", "kill", 20, "undead"), 2: ("击杀节肢怪物", "kill", 15, "arthropod"),
    3: ("击杀咒术师", "kill", 8, "arcane"), 4: ("击杀下界怪物", "kill", 15, "nether"),
    5: ("击败精英", "elite", 2, None),
    6: ("上交铁锭", "give", 16, "minecraft:iron_ingot[!minecraft:custom_data]"),
    7: ("上交金锭", "give", 6, "minecraft:gold_ingot[!minecraft:custom_data]"),
    8: ("上交骸骨", "give", 24, "minecraft:bone"),
    9: ("上交蛛丝", "give", 24, "minecraft:string"),
    10: ("上交火药", "give", 12, "minecraft:gunpowder"),
    11: ("上交烈焰粉", "give", 10, "minecraft:blaze_powder"),
    12: ("上交末影珍珠", "give", 4, "minecraft:ender_pearl"),
    13: ("通过试炼的层数", "trial", 5, None),
    14: ("在失乐园打倒怪物", "paradise", 30, None),
    15: ("在失乐园打倒首领", "paradise_champ", 2, None),
    16: ("完成城镇委托", "town_quest", 2, None),          # 城镇支线（add_town_life.py）
    17: ("发现新的群系、城镇或地标", "explore", 1, None),  # 见闻录（add_explore.py）
    18: ("参与全村副本", "town_event", 1, None),          # 三场副本（add_town_events.py）
}
NB = len(BOUNTIES)


def fn(name, lines):
    global COUNT
    path = os.path.join(FUNC, "events", name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT += 1


def X(name):
    return "%s/%s" % (P, name)


def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def J(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def seg(text, colour, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def read(rel):
    return io.open(os.path.join(FUNC, rel), encoding="utf-8").read()


def write(rel, s):
    io.open(os.path.join(FUNC, rel), "w", encoding="utf-8", newline="\n").write(s)


def patch(rel, guard, text, where="end"):
    s = read(rel)
    if guard in s:
        return
    if where == "end":
        s = s.rstrip("\n") + "\n" + text
    else:
        assert where in s, (rel, where)
        s = s.replace(where, text + where, 1)
    write(rel, s)


def broadcast(k, body, who="@a"):
    name, en, col, _d = EVENTS[k]
    return "tellraw %s %s" % (who, J(["", seg("〖事件%s%s〗" % (ui.TAG_JOIN, name), col, True),
                                     seg(" " + ui.fraktur(en), ui.BROADCAST_GLOSS), seg("  ", ui.BROADCAST_BODY)] + body))


def body(text):
    return [seg(text, ui.BROADCAST_BODY)]


def coords():
    return [seg("　坐标 ", ui.BROADCAST_BODY), {"nbt": "cur.x", "storage": "rpg:events", "color": ui.BROADCAST_NAME},
            seg(", ", ui.BROADCAST_BODY), {"nbt": "cur.z", "storage": "rpg:events", "color": ui.BROADCAST_NAME}]


# ============================================================================ 核心：调度
def core():
    hook_tag(DP, "load", P + "/load", False)
    fn("load", ["scoreboard objectives add %s dummy" % o for o in
                (O, "rpg_ev_tc", "rpg_bt_day", "rpg_bt_total", "rpg_bt_t1", "rpg_bt_t2", "rpg_bt_t3",
                 "rpg_bt_p1", "rpg_bt_p2", "rpg_bt_p3", "rpg_bt_c1", "rpg_bt_c2", "rpg_bt_c3")] + [
        "scoreboard objectives add rpg_jr_do trigger",
        "scoreboard players set #20 %s 20" % O, "scoreboard players set #8 %s 8" % O,
        "scoreboard players set #7 %s 7" % O, "scoreboard players set #24000 %s 24000" % O,
        "execute unless data storage rpg:events cur run data modify storage rpg:events cur set value {n:\"\",x:0,z:0}",
        "execute unless score #ev %s matches 0.. run scoreboard players set #ev %s 0" % (O, O),
    ])
    hook_tag(DP, "tick", P + "/tick", True)
    fn("tick", [
        "execute as @a[scores={rpg_jr_do=1..}] at @s run function %s" % X("jr/press"),
        "scoreboard players add #t %s 1" % O,
        "execute if score #t %s matches 20.. run function %s" % (O, X("sec")),
    ])
    sec = ["scoreboard players set #t %s 0" % O,
           "execute store result score #now %s run time query gametime" % O,
           "scoreboard players enable @a rpg_jr_do",
           "# 进行中的事件",
           "execute if score #ev %s matches 1.. run function %s" % (O, X("run")),
           "# 每 10 分钟掷一次",
           "scoreboard players add #roll %s 1" % O,
           "execute if score #roll %s matches 600.. run function %s" % (O, X("roll")),
           "# 悬赏换日",
           "execute store result score #day %s run time query day" % O,
           "execute as @a[scores={rpg_ob=100}] unless score @s rpg_bt_day = #day %s run function %s" % (O, X("bt/reroll"))]
    fn("sec", sec)
    roll = ["scoreboard players set #roll %s 0" % O,
            "execute if score #ev %s matches 1.. run return 0" % O,
            "tag @a remove rpg.ev.host",
            "tag @r[scores={rpg_ob=100},gamemode=!spectator] add rpg.ev.host",
            "execute unless entity @a[tag=rpg.ev.host] run return 0",
            "execute store result score #r %s run random value 1..5" % O,
            "execute as @a[tag=rpg.ev.host,limit=1] at @s run function %s" % X("try")]
    fn("roll", roll)
    fn("try", [
        "# as/at 选中的玩家：主世界才开；不满足条件就换成寻宝者",
        "execute unless dimension minecraft:overworld run return 0",
        "execute store result score #day %s run time query daytime" % O,
        "scoreboard players set #k %s 4" % O,
        "execute if score #r %s matches 1 if score #day %s matches 13000..22000 if score @s rpg_sef matches 3.. run scoreboard players set #k %s 1" % (O, O, O),
        "execute if score #r %s matches 2 if score @s rpg_sef matches 4.. run scoreboard players set #k %s 2" % (O, O),
        "execute if score #r %s matches 3 if score @s rpg_sef matches 5.. run scoreboard players set #k %s 3" % (O, O),
        "execute if score #r %s matches 5 if entity @e[type=minecraft:villager,tag=rpg.vacant,distance=..64] run scoreboard players set #k %s 5" % (O, O),
    ] + ["execute if score #k %s matches %d run return run function %s" % (O, k, X("e%d/start" % k)) for k in EVENTS])
    run = ["# 进行中的事件（每秒）",
           "scoreboard players operation #left %s = #end %s" % (O, O),
           "scoreboard players operation #left %s -= #now %s" % (O, O),
           "scoreboard players operation #left %s /= #20 %s" % (O, O)]
    for k in EVENTS:
        run.append("execute if score #ev %s matches %d run function %s" % (O, k, X("e%d/sec" % k)))
    run.append("execute if score #ev %s matches 1.. if score #left %s matches ..0 run function %s" % (O, O, X("end")))
    fn("run", run)
    fn("end", ["# 事件结束（超时或完成）"] +
       ["execute if score #ev %s matches %d run function %s" % (O, k, X("e%d/stop" % k)) for k in EVENTS] +
       ["scoreboard players set #ev %s 0" % O, "data modify storage rpg:events cur.n set value \"\"",
        "kill @e[type=minecraft:marker,tag=rpg.ev.mk]"])
    # 开始一个事件的公共部分：#ev、#end、坐标
    for k, (name, en, col, dur) in EVENTS.items():
        fn("e%d/begin" % k, [
            "scoreboard players set #ev %s %d" % (O, k),
            "scoreboard players operation #end %s = #now %s" % (O, O),
            "scoreboard players add #end %s %d" % (O, dur),
            "data modify storage rpg:events cur.n set value \"%s\"" % name,
            "execute store result storage rpg:events cur.x int 1 run data get entity @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] Pos[0]",
            "execute store result storage rpg:events cur.z int 1 run data get entity @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] Pos[2]"])
    fn("place", [
        "# as/at 主持玩家：在 16~40 格外的地面上放事件标记",
        "kill @e[type=minecraft:marker,tag=rpg.ev.mk]",
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.ev.mk\"]}",
        "spreadplayers ~ ~ 4 28 under 200 false @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1]"])
    fn("place_near", [
        "kill @e[type=minecraft:marker,tag=rpg.ev.mk]",
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.ev.mk\"]}",
        "spreadplayers ~ ~ 2 10 under 200 false @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1]"])
    # 管理员：直接开某个事件 / 结束
    for k in EVENTS:
        fn("admin/start_%d" % k, ["function %s" % X("end"), "scoreboard players operation #now %s = #now %s" % (O, O),
                                  "execute store result score #now %s run time query gametime" % O,
                                  "function %s" % X("e%d/start" % k)])
    fn("admin/end", ["function %s" % X("end")])


# ============================================================================ 1 罪潮之夜
def tide():
    fn("e1/start", ["function %s" % X("place_near"), "function %s" % X("e1/begin"),
                    "scoreboard players set #tide %s 1" % O,
                    "scoreboard players set @a rpg_ev_tc 0",
                    "tag @a remove rpg.ev.yesod",
                    broadcast(1, body("今夜罪孽涨潮。精英成群出没，残魂也比往常更多（10 分钟）。")),
                    "playsound minecraft:ambient.cave master @a ~ ~ ~ 1 0.5"])
    fn("e1/sec", [])
    fn("e1/stop", ["scoreboard players set #tide %s 0" % O, broadcast(1, body("潮水退了。"))])
    # 精英出现率 ×3（add_elites 的 roll）
    patch("elite/roll.mcfunction", "#tide rpg_ev",
          "execute if score #tide rpg_ev matches 1 run scoreboard players operation #p rpg_el *= #3 rpg_el\n",
          where="execute store result score #r rpg_el run random value 1..1000")
    # 杀怪残魂再掷一次
    wj(os.path.join(DP, "data", "rpg", "advancement", "events", "tide_kill.json"), {
        "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
            {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": "#rpg:world_mobs"}}]}}},
        "rewards": {"function": X("e1/kill")}})
    fn("e1/kill", ["advancement revoke @s only rpg:events/tide_kill",
                   "execute unless score #tide %s matches 1 run return 0" % O,
                   "execute if predicate {condition:\"minecraft:random_chance\",chance:0.06} run loot give @s loot rpg:forge/item/soul"])
    fn("e1/champ", ["# 罪潮之夜里打倒首领（as 玩家）",
                    "execute unless score #tide %s matches 1 run return 0" % O,
                    "scoreboard players add @s rpg_ev_tc 1",
                    "execute if score @s rpg_ev_tc matches 3 unless entity @s[tag=rpg.ev.yesod] run function %s" % X("e1/yesod")])
    fn("e1/yesod", ["tag @s add rpg.ev.yesod", "function rpg:world/kab/line_11",
                    "tellraw @s " + J(["", seg("[秘仪]", ui.RITUAL, True), seg("　月亮底下最长的一夜里，你站到了最后。源质「基础」。", ui.GRAY)])])
    for g in W.GROUPS:
        patch("elite/kill/%s_champion.mcfunction" % g, X("e1/champ"), "function %s\n" % X("e1/champ"))


# ============================================================================ 2 坠星
def star():
    fn("e2/start", ["function %s" % X("place"), "function %s" % X("e2/begin"),
                    "scoreboard players set #stage %s 0" % O,
                    broadcast(2, body("一颗星从天上落下来了。") + coords()),
                    "playsound minecraft:entity.firework_rocket.launch master @a ~ ~ ~ 1 0.5"])
    falling = ["# 前 3 秒：火光从天上落到标记处；第 3 秒落地"]
    for k in range(1, 4):
        falling.append("execute if score #stage %s matches %d at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run particle minecraft:flame ~ ~%d ~ 0.4 1.2 0.4 0.05 40 force" % (O, k - 1, 36 - k * 10))
        falling.append("execute if score #stage %s matches %d at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run particle minecraft:end_rod ~ ~%d ~ 0.3 0.8 0.3 0.02 16 force" % (O, k - 1, 36 - k * 10))
    fn("e2/sec", falling + [
        "scoreboard players add #stage %s 1" % O,
        "execute if score #stage %s matches 3 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function %s" % (O, X("e2/land")),
        "execute if score #stage %s matches 4.. at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run particle minecraft:end_rod ~ ~1 ~ 0.6 0.6 0.6 0.01 4" % O,
        "execute if score #stage %s matches 5.. unless entity @e[tag=rpg.ev.star] at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function %s" % (O, X("e2/done")),
    ])
    guards = []
    for mob, dx, dz in (("husk", 2, 0), ("zombie", -2, 1), ("skeleton", 0, -2)):
        guards.append("summon minecraft:%s ~%d ~ ~%d {Tags:[\"rpg.ev.star\",\"rpg.ev.new\"],PersistenceRequired:1b}" % (mob, dx, dz))
    fn("e2/land", [
        "particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1 force",
        "particle minecraft:flame ~ ~0.5 ~ 2 0.5 2 0.1 120 force",
        "playsound minecraft:entity.generic.explode master @a[distance=..64] ~ ~ ~ 2 0.6",
        "summon minecraft:block_display ~-0.5 ~ ~-0.5 {Tags:[\"rpg.ev.deco\"],block_state:{Name:\"minecraft:crying_obsidian\"},brightness:{sky:15,block:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}",
        "summon minecraft:block_display ~0.1 ~0.6 ~0.1 {Tags:[\"rpg.ev.deco\"],block_state:{Name:\"minecraft:magma_block\"},brightness:{sky:15,block:15},transformation:{translation:[-0.3f,0f,-0.3f],left_rotation:[0.2f,0.1f,0f,0.97f],scale:[0.6f,0.6f,0.6f],right_rotation:[0f,0f,0f,1f]}}",
    ] + guards + [
        "scoreboard players set #sef rpg_el 4",
        "execute as @a[distance=..64] if score @s rpg_sef > #sef rpg_el run scoreboard players operation #sef rpg_el = @s rpg_sef",
        "execute as @e[tag=rpg.ev.new] at @s run function rpg:elite/make",
        "tag @e[tag=rpg.ev.new] remove rpg.ev.new",
    ])
    fn("e2/done", [
        "execute as @a[distance=..48,gamemode=!spectator] run function %s" % X("e2/reward"),
        broadcast(2, body("陨星的守卫都倒下了。")),
        "function %s" % X("end")])
    fn("e2/reward", ["loot give @s loot rpg:world/sp/star", "loot give @s loot rpg:world/raw/diamond",
                     "execute if predicate {condition:\"minecraft:random_chance\",chance:0.5} run loot give @s loot rpg:world/sp/star"])
    fn("e2/stop", ["kill @e[tag=rpg.ev.deco]", "tag @e[tag=rpg.ev.star] remove rpg.ev.star"])
    wj(os.path.join(DP, "data", "rpg", "advancement", "events", "star_guard.json"), {
        "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
            {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": "{Tags:[\"rpg.ev.star\"]}"}}]}}},
        "rewards": {"function": X("e2/guard")}})
    fn("e2/guard", ["advancement revoke @s only rpg:events/star_guard",
                    "execute if predicate {condition:\"minecraft:random_chance\",chance:0.1} run function %s" % X("e2/hod")])
    fn("e2/hod", ["function rpg:world/kab/line_10",
                  "tellraw @s " + J(["", seg("[秘仪]", ui.RITUAL, True), seg("　从天上掉下来的光，落在了你手里。源质「光辉」。", ui.GRAY)])])


# ============================================================================ 3 罪仆巡逻
def patrol():
    start = ["function %s" % X("place"), "function %s" % X("e3/begin"),
             "execute store result score #pp %s run random value 1..7" % O]
    for p in ui.PILLARS:
        d = os.path.join(FUNC, "minion", "summon", p["slug"])
        spirits = sorted(f[:-11] for f in os.listdir(d) if f.endswith(".mcfunction") and f != "all.mcfunction")[:3]
        fn("e3/spawn_%d" % p["n"], ["function rpg:minion/summon/%s/%s" % (p["slug"], s) for s in spirits] +
           ["tag @e[tag=rpg.demon.minion,distance=..6] add rpg.ev.patrol"])
        start.append("execute if score #pp %s matches %d at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function %s" % (O, p["n"], X("e3/spawn_%d" % p["n"])))
    start += [broadcast(3, body("一队罪仆在附近游荡。") + coords()),
              "playsound minecraft:entity.evoker.prepare_summon master @a ~ ~ ~ 1 0.6"]
    fn("e3/start", start)
    fn("e3/sec", ["execute unless entity @e[tag=rpg.ev.patrol] at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function %s" % X("e3/done")])
    reward = ["loot give @s loot rpg:world/sin_shard_%d" % 0]
    rw = []
    for p in ui.PILLARS:
        rw += ["execute if score #pp %s matches %d run loot give @s loot rpg:world/sin_shard_%d" % (O, p["n"], p["n"]),
               "execute if score #pp %s matches %d run loot give @s loot rpg:world/sin_shard_%d" % (O, p["n"], p["n"]),
               "execute if score #pp %s matches %d if predicate {condition:\"minecraft:random_chance\",chance:0.25} run function rpg:inquest/give/pact%d" % (O, p["n"], p["n"])]
    fn("e3/reward", rw)
    fn("e3/done", ["execute as @a[distance=..48,gamemode=!spectator] run function %s" % X("e3/reward"),
                   broadcast(3, body("巡逻的罪仆都倒下了。")), "function %s" % X("end")])
    fn("e3/stop", ["tag @e[tag=rpg.ev.patrol] remove rpg.ev.patrol"])


# ============================================================================ 4 寻宝者
def goblin():
    import add_world_loot as L
    tpl = json.load(io.open(os.path.join(HERE, "world_loot_currency.json"), encoding="utf-8"))
    cur = tpl["entries"][1]
    wj(os.path.join(LOOT, "world", "currency.json"), {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": [
        dict(cur, functions=[f for f in cur["functions"] if "set_count" not in f.get("function", "")] + [
            {"function": "minecraft:set_count", "count": 1}])]}]})
    wj(os.path.join(LOOT, "world", "goblin.json"), {"type": "minecraft:generic", "pools": [
        {"rolls": {"type": "minecraft:uniform", "min": 3, "max": 6}, "entries": [{"type": "minecraft:loot_table", "value": "rpg:world/currency"}]},
        {"rolls": 1, "entries": [L.raw_entry("iron_ingot", 2, 4)]},
        {"rolls": 1, "entries": [L.raw_entry("gold_ingot", 1, 2)]},
        {"rolls": 1, "conditions": [{"condition": "minecraft:random_chance", "chance": 0.3}],
         "entries": [{"type": "minecraft:loot_table", "value": "rpg:world/bp_fragment"}]}]})
    name = J(["", seg(ui.fraktur("Treasure Rabbit"), ui.WHITE)])
    fn("e4/start", ["function %s" % X("place_near"), "function %s" % X("e4/begin"),
                    "execute at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run summon minecraft:rabbit ~ ~ ~ {Tags:[\"rpg.ev.gob\"],RabbitType:1,PersistenceRequired:1b,"
                    "CustomNameVisible:1b,CustomName:%s,attributes:[{id:\"scale\",base:1.4d},{id:\"movement_speed\",base:0.45d},{id:\"max_health\",base:12d}],Health:12f,"
                    "active_effects:[{id:\"glowing\",duration:-1,amplifier:0,show_particles:0b}]}" % name,
                    broadcast(4, body("一只背着钱袋的兔子在附近乱跑，30 秒后就跑没了。"), who="@a[distance=..64]"),
                    "playsound minecraft:entity.rabbit.jump master @a[distance=..64] ~ ~ ~ 1 0.6"])
    fn("e4/sec", ["execute as @e[tag=rpg.ev.gob] at @s run particle minecraft:wax_on ~ ~0.6 ~ 0.3 0.3 0.3 0 3",
                  "execute unless entity @e[tag=rpg.ev.gob] run function %s" % X("end")])
    fn("e4/stop", ["execute as @e[tag=rpg.ev.gob] at @s run particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.05 20",
                   "tp @e[tag=rpg.ev.gob] ~ -400 ~", "kill @e[tag=rpg.ev.gob]"])
    wj(os.path.join(DP, "data", "rpg", "advancement", "events", "goblin.json"), {
        "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
            {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": "{Tags:[\"rpg.ev.gob\"]}"}}]}}},
        "rewards": {"function": X("e4/kill")}})
    fn("e4/kill", ["advancement revoke @s only rpg:events/goblin", "loot give @s loot rpg:world/goblin",
                   "scoreboard players add @s rpg_ev_gob 1",
                   "playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 0.8"])
    patch("events/load.mcfunction", "rpg_ev_gob", "scoreboard objectives add rpg_ev_gob dummy\n")


# ============================================================================ 5 空缺者显现
def vacant():
    fn("e5/start", [
        "kill @e[type=minecraft:marker,tag=rpg.ev.mk]",
        "execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..64,limit=1,sort=nearest] at @s run summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.ev.mk\"]}",
        "execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..64,limit=1,sort=nearest] run effect give @s minecraft:glowing 60 0 true",
        "function %s" % X("e5/begin"),
        broadcast(5, body("村子里有一个人不对劲。他在发光。") + coords()),
        "playsound minecraft:ambient.cave master @a ~ ~ ~ 1 1.4"])
    fn("e5/sec", [])
    fn("e5/stop", [])


# ============================================================================ 悬赏
def bounty():
    # 按组的击杀进度
    for g in ("undead", "arthropod", "arcane", "nether"):
        wj(os.path.join(DP, "data", "rpg", "tags", "entity_type", "wl_%s.json" % g),
           {"values": ["minecraft:" + m for m in W.GROUPS[g][1]]})
        wj(os.path.join(DP, "data", "rpg", "advancement", "events", "bt_%s.json" % g), {
            "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": "#rpg:wl_%s" % g}}]}}},
            "rewards": {"function": X("bt/kill_%s" % g)}})
        ids = [k for k, v in BOUNTIES.items() if v[3] == g]
        lines = ["advancement revoke @s only rpg:events/bt_%s" % g]
        for s in (1, 2, 3):
            for k in ids:
                lines.append("execute if score @s rpg_bt_t%d matches %d run scoreboard players add @s rpg_bt_p%d 1" % (s, k, s))
        fn("bt/kill_%s" % g, lines)
    el = [k for k, v in BOUNTIES.items() if v[1] == "elite"]
    fn("bt/elite", ["execute if score @s rpg_bt_t%d matches %d run scoreboard players add @s rpg_bt_p%d 1" % (s, k, s) for s in (1, 2, 3) for k in el])
    for kind in ("trial", "paradise", "paradise_champ", "town_quest", "explore", "town_event"):      # 失乐园、城镇、见闻录里调
        ids = [k for k, v in BOUNTIES.items() if v[1] == kind]
        fn("bt/" + kind, ["execute if score @s rpg_bt_t%d matches %d run scoreboard players add @s rpg_bt_p%d 1" % (s, k, s) for s in (1, 2, 3) for k in ids])
    for g in W.GROUPS:
        for suffix in ("", "_champion"):
            patch("elite/kill/%s%s.mcfunction" % (g, suffix), X("bt/elite"), "function %s\n" % X("bt/elite"))
    # 换日：三条不重样
    fn("bt/reroll", [
        "scoreboard players operation @s rpg_bt_day = #day %s" % O,
        "execute store result score @s rpg_bt_t1 run random value 1..%d" % NB,
        "execute store result score #d %s run random value 1..%d" % (O, NB - 1),
        "execute store result score #e %s run random value 1..%d" % (O, NB - 1),
        "execute if score #e %s = #d %s run function %s" % (O, O, X("bt/bump")),
        "scoreboard players operation @s rpg_bt_t2 = @s rpg_bt_t1",
        "scoreboard players operation @s rpg_bt_t2 += #d %s" % O,
        "scoreboard players operation @s rpg_bt_t3 = @s rpg_bt_t1",
        "scoreboard players operation @s rpg_bt_t3 += #e %s" % O,
        "execute if score @s rpg_bt_t2 matches %d.. run scoreboard players remove @s rpg_bt_t2 %d" % (NB + 1, NB),
        "execute if score @s rpg_bt_t3 matches %d.. run scoreboard players remove @s rpg_bt_t3 %d" % (NB + 1, NB),
    ] + ["scoreboard players set @s rpg_bt_p%d 0" % s for s in (1, 2, 3)] +
       ["scoreboard players set @s rpg_bt_c%d 0" % s for s in (1, 2, 3)] + ["tag @s remove rpg.bt.all"])
    fn("bt/bump", ["scoreboard players add #e %s 1" % O,
                   "execute if score #e %s matches %d.. run scoreboard players set #e %s 1" % (O, NB, O)])
    # 领取：第 s 条
    for s in (1, 2, 3):
        lines = ["# 领取第 %d 条悬赏（as 玩家）" % s,
                 "execute if score @s rpg_bt_c%d matches 1 run return run %s" % (s, say("这条已经领过了"))]
        for k, (text, kind, goal, key) in BOUNTIES.items():
            if kind == "give":
                lines += ["execute if score @s rpg_bt_t%d matches %d store result score #c %s run clear @s %s 0" % (s, k, O, key),
                          "execute if score @s rpg_bt_t%d matches %d unless score #c %s matches %d.. run return run %s" % (s, k, O, goal, say("%s不够（要 %d）" % (text[2:], goal))),
                          "execute if score @s rpg_bt_t%d matches %d run clear @s %s %d" % (s, k, key, goal)]
            else:
                lines.append("execute if score @s rpg_bt_t%d matches %d unless score @s rpg_bt_p%d matches %d.. run return run %s" % (s, k, s, goal, say("还没完成")))
        lines += ["scoreboard players set @s rpg_bt_c%d 1" % s, "function %s" % X("bt/reward")]
        fn("bt/claim_%d" % s, lines)
    fn("bt/reward", [
        "loot give @s loot rpg:world/currency", "loot give @s loot rpg:world/currency", "loot give @s loot rpg:world/currency",
        "loot give @s loot rpg:elite/badge",
        "scoreboard players add @s rpg_ex_xp 10",
        "scoreboard players add @s rpg_bt_total 1",
        "playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4",
        say("悬赏完成：货币 ×3、精英徽记 ×1、阅历 +10"),
        "execute if score @s rpg_bt_c1 matches 1 if score @s rpg_bt_c2 matches 1 if score @s rpg_bt_c3 matches 1 unless entity @s[tag=rpg.bt.all] run function %s" % X("bt/all"),
        "execute if score @s rpg_bt_total matches 21.. unless entity @s[tag=rpg.wl.malkuth] run function %s" % X("bt/malkuth"),
    ])
    fn("bt/all", ["tag @s add rpg.bt.all", "loot give @s loot rpg:forge/item/forge_stone", say("今天的三条悬赏都完成了：铸造之石 ×1")])
    fn("bt/malkuth", ["tag @s add rpg.wl.malkuth", "function rpg:world/kab/line_12",
                      "tellraw @s " + J(["", seg("[秘仪]", ui.RITUAL, True), seg("　大地上的事你都办妥了。源质「王国」。", ui.GRAY)])])


def say(text):
    return "tellraw @s " + J(["", seg("[悬赏]", ui.HOLY_DARK, True), seg("　" + text, ui.GRAY)])


# ============================================================================ 旅程页
def journey():
    T = lambda text, col=ui.BROADCAST_BODY, bold=False: {"text": text, "color": col, "bold": bold, "italic": False}

    def append(comp, cond=""):
        line = "%sdata modify storage rpg:panel ui.body append value %s" % (("execute %s run " % cond) if cond else "", J(comp))
        return ("$" + line) if "$(" in line else line

    def action(label, cmd, col=ui.BROADCAST_HOLY, tip=None):
        a = {"label": T(label, col, True), "action": {"type": "minecraft:run_command", "command": cmd}}
        if tip:
            a["tooltip"] = T(tip, ui.BROADCAST_BODY)
        return "data modify storage rpg:panel ui.actions append value " + J(a)

    lines = ["# 旅程页（as 玩家）",
             "data modify storage rpg:panel ui set value {title:{text:\"\"},body:[],actions:[]}",
             "data modify storage rpg:panel ui.title set value " + J(["", T("旅程", ui.BROADCAST_HOLY, True), T(" " + ui.fraktur("Journey"), ui.BROADCAST_GLOSS)]),
             append({"text": "", "extra": [T("当前事件　", ui.BROADCAST_BODY, True)]}),
             append({"text": "", "extra": [T("暂时没有。\n\n", ui.MUTED)]}, "if score #ev %s matches 0" % O),
             append({"text": "", "extra": [T("$(n)", ui.BROADCAST_NAME, True), T("　坐标 "), T("$(x), $(z)", ui.BROADCAST_NAME),
                                           T("　还剩 "), T("$(left)", ui.BROADCAST_NAME), T(" 秒\n\n")]},
                    "if score #ev %s matches 1.." % O),
             append({"text": "", "extra": [T("今日悬赏　", ui.BROADCAST_BODY, True), T("完成后在下面领取\n", ui.MUTED)]})]
    for s in (1, 2, 3):
        for k, (text, kind, goal, key) in BOUNTIES.items():
            row = [T("%d　" % s, ui.MUTED), T(text, ui.BROADCAST_NAME)]
            if kind == "give":
                row.append(T("　×%d" % goal))
            else:
                row += [T("　"), T("$(p%d)" % s, ui.BROADCAST_NAME), T("/%d" % goal)]
            lines.append(append({"text": "", "extra": row}, "if score @s rpg_bt_t%d matches %d" % (s, k)))
        lines.append(append({"text": "", "extra": [T("　已领取\n", ui.READY)]}, "if score @s rpg_bt_c%d matches 1" % s))
        lines.append(append({"text": "", "extra": [T("\n")]}, "unless score @s rpg_bt_c%d matches 1" % s))
    lines += [append({"text": "", "extra": [T("\n累计完成 "), T("$(total)", ui.BROADCAST_NAME), T(" 条悬赏")]}),
              action("领取 1", "/trigger rpg_jr_do set 11"), action("领取 2", "/trigger rpg_jr_do set 12"),
              action("领取 3", "/trigger rpg_jr_do set 13"),
              action("配方书", "/trigger rpg_jr_do set 2", tip="锻造配方与材料来源"),
              action("返回面板", "/trigger rpg_panel set 8"),
              "function rpg:panel/ui/show with storage rpg:panel ui"]
    fn("jr/body", lines)
    fill = ["# 旅程页的数值 → storage rpg:events v（面板页都是这样拼字的）",
            "scoreboard players add @s rpg_bt_total 0",
            "data modify storage rpg:events v set value {n:\"\",x:0,z:0,left:0}",
            "data modify storage rpg:events v.n set from storage rpg:events cur.n",
            "data modify storage rpg:events v.x set from storage rpg:events cur.x",
            "data modify storage rpg:events v.z set from storage rpg:events cur.z",
            "execute store result storage rpg:events v.left int 1 run scoreboard players get #left %s" % O,
            "execute store result storage rpg:events v.total int 1 run scoreboard players get @s rpg_bt_total"]
    for s_ in (1, 2, 3):
        fill += ["scoreboard players add @s rpg_bt_p%d 0" % s_,
                 "execute store result storage rpg:events v.p%d int 1 run scoreboard players get @s rpg_bt_p%d" % (s_, s_)]
    fill.append("function %s with storage rpg:events v" % X("jr/body"))
    fn("jr/open", fill)
    # 配方书
    import add_world_items as WI
    import forge_spec as FS
    rec = ["# 配方书（as 玩家）",
           "data modify storage rpg:panel ui set value {title:{text:\"\"},body:[],actions:[]}",
           "data modify storage rpg:panel ui.title set value " + J(["", T("配方书", ui.BROADCAST_HOLY, True), T(" " + ui.fraktur("Recipes"), ui.BROADCAST_GLOSS)])]
    book = [("魂火冶炼", "器胚 + 主材（铁锭 ×6 / 钻石 ×4 / 下界合金锭 + 钻石 ×4）+ 残魂 1~3"),
            ("罪器锻造", "武器核心 + 同柱罪印碎片 ×8 + 下界合金锭 + 器胚 + 残魂 ×8，原质 5 阶起，魔化 +15"),
            ("史诗图纸", "图纸 + 特殊材料 ×1 + 钻石 ×6 + 器胚 + 残魂 ×4，原质 4 阶起"),
            ("传说图纸", "图纸 + 特殊材料 ×3 + 下界合金锭 ×2 + 器胚 + 残魂 ×6，原质 6 阶起"),
            ("材料转换", "32 铁锭 + 4 残魂 → 钻石；16 钻石 + 8 残魂 → 下界合金锭；9 金粒 → 金锭；4 金锭 → 镀金箔；10 图纸碎片 → 自选图纸")]
    src = [("铁锭", "亡灵、节肢、苦力怕、咒术、末地；精英必掉"), ("钻石", "咒术、末地、水域；精英多掉一档"),
           ("下界合金锭", "下界怪物（凋灵骷髅最多）、下界首领"), ("残魂 / 器胚", "所有敌对生物、精英、首领"),
           ("罪印碎片", "该柱罪仆、罪仆巡逻"), ("图纸", "首领精英、Boss 首杀、坠星与支线；10 片碎片合一张")]
    for k, (nm, ic, lines2) in WI.SPECIAL.items():
        pass
    sp_src = {"star": "坠星事件、末地首领", "wind": "咒术首领（旋风人）", "tear": "远古守卫者、水域首领",
              "core": "下界首领", "stone": "地下（y < 0）的首领", "bronze": "圣卫", "soil": "亡灵首领"}
    rec.append(append({"text": "", "extra": [T("配方\n", ui.BROADCAST_BODY, True)]}))
    for nm, text in book:
        rec.append(append({"text": "", "extra": [T(nm, ui.BROADCAST_NAME, True), T("　" + text + "\n")]}))
    rec.append(append({"text": "", "extra": [T("\n材料从哪来\n", ui.BROADCAST_BODY, True)]}))
    for nm, text in src:
        rec.append(append({"text": "", "extra": [T(nm, ui.BROADCAST_NAME, True), T("　" + text + "\n")]}))
    for k, (nm, ic, _l) in WI.SPECIAL.items():
        rec.append(append({"text": "", "extra": [T(nm, ui.BROADCAST_NAME, True), T("　" + sp_src[k] + "\n")]}))
    rec += [action("返回旅程", "/trigger rpg_jr_do set 1"), "function rpg:panel/ui/show with storage rpg:panel ui"]
    fn("jr/recipes", rec)
    fn("jr/press", [
        "scoreboard players operation #do %s = @s rpg_jr_do" % O,
        "scoreboard players set @s rpg_jr_do 0",
        "scoreboard players enable @s rpg_jr_do",
        "execute if score #do %s matches 11 run function %s" % (O, X("bt/claim_1")),
        "execute if score #do %s matches 12 run function %s" % (O, X("bt/claim_2")),
        "execute if score #do %s matches 13 run function %s" % (O, X("bt/claim_3")),
        "execute if score #do %s matches 2 run return run function %s" % (O, X("jr/recipes")),
        "function %s" % X("jr/open"),
    ])
    # 主面板加「旅程」按钮（放在 HUD 开关之前）
    s = read("panel/pages/panel_open.mcfunction")
    if "rpg_jr_do set 1" not in s:
        lines = s.split("\n")
        at = next(i for i, l in enumerate(lines) if "HUD 开关" in l and "ui.actions append" in l)
        btn = {"label": T("旅程", ui.BROADCAST_HOLY, True), "tooltip": T("当前事件、今日悬赏与配方书", ui.BROADCAST_BODY),
               "action": {"type": "minecraft:run_command", "command": "/trigger rpg_jr_do set 1"}}
        lines.insert(at, "data modify storage rpg:panel ui.actions append value " + J(btn))
        write("panel/pages/panel_open.mcfunction", "\n".join(lines))


def main():
    import shutil
    shutil.rmtree(os.path.join(FUNC, "events"), ignore_errors=True)
    core()
    tide()
    star()
    patrol()
    goblin()
    vacant()
    bounty()
    journey()
    print("events: %d functions, %d events, %d bounty kinds" % (COUNT, len(EVENTS), NB))


if __name__ == "__main__":
    main()
