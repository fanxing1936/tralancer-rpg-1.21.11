# -*- coding: utf-8 -*-
"""阵营与玩家对战（《开局参与感》策划书「对立感从哪来」）：

- 多人服里的对抗只在野外：城镇的安全区（镇中心 72 格内，副本进行时除外）、林中营地（12 格内）不能互打；
- 同阵营不伤友军：教廷一方（没入伙的人，rpg.ch）互相、恶魔一方（rpg.dm）互相都不伤；两个阵营之间在野外可以互打；
- 抓通缉犯：暴露的恶魔信徒（rpg.dm.wanted，add_demon 的五分钟）被教廷一方的人打倒，打倒的人领赏。

做法：名字前的称号已经占用了队伍（rpg_t_*），不能再靠队伍的「友军伤害」开关；所以每刻记下每人的血量，
被不该打的人打中时（进度 entity_hurt_player 判断双方标签）立刻用瞬间治疗补回去，锻造的额外伤害也跳过。

python add_pvp.py ../rpg
"""
import io
import json
import os
import sys

import rpg_ui_style as ui
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
V = "rpg:pvp"
COUNT = [0]


def J(c):
    return json.dumps(c, ensure_ascii=False, separators=(",", ":"))


def T(text, colour=ui.BROADCAST_BODY, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def fn(name, lines):
    path = os.path.join(FUNC, "pvp", name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT[0] += 1


def wj(rel, doc):
    path = os.path.join(DP, "data", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)


def tagged(t):
    return {"nbt": "{Tags:[\"%s\"]}" % t}


def build():
    fn("load", ["scoreboard objectives add rpg_pv_hp dummy", "scoreboard objectives add rpg_pv_n dummy", "schedule function %s/sec 20t" % V])
    hook_tag(DP, "load", V + "/load", False)
    fn("tick", ["# 每刻记下血量（×10），挨了不该挨的打时补回去",
                "execute as @a store result score @s rpg_pv_hp run data get entity @s Health 10"])
    hook_tag(DP, "tick", V + "/tick", False)
    fn("sec", ["schedule function %s/sec 20t" % V,
               "tag @a[tag=!rpg.dm] add rpg.ch", "tag @a[tag=rpg.dm] remove rpg.ch",
               "tag @a remove rpg.safe",
               "execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c,tag=!rpg.tw.lm] at @s unless score @s rpg_tw_ev matches 1.. run tag @a[distance=..72] add rpg.safe",
               "execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.at.camp] at @s run tag @a[distance=..12] add rpg.safe",
               "tag @a remove rpg.dm.wanted", "tag @a[scores={rpg_dm_exp=1..}] add rpg.dm.wanted"])
    cases = {"ch": ([tagged("rpg.ch")], tagged("rpg.ch")), "dm": ([tagged("rpg.dm")], tagged("rpg.dm")), "safe": ([tagged("rpg.safe")], {})}
    for k, (victim, attacker) in cases.items():
        src = {"type": "minecraft:player"}
        src.update(attacker)
        wj("rpg/advancement/pvp/%s.json" % k, {"criteria": {"hit": {"trigger": "minecraft:entity_hurt_player", "conditions": {
            "damage": {"source_entity": src}}}}, "rewards": {"function": "%s/undo_%s" % (V, k)}})
        msg = {"ch": "同阵营不伤友军", "dm": "同阵营不伤友军", "safe": "镇里和营地里不能动手"}[k]
        need = {"ch": "rpg.ch", "dm": "rpg.dm", "safe": "rpg.safe"}[k]
        fn("undo_%s" % k, ["advancement revoke @s only rpg:pvp/%s" % k, "execute unless entity @s[tag=%s] run return 0" % need, "function %s/undo" % V,
                           "title @s actionbar " + J(["", T(msg, ui.MUTED)])])
    fn("undo", ["# 补回刚才挨的那一下（as 挨打的人）：瞬间治疗一次补 4 点",
                "execute store result score #now rpg_pv_n run data get entity @s Health 10",
                "scoreboard players operation #lost rpg_pv_n = @s rpg_pv_hp",
                "scoreboard players operation #lost rpg_pv_n -= #now rpg_pv_n",
                "execute if score #lost rpg_pv_n matches 1.. run function %s/heal" % V])
    fn("heal", ["effect give @s minecraft:instant_health 1 0 true", "scoreboard players remove #lost rpg_pv_n 40",
                "execute if score #lost rpg_pv_n matches 1.. run function %s/heal" % V])
    # 抓通缉犯
    wj("rpg/advancement/pvp/bounty.json", {"criteria": {"k": {"trigger": "minecraft:player_killed_entity", "conditions": {
        "entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": dict(type="minecraft:player", **tagged("rpg.dm.wanted"))}]}}},
        "rewards": {"function": V + "/bounty"}})
    fn("bounty", ["advancement revoke @s only rpg:pvp/bounty", "execute unless entity @s[tag=rpg.ch] run return 0"] + ["loot give @s loot rpg:world/currency"] * 5 + [
        "scoreboard players add @s rpg_tl_ch 10",
        "tellraw @a " + J(["", T("〖通缉令〗", ui.BROADCAST_HOLY, True), T(ui.GAP, ui.BROADCAST_BODY), {"selector": "@s", "color": ui.BROADCAST_NAME},
                           T(" 拿下了一名暴露的恶魔信徒，领了教廷的赏。", ui.BROADCAST_BODY)])])
    # 锻造的额外伤害：同阵营、安全区里不加
    p = os.path.join(FUNC, "forge", "hit", "apply.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg.safe" not in s:
        head = ("# 阵营（add_pvp.py）：同阵营、安全区里的玩家不吃额外伤害\n"
                "execute if entity @s[type=minecraft:player,tag=rpg.safe] run return 0\n"
                "execute if entity @s[type=minecraft:player,tag=rpg.ch] if entity @a[tag=rpg.fg.atk,tag=rpg.ch] run return 0\n"
                "execute if entity @s[type=minecraft:player,tag=rpg.dm] if entity @a[tag=rpg.fg.atk,tag=rpg.dm] run return 0\n")
        io.open(p, "w", encoding="utf-8", newline="\n").write(head + s)


def main():
    build()
    print("pvp: %d 个函数" % COUNT[0])


if __name__ == "__main__":
    main()
