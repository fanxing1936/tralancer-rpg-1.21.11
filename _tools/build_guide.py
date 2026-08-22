# -*- coding: utf-8 -*-
"""Generate the TRALANCER RPG codex (HTML) from the data pack's own item data."""

import io
import json
import os
import re
import sys

import icons

DATA = json.load(io.open("../_data_items.json", encoding="utf-8"))
OUT_HTML = "../TRALANCER-RPG-图鉴.html"

SEP = "+------------------+"

RARITY = {
    "神圣": ("holy", "神圣"), "恶魔": ("devil", "恶魔"),
    "传说": ("legend", "传说"), "史诗": ("epic", "史诗"),
    "勇者": ("brave", "勇者"),
    # a couple of items spell the top tier out in latin
    "限定传说": ("lgd", "限定传说"),
    "l·legend": ("lgd", "限定传说"), "legend": ("legend", "传说"),
}
# names that repeat across a whole family -- the bracket label is what actually
# tells two of them apart, so it becomes the heading instead of the tier chip
FAMILY = ("镶嵌符文", "镶嵌符石", "试金石", "玩家面板", "货币", "黄金", "钻石",
          "剑胚", "生铁", "冶炼石", "传说冶炼石")

ATTR_CN = {
    "attack_damage": "攻击伤害", "attack_speed": "攻击速度", "max_health": "最大生命",
    "armor": "护甲", "armor_toughness": "护甲韧性", "movement_speed": "移动速度",
    "knockback_resistance": "击退抗性", "attack_knockback": "击退强度",
    "max_absorption": "伤害吸收", "luck": "幸运", "gravity": "重力",
    "safe_fall_distance": "安全坠落", "burning_time": "燃烧时间",
    "oxygen_bonus": "氧气加成", "scale": "体型", "jump_strength": "跳跃力",
    "sweeping_damage_ratio": "横扫比例", "entity_interaction_range": "交互距离",
    "block_interaction_range": "方块交互距离",
}

ENCH_CN = {
    "sharpness": "锋利", "smite": "亡灵杀手", "bane_of_arthropods": "节肢杀手",
    "knockback": "击退", "fire_aspect": "火焰附加", "looting": "抢夺",
    "sweeping_edge": "横扫之刃", "power": "力量", "punch": "冲击",
    "flame": "火矢", "infinity": "无限", "piercing": "穿透",
    "quick_charge": "快速装填", "multishot": "多重射击", "breach": "破甲",
    "density": "致密", "wind_burst": "风爆", "thorns": "荆棘",
    "lunge": "突进",
    "protection": "保护", "fire_protection": "火焰保护",
    "blast_protection": "爆炸保护", "projectile_protection": "弹射物保护",
    "unbreaking": "耐久", "mending": "经验修补", "efficiency": "效率",
    "depth_strider": "深海探索者", "respiration": "水下呼吸",
    "feather_falling": "摔落缓冲", "soul_speed": "灵魂疾行", "swift_sneak": "迅捷潜行",
}

ITEM_CN = {
    "netherite_sword": "下界合金剑", "diamond_sword": "钻石剑",
    "netherite_axe": "下界合金斧", "iron_axe": "铁斧", "mace": "重锤",
    "netherite_spear": "下界合金枪", "diamond_spear": "钻石枪",
    "iron_spear": "铁枪", "golden_spear": "金枪", "copper_spear": "铜枪",
    "stone_spear": "石枪", "wooden_spear": "木枪",
    "bow": "弓", "crossbow": "弩", "quartz": "下界石英",
    "amethyst_shard": "紫水晶碎片", "nether_star": "下界之星",
    "totem_of_undying": "不死图腾", "player_head": "玩家头颅",
    "leather_helmet": "皮革头盔", "leather_chestplate": "皮革胸甲",
    "leather_boots": "皮革靴子", "chainmail_helmet": "锁链头盔",
    "chainmail_chestplate": "锁链胸甲", "netherite_chestplate": "下界合金胸甲",
    "netherite_leggings": "下界合金护腿", "netherite_boots": "下界合金靴子",
    "diamond_helmet": "钻石头盔", "iron_leggings": "铁护腿",
    "potion": "药水", "splash_potion": "喷溅药水", "lingering_potion": "滞留药水",
    "allay_spawn_egg": "悦灵刷怪蛋", "wooden_sword": "木剑", "raw_iron": "粗铁",
    "echo_shard": "回响碎片", "diamond": "钻石", "gold_ingot": "金锭",
    "raw_gold": "粗金", "music_disc_precipice": "音乐唱片·绝境",
    "music_disc_relic": "音乐唱片·遗迹", "music_disc_13": "音乐唱片 13",
    "music_disc_11": "音乐唱片 11", "music_disc_stal": "音乐唱片 stal",
    "music_disc_5": "音乐唱片 5", "vault": "宝库",
}


def cn_item(i):
    i = i.split(":")[-1]
    if i.endswith("_armor_trim_smithing_template"):
        return "锻造模板·" + i[:-len("_armor_trim_smithing_template")]
    return ITEM_CN.get(i, i)


def split_lore(lore):
    """The pack's lore uses +---+ rules: flavour block, then a skill block."""
    blocks, cur = [], []
    for line in lore:
        if line.strip() == SEP:
            if cur:
                blocks.append(cur)
                cur = []
            continue
        cur.append(line)
    if cur:
        blocks.append(cur)
    flavour = blocks[0] if blocks else []
    skill = blocks[1] if len(blocks) > 1 else []
    return flavour, skill


SKILL_RE = re.compile(r"^([\U0001F300-\U0001FAFF☀-➿]?)(主动技能|被动技能|镶嵌技能)\[([^\]]+)\]")


def parse_skill(skill):
    if not skill:
        return None
    head = skill[0]
    m = SKILL_RE.match(head)
    if not m:
        return {"kind": "", "name": head, "text": " ".join(skill[1:])}
    return {"icon": m.group(1), "kind": m.group(2), "name": m.group(3),
            "text": " ".join(skill[1:])}


def fmt_amount(m):
    a = m["amount"]
    if m["op"] == "add_multiplied_base":
        return "%+g%%" % (a * 100)
    return "%+g" % a


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


# --------------------------------------------------------------------------
def card(it, show_tags=True):
    rar = it["rarity"]
    cls, label = RARITY.get(rar, ("none", rar or ""))
    flavour, skill = split_lore(it["lore"])
    sk = parse_skill(skill)

    heading, base = it["name"] or "（无名）", cn_item(it["item"])
    if cls == "none" and it["name"] in FAMILY:
        if label:
            heading, label = label, ""
            base = "%s · %s" % (it["name"], cn_item(it["item"]))

    # 新锻 gear is ordinary gear -- it carries the same tags, rarities and skill
    # format, so it gets no badge and no separate shelf.
    bits = ['<article class="card r-%s" data-rarity="%s" data-name="%s">' %
            (cls, cls, esc(it["name"] + " " + (rar or "") + " " +
                           (sk["name"] if sk else "")))]
    bits.append('<header class="card-h">')
    bits.append(icons.item_img(it, heading))
    bits.append('<div class="card-id">')
    if label:
        bits.append('<span class="tier">%s</span>' % esc(label))
    bits.append('<h3>%s</h3>' % esc(heading))
    bits.append('<p class="base">%s</p>' % esc(base))
    bits.append("</div></header>")

    if flavour:
        bits.append('<p class="flavour">%s</p>' % esc("　".join(flavour)))

    if sk:
        bits.append('<div class="skill"><span class="skill-kind">%s</span>'
                    '<span class="skill-name">%s</span><p>%s</p></div>'
                    % (esc(sk.get("kind") or "技能"), esc(sk["name"]), esc(sk["text"])))

    rows = []
    if it["modifiers"]:
        seen = []
        for m in it["modifiers"]:
            seen.append("%s %s<span class=\"slot\">%s</span>"
                        % (esc(ATTR_CN.get(m["attr"], m["attr"])), fmt_amount(m),
                           esc(m["slot"])))
        rows.append(("属性", " · ".join(seen)))
    if it["enchantments"]:
        e = " · ".join("%s %s" % (ENCH_CN.get(k, k), v)
                       for k, v in sorted(it["enchantments"].items()))
        rows.append(("附魔", esc(e)))
    misc = []
    if it["unbreakable"]:
        misc.append("不可破坏")
    if it["consumable"]:
        misc.append("右键长按发动")
    if it["cmd"]:
        misc.append("模型 %d" % int(it["cmd"]))
    if misc:
        rows.append(("其他", esc(" · ".join(misc))))
    if show_tags and it["tags"]:
        rows.append(("标签", '<code>%s</code>' % esc(" ".join(it["tags"]))))
    if rows:
        bits.append('<dl class="stats">')
        for k, v in rows:
            bits.append("<dt>%s</dt><dd>%s</dd>" % (k, v))
        bits.append("</dl>")
    bits.append("</article>")
    return "".join(bits)


ORIGIN = {
    1110003.0: "闲置贴图 · 弩（含全部装填分帧）",
    1110004.0: "闲置贴图 · 弩（含全部装填分帧）",
    1110002.0: "闲置贴图 · 弓（含全部拉弓分帧）",
    1110001.0: "闲置贴图 · 钓竿（含抛竿分帧）",
    1110011.0: "闲置贴图 · 剑",
    1110012.0: "新绘贴图 · 圣殿双柱之一",
    1110013.0: "新绘贴图 · 圣殿双柱之一",
    1110014.0: "作者贴图 · 蛇矛（第五位恶魔）",
    1110007.0: "作者贴图 · 巨锚（第六位恶魔）",
}


def roster(items):
    """A compact index for section VIII -- the full cards now live inline in
    the weapon plates, so this only says what each piece is and where its art
    came from."""
    rows = []
    for x in items:
        rar = x["rarity"]
        cls, label = RARITY.get(rar, ("none", rar or ""))
        _flavour, skill = split_lore(x["lore"])
        sk = parse_skill(skill)
        rows.append(
            '<tr><td class="has-icon">%s<span>'
            '<span class="nm" style="color:var(--r-%s)">%s</span>'
            '<span class="sm">%s</span></span></td>'
            '<td>%s</td><td>%s</td><td>%s</td></tr>'
            % (icons.item_img(x), cls, esc(x["name"] or "（无名）"),
               esc(cn_item(x["item"])), esc(label),
               esc("%s［%s］" % (sk.get("kind") or "技能", sk["name"]) if sk else "—"),
               esc(ORIGIN.get(x["cmd"], "—"))))
    return ('<div class="tw"><table><thead><tr><th>装备</th><th>品质</th>'
            '<th>技能</th><th>贴图来源</th></tr></thead><tbody>%s</tbody>'
            '</table></div>' % "".join(rows))


def main():
    w = DATA["command/give/weapon.mcfunction"]
    it = DATA["command/give/item.mcfunction"]
    up = DATA["command/give/weapon_up_item.mcfunction"]
    extra = DATA.get("command/give/extra.mcfunction", [])

    # The newly forged gear used to sit in a section of its own.  It is real
    # equipment with the same tags, rarities and skill format as everything
    # else, so it belongs in the codex proper -- it is folded into the same
    # pools here and only carries a "新锻" marker to stay findable.
    for x in extra:
        x["_new"] = True
    w = w + extra

    weapons = [x for x in w if any(t in x["tags"] for t in ("sword_tag", "bow_tag"))]
    armour = [x for x in w if "chestplate_tag" in x["tags"]]
    consum = [x for x in w if x not in weapons and x not in armour and x["name"]]
    runes = [x for x in it if "add_weapon_tag" in x["tags"] or
             any(t in x["tags"] for t in ("sweep_tag", "wind_tag", "flame_tag"))]
    stones = [x for x in it if x["item"].endswith("_armor_trim_smithing_template")]
    mats = [x for x in it if x not in runes and x not in stones
            and "enchant_tag" not in x["tags"]]
    ench = [x for x in it if "enchant_tag" in x["tags"]]

    print("weapons %d  armour %d  consumables %d  runes %d  stones %d  materials %d  whetstones %d"
          % (len(weapons), len(armour), len(consum), len(runes), len(stones),
             len(mats), len(ench)))

    ench_list = sorted(set(
        "%s %s" % (ENCH_CN.get(k, k), v)
        for x in ench for k, v in x["enchantments"].items()))

    json.dump({"weapons": weapons, "armour": armour, "consum": consum,
               "runes": runes, "stones": stones, "mats": mats,
               "ench_list": ench_list},
              io.open("../_guide_sections.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # cards are emitted here so the HTML file stays hand-authored
    frag = {
        "weapons": "\n".join(card(x) for x in weapons),
        "armour": "\n".join(card(x) for x in armour),
        "consum": "\n".join(card(x, show_tags=False) for x in consum),
        "runes": "\n".join(card(x) for x in runes),
        "stones": "\n".join(card(x, show_tags=False) for x in stones),
        "mats": "\n".join(card(x) for x in mats),
        "ench": "、".join(ench_list),
    }
    io.open("../_guide_fragments.json", "w", encoding="utf-8", newline="\n").write(
        json.dumps(frag, ensure_ascii=False))


if __name__ == "__main__":
    main()
