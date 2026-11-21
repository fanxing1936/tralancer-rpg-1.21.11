# -*- coding: utf-8 -*-
"""装备养成重置（docs/EQUIP-REWORK.md）：魂火冶炼、工坊、六源、符文、符石、属性块、掉落。

    python add_forge.py <resourcepack> <rpg>            # 早段：build.sh 里 make_boxes 之前
    python add_forge.py <resourcepack> <rpg> --late     # 晚段：boss 胜利掉源、HUD 能量槽
    python add_forge.py <resourcepack> --rp-only        # rp_build.sh：只装图标

早段会：
* 换掉旧材料、旧符文符石、旧唱片的发放行，写出 31 件新物品和各自的掉落表；
* 改写七张自写生物表、试炼之室、宝库、35 张仆从表的掉落；退役 13 张旧表；
* 退役 rpg:command/com 里的旧养成逻辑（丢地合成、12 行属性块、每 5 刻刷新）；
* 写出 rpg:forge/* 全部函数，挂进 #minecraft:tick 与 load。
"""

import glob
import io
import json
import os
import random
import re
import shutil
import sys
import zipfile

import rpg_ui_style as ui
import forge_spec as S
import forge_common as FC
import forge_core
import forge_ops
import forge_runtime
from forge_common import Out, read, write, J, WS

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
RP = ARGS[0] if ARGS else "../resourcepack"
DP = ARGS[1] if len(ARGS) > 1 else "../rpg"
LATE = "--late" in sys.argv
RP_ONLY = "--rp-only" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "forge_art", "pixel16")
FUNC = os.path.join(DP, "data/rpg/function")
LOOT = os.path.join(DP, "data/rpg/loot_table")
GIVE = os.path.join(FUNC, "command/give")
MARK = "rpg:forge/"


# ---------------------------------------------------------------------------
# 资源包：图标
# ---------------------------------------------------------------------------
def build_rp(items):
    from mc_env import JAR
    missing = []
    z = zipfile.ZipFile(JAR)
    for key in items:
        tex = os.path.join(RP, "assets/rpg/textures/item/forge/%s.png" % key)
        src = os.path.join(ART, key + ".png")
        if not os.path.isdir(os.path.dirname(tex)):
            os.makedirs(os.path.dirname(tex))
        if os.path.isfile(src):
            shutil.copyfile(src, tex)
        else:
            missing.append(key)
            with open(tex, "wb") as fh:
                fh.write(z.read("assets/minecraft/textures/item/paper.png"))
        write(os.path.join(RP, "assets/rpg/models/item/forge/%s.json" % key),
              J({"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/forge/%s" % key}}) + "\n")
        write(os.path.join(RP, "assets/rpg/items/forge/%s.json" % key),
              J({"model": {"type": "minecraft:model", "model": "rpg:item/forge/%s" % key}}) + "\n")
    # 武器名前的源图标：同一张 16x16 源贴图缩到文字高度，放在独立字体里，不占 default 的码位
    providers = [{"type": "bitmap", "file": "rpg:item/forge/source_%s.png" % s["id"], "height": 8, "ascent": 7,
                  "chars": [S.SOURCE_GLYPH[s["id"]]]} for s in S.SOURCES]
    write(os.path.join(RP, "assets/rpg/font/forge_src.json"), J({"providers": providers}) + "\n")
    return missing


# ---------------------------------------------------------------------------
# give 行解析（迁移表要用：原生圣器、原名、原来的右键组件）
# ---------------------------------------------------------------------------
def grab(line, key):
    """取出 `key=<值>` 的值（配平括号与引号）。"""
    m = re.search(r"[\[,]%s=" % re.escape(key), line)
    if not m:
        return None
    i = m.end()
    depth, quote, j = 0, None, i
    while j < len(line):
        ch = line[j]
        if quote:
            if ch == "\\":
                j += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch in "[{(":
            depth += 1
        elif ch in "]})":
            if depth == 0:
                return line[i:j]
            depth -= 1
        elif ch == "," and depth == 0:
            return line[i:j]
        j += 1
    return None


GENERIC = {"sword_tag", "bow_tag", "chestplate_tag", "holy_weapon_tag", "devil_tag", "weapon_tag",
           "axe_tag", "add_weapon_tag", "currency_tag", "rpg_fm"}


def migration_table():
    lines = []
    for f in ("weapon", "extra", "michael", "dungeons", "armor"):
        p = os.path.join(GIVE, f + ".mcfunction")
        if os.path.isfile(p):
            lines += [l.strip() for l in io.open(p, encoding="utf-8") if l.startswith("give ")]
    flags_of = []
    count = {}
    for l in lines:
        cd = grab(l, "custom_data") or ""
        keys = re.findall(r"([A-Za-z_][A-Za-z0-9_]*):", cd)
        keys = [k for k in keys if k.endswith("_tag") and k not in GENERIC]
        flags_of.append(keys)
        for k in set(keys):
            count[k] = count.get(k, 0) + 1
    native, names, uses, seen = [], [], [], set()
    for l, keys in zip(lines, flags_of):
        ident = next((k for k in keys if count[k] == 1), None)
        if "holy_weapon_tag:1b" in l:
            native += [k for k in keys]
        if not ident or ident in seen:
            continue
        seen.add(ident)
        name = grab(l, "custom_name")
        if name:
            names.append((ident, name))
        comps = [(c, grab(l, c)) for c in ("consumable", "food") if grab(l, c)]
        if comps and any(c == "consumable" for c, _ in comps):
            uses.append((ident, comps))
    return {"native_holy": sorted(set(native)), "names": names, "uses": uses}


# ---------------------------------------------------------------------------
# 发放行
# ---------------------------------------------------------------------------
OLD_GIVE = re.compile(r"custom_data=\{[^}]*(add_weapon_tag|level_item|enchant_tag|gold_tag|diamond_tag|"
                      r"echo_tag|fec_tag|embryo_tag|weapon_tree)")


def build_give(items):
    p = os.path.join(GIVE, "item.mcfunction")
    old = read(p).splitlines()
    kept = [l for l in old if not (l.startswith("give") and OLD_GIVE.search(l))]
    removed = len(old) - len(kept)
    # 旧材料段落里的空注释行也一起收拾掉
    body = "\n".join(kept).rstrip("\n")
    new = ["", "##装备养成：材料、符文、符石（docs/EQUIP-REWORK.md）"]
    new += ["give @a %s" % snbt for key, (snbt, cat) in items.items() if cat in ("material", "rune", "stone")]
    write(p, body + "\n" + "\n".join(new) + "\n")
    write(os.path.join(GIVE, "weapon_up_item.mcfunction"),
          "\n".join("give @a %s" % snbt for key, (snbt, cat) in items.items() if cat == "source") + "\n")
    write(os.path.join(GIVE, "forge.mcfunction"),
          "# 装备养成的全部材料各一件（只发给自己）\n" +
          "\n".join("give @s %s" % snbt for snbt, _cat in items.values()) + "\n")
    return removed


# ---------------------------------------------------------------------------
# 掉落
# ---------------------------------------------------------------------------
def entry_item(snbt):
    """把 give 用的 SNBT 拆成 loot 条目：物品 id + set_components。"""
    ident, comps = snbt.split("[", 1)
    comps = comps[:-1]
    return ident, comps


def loot_item_table(snbt):
    ident, comps = entry_item(snbt)
    funcs = []
    for part in split_top(comps):
        k, v = part.split("=", 1)
        funcs.append((k, v))
    # set_components 的值要 JSON；这里直接用 SNBT 字符串最省事：custom_data 走 set_custom_data，
    # 其余组件逐个转换。名字与 lore 本来就是 JSON。
    components = {}
    custom = None
    for k, v in funcs:
        if k == "custom_data":
            custom = v
        elif k in ("custom_name",):
            components["minecraft:custom_name"] = json.loads(v)
        elif k == "lore":
            components["minecraft:lore"] = json.loads(v)
        elif k == "item_model":
            components["minecraft:item_model"] = json.loads(v)
        elif k == "max_stack_size":
            components["minecraft:max_stack_size"] = int(v)
        elif k == "consumable":
            components["minecraft:consumable"] = {
                "consume_seconds": FC.CONSUME_SECONDS, "animation": "none",
                "sound": "minecraft:intentionally_empty", "has_consume_particles": False}
    functions = [{"function": "minecraft:set_components", "components": components}]
    if custom:
        functions.append({"function": "minecraft:set_custom_data", "tag": custom})
    return {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": [
        {"type": "minecraft:item", "name": ident, "functions": functions}]}]}


def split_top(s):
    out, depth, quote, start, j = [], 0, None, 0, 0
    while j < len(s):
        ch = s[j]
        if quote:
            if ch == "\\":
                j += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch in "[{(":
            depth += 1
        elif ch in "]})":
            depth -= 1
        elif ch == "," and depth == 0:
            out.append(s[start:j])
            start = j + 1
        j += 1
    out.append(s[start:])
    return out


def ref(key, weight=1):
    return {"type": "minecraft:loot_table", "value": MARK + "item/" + key, "weight": weight}


def chance(p, looting=True):
    if looting:
        return [{"condition": "minecraft:killed_by_player"},
                {"condition": "minecraft:random_chance_with_enchanted_bonus", "enchantment": "minecraft:looting",
                 "unenchanted_chance": p,
                 "enchanted_chance": {"type": "minecraft:linear", "base": p + 0.01, "per_level_above_first": 0.01}}]
    return [{"condition": "minecraft:random_chance", "chance": p}]


def loot_json(path):
    return json.load(io.open(path, encoding="utf-8"))


def dump(path, doc):
    write(path, json.dumps(doc, ensure_ascii=False, indent=2) + "\n")


def is_retired_entry(e):
    """旧掉落：改名原版装备、旧装备表、[货币]钻石与黄金。"""
    if e.get("type", "").endswith("loot_table") and isinstance(e.get("value"), str):
        v = e["value"]
        return v.startswith("rpg:armor/") or v in RETIRED_TRIAL
    if not e.get("type", "").endswith("item"):
        return False
    blob = json.dumps(e, ensure_ascii=False)
    if "diamond_tag" in blob or "gold_tag" in blob:
        return True
    name = e.get("name", "").split(":")[-1]
    gear = name.endswith(("_sword", "_axe", "_helmet", "_chestplate", "_leggings", "_boots")) or name in ("bow", "crossbow", "mace")
    return gear and "+------------------+" in blob and "rpg_eq" not in blob


RETIRED_TRIAL = {"rpg:trial/%s" % k for k in ("sword", "bow", "helmet", "chestplate", "leggings", "boots", "epic_sword")}


def scrub_pool(pool):
    """去掉退役条目；被去掉的权重并入空条目（没有就新建），保持其余条目的概率。"""
    removed = 0
    keep = []
    for e in pool.get("entries", []):
        if is_retired_entry(e):
            removed += e.get("weight", 1)
        else:
            keep.append(e)
    pool["entries"] = keep
    return removed


def build_loot(items):
    n = 0
    for key, (snbt, _cat) in items.items():
        dump(os.path.join(LOOT, "forge/item/%s.json" % key), loot_item_table(snbt))
        n += 1
    dump(os.path.join(LOOT, "forge/rune_any.json"), {"type": "minecraft:generic", "pools": [
        {"rolls": 1, "entries": [ref("rune_" + r["id"]) for r in S.RUNES]}]})
    dump(os.path.join(LOOT, "forge/stone_any.json"), {"type": "minecraft:generic", "pools": [
        {"rolls": 1, "entries": [ref("stone_" + s["id"]) for s in S.STONES]}]})
    for name, extra in (("bundle", 1.0), ("bundle_ominous", 2.0)):
        dump(os.path.join(LOOT, "forge/%s.json" % name), {"type": "minecraft:generic", "pools": [
            {"rolls": 2, "entries": [ref("forge_stone")]},
            {"rolls": 1, "entries": [ref("wash_gem")]},
            {"rolls": 1, "entries": [ref("gild_leaf")]},
            {"rolls": 1, "conditions": chance(0.2 * extra, False),
             "entries": [{"type": "minecraft:loot_table", "value": MARK + "rune_any"}]},
            {"rolls": 1, "conditions": chance(0.1 * extra, False),
             "entries": [{"type": "minecraft:loot_table", "value": MARK + "stone_any"}]}]})
    for sid in S.SOURCE_BOSS:
        dump(os.path.join(LOOT, "forge/boss/%s.json" % sid), {"type": "minecraft:generic", "pools": [
            {"rolls": 1, "conditions": chance(S.BOSS_SOURCE_CHANCE, False), "entries": [ref("source_" + sid)]},
            {"rolls": 1, "conditions": chance(S.BOSS_STONE_CHANCE, False),
             "entries": [{"type": "minecraft:loot_table", "value": MARK + "stone_any"}]}]})

    report = {}
    # 七张自写的生物表（马除外）
    for mob in ("creeper", "husk", "skeleton", "zombie", "zombie_villager"):
        p = os.path.join(DP, "data/minecraft/loot_table/entities/%s.json" % mob)
        if not os.path.isfile(p):
            continue
        doc = loot_json(p)
        doc["pools"] = [pl for pl in doc.get("pools", []) if MARK not in json.dumps(pl)]
        for pool in doc["pools"]:
            gone = scrub_pool(pool)
            if gone:
                empt = next((e for e in pool["entries"] if e.get("type", "").endswith("empty")), None)
                if empt:
                    empt["weight"] = empt.get("weight", 1) + gone
                else:
                    pool["entries"].append({"type": "minecraft:empty", "weight": gone})
        for key, pr in S.DROP_COMMON.items():
            doc["pools"].append({"rolls": 1, "conditions": chance(pr), "entries": [ref(key)]})
        dump(p, doc)
        report[mob] = "ok"

    # 试炼之室
    def edit(rel, adds):
        p = os.path.join(LOOT, rel)
        doc = loot_json(p)
        pool = doc["pools"][0]
        pool["entries"] = [e for e in pool["entries"] if MARK not in json.dumps(e)]
        scrub_pool(pool)
        pool["entries"] += adds
        dump(p, doc)

    edit("trial/trial.json", [ref("blank", 2), ref("soul", 6), ref("forge_stone", 3), ref("wash_gem", 3),
                              ref("gild_leaf", 2),
                              {"type": "minecraft:loot_table", "value": MARK + "rune_any", "weight": 6}])
    edit("trial/trial_ominous.json", [ref("blank", 2), ref("soul", 6), ref("forge_stone", 3), ref("wash_gem", 4),
                                      ref("gild_leaf", 3),
                                      {"type": "minecraft:loot_table", "value": MARK + "rune_any", "weight": 6},
                                      {"type": "minecraft:loot_table", "value": MARK + "stone_any", "weight": 5}])
    for rel in ("trial/valuable.json", "trial/valuable_ominous.json"):
        edit(rel, [ref("gild_leaf", 5), ref("wash_gem", 5)])
    # 宝库
    dump(os.path.join(LOOT, "loot/loot.json"), {"type": "minecraft:generic", "pools": [
        {"rolls": 1, "entries": [{"type": "minecraft:loot_table", "value": MARK + "bundle"}]}]})
    dump(os.path.join(LOOT, "loot/loot_ominous.json"), {"type": "minecraft:generic", "pools": [
        {"rolls": 1, "entries": [{"type": "minecraft:loot_table", "value": MARK + "bundle_ominous"}]}]})
    # 退役旧表
    retired = 0
    for k in ("sword", "bow", "helmet", "chestplate", "leggings", "boots", "epic_sword"):
        p = os.path.join(LOOT, "trial/%s.json" % k)
        if os.path.isfile(p):
            os.remove(p)
            retired += 1
    for p in glob.glob(os.path.join(LOOT, "armor/*.json")):
        os.remove(p)
        retired += 1
    lf = os.path.join(FUNC, "loot/loot.mcfunction")
    if os.path.isfile(lf):
        write(lf, read(lf).replace("loot rpg:trial/sword", "loot rpg:forge/bundle"))
    # 仆从表
    minions = 0
    for p in glob.glob(os.path.join(LOOT, "minion/**/*.json"), recursive=True):
        doc = loot_json(p)
        doc["pools"] = [pl for pl in doc.get("pools", []) if MARK not in json.dumps(pl)]
        doc["pools"].append({"rolls": 1, "conditions": chance(S.DROP_MINION["soul"]), "entries": [ref("soul")]})
        doc["pools"].append({"rolls": 1, "conditions": chance(S.DROP_MINION["rune"]),
                             "entries": [{"type": "minecraft:loot_table", "value": MARK + "rune_any"}]})
        dump(p, doc)
        minions += 1
    return n, report, retired, minions


# ---------------------------------------------------------------------------
# 冶炼产物
# ---------------------------------------------------------------------------
def smelt_functions():
    out = []
    for k, (tkey, disp, _mats) in enumerate(S.TIERS):
        for key, name, kind, bases in S.SMELT_TYPES:
            base = bases[k]
            parts = []
            if disp:
                parts.append(FC.c(ui.tier_tag(disp), ui.tier_colour(disp), True))
            parts.append(FC.c("$(p)" + name, ui.WHITE))
            comps = ["custom_name=" + J(FC.row(*parts)),
                     "lore=" + J([FC.row(FC.c("出自魂火的冶炼", ui.MUTED))]),
                     "custom_data={rpg_forged:1b}"]
            if kind == "melee":
                dmg, spd = S.MELEE_STATS[key][k]
                comps.append("attribute_modifiers=[{type:\"minecraft:attack_damage\",id:\"rpg:forge/base\",amount:%sd,operation:\"add_value\",slot:\"mainhand\"},"
                             "{type:\"minecraft:attack_speed\",id:\"rpg:forge/base_spd\",amount:%sd,operation:\"add_value\",slot:\"mainhand\"}]"
                             % (dmg - 1, round(spd - 4, 2)))
                if k:
                    comps.append("enchantments={\"minecraft:unbreaking\":%d}" % k)
            elif kind == "ranged":
                comps.append("enchantments={\"minecraft:%s\":%d,\"minecraft:unbreaking\":%d}" % (S.RANGED_ENCH[key], k + 1, k + 1))
            else:
                arm, tough, kb = S.ARMOR_STATS[key][k]
                slot = S.ARMOR_SLOT[key]
                mods = ["{type:\"minecraft:armor\",id:\"rpg:forge/base_a\",amount:%sd,operation:\"add_value\",slot:\"%s\"}" % (arm, slot)]
                if tough:
                    mods.append("{type:\"minecraft:armor_toughness\",id:\"rpg:forge/base_t\",amount:%sd,operation:\"add_value\",slot:\"%s\"}" % (tough, slot))
                if kb:
                    mods.append("{type:\"minecraft:knockback_resistance\",id:\"rpg:forge/base_k\",amount:%sd,operation:\"add_value\",slot:\"%s\"}" % (kb, slot))
                comps.append("attribute_modifiers=[%s]" % ",".join(mods))
                if k:
                    comps.append("enchantments={\"minecraft:protection\":%d}" % k)
            out.append(("smelt/m/%s_%s" % (key, tkey),
                        "$item replace entity %s contents with minecraft:%s[%s]" % (WS, base, ",".join(comps))))
    return out


def volley_offsets():
    rnd = random.Random(20261121)
    out = []
    for t in range(58, 0, -3):
        out.append((t, (rnd.uniform(-2.2, 2.2), rnd.uniform(-2.2, 2.2))))
        out.append((t, (rnd.uniform(-2.2, 2.2), rnd.uniform(-2.2, 2.2))))
    return out


# ---------------------------------------------------------------------------
# 接线与退役
# ---------------------------------------------------------------------------
def wire():
    tag = os.path.join(DP, "data/minecraft/tags/function/tick.json")
    doc = loot_json(tag)
    if "rpg:forge/tick" not in doc["values"]:
        doc["values"].insert(doc["values"].index("rpg:command/tick_end"), "rpg:forge/tick")
        dump(tag, doc)
    sb = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = read(sb)
    if "function rpg:forge/load" not in s:
        write(sb, s.rstrip("\n") + "\n\n##装备养成\nfunction rpg:forge/load\n")
    for name in ("bypasses_cooldown", "no_knockback"):
        p = os.path.join(DP, "data/minecraft/tags/damage_type/%s.json" % name)
        doc = loot_json(p) if os.path.isfile(p) else {"replace": False, "values": []}
        if "rpg:forge_bonus" not in doc["values"]:
            doc["values"].append("rpg:forge_bonus")
        dump(p, doc)
    tags = {
        "melee": ["#minecraft:swords", "#minecraft:axes", "#minecraft:spears", "minecraft:mace", "minecraft:trident"],
        "ranged": ["minecraft:bow", "minecraft:crossbow"],
        "armor": ["#minecraft:head_armor", "#minecraft:chest_armor", "#minecraft:leg_armor", "#minecraft:foot_armor"],
    }
    tags["any"] = ["#rpg:forge/melee", "#rpg:forge/ranged", "#rpg:forge/armor"]
    for k, v in tags.items():
        dump(os.path.join(DP, "data/rpg/tags/item/forge/%s.json" % k), {"values": v})


RETIRE_NOTE = "# 已退役：装备养成重置（docs/EQUIP-REWORK.md）由 rpg:forge/* 接管。\n"


def retire():
    com = os.path.join(FUNC, "command/com.mcfunction")
    keep, on = [], False
    for line in read(com).splitlines():
        if line.startswith("##"):
            on = line.startswith("##显示名称") or line.startswith("##玩家面板")
        if on or line.startswith("execute as @a[tag=rpg.h.skull_tag1]"):
            keep.append(line)
    keep.append("execute as @a[scores={rpg_com_clock=5..}] at @s run function rpg:command/com/player_values")
    keep.append("scoreboard players add @a rpg_com_clock 1")
    keep.append("scoreboard players set @a[scores={rpg_com_clock=5..}] rpg_com_clock 0")
    write(com, RETIRE_NOTE + "\n".join(keep) + "\n")
    pv = os.path.join(FUNC, "command/com/player_values.mcfunction")
    if os.path.isfile(pv):
        write(pv, "\n".join(l for l in read(pv).splitlines()
                            if "sword_value" not in l and "chestplate_value" not in l) + "\n")
    n = 0
    for f in ("g0", "g1", "g2", "g3", "g4", "g5", "g6", "xilian", "branch", "add", "fumo", "smithing",
              "weapon", "weapon_feedback"):
        p = os.path.join(FUNC, "command/com/%s.mcfunction" % f)
        if os.path.isfile(p):
            write(p, RETIRE_NOTE)
            n += 1
    for p in (os.path.join(FUNC, "item/rune/runes.mcfunction"), os.path.join(FUNC, "command/weapon_level.mcfunction")):
        if os.path.isfile(p):
            write(p, RETIRE_NOTE)
            n += 1
    tk = os.path.join(FUNC, "command/tick.mcfunction")
    s = read(tk)
    s2 = "\n".join(l for l in s.splitlines() if not re.match(
        r"function rpg:item/sword/main/(sweep|flame|wind)/", l)) + "\n"
    write(tk, s2)
    return n


def late():
    # 旧烙印武器的原名：按最终（已规范化）的发放行重写
    out = Out(DP)
    forge_core.build_restore(out, migration_table())
    out.flush()
    # boss 胜利：掉源（30%）与符石（25%）
    patched = 0
    for sid, (boss, center) in S.SOURCE_BOSS.items():
        p = os.path.join(FUNC, boss, "victory.mcfunction")
        if not os.path.isfile(p):
            continue
        s = read(p)
        line = ("execute at @e[type=minecraft:marker,tag=%s,limit=1] run loot spawn ~ ~1 ~ loot rpg:forge/boss/%s" % (center, sid)
                if center else "loot spawn ~ ~1 ~ loot rpg:forge/boss/%s" % sid)
        if line in s:
            continue
        lines = s.rstrip("\n").splitlines()
        idx = next((i for i, l in enumerate(lines) if l.startswith("function rpg:%s/clear" % boss)), len(lines))
        lines.insert(idx, "# 装备养成：%s之源与符石" % next(x["name"] for x in S.SOURCES if x["id"] == sid))
        lines.insert(idx + 1, line)
        write(p, "\n".join(lines) + "\n")
        patched += 1
    # 圣器：神圣之源且 Lv.5 以上（渲染时写进 rpg_eq.holy）
    ip = os.path.join(FUNC, "command/index_player.mcfunction")
    s = read(ip)
    hook = ["# 装备养成：注入神圣之源、且装备 Lv.%d 以上的武器也算圣器" % S.HOLY_SOURCE_LV,
            "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{holy:1b}}] run tag @s add rpg.holy",
            "execute if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_eq:{holy:1b}}] run tag @s add rpg.holy"]
    if hook[1] not in s:
        lines = s.rstrip("\n").splitlines()
        last = max(i for i, l in enumerate(lines) if "run tag @s add rpg.holy" in l)
        lines[last + 1:last + 1] = hook
        write(ip, "\n".join(lines) + "\n")
    # HUD：状态行里加符石能量
    st = os.path.join(FUNC, "hud/status.mcfunction")
    s = read(st)
    hook = "execute if entity @s[tag=rpg.fg.st] run function rpg:forge/hud"
    if hook not in s:
        lines = s.splitlines()
        idx = next(i for i, l in enumerate(lines) if "render with storage rpg:hud" in l)
        lines.insert(idx, hook)
        write(st, "\n".join(lines) + "\n")
    return patched


def enchant_ids():
    from mc_env import JAR
    z = zipfile.ZipFile(JAR)
    pre = "data/minecraft/enchantment/"
    return sorted(n[len(pre):-5] for n in z.namelist() if n.startswith(pre) and n.endswith(".json") and "/" not in n[len(pre):])


def main():
    items = FC.all_items()
    if RP and os.path.isdir(RP):
        missing = build_rp(items)
        print("forge: %d icons installed%s" % (len(items) - len(missing),
                                              ("; %d placeholders: %s" % (len(missing), " ".join(missing[:8]))) if missing else ""))
    if RP_ONLY:
        return
    if LATE:
        print("forge late: %d boss victories patched, HUD energy slot wired" % late())
        return
    out = Out(DP)
    mig = migration_table()
    forge_core.build_load(out)
    forge_core.build_workbench(out)
    forge_core.build_init(out, mig)
    forge_core.build_render(out)
    forge_core.build_xp(out)
    forge_ops.build_use(out)
    forge_ops.build_xp(out)
    forge_ops.build_wash(out)
    forge_ops.build_gild(out, enchant_ids())
    forge_ops.build_sources(out)
    forge_ops.build_runes(out)
    forge_ops.build_stones(out)
    forge_ops.build_smelt(out, smelt_functions())
    forge_runtime.build_tick(out)
    forge_runtime.build_player(out)
    conv = forge_runtime.build_conv(out, items)
    forge_runtime.build_hit(out)
    forge_runtime.build_sources(out)
    forge_runtime.build_runes(out)
    forge_runtime.build_arrows(out)
    forge_runtime.build_fx(out)
    forge_runtime.build_stones(out, volley_offsets())
    forge_runtime.build_hud(out)
    nfiles = out.flush()
    removed = build_give(items)
    nloot, report, retired, minions = build_loot(items)
    wire()
    nret = retire()
    print("forge: %d functions/files, %d old give lines replaced, %d item tables, mobs %s, %d minion tables, "
          "%d retired tables, %d retired functions, %d old-item conversions; migration: %d native holy flags, "
          "%d names, %d right-click restores"
          % (nfiles, removed, nloot, ",".join(sorted(report)), minions, retired, nret, conv,
             len(mig["native_holy"]), len(mig["names"]), len(mig["uses"])))


if __name__ == "__main__":
    main()
