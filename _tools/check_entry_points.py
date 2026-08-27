# -*- coding: utf-8 -*-
"""构建期断言：两道自然入口不能静默断线或意外多发。"""
from __future__ import annotations

import json
import sys
from pathlib import Path


DP = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
FUNC = DP / "data" / "rpg" / "function"
ADV = DP / "data" / "rpg" / "advancement"
errors: list[str] = []


def source(rel: str) -> str:
    path = FUNC / rel
    if not path.is_file():
        errors.append("missing entry function: " + rel)
        return ""
    return path.read_text(encoding="utf-8")


chapter_invite = source("entry/chapter/invite.mcfunction")
endless_invite = source("entry/endless/invite.mcfunction")
chapter_use = source("entry/chapter/use.mcfunction")
endless_use = source("entry/endless/use.mcfunction")
free = source("rite/free.mcfunction")

chapter_hook = "execute as @a[distance=..8,tag=!rpg.ch1.invited] run function rpg:entry/chapter/invite"
if free.count(chapter_hook) != 1:
    errors.append("rite/free must contain exactly one 8-block chapter invitation hook")
if "@p" in free or "sort=nearest" in free:
    errors.append("rite/free invitation must not choose a nearest player")

reveal_calls = 0
for pillar in range(1, 8):
    reveal = source("inquest/reveal/%d.mcfunction" % pillar)
    hook = "execute unless entity @s[tag=rpg.endless.invited] run function rpg:entry/endless/invite"
    if reveal.count("tag @s add rpg.name.%d" % pillar) != 1 or reveal.count(hook) != 1:
        errors.append("pillar %d true-name landing is not wired exactly once" % pillar)
    reveal_calls += reveal.count(hook)
if reveal_calls != 7:
    errors.append("all seven true-name landings must share the one endless invitation function")

all_functions = "\n".join(
    path.read_text(encoding="utf-8") for path in FUNC.rglob("*.mcfunction"))

# 按**身份**数发放点，不按底材。
#
# 原本这里数的是 `give @s minecraft:echo_shard[` —— 那在写下它的那一刻确实
# 只有一处，但那是**偶然的唯一性**：七件封印遗物同样是 echo_shard，
# 只是当时写的是不带命名空间的 `echo_shard`，恰好没撞上。遗物那边一改写，
# 断言立刻误报"信物有多个发放点"。
#
# 底材会重名，custom_data 标记不会 —— 那才是这件东西的身份。
for marker, label in (("rpg_ch1_roster", "parish roster"),
                      ("rpg_endless_token", "corridor token")):
    sites = sum(1 for line in all_functions.split("\n")
                if line.lstrip().startswith(("give ", "execute"))
                and "give " in line and marker in line)
    if sites != 1:
        errors.append("%s must have exactly one give site (found %d)"
                      % (label, sites))

for body, tag, marker, label in (
        (chapter_invite, "rpg.ch1.invited", "rpg_ch1_roster", "chapter"),
        (endless_invite, "rpg.endless.invited", "rpg_endless_token", "endless")):
    if body.count("tag @s add " + tag) != 1 or body.find("tag @s add " + tag) > body.find("give @s "):
        errors.append(label + " invitation must persist its guard before giving")
    for signature in (marker + ":1b", "minecraft:consumable", "minecraft:max_stack_size=1", "背包已满", "脚边"):
        if signature not in body:
            errors.append(label + " invitation missing: " + signature)

for name, marker, reward in (
        ("chapter_use", "{rpg_ch1_roster:1b}", "rpg:entry/chapter/use"),
        ("endless_use", "{rpg_endless_token:1b}", "rpg:entry/endless/use")):
    path = ADV / "entry" / (name + ".json")
    if not path.is_file():
        errors.append("missing entry advancement: " + name)
        continue
    doc = json.loads(path.read_text(encoding="utf-8"))
    dumped = json.dumps(doc, ensure_ascii=False)
    if "minecraft:using_item" not in dumped or marker not in dumped or doc.get("rewards", {}).get("function") != reward:
        errors.append(name + " advancement is not the expected using_item route")

for signature in ("gamemode=spectator", "unless dimension minecraft:overworld",
                  "minecraft:villager,distance=..72", "minecraft:iron_golem,distance=..72",
                  "rpg.advent,distance=..72", "rpg.rite.anchor,distance=..72",
                  "72 格内无村民与铁傀儡", "function rpg:campaign/beelzebub/start"):
    if signature not in chapter_use:
        errors.append("chapter site gate missing: " + signature)
if chapter_use.rfind("function rpg:campaign/beelzebub/start") < chapter_use.find("minecraft:iron_golem,distance=..72"):
    errors.append("chapter start is reachable before settlement validation")
if "37×65 格" not in source("campaign/beelzebub/scene/preflight.mcfunction"):
    errors.append("roster terrain failure lacks an actionable footprint hint")

for signature in ("rpg.end.controller", "已有七柱回廊正在运行",
                  "rpg.ch1.controller", "第一章调查尚未结束", "function rpg:endless/start"):
    if signature not in endless_use:
        errors.append("endless use gate missing: " + signature)

give_items = source("command/give/item.mcfunction")
for phrase in ("驱净空缺者", "更长的线索", "证得任一柱真名后", "会有人来找你"):
    if give_items.count(phrase) != 1:
        errors.append("handbook entry-page phrase missing or duplicated: " + phrase)

# 两个入口都靠事件与进度触发；任何 tick 接线都意味着设计退化成了轮询。
for rel in ("command/tick.mcfunction", "command/tick_end.mcfunction"):
    if "rpg:entry/" in source(rel):
        errors.append("entry point must not add a per-tick traversal: " + rel)

if errors:
    print("entry point audit failed (%d):" % len(errors))
    for error in errors:
        print("  - " + error)
    raise SystemExit(1)
print("entry point audit: chapter invitation 1x / true-name landings 7x -> token give 1x / active-item gates wired")
