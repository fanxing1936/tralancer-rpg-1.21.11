#!/usr/bin/env python3
"""Static checks for the generated 1.21.11 mob-death drop policy."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from add_drop_policy import (
    CHARGED_CREEPER_TABLES,
    CUSTOM_ENTITY_TABLES,
    EMPTY_ENTITY_TABLE,
    EXCLUDED_ENTITY_TABLES,
    VANILLA_1_21_11_ENTITIES,
)


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    dp = Path(sys.argv[1] if len(sys.argv) > 1 else "rpg")
    problems: list[str] = []
    vanilla = dp / "data/minecraft/loot_table"
    suppressed = set(VANILLA_1_21_11_ENTITIES) - CUSTOM_ENTITY_TABLES - EXCLUDED_ENTITY_TABLES

    for name in sorted(suppressed):
        path = vanilla / "entities" / f"{name}.json"
        if not path.is_file() or read_json(path) != EMPTY_ENTITY_TABLE:
            problems.append(f"not an empty suppressed entity table: {name}")

    for name in sorted(CUSTOM_ENTITY_TABLES):
        path = vanilla / "entities" / f"{name}.json"
        if not path.is_file() or read_json(path) == EMPTY_ENTITY_TABLE:
            problems.append(f"authored entity table missing or emptied: {name}")

    for name in sorted(EXCLUDED_ENTITY_TABLES):
        path = vanilla / "entities" / f"{name}.json"
        if path.is_file() and read_json(path) == EMPTY_ENTITY_TABLE:
            problems.append(f"excluded inventory-bearing table was emptied: {name}")

    for name in sorted(CHARGED_CREEPER_TABLES):
        path = vanilla / "charged_creeper" / f"{name}.json"
        if not path.is_file() or read_json(path) != EMPTY_ENTITY_TABLE:
            problems.append(f"charged-creeper table not suppressed: {name}")

    returned = read_json(dp / "data/rpg/loot_table/squad/equipment_return.json")
    return_text = json.dumps(returned, ensure_ascii=False, separators=(",", ":"))
    for token in ('"type":"minecraft:slots"', '"source":"this"', '"slots":"weapon.mainhand"'):
        if token not in return_text:
            problems.append(f"mercenary equipment return lacks {token}")

    tick = (dp / "data/rpg/function/drop_policy/tick.mcfunction").read_text(encoding="utf-8")
    prepare = (dp / "data/rpg/function/drop_policy/prepare.mcfunction").read_text(encoding="utf-8")
    required = (
        "type=#rpg:drop_policy_mobs",
        "tag=!rpg.drop_policy.v1",
        "DeathLootTable set value \"rpg:squad/equipment_return\"",
        "CanPickUpLoot:0b",
        "mainhand:0f",
        "offhand:0f",
        "body:0f",
        "saddle:0f",
    )
    joined = tick + prepare
    main_tick = (dp / "data/rpg/function/command/tick.mcfunction").read_text(encoding="utf-8")
    if not main_tick.startswith("function rpg:drop_policy/tick\n"):
        problems.append("drop policy is not wired before combat tick")
    for token in required:
        if token not in joined:
            problems.append(f"runtime guard lacks {token}")
    for forbidden in ("kill @e[type=minecraft:item", "doMobLoot false", "doMobLoot set false"):
        if forbidden in joined:
            problems.append(f"unsafe global strategy present: {forbidden}")

    manifest = read_json(dp / "data/rpg/drop_policy_manifest.json")
    if not manifest.get("hardcoded_boundaries"):
        problems.append("manifest does not document hardcoded boundaries")

    if problems:
        print("drop-policy check FAILED")
        for problem in problems:
            print(f"  - {problem}")
        raise SystemExit(1)
    print("drop-policy check PASS")
    print(f"  {len(suppressed)} vanilla entity loot tables empty; 7 authored tables preserved")
    print("  charged-creeper heads suppressed; ordinary item entities untouched")
    print("  mercenary main-hand return uses minecraft:slots")


if __name__ == "__main__":
    main()
