#!/usr/bin/env python3
"""Static acceptance gate for Chapter I campaign ownership and progression."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

from beelzebub_campaign_config import load_config

root = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
fun = root / "data" / "rpg" / "function"
errors: list[str] = []
CONFIG = load_config(pack_root=root)
RUNTIME = CONFIG["runtime"]
RECOVERY = RUNTIME["recovery"]
BOSS = CONFIG["actors"]["boss"]
MINIONS = CONFIG["actors"]["minions"]


def read(rel: str) -> str:
    p = fun / rel
    if not p.is_file(): errors.append("missing function: " + rel); return ""
    return p.read_text(encoding="utf-8")


required = [
    "campaign/beelzebub/start.mcfunction", "campaign/beelzebub/tick.mcfunction",
    "campaign/beelzebub/menu.mcfunction", "campaign/beelzebub/join.mcfunction",
    "campaign/beelzebub/rescue.mcfunction", "campaign/beelzebub/abort.mcfunction",
    "campaign/beelzebub/finish.mcfunction", "campaign/beelzebub/complete_player.mcfunction",
    "campaign/beelzebub/next_hunt.mcfunction", "campaign/beelzebub/recover_boss.mcfunction",
    "campaign/beelzebub/recover_minions.mcfunction", "campaign/beelzebub/claim_rite.mcfunction",
    "campaign/beelzebub/give/pending_page.mcfunction", "campaign/beelzebub/orphan_scrub.mcfunction",
    "campaign/beelzebub/verdict/reject.mcfunction", "campaign/beelzebub/career_confirm.mcfunction",
    "campaign/beelzebub/recap/menu.mcfunction", "campaign/beelzebub/recap/anomaly.mcfunction",
    "campaign/beelzebub/recap/minions.mcfunction", "campaign/beelzebub/recap/area.mcfunction",
    "campaign/beelzebub/recap/hypothesis.mcfunction", "campaign/beelzebub/recap/prep.mcfunction",
    "campaign/beelzebub/boss/begin.mcfunction", "campaign/beelzebub/puzzle/refresh_enemies.mcfunction",
    "campaign/beelzebub/route/activate.mcfunction", "campaign/beelzebub/route/wrong.mcfunction",
    "campaign/beelzebub/hypothesis_board/activate.mcfunction", "campaign/beelzebub/hypothesis_board/wrong.mcfunction",
    "campaign/beelzebub/calibration/activate.mcfunction", "campaign/beelzebub/calibration/wrong.mcfunction",
]
required += [f"campaign/beelzebub/stage/{n}_{suffix}.mcfunction" for n in range(11) for suffix in ("enter", "tick")]
for rel in required: read(rel)

# Schema and one guarded runtime entry.
sore = read("command/soreboard.mcfunction")
objectives = ("rpg_ch1_id", "rpg_ch1_stage", "rpg_ch1_sub", "rpg_ch1_time", "rpg_ch1_obj",
              "rpg_ch1_choice", "rpg_ch1_done", "rpg_ch1_next", "rpg_ch1_replay",
              "rpg_ch1_reward", "rpg_ch1_fail", "rpg_ch1_seen", "rpg_ch1_safe", "rpg_ch1_yaw", "rpg_ch1_guard",
              "rpg_ch1_roster", "rpg_ch1_empty", "rpg_ch1_hp", "rpg_ch1_rescue", "rpg_ch1_verdict", "rpg_ch1_session")
for obj in objectives:
    if sore.count(f"scoreboard objectives add {obj} dummy") != 1: errors.append("objective missing or duplicated: " + obj)
tick_root = read("exorcism.mcfunction")
hook = "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] at @s run function rpg:campaign/beelzebub/tick"
if tick_root.count(hook) != 1: errors.append("campaign root hook must be unique and controller-guarded")

# Explicit membership: nearby strangers are never silently accepted.
start_gate = read("campaign/beelzebub/start.mcfunction")
start = start_gate + "\n" + read("campaign/beelzebub/start_pass.mcfunction")
join = read("campaign/beelzebub/join.mcfunction")
tick = read("campaign/beelzebub/tick.mcfunction")
for token in ("#next rpg_ch1_id", "rpg.ch1.controller", "rpg.ch1.anchor", "rpg.ch1.accepted", "rpg.ch1.member", "scoreboard players operation @s rpg_ch1_id", "random value 1..2147483647", "rpg_ch1_session"):
    if token not in start: errors.append("start lacks ownership token: " + token)
if re.search(r"tag @a\[distance=.*\] add rpg\.ch1\.(accepted|member)", start): errors.append("start silently absorbs nearby players")
preflight = read("campaign/beelzebub/scene/preflight.mcfunction")
safe = RUNTIME["safe_plane"]
safe_samples = len(safe["ground_sample_x"]) * len(safe["ground_sample_z"]) + len(safe["tall_sample_x"]) * len(safe["tall_sample_z"])
if preflight.count("scoreboard players add @s rpg_ch1_safe 1") != safe_samples or f"rpg_ch1_safe matches {safe_samples}" not in preflight:
    errors.append("63+9 startup safety samples incomplete")
for token in (f"unless dimension {RUNTIME['dimension']}", f"type=minecraft:villager,distance=..{RUNTIME['scene_radius']}", f"tag=rpg.advent,distance=..{RUNTIME['scene_radius']}", f"tag=rpg.rite.anchor,distance=..{RUNTIME['scene_radius']}"):
    if token not in start_gate: errors.append("preflight gate missing: " + token)
if "rotated 0 0" not in start_gate or "rotated 90 0" not in start_gate or "rotated -90 0" not in start_gate or "rotated 180 0" not in start_gate:
    errors.append("preflight orientation is not snapped to four cardinal directions")
for token in ("tag @s add rpg.ch1.accepted", "tag @s add rpg.ch1.member", "rpg_ch1_id = @e", "rpg_ch1_session = @e", "rpg_ch1_stage=3.."):
    if token not in join: errors.append("join gate missing: " + token)
for token in ("rpg_ch1_roster 1", "scoreboard players add @s rpg_ch1_roster 1",
              f"scores={{rpg_ch1_roster={RUNTIME['max_party_size']}..}}] run return"):
    if token not in start + join: errors.append("fixed roster accounting missing: " + token)
if f"@a[tag=rpg.ch1.member,distance=..{RUNTIME['active_radius']}" not in tick or "if score @s rpg_ch1_id =" not in tick:
    errors.append("presence set is not member+ID scoped")
if f"tag @a[distance=..{RUNTIME['active_radius']}" in tick: errors.append("tick absorbs unregistered bystanders")
if "unless entity @a[tag=rpg.ch1.current" not in tick: errors.append("chapter pause guard missing")
if "scoreboard players add @s rpg_fall 1" not in tick: errors.append("paused boss lifetime is not restored")

panel = read("panel/tick.mcfunction")
for value, target in ((11, "menu"), (12, "start"), (13, "rescue"), (14, "join"), (15, "next_hunt")):
    if f"rpg_panel matches {value} run function rpg:campaign/beelzebub/{target}" not in panel: errors.append(f"panel dispatch missing: {value}->{target}")
if panel.count("campaign/beelzebub/orphan_scrub") != 3 or "unless score @s rpg_ch1_id =" not in panel or "unless score @s rpg_ch1_session =" not in panel:
    errors.append("offline-return/orphan scrub hooks are incomplete")

# Eleven reachable story states. Stage 7 exits through verdict, every other
# nonterminal stage must have an explicit advance path.
for n in range(11):
    enter, st = read(f"campaign/beelzebub/stage/{n}_enter.mcfunction"), read(f"campaign/beelzebub/stage/{n}_tick.mcfunction")
    if not enter.strip(): errors.append(f"empty stage enter: {n}")
    if n not in (7, 10) and "function rpg:campaign/beelzebub/advance" not in st: errors.append(f"stage {n} has no forward edge")

# Narrative investigation is a playable inference chain, not three labels that
# disclose the answer.  A timed prologue establishes role and method; four
# checkpoints preserve a player-repeatable case summary across combat breaks.
stage0_tick = read("campaign/beelzebub/stage/0_tick.mcfunction")
for token in ("征调令", "粮册写着满仓", "司钟人三天前就死了", "先记录事实，再比较解释", "rpg_ch1_time matches 400.."):
    if token not in read("campaign/beelzebub/stage/0_enter.mcfunction") + stage0_tick:
        errors.append("playable prologue missing: " + token)
menu = read("campaign/beelzebub/menu.mcfunction")
menu_recap = read("campaign/beelzebub/recap/menu.mcfunction")
if "function rpg:campaign/beelzebub/recap/menu" not in menu:
    errors.append("chapter menu has no persistent case recap")
for stage_range in ("0..1", "2..3", "4", "5", "6", "7", "8..9", "10"):
    if f"rpg_ch1_stage={stage_range}" not in menu_recap:
        errors.append("case recap misses stage range: " + stage_range)
recap_expectations = {
    "anomaly": ("案情复盘", "◆ 已知", "◇ 矛盾", "→ 下一步", "疫病", "亡灵"),
    "minions": ("五种职责", "卡西安签章", "桌子的主人"),
    "area": ("案情复盘", "◆ 已知", "◇ 矛盾", "→ 下一步", "第七粮仓", "卡西安："),
    "hypothesis": ("案情复盘", "◆ 已知", "◇ 矛盾", "→ 下一步", "假说修正", "弱点假说"),
    "prep": ("对象", "弱点", "风险", "见证人印"),
}
for name, tokens in recap_expectations.items():
    body = read(f"campaign/beelzebub/recap/{name}.mcfunction")
    for token in tokens:
        if token not in body: errors.append(f"{name} recap missing: {token}")
for stage, tag in ((1, "anomaly"), (3, "minions"), (4, "area"), (5, "hypothesis"), (6, "prep")):
    body = read(f"campaign/beelzebub/stage/{stage}_tick.mcfunction")
    if f"recap/{tag}" not in body or f"rpg.ch1.recap.{tag}" not in body:
        errors.append(f"stage {stage} can skip its narrative recap")
stage1_points = "\n".join(read(f"campaign/beelzebub/point/anom{n}.mcfunction") for n in range(1, 4))
for token in ("观察：", "更像命令，不像预言", "先问它们替谁带路"):
    if token not in stage1_points: errors.append("first misdirection/cross-check missing: " + token)
stage4_points = "\n".join(read(f"campaign/beelzebub/point/trail{n}.mcfunction") for n in range(1, 5))
for token in ("口粮", "尸体", "早于卡西安接任", "三条路线"):
    if token not in stage4_points + read("campaign/beelzebub/recap/area.mcfunction"):
        errors.append("second misdirection/cross-check missing: " + token)
if "rpg_ch1_stage 8" not in "\n".join(read(f"campaign/beelzebub/verdict/{k}.mcfunction") for k in ("eliminate", "banish", "seal", "pact")):
    errors.append("verdicts do not enter stage 8")
stage10_enter = read("campaign/beelzebub/stage/10_enter.mcfunction")
stage10_tick = read("campaign/beelzebub/stage/10_tick.mcfunction")
if "complete_player" in stage10_enter: errors.append("terminal state settles before career choice")
for token in ("rpg_ch1_time matches 600..", "tag=!rpg.ch1.career.confirmed", "career_confirm", "rpg_ch1_time 600"):
    if token not in stage10_tick: errors.append("career-gated terminal flow missing: " + token)
if re.search(r"rpg_ch1_time matches \d+\.\. run function rpg:campaign/beelzebub/finish", stage10_tick):
    errors.append("terminal state still auto-finishes without checking career choice")
career_confirm = read("campaign/beelzebub/career_confirm.mcfunction")
if "complete_player" not in career_confirm or "tag @s add rpg.ch1.career.confirmed" not in career_confirm:
    errors.append("career confirmation does not settle and mark the participant")

# Real, safe vacant interaction; generic transfer/random-lord behavior excluded.
vac_stage = read("campaign/beelzebub/stage/2_enter.mcfunction") + read("campaign/beelzebub/stage/2_tick.mcfunction")
for token in ("summon minecraft:villager", "rpg.ch1.vacant.safe", "rpg.vacant", "Invulnerable:1b", "function rpg:vacant/reveal"):
    if token not in vac_stage: errors.append("vacant interaction missing: " + token)
vac_loop = read("vacant/vacant.mcfunction")
if "tag=!rpg.ch1.vacant.safe" not in vac_loop: errors.append("canonical vacant loop does not exclude story-safe actor")
vac_resolve = read("campaign/beelzebub/vacant_reveal.mcfunction")
if "tag @s remove rpg.vacant" not in vac_resolve or "rpg:vacant/loose" in vac_resolve or "rpg:vacant/transfer" in vac_resolve:
    errors.append("story vacant is not safely resolved")

# Goetic calls have exact old/new isolation, role checks, ID copy and 2/2/1 waves.
roles = (("zepar", 1), ("botis", 2), ("bathin", 3), ("sallos", 4), ("purson", 5))
for name, role in roles:
    data = read(f"campaign/beelzebub/spawn/minion/{name}.mcfunction")
    for token in (f"function rpg:minion/summon/beelzebub/{name}", "rpg.ch1.preexisting", "tag=!rpg.ch1.preexisting", f"rpg_mn_role={role}", "rpg_ch1_id = @s rpg_ch1_id"):
        if token not in data: errors.append(f"{name} spawn lacks exact ownership: {token}")
stage3 = read("campaign/beelzebub/stage/3_enter.mcfunction")
wave2, wave3 = read("campaign/beelzebub/minion/wave2.mcfunction"), read("campaign/beelzebub/minion/wave3.mcfunction")
if any(x in stage3 for x in ("bathin", "sallos", "purson")): errors.append("all five minions still spawn at once")
if not all(x in wave2 for x in ("bathin", "sallos")) or "purson" not in wave3: errors.append("2/2/1 minion waves incomplete")
if "rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller" not in read("campaign/beelzebub/stage/3_tick.mcfunction"):
    errors.append("minion liveness is not controller-ID scoped")
scale = read("campaign/beelzebub/minion/scale.mcfunction")
expected_rosters = tuple(range(2, RUNTIME["max_party_size"] + 1))
expected_hp = {spec["role"]: tuple(spec["health_by_party"][str(roster)] for roster in expected_rosters)
               for spec in MINIONS.values()}
for role, values in expected_hp.items():
    for roster, hp in zip(expected_rosters, values):
        signature = f"if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id if score @s rpg_mn_role matches {role} if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_roster matches {roster} run attribute @s minecraft:max_health base set {hp}"
        if signature not in scale or f"{{Health:{hp}f}}" not in scale: errors.append(f"minion scale missing role={role} roster={roster} hp={hp}")
if "rpg_ch1_roster" in read("campaign/beelzebub/spawn/boss.mcfunction"):
    errors.append("Boss incorrectly inherits party health scaling")

# Combat and critical story are separated by explicit safe sub-states.  Enemy
# spawn functions must not share an entry file/tick with unguarded exposition.
stage3_enter = read("campaign/beelzebub/stage/3_enter.mcfunction")
stage3_tick = read("campaign/beelzebub/stage/3_tick.mcfunction")
if "spawn/minion/" in stage3_enter or "minion/wave" in stage3_enter:
    errors.append("Stage 3 still spawns enemies in the briefing entry")
for wave in (1, 2, 3):
    body = read(f"campaign/beelzebub/minion/wave{wave}.mcfunction")
    if "[战斗开始]" not in body or any(speaker in body for speaker in ("米拉：", "伊莱亚：", "别西卜：", "卡西安：")):
        errors.append(f"wave {wave} mixes critical dialogue into active combat")
for state, wave in ((12, 2), (13, 3)):
    for token in (f"rpg_ch1_sub matches {state}", f"minion/wave{wave}", "[战斗即将开始]"):
        if token not in stage3_tick:
            errors.append(f"Stage 3 safe intermission {state} missing: {token}")
stage7_enter = read("campaign/beelzebub/stage/7_enter.mcfunction")
stage7_tick = read("campaign/beelzebub/stage/7_tick.mcfunction")
if "spawn/boss" in stage7_enter:
    errors.append("Stage 7 still spawns the boss before its safe briefing")
if "rpg_ch1_sub matches 0" not in stage7_tick or "boss/begin" not in stage7_tick:
    errors.append("Stage 7 has no briefing-to-combat gate")
for line in stage7_tick.splitlines():
    if "tellraw" in line and "rpg_ch1_sub matches 0" not in line:
        errors.append("Stage 7 has unguarded narrative dialogue during active combat: " + line)
if "rpg_ch1_sub matches 1" not in stage7_tick or "recover_boss" not in stage7_tick:
    errors.append("Stage 7 boss recovery is not gated to the combat state")

# Three different puzzle verbs must be reachable only after their observation
# phase, own all spawned retaliation enemies, and return to a complete board.
puzzle_specs = (
    (4, "route", ("route1", "route2", "route3"), "puzzle.wait.route"),
    (5, "hypothesis_board", ("theory1", "theory2", "theory3"), "puzzle.wait.theory"),
    (6, "calibration", ("slot1", "slot2", "slot3"), "puzzle.wait.slot"),
)
for stage, group, keys, wait_tag in puzzle_specs:
    body = read(f"campaign/beelzebub/stage/{stage}_tick.mcfunction")
    for token in (f"{group}/activate", "puzzle/refresh_enemies", f"rpg.ch1.{wait_tag}", f"{group}/respawn"):
        if token not in body:
            errors.append(f"Stage {stage} puzzle lifecycle missing: {token}")
    for key in keys:
        probe = read(f"campaign/beelzebub/probe/{key}.mcfunction")
        if f"rpg_ch1_seen matches {RUNTIME['observation_ticks']['puzzle']}.." not in probe or f"choice/{key}" not in probe:
            errors.append(f"puzzle choice probe missing or untimed: {key}")
    wrong = read(f"campaign/beelzebub/{group}/wrong.mcfunction")
    for token in ("rpg.ch1.puzzle.enemy.current", "life_ticks:1200", "rpg_ch1_id = @s rpg_ch1_id", f"rpg.ch1.{wait_tag}"):
        if token not in wrong:
            errors.append(f"{group} wrong-answer recovery lacks: {token}")
refresh_puzzle = read("campaign/beelzebub/puzzle/refresh_enemies.mcfunction")
if f"distance={RUNTIME['scene_radius'] + 0.01}.." not in refresh_puzzle:
    errors.append("puzzle retaliation enemies have no arena-boundary recovery")
route_order = {"route2": 0, "route1": 1, "route3": 2}
for key, expected in route_order.items():
    if f"rpg_ch1_choice matches {expected}" not in read(f"campaign/beelzebub/route/resolve_{key}.mcfunction"):
        errors.append(f"route cipher order drifted: {key} should be step {expected}")
if "rpg.ch1.theory.1" not in read("campaign/beelzebub/hypothesis_board/reject1.mcfunction") or "rpg.ch1.theory.2" not in read("campaign/beelzebub/hypothesis_board/reject2.mcfunction"):
    errors.append("hypothesis board does not preserve both rejected false theories")
if "hypothesis_board/wrong" not in read("campaign/beelzebub/hypothesis_board/resolve_theory3.mcfunction"):
    errors.append("rejecting the retained Beelzebub hypothesis is not handled")
slot_items = {"slot1": "rpg_nail:1b", "slot2": "rpg_medium:4b", "slot3": "rpg_ch1_pending_page:1b"}
for slot, identity in slot_items.items():
    if identity not in read(f"campaign/beelzebub/calibration/resolve_{slot}.mcfunction"):
        errors.append(f"ritual calibration item mapping drifted: {slot}")

# Environment yields hypothesis only. Canonical skill hooks produce distinct
# witness facts; chapter binding additionally requires witness.ready.
stage5_tree = "\n".join(read(x) for x in ["campaign/beelzebub/stage/5_enter.mcfunction", "campaign/beelzebub/stage/5_tick.mcfunction"] + [f"campaign/beelzebub/point/hyp{n}.mcfunction" for n in range(1, 4)])
if "inquest/clue/4_" in stage5_tree or "rpg.name.4" in stage5_tree: errors.append("environment hypothesis still prematurely confirms true name")
for n in range(1, 4):
    if f"rpg.ch1.done.hyp.{n}" not in read(f"campaign/beelzebub/point/hyp{n}.mcfunction"): errors.append(f"hypothesis fact {n} missing")
for n in range(1, 6):
    skill = read(f"taint/sk4_{n}.mcfunction")
    if f"function rpg:campaign/beelzebub/witness/skill{n}" not in skill or "tag=rpg.ch1.boss" not in skill or "tag=rpg.ch1.member" not in skill:
        errors.append(f"chapter skill witness hook {n} missing/scoped incorrectly")
    record = read(f"campaign/beelzebub/witness/record{n}.mcfunction")
    if f"rpg.ch1.witness.skill.{n}" not in record: errors.append(f"distinct witness fact {n} missing")
recount = read("campaign/beelzebub/witness/recount.mcfunction")
if "rpg_ch1_seen matches 3.." not in recount or "witness/confirm" not in recount: errors.append("three-distinct witness threshold missing")
confirm = read("campaign/beelzebub/witness/confirm.mcfunction")
if "rpg.ch1.witness.ready" not in confirm or "witness/confirm_player" not in confirm: errors.append("witness confirmation does not publish ready/player truth")
cache1 = read("campaign/beelzebub/point/cache1.mcfunction")
pending = read("campaign/beelzebub/give/pending_page.mcfunction")
confirm_player = read("campaign/beelzebub/witness/confirm_player.mcfunction")
reissue = read("campaign/beelzebub/cache/reissue_missing.mcfunction")
if "campaign/beelzebub/give/pending_page" not in cache1 or "inquest/give/page4" in cache1:
    errors.append("Stage 6 cache1 does not exclusively issue the pending missing page")
if "rpg_ch1_pending_page:1b" not in pending or "rpg_rite_page" in pending or "rpg_lord" in pending:
    errors.append("pending missing page can masquerade as a canonical confirmed page")
if "clear @s minecraft:paper[minecraft:custom_data~{rpg_ch1_pending_page:1b}]" not in confirm_player or "inquest/give/page4" not in confirm_player:
    errors.append("three-witness confirmation does not replace pending page with formal page4")
if "inquest/give/page4" in reissue or "tag=rpg.ch1.witness.ready" not in reissue:
    errors.append("tool reissue can publish formal page4 before witness.ready")
bind = read("inquest/stage1.mcfunction")
if "tag=rpg.ch1.boss" not in bind or "tag=rpg.ch1.witness.ready" not in bind or "if score @s rpg_ch1_id =" not in bind:
    errors.append("chapter Beelzebub bind lacks controller witness+ID gate")

# Configured chapter boss is isolated from preexisting lords; rite inherits both IDs.
boss = read("campaign/beelzebub/spawn/boss.mcfunction")
for token in (f"function {BOSS['summon_function']}", "rpg.ch1.preexisting", "tag=!rpg.ch1.preexisting", f"scores={{rpg_dm_lord={BOSS['lord_score']}}}", "rpg_ch1_id = @s rpg_ch1_id", f"minecraft:max_health base set {BOSS['health']}", f"Health:{BOSS['health']}f"):
    if token not in boss: errors.append("boss spawn isolation missing: " + token)
rite = read("campaign/beelzebub/claim_rite.mcfunction")
if "tag @s add rpg.ch1.rite" not in rite or f"rpg_ch1_id = @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.current" not in rite:
    errors.append("rite does not inherit campaign boss ID")
for kind in ("eliminate", "banish", "seal", "pact"):
    outcome = read(f"inquest/outcome/{kind}.mcfunction")
    first = outcome.splitlines()[0] if outcome.splitlines() else ""
    for token in ("@s[tag=rpg.ch1.rite]", "rpg_ch1_id", "rpg_rite_id", f"verdict/{kind}"):
        if token not in first: errors.append(f"{kind} verdict route lacks exact {token}")
    verdict = read(f"campaign/beelzebub/verdict/{kind}.mcfunction")
    if "rpg.ch1.rite.active" not in verdict or "rpg_ch1_id" not in verdict or "rpg_rite_id" not in verdict:
        errors.append(f"{kind} verdict implementation not double-bound")

# In 1.21.11 the flash particle requires an explicit color payload. A bare
# ``minecraft:flash`` passes text-level validation but makes the whole function
# fail Brigadier loading on a real server.
escape = read("campaign/beelzebub/escape_boss.mcfunction")
if "particle minecraft:flash{color:" not in escape or "particle minecraft:flash ~" in escape:
    errors.append("escape flash particle lacks the required 1.21.11 color payload")
choice_final = read("inquest/choice/final.mcfunction")
first_choice_lines = "\n".join(choice_final.splitlines()[:12])
for token in ("tag=rpg.ch1.member", "tag=rpg.ch1.rite", "rpg_ch1_id", "rpg_ch1_session", "verdict/reject"):
    if token not in first_choice_lines: errors.append("campaign choice admission gate missing: " + token)
if "tag @s add rpg.rite.chooser" not in choice_final:
    errors.append("campaign choice gate broke the generic rite choice path")

# Failure recovery, idempotent personal rewards, career and higher-rank consumer.
if "recover_minions" not in read("campaign/beelzebub/stage/3_tick.mcfunction"): errors.append("minion spawn/wipe recovery absent")
stage3_tick = read("campaign/beelzebub/stage/3_tick.mcfunction")
if "mira/capture" not in stage3_tick or "mira/rescue_capture" not in stage3_tick or f"rpg_ch1_guard {RECOVERY['mira_rescue_window_ticks']}" not in read("campaign/beelzebub/mira/capture.mcfunction"):
    errors.append("Mira protection/capture/recovery loop absent")
if f"rpg_ch1_rescue matches {RECOVERY['mira_rescue_ticks']}.." not in stage3_tick or "unless entity @a[tag=rpg.ch1.current,distance=..3" not in stage3_tick:
    errors.append("Stage 3 Mira rescue is not a continuous 40-tick proximity action")
if f"positioned {CONFIG['actors']['npcs']['mira_guard']['spawn']} run tp" not in read("campaign/beelzebub/mira/rescue_capture.mcfunction"):
    errors.append("Stage 3 Mira rescue does not return her to the team anchor")
if "recover_boss" not in read("campaign/beelzebub/stage/7_tick.mcfunction") or "inquest/tool/cleanup" not in read("campaign/beelzebub/recover_boss.mcfunction"):
    errors.append("boss/rite failure recovery absent")
failure = read("campaign/beelzebub/roster/failure_tick.mcfunction")
for token in ("#ch1_online rpg_ch1_empty", "#ch1_alive rpg_ch1_empty", "data get entity @s Health 100", f"rpg_ch1_empty matches {RECOVERY['party_wipe_ticks']}..", "roster/failure_recover"):
    if token not in failure: errors.append("200-tick total-party failure gate missing: " + token)
if "@a[tag=rpg.ch1.member,distance=" in failure or "@a[tag=rpg.ch1.member,gamemode=!spectator,distance=" in failure:
    errors.append("failure gate mistakes living members outside the arena for a wipe")
if "rpg_ch1_stage matches 3 run function rpg:campaign/beelzebub/roster/failure_tick" not in tick or "rpg_ch1_stage matches 7 run function rpg:campaign/beelzebub/roster/failure_tick" not in tick:
    errors.append("failure gate is not active in both Stage 3 and Stage 7")
failure_recover = read("campaign/beelzebub/roster/failure_recover.mcfunction")
if "recover_minions" not in failure_recover or "recover_boss" not in failure_recover:
    errors.append("wipe recovery does not return to both stage checkpoints")
recover_boss = read("campaign/beelzebub/recover_boss.mcfunction")
if f"kill @e[type={BOSS['entity_type']},tag=rpg.ch1.boss.current]" not in recover_boss or "if score @s rpg_ch1_id =" not in recover_boss:
    errors.append("Stage 7 wipe can leave the old ID-owned boss alive")
if "rpg.ch1.kit.issued" not in reissue or reissue.count("execute unless items entity @s inventory.*") < 9:
    errors.append("returning fixed members do not receive one-time missing ritual tools")
collapse = read("inquest/anchor_collapse.mcfunction")
if not collapse.startswith("execute if entity @s[tag=rpg.ch1.rite]") or "rpg_ch1_id" not in collapse.splitlines()[0] or "rpg_rite_id" not in collapse.splitlines()[0]:
    errors.append("stability collapse can still reach generic eliminate rewards")
stage4 = read("inquest/anchor_stage4.mcfunction")
if not stage4.startswith("execute if entity @s[tag=rpg.ch1.rite] run return run function rpg:campaign/beelzebub/rite/stage4"):
    errors.append("chapter verdict timeout still reaches generic auto-banish")
if "outcome/" in read("campaign/beelzebub/rite/stage4.mcfunction"):
    errors.append("chapter verdict timeout chooses an outcome")
complete = read("campaign/beelzebub/complete_player.mcfunction")
complete_lines = complete.splitlines()
if len(complete_lines) < 3 or "rpg_ch1_verdict =" not in complete_lines[0] or complete_lines[1] != "execute if score @s rpg_ch1_reward matches 1.. run return 0" or complete_lines[2] != "scoreboard players set @s rpg_ch1_reward 1":
    errors.append("verdict persistence/reward idempotency transaction order is unsafe")
for token in ("rpg_ex_xp 60", "inquest/career/sync", "inquest/career/claim", "rpg_ch1_next 1"):
    if token not in complete: errors.append("completion progression missing: " + token)
next_hunt = read("campaign/beelzebub/next_hunt.mcfunction")
if "rpg_ch1_next matches 1.." not in next_hunt or "function rpg:panel/inquest" not in next_hunt: errors.append("higher-rank unlock has no guarded consumer")

# Stage 9 proves Mira's personhood before intervention, then binds rescue to the
# current fixed member, instance ID and that instance's witness within 12 blocks.
stage9_enter = read("campaign/beelzebub/stage/9_enter.mcfunction")
stage9_tick = read("campaign/beelzebub/stage/9_tick.mcfunction")
rescue = read("campaign/beelzebub/rescue.mcfunction")
if "rpg_panel set 13" in stage9_enter: errors.append("Stage 9 rescue is offered before Mira's testimony")
statement_ticks = [40, 85, 130, 175]
positions = [stage9_tick.find(f"rpg_ch1_time matches {n} run tellraw") for n in statement_ticks]
button_pos = stage9_tick.find("rpg_ch1_time matches 220 run tellraw")
if any(p < 0 for p in positions) or button_pos < 0 or not all(p < button_pos for p in positions):
    errors.append("Stage 9 lacks four fixed-timing personality statements before rescue opens")
for token in ("tag=rpg.ch1.member", "rpg_ch1_stage=9", "rpg_ch1_time matches 220..", "rpg_ch1_id", "rpg_ch1_session", "tag=rpg.ch1.witness.current,distance=..12"):
    if token not in rescue: errors.append("Stage 9 rescue admission missing: " + token)

# Continuous observation/read gates add 700 ticks (35 seconds) of active
# investigation without padding combat. Total 20-60 minute duration remains a
# runtime playtest target because combat and four-stage ritual are player-driven.
observation_ticks = 0
timing = RUNTIME["observation_ticks"]
for key, threshold in [(f"anom{n}", timing["anomaly"]) for n in range(1, 4)] + [(f"trail{n}", timing["trail"]) for n in range(1, 5)] + [(f"hyp{n}", timing["hypothesis"]) for n in range(1, 4)] + [(f"cache{n}", timing["cache"]) for n in range(1, 4)]:
    probe = read(f"campaign/beelzebub/probe/{key}.mcfunction")
    if f"rpg_ch1_seen matches {threshold}.." not in probe or "matches 0 run scoreboard players set @s rpg_ch1_seen 0" not in probe:
        errors.append(f"active observation gate missing/reset-unsafe: {key}")
    else:
        observation_ticks += threshold
if observation_ticks <= 0: errors.append("configured active investigation rhythm is empty")

# Cleanup and performance safety: no terrain edits, no broad world deletion,
# no heavy repeating selector lacking an ownership tag/type.
campaign_dir = fun / "campaign" / "beelzebub"
display_count = 0
for p in campaign_dir.rglob("*.mcfunction"):
    data = p.read_text(encoding="utf-8")
    if re.search(r"\b(setblock|fill|clone|place|forceload)\b", data): errors.append("terrain mutation: " + str(p.relative_to(fun)))
    for line in data.splitlines():
        if "summon minecraft:text_display" not in line:
            continue
        display_count += 1
        if re.search(r'text:"\[\\"', line):
            errors.append("text_display component is double-encoded as literal JSON: " + str(p.relative_to(fun)))
        if "text:[" not in line:
            errors.append("text_display does not use a direct 1.21.11 component list: " + str(p.relative_to(fun)))
if display_count < 13:
    errors.append("campaign investigation displays are unexpectedly missing")
for rel in ("campaign/beelzebub/finish.mcfunction", "campaign/beelzebub/abort.mcfunction"):
    cleanup_data = read(rel)
    for token in ("rpg.ch1.cleanup.controller", "@a[tag=rpg.ch1.member]", "if score @s rpg_ch1_id =", "rpg.ch1.cleanup.player", "scoreboard players set @a[tag=rpg.ch1.cleanup.player] rpg_ch1_id 0"):
        if token not in cleanup_data: errors.append(f"same-ID member cleanup missing in {rel}: {token}")
    if "@a[tag=rpg.ch1.current] remove rpg.ch1.member" in cleanup_data:
        errors.append(f"cleanup still depends on current-area membership in {rel}")
    for line in cleanup_data.splitlines():
        if line.startswith("kill @e[") and f"distance=..{RUNTIME['scene_radius']}" not in line: errors.append(f"unbounded cleanup in {rel}: {line}")
orphan = read("campaign/beelzebub/orphan_scrub.mcfunction")
for forbidden in ("rpg_ch1_done", "rpg_ch1_next", "rpg_ch1_reward", "rpg.ch1.borderer", "rpg_ch1_verdict"):
    if forbidden in orphan: errors.append("orphan scrub erases permanent archive state: " + forbidden)
for p in campaign_dir.rglob("*_tick.mcfunction"):
    for line in p.read_text(encoding="utf-8").splitlines():
        if "@e[" in line and "type=" not in line and "tag=" not in line: errors.append(f"unbounded tick selector: {p.relative_to(fun)} :: {line}")

adv = root / "data" / "rpg" / "advancement" / "campaign" / "beelzebub.json"
try: json.loads(adv.read_text(encoding="utf-8"))
except Exception as exc: errors.append("invalid advancement: " + str(exc))

if errors:
    print(f"Chapter I check FAILED ({len(errors)})")
    for error in errors: print("- " + error)
    raise SystemExit(1)
print("Chapter I check OK: 11-state flow, fixed membership, ID/rite ownership, true vacant, three witnesses, recovery, rewards and safety")
