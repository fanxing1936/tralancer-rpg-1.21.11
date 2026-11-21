# -*- coding: utf-8 -*-
"""装备养成重置的公共工具：路径、文本组件、材料物品的 SNBT。"""

import io
import json
import os

import rpg_ui_style as ui
import forge_spec as S

NS = "rpg:forge"
WS = "@e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1]"
CD = 'item.components."minecraft:custom_data"'
EQ = CD + ".rpg_eq"
CONSUME_SECONDS = 1234567.0


class Out(object):
    """收集要写出的文件，最后一次写盘。"""

    def __init__(self, dp, rp=None):
        self.dp = dp
        self.rp = rp
        self.files = {}

    def fn(self, rel, text):
        path = os.path.join(self.dp, "data/rpg/function/forge", rel + ".mcfunction")
        body = text.strip("\n") + "\n"
        self.files[path] = body

    def js(self, rel, doc):
        self.files[os.path.join(self.dp, rel)] = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"

    def flush(self):
        for path, body in self.files.items():
            d = os.path.dirname(path)
            if not os.path.isdir(d):
                os.makedirs(d)
            with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(body)
        return len(self.files)


def read(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def J(value):
    """紧凑 JSON；同时也是合法的 SNBT。"""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def c(text, colour=ui.WHITE, bold=False):
    return ui.comp(text, colour, bold)


def row(*parts):
    return [""] + list(parts)


RULE = row(c(ui.RULE_TEXT, ui.WHITE))


# ---------------------------------------------------------------------------
# 材料物品
# ---------------------------------------------------------------------------
def consumable():
    return ('consumable={consume_seconds:%sf,animation:"none",'
            'sound:"minecraft:intentionally_empty",has_consume_particles:false}' % CONSUME_SECONDS)


def item_snbt(key, name_parts, lore_rows, data, stack=64):
    """一个养成材料的完整 SNBT（不带物品 id）。"""
    parts = [
        "custom_name=" + J(row(*name_parts)),
        "lore=" + J([RULE] + [row(*r) for r in lore_rows] + [RULE]),
        'item_model="rpg:forge/%s"' % key,
        consumable(),
        "max_stack_size=%d" % stack,
        "custom_data={rpg_fm:1b,%s}" % data,
    ]
    return "minecraft:paper[" + ",".join(parts) + "]"


def all_items():
    """key -> (SNBT, 分类)。分类给 loot 和物品盒用。"""
    out = {}
    for key, (name, tag, colour, text) in S.MATERIALS.items():
        out[key] = (item_snbt(key, [c(tag, colour, True), c(name)],
                              [[c(t, ui.GRAY)] for t in text],
                              'rpg_mat:"%s"' % key), "material")
    for s in S.SOURCES:
        tier = "holy" if s["side"] == "holy" else "devil"
        tag_colour = ui.PASSION if tier == "holy" else ui.NAMELESS["lit"]
        rows = [[c("副手拿武器，主手右键", ui.GRAY)],
                [c("🜏效果 ", ui.WHITE, True), c("[%s]" % s["name"], s["colour"], True)],
                [c(s["text"], ui.GRAY)]]
        if s["cost"]:
            rows.append([c("代价 ", ui.WHITE, True), c(s["cost"], ui.WARN)])
        if s["side"] == "holy":
            rows.append([c("武器 Lv.%d 起算圣器" % S.HOLY_SOURCE_LV, ui.HOLY)])
        rows.append([c("一把武器只有一个源，新源会覆盖旧源", ui.MUTED)])
        out["source_" + s["id"]] = (item_snbt(
            "source_" + s["id"],
            [c(ui.tier_tag(tier), tag_colour, True), c(s["name"] + "之源")], rows,
            'rpg_mat:"source",rpg_src:"%s"' % s["id"], 16), "source")
    for r in S.RUNES:
        col = S.PART_COLOUR[r["part"]]
        out["rune_" + r["id"]] = (item_snbt(
            "rune_" + r["id"], [c("[符文]", col, True), c(r["name"])],
            [[c("镶嵌于 ", ui.GRAY), c("[%s]" % S.PART_NAME[r["part"]], col, True)],
             [c("🪓被动 ", ui.WHITE, True), c("[%s]" % r["name"], col, True)],
             [c(r["text"], ui.GRAY)],
             [c("副手拿装备，主手右键镶嵌", ui.MUTED)]],
            'rpg_mat:"rune",rpg_rune:"%s"' % r["id"]), "rune")
    for s in S.STONES:
        col = S.STONE_COLOUR[s["id"]]
        part = {"melee": "近战武器", "ranged": "弓弩", "any": "武器"}[s["part"]]
        out["stone_" + s["id"]] = (item_snbt(
            "stone_" + s["id"], [c("[符石]", S.C_STONE, True), c(s["name"])],
            [[c("镶嵌于 ", ui.GRAY), c("[%s]" % part, col, True)],
             [c("🔱主动 ", ui.WHITE, True), c("[%s]" % s["name"], col, True)],
             [c(s["text"], ui.GRAY)],
             [c("打怪攒满能量后按 F 释放", ui.MUTED)]],
            'rpg_mat:"stone",rpg_stone:"%s"' % s["id"]), "stone")
    return out


def name_comp(kind, key):
    """属性块里显示的名字组件（JSON 字符串，存进 storage 给宏用）。"""
    if kind == "src":
        s = next(x for x in S.SOURCES if x["id"] == key)
        return J(c("[%s]" % s["name"], s["colour"], True))
    if kind == "srcd":
        s = next(x for x in S.SOURCES if x["id"] == key)
        return J(c(" " + s["text"], ui.GRAY))
    if kind == "rune":
        r = next(x for x in S.RUNES if x["id"] == key)
        return J(c("[%s]" % r["name"], S.PART_COLOUR[r["part"]], True))
    if kind == "stone":
        s = next(x for x in S.STONES if x["id"] == key)
        return J(c("[%s]" % s["name"], S.STONE_COLOUR[key], True))
    raise KeyError(kind)


NONE = J(c("—", ui.MUTED))
LOCK = J(c("🔒Lv.5", ui.MUTED))
NA = J(c("不可镶嵌", ui.MUTED))
