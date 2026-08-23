# -*- coding: utf-8 -*-
"""Pull every RPG item out of the data pack into structured JSON for the guide."""

import io
import json
import os
import re
import sys

from snbt import Parser, ParseError, Comp, Lst, Str, Word
import mcfunc

PACK = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(PACK, "data/rpg/function")


def node_to_py(n):
    if isinstance(n, Str):
        return n.val
    if isinstance(n, Word):
        t = n.text
        if t in ("true", "false"):
            return t == "true"
        m = re.match(r"^(-?\d+(?:\.\d+)?)[bslfdBSLFD]?$", t)
        if m:
            v = m.group(1)
            return float(v) if "." in v else int(v)
        return t
    if isinstance(n, Lst):
        return [node_to_py(x) for x in n.items]
    if isinstance(n, Comp):
        return dict((n.keytext(k), node_to_py(v)) for k, v in n.items)
    return None


def flatten(tc):
    """Text component -> (plain text, list of (text, colour)) ."""
    parts = []

    def walk(node, inherited=None):
        if isinstance(node, list):
            for x in node:
                walk(x, inherited)
            return
        if isinstance(node, str):
            if node:
                parts.append((node, inherited))
            return
        if isinstance(node, dict):
            colour = node.get("color", inherited)
            if node.get("text"):
                parts.append((node["text"], colour))
            if "translate" in node and "text" not in node:
                parts.append(("{%s}" % node["translate"], colour))
            for x in node.get("extra", []):
                walk(x, colour)

    walk(tc)
    return "".join(p[0] for p in parts), parts


RARITY = {
    "[legend]": ("传说", "gold"), "[epic]": ("史诗", "dark_purple"),
    "[DEVIL]": ("恶魔", "dark_red"), "[brave]": ("勇者", "aqua"),
    "[HOLY]": ("神圣", "yellow"), "[rare]": ("稀有", "blue"),
}

GIVE_RE = re.compile(r"^give\s+\S+\s+([a-z0-9_:]+)\[")


def parse_give(line):
    m = GIVE_RE.match(line.strip())
    if not m:
        return None
    item_id = m.group(1)
    i = line.index("[", m.end() - 1)
    try:
        p = Parser(line, i)
        block = p.component_block()
    except ParseError:
        return None
    comps = {}
    for name, value, neg, sep in block.entries:
        if value is not None:
            comps[name.split(":")[-1]] = node_to_py(value)
    return item_id, comps


def describe(item_id, c):
    name_tc = c.get("custom_name")
    plain, parts = flatten(name_tc) if name_tc is not None else ("", [])
    rarity = None
    display = plain
    for tag, (label, colour) in RARITY.items():
        if plain.startswith(tag):
            rarity = label
            display = plain[len(tag):]
            break
    if rarity is None and parts:
        m = re.match(r"^\[([^\]]+)\]", plain)
        if m:
            rarity = m.group(1)
            display = plain[m.end():]

    lore = []
    for l in c.get("lore", []) or []:
        t, _ = flatten(l)
        lore.append(t)

    mods = []
    for m in c.get("attribute_modifiers", []) or []:
        if isinstance(m, dict):
            mods.append({"attr": m.get("type"), "amount": m.get("amount"),
                         "op": m.get("operation"), "slot": m.get("slot", "any")})

    return {
        "item": item_id,
        "name": display.strip(),
        "rarity": rarity,
        "name_colour": parts[-1][1] if parts else None,
        "lore": lore,
        # 基础物品 id。图鉴用它分武器/护甲 —— 早先分类看的是 custom_data 里的
        # bow_tag/sword_tag，可那些是**玩法开关**（bow_tag 会给箭加速并召苦力怕），
        # 一旦某件武器出于玩法原因不该带那个开关，它就会从武器图鉴里消失。
        "id": item_id,
        "enchantments": c.get("enchantments") or {},
        "modifiers": mods,
        "tags": sorted((c.get("custom_data") or {}).keys()),
        "custom_data": c.get("custom_data") or {},
        "cmd": (c.get("custom_model_data") or {}).get("floats", [None])[0],
        "unbreakable": "unbreakable" in c,
        "consumable": (c.get("consumable") or {}).get("consume_seconds"),
        "components": sorted(c.keys()),
        # kept verbatim because the icon renderer has to reproduce exactly what
        # the client draws: the dye tint on leather, the trim overlay and its
        # material palette, and the potion colour
        "dyed_color": c.get("dyed_color"),
        "trim": c.get("trim"),
        "potion_contents": c.get("potion_contents"),
    }


def main():
    out = {}
    for rel in ("command/give/weapon.mcfunction", "command/give/item.mcfunction",
                "command/give/weapon_up_item.mcfunction",
                "command/give/extra.mcfunction"):
        path = os.path.join(FUNC, rel)
        if not os.path.isfile(path):
            continue
        bucket = []
        for line in io.open(path, encoding="utf-8"):
            got = parse_give(line)
            if got:
                bucket.append(describe(*got))
        out[rel] = bucket
        print("%-42s %d items" % (rel, len(bucket)))

    with io.open("../_data_items.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
