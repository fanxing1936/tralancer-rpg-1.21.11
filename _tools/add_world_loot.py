# -*- coding: utf-8 -*-
"""世界怪物掉落表 + 禁用原版合成（策划书第一步，用户 2026-11-23）。

    python add_world_loot.py ../rpg

* 7 组敌对生物（world_loot_spec.GROUPS）各写一张 minecraft:entities/<生物> 表：
  原版产物（[货币] 前缀 + 两行 Lore，沿用原来七张自写表的样子）、锻造原料（[锻造] 前缀，直接掉成品）、
  残魂、器胚、货币。原料、残魂、器胚只认玩家亲手击杀，抢夺按原版规则加成。
  原来七张自写表里的货币池原样保留（读现有文件里带 currency_tag 的那一池）。
* add_drop_policy.py 从 WORLD_TABLES 读名单，把这些生物从「清空」改成「自写」——所以本脚本必须在它之前跑。
* 原版合成：limited_crafting 打开（只能合成已解锁的配方），每 2 秒把玩家配方书里的配方整个收回。冒险模式里没有挖矿、没有合成台，原料只能来自怪物。
"""
import copy
import io
import json
import os
import sys

import rpg_ui_style as ui
import world_loot_spec as S
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
ENT = os.path.join(DP, "data", "minecraft", "loot_table", "entities")
FUNC = os.path.join(DP, "data", "rpg", "function", "world")
HERE = os.path.dirname(os.path.abspath(__file__))
C_FORGE = ui.mix(ui.HOLY_DARK, ui.WARN, 0.35)
RULE = ["", {"text": ui.RULE_TEXT, "color": ui.WHITE, "bold": False, "italic": False}]


def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def fn(name, lines):
    path = os.path.join(FUNC, name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def seg(text, colour, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def chance(p):
    return [{"condition": "minecraft:killed_by_player"},
            {"condition": "minecraft:random_chance_with_enchanted_bonus", "enchantment": "minecraft:looting",
             "unenchanted_chance": p,
             "enchanted_chance": {"type": "minecraft:linear", "base": round(p * 1.2, 4),
                                  "per_level_above_first": round(p * 0.2, 4)}}]


def count(lo, hi):
    if lo == hi:
        return {"function": "minecraft:set_count", "count": lo}
    return {"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}


def raw_entry(item, lo, hi):
    name, lines = S.RAW[item]
    return {"type": "minecraft:item", "name": "minecraft:" + item, "functions": [
        {"function": "minecraft:set_components", "components": {
            "minecraft:custom_name": ["", seg("[锻造]", C_FORGE, True), seg(name, ui.WHITE)],
            "minecraft:lore": [RULE] + [["", seg(l, ui.GRAY)] for l in lines] + [RULE]}},
        count(lo, hi)]}


def base_entry(mob, item, name, lo, hi, tag, line2):
    """原版产物：沿用原来七张自写表的格式（[货币] 灰前缀 + 「X 的[Y]」两行 Lore）。"""
    lead, noun = line2
    return {"type": "minecraft:item", "name": "minecraft:" + item, "functions": [
        {"function": "minecraft:set_components", "components": {
            "minecraft:custom_name": ["", seg("[货币]", ui.MUTED, True), seg(name, ui.WHITE)],
            "minecraft:lore": [RULE,
                               ["", seg(S.MOB_NAME[mob] + "的", ui.GRAY), seg("[%s]" % tag, ui.MUTED, True)],
                               ["", seg(lead, ui.GRAY), seg("[%s]" % noun, ui.MUTED, True)],
                               RULE]}},
        count(lo, hi),
        {"function": "minecraft:enchanted_count_increase", "enchantment": "minecraft:looting",
         "count": {"type": "minecraft:uniform", "min": 0, "max": 1}}]}


def currency_pool(mob, p):
    """原来就有货币池的表原样保留；新表用模板，概率按组表。"""
    old = os.path.join(ENT, mob + ".json")
    if os.path.exists(old):
        for pool in json.load(io.open(old, encoding="utf-8")).get("pools", []):
            if "currency_tag" in json.dumps(pool):
                return pool
    if p is None:
        p = 0.10
    tpl = json.load(io.open(os.path.join(HERE, "world_loot_currency.json"), encoding="utf-8"))
    pool = copy.deepcopy(tpl)
    pool["entries"][0]["weight"] = int(round((1 - p) * 100))
    pool["entries"][1]["weight"] = int(round(p * 100))
    return pool


def table(mob, base, raws, soul, blank, money):
    pools = [currency_pool(mob, money)]
    for item, name, lo, hi, tag, line2 in base:
        pools.append({"rolls": 1, "entries": [base_entry(mob, item, name, lo, hi, tag, line2)]})
    for item, p, lo, hi in raws + S.EXTRA.get(mob, []):
        pools.append({"rolls": 1, "conditions": chance(p) if p < 1 else [{"condition": "minecraft:killed_by_player"}],
                      "entries": [raw_entry(item, lo, hi)]})
    for ref, p in (("rpg:forge/item/soul", soul), ("rpg:forge/item/blank", blank)):
        pools.append({"rolls": 1, "conditions": chance(p), "entries": [{"type": "minecraft:loot_table", "value": ref}]})
    return {"type": "minecraft:entity", "pools": pools}


def recipes():
    hook_tag(DP, "load", "rpg:world/load", False)
    fn("load", ["# 冒险模式：原版合成表全部禁用（world_loot / 用户 2026-11-23）",
                "gamerule limited_crafting true",
                "scoreboard objectives add rpg_wl_rl dummy"])
    hook_tag(DP, "tick", "rpg:world/tick", True)
    fn("tick", ["# 每 2 秒：配方书里出现原版配方（捡东西时原版会自动解锁）就整个收回。",
                "# recipe_unlocked 进度在 1.21.11 必须指定配方，没法当「任意解锁」用，所以改成轮询。",
                "scoreboard players add #t rpg_wl_rl 1",
                "execute if score #t rpg_wl_rl matches 40.. run function rpg:world/recipe_scan"])
    fn("recipe_scan", ["scoreboard players set #t rpg_wl_rl 0",
                       "execute as @a if data entity @s recipeBook.recipes[0] run recipe take @s *"])


def recipe_advancements():
    """原版的配方解锁进度全部改成永不触发：捡东西时不再解锁配方，也不会弹「新配方已解锁」。"""
    import zipfile
    from mc_env import JAR
    if not os.path.isfile(JAR):
        print("world loot: client jar not found, recipe advancements not overridden")
        return 0
    n = 0
    with zipfile.ZipFile(JAR) as z:
        for name in z.namelist():
            if name.startswith("data/minecraft/advancement/recipes/") and name.endswith(".json"):
                wj(os.path.join(DP, *name.split("/")), {"criteria": {"never": {"trigger": "minecraft:impossible"}}})
                n += 1
    return n


def main():
    n = 0
    for key, (gname, mobs, raws, soul, blank, money) in S.GROUPS.items():
        for mob, base in mobs.items():
            wj(os.path.join(ENT, mob + ".json"), table(mob, base, raws, soul, blank, money))
            n += 1
    recipes()
    k = recipe_advancements()
    assert n == len(S.WORLD_TABLES)
    print("world loot: %d mob tables in %d groups, vanilla crafting locked (%d recipe advancements silenced)" % (n, len(S.GROUPS), k))


if __name__ == "__main__":
    main()
