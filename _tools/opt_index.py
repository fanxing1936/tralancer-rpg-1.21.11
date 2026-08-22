# -*- coding: utf-8 -*-
"""Turn the flag index inside out: iterate each population once, not once per flag.

The generated index clears and then sets ~110 player flags and ~50 dropped-item
flags, each on its own `@a` / `@e[type=item]` line -- so the player list gets
walked ~110 times and the item list ~50 times every tick, to do work that is
entirely per-entity.

Rewriting it as `execute as <population> run function <body>` with every line
inside operating on `@s` costs exactly one walk per population.  Each entity
still gets its clears before its sets, and tags are per-entity and independent,
so the resulting tag state is identical.
"""

import io
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(ROOT, "data/rpg/function/command")
INDEX = os.path.join(FUNC, "index.mcfunction")

CLEAR_RE = re.compile(r"^tag (@[aes](?:\[[^\]]*\])?) remove ([A-Za-z0-9_.+-]+)$")
SET_RE = re.compile(
    r"^execute as (@[aes](?:\[[^\]]*\])?) if items entity @s (\S+) (\*\[[^\]]*\]) "
    r"run tag @s add ([A-Za-z0-9_.+-]+)$")

BODY = {"@a": "index_player", "@e[type=minecraft:item]": "index_item"}


def main():
    if not os.path.isfile(INDEX):
        print("no index to fold")
        return
    lines = io.open(INDEX, encoding="utf-8").read().split("\n")

    clears, sets, rest = {}, {}, []
    for l in lines:
        st = l.strip()
        m = CLEAR_RE.match(st)
        if m and m.group(1) in BODY:
            clears.setdefault(m.group(1), []).append(m.group(2))
            continue
        m = SET_RE.match(st)
        if m and m.group(1) in BODY:
            sets.setdefault(m.group(1), []).append((m.group(2), m.group(3), m.group(4)))
            continue
        rest.append(l)

    if not sets:
        print("index already folded")
        return

    folded = 0
    head = ["# Auto-generated per-tick flag index.",
            "# 每个族群只遍历一次：清标记与判定都在 @s 上完成，",
            "# 于是玩家表每刻只走一遍、掉落物表也只走一遍。", ""]
    calls = []
    for sel, name in BODY.items():
        if sel not in sets:
            continue
        body = ["# %s 的全部 custom_data 标记，逐个实体一次算完。" % sel, ""]
        body += ["tag @s remove %s" % t for t in clears.get(sel, [])]
        body.append("")
        body += ["execute if items entity @s %s %s run tag @s add %s" % (slot, pred, tag)
                 for slot, pred, tag in sets[sel]]
        io.open(os.path.join(FUNC, name + ".mcfunction"), "w",
                encoding="utf-8", newline="\n").write("\n".join(body).rstrip("\n") + "\n")
        calls.append("execute as %s run function rpg:command/%s" % (sel, name))
        folded += len(clears.get(sel, [])) + len(sets[sel])

    # the per-scope headings described blocks that no longer exist here
    stale = ("# Auto-generated", "# Each custom_data", "# The pack tests",
             "# selectors.", "# the whole entity", "# which reads", "# Runs first",
             "## main-hand", "## off-hand", "## worn", "## dropped")
    tail = [l for l in rest
            if l.strip() and not any(l.strip().startswith(x) for x in stale)]
    out = head + calls + [""] + tail
    io.open(INDEX, "w", encoding="utf-8", newline="\n").write(
        "\n".join(out).rstrip("\n") + "\n")
    print("index folded: %d lines -> %d population walks" % (folded, len(calls)))


if __name__ == "__main__":
    main()
