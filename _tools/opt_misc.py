# -*- coding: utf-8 -*-
"""Small targeted tick-cost fixes that don't fit the generic passes."""

import io
import os
import sys

GOLD_HEX = "#FFD700"

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"

HEALTH = os.path.join(ROOT, "data", "rpg", "function", "entities",
                      "drowned", "health.mcfunction")
GUARD_NOTE = [
    "# rpg:entities/drowned/magic is a 3568-command particle circle.  Only draw it",
    "# when a player is close enough for the particles to render at all.",
]


def guard_magic_circle():
    if not os.path.isfile(HEALTH):
        return 0
    lines = io.open(HEALTH, encoding="utf-8").read().rstrip("\n").split("\n")
    out, changed = [], 0
    for line in lines:
        if "entities/drowned/magic" in line and "if entity @a" not in line:
            line = line.replace("at @s run function",
                                "at @s if entity @a[distance=..48] run function")
            changed += 1
        out.append(line)
    if changed:
        out = GUARD_NOTE + out
        io.open(HEALTH, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    return changed


def fix_belial_devil_tag():
    """贝利尔 shipped with custom_data={blil_tag:1b,sword_tag:1b} -- the only one
    of the five demons missing devil_tag, so anything keyed on the demon flag
    (rpg.h.devil_tag1) silently skipped it."""
    path = os.path.join(ROOT, "data/rpg/function/command/give/weapon.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    old = "custom_data={blil_tag:1b,sword_tag:1b}"
    new = "custom_data={blil_tag:1b,sword_tag:1b,devil_tag:1b}"
    if old not in s:
        return 0
    n = s.count(old)
    io.open(path, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
    return n


def fix_limited_legend():
    """`[l·legend]` was half English and shipped in two different colours
    (#ffcc33 on one weapon, #D84E4E on the other).  It becomes 限定传说 in a
    single gold, one step brighter than the plain 传说 tier's vanilla `gold`
    so the two stay distinguishable."""
    import glob
    n = 0
    for path in glob.glob(os.path.join(
            ROOT, "data/rpg/function/command/give/*.mcfunction")):
        s = io.open(path, encoding="utf-8").read()
        before = s
        for colour in ('"italic":false,"bold":true,"color":"#ffcc33"',
                       '"italic":false,"color":"#D84E4E","bold":true'):
            s = s.replace('{"text":"[l·legend]",' + colour + "}",
                          '{"text":"[限定传说]","italic":false,'
                          '"color":"%s","bold":true}' % GOLD_HEX)
        if s != before:
            io.open(path, "w", encoding="utf-8", newline="\n").write(s)
            n += before.count("[l·legend]")
    return n


if __name__ == "__main__":
    print("magic-circle proximity guards added: %d" % guard_magic_circle())
    print("limited-legend prefix normalised: %d" % fix_limited_legend())
    print("belial devil_tag added: %d" % fix_belial_devil_tag())
