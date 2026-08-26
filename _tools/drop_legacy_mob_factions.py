#!/usr/bin/env python3
"""Remove retired overworld variants and the three legacy faction armies."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path


root = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
function_root = root / "data" / "rpg" / "function"

# These are self-contained legacy encounter trees.  Warden/demon content is a
# different system and deliberately remains untouched.
for relative in ("entities/drowned", "entities/piglin", "entities/illager"):
    target = function_root / relative
    if target.exists():
        shutil.rmtree(target)

# Optimisation rewrites the original world-wide rolls into per-mob batch
# functions, so remove both the generated entry points and their tick hooks.
spawn_root = function_root / "command" / "spawn"
for name in ("zombie", "zombie_batch", "zombie_gear", "skeleton", "skeleton_batch", "skeleton_gear"):
    target = spawn_root / f"{name}.mcfunction"
    if target.exists():
        target.unlink()

tick = function_root / "command" / "tick.mcfunction"
if tick.exists():
    lines = tick.read_text(encoding="utf-8").splitlines()
    retired = ("rpg:command/spawn/zombie", "rpg:command/spawn/skeleton")
    kept = [line for line in lines if not any(token in line for token in retired)]
    tick.write_text("\n".join(kept).rstrip() + "\n", encoding="utf-8", newline="\n")

print("Retired mob content removed: zombie/skeleton variants, wind raiders, drowned and piglin armies")
