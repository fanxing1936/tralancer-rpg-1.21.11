# -*- coding: utf-8 -*-
"""Audit the public debug catalogue against the pack and generated docs."""
import json
import re
from pathlib import Path
from debug_commands import ALL_COMMANDS, STAGES

ROOT = Path(__file__).resolve().parent.parent
FUNCTION_ROOT = ROOT / "rpg" / "data" / "rpg" / "function"


def fail(message):
    raise SystemExit("debug command audit failed: " + message)


commands = [item["command"] for item in ALL_COMMANDS]
if len(commands) != len(set(commands)):
    fail("duplicate commands in catalogue")
for command_text in commands:
    if command_text.startswith("/function rpg:"):
        function_id = command_text.removeprefix("/function rpg:")
        path = FUNCTION_ROOT / (function_id + ".mcfunction")
        if not path.is_file():
            fail(f"missing function for {command_text}: {path}")
    if "_worker" in command_text or command_text.endswith("/stage_reset"):
        fail(f"internal helper exposed as public command: {command_text}")

catalogue = set(commands)
by_command = {item["command"]: item for item in ALL_COMMANDS}
for path in (FUNCTION_ROOT / "minion" / "summon").rglob("*.mcfunction"):
    expected = "/function rpg:" + path.relative_to(FUNCTION_ROOT).with_suffix("").as_posix()
    if expected not in catalogue:
        fail(f"unlisted minion summon: {expected}")
    if path.name != "all.mcfunction":
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        match = re.search(r"麾下([^：]+)：([^。]+)", first_line)
        if not match:
            fail(f"minion public comment has no role/name contract: {expected}")
        role, name = match.groups()
        documented = by_command[expected]["use"]
        if role not in documented or name not in documented:
            fail(f"minion annotation drift for {expected}: expected {role}/{name}")

debug_root = FUNCTION_ROOT / "campaign" / "beelzebub" / "debug"
for path in debug_root.rglob("*.mcfunction"):
    if path.stem.endswith("_worker") or path.stem == "stage_reset":
        continue
    expected = "/function rpg:" + path.relative_to(FUNCTION_ROOT).with_suffix("").as_posix()
    if expected not in catalogue:
        fail(f"unlisted chapter debug entry: {expected}")

menu = (debug_root / "menu.mcfunction").read_text(encoding="utf-8")
for clicked in re.findall(r'"command":"(/function rpg:[^"]+)"', menu):
    if clicked not in catalogue:
        fail(f"chapter debug menu command missing from catalogue: {clicked}")

endless_debug = FUNCTION_ROOT / "endless" / "debug"
for path in endless_debug.rglob("*.mcfunction"):
    expected = "/function rpg:" + path.relative_to(FUNCTION_ROOT).with_suffix("").as_posix()
    if expected not in catalogue:
        fail(f"unlisted endless debug entry: {expected}")
endless_menu = (endless_debug / "menu.mcfunction").read_text(encoding="utf-8")
for clicked in re.findall(r'"command":"(/function rpg:[^"]+)"', endless_menu):
    if clicked not in catalogue:
        fail(f"endless debug menu command missing from catalogue: {clicked}")
for required in ("/function rpg:endless/start", "/function rpg:endless/join",
                 "/function rpg:endless/abort", "/function rpg:endless/debug/menu"):
    if required not in catalogue:
        fail(f"endless public entry omitted: {required}")

for stage, expected_label in enumerate(STAGES):
    stage_source = (FUNCTION_ROOT / "campaign" / "beelzebub" / "stage" / f"{stage}_enter.mcfunction").read_text(encoding="utf-8")
    match = re.search(r'^bossbar set rpg:chapter1 name .*?"text":"([^"]+)"', stage_source, re.MULTILINE)
    if not match or (stage == 7 and not expected_label.startswith("万蝇腐宴｜")) or (stage != 7 and match.group(1) != expected_label):
        fail(f"Stage {stage} annotation drift: documented={expected_label!r}, runtime={match.group(1) if match else None!r}")

load_values = json.loads((ROOT / "rpg" / "data" / "minecraft" / "tags" / "function" / "load.json").read_text(encoding="utf-8"))["values"]
for function_id in ("rpg:command/soreboard", "rpg:command/bossbar"):
    if function_id not in load_values:
        fail(f"initialization annotation says auto-load but load tag omits {function_id}")

for command_text in ("/function rpg:command/give/box", "/function rpg:command/give/extra", "/function rpg:command/give/item", "/function rpg:command/give/weapon_up_item"):
    function_id = command_text.removeprefix("/function rpg:")
    source = (FUNCTION_ROOT / (function_id + ".mcfunction")).read_text(encoding="utf-8")
    if "give @a " not in source or "@a" not in by_command[command_text]["prerequisite"]:
        fail(f"group-give annotation drift for {command_text}")

for required in ("/function rpg:command/summon_devil", "/function rpg:taint/lord"):
    if required not in catalogue:
        fail(f"known manual demon summon entry omitted: {required}")

for output in (ROOT / "TRALANCER-RPG-图鉴.html", ROOT / "DEBUG-COMMANDS.md"):
    if not output.is_file():
        fail(f"missing generated document: {output.name}")
    text = output.read_text(encoding="utf-8")
    missing = [cmd for cmd in commands if cmd not in text]
    if missing:
        fail(f"{output.name} omits {len(missing)} command(s), first: {missing[0]}")
    if output.suffix == ".html" and text.count('<tr><td class="num"><code>') != len(commands):
        fail("HTML debug table row count does not match catalogue")
print(f"debug command audit: PASS ({len(commands)} public commands, all functions and docs present)")
