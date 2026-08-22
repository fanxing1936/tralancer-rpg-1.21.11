# -*- coding: utf-8 -*-
"""Render the loot-table items (ranged stats) into guide fragments."""

import io
import json

from build_guide import ATTR_CN, ENCH_CN, ITEM_CN, cn_item, esc, RARITY
import icons

LOOT = json.load(io.open("../_data_loot.json", encoding="utf-8"))
SEP = "+------------------+"

# the bracket prefix these loot items use is a loose grade, not the give-command tier
GRADE = {
    "legend": ("legend", "传说"), "epic": ("epic", "史诗"),
    "brave": ("brave", "勇者"), "barve": ("brave", "勇者"),   # author's typo
    "uncommon": ("none", "常见"), "food": ("none", "食物"),
    "currency": ("none", "货币"), "item": ("none", "材料"),
}


def split_name(raw):
    if raw and raw.startswith("["):
        i = raw.find("]")
        if i > 0:
            return raw[1:i], raw[i + 1:].strip()
    return None, (raw or "").strip()


def split_lore(lore):
    blocks, cur = [], []
    for l in lore:
        if l.strip() == SEP:
            if cur:
                blocks.append(cur)
                cur = []
            continue
        cur.append(l)
    if cur:
        blocks.append(cur)
    return (blocks[0] if blocks else []), (blocks[1] if len(blocks) > 1 else [])


def rng(a):
    lo, hi = a["range"] if a["range"] else (None, None)
    if lo is None:
        return "—"
    mult = a["op"] == "add_multiplied_base"
    f = (lambda v: "%+g%%" % (v * 100)) if mult else (lambda v: "%+g" % v)
    return f(lo) if lo == hi else "%s ~ %s" % (f(lo), f(hi))


def ench_note(e):
    n = len(e)
    if not n:
        return None
    if all(x == "任意附魔" for x in e):
        return "随机附魔 ×%d" % n
    return "、".join(str(x) for x in e)


def card(e, cls, grade, name):
    flavour, skill = split_lore(e["lore"])
    sk = skill[0] if skill else ""
    sk_name = ""
    if "[" in sk and "]" in sk:
        sk_name = sk[sk.index("[") + 1:sk.index("]")]
    sk_kind = "主动技能" if "主动" in sk else ("被动技能" if "被动" in sk else "")

    b = ['<article class="card r-%s" data-rarity="%s" data-name="%s">'
         % (cls, cls, esc(name + " " + grade + " " + sk_name))]
    b.append('<header class="card-h">%s<div class="card-id">'
             '<span class="tier">%s</span><h3>%s</h3>'
             '<p class="base">%s</p></div></header>'
             % (icons.loot_img(e, name), esc(grade), esc(name),
                esc(cn_item(e["item"]))))
    if flavour:
        b.append('<p class="flavour">%s</p>' % esc("　".join(flavour)))
    if sk_name:
        b.append('<div class="skill"><span class="skill-kind">%s</span>'
                 '<span class="skill-name">%s</span><p>%s</p></div>'
                 % (esc(sk_kind or "技能"), esc(sk_name),
                    esc(" ".join(skill[1:]))))
    rows = []
    if e["attrs"]:
        rows.append(("属性", " · ".join(
            "%s %s<span class=\"slot\">%s</span>"
            % (esc(ATTR_CN.get(a["attr"], a["attr"])), rng(a), esc(a["slot"]))
            for a in e["attrs"])))
    en = ench_note(e["ench"])
    if en:
        rows.append(("附魔", esc(en)))
    misc = []
    if e["damage"]:
        misc.append("耐久损耗 %g–%g" % tuple(e["damage"]))
    if e["count"] and tuple(e["count"]) != (1, 1):
        misc.append("数量 %g–%g" % tuple(e["count"]))
    for c in e["components"]:
        if c.endswith("consumable"):
            misc.append("右键长按发动")
    if misc:
        rows.append(("其他", esc(" · ".join(misc))))
    if e["tags"]:
        rows.append(("标签", "<code>%s</code>" % esc(" ".join(sorted(e["tags"])))))
    if rows:
        b.append('<dl class="stats">')
        for k, v in rows:
            b.append("<dt>%s</dt><dd>%s</dd>" % (k, v))
        b.append("</dl>")
    b.append("</article>")
    return "".join(b)


def cards_for(table):
    out = []
    for p in LOOT[table]:
        for e in p["entries"]:
            if not e.get("name"):
                continue
            grade_raw, name = split_name(e["name"])
            cls, grade = GRADE.get(grade_raw, ("none", grade_raw or ""))
            out.append(card(e, cls, grade, name))
    return "\n".join(out)


def drop_table(tables, title):
    """Compact table for the randomly-rolled armour / weapon drops."""
    rows = []
    for t in tables:
        for p in LOOT[t]:
            total = sum(x["weight"] for x in p["entries"])
            for e in p["entries"]:
                if not e.get("name"):
                    continue
                grade_raw, name = split_name(e["name"])
                cls, grade = GRADE.get(grade_raw, ("none", grade_raw or ""))
                attrs = "、".join(
                    "%s %s" % (ATTR_CN.get(a["attr"], a["attr"]), rng(a))
                    for a in e["attrs"]) or "—"
                rows.append(
                    "<tr><td class=\"has-icon\">%s<span><span class=\"nm\" style=\"color:var(--r-%s)\">%s</span>"
                    "<span class=\"sm\">%s</span></span></td>"
                    "<td class=\"num\">%s</td><td class=\"num\">%.0f%%</td>"
                    "<td>%s</td><td>%s</td></tr>"
                    % (icons.loot_img(e, name), cls, esc(name),
                       esc(cn_item(e["item"])), esc(grade),
                       100.0 * e["weight"] / total, esc(attrs),
                       esc(ench_note(e["ench"]) or "—")))
    return ('<h3 class="sub-h">%s</h3><div class="tw"><table>'
            '<thead><tr><th>物品</th><th>品级</th><th>权重</th>'
            '<th>随机属性范围</th><th>附魔</th></tr></thead><tbody>%s</tbody></table></div>'
            % (title, "".join(rows)))


def reward_table(table, title):
    rows = []
    for p in LOOT[table]:
        total = sum(e["weight"] for e in p["entries"])
        rolls = p["rolls"]
        for e in sorted(p["entries"], key=lambda x: -x["weight"]):
            grade_raw, name = split_name(e["name"]) if e["name"] else (None, "")
            cls, grade = GRADE.get(grade_raw, ("none", grade_raw or ""))
            label = name or cn_item(e["item"])
            cnt = ("%g–%g" % tuple(e["count"])) if e["count"] and e["count"][0] != e["count"][1] else (
                "%g" % e["count"][0] if e["count"] else "1")
            note = []
            if e["tags"]:
                note.append("标签 " + " ".join(sorted(e["tags"])))
            if e.get("ref"):
                note.append("子表")
            rows.append("<tr><td class=\"has-icon\">%s<span><span class=\"nm\" style=\"color:var(--r-%s)\">%s</span>"
                        "<span class=\"sm\">%s</span></span></td><td class=\"num\">%.1f%%</td>"
                        "<td class=\"num\">%s</td><td>%s</td></tr>"
                        % (icons.loot_img(e, label), cls, esc(label),
                           esc(cn_item(e["item"])),
                           100.0 * e["weight"] / total, cnt, esc("；".join(note) or "—")))
    return ('<h3 class="sub-h">%s<span class="rolls">每次 %g 抽</span></h3>'
            '<div class="tw"><table><thead><tr><th>产出</th><th>单抽概率</th>'
            '<th>数量</th><th>备注</th></tr></thead><tbody>%s</tbody></table></div>'
            % (title, rolls[0] if rolls else 1, "".join(rows)))


def main():
    frag = {
        "loot_epic": cards_for("rpg:trial/epic_sword"),
        "loot_drops": drop_table(
            ["rpg:armor/sword", "rpg:armor/bow"], "怪物携带的武器 · rpg:armor/sword · bow")
        + drop_table(["rpg:armor/helmet", "rpg:armor/chestplate",
                      "rpg:armor/leggings", "rpg:armor/boots"],
                     "怪物携带的护甲 · rpg:armor/*"),
        "loot_trial": drop_table(
            ["rpg:trial/sword", "rpg:trial/bow"], "试炼武器 · rpg:trial/sword · bow")
        + drop_table(["rpg:trial/helmet", "rpg:trial/chestplate",
                      "rpg:trial/leggings", "rpg:trial/boots"],
                     "试炼护甲 · rpg:trial/*"),
        "loot_reward": reward_table("rpg:trial/trial", "普通试炼奖励 · rpg:trial/trial")
        + reward_table("rpg:trial/trial_ominous", "不祥试炼奖励 · rpg:trial/trial_ominous")
        + reward_table("rpg:trial/valuable", "试炼珍品 · rpg:trial/valuable")
        + reward_table("rpg:trial/valuable_ominous", "不祥珍品 · rpg:trial/valuable_ominous"),
    }
    old = json.load(io.open("../_guide_fragments.json", encoding="utf-8"))
    old.update(frag)
    io.open("../_guide_fragments.json", "w", encoding="utf-8", newline="\n").write(
        json.dumps(old, ensure_ascii=False))
    print("loot fragments: " + ", ".join("%s=%d" % (k, len(v)) for k, v in frag.items()))


if __name__ == "__main__":
    main()
