# -*- coding: utf-8 -*-
"""Requirement-level audit for the ritual Boss phase-two state machine."""

import io
import os
import sys


DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")


def read(rel):
    with io.open(os.path.join(FUNC, rel.replace("/", os.sep)), encoding="utf-8") as f:
        return f.read()


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def particle_id(line):
    return line.split("particle ", 1)[1].split(" ", 1)[0]


def line_with(lines, token):
    return next(line for line in lines if token in line)


def main():
    dispatch = read("inquest/phase2/pressure.mcfunction")
    names = set()
    signatures = {1: "end_rod", 2: "bubble_column_up", 3: "soul",
                  4: "mycelium", 5: "soul_fire_flame", 6: "reverse_portal",
                  7: "end_rod"}
    for lord in range(1, 8):
        bind = read("inquest/bind/%d.mcfunction" % lord)
        anchor = read("inquest/anchor_bind/%d.mcfunction" % lord)
        need("phase2/shockwave" in bind, "shockwave missing for lord %d" % lord)
        need("rpg_ex_stab 50" in anchor, "stability is not 50 for lord %d" % lord)
        need("rpg_totem 2400" in anchor, "phase-two timer is not 120 seconds")
        for variant in range(1, 4):
            route = "inquest/phase2/pressure/%d_%d.mcfunction" % (lord, variant)
            body = read(route)
            need("phase2/pressure/%d_%d" % (lord, variant) in dispatch,
                 "unreachable pressure variant %d/%d" % (lord, variant))
            need("particle " in body and "tellraw " in body,
                 "pressure variant lacks presentation %d/%d" % (lord, variant))
            need(body.count("particle ") >= 5 and body.count("playsound ") >= 1,
                 "pressure variant presentation is still too light %d/%d" % (lord, variant))
            need("dust_color_transition" in body and
                 ("particle %s " % signatures[lord]) in body,
                 "pressure variant does not follow weapon palette layering %d/%d" %
                 (lord, variant))
            need("particle sonic_boom ~ ~2.2" not in body,
                 "generic sonic-boom template leaked into themed pressure")
            body_lines = body.splitlines()
            first_materials = [particle_id(line_with(body_lines, token)) for token in
                               ("~ ~1.15 ~", "~ ~1.55 ~", "~ ~1 ~ 0.38")]
            need(len(set(first_materials)) == 3,
                 "pressure layers reuse one material %d/%d: %r" %
                 (lord, variant, first_materials))
            need("run damage @s" in body,
                 "pressure variant is not a real AOE damage skill %d/%d" % (lord, variant))
            need("distance=4.01..24" in body or "distance=5..24" in body or
                 "distance=6..24" in body or "distance=7..24" in body or
                 "distance=8..24" in body,
                 "pressure variant lacks outer-field gameplay %d/%d" % (lord, variant))
            first = next(line for line in body.splitlines() if line.startswith("tellraw "))
            need(first not in names, "duplicated pressure identity %d/%d" % (lord, variant))
            names.add(first)
            need("damage @a[" not in body, "multi-target damage syntax regression")
            wave = read("inquest/phase2/wave/%d_%d.mcfunction" % (lord, variant))
            need(wave.count("run damage @s") >= 2 and wave.count("particle ") >= 6,
                 "pressure follow-up waves incomplete %d/%d" % (lord, variant))
            wave_lines = wave.splitlines()
            middle = [particle_id(line_with(wave_lines, token)) for token in
                      ("~ ~1.1 ~", "~ ~1.5 ~", "~ ~1 ~ 0.42")]
            ending = [particle_id(line_with(wave_lines, token)) for token in
                      ("~ ~1.3 ~", "~ ~1.4 ~", "~ ~1 ~ 0.68")]
            need(len(set(middle)) == 3 and len(set(ending)) == 3,
                 "wave layers reuse one material %d/%d: mid=%r end=%r" %
                 (lord, variant, middle, ending))
    need(len(names) == 21, "pressure identity count mismatch")
    need("random value 1..3" in dispatch and "random value 280..360" in dispatch,
         "pressure rotation is not random and periodic")
    need("run damage @s 6 minecraft:magic" in read("inquest/phase2/pressure_core.mcfunction"),
         "pressure impact damage was not strengthened")
    need("pressure_warning" in read("inquest/phase2/pressure_tick.mcfunction"),
         "periodic pressure warning missing")
    warning_dispatch = read("inquest/phase2/pressure_warning.mcfunction")
    for lord in range(1, 8):
        need("phase2/warning/%d" % lord in warning_dispatch,
             "lord-specific pressure warning missing: %d" % lord)
        warning = read("inquest/phase2/warning/%d.mcfunction" % lord)
        need("dust_color_transition" in warning and
             ("particle %s " % signatures[lord]) in warning,
             "warning palette is not lord-specific: %d" % lord)
    need("rpg_ex_wave matches 12" in read("inquest/phase2/wave_tick.mcfunction") and
         "rpg_ex_wave matches 1" in read("inquest/phase2/wave_tick.mcfunction"),
         "three-stage pressure timing missing")

    anchor_tick = read("inquest/anchor_tick.mcfunction")
    for route in ("phase2/tick", "phase2/pressure_tick", "counter/tick",
                  "struggle_tick", "start_verdict", "anchor_collapse"):
        need(route in anchor_tick, "anchor state route missing: " + route)
    need("rpg_ex_stab matches 100.." in anchor_tick, "100 verdict threshold missing")
    need("outcome/eliminate_boss" in read("inquest/anchor_collapse.mcfunction"),
         "zero stability does not force eliminate")
    need("Health:700f" in read("inquest/outcome/eliminate_boss.mcfunction"),
         "forced eliminate is not 700 health")
    lock = read("inquest/phase2/lock_boss.mcfunction")
    need("knockback_resistance modifier add rpg:rite_lock 1" in lock and
         "Motion:[0d,0d,0d]" in lock and "NoAI:1b" in lock and
         "run tp @e[type=minecraft:vindicator,tag=rpg.rite.lock.source" in lock,
         "bound demon is not locked to the ritual centre")
    need("phase2/lock_boss" in read("inquest/bound_tick.mcfunction"),
         "boss lock is not on the bound tick path")
    eliminate = read("inquest/outcome/eliminate_boss.mcfunction")
    need("modifier remove rpg:rite_lock" in eliminate and "NoAI:0b" in eliminate,
         "boss lock is not released for eliminate outcome")

    right = read("inquest/right_click.mcfunction")
    for lord in range(1, 8):
        need("right_click/medium%d" % lord in right, "right-click medium missing")
        need("right_click/page%d" % lord in right, "right-click page missing")
        need("rpg_right_click:1b" in read("inquest/give/medium%d.mcfunction" % lord),
             "medium is not useable")
    for key in ("nail", "incense", "lantern", "chalk1", "chalk2", "chalk3"):
        need("rpg_right_click:1b" in read("inquest/give/%s.mcfunction" % key),
             "tool is not useable: " + key)
    need("minecraft:using_item" in io.open(
        os.path.join(DP, "data/rpg/advancement/inquest/right_click.json"),
        encoding="utf-8").read(), "right-click advancement missing")
    need("minecraft:paper" in read("inquest/choice/seal.mcfunction"),
         "new lantern cannot be selected from verdict UI")

    need("rpg_ex_hud_t=1.." in read("hud/hud.mcfunction"),
         "ritual stability is not persistent HUD priority")
    need("$(d)" in read("hud/render.mcfunction"), "ritual HUD segment not rendered")
    need("storage rpg:hud d set value" in read("hud/status.mcfunction"),
         "ritual HUD segment leaks after the rite")
    print("ritual phase2 audit: 7 lords x 3 reachable pressure fields = 21")
    print("ritual phase2 audit: 21 triple-wave AOE fields + centre-locked boss = PASS")
    print("ritual phase2 audit: 50/100/0 state gates, right-click kit, persistent HUD = PASS")


if __name__ == "__main__":
    main()
