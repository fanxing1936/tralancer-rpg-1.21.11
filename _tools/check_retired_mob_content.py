#!/usr/bin/env python3
"""Fail publication if any retired legacy mob entry point returns."""
from __future__ import annotations

import sys
from pathlib import Path


root = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
functions = root / "data" / "rpg" / "function"
errors: list[str] = []

for relative in ("entities/drowned", "entities/piglin", "entities/illager"):
    if (functions / relative).exists():
        errors.append(f"retired function tree still exists: {relative}")

for name in ("zombie", "zombie_batch", "zombie_gear", "skeleton", "skeleton_batch", "skeleton_gear"):
    if (functions / "command" / "spawn" / f"{name}.mcfunction").exists():
        errors.append(f"retired variant function still exists: command/spawn/{name}")

for path in functions.rglob("*.mcfunction"):
    body = path.read_text(encoding="utf-8")
    for token in ("rpg:command/spawn/zombie", "rpg:command/spawn/skeleton", "rpg:entities/drowned/", "rpg:entities/piglin/", "rpg:entities/illager/"):
        if token in body:
            errors.append(f"retired reference {token} in {path.relative_to(functions)}")

if errors:
    print(f"Retired mob content check FAILED ({len(errors)})")
    for error in errors:
        print("- " + error)
    raise SystemExit(1)
print("Retired mob content check OK: vanilla zombies/skeletons; no wind, drowned or piglin armies")
