# -*- coding: utf-8 -*-
"""Estimate per-tick cost of a data pack: how many entity-selector scans and
how many expensive NBT reads the `#minecraft:tick` chain performs each tick."""

import io
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"

FUNC_RE = re.compile(r"\bfunction\s+([a-z0-9_.-]+:[a-z0-9_./-]+)")
SEL_RE = re.compile(r"@[aeprsn](\[[^\]]*\])?")


def fpath(ref):
    ns, path = ref.split(":", 1)
    return os.path.join(ROOT, "data", ns, "function", path + ".mcfunction")


def read(ref):
    p = fpath(ref)
    if not os.path.isfile(p):
        return None
    with io.open(p, encoding="utf-8") as fh:
        return fh.read().split("\n")


def cost_of_selector(sel):
    """Rough relative cost of evaluating one selector once."""
    if sel.startswith("@s"):
        return 0
    body = sel[2:]
    if "nbt=" in body:
        return 40          # full NBT serialisation per candidate entity
    if body.startswith("[") and ("type=" in body and "#" not in body):
        return 2           # single entity type -> indexed lookup
    return 4               # full entity-list walk with a cheap predicate


def analyse(ref, seen, acc, depth=0):
    if ref in seen or depth > 12:
        return
    seen = seen | {ref}
    lines = read(ref)
    if lines is None:
        return
    for line in lines:
        st = line.strip()
        if not st or st.startswith("#"):
            continue
        acc["commands"] += 1
        for m in SEL_RE.finditer(st):
            acc["selector_cost"] += cost_of_selector(m.group(0))
            if "nbt=" in (m.group(1) or ""):
                acc["nbt_selectors"] += 1
        if re.search(r"\bdata get entity\b", st):
            acc["data_get_entity"] += 1
        if st.startswith("particle ") or " run particle " in st:
            acc["particle"] += 1
        for m in FUNC_RE.finditer(st):
            analyse(m.group(1), seen, acc, depth + 1)


def main():
    tag = os.path.join(ROOT, "data", "minecraft", "tags", "function", "tick.json")
    with io.open(tag, encoding="utf-8") as fh:
        roots = json.load(fh)["values"]

    total = {"commands": 0, "selector_cost": 0, "nbt_selectors": 0,
             "data_get_entity": 0, "particle": 0}
    for r in roots:
        acc = {"commands": 0, "selector_cost": 0, "nbt_selectors": 0,
               "data_get_entity": 0, "particle": 0}
        analyse(r, set(), acc)
        print("  %-42s commands=%-6d selector_cost=%-7d nbt_sel=%-5d data_get=%-4d particles=%d"
              % (r, acc["commands"], acc["selector_cost"], acc["nbt_selectors"],
                 acc["data_get_entity"], acc["particle"]))
        for k in total:
            total[k] += acc[k]
    print()
    print("  TOTAL per tick: commands=%d  selector_cost=%d  nbt-matching selectors=%d  "
          "data-get-entity=%d  particle cmds=%d"
          % (total["commands"], total["selector_cost"], total["nbt_selectors"],
             total["data_get_entity"], total["particle"]))


if __name__ == "__main__":
    main()
