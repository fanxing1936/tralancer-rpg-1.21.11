# -*- coding: utf-8 -*-
"""领取箱补齐：rpg:command/give/box 里再加 make_boxes 之后才生成的物品（用户 2026-11-24「所有出现在rpg中的材料是否都归类到了give BOX里面」）。

    python add_give_boxes.py ../rpg

make_boxes.py 在构建中段运行，只收当时已有的 give 行；世界掉落、图纸、罪印碎片、圣徽、传承书等在它之后才写出来，
而且多数只在掉落表里、没有 give 行。这里按类追加：
  [锻造原料] [遗物] [世界材料] [罪印碎片] [锻造图纸] [圣力魔力] [试炼物资]
物品组件直接读掉落表 / give 行，和掉落的一模一样。结尾扫一遍全部掉落表：凡是带自定义名字、箱里没有的物品，构建就失败。
"""
import glob
import io
import json
import os
import re
import sys

import add_merchants as M
import make_boxes as B
import world_loot_spec as W

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
DATA = os.path.join(DP, "data")
FUNC = os.path.join(DATA, "rpg", "function")
BOX = os.path.join(FUNC, "command", "give", "box.mcfunction")
SLOTS = 27
MARK = "# --- add_give_boxes.py 追加 ---"


def text_of(comp):
    if isinstance(comp, str):
        return comp
    if isinstance(comp, dict):
        return comp.get("text", "") + "".join(text_of(x) for x in comp.get("extra", []))
    if isinstance(comp, list):
        return "".join(text_of(x) for x in comp)
    return ""


def name_of(entry):
    nm = ""
    for f in entry.get("functions", []):
        k = f.get("function", "").replace("minecraft:", "")
        if k == "set_name":
            nm = text_of(f["name"])
        elif k == "set_components" and "minecraft:custom_name" in f["components"]:
            nm = text_of(f["components"]["minecraft:custom_name"])
    return nm


def loot_items():
    """名字 → (物品 id, 组件 SNBT)：全部掉落表里带自定义名字的物品，同名只取第一件。"""
    out = {}

    def walk(o):
        if isinstance(o, dict):
            if o.get("type", "").endswith("item") and "name" in o and name_of(o):
                out.setdefault(name_of(o), M.item_of(o))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for path in sorted(glob.glob(os.path.join(DATA, "**", "loot_table", "**", "*.json"), recursive=True)):
        walk(json.load(io.open(path, encoding="utf-8")))
    return out


def normalise():
    """[food] → [食物]：前缀一律中文（ART-STYLE §2.1）。"""
    for name in ("trial.json", "trial_ominous.json"):
        p = os.path.join(DATA, "rpg", "loot_table", "trial", name)
        s = io.open(p, encoding="utf-8").read()
        if "[food]" in s:
            io.open(p, "w", encoding="utf-8", newline="\n").write(s.replace("[food]", "[食物]"))


def give_items(rel):
    """函数里的 give 行 → (id, 组件 SNBT)"""
    out = []
    for line in io.open(os.path.join(FUNC, rel + ".mcfunction"), encoding="utf-8"):
        line = re.sub(r"^execute .*? run (?=give )", "", line.strip())
        parsed = B.parse_give(line)
        if not parsed or parsed[1] is None:
            continue
        parts = ['"%s":%s' % (n if ":" in n else "minecraft:" + n, v.dump())
                 for n, v, neg, _s in parsed[1].entries if v is not None and not neg]
        out.append((parsed[0] if ":" in parsed[0] else "minecraft:" + parsed[0], "{" + ",".join(parts) + "}"))
    return out


def stack(iid, comps, want):
    m = re.search(r'"minecraft:max_stack_size":(\d+)', comps)
    base = iid.split(":")[-1]
    limit = int(m.group(1)) if m else (1 if base in B.UNSTACKABLE_IDS or base == "totem_of_undying" else 16 if base == "ender_pearl" else 64)
    return min(want, limit)


def box(colour, label, part, total, items):
    suffix = " %d/%d" % (part, total) if total > 1 else ""
    name = ('["",{"text":"[%s]","italic":false,"color":"gold","bold":true},{"text":"%s","italic":false,"color":"white"}]' % (label, suffix))
    lore = ('lore=[["",%s],["",{"text":"内含 %d 类 · 共 %d 件","italic":false,"color":"gray"}],["",%s]]'
            % (B.RULE, len(items), sum(c for _i, _c, c in items), B.RULE))
    slots = ",".join('{slot:%d,item:{id:"%s",count:%d,components:%s}}' % (i, iid, c, comps) for i, (iid, comps, c) in enumerate(items))
    return "give @a %s_shulker_box[custom_name=%s,%s,container=[%s]]" % (colour, name, lore, slots)


def main():
    import add_world_items as WI
    import rpg_ui_style as ui
    normalise()
    loot = loot_items()
    raw = ["[锻造]" + v[0] for v in W.RAW.values()]
    prod = []
    for _n, mobs, *_r in W.GROUPS.values():
        for ds in mobs.values():
            for d in ds:
                if W.RELIC + d[1] not in prod:
                    prod.append(W.RELIC + d[1])
    prod += [W.RELIC + n for n in ("铁粒", "禁果", "血泥", "断羽", "达阿特的碎镜")]
    world = ["[货币]精英徽记", "[锻造]图纸碎片"] + ["[锻造]" + v[0] for v in WI.SPECIAL.values()]
    shards = ["[恶魔]罪印碎片 · " + p["who"] for p in ui.PILLARS]
    bps = ["%s图纸 · %s" % (WI.TIER_TAG[w[2]], w[1]) for w in WI.WEAPONS]
    trial = ["[传说]试炼之匙", "[传说]灾厄试炼之匙", "[传说]不死图腾", "[食物]压缩肉干"]
    cats = [("lime", "锻造原料", raw, 64), ("green", "遗物", prod, 64), ("gray", "世界材料", world, 64),
            ("red", "罪印碎片", shards, 64), ("brown", "锻造图纸", bps, 1), ("cyan", "试炼物资", trial, 16)]
    lines = [MARK, ""]
    kinds = boxes = 0
    placed = set()
    for colour, label, names, want in cats:
        miss = [n for n in names if n not in loot]
        if miss:
            raise SystemExit("give boxes: 掉落表里没有 %s" % miss)
        placed |= set(names)
        items = [(loot[n][0], loot[n][1], stack(loot[n][0], loot[n][1], want)) for n in names]
        emit(lines, colour, label, items)
        kinds += len(items)
        boxes += (len(items) + SLOTS - 1) // SLOTS
    # 有 give 行、但在 make_boxes 之后才写出来的
    late = give_items("force/admin/give") + give_items("force/admin/legacy") + give_items("jacques_ally/give") + give_items("prologue/reward")
    emit(lines, "yellow", "圣力魔力", [(i, c, 1) for i, c in late])
    kinds += len(late)
    boxes += 1

    s = io.open(BOX, encoding="utf-8").read()
    s = s.split(MARK)[0].rstrip("\n") + "\n\n" + "\n".join(lines)
    # 覆盖核对：每件带自定义名字的掉落都要在箱里（只比本名，前面的图标字形与 [前缀] 不算）
    gone = [n for n in loot if n not in placed and '"%s"' % re.sub(r"^.*?\]", "", n) not in s and ('"text":"%s"' % re.sub(r"^.*?\]", "", n)) not in s
            and re.sub(r"^.*?\]", "", n) not in s]
    if gone:
        raise SystemExit("give boxes: 没装箱的掉落物 %s" % gone)
    with io.open(BOX, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(s.rstrip("\n") + "\n")
    print("give boxes: +%d boxes, %d kinds; %d named loot items all covered" % (boxes, kinds, len(loot)))


def emit(lines, colour, label, items):
    chunks = [items[i:i + SLOTS] for i in range(0, len(items), SLOTS)]
    lines.append("## %s -- %d 类，%d 盒" % (label, len(items), len(chunks)))
    for k, c in enumerate(chunks, 1):
        lines.append(box(colour, label, k, len(chunks), c))
    lines.append("")


if __name__ == "__main__":
    main()
