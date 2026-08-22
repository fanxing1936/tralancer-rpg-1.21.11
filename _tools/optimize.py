# -*- coding: utf-8 -*-
"""Performance pass.

The pack's hot loops re-match the same NBT over and over: 640 selectors read
`SelectedItem` off every player, 495 read `Item` off every dropped item, and
another ~140 read `Tags`/`equipment`.  Every one of those forces Minecraft to
serialise the whole entity to NBT.  This pass computes each distinct flag once
per tick into an entity tag and rewrites the selectors to test the tag instead.
"""

import io
import json
import os
import re
import sys

from snbt import Parser, ParseError, Comp, Lst, Str, Word
import mcfunc

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"

STATS = {}


def bump(k, n=1):
    STATS[k] = STATS.get(k, 0) + n


# --- index registry ---------------------------------------------------------
# tag name -> (scope, slot_source, custom_data key, value)
INDEX = {}
SCOPE_SELECTOR = {
    "held": "@a",
    "worn": "@a",
    "item": "@e[type=minecraft:item]",
}
SCOPE_TITLE = {
    "held": "main-hand item flags",
    "worn": "worn armour / offhand flags",
    "item": "dropped item flags",
}
# entity `equipment` slot name -> the slot_source name `execute if items` wants
SLOT_SOURCE = {
    "head": "armor.head", "chest": "armor.chest", "legs": "armor.legs",
    "feet": "armor.feet", "offhand": "weapon.offhand",
    "mainhand": "weapon.mainhand", "body": "armor.body", "saddle": "saddle",
}


def single(node, key):
    """If `node` is a compound with exactly one entry named `key`, return it."""
    if isinstance(node, Comp) and len(node.items) == 1:
        k, v = node.items[0]
        if node.keytext(k) == key:
            return v
    return None


def only_entry(node):
    if isinstance(node, Comp) and len(node.items) == 1:
        k, v = node.items[0]
        return node.keytext(k), v
    return None, None


def custom_data_flag(node):
    """`{components:{"minecraft:custom_data":{key:1b}}}` -> ("key", "1")."""
    comps = single(node, "components")
    if comps is None:
        return None
    cd = single(comps, "minecraft:custom_data")
    if cd is None:
        cd = single(comps, "custom_data")
    if cd is None:
        return None
    key, val = only_entry(cd)
    if key is None or not isinstance(val, Word):
        return None
    v = val.text.rstrip("bBsSlL")
    if not re.match(r"^-?\d+$", v):
        return None
    return key, v


SLOTS = ("head", "chest", "legs", "feet", "offhand", "mainhand", "body", "saddle")


def classify(node):
    """Return (scope, tag, slot_source, key, value) for an indexable nbt= value."""
    inner = single(node, "SelectedItem")
    if inner is not None:
        flag = custom_data_flag(inner)
        if flag:
            return "held", "rpg.h.%s%s" % flag, "weapon.mainhand", flag[0], flag[1]

    inner = single(node, "Item")
    if inner is not None:
        flag = custom_data_flag(inner)
        if flag:
            return "item", "rpg.i.%s%s" % flag, "contents", flag[0], flag[1]

    inner = single(node, "equipment")
    if inner is not None:
        slot, stack = only_entry(inner)
        if slot in SLOTS:
            flag = custom_data_flag(stack)
            if flag:
                return ("worn", "rpg.e.%s_%s%s" % (slot, flag[0], flag[1]),
                        SLOT_SOURCE[slot], flag[0], flag[1])
    return (None,) * 5


def register(info):
    scope, tag, slot, key, val = info
    if tag not in INDEX:
        INDEX[tag] = (scope, slot, key, val)


# --- selector rewriting -----------------------------------------------------

def rewrite_selector_body(inner):
    """Replace indexable `nbt=` terms inside one selector body with `tag=`."""
    out = []
    j = 0
    while j < len(inner):
        c = inner[j]
        if c in ('"', "'"):
            k = mcfunc.skip_string(inner, j)
            out.append(inner[j:k])
            j = k
            continue
        if inner.startswith("nbt=", j) and (j == 0 or inner[j - 1] == ","):
            start = j
            j += 4
            neg = False
            if j < len(inner) and inner[j] == "!":
                neg = True
                j += 1
            try:
                p = Parser(inner, j)
                node = p.value()
            except ParseError:
                out.append(inner[start:j])
                continue
            end = p.i

            tags = single(node, "Tags")
            if isinstance(tags, Lst) and all(isinstance(t, Str) for t in tags.items):
                if not neg:
                    bump("Tags nbt match -> tag=")
                    out.append(",".join("tag=" + t.val for t in tags.items))
                    j = end
                    continue
                if len(tags.items) == 1:
                    bump("Tags nbt match -> tag=")
                    out.append("tag=!" + tags.items[0].val)
                    j = end
                    continue

            info = classify(node)
            scope, tag = info[0], info[1]
            if tag:
                register(info)
                bump("%s nbt match -> tag=" % scope)
                out.append("tag=" + ("!" if neg else "") + tag)
                j = end
                continue

            # a single nbt= term testing several independent flags
            if not neg and isinstance(node, Comp) and len(node.items) > 1:
                parts = []
                for k, v in node.items:
                    sub = Comp([(k, v)])
                    info = classify(sub)
                    if not info[1]:
                        parts = None
                        break
                    register(info)
                    parts.append("tag=" + info[1])
                if parts:
                    bump("compound nbt match -> tag=")
                    out.append(",".join(parts))
                    j = end
                    continue

            bump("nbt match left as-is")
            out.append(inner[start:end])
            j = end
            continue
        out.append(c)
        j += 1
    return "".join(out)


def rewrite_line(line):
    st = line.strip()
    if not st or st.startswith("#"):
        return line
    out = []
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        if c in ('"', "'"):
            k = mcfunc.skip_string(line, i)
            out.append(line[i:k])
            i = k
            continue
        if c == "[" and mcfunc.SELECTOR_RE.search(line[max(0, i - 2):i]):
            end = mcfunc.match_bracket(line, i)
            body = rewrite_selector_body(line[i + 1:end - 1])
            if line[i - 2:i] == "@e":
                # the index only ever puts these tags on one population, so the
                # world-wide @e walk can be narrowed without changing results
                if re.search(r"(^|,)tag=rpg\.(h|e)\.", body):
                    bump("@e narrowed to @a")
                    out[-1] = "a"
                elif re.search(r"(^|,)tag=rpg\.i\.", body) and "type=" not in body:
                    bump("@e narrowed to item entities")
                    body = "type=minecraft:item," + body
            out.append("[" + body + "]")
            i = end
            continue
        if c in "{[":
            # skip whole NBT / component regions so we never touch their insides
            end = mcfunc.match_bracket(line, i)
            out.append(line[i:end])
            i = end
            continue
        out.append(c)
        i += 1
    return "".join(out)


# --- index function ---------------------------------------------------------

def write_index():
    lines = [
        "# Auto-generated per-tick flag index.",
        "# The pack tests the same handful of custom_data flags from hundreds of",
        "# selectors.  Written as nbt={...} each of those makes the game serialise",
        "# the whole entity; here every flag is resolved once with `if items`,",
        "# which reads the slot directly, and cached as an entity tag.",
        "# Runs first in #minecraft:tick.",
        "",
    ]
    by_scope = {}
    for tag, (scope, slot, key, val) in sorted(INDEX.items()):
        by_scope.setdefault(scope, []).append((tag, slot, key, val))

    for scope in ("held", "worn", "item"):
        entries = by_scope.get(scope)
        if not entries:
            continue
        sel = SCOPE_SELECTOR[scope]
        lines.append("## " + SCOPE_TITLE[scope])
        for tag, _s, _k, _v in entries:
            lines.append("tag %s remove %s" % (sel, tag))
        for tag, slot, key, val in entries:
            lines.append("execute as %s if items entity @s %s "
                         "*[minecraft:custom_data~{%s:%sb}] run tag @s add %s"
                         % (sel, slot, key, val, tag))
        lines.append("")

    lines.append("## damage detection")
    lines.append("tag @e[tag=rpg.hurt] remove rpg.hurt")
    lines.append("execute as @a at @s run function rpg:command/damage_scan")
    lines.append("")

    path = os.path.join(ROOT, "data", "rpg", "function", "command", "index.mcfunction")
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


DAMAGE_SCAN = """\
# Snapshot health for entities a player could plausibly have hit, and flag the
# ones whose health moved since last tick.  Run once per player from
# rpg:command/index instead of once per weapon-effect line for every entity.
execute as @e[type=!#rpg:no_damage_track,distance=..64] store result score @s damage_action run data get entity @s Health
# 第一次见到的实体先把基准对齐：否则它会被当成"刚受伤"，
# 读档时区块一批批加载，每批新实体都会误触发一次全部武器判定 —— 就是进档后那阵卡顿。
# `unless score X = X` 在分数不存在时成立，是判断"这个分数有没有值"的惯用写法。
execute as @e[type=!#rpg:no_damage_track,distance=..64] unless score @s damage_timing = @s damage_timing run scoreboard players operation @s damage_timing = @s damage_action
execute as @e[type=!#rpg:no_damage_track,distance=..64] unless score @s damage_action = @s damage_timing run tag @s add rpg.hurt
"""

TICK_END = """\
# Commit this tick's health snapshot; runs last in #minecraft:tick.
execute as @e[tag=rpg.hurt] run scoreboard players operation @s damage_timing = @s damage_action
"""

# entity types that can never be the victim of a weapon proc -- excluded from
# the per-tick health scan.  `required:false` keeps the tag valid if a type is
# renamed or removed in a future version.
NO_DAMAGE_TRACK = """\
item experience_orb area_effect_cloud eye_of_ender falling_block firework_rocket
item_frame glow_item_frame painting leash_knot lightning_bolt marker interaction
text_display block_display item_display arrow spectral_arrow trident snowball egg
ender_pearl potion splash_potion lingering_potion small_fireball fireball
dragon_fireball wither_skull shulker_bullet llama_spit evoker_fangs wind_charge
breeze_wind_charge fishing_bobber end_crystal tnt ominous_item_spawner
minecart chest_minecart furnace_minecart tnt_minecart hopper_minecart
spawner_minecart command_block_minecart boat chest_boat oak_boat oak_chest_boat
spruce_boat spruce_chest_boat birch_boat birch_chest_boat jungle_boat
jungle_chest_boat acacia_boat acacia_chest_boat cherry_boat cherry_chest_boat
dark_oak_boat dark_oak_chest_boat pale_oak_boat pale_oak_chest_boat
mangrove_boat mangrove_chest_boat bamboo_raft bamboo_chest_raft
""".split()


def write_support_files():
    fdir = os.path.join(ROOT, "data", "rpg", "function", "command")
    with io.open(os.path.join(fdir, "damage_scan.mcfunction"), "w",
                 encoding="utf-8", newline="\n") as fh:
        fh.write(DAMAGE_SCAN)
    with io.open(os.path.join(fdir, "tick_end.mcfunction"), "w",
                 encoding="utf-8", newline="\n") as fh:
        fh.write(TICK_END)

    tdir = os.path.join(ROOT, "data", "rpg", "tags", "entity_type")
    if not os.path.isdir(tdir):
        os.makedirs(tdir)
    with io.open(os.path.join(tdir, "no_damage_track.json"), "w",
                 encoding="utf-8", newline="\n") as fh:
        json.dump({"values": [{"id": "minecraft:" + t, "required": False}
                              for t in NO_DAMAGE_TRACK]},
                  fh, indent=2)
        fh.write("\n")

    # 计分板必须在每次载入世界时就建好，否则所有 scores={...} 判定都静默失效
    load = os.path.join(ROOT, "data", "minecraft", "tags", "function", "load.json")
    with io.open(load, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"replace": False, "values": ["rpg:command/soreboard"]}, fh, indent=2)
        fh.write("\n")

    tick = os.path.join(ROOT, "data", "minecraft", "tags", "function", "tick.json")
    doc = json.load(io.open(tick, encoding="utf-8"))
    values = [v for v in doc["values"]
              if v not in ("rpg:command/index", "rpg:command/tick_end")]
    doc["values"] = ["rpg:command/index"] + values + ["rpg:command/tick_end"]
    with io.open(tick, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")


# --- per-file surgery -------------------------------------------------------

DAMAGE_SNAPSHOT = ("execute as @e at @s store result score @s damage_action "
                   "run data get entity @s Health")
DAMAGE_COMMIT = ("execute as @e at @s run scoreboard players operation "
                 "@s damage_timing = @s damage_action")
HURT_PREFIX = ("execute as @e at @s unless score @s damage_action = "
               "@s damage_timing ")


def rework_damage_lines(lines):
    out = []
    for line in lines:
        st = line.strip()
        if st == DAMAGE_SNAPSHOT or st == DAMAGE_COMMIT:
            bump("per-entity health scan removed")
            continue
        if st.startswith(HURT_PREFIX):
            bump("hurt test -> tag=rpg.hurt")
            out.append("execute as @e[tag=rpg.hurt] at @s " + st[len(HURT_PREFIX):])
            continue
        out.append(line)
    return out


def main():
    files = []
    for dirpath, _d, names in os.walk(ROOT):
        for fn in names:
            if fn.endswith(".mcfunction"):
                files.append(os.path.join(dirpath, fn))

    for path in files:
        src = io.open(path, encoding="utf-8").read()
        lines = src.split("\n")
        lines = rework_damage_lines(lines)
        lines = [rewrite_line(l) for l in lines]
        new = "\n".join(lines)
        if new != src:
            io.open(path, "w", encoding="utf-8", newline="\n").write(new)

    write_index()
    write_support_files()

    print("indexed flags: %d" % len(INDEX))
    for k in sorted(STATS):
        print("  %-38s %d" % (k, STATS[k]))


if __name__ == "__main__":
    main()
