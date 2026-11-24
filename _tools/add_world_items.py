# -*- coding: utf-8 -*-
"""图纸、特殊材料与原先拿不到的东西（策划书第四步，用户 2026-11-23）。

    python add_world_items.py ../rpg

* 7 种特殊材料（[锻造]，Codex 图标 rpg:world/<名>）、21 张图纸（[史诗]/[传说]图纸 · <武器>）、图纸碎片。
* 图纸锻造：主手器胚、副手图纸，对准灵魂营火 → 魂火冶炼对话框「图纸锻造」（按钮 70..79）。
  史诗：图纸 + 特殊材料 ×1 + 钻石 ×6 + 器胚 + 残魂 ×4，原质 ≥ 4；传说：图纸 + 特殊材料 ×3 + 下界合金锭 ×2 + 器胚 + 残魂 ×6，原质 ≥ 6。
  成品就是图鉴里那一件（从 command/give 里按名字和玩法标签找到原 give 行，原样发）。
* 图纸碎片 ×10 → 自选图纸：材料转换里的「碎片合图纸」（按钮 65，选图纸 80..100）。
* 来源：首领精英（特殊材料按组 25%、传说图纸 4%、史诗图纸 8%、碎片 30%）、普通精英（史诗图纸 1%）、
  地下（y < 0）首领的山岩之心、远古守卫者的深海之泪、圣卫的圣殿铜；Boss 首杀给一张主题传说图纸。
* 卡巴拉：路西法 → 血契、教皇 → 真·十字架、米迦勒 → 王冠、篡夺者 → 智慧、扫罗 → 严厉、雅克 → 美丽（首杀必掉，之后 20%）；
  胜利 = 累计击杀 100 名精英；王国 = 世界怪物 0.1%。其余（理解、慈悲、光辉、基础）在事件与支线里给。
* 七大罪之仆到原质第 3 阶，自己领主的未立约契约书会出现在背包里。
"""
import io
import json
import os
import re
import sys

import forge_ops as FO
import forge_spec as FS
import rpg_ui_style as ui
import world_loot_spec as W
from forge_ops import NL, T_BODY, T_HOLY, T_MUTED, T_NAME, T_WARN, dialog, say, tt

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
LOOT = os.path.join(DP, "data", "rpg", "loot_table")
COUNT = 0
C_FORGE = FS.C_FORGE

# 特殊材料：id → (名, 图标, 两行说明)
SPECIAL = {
    "star": ("星辰残片", "star_fragment", ["从天上掉下来的光", "锻造无垠星空等武器"]),
    "wind": ("风之精魄", "wind_essence", ["被困住的一阵风", "锻造风之回响、疾风迸发之弓"]),
    "tear": ("深海之泪", "abyss_tear", ["深海里结成的宝石", "锻造利维坦之歌、蔚蓝追寻者"]),
    "core": ("熔核", "molten_core", ["还在发烫的石核", "锻造熔火之锤、薪炎之傲"]),
    "stone": ("山岩之心", "mountain_heart", ["地底深处的岩心", "锻造高山之啸、大地之脊"]),
    "bronze": ("圣殿铜", "temple_bronze", ["圣卫铠甲上剥下的铜", "锻造雅斤、波阿斯、竖琴弩"]),
    "soil": ("墓土", "grave_soil", ["埋过太多死人的土", "锻造坟墓克星、剧毒之牙"]),
}
# 武器：id, 名, 档（epic/legend）, 特殊材料, 玩法标签（找 give 行）
WEAPONS = [
    ("starry", "无垠星空", "legend", "star", "saber_tag"),
    ("leviathan_song", "利维坦之歌", "legend", "tear", "bubble_tag"),
    ("flame_pride", "薪炎之傲", "legend", "core", "burn_tag"),
    ("wind_echo", "风之回响", "legend", "wind", "typhoon_tag"),
    ("mountain_roar", "高山之啸", "legend", "stone", "montain_tag"),
    ("grave_bane", "坟墓克星", "legend", "soil", "grave_bane_tag"),
    ("harp_crossbow", "竖琴弩", "legend", "bronze", "harp_crossbow_tag"),
    ("azure_seeker", "蔚蓝追寻者", "legend", "tear", "deep_seek_tag"),
    ("gale_bow", "疾风迸发之弓", "legend", "wind", "rift_tag"),
    ("jachin", "雅斤", "legend", "bronze", "jachin_tag"),
    ("boaz", "波阿斯", "legend", "bronze", "boaz_tag"),
    ("molten_hammer", "熔火之锤", "legend", "core", "forge_tag"),
    ("dark_sun", "漆黑之日", "epic", "star", "night_tag"),
    ("chainsaw", "切割链锯", "epic", "core", "chainsaw_tag"),
    ("earth_spine", "大地之脊", "epic", "stone", "montain_tag"),
    ("venom_fang", "剧毒之牙", "epic", "soil", "potion_tag"),
    ("wind_bone", "风骨", "epic", "wind", "pen_tag"),
    ("mischief_bow", "稚弩", "epic", "wind", "mischief_tag"),
    ("vine_whip", "藤蔓之鞭", "epic", "stone", "vine_tag"),
    ("truth_blade", "求真之刃", "epic", "bronze", "truth_tag"),
    ("crystal_roar", "晶啸", "epic", "tear", "chime_tag"),
]
COST = {"epic": dict(sp=1, main=("minecraft:diamond[!minecraft:custom_data]", 6, "钻石"), souls=4, sef=4),
        "legend": dict(sp=3, main=("minecraft:netherite_ingot[!minecraft:custom_data]", 2, "下界合金锭"), souls=6, sef=6)}
TIER_TAG = {"epic": "[史诗]", "legend": "[传说]"}
# 精英组 → 首领掉的特殊材料
GROUP_SP = {"undead": "soil", "arthropod": "stone", "explosive": "stone", "arcane": "wind", "nether": "core",
            "end": "star", "water": "tear"}
# Boss → (首杀传说图纸, 卡巴拉物品 give 行号：2 血契、3..12 第 1..10 源质、13 真·十字架)
BOSS_GIFT = {"michael": ("gale_bow", 3), "usurper": ("azure_seeker", 4), "saul": ("mountain_roar", 7),
             "jacques": ("grave_bane", 8), "lucifer": ("flame_pride", 2), "pope": ("jachin", 13)}
SOUL = "minecraft:paper[minecraft:custom_data~{rpg_mat:\"soul\"}]"


def fn(name, lines):
    global COUNT
    path = os.path.join(FUNC, name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT += 1


def read(rel):
    return io.open(os.path.join(FUNC, rel), encoding="utf-8").read()


def write(rel, s):
    io.open(os.path.join(FUNC, rel), "w", encoding="utf-8", newline="\n").write(s)


def patch(rel, guard, text, where="end"):
    s = read(rel)
    if guard in s:
        return
    if where == "end":
        s = s.rstrip("\n") + "\n" + text
    else:
        assert where in s, (rel, where)
        s = s.replace(where, text + where, 1)
    write(rel, s)


def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def seg(text, colour, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


RULE = ["", seg(ui.RULE_TEXT, ui.WHITE)]


def item_entry(model, prefix, colour, name, lines, data, stack=64):
    return {"type": "minecraft:item", "name": "minecraft:paper", "functions": [
        {"function": "minecraft:set_components", "components": {
            "minecraft:custom_name": ["", seg(prefix, colour, True), seg(name, ui.WHITE)],
            "minecraft:lore": [RULE] + [["", seg(l, ui.GRAY)] for l in lines] + [RULE],
            "minecraft:item_model": model, "minecraft:max_stack_size": stack}},
        {"function": "minecraft:set_custom_data", "tag": data}]}


def table(*entries):
    return {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": list(entries)}]}


# ============================================================================ 物品
def items():
    for k, (name, icon, lines) in SPECIAL.items():
        wj(os.path.join(LOOT, "world", "sp", k + ".json"),
           table(item_entry("rpg:world/" + icon, "[锻造]", C_FORGE, name, lines, "{rpg_mat:\"sp_%s\"}" % k)))
    for wid, name, tier, sp, _tag in WEAPONS:
        c = COST[tier]
        lines = ["锻造%s%s的图纸" % (TIER_TAG[tier], name),
                 "%s ×%d、%s ×%d、器胚、残魂 ×%d" % (SPECIAL[sp][0], c["sp"], c["main"][2], c["main"][1], c["souls"]),
                 "原质 %d 阶起；副手拿图纸，主手器胚对准魂火" % c["sef"]]
        wj(os.path.join(LOOT, "world", "bp", wid + ".json"),
           table(item_entry("rpg:world/blueprint_" + tier, TIER_TAG[tier], ui.tier_colour(tier), "图纸 · " + name, lines,
                            "{rpg_bp:\"%s\"}" % wid, stack=16)))
    for tier in ("epic", "legend"):
        wj(os.path.join(LOOT, "world", "bp_%s_any.json" % tier), {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": [
            {"type": "minecraft:loot_table", "value": "rpg:world/bp/" + w[0]} for w in WEAPONS if w[2] == tier]}]})
    wj(os.path.join(LOOT, "world", "bp_fragment.json"),
       table(item_entry("rpg:world/blueprint_fragment", "[锻造]", C_FORGE, "图纸碎片",
                        ["一角撕下来的旧图纸", "10 片在魂火边合成一张自选图纸"], "{rpg_mat:\"bp_frag\"}")))


# ============================================================================ 武器的 give 行
def weapon_gives():
    give_dir = os.path.join(FUNC, "command", "give")
    lines = []
    for f in sorted(os.listdir(give_dir)):
        if f.endswith(".mcfunction"):
            lines += io.open(os.path.join(give_dir, f), encoding="utf-8").read().splitlines()
    for wid, name, tier, sp, tag in WEAPONS:
        hit = [l for l in lines if l.startswith("give ") and ("%s:1b" % tag) in l and ("\"%s\"" % name) in l]
        assert hit, (wid, name)
        line = re.sub(r"^give @[a-z](\[[^\]]*\])? ", "give @s ", hit[0])
        fn("world/bp/give_%s" % wid, ["# %s%s（与图鉴里同一件）" % (TIER_TAG[tier], name), line])


# ============================================================================ 图纸锻造与碎片合图纸
def forge():
    find = ["# 副手图纸是哪一张 → rpg_fg_arg（1..21），0 = 没有"]
    find.append("scoreboard players set @s rpg_fg_arg 0")
    for i, w in enumerate(WEAPONS, 1):
        find.append("execute if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_bp:\"%s\"}] run scoreboard players set @s rpg_fg_arg %d" % (w[0], i))
    fn("forge/bp/find", find)
    fn("forge/bp/do", [
        "# 图纸锻造：70 打开（读副手图纸），71 开炉",
        "execute if score #do rpg_fg matches 70 run return run function rpg:forge/bp/open",
        "execute if score #do rpg_fg matches 71 run return run function rpg:forge/bp/start",
    ])
    op = ["function rpg:forge/bp/find",
          "execute if score @s rpg_fg_arg matches 0 run return run %s" % say("副手拿着图纸，主手拿器胚，再对准魂火右键", T_WARN)]
    st = ["# 开炉：靠近灵魂火、再核对一遍",
          "function rpg:forge/bp/find",
          "scoreboard players operation #me rpg_fg = @s rpg_fg_id",
          "scoreboard players set #fire rpg_fg 0",
          "execute as @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8] if score @s rpg_fg_eo = #me rpg_fg at @s if block ~ ~ ~ #rpg:forge/soul_fire run scoreboard players set #fire rpg_fg 1",
          "execute if score #fire rpg_fg matches 0 run return run %s" % say("离灵魂火太远了，靠近些再开炉", T_WARN)]
    for i, (wid, name, tier, sp, _t) in enumerate(WEAPONS, 1):
        c = COST[tier]
        spsel = "minecraft:paper[minecraft:custom_data~{rpg_mat:\"sp_%s\"}]" % sp
        chk = ["# 核对%s的材料：#ok 1 = 够" % name, "scoreboard players set #ok rpg_fg 0",
               "execute unless score @s rpg_sef matches %d.. run return run %s" % (c["sef"], say("原质要到第 %d 阶才能锻%s" % (c["sef"], TIER_TAG[tier]), T_WARN)),
               'execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank"}] run return run %s' % say("主手要拿着器胚", T_WARN),
               "execute store result score #c rpg_fg run clear @s %s 0" % spsel,
               "execute unless score #c rpg_fg matches %d.. run return run %s" % (c["sp"], say("%s不够（要 %d）" % (SPECIAL[sp][0], c["sp"]), T_WARN)),
               "execute store result score #c rpg_fg run clear @s %s 0" % c["main"][0],
               "execute unless score #c rpg_fg matches %d.. run return run %s" % (c["main"][1], say("%s不够（要 %d）" % (c["main"][2], c["main"][1]), T_WARN)),
               "execute store result score #c rpg_fg run clear @s %s 0" % SOUL,
               "execute unless score #c rpg_fg matches %d.. run return run %s" % (c["souls"], say("残魂不够（要 %d）" % c["souls"], T_WARN)),
               "scoreboard players set #ok rpg_fg 1"]
        fn("forge/bp/check_%s" % wid, chk)
        conf = [tt("将锻造　", T_MUTED), tt(TIER_TAG[tier], ui.tier_colour(tier), True), tt(name, T_NAME, True), NL,
                tt("消耗　", T_MUTED), tt("图纸 ×1、%s ×%d、%s ×%d、器胚 ×1、残魂 ×%d" % (SPECIAL[sp][0], c["sp"], c["main"][2], c["main"][1], c["souls"]), T_BODY), NL, NL,
                tt("锻约 3 秒，成品交到你手上。", T_MUTED)]
        fn("forge/bp/confirm_%s" % wid, [dialog("图纸锻造 · 确认", conf, [("开炉", T_HOLY, 71)])])
        op.append("execute if score @s rpg_fg_arg matches %d run function rpg:forge/bp/check_%s" % (i, wid))
        op.append("execute if score @s rpg_fg_arg matches %d if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/confirm_%s" % (i, wid))
        st.append("execute if score @s rpg_fg_arg matches %d run function rpg:forge/bp/check_%s" % (i, wid))
        st.append("execute if score @s rpg_fg_arg matches %d if score #ok rpg_fg matches 1 run return run function rpg:forge/bp/make_%s" % (i, wid))
        fn("forge/bp/make_%s" % wid, [
            "item replace entity @s weapon.offhand with minecraft:air",
            "clear @s %s %d" % (spsel, c["sp"]),
            "clear @s %s %d" % (c["main"][0], c["main"][1]),
            "clear @s %s %d" % (SOUL, c["souls"]),
            FO.CONSUME,
            "function rpg:world/bp/give_%s" % wid,
            "execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.3 0.5 0.3 0.05 60",
            "playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 1 0.8",
            "playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.2",
            "tellraw @s " + FO.J(["", tt("[锻造]", C_FORGE, True), tt("　按图纸锻成：", T_BODY),
                                  tt(TIER_TAG[tier], ui.tier_colour(tier), True), tt(name, T_NAME, True)]),
        ])
    fn("forge/bp/open", op)
    fn("forge/bp/start", st)
    # 碎片合图纸（材料转换的 65，选哪张 80..100）
    frag = "minecraft:paper[minecraft:custom_data~{rpg_mat:\"bp_frag\"}]"
    pick = [tt("10 片图纸碎片合成一张自选图纸。", T_BODY), NL, tt("选一张：", T_MUTED)]
    fn("forge/bp/frag_open", [
        "execute store result score #c rpg_fg run clear @s %s 0" % frag,
        "execute unless score #c rpg_fg matches 10.. run return run %s" % say("图纸碎片不够（要 10 片）", T_WARN),
        dialog("碎片合图纸", pick, [(w[1], ui.tier_colour(w[2]), 80 + i) for i, w in enumerate(WEAPONS)], exit_label="合上")])
    sel = ["# 选了第 #do - 80 张",
           "execute store result score #c rpg_fg run clear @s %s 0" % frag,
           "execute unless score #c rpg_fg matches 10.. run return run %s" % say("图纸碎片不够（要 10 片）", T_WARN)]
    for i, w in enumerate(WEAPONS):
        sel.append("execute if score #do rpg_fg matches %d run loot give @s loot rpg:world/bp/%s" % (80 + i, w[0]))
    sel += ["clear @s %s 10" % frag, "playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8"]
    fn("forge/bp/frag_do", sel)
    # 冶炼对话框：图纸锻造按钮 + 路由；材料转换里加「碎片合图纸」
    import forge_ops  # noqa
    patch("forge/smelt/do.mcfunction", "rpg:forge/bp/do",
          "execute if score #do rpg_fg matches 70..79 run return run function rpg:forge/bp/do\n"
          "execute if score #do rpg_fg matches 80..109 run return run function rpg:forge/bp/frag_do\n",
          where="execute if score #do rpg_fg matches 20..28 run scoreboard players operation")
    patch("forge/conv/do.mcfunction", "rpg:forge/bp/frag_open",
          "execute if score #do rpg_fg matches 65 run return run function rpg:forge/bp/frag_open\n")


def smelt_buttons():
    """把「图纸锻造」「碎片合图纸」按钮加进两个对话框（改已生成的对话框 JSON）。"""
    for rel, label, code in (("forge/smelt/open.mcfunction", "图纸锻造", 70), ("forge/conv/show.mcfunction", "碎片合图纸", 65)):
        s = read(rel)
        if "rpg_fg_do set %d\"" % code in s:
            continue
        lines = s.rstrip("\n").split("\n")
        idx = next(i for i, l in enumerate(lines) if "dialog show @s " in l)
        line = lines[idx]
        pre, js = line.split("dialog show @s ", 1)
        doc = json.loads(js)
        doc["actions"].append({"label": tt(label, T_HOLY, True),
                               "action": {"type": "minecraft:run_command", "command": "/trigger rpg_fg_do set %d" % code}})
        lines[idx] = pre + "dialog show @s " + FO.J(doc)
        write(rel, "\n".join(lines) + "\n")


# ============================================================================ 来源
def sources():
    rnd = lambda p: [{"condition": "minecraft:random_chance", "chance": p}]
    for g in W.GROUPS:
        champ = {"type": "minecraft:generic", "pools": [
            {"rolls": 1, "conditions": rnd(0.25), "entries": [{"type": "minecraft:loot_table", "value": "rpg:world/sp/" + GROUP_SP[g]}]},
            {"rolls": 1, "conditions": rnd(0.04), "entries": [{"type": "minecraft:loot_table", "value": "rpg:world/bp_legend_any"}]},
            {"rolls": 1, "conditions": rnd(0.08), "entries": [{"type": "minecraft:loot_table", "value": "rpg:world/bp_epic_any"}]},
            {"rolls": {"type": "minecraft:uniform", "min": 1, "max": 2}, "conditions": rnd(0.30),
             "entries": [{"type": "minecraft:loot_table", "value": "rpg:world/bp_fragment"}]}]}
        wj(os.path.join(LOOT, "world", "elite_extra", g + "_champion.json"), champ)
        wj(os.path.join(LOOT, "world", "elite_extra", g + ".json"), {"type": "minecraft:generic", "pools": [
            {"rolls": 1, "conditions": rnd(0.01), "entries": [{"type": "minecraft:loot_table", "value": "rpg:world/bp_epic_any"}]}]})
        patch("elite/kill/%s.mcfunction" % g, "elite_extra",
              "loot give @s loot rpg:world/elite_extra/%s\n"
              "execute if score @s rpg_el_kill matches 100 run function rpg:world/kab/give_victory\n" % g)
        patch("elite/kill/%s_champion.mcfunction" % g, "elite_extra",
              "loot give @s loot rpg:world/elite_extra/%s_champion\n"
              "execute if entity @s[y=-64,dy=63] if predicate {condition:\"minecraft:random_chance\",chance:0.25} run loot give @s loot rpg:world/sp/stone\n"
              "execute if score @s rpg_el_kill matches 100 run function rpg:world/kab/give_victory\n" % g)
    # 远古守卫者 50% 深海之泪
    p = os.path.join(DP, "data", "minecraft", "loot_table", "entities", "elder_guardian.json")
    doc = json.load(io.open(p, encoding="utf-8"))
    if "rpg:world/sp/tear" not in json.dumps(doc):
        doc["pools"].append({"rolls": 1, "conditions": [{"condition": "minecraft:killed_by_player"}] + rnd(0.5),
                             "entries": [{"type": "minecraft:loot_table", "value": "rpg:world/sp/tear"}]})
        wj(p, doc)
    # 王国：世界怪物 0.1%（玩家击杀进度 + 随机条件）
    wj(os.path.join(DP, "data", "rpg", "tags", "entity_type", "world_mobs.json"), {"values": ["minecraft:" + m for m in W.WORLD_TABLES]})
    wj(os.path.join(DP, "data", "rpg", "advancement", "world", "malkuth.json"), {
        "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
            {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": "#rpg:world_mobs"}},
            {"condition": "minecraft:random_chance", "chance": 0.001}]}}},
        "rewards": {"function": "rpg:world/kab/malkuth"}})
    fn("world/kab/malkuth", ["advancement revoke @s only rpg:world/malkuth", "function rpg:world/kab/line_12",
                             "tellraw @s " + FO.J(["", tt("[秘仪]", ui.RITUAL, True), tt("　尘土里有东西在发光：源质「王国」。", T_BODY)])])
    # 圣卫 20% 圣殿铜（三种圣卫各一个进度）
    for tag in ("rpg.hg", "rpg.tg", "rpg.rg"):
        wj(os.path.join(DP, "data", "rpg", "advancement", "world", "kill_%s.json" % tag.replace(".", "_")), {
            "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": "{Tags:[\"%s\"]}" % tag}}]}}},
            "rewards": {"function": "rpg:world/kill_guard_%s" % tag.split(".")[1]}})
        fn("world/kill_guard_%s" % tag.split(".")[1], [
            "advancement revoke @s only rpg:world/kill_%s" % tag.replace(".", "_"),
            "execute if predicate {condition:\"minecraft:random_chance\",chance:0.2} run loot give @s loot rpg:world/sp/bronze"])


# ============================================================================ 卡巴拉与契约书
def kabbalah():
    give = read("ritual/life_tree/give/all.mcfunction").splitlines()
    assert len(give) >= 13 and "rpg_kabbalah_contract" in give[1] and "rpg_true_cross" in give[12], "life_tree give lines moved"
    for ln in range(2, 14):
        fn("world/kab/line_%d" % ln, [give[ln - 1]])
    fn("world/kab/give_victory", [
        "# 累计击杀 100 名精英：第 7 源质「胜利」",
        "execute if entity @s[tag=rpg.wl.victory] run return 0",
        "tag @s add rpg.wl.victory",
        "function rpg:world/kab/line_9",
        "tellraw @s " + FO.J(["", tt("[秘仪]", ui.RITUAL, True), tt("　第一百名精英倒下。你得到了源质「胜利」。", T_BODY)])])
    for boss, (wid, ln) in BOSS_GIFT.items():
        name = next(w[1] for w in WEAPONS if w[0] == wid)
        fn("world/boss/first_%s" % boss, [
            "loot give @s loot rpg:world/bp/%s" % wid,
            "function rpg:world/kab/line_%d" % ln,
            "tellraw @s " + FO.J(["", tt("[秘仪]", ui.RITUAL, True), tt("　首次击败，额外得到图纸与一件秘仪之物。", T_BODY)])])
        fn("world/boss/again_%s" % boss, [
            "execute if predicate {condition:\"minecraft:random_chance\",chance:0.2} run function rpg:world/kab/line_%d" % ln])
        patch("sephira/boss/first_%s.mcfunction" % boss, "rpg:world/boss/first_%s" % boss,
              "function rpg:world/boss/first_%s\n" % boss)
        patch("sephira/boss/cr_%s.mcfunction" % boss, "rpg:world/boss/again_%s" % boss,
              "function rpg:world/boss/again_%s\n" % boss, where="execute if score @s rpg_bkd_%s matches 3.. run return 0" % boss)
    # 七大罪之仆：原质第 3 阶，自己领主的未立约契约书出现在背包里
    fn("world/pact_book", ["tag @s add rpg.wl.book"] +
       ["execute if score @s rpg_ident_sin matches %d run function rpg:inquest/give/pact%d" % (p["n"], p["n"]) for p in ui.PILLARS] +
       ["tellraw @s " + FO.J(["", tt("[契约]", ui.RITUAL, True), tt("　你的领主在你背包里留下了一本契约之书。", T_BODY)])])
    patch("world/recipe_scan.mcfunction", "rpg:world/pact_book",
          "execute as @a[scores={rpg_ident=4,rpg_sef=3..},tag=!rpg.wl.book] run function rpg:world/pact_book\n")


def validate():
    for w in WEAPONS:
        assert os.path.exists(os.path.join(FUNC, "world", "bp", "give_%s.mcfunction" % w[0])), w
    for b in BOSS_GIFT:
        assert "rpg:world/boss/first_%s" % b in read("sephira/boss/first_%s.mcfunction" % b)
    assert "rpg_fg_do set 70\"" in read("forge/smelt/open.mcfunction")


def main():
    items()
    weapon_gives()
    forge()
    smelt_buttons()
    sources()
    kabbalah()
    validate()
    print("world items: %d functions, %d special materials, %d blueprints" % (COUNT, len(SPECIAL), len(WEAPONS)))


if __name__ == "__main__":
    main()
