# -*- coding: utf-8 -*-
"""Structural regression audit for the persistent 35-member Goetic legions."""

import io
import json
import os
import re
import sys


ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(ROOT, "data/rpg/function")
LOOT = os.path.join(ROOT, "data/rpg/loot_table/minion")
problems = []

LORDS = [
    ("lucifer", ["bael", "agares", "vassago", "samigina", "marbas"]),
    ("leviathan", ["valefor", "amon", "barbatos", "paimon", "buer"]),
    ("abaddon", ["gusion", "sitri", "beleth", "leraje", "eligos"]),
    ("beelzebub", ["zepar", "botis", "bathin", "sallos", "purson"]),
    ("samael", ["marax", "ipos", "aim", "naberius", "glasya_labolas"]),
    ("belial", ["bune", "ronove", "berith", "astaroth", "forneus"]),
    ("mammon", ["foras", "asmoday", "gaap", "furfur", "marchosias"]),
]
ROLE_ENTITIES = ("vindicator", "pillager", "evoker", "illusioner", "vindicator")


def read(rel):
    path = os.path.join(FUNC, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        problems.append("missing function: " + rel)
        return ""
    with io.open(path, encoding="utf-8") as handle:
        return handle.read()


score = read("command/soreboard.mcfunction")
for objective in ("rpg_mn_lord", "rpg_mn_role", "rpg_mn_cd", "rpg_mn_tick", "rpg_mn_slot"):
    if "scoreboard objectives add %s dummy" % objective not in score:
        problems.append("missing objective: " + objective)
if "rpg_mn_life" in score:
    problems.append("obsolete lifetime objective remains")

if "function rpg:minion/tick" not in read("exorcism.mcfunction"):
    problems.append("missing guarded ecosystem tick hook")
if "rpg:minion/summon_try" in read("taint/cast.mcfunction"):
    problems.append("ordinary cast still summons minions; phase two must own the hook")
pressure = read("inquest/phase2/pressure.mcfunction")
if "function rpg:minion/phase2_summon" not in pressure:
    problems.append("phase-two pressure summon hook missing")

phase = read("minion/phase2_summon.mcfunction")
if "rpg_mn_slot matches 6.." not in phase:
    problems.append("phase-two five-role rotation missing")

summon_count = 0
ability_count = 0
for lord_index, (lord, spirits) in enumerate(LORDS, 1):
    all_fn = read("minion/summon/%s/all.mcfunction" % lord)
    if all_fn.count("function rpg:minion/summon/%s/" % lord) != 5:
        problems.append("%s all-command does not expose five spirits" % lord)
    for role_index, spirit in enumerate(spirits, 1):
        summon = read("minion/summon/%s/%s.mcfunction" % (lord, spirit))
        summon_lines = [line for line in summon.splitlines() if line.startswith("summon minecraft:")]
        if len(summon_lines) != 1 or not summon_lines[0].startswith("summon minecraft:%s " % ROLE_ENTITIES[role_index - 1]):
            problems.append("%s/%s must summon its role-specific illager" % (lord, spirit))
        else:
            summon_count += 1
        if "PersistenceRequired:1b" not in summon or "rpg_mn_life" in summon:
            problems.append("%s/%s is not independently persistent" % (lord, spirit))
        if role_index == 3 and "NoAI:1b" not in summon:
            problems.append("%s ritualist can cast uncontrolled vanilla evoker spells" % lord)
        if '"rpg.demon"' in "\n".join(summon_lines):
            problems.append("%s/%s reuses boss-only tag" % (lord, spirit))
        if "rpg_mn_lord %d" % lord_index not in summon or "rpg_mn_role %d" % role_index not in summon:
            problems.append("%s/%s lacks identity scores" % (lord, spirit))
        if "DeathLootTable:\"rpg:minion/%s/%s\"" % (lord, spirit) not in summon:
            problems.append("%s/%s lacks unique loot table" % (lord, spirit))

        ability = read("minion/ability/%s_%d.mcfunction" % (lord, role_index))
        if "scoreboard players set @s rpg_mn_cd" not in ability:
            problems.append("%s role %d ability lacks cooldown" % (lord, role_index))
        if role_index in (2, 4, 5) and "gamemode=!spectator,gamemode=!creative" not in ability:
            problems.append("%s role %d player filter incomplete" % (lord, role_index))
        if re.search(r"^damage\s+@[ae]\[", ability, re.M):
            problems.append("%s role %d sends multi-target selector directly to damage" % (lord, role_index))
        if ability:
            ability_count += 1

        loot = os.path.join(LOOT, lord, spirit + ".json")
        try:
            with io.open(loot, encoding="utf-8") as handle:
                data = json.load(handle)
            if len(data.get("pools", [])) != 2:
                problems.append("%s/%s loot lacks lord and role pools" % (lord, spirit))
        except Exception as exc:
            problems.append("%s/%s loot invalid: %s" % (lord, spirit, exc))

        needle = "rpg_mn_lord=%d,rpg_mn_role=%d" % (lord_index, role_index)
        target = "function rpg:minion/summon/%s/%s" % (lord, spirit)
        if needle not in phase or target not in phase:
            problems.append("%s/%s is unreachable from phase two or lacks living-role cap" % (lord, spirit))

tick = read("minion/tick.mcfunction")
beat = read("minion/beat.mcfunction")
entity_tick = read("minion/entity_tick.mcfunction")
if "matches 10.." not in tick or "execute as @e[tag=rpg.demon.minion]" not in beat:
    problems.append("runtime is not ten-tick batched")
if "rpg_mn_life" in entity_tick or "owner" in entity_tick or "fade" in entity_tick:
    problems.append("runtime still couples minions to lifetime or owner")
if "rpg_ex_xp 1" not in read("minion/reward.mcfunction"):
    problems.append("kills do not feed exorcist progression")

adv = os.path.join(ROOT, "data/rpg/advancement/minion/kill.json")
try:
    with io.open(adv, encoding="utf-8") as handle:
        if "rpg.demon.minion" not in json.dumps(json.load(handle)):
            problems.append("kill advancement does not identify minions")
except Exception as exc:
    problems.append("kill advancement invalid: %s" % exc)

if summon_count != 35:
    problems.append("expected 35 manual summons, found %d" % summon_count)
if ability_count != 35:
    problems.append("expected 35 role abilities, found %d" % ability_count)

if problems:
    print("GOETIC LEGION AUDIT: FAIL")
    for problem in problems:
        print(" - " + problem)
    raise SystemExit(1)

print("GOETIC LEGION AUDIT: PASS")
print("  35 unique Goetic minions / 7 lords / 5 persistent roles")
print("  manual all/individual summons and phase-two capped rotation present")
print("  35 cooldown abilities, 35 two-pool loot tables, career reward present")
print("  runtime remains one guarded ten-tick ecology pass")
