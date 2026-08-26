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
ROLE_COOLDOWNS = (110, 85, 125, 100, 75)
SKILL_NAMES = [
    ["王冠护持", "罪痕标定", "晨星赐福", "失坠敕令", "王座裁落"],
    ["妒潮护幕", "寒潮猎印", "回潮再生", "海渊重压", "沉锚碾落"],
    ["死寂护幕", "疫矢猎印", "灵魂归仓", "深渊低语", "刈魂"],
    ["腐宴护壳", "饥印", "吞食反哺", "蝇幕蚀志", "饥啮"],
    ["怒血共鸣", "血猎标记", "狂血灌注", "死亡低语", "怒斩"],
    ["紫宴护幕", "魅视缚足", "献身回流", "感官倒悬", "强制朝拜"],
    ["金契护体", "债印", "复利回偿", "重税", "一次结清"],
]


def read(rel):
    path = os.path.join(FUNC, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        problems.append("missing function: " + rel)
        return ""
    with io.open(path, encoding="utf-8") as handle:
        return handle.read()


def particle_budget(data):
    total = 0
    for line in data.splitlines():
        if "particle " not in line:
            continue
        match = re.search(r"\s(\d+)(?:\s+(?:force|normal))?$", line)
        if not match:
            problems.append("cannot statically budget particle line: " + line)
            continue
        total += int(match.group(1))
    return total


score = read("command/soreboard.mcfunction")
for objective in ("rpg_mn_lord", "rpg_mn_role", "rpg_mn_cd", "rpg_mn_tick", "rpg_mn_slot", "rpg_mn_owner", "rpg_mn_cast"):
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
for token in ("rpg.rite.anchor.current", "rpg.demon.minion.owned", "rpg_mn_owner =", "rpg_rite_id"):
    if token not in phase:
        problems.append("phase-two exact rite ownership missing: " + token)
if "distance=..36" in phase:
    problems.append("phase-two duplicate guard still uses the obsolete 36-block approximation")

summon_count = 0
ability_count = 0
seen_skills = set()
initial_cooldowns = dict((role, set()) for role in range(1, 6))
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
        for token in ("rpg_mn_owner 0", "tag=rpg.rite.anchor", "rpg_mn_owner = @s rpg_rite_id", "tag=rpg.ch1.rite", "rpg_ch1_id = @s rpg_ch1_id", "add rpg.ch1.minion", "rpg_mn_cast 0"):
            if token not in summon:
                problems.append("%s/%s ownership/campaign inheritance missing: %s" % (lord, spirit, token))
        initial = re.search(r"rpg_mn_cd (\d+)", summon)
        if not initial:
            problems.append("%s/%s lacks deterministic initial cooldown" % (lord, spirit))
        else:
            initial_cooldowns[role_index].add(int(initial.group(1)))
        if "DeathLootTable:\"rpg:minion/%s/%s\"" % (lord, spirit) not in summon:
            problems.append("%s/%s lacks unique loot table" % (lord, spirit))

        ability = read("minion/ability/%s_%d.mcfunction" % (lord, role_index))
        resolution = read("minion/ability/resolve/%s_%d.mcfunction" % (lord, role_index))
        combined = ability + "\n" + resolution
        skill = SKILL_NAMES[lord_index - 1][role_index - 1]
        if skill not in ability:
            problems.append("%s/%s lacks its unique named skill %s" % (lord, spirit, skill))
        elif skill in seen_skills:
            problems.append("duplicate skill identity: " + skill)
        else:
            seen_skills.add(skill)
        if "scoreboard players set @s rpg_mn_cd" not in ability:
            problems.append("%s role %d ability lacks cooldown" % (lord, role_index))
        expected_cd = ROLE_COOLDOWNS[role_index - 1] + (lord_index - 1) * 4
        if "scoreboard players set @s rpg_mn_cd %d" % expected_cd not in ability:
            problems.append("%s role %d cooldown is not desynchronised as specified" % (lord, role_index))
        if "scoreboard players add #casts rpg_mn_tick 1" not in ability:
            problems.append("%s role %d bypasses the per-beat cast budget" % (lord, role_index))
        expected_windup = 10 if role_index in (1, 5) else 20
        if "scoreboard players set @s rpg_mn_cast %d" % expected_windup not in ability or "tag @s add rpg.demon.minion.casting" not in ability:
            problems.append("%s role %d lacks its 10/20-tick windup state" % (lord, role_index))
        if "tag @s remove rpg.demon.minion.casting" not in resolution or "scoreboard players set @s rpg_mn_cast 0" not in resolution:
            problems.append("%s role %d resolution does not close the cast state" % (lord, role_index))
        if " run damage @s " in ability:
            problems.append("%s role %d still settles damage during the telegraph" % (lord, role_index))
        for line in ability.splitlines():
            if "effect give" in line and "minecraft:glowing 1 0 true" not in line:
                problems.append("%s role %d applies non-telegraph effects before resolution" % (lord, role_index))
        if "[罪仆术式] " not in ability or ability.count("playsound ") < 2:
            problems.append("%s role %d lacks readable audiovisual telegraph" % (lord, role_index))
        windup_particles, resolve_particles = particle_budget(ability), particle_budget(resolution)
        if windup_particles > 12 or resolve_particles > 12 or windup_particles + resolve_particles > 28:
            problems.append("%s role %d particle budget exceeds 12/pulse or 28/cast: %d+%d" % (lord, role_index, windup_particles, resolve_particles))
        if role_index in (2, 4, 5) and "gamemode=!spectator,gamemode=!creative" not in combined:
            problems.append("%s role %d player filter incomplete" % (lord, role_index))
        if role_index in (2, 4, 5) and ("rpg.demon.minion.caster" not in resolution or " run damage @s " not in resolution):
            problems.append("%s role %d damage lacks exact caster attribution" % (lord, role_index))
        if role_index == 2 and "sort=nearest,limit=1" not in combined:
            problems.append("%s hunter is not a focused single-target skill" % lord)
        if role_index == 4 and "execute as @a[distance=..8" not in resolution:
            problems.append("%s hexer is not a bounded AOE skill" % lord)
        if role_index in (1, 3) and "scores={rpg_mn_lord=%d}" % lord_index not in combined:
            problems.append("%s support skill can affect another lord's cohort" % lord)
        if re.search(r"^damage\s+@[ae]\[", combined, re.M):
            problems.append("%s role %d sends multi-target selector directly to damage" % (lord, role_index))
        if "@p" in combined:
            problems.append("%s role %d uses multiplayer-unsafe nearest-player shorthand" % (lord, role_index))
        for selector in re.findall(r"@a\[[^\]]*\]", combined):
            if "distance=" not in selector:
                problems.append("%s role %d has unbounded player selector: %s" % (lord, role_index, selector))
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
if "scoreboard players set #casts rpg_mn_tick 0" not in beat or "if score #casts rpg_mn_tick matches ..1" not in entity_tick:
    problems.append("runtime lacks the two-casts-per-beat performance guard")
for token in ("rpg_mn_cast=1..", "rpg_mn_cast=..0", "function rpg:minion/resolve_dispatch"):
    if token not in entity_tick:
        problems.append("runtime two-stage cast transition missing: " + token)
if "rpg_mn_role=3}] unless entity @a[distance=..14" not in entity_tick or "unless entity @s[scores={rpg_mn_role=3}] unless entity @a[distance=..12" not in entity_tick:
    problems.append("ritualist 14-block support trigger is not separated from the 12-block combat trigger")
resolve_dispatch = read("minion/resolve_dispatch.mcfunction")
if resolve_dispatch.count("function rpg:minion/ability/resolve/") != 35:
    problems.append("resolve dispatch does not expose all 35 delayed abilities")
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
if len(seen_skills) != 35:
    problems.append("expected 35 unique named skills, found %d" % len(seen_skills))
for role_index, values in initial_cooldowns.items():
    if len(values) != 7:
        problems.append("role %d initial casts are not staggered across seven cohorts" % role_index)

if problems:
    print("GOETIC LEGION AUDIT: FAIL")
    for problem in problems:
        print(" - " + problem)
    raise SystemExit(1)

print("GOETIC LEGION AUDIT: PASS")
print("  35 unique Goetic minions / 7 lords / 5 persistent roles")
print("  manual all/individual summons and phase-two capped rotation present")
print("  35 named audiovisual abilities, 35 two-pool loot tables, career reward present")
print("  one ten-tick ecology pass / two casts per beat / 10-20 tick telegraph then resolve")
print("  exact rite ownership / campaign cleanup inheritance / <=12 particles per pulse")
