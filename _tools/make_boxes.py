# -*- coding: utf-8 -*-
"""Build a complete, type-classified catalogue of custom give items.

The command ``rpg:command/give/box`` gives one or more shulker boxes per
semantic category. It includes the four legacy catalogue functions plus the
exorcism tools, true-name pages and verdict rewards. Runtime-only duplicate
givers are omitted because their byte-identical originals are already listed.
"""

import glob
import io
import os
import re
import sys

import snbt


DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")
OUT = os.path.join(FUNC, "command/give/box.mcfunction")
SLOTS = 27

LEGACY = [
    "command/give/weapon.mcfunction",
    "command/give/item.mcfunction",
    "command/give/weapon_up_item.mcfunction",
    "command/give/extra.mcfunction",
]

EXORCISM_GLOBS = [
    "inquest/give/nail.mcfunction",
    "inquest/give/bell.mcfunction",
    "inquest/give/incense.mcfunction",
    "inquest/give/lantern.mcfunction",
    "inquest/give/strong_water.mcfunction",
    "inquest/give/chalk?.mcfunction",
    "inquest/give/medium?.mcfunction",
    "inquest/give/page?.mcfunction",
    "inquest/give/relic?.mcfunction",
    "inquest/give/core?.mcfunction",
]

# key -> box colour, visible label. Order is the hand-out order.
CATEGORIES = [
    ("weapon", "red", "武器"),
    ("armor", "purple", "防具"),
    ("rune", "cyan", "符文镶嵌"),
    ("forge", "yellow", "锻造升级"),
    ("utility", "blue", "药剂功能"),
    ("test", "gray", "测试物"),
    ("pact", "black", "罪约契约"),
    ("divine", "light_blue", "上位契约"),
    ("kabbalah", "magenta", "卡巴拉秘仪"),
    ("mercenary", "green", "佣兵"),
    ("exorcism", "white", "驱魔器具"),
    ("page", "light_blue", "真名档案"),
    ("verdict", "brown", "裁决遗物"),
]

RULE = '{"text":"+------------------+","italic":false,"color":"white"}'
ARMOR_SUFFIXES = ("_helmet", "_chestplate", "_leggings", "_boots")
WEAPON_IDS = {
    "bow", "crossbow", "mace", "trident", "spear", "netherite_spear",
    "wooden_sword", "stone_sword", "iron_sword", "golden_sword",
    "diamond_sword", "netherite_sword", "wooden_axe", "stone_axe",
    "iron_axe", "golden_axe", "diamond_axe", "netherite_axe",
}
UNSTACKABLE_IDS = {
    "potion", "splash_potion", "lingering_potion", "goat_horn",
    "enchanted_book", "written_book", "crossbow", "bow", "mace",
    "trident", "spear", "netherite_spear", "elytra",
}


def relpath(path):
    return os.path.relpath(path, FUNC).replace(os.sep, "/")


def parse_give(line):
    """Return ``(item id, component block, count)`` for a direct give."""
    match = re.match(r"^give\s+\S+\s+(.+?)\s*$", line.strip())
    if not match:
        return None
    rest = match.group(1)
    b = rest.find("[")
    if b < 0:
        fields = rest.split()
        count = int(fields[1]) if len(fields) > 1 and fields[1].isdigit() else 1
        return fields[0], None, count
    item = rest[:b]
    block, end = snbt.parse_component_block(rest, b)
    suffix = rest[end:].strip()
    count = int(suffix.split()[0]) if suffix and suffix.split()[0].isdigit() else 1
    return item, block, count


def component_blob(block):
    if block is None:
        return ""
    return ",".join("%s=%s" % (name, value.dump())
                    for name, value, neg, _sep in block.entries
                    if value is not None and not neg)


def category(source, item, block):
    blob = component_blob(block)
    base = item.split(":")[-1]

    if source.startswith("inquest/give/page"):
        return "page"
    if source.startswith("inquest/give/relic") or source.startswith("inquest/give/core"):
        return "verdict"
    if source.startswith("inquest/give/"):
        return "exorcism"
    if "pact_tag:1b" in blob:
        return "pact"
    if "rpg_divine_pact:1b" in blob:
        return "divine"
    if any(flag in blob for flag in
           ("rpg_kabbalah_contract:1b", "rpg_sephirah:", "rpg_true_cross:1b")):
        return "kabbalah"
    if "squad_hire:1b" in blob or "squad_order:1b" in blob:
        return "mercenary"
    if ('"text":"[驱魔]"' in blob or "rpg_rite_tool:1b" in blob or
            "rite_tag:1b" in blob):
        return "exorcism"
    if base.endswith(ARMOR_SUFFIXES) or base in {"elytra", "turtle_helmet"}:
        return "armor"
    if (base in WEAPON_IDS or base.endswith(("_sword", "_axe", "_spear")) or
            "sword_tag:1b" in blob or "bow_tag:1b" in blob):
        return "weapon"
    if "试金石" in blob:
        return "test"
    if ("镶嵌符" in blob or any(name in blob for name in
            ("力量之石", "肃杀之石", "守护之石", "明辨之石", "急奔之石", "万钧之石"))):
        return "rune"
    if (source.endswith("weapon_up_item.mcfunction") or
            any(name in blob for name in ("铸造之石", "剑胚", "生铁", "冶炼石")) or
            base in {"raw_gold", "gold_ingot", "diamond"}):
        return "forge"
    return "utility"


def entry(slot, item, block, count):
    ident = item if ":" in item else "minecraft:" + item
    components = "components:{}"
    if block is not None:
        parts = []
        for name, value, neg, _sep in block.entries:
            if value is None or neg:
                continue
            key = name if ":" in name else "minecraft:" + name
            parts.append('"%s":%s' % (key, value.dump()))
        components = "components:{%s}" % ",".join(parts)
    return '{slot:%d,item:{id:"%s",count:%d,%s}}' % (
        slot, ident, max(1, count), components)


def max_stack(item, block):
    if block is not None:
        for name, value, neg, _sep in block.entries:
            if name.split(":")[-1] == "max_stack_size" and value is not None and not neg:
                raw = value.dump().rstrip("bBsSlLfFdD")
                if raw.isdigit():
                    return max(1, int(raw))
    base = item.split(":")[-1]
    if (base in UNSTACKABLE_IDS or base.endswith(ARMOR_SUFFIXES) or
            base.endswith(("_sword", "_axe", "_spear"))):
        return 1
    return 64


def stack_records(records):
    """Split one give amount across legal container stacks."""
    out = []
    for source, item, block, count in records:
        limit = max_stack(item, block)
        left = count
        while left > 0:
            size = min(left, limit)
            out.append((source, item, block, size))
            left -= size
    return out


def box(colour, label, part, total, records):
    suffix = " %d/%d" % (part, total) if total > 1 else ""
    name = ('["",{"text":"[%s]","italic":false,"color":"gold","bold":true},'
            '{"text":"%s","italic":false,"color":"white"}]' % (label, suffix))
    amount = sum(record[3] for record in records)
    types = len({(record[0], record[1], component_blob(record[2]))
                 for record in records})
    lore = ("lore=[[\"\",%s],"
            '["",{"text":"内含 %d 类 · 共 %d 件","italic":false,"color":"gray"}],'
            "[\"\",%s]]" % (RULE, types, amount, RULE))
    entries = [entry(i, item, block, count)
               for i, (_source, item, block, count) in enumerate(records)]
    return "give @a %s_shulker_box[custom_name=%s,%s,container=[%s]]" % (
        colour, name, lore, ",".join(entries))


def source_files():
    paths = [os.path.join(FUNC, rel.replace("/", os.sep)) for rel in LEGACY]
    for pattern in EXORCISM_GLOBS:
        paths.extend(sorted(glob.glob(os.path.join(FUNC, pattern.replace("/", os.sep)))))
    seen = set()
    out = []
    for path in paths:
        key = os.path.normcase(os.path.abspath(path))
        if key not in seen:
            seen.add(key)
            out.append(path)
    return out


def all_direct_give_keys():
    """Every unique item produced by a direct give anywhere in the pack."""
    keys = set()
    for root, _dirs, names in os.walk(FUNC):
        for name in names:
            path = os.path.join(root, name)
            if not name.endswith(".mcfunction") or os.path.normcase(path) == os.path.normcase(OUT):
                continue
            for line in io.open(path, encoding="utf-8"):
                parsed = parse_give(line)
                if parsed:
                    item, block, _count = parsed
                    keys.add((item, component_blob(block)))
    return keys


def main():
    grouped = {key: [] for key, _colour, _label in CATEGORIES}
    seen = {}
    source_count = 0
    for path in source_files():
        if not os.path.isfile(path):
            raise RuntimeError("catalogue source missing: " + path)
        source = relpath(path)
        for line in io.open(path, encoding="utf-8"):
            parsed = parse_give(line)
            if not parsed:
                continue
            item, block, count = parsed
            source_count += 1
            key = (item, component_blob(block))
            if key in seen:
                print("  duplicate skipped: %s (already %s)" % (source, seen[key]))
                continue
            seen[key] = source
            grouped[category(source, item, block)].append((source, item, block, count))

    global_keys = all_direct_give_keys()
    missing = global_keys.difference(seen)
    extra = set(seen).difference(global_keys)
    if missing or extra:
        raise RuntimeError("catalogue coverage mismatch: missing=%d extra=%d" %
                           (len(missing), len(extra)))

    lines = [
        "# 全量分类领取：每种自定义物品只收录一次，每盒最多 27 类。",
        "# 由 make_boxes.py 从旧领取目录与驱魔体系的规范 give 函数生成。",
        "# 盒内组件和原始 give 完全一致；原命令的发放数量也会保留。",
        "",
    ]
    total_unique = 0
    total_boxes = 0
    for key, colour, label in CATEGORIES:
        records = grouped[key]
        if not records:
            continue
        stacks = stack_records(records)
        chunks = [stacks[i:i + SLOTS] for i in range(0, len(stacks), SLOTS)]
        lines.append("## %s -- %d 类，%d 盒" % (label, len(records), len(chunks)))
        for number, chunk in enumerate(chunks, 1):
            lines.append(box(colour, label, number, len(chunks), chunk))
        lines.append("")
        total_unique += len(records)
        total_boxes += len(chunks)
        print("  %-10s %3d types / %d slots -> %d box(es)" %
              (label, len(records), len(stacks), len(chunks)))

    if total_unique != len(seen):
        raise RuntimeError("catalogue grouping lost items: %d != %d" %
                           (total_unique, len(seen)))
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))
    print("boxes: %d, holding %d unique types from %d give lines; global missing=0 extra=0 -> rpg:command/give/box" %
          (total_boxes, total_unique, source_count))


if __name__ == "__main__":
    main()
