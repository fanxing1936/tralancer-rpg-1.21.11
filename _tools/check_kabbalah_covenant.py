# -*- coding: utf-8 -*-
"""Audit Blood Covenant and the ten offering foundation.

The Old/New Covenant reward chain is audited separately after its late build
stage by check_divine_covenants.py.
"""

import io
import json
import os
import re
import sys


ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(ROOT, "data/rpg/function")
ADV = os.path.join(ROOT, "data/rpg/advancement")
problems = []

ROWS = [
    (1, "kether", "white_dye"), (2, "chokmah", "light_gray_dye"),
    (3, "binah", "black_dye"), (4, "chesed", "blue_dye"),
    (5, "geburah", "red_dye"), (6, "tiphareth", "yellow_dye"),
    (7, "netzach", "green_dye"), (8, "hod", "orange_dye"),
    (9, "yesod", "purple_dye"), (10, "malkuth", "brown_dye"),
]


def read(rel):
    path = os.path.join(FUNC, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        problems.append("missing function: " + rel)
        return ""
    with io.open(path, encoding="utf-8") as handle:
        return handle.read()


score = read("command/soreboard.mcfunction")
for objective in ("rpg_lt_fill", "rpg_lt_usecd", "rpg_lt_covenant", "rpg_lt_bless"):
    if "scoreboard objectives add %s dummy" % objective not in score:
        problems.append("missing objective: " + objective)

runtime = read("exorcism.mcfunction")
if "@a[scores={rpg_lt_usecd=1..}]" not in runtime:
    problems.append("input cooldown does not decay")

adv_path = os.path.join(ADV, "ritual", "life_tree", "use.json")
try:
    with io.open(adv_path, encoding="utf-8") as handle:
        adv = json.load(handle)
    dumped = json.dumps(adv)
    if "minecraft:using_item" not in dumped or "rpg_kabbalah_use:1b" not in dumped or "rpg:ritual/life_tree/input" not in dumped:
        problems.append("using-item advancement is incomplete")
except Exception as exc:
    problems.append("use advancement invalid: %s" % exc)

catalog = read("command/give/extra.mcfunction")
if catalog.count("rpg_kabbalah_contract:1b") != 1 or "minecraft:flower_banner_pattern" not in catalog or "卡巴拉血契" not in catalog:
    problems.append("catalog lacks exactly one flower-pattern Blood Covenant")
if catalog.count("rpg_sephirah:") != 10:
    problems.append("catalog must expose exactly ten Sephirah items")
if '"text":"[秘仪]"' not in catalog or '"text":"卡巴拉血契","color":"#FFFFFF","bold":false' not in catalog:
    problems.append("Blood Covenant name does not use bold prefix + plain proper name")
if any(dark in catalog for dark in ("#202028", "#7A4630")):
    problems.append("particle-only dark Sephirah colours leaked into item text")

all_give = read("ritual/life_tree/give/all.mcfunction")
if (all_give.count("rpg_kabbalah_contract:1b") != 1 or
        all_give.count("rpg_sephirah:") != 10 or
        all_give.count("rpg_true_cross:1b") != 1):
    problems.append("direct give/all does not contain the 12-piece ritual kit")
if "『旧约』" not in all_give or "十源质归位后，立下『新约』" in all_give:
    problems.append("Blood Covenant lore still describes the retired direct-New reward")

input_fn = read("ritual/life_tree/input.mcfunction")
if "flower_banner_pattern" not in input_fn or "function rpg:ritual/life_tree/place" not in input_fn:
    problems.append("Blood Covenant does not unfold the tree")
if "tag=!rpg.lt.complete" not in input_fn:
    problems.append("completed trees still accept offerings")

for n, key, dye in ROWS:
    if "minecraft:%s[minecraft:custom_data~{rpg_sephirah:%db}]" % (dye, n) not in input_fn:
        problems.append("input route missing for %s" % key)
    offer = read("ritual/life_tree/offer/%d.mcfunction" % n)
    checks = (
        "tag @s add rpg.lt.%s" % key,
        "scoreboard players add @s rpg_lt_fill 1",
        "clear @a[tag=rpg.kabbalah.user",
        "minecraft:%s[minecraft:custom_data~{rpg_sephirah:%db}] 1" % (dye, n),
        "summon minecraft:item_display",
        "rpg.ritual.life_tree.prop.%s" % key,
        "rpg_lt_fill matches 10..",
    )
    for needle in checks:
        if needle not in offer:
            problems.append("%s offering lacks: %s" % (key, needle))
    if offer.count("run return 0") != 1:
        problems.append("%s duplicate protection malformed" % key)

draw = read("ritual/life_tree/draw.mcfunction")
if draw.count("# FILLED ") != 10 or draw.count("tag=rpg.lt.") != 20:
    problems.append("ten filled-node highlights are incomplete")

place = read("ritual/life_tree/place.mcfunction")
if "rpg_lt_fill 0" not in place:
    problems.append("new tree does not initialise offering progress")

complete = read("ritual/life_tree/complete.mcfunction")
if "tag @s add rpg.lt.complete" not in complete:
    problems.append("ten-node completion does not close the offering stage")
if "give_old_covenant" not in complete or "give_new_covenant" in complete:
    problems.append("ten-node completion must award Old Covenant before Daath")

clear = read("ritual/life_tree/clear.mcfunction")
clear_all = read("ritual/life_tree/clear_all.mcfunction")
if "type=minecraft:item_display,tag=rpg.ritual.life_tree.prop,distance=..8" not in clear:
    problems.append("local clear leaks dye displays")
if "kill @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.prop]" not in clear_all:
    problems.append("global clear leaks dye displays")

if re.search(r"^damage\s+@[ae]\[", "\n".join((input_fn, complete)), re.M):
    problems.append("new system contains unsafe multi-target damage")

if problems:
    print("KABBALAH COVENANT AUDIT: FAIL")
    for problem in problems:
        print(" - " + problem)
    raise SystemExit(1)

print("KABBALAH COVENANT AUDIT: PASS")
print("  flower banner-pattern Blood Covenant + 10 legible dye offerings + True Cross")
print("  position-aware placement, duplicate/wrong-node safety and 10 ground displays")
print("  completion handoff is closed for the divine-covenant reward stage")
