# -*- coding: utf-8 -*-
"""Structural sanity checks over a migrated data pack."""

import io
import json
import os
import re
import sys

from snbt import Parser, ParseError, Comp, Lst, Str, Word
import mcfunc

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"

problems = []
LEGACY = {
    "ArmorItems": r"ArmorItems",
    "HandItems": r"HandItems",
    "DropChances": r"(Armor|Hand)DropChances",
    "body_armor_item": r"body_armor_item",
    "SaddleItem": r"SaddleItem",
    "show_in_tooltip": r"show_in_tooltip",
    "fire_resistant": r"fire_resistant",
    "eat_seconds": r"eat_seconds",
    "enchantments.levels": r"enchantments\s*[=:]\s*\{\s*levels",
    "attribute_modifiers.modifiers": r"attribute_modifiers\s*[=:]\s*\{\s*modifiers",
    "dyed_color.rgb": r"dyed_color\s*[=:]\s*\{\s*rgb",
    "attribute category prefix": r'"(generic|horse|zombie)\.[a-z_]+"',
    "Count in stack": r"\bCount\s*:",
}


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


# ---------------------------------------------------------------------------
def check_equipment(node, where):
    if isinstance(node, Comp):
        eq = node.get("equipment")
        if isinstance(eq, Comp):
            for k, v in eq.items:
                if not (isinstance(v, Comp) and v.has("id")):
                    problems.append("%s: equipment.%s has no item id" %
                                    (where, eq.keytext(k)))
        for _, v in node.items:
            check_equipment(v, where)
    elif isinstance(node, Lst):
        for v in node.items:
            check_equipment(v, where)


def scan_nbt(line, where):
    """Re-parse every NBT/component region; report anything that fails."""
    i, n = 0, len(line)
    while i < n:
        c = line[i]
        if c in ('"', "'"):
            i = mcfunc.skip_string(line, i)
            continue
        if c == "{":
            try:
                p = Parser(line, i)
                node = p.compound()
                check_equipment(node, where)
                i = p.i
                continue
            except ParseError as exc:
                problems.append("%s: unparsable compound (%s)" % (where, exc))
                return
        if c == "[":
            prev2 = line[max(0, i - 2):i]
            if mcfunc.SELECTOR_RE.search(prev2):
                _t, i = mcfunc.selector_region(line, i)
                continue
            prev = line[i - 1] if i else ""
            try:
                p = Parser(line, i)
                if prev in mcfunc.WORDCH:
                    p.component_block()
                else:
                    node = p.list()
                    check_equipment(node, where)
                i = p.i
                continue
            except ParseError as exc:
                problems.append("%s: unparsable bracket (%s)" % (where, exc))
                return
        i += 1


# ---------------------------------------------------------------------------
functions = set()
resources = {"loot_table": set(), "item_modifier": set(), "advancement": set(),
             "predicate": set(), "trim_material": set(), "trial_spawner": set()}

for dirpath, _d, files in os.walk(ROOT):
    for fn in files:
        r = rel(os.path.join(dirpath, fn))
        m = re.match(r"data/([^/]+)/(function|loot_table|item_modifier|advancement|"
                     r"predicate|trim_material|trial_spawner)/(.+)\.(mcfunction|json)$", r)
        if m:
            ns, kind, path, _ext = m.groups()
            if kind == "function":
                functions.add(ns + ":" + path)
            else:
                resources[kind].add(ns + ":" + path)

REFS = [
    (re.compile(r"\bfunction\s+([a-z0-9_.-]+:[a-z0-9_./-]+)"), functions, "function"),
    (re.compile(r"\bloot\s+([a-z0-9_.-]+:[a-z0-9_./-]+)"), resources["loot_table"], "loot table"),
    (re.compile(r"\bcontents\s+([a-z0-9_.-]+:[a-z0-9_./-]+)"), resources["item_modifier"], "item modifier"),
    (re.compile(r"\badvancement\s+(?:grant|revoke)\s+\S+\s+(?:only|through|from|until)\s+([a-z0-9_.-]+:[a-z0-9_./-]+)"),
     resources["advancement"], "advancement"),
]

for dirpath, _d, files in os.walk(ROOT):
    for fn in files:
        path = os.path.join(dirpath, fn)
        r = rel(path)
        if fn.endswith(".mcfunction"):
            with io.open(path, encoding="utf-8") as fh:
                for ln, line in enumerate(fh.read().split("\n"), 1):
                    st = line.strip()
                    if not st or st.startswith("#"):
                        continue
                    where = "%s:%d" % (r, ln)
                    # 宏行（$ 开头）里的 $(name) 要到运行时才替换，
                    # 静态解析括号必然失败 —— 跳过语法扫描，只留引用检查。
                    if not st.startswith("$"):
                        scan_nbt(line, where)
                    for name, pat in LEGACY.items():
                        if re.search(pat, line) and "entity.generic." not in line:
                            problems.append("%s: legacy %s" % (where, name))
                    for rx, pool, kind in REFS:
                        for mm in rx.finditer(line):
                            ref = mm.group(1)
                            if ref.startswith("minecraft:"):
                                continue
                            if ref not in pool:
                                problems.append("%s: missing %s %s" % (where, kind, ref))
        elif fn.endswith(".json"):
            try:
                doc = json.load(io.open(path, encoding="utf-8"))
            except ValueError as exc:
                problems.append("%s: bad JSON %s" % (r, exc))
                continue
            blob = json.dumps(doc, ensure_ascii=False)
            for name, pat in LEGACY.items():
                if name == "Count in stack":
                    continue
                if re.search(pat, blob) and "entity.generic." not in blob:
                    problems.append("%s: legacy %s" % (r, name))

print("functions: %d   loot tables: %d   item modifiers: %d   advancements: %d"
      % (len(functions), len(resources["loot_table"]),
         len(resources["item_modifier"]), len(resources["advancement"])))
if problems:
    print("\n%d problems:" % len(problems))
    for p in problems[:80]:
        print("  " + p)
    # build.sh uses `set -e`; validation must therefore return failure, not
    # merely print a red-looking report and let packaging continue.
    sys.exit(1)
else:
    print("\nno problems found")
