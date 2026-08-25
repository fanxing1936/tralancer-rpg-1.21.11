# -*- coding: utf-8 -*-
"""Structural and geometric audit for the particle Tree of Life."""

import io
import os
import re
import sys


ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(ROOT, "data/rpg/function")
problems = []


def read(rel):
    path = os.path.join(FUNC, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        problems.append("missing function: " + rel)
        return ""
    with io.open(path, encoding="utf-8") as handle:
        return handle.read()


score = read("command/soreboard.mcfunction")
if "scoreboard objectives add rpg_lt_tick dummy" not in score:
    problems.append("missing life-tree clock objective")

runtime = read("exorcism.mcfunction")
if "if entity @e[type=minecraft:marker,tag=rpg.ritual.life_tree,limit=1] run function rpg:ritual/life_tree/tick" not in runtime:
    problems.append("missing type-guarded runtime hook")

tick = read("ritual/life_tree/tick.mcfunction")
if "matches 10.." not in tick or "execute as @e[type=minecraft:marker,tag=rpg.ritual.life_tree]" not in tick:
    problems.append("tree is not batched to ten-tick marker redraws")

place = read("ritual/life_tree/place.mcfunction")
for needle in ("@s[type=minecraft:player]", "Rotation[0]", "Rotation[1] set value 0.0f", "function rpg:ritual/life_tree/draw"):
    if needle not in place:
        problems.append("place function lacks: " + needle)
if "distance=..2,limit=1" not in place:
    problems.append("place function lacks duplicate-anchor guard")

clear = read("ritual/life_tree/clear.mcfunction")
clear_all = read("ritual/life_tree/clear_all.mcfunction")
if "type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..12" not in clear:
    problems.append("nearby clear is not safely scoped")
if "kill @e[type=minecraft:marker,tag=rpg.ritual.life_tree]" not in clear_all:
    problems.append("global clear command missing")

draw = read("ritual/life_tree/draw.mcfunction")
nodes = re.findall(r"^# NODE (\w+) / .* diameter=([0-9.]+) points=(\d+)(?: dashed)?$", draw, re.M)
paths = re.findall(r"^# PATH (\w+) -> (\w+) samples=(\d+)$", draw, re.M)
if len(nodes) != 11:
    problems.append("expected 10 visible circles plus Daath, found %d" % len(nodes))
if any(abs(float(diameter) - 1.0) > 0.001 for _, diameter, _ in nodes):
    problems.append("one or more node diameters differ from one block")
if len(paths) != 22:
    problems.append("expected canonical 22 paths, found %d" % len(paths))
if draw.count("# NODE daath") != 1 or "# NODE daath" not in draw or "dashed" not in next((line for line in draw.splitlines() if line.startswith("# NODE daath")), ""):
    problems.append("hidden Daath ring is not dashed")

particle_lines = [line for line in draw.splitlines() if line.startswith("particle ")]
if not 350 <= len(particle_lines) <= 500:
    problems.append("particle density escaped budget: %d commands/redraw" % len(particle_lines))
if any(" ^" not in line for line in particle_lines):
    problems.append("one or more particles are not marker-local/orientable")
if any(re.search(r"\^(-?\d+(?:\.\d+)?) \^(\d+(?:\.\d+)?) \^(-?\d+(?:\.\d+)?)", line) is None for line in particle_lines):
    problems.append("malformed local particle coordinate")

# The image's proportional footprint: about four blocks wide and 8.5 tall.
coords = []
for line in particle_lines:
    match = re.search(r"\^(-?\d+(?:\.\d+)?) \^(?:\d+(?:\.\d+)?) \^(-?\d+(?:\.\d+)?)", line)
    if match:
        coords.append((float(match.group(1)), float(match.group(2))))
if coords:
    width = max(x for x, _ in coords) - min(x for x, _ in coords)
    height = max(z for _, z in coords) - min(z for _, z in coords)
    if not 3.8 <= width <= 4.1:
        problems.append("footprint width out of proportion: %.3f" % width)
    if not 8.3 <= height <= 8.6:
        problems.append("footprint height out of proportion: %.3f" % height)

if problems:
    print("LIFE TREE PARTICLE AUDIT: FAIL")
    for problem in problems:
        print(" - " + problem)
    raise SystemExit(1)

print("LIFE TREE PARTICLE AUDIT: PASS")
print("  10 Sephiroth + dashed Daath / 22 paths / diameter exactly 1 block")
print("  footprint %.3f x %.3f blocks / %d particle commands per 10-tick redraw" % (width, height, len(particle_lines)))
print("  player-yaw placement, local clear, global clear and guarded runtime present")
