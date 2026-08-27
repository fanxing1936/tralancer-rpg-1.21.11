# -*- coding: utf-8 -*-
"""Pull the randomly-rolled items out of the loot tables.

Unlike the `give` functions, these items have ranged attributes (uniform min/max)
and random enchantments, so each entry is a *template* rather than a fixed item.
"""

import io
import json
import os
import re
import sys
from snbt import parse_value
from extract_items import node_to_py

PACK = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
ROOT = os.path.join(PACK, "data/rpg/loot_table")


def flatten(tc):
    """Loot-table text components -> plain string."""
    out = []

    def walk(n):
        if isinstance(n, list):
            for x in n:
                walk(x)
        elif isinstance(n, str):
            out.append(n)
        elif isinstance(n, dict):
            if isinstance(n.get("text"), str):
                out.append(n["text"])
            if "translate" in n and "text" not in n:
                out.append("{%s}" % n["translate"])
            if "score" in n:
                out.append("<%s>" % n["score"].get("objective", "?"))
            for x in n.get("extra", []):
                walk(x)
    walk(tc)
    return "".join(out)


def num(v):
    """A loot number provider -> (min, max) or a single value."""
    if isinstance(v, (int, float)):
        return (v, v)
    if isinstance(v, dict):
        t = (v.get("type") or "").split(":")[-1]
        if t in ("uniform", "") and "min" in v:
            return (v["min"], v["max"])
        if t == "constant":
            return (v["value"], v["value"])
        if t == "binomial":
            return (0, v.get("n"))
    return None


def fname(f):
    return (f.get("function") or "").split(":")[-1]


def read_entry(e):
    it = {"item": e.get("name", "?"), "weight": e.get("weight", 1),
          "name": None, "lore": [], "attrs": [], "ench": [], "tags": {},
          "damage": None, "count": None, "components": {}}
    for f in e.get("functions", []):
        n = fname(f)
        if n == "set_name":
            it["name"] = flatten(f.get("name"))
        elif n == "set_lore":
            it["lore"] += [flatten(l) for l in f.get("lore", [])]
        elif n == "set_attributes":
            for m in f.get("modifiers", []):
                it["attrs"].append({
                    "attr": m.get("attribute"), "op": m.get("operation"),
                    "slot": m.get("slot", "any"), "range": num(m.get("amount")),
                })
        elif n == "enchant_randomly":
            opts = f.get("options")
            it["ench"].append(opts if opts else "任意附魔")
        elif n == "enchant_with_levels":
            it["ench"].append("附魔台等价 %s" % (num(f.get("levels")),))
        elif n == "set_custom_data":
            tag = f.get("tag", {})
            if isinstance(tag, str):
                tag = node_to_py(parse_value(tag)[0])
            it["tags"].update(tag)
        elif n == "set_damage":
            it["damage"] = num(f.get("damage"))
        elif n == "set_count":
            it["count"] = num(f.get("count"))
        elif n == "set_components":
            it["components"].update(f.get("components", {}))
    return it


def read_table(path):
    doc = json.load(io.open(path, encoding="utf-8"))
    pools = []
    for p in doc.get("pools", []):
        entries = []
        for e in p.get("entries", []):
            t = (e.get("type") or "").split(":")[-1]
            if t == "item":
                entries.append(read_entry(e))
            elif t == "loot_table":
                entries.append({"item": "→ " + str(e.get("value") or e.get("name")),
                                "weight": e.get("weight", 1), "name": None,
                                "lore": [], "attrs": [], "ench": [], "tags": {},
                                "damage": None, "count": None, "components": {},
                                "ref": True})
            elif t == "tag":
                entries.append({"item": "#" + str(e.get("name")), "weight": e.get("weight", 1),
                                "name": None, "lore": [], "attrs": [], "ench": [],
                                "tags": {}, "damage": None, "count": None,
                                "components": {}, "ref": True})
        pools.append({"rolls": num(p.get("rolls")), "entries": entries,
                      "conditions": len(p.get("conditions", []))})
    return pools


def main():
    out = {}
    for dirpath, _d, files in os.walk(ROOT):
        for fn in sorted(files):
            if not fn.endswith(".json"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/")
            out["rpg:" + rel[:-5]] = read_table(os.path.join(dirpath, fn))

    total = sum(len(p["entries"]) for t in out.values() for p in t)
    named = sum(1 for t in out.values() for p in t for e in p["entries"] if e["name"])
    print("tables %d   entries %d   named %d" % (len(out), total, named))
    json.dump(out, io.open("../_data_loot.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
