# -*- coding: utf-8 -*-
"""Static contract audit for the endless exorcism mode."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DP = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "rpg").resolve()
FUNC = DP / "data" / "rpg" / "function"
CFG = json.loads((ROOT / "_endless_exorcism_config.json").read_text(encoding="utf-8"))
errors: list[str] = []


def source(rel):
    path = FUNC / rel
    if not path.is_file():
        errors.append("missing function: " + rel)
        return ""
    return path.read_text(encoding="utf-8")


if CFG.get("boss_interval") != 5:
    errors.append("boss interval must be 5")
if CFG.get("roster_cycle") != 72:
    errors.append("roster cycle must cover all 72 Goetic spirits")
if len(CFG.get("spawn_offsets", [])) != 5:
    errors.append("five configurable spawn offsets required")
if len({tuple(v) for v in CFG.get("spawn_offsets", [])}) != 5:
    errors.append("spawn offsets must be distinct")

required = [
    "endless/start.mcfunction", "endless/setup.mcfunction", "endless/tick.mcfunction",
    "endless/abort.mcfunction", "endless/cleanup.mcfunction", "endless/join.mcfunction",
    "endless/floor/begin.mcfunction", "endless/floor/clear.mcfunction",
    "endless/boss/dispatch.mcfunction", "endless/enemy/scale.mcfunction",
    "endless/reward/open.mcfunction", "endless/reward/claim.mcfunction",
    "endless/reward/timeout.mcfunction", "endless/reward/close.mcfunction",
    "endless/debug/menu.mcfunction", "endless/member/clear_boons.mcfunction",
    "endless/member/stale_cleanup.mcfunction", "panel/endless.mcfunction",
]
for rel in required:
    source(rel)

tick = source("endless/tick.mcfunction")
for signature in ("rpg_end_id", "rpg_end_idle", "function rpg:endless/state/combat",
                  "function rpg:endless/state/reward", "rpg_end_leave",
                  "rpg.end.member.current", "function rpg:endless/member/stale_cleanup"):
    if signature not in tick:
        errors.append("tick contract missing: " + signature)

begin = source("endless/floor/begin.mcfunction")
for signature in ("%= #five", "#boss rpg_end_tmp 1", "function rpg:endless/boss/dispatch",
                  "function rpg:endless/deck/dispatch", "#spawn rpg_end_tmp 5",
                  "#ordinary rpg_end_tmp -= #skipped rpg_end_tmp"):
    if signature not in begin:
        errors.append("floor routing missing: " + signature)

formations = []
all_names = set()
for floor in range(1, 73):
    body = source(f"endless/deck/{floor}.mcfunction")
    match = re.search(r"^# 第 \d+ 号编队：(.*)$", body, re.MULTILINE)
    if not match:
        errors.append(f"floor {floor} has no formation manifest")
        continue
    names = tuple(part.strip() for part in match.group(1).split("/"))
    if len(names) != 5 or len(set(names)) != 5:
        errors.append(f"floor {floor} formation is not five distinct demons: {names}")
    all_names.update(names)
    formations.append(names)
    summon_lines = [line for line in body.splitlines()
                    if " positioned " in line and " run function rpg:" in line]
    if len(summon_lines) != 5:
        errors.append(f"floor {floor} does not expose five scalable summon slots")
    if body.count("rpg.end.enemy.current") < 5 or "rpg_end_id = @s rpg_end_id" not in body:
        errors.append(f"floor {floor} lacks immediate ID-owned enemy capture")
if len(set(formations)) != 72:
    errors.append("the 72-floor deck contains repeated formations")
if len(all_names) != 72:
    errors.append(f"deck exposes {len(all_names)} unique names instead of all 72 pillars")

wandering = list((FUNC / "endless" / "summon").glob("*.mcfunction"))
if len(wandering) != 37:
    errors.append(f"expected 37 roaming-spirit summons, found {len(wandering)}")
for path in wandering:
    body = path.read_text(encoding="utf-8")
    for signature in ("rpg.demon.minion.roaming", "rpg_mn_lord", "rpg_mn_role",
                      "PersistenceRequired:1b", 'DeathLootTable:"minecraft:empty"'):
        if signature not in body:
            errors.append(f"roaming spirit {path.name} lacks {signature}")

boss_dispatch = source("endless/boss/dispatch.mcfunction")
for lord in range(1, 8):
    if f"function rpg:endless/boss/{lord}" not in boss_dispatch:
        errors.append(f"boss rotation omits lord {lord}")
    body = source(f"endless/boss/{lord}.mcfunction")
    for signature in (f"function rpg:taint/lord{lord}", "rpg.end.boss", "rpg_end_id = @s rpg_end_id"):
        if signature not in body:
            errors.append(f"boss {lord} ownership/scaling missing: {signature}")

scale = source("endless/enemy/scale.mcfunction")
for tier in range(1, 21):
    if f"#tier rpg_end_tmp matches {tier}" not in scale:
        errors.append(f"difficulty tier {tier} missing")
for role in range(1, 6):
    if f"rpg_mn_role matches {role}" not in scale:
        errors.append(f"minion role {role} lacks scaling")

reward_open = source("endless/reward/open.mcfunction")
for value, label in ((1, "圣恩"), (2, "断罪"), (3, "遗珍")):
    if f"/trigger rpg_end_pick set {value}" not in reward_open or label not in reward_open:
        errors.append(f"reward choice missing: {label}")
claim = source("endless/reward/claim.mcfunction")
for rel in ("reward/grace", "reward/judgment", "reward/loot_dispatch", "reward/boss_bonus"):
    if f"function rpg:endless/{rel}" not in claim:
        errors.append("claim route missing: " + rel)
if "rpg_end_claim matches 1.. run return 0" not in claim:
    errors.append("reward claim is not idempotent")
if "rpg_end_pick 3" not in source("endless/reward/timeout.mcfunction"):
    errors.append("reward timeout does not fall back to loot")

# Boss floors do not consume formation slots. The first 72 ordinary battles
# therefore span total floors 1..90 and must expose deck indices 1..72 once.
reachable = [floor - floor // CFG["boss_interval"] for floor in range(1, 91)
             if floor % CFG["boss_interval"]]
if reachable != list(range(1, 73)):
    errors.append("ordinary-floor ordinal does not cover deck 1..72 before repeating")

loot_signatures = ("gold_ingot", "iron_block", "diamond", "echo_shard",
                   "netherite_scrap", "netherite_scrap 2", "netherite_ingot")
for index, signature in enumerate(loot_signatures, 1):
    if signature not in source(f"endless/reward/loot/{index}.mcfunction"):
        errors.append(f"reward tier {index} lacks its richer material: {signature}")

scoreboard = source("command/soreboard.mcfunction")
for objective in ("rpg_end_id", "rpg_end_floor", "rpg_end_state", "rpg_end_pick",
                  "rpg_end_leave", "rpg_end_best", "rpg_end_power", "rpg_end_vital"):
    if f"scoreboard objectives add {objective} " not in scoreboard:
        errors.append("objective missing: " + objective)
if "bossbar add rpg:endless" not in source("command/bossbar.mcfunction"):
    errors.append("endless bossbar is not loaded")
if "function rpg:endless/tick" not in source("exorcism.mcfunction"):
    errors.append("endless tick is not wired")
if "function rpg:endless/member/stale_cleanup" not in source("exorcism.mcfunction"):
    errors.append("offline stale members are not cleaned when no controller exists")
if "function rpg:panel/endless" not in source("panel/tick.mcfunction") or "[无尽副本]" not in source("panel/open.mcfunction"):
    errors.append("player panel integration missing")
panel_tick = source("panel/tick.mcfunction")
panel_endless = source("panel/endless.mcfunction")
for value, route in ((16, "rpg:endless/start"), (17, "rpg:endless/join")):
    if f"/trigger rpg_panel set {value}" not in panel_endless or f"rpg_panel matches {value} run function {route}" not in panel_tick:
        errors.append(f"ordinary-player trigger route missing: {route}")
if "/function rpg:endless/start" in panel_endless or "/function rpg:endless/join" in panel_endless:
    errors.append("ordinary player panel still exposes permission-gated /function buttons")
floor_begin = source("endless/floor/begin.mcfunction")
if "store result bossbar rpg:endless max run scoreboard players get #spawn" not in floor_begin:
    errors.append("ordinary-floor bossbar maximum is not derived from actual spawn count")
if "bossbar set rpg:endless max 1" not in floor_begin:
    errors.append("boss-floor bossbar maximum is not one")
if "剩余" not in source("endless/state/combat.mcfunction"):
    errors.append("combat bossbar has no remaining-enemy objective")

clear_boons = source("endless/member/clear_boons.mcfunction")
apply_boons = source("endless/member/apply_boons.mcfunction")
stale_cleanup = source("endless/member/stale_cleanup.mcfunction")
for modifier in ("rpg:endless/vital_health", "rpg:endless/vital_armor",
                 "rpg:endless/vital_anchor", "rpg:endless/power_damage",
                 "rpg:endless/power_speed"):
    if f"modifier remove {modifier}" not in clear_boons:
        errors.append("reversible boon cleanup missing: " + modifier)
if "modifier add rpg:endless/" not in apply_boons or "effect give" in apply_boons:
    errors.append("floor boons are not implemented as reversible modifiers")
for rel in ("endless/leave.mcfunction", "endless/cleanup.mcfunction",
            "endless/start.mcfunction", "endless/join.mcfunction"):
    body = source(rel)
    if "clear_boons" not in body and "stale_cleanup" not in body:
        errors.append(f"boon cleanup missing from {rel}")
for token in ("tag @s remove rpg.end.member", "tag @s remove rpg.end.member.current",
              "rpg_end_claim 1", "rpg_end_power 0", "rpg_end_vital 0"):
    if token not in stale_cleanup:
        errors.append("stale member recovery missing: " + token)
for rel in ("endless/state/reward.mcfunction", "endless/reward/timeout.mcfunction",
            "endless/floor/clear.mcfunction"):
    body = source(rel)
    if "tag=rpg.end.member," in body or "tag=rpg.end.member]" in body:
        errors.append(f"stale member selector can block or receive rewards in {rel}")
for lord in range(1, 8):
    boss_line = next((line for line in source(f"endless/boss/{lord}.mcfunction").splitlines() if "[领主降临]" in line), "")
    # Prefix may be bold; the following proper-name component must not be.
    if not re.search(r'\[领主降临\].*?"bold":true.*?\{"text":"[^"]+ ","color":"#[0-9A-Fa-f]{6}","bold":false', boss_line):
        errors.append(f"boss {lord} proper name remains bold")
if "rpg.end.controller" not in source("campaign/beelzebub/start.mcfunction"):
    errors.append("campaign/endless mutual exclusion missing")

for path in (FUNC / "endless").rglob("*.mcfunction"):
    body = path.read_text(encoding="utf-8")
    if "actionbar" in body:
        errors.append(f"direct actionbar writer in {path.relative_to(FUNC)}")

pack_cfg = DP / "data" / "rpg" / "endless_config.json"
if not pack_cfg.is_file() or json.loads(pack_cfg.read_text(encoding="utf-8")) != CFG:
    errors.append("pack config snapshot missing or stale")

if errors:
    print(f"ENDLESS EXORCISM AUDIT FAILED ({len(errors)})")
    for error in errors:
        print("- " + error)
    raise SystemExit(1)
print("ENDLESS EXORCISM AUDIT: PASS")
print("  all 72 Goetic spirits / 72 distinct formations / 7-lord rotation / 20 difficulty tiers")
print("  per-player grace, judgment and loot rewards / timeout recovery / ID ownership")
