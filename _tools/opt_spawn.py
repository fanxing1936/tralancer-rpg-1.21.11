# -*- coding: utf-8 -*-
"""Collapse the per-tick mob-outfitting block in rpg:command/tick.

Originally each mob family cost 6-11 world-wide entity scans every tick (one per
line).  Rolling the per-mob work into a sub-function makes it 3, without
changing the order the game sees: the roll/summon pass still runs before the
gear pass, and the gear pass still picks up mobs summoned by the roll pass.
"""

import io
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FDIR = os.path.join(ROOT, "data", "rpg", "function", "command")
TICK = os.path.join(FDIR, "tick.mcfunction")

FAMILIES = [
    ("skeleton", "#minecraft:skeletons", "skeleton"),
    ("zombie", "#minecraft:zombies", "zombie"),
    ("creeper", "minecraft:creeper", "creeper"),
]


def strip_prefix(line, sel_re):
    """`execute as @e[<sel>] ...` -> the part after the selector."""
    m = sel_re.match(line)
    return m.group(1) if m else None


def main():
    src = io.open(TICK, encoding="utf-8").read().split("\n")
    out = []
    written = {}
    i = 0
    while i < len(src):
        line = src[i]
        st = line.strip()
        handled = False
        for name, type_sel, tag in FAMILIES:
            head = "execute as @e[type=%s,tag=!%s] at @s store result score @s random run random value" % (type_sel, tag)
            if not st.startswith(head):
                continue
            roll, gear = ["execute " + st[st.index("store result"):]], []
            j = i + 1
            sel_prefix = "execute as @e[type=%s,tag=!%s," % (type_sel, tag)
            loot_prefix = "loot replace entity @e[type=%s,tag=!%s] " % (type_sel, tag)
            tag_line = "tag @e[type=%s] add %s" % (type_sel, tag)
            while j < len(src):
                s2 = src[j].strip()
                if not s2:
                    j += 1
                    continue
                if s2.startswith(sel_prefix):
                    rest = s2[len(sel_prefix):]
                    scores = re.match(r"scores=\{random=([0-9.]+)\}\] at @s run (.*)$", rest)
                    if not scores:
                        break
                    roll.append("execute if score @s random matches %s run %s"
                                % (scores.group(1), scores.group(2)))
                    j += 1
                    continue
                if s2.startswith(loot_prefix):
                    gear.append("loot replace entity @s " + s2[len(loot_prefix):])
                    j += 1
                    continue
                if s2 == tag_line:
                    j += 1
                    break
                break

            body = ["# Per-mob roll for a %s variant (was %d world-wide scans in rpg:command/tick)."
                    % (name, len(roll))] + roll
            written[name] = body
            out.append("execute as @e[type=%s,tag=!%s] at @s run function rpg:command/spawn/%s"
                       % (type_sel, tag, name))
            if gear:
                written[name + "_gear"] = [
                    "# Roll this mob's RPG gear.  Runs on a fresh selection so that mobs",
                    "# summoned by rpg:command/spawn/%s are outfitted too." % name,
                ] + gear
                out.append("execute as @e[type=%s,tag=!%s] run function rpg:command/spawn/%s_gear"
                           % (type_sel, tag, name + ""))
            out.append(tag_line)
            i = j
            handled = True
            break
        if handled:
            continue
        out.append(line)
        i += 1

    sdir = os.path.join(FDIR, "spawn")
    if not os.path.isdir(sdir):
        os.makedirs(sdir)
    for name, body in written.items():
        with io.open(os.path.join(sdir, name + ".mcfunction"), "w",
                     encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(body) + "\n")

    with io.open(TICK, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out))

    print("split out: %s" % ", ".join(sorted(written)))
    print("spawn batches capped: %d" % batch_spawn())


# How many newly-seen mobs may be outfitted in a single tick.  Each one costs
# four or five `loot replace entity` calls, and every one of those really does
# roll a loot table (random enchantments, random attribute rolls).  Unbounded,
# a `/summon`-ed wave -- or a spawner burst, or a chunk full of mobs streaming
# in -- puts the whole batch on one tick, which is exactly the stutter that
# shows up when mobs appear.  Spilling the remainder to the next tick is
# invisible in play (the gear lands a few hundredths of a second later) and
# turns a spike into a flat line.
BATCH = 4

SPAWN_RE = re.compile(
    r"^execute as @e\[type=(?P<type>[^,\]]+),tag=!(?P<tag>[^,\]]+)\] "
    r"(?P<at>at @s )?run function rpg:command/spawn/(?P<fn>\S+)$")


def batch_spawn():
    """Rewrite the emitted spawn block so each family does bounded work."""
    lines = io.open(TICK, encoding="utf-8").read().split("\n")
    out, i, capped = [], 0, 0
    while i < len(lines):
        m = SPAWN_RE.match(lines[i].strip())
        if not m:
            out.append(lines[i])
            i += 1
            continue
        type_sel, tag = m.group("type"), m.group("tag")
        # gather this family's run of lines plus its trailing blanket tag
        body, j = [], i
        while j < len(lines):
            mm = SPAWN_RE.match(lines[j].strip())
            if mm and mm.group("type") == type_sel and mm.group("tag") == tag:
                body.append((mm.group("at") or "", mm.group("fn")))
                j += 1
                continue
            if lines[j].strip() == "tag @e[type=%s] add %s" % (type_sel, tag):
                j += 1
            break
        if not body:
            out.append(lines[i])
            i += 1
            continue

        name = body[0][1]
        batch = ["# 每刻最多给 %d 只新生物配装。" % BATCH,
                 "# 一次性召唤一群时，如果不封顶，全部的战利品表掷点会挤在同一刻。",
                 "tag @e[type=%s,tag=!%s,limit=%d] add rpg.spawn.new"
                 % (type_sel, tag, BATCH)]
        for at, fn in body:
            batch.append("execute as @e[tag=rpg.spawn.new] %srun function "
                         "rpg:command/spawn/%s" % (at, fn))
        batch.append("tag @e[tag=rpg.spawn.new] add %s" % tag)
        batch.append("tag @e[tag=rpg.spawn.new] remove rpg.spawn.new")

        sdir = os.path.join(FDIR, "spawn")
        with io.open(os.path.join(sdir, name + "_batch.mcfunction"), "w",
                     encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(batch) + "\n")

        # the guard: `if entity ... limit=1` stops at the first new mob, so a
        # tick with nothing new never enters the function at all
        out.append("execute if entity @e[type=%s,tag=!%s,limit=1] run function "
                   "rpg:command/spawn/%s_batch" % (type_sel, tag, name))
        capped += 1
        i = j
    io.open(TICK, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return capped


if __name__ == "__main__":
    main()
