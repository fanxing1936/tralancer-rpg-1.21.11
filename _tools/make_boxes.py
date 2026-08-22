# -*- coding: utf-8 -*-
"""Pack every `give` item into shulker boxes, and add one command for the lot.

`rpg:command/give/*` hands out ~110 items one at a time, which overflows an
inventory several times over.  This walks those functions, converts each
`give @a <id>[<components>]` into a container entry, and emits
`rpg:command/give/box` -- a single function that gives one shulker box per
category, each box holding up to 27 of the originals.

The only real work is the syntax shift.  A give command writes components as
`id[custom_name=...,lore=[...]]`; inside a `container` entry the same data is a
map keyed by namespaced id: `components:{"minecraft:custom_name":...}`.
snbt.py already parses the bracket form, so each value is re-dumped verbatim
under its full key -- no re-serialisation of the values themselves, which
keeps the items byte-identical to what the originals produced.
"""

import io
import os
import sys

import snbt

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
GIVE = os.path.join(DP, "data/rpg/function/command/give")

SLOTS = 27

# source function -> (box colour, label shown on the box)
SOURCES = [
    ("weapon.mcfunction", "red", "武器"),
    ("item.mcfunction", "blue", "道具"),
    ("weapon_up_item.mcfunction", "yellow", "升级材料"),
    ("extra.mcfunction", "lime", "新锻装备"),
]

RULE = '{"text":"+------------------+","italic":false,"color":"dark_gray"}'


def parse_give(line):
    """`give @a <id>[<components>]` -> (id, components snbt) or None."""
    line = line.strip()
    # one entry uses @s (the vault block), the rest @a -- take both
    for head in ("give @a ", "give @s "):
        if line.startswith(head):
            rest = line[len(head):]
            break
    else:
        return None
    b = rest.find("[")
    if b < 0:                       # plain `give @a stone` / `give @a stone 3`
        item = rest.split()[0]
        return item, None
    item = rest[:b]
    block, _end = snbt.parse_component_block(rest, b)
    return item, block


def entry(slot, item, block):
    """One `container` entry."""
    ident = item if ":" in item else "minecraft:" + item
    out = 'components:{}'
    if block is not None:
        parts = []
        for name, value, neg, _sep in block.entries:
            if value is None or neg:
                continue
            key = name if ":" in name else "minecraft:" + name
            parts.append('"%s":%s' % (key, value.dump()))
        out = "components:{%s}" % ",".join(parts)
    return '{slot:%d,item:{id:"%s",count:1,%s}}' % (slot, ident, out)


def box(colour, label, part, total, entries):
    name = ('["",{"text":"[%s]","italic":false,"color":"gold","bold":true},'
            '{"text":" %s","italic":false,"color":"white"}]'
            % (label, "%d/%d" % (part, total) if total > 1 else ""))
    lore = ("lore=[[\"\",%s],"
            '["",{"text":"内含 %d 件，取出即用","italic":false,"color":"gray"}],'
            "[\"\",%s]]" % (RULE, len(entries), RULE))
    return ("give @a %s_shulker_box[custom_name=%s,%s,container=[%s]]"
            % (colour, name, lore, ",".join(entries)))


def main():
    lines = ["# 一次取齐：每个类别一只潜影盒，每盒最多 27 件。",
             "# 由 make_boxes.py 从 rpg:command/give/* 直接打包，",
             "# 盒内物品与逐件 give 出来的完全一致。", ""]
    total_items = 0
    for src, colour, label in SOURCES:
        path = os.path.join(GIVE, src)
        if not os.path.isfile(path):
            continue
        items = []
        for line in io.open(path, encoding="utf-8"):
            got = parse_give(line)
            if got:
                items.append(got)
        if not items:
            continue
        chunks = [items[i:i + SLOTS] for i in range(0, len(items), SLOTS)]
        lines.append("## %s -- %d 件，%d 盒" % (label, len(items), len(chunks)))
        for n, chunk in enumerate(chunks, 1):
            lines.append(box(colour, label, n, len(chunks),
                             [entry(i, it, bl) for i, (it, bl) in enumerate(chunk)]))
        lines.append("")
        total_items += len(items)
        print("  %-26s %3d items -> %d box(es)" % (src, len(items), len(chunks)))

    with io.open(os.path.join(GIVE, "box.mcfunction"), "w",
                 encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    boxes = sum(1 for l in lines if l.startswith("give @a "))
    print("boxes: %d, holding %d items -> rpg:command/give/box" % (boxes, total_items))


if __name__ == "__main__":
    main()
