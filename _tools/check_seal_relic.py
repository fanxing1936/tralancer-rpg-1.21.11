#!/usr/bin/env python3
"""Static contract checks for the generated sealed-relic agitation system."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def main() -> None:
    dp = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
    func = dp / "data/rpg/function"
    errors: list[str] = []

    def read(rel: str) -> str:
        path = func / rel
        if not path.is_file():
            errors.append("missing generated function: " + rel)
            return ""
        return path.read_text(encoding="utf-8")

    tick = read("inquest/seal/tick.mcfunction")
    gate = read("inquest/seal/escape_gate.mcfunction")
    dispatch = read("inquest/seal/escape.mcfunction")
    reindex = read("inquest/seal/reindex.mcfunction")
    panel = read("panel/inquest.mcfunction")
    pool = read("rite/pool_beat.mcfunction")
    suppress = read("inquest/seal/suppress.mcfunction")

    if "random value" in tick:
        errors.append("seal tick still contains random escape logic")
    exact_trigger = (
        "execute if score @s rpg_agit matches 100.. run return run function "
        "rpg:inquest/seal/escape_gate"
    )
    if tick.count(exact_trigger) != 1:
        errors.append("escape is not triggered exactly once by rpg_agit 100")
    if "execute unless score @s rpg_agit matches 100.. run return 0" not in gate:
        errors.append("escape gate lacks its independent agitation-100 guard")
    if "rpg_agit matches 99" in tick + gate:
        errors.append("agitation 99 can reach escape")

    root_callers = []
    call_re = re.compile(r"\bfunction rpg:inquest/seal/escape(?:\s|$)")
    for path in func.rglob("*.mcfunction"):
        source = path.read_text(encoding="utf-8")
        if call_re.search(source):
            root_callers.append(path.relative_to(func).as_posix())
    if root_callers != ["inquest/seal/escape_gate.mcfunction"]:
        errors.append("escape root has additional trigger points: %r" % root_callers)
    for number in range(1, 8):
        expected = ("execute if score @s rpg_rel_1 matches %d run return run function "
                    "rpg:inquest/seal/escape%d" % (number, number))
        if expected not in dispatch:
            errors.append("escape dispatch does not preserve escape%d" % number)

    warning_contract = {
        "inquest/seal/warn_agitated.mcfunction": ("[遗物躁动]", "躁动"),
        "inquest/seal/warn_danger.mcfunction": ("[遗物危险]", "圣水", "压制"),
        "inquest/seal/warn_critical.mcfunction": ("[遗物临界]", "rpg_rel_left", "距逃逸还差"),
    }
    for rel, needles in warning_contract.items():
        source = read(rel)
        for needle in needles:
            if needle not in source:
                errors.append("%s lacks warning token %s" % (rel, needle))

    if "# seal relic active slot limit: 2" not in reindex:
        errors.append("slot-limit contract is not declared as 2")
    if "rpg_rel_n matches ..1" not in reindex:
        errors.append("slot index does not stop accepting relics after two")
    indexed_slots = set(re.findall(r"entity @s ((?:hotbar|inventory)\.\d+)", reindex))
    if len(indexed_slots) != 36:
        errors.append("slot index does not inspect the full ordered inventory")
    if "rpg_rel_1" not in panel or "rpg_rel_2" not in panel:
        errors.append("player panel does not name both active relic slots")

    if "scoreboard players remove @s rpg_agit 3" not in pool:
        errors.append("holy-water pool does not purify 3 agitation per beat")
    for needle in ("scoreboard players remove @s rpg_agit 20",
                   "scoreboard players set @s rpg_rel_cd 600",
                   "minecraft:slowness 8 0"):
        if needle not in suppress:
            errors.append("suppression lacks cost/effect token: " + needle)

    ability_contract = {
        "inquest/seal/ability/beelzebub_heal.mcfunction":
            ("minecraft:regeneration", "scoreboard players add @s rpg_agit 3"),
        "inquest/seal/ability/leviathan.mcfunction":
            ("尚无可反制的术式", "reflect_magic", "scoreboard players set @s rpg_rel_rec 0"),
        "inquest/seal/ability/abaddon.mcfunction":
            ("effect give @s minecraft:slowness", "#rpg:seal_hostile"),
    }
    for rel, needles in ability_contract.items():
        source = read(rel)
        for needle in needles:
            if needle not in source:
                errors.append("%s lacks %s" % (rel, needle))

    for rel, needle in (("hud/status.mcfunction", "rpg:hud/seal/render"),
                        ("hud/demon/r1.mcfunction", "$(r),$(a),$(b),$(c),$(d)")):
        if needle not in read(rel):
            errors.append("two-layer relic HUD missing from " + rel)
    rp = dp.parent / "resourcepack"
    font_path = rp / "assets/rpg/font/combat_prompt.json"
    status_texture = rp / "assets/rpg/textures/font/seal_status.png"
    if not font_path.is_file() or not status_texture.is_file():
        errors.append("sealed-relic raised status atlas is missing")
    else:
        font = json.loads(font_path.read_text(encoding="utf-8"))
        providers = font.get("providers", [])
        if not any(p.get("file") == "rpg:font/seal_status.png" and
                   p.get("height") == 28 and p.get("ascent") == 27
                   for p in providers):
            errors.append("sealed-relic status atlas is not a 28/27 bitmap provider")

    if errors:
        print("seal-relic check FAILED")
        for error in errors:
            print("  - " + error)
        raise SystemExit(1)
    print("seal-relic check PASS")
    print("  agitation 100 is the sole escape trigger; 99 is safe")
    print("  three warning tiers, ordered two-slot index and all three abilities wired")
    print("  holy-water purification and suppression costs are statically visible")


if __name__ == "__main__":
    main()
