# -*- coding: utf-8 -*-
"""朗基努斯之枪: mace -> netherite_spear.

A spear called a spear should be one.  1.21.11 has the item, so the weapon
moves onto `minecraft:netherite_spear` and picks up the real polearm rendering
(flat sprite in the GUI, a dedicated in-hand model everywhere else).

Two things had to change with it:

* **The trigger.**  The skill fired through the `food` + `consumable` hack,
  which a spear ignores -- its own charge action wins, exactly as the fishing
  rod's cast did.  Since the spear's charge *is* a real use action,
  `minecraft:using_item` fires on it directly and the two components come off.
  ［王座］ counts `power_step` up on every repeat of that trigger, i.e. it is a
  hold-to-charge skill already, so the spear's charge maps onto it one to one
  and no cooldown is wanted here (unlike 路西法, whose skill fires once).
* **The model.**  `king_sword` hung off `huge_sword_handheld`; on a spear base
  it follows vanilla's shape instead, with a mirrored in-hand sprite.
* **The lunge.**  The holy spear is authored with Lunge III, using the native
  1.21.11 spear jab movement rather than a duplicate command-based dash.
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

CMD = 1110003
BASE = "netherite_spear"
ART = "king_sword"
LUNGE = 3

# The original five are kept as they were.  `supported_items` only gates the
# enchanting table and the anvil -- writing an enchantment straight into the
# `enchantments` component applies it regardless, and what decides whether it
# does anything is the effect it declares:
#   breach  -- minecraft:armor_effectiveness, slots [mainhand].  A generic
#              effect with no item condition, so it works on the spear.
#   thorns  -- minecraft:post_attack with enchanted: victim, slots [any].
#              Fires when the holder is struck, so it works here too.
#   density -- minecraft:smash_damage_per_fallen_block.  That effect only
#              feeds the mace's smash attack, which a spear does not have, so
#              this one shows in the tooltip but contributes nothing.  Kept
#              because the author asked for it; swap it for `lunge` (the
#              spear's own post-piercing dash) to make the slot do work.


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
    assert marker in line, "Longinus item has no enchantments component"
    return line.replace(marker, marker + "lunge:%d," % LUNGE, 1)


def convert_give():
    path = os.path.join(FUNC, "command/give/weapon.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    out, hits, found = [], 0, 0
    for line in s.split("\n"):
        if "朗基努斯之枪" not in line:
            out.append(line)
            continue
        found += 1
        if line.startswith("give @a mace["):
            line = "give @a %s[" % BASE + line[len("give @a mace["):]
            hits += 1
        assert line.startswith("give @a %s[" % BASE), "unexpected Longinus base item"
        line = strip_component(line, "food")
        line = strip_component(line, "consumable")
        out.append(add_lunge(line))
    assert found == 1, "Longinus give card is not unique"
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return hits


def convert_advancement():
    """The spear's charge is a real use action, so key off the item itself."""
    wj(os.path.join(ADV, "power.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {
                "items": "minecraft:" + BASE,
                "predicates": {"minecraft:custom_data": "{power_tag:1b}"},
            }}}},
        "rewards": {"function": "rpg:item/sword/legend/power/trigger"},
    })


def mirror(w, h, rgba):
    out = bytearray(w * h * 4)
    for y in range(h):
        for x in range(w):
            s = (y * w + x) * 4
            d = (y * w + (w - 1 - x)) * 4
            out[d:d + 4] = rgba[s:s + 4]
    return bytes(out)


def convert_models():
    w, h, rgba = P.read(os.path.join(RPG_TEX, ART + ".png"))
    P.write(os.path.join(RPG_TEX, ART + "_in_hand.png"), w, h, mirror(w, h, rgba))
    wj(os.path.join(RPG_MODELS, ART + ".json"),
       {"parent": "item/generated", "textures": {"layer0": "rpg:item/" + ART}})
    wj(os.path.join(RPG_MODELS, ART + "_in_hand.json"),
       {"parent": "minecraft:item/spear_in_hand",
        "textures": {"layer0": "rpg:item/" + ART + "_in_hand"}})

    mine = {"type": "minecraft:select",
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
        with zipfile.ZipFile(JAR) as z:
            doc = json.loads(
                z.read("assets/minecraft/items/%s.json" % BASE).decode("utf-8"))
    node = doc["model"]
    if (node.get("type") or "").split(":")[-1] != "range_dispatch":
        node = {"type": "minecraft:range_dispatch",
                "property": "minecraft:custom_model_data",
                "fallback": node, "entries": []}
        doc["model"] = node
    entries = node.setdefault("entries", [])
    entries[:] = [e for e in entries if e["threshold"] != CMD]
    entries.append({"threshold": CMD, "model": mine})
    entries.sort(key=lambda e: e["threshold"])
    wj(path, doc)

    # and take the now-unused branch back off the mace
    mace = os.path.join(MC_ITEMS, "mace.json")
    dropped = 0
    if os.path.isfile(mace):
        doc = json.load(io.open(mace, encoding="utf-8"))
        ent = doc.get("model", {}).get("entries")
        if isinstance(ent, list):
            before = len(ent)
            ent[:] = [e for e in ent if e["threshold"] != CMD]
            dropped = before - len(ent)
            if dropped:
                wj(mace, doc)
    return dropped


def main():
    hits = convert_give()
    convert_advancement()
    dropped = convert_models()
    print("longinus: give rewritten=%d  mace branch dropped=%d  base=%s cmd=%d lunge=%d"
          % (hits, dropped, BASE, CMD, LUNGE))


if __name__ == "__main__":
    main()
