# -*- coding: utf-8 -*-
"""Where does the per-tick cost actually sit now?

Breaks the #minecraft:tick chain down per function and per selector shape, and
flags blocks of consecutive lines that all open with the same world-wide `@e`
walk -- those are the ones a single guard can collapse.
"""

import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC_RE = re.compile(r"\bfunction\s+([a-z0-9_.-]+:[a-z0-9_./-]+)")
SEL_RE = re.compile(r"@[aeprsn](\[[^\]]*\])?")
HEAD_RE = re.compile(r"^execute\s+(?:as|if entity|unless entity)\s+(@[aeprsn](?:\[[^\]]*\])?)")


def path_of(ref):
    ns, path = ref.split(":", 1)
    return os.path.join(ROOT, "data", ns, "function", path + ".mcfunction")


def lines_of(ref):
    p = path_of(ref)
    if not os.path.isfile(p):
        return None
    return io.open(p, encoding="utf-8").read().split("\n")


def kind(sel):
    """How expensive is one evaluation of this selector?"""
    if sel.startswith("@s"):
        return "self"
    body = sel[2:]
    if "nbt=" in body:
        return "nbt-scan"
    if sel.startswith("@a"):
        return "players"
    if re.search(r"type=(?!!)[a-z0-9_:]+", body) and "#" not in body:
        return "typed"
    return "world-walk"


COST = {"self": 0, "players": 1, "typed": 2, "world-walk": 4, "nbt-scan": 40}

GUARD_RE = re.compile(
    r"^execute if entity (@e\[[^\]]*\]) run function\s+([a-z0-9_.-]+:[a-z0-9_./-]+)$")


def walk(ref, seen, per_fn, order, guarded=False):
    if ref in seen:
        return
    seen.add(ref)
    ls = lines_of(ref)
    if ls is None:
        return
    order.append(ref)
    counts = Counter()
    heads = Counter()
    run, prev = 0, None
    runs = []
    for line in ls:
        st = line.strip()
        if not st or st.startswith("#"):
            continue
        counts["commands"] += 1
        for m in SEL_RE.finditer(st):
            k = kind(m.group(0))
            counts[k] += 1
            counts["cost"] += COST[k]
        h = HEAD_RE.match(st)
        head = h.group(1) if h else None
        if head and kind(head) in ("world-walk", "typed", "players"):
            heads[head] += 1
        if head == prev:
            run += 1
        else:
            if prev and run >= 8:
                runs.append((run, prev))
            prev, run = head, 1
        g = GUARD_RE.match(st)
        if g:
            # the body only runs when the tag is actually populated
            counts["guards"] += 1
            walk(g.group(2), seen, per_fn, order, guarded=True)
            continue
        for m in FUNC_RE.finditer(st):
            walk(m.group(1), seen, per_fn, order, guarded)
    if prev and run >= 8:
        runs.append((run, prev))
    counts["guarded"] = 1 if guarded else 0
    per_fn[ref] = (counts, heads, runs)


def main():
    tag = os.path.join(ROOT, "data", "minecraft", "tags", "function", "tick.json")
    roots = json.load(io.open(tag, encoding="utf-8"))["values"]
    per_fn, order, seen = {}, [], set()
    for r in roots:
        walk(r, seen, per_fn, order)

    tot, idle = Counter(), Counter()
    for c, _h, _r in per_fn.values():
        tot.update(c)
        if not c["guarded"]:
            idle.update(c)
    # idle also pays one walk per guard that turns out to be empty
    idle_walks = idle["world-walk"] + tot["guards"]
    print("worst case (everything firing): %d commands, cost %d, world-walks %d"
          % (tot["commands"], tot["cost"], tot["world-walk"]))
    print("idle  (nothing hurt, no boss, no arrows): %d commands, world-walks %d"
          % (idle["commands"] + tot["guards"], idle_walks))
    print("  guards: %d   lines behind them: %d"
          % (tot["guards"], tot["commands"] - idle["commands"]))
    print("  self %d | players %d | typed %d | world-walk %d | nbt-scan %d"
          % (tot["self"], tot["players"], tot["typed"], tot["world-walk"], tot["nbt-scan"]))

    print("\n-- heaviest functions --")
    rows = sorted(per_fn.items(), key=lambda kv: -kv[1][0]["cost"])[:10]
    for ref, (c, _h, _r) in rows:
        print("  %-46s cmds %-5d cost %-6d walks %-5d typed %-4d"
              % (ref, c["commands"], c["cost"], c["world-walk"], c["typed"]))

    print("\n-- guardable runs (>=8 consecutive lines opening on the same walk) --")
    total_guardable = 0
    for ref, (_c, _h, runs) in per_fn.items():
        for n, head in sorted(runs, reverse=True):
            if kind(head) == "world-walk":
                total_guardable += n
                print("  %-46s %3d x %s" % (ref, n, head[:52]))
    print("  -> %d lines sit behind a repeated world-walk" % total_guardable)


if __name__ == "__main__":
    main()
