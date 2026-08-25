# -*- coding: utf-8 -*-
"""如意金箍棒: mace -> netherite_spear, with native spear rendering.

The weapon already behaves like a long polearm, and Java 1.21.11 has a real
Netherite Spear.  Move the generated item onto that base, replace the old
consumable right-click shim with the spear's native using-item trigger, give it
Lunge III, and dispatch its existing art through separate GUI/in-hand models.
"""

import io
import json
import os
import sys

import png_tool as P

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

RPG_MODELS = os.path.join(RP, "assets/rpg/models/item")
RPG_TEX = os.path.join(RP, "assets/rpg/textures/item")
MC_ITEMS = os.path.join(RP, "assets/minecraft/items")
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement/item")
JAR = r"F:/筑梦 MCBE/HMCL启动器/新建文件夹/versions/1.21.11-Fabric/1.21.11-Fabric.jar"

CMD = 1110004
BASE = "netherite_spear"
ART = "long_stick"
LUNGE = 3


def wj(path, doc):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def strip_component(line, name):
    """Remove `name={...}` from an item-component list, brace-aware."""
    key = name + "="
    i = line.find(key)
    if i < 0:
        return line
    j = i + len(key)
    if j < len(line) and line[j] == "{":
        depth = 0
        while j < len(line):
            if line[j] == "{":
                depth += 1
            elif line[j] == "}":
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
    else:
        while j < len(line) and line[j] not in ",]":
            j += 1
    if j < len(line) and line[j] == ",":
        j += 1
    elif i > 0 and line[i - 1] == ",":
        i -= 1
    return line[:i] + line[j:]


def add_lunge(line):
    if "lunge:" in line:
        return line
    marker = "enchantments={"
    assert marker in line, "Wukong item has no enchantments component"
    return line.replace(marker, marker + "lunge:%d," % LUNGE, 1)


def convert_give():
    path = os.path.join(FUNC, "command/give/weapon.mcfunction")
    src = io.open(path, encoding="utf-8").read()
    out, hits = [], 0
    found = 0
    for line in src.split("\n"):
        if "如意金箍棒" not in line:
            out.append(line)
            continue
        found += 1
        if line.startswith("give @a mace["):
            line = "give @a %s[" % BASE + line[len("give @a mace["):]
            hits += 1
        assert line.startswith("give @a %s[" % BASE), "unexpected Wukong base item"
        line = strip_component(line, "food")
        line = strip_component(line, "consumable")
        out.append(add_lunge(line))
    assert found == 1, "Wukong give card is not unique"
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return hits


def convert_advancement():
    """The native spear use action replaces the old fake-food trigger."""
    wj(os.path.join(ADV, "wukong.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {
                "items": "minecraft:" + BASE,
                "predicates": {"minecraft:custom_data": "{wukong_tag:1b}"},
            }}}},
        "rewards": {"function": "rpg:item/sword/legend/wukong/fly"},
    })


def mirror(w, h, rgba):
    out = bytearray(w * h * 4)
    for y in range(h):
        for x in range(w):
            src = (y * w + x) * 4
            dst = (y * w + (w - 1 - x)) * 4
            out[dst:dst + 4] = rgba[src:src + 4]
    return bytes(out)


def convert_models():
    w, h, rgba = P.read(os.path.join(RPG_TEX, ART + ".png"))
    P.write(os.path.join(RPG_TEX, ART + "_in_hand.png"), w, h, mirror(w, h, rgba))
    wj(os.path.join(RPG_MODELS, ART + ".json"),
       {"parent": "item/generated", "textures": {"layer0": "rpg:item/" + ART}})
    wj(os.path.join(RPG_MODELS, ART + "_in_hand.json"),
       {"parent": "minecraft:item/spear_in_hand",
        "textures": {"layer0": "rpg:item/" + ART + "_in_hand"}})

    model = {"type": "minecraft:select",
             "property": "minecraft:display_context",
             "cases": [{"when": ["gui", "ground", "fixed", "on_shelf"],
                        "model": {"type": "minecraft:model",
                                  "model": "rpg:item/" + ART}}],
             "fallback": {"type": "minecraft:model",
                          "model": "rpg:item/" + ART + "_in_hand"}}

    path = os.path.join(MC_ITEMS, BASE + ".json")
    if os.path.isfile(path):
        doc = json.load(io.open(path, encoding="utf-8"))
    else:
        import zipfile
        with zipfile.ZipFile(JAR) as jar:
            doc = json.loads(jar.read(
                "assets/minecraft/items/%s.json" % BASE).decode("utf-8"))
    node = doc["model"]
    if (node.get("type") or "").split(":")[-1] != "range_dispatch":
        node = {"type": "minecraft:range_dispatch",
                "property": "minecraft:custom_model_data",
                "fallback": node, "entries": []}
        doc["model"] = node
    entries = node.setdefault("entries", [])
    entries[:] = [e for e in entries if e["threshold"] != CMD]
    entries.append({"threshold": CMD, "model": model})
    entries.sort(key=lambda e: e["threshold"])
    wj(path, doc)

    mace = os.path.join(MC_ITEMS, "mace.json")
    dropped = 0
    if os.path.isfile(mace):
        doc = json.load(io.open(mace, encoding="utf-8"))
        entries = doc.get("model", {}).get("entries")
        if isinstance(entries, list):
            before = len(entries)
            entries[:] = [e for e in entries if e["threshold"] != CMD]
            dropped = before - len(entries)
            if dropped:
                wj(mace, doc)
    return dropped


def main():
    hits = convert_give()
    convert_advancement()
    dropped = convert_models()
    print("wukong: give rewritten=%d  mace branch dropped=%d  base=%s cmd=%d lunge=%d"
          % (hits, dropped, BASE, CMD, LUNGE))


if __name__ == "__main__":
    main()
