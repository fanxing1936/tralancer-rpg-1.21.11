# -*- coding: utf-8 -*-
"""罪器锻造与材料转换（策划书第三步，用户 2026-11-23：罪器锻造带魔化代价；原版合成禁用，转换只在锻造对话框里做）。

    python add_forge_world.py ../rpg

入口：主手器胚对准灵魂营火右键 → 魂火冶炼对话框底部的「罪器锻造」「材料转换」（forge_ops.build_smelt，
按钮 50..59 / 60..69 交给这里的 rpg:forge/sin/do、rpg:forge/conv/do）。对话框用 forge_ops.dialog，样式与冶炼一致。

* 罪印碎片：[恶魔]（该柱亮色）罪印碎片 · <领主>；该柱 5 名罪仆各 30%（玩家亲手击杀）。图标 rpg:world/sin_shard，按柱色染。
* 罪器锻造：武器核心 · 该柱 ×1、罪印碎片 ×8、下界合金锭 ×1、器胚 ×1（主手那块）、残魂 ×8，原质 ≥ 5；
  锻成时魔化 +15（圣力者照常折成生命力与同化）。边缘者不要下界合金锭；七大罪之仆锻本柱只要 4 片碎片。
  成品就是驱魔「契约」结局给的那件（rpg:inquest/give/pact_weapon<n>）。
* 材料转换：32 铁锭 + 4 残魂 → 1 钻石；16 钻石 + 8 残魂 → 1 下界合金锭；9 金粒 → 1 金锭；4 金锭 → 1 镀金箔。
"""
import io
import json
import os
import sys

import forge_ops as FO
import forge_spec as S
import rpg_ui_style as ui
from forge_ops import NL, T_BODY, T_HOLY, T_MUTED, T_NAME, T_WARN, dialog, say, tt

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function", "forge")
LOOT = os.path.join(DP, "data", "rpg", "loot_table")
COUNT = 0
SHARDS, SHARDS_OWN, SOULS, TAINT, SEF = 8, 4, 8, 15, 5
LORDS = [(p["n"], p["slug"], p["who"], p["lit"]) for p in ui.PILLARS]
CORE = "minecraft:nether_star[minecraft:custom_data~{rpg_weapon_core:1b,rpg_lord:%d}]"
SHARD = "minecraft:paper[minecraft:custom_data~{rpg_mat:\"sin_shard\",rpg_lord:%d}]"
SOUL = "minecraft:paper[minecraft:custom_data~{rpg_mat:\"soul\"}]"
NETH = "minecraft:netherite_ingot[!minecraft:custom_data]"


def fn(name, lines):
    global COUNT
    path = os.path.join(FUNC, name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT += 1


def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def seg(text, colour, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


# ============================================================================ 物品与掉落
def items():
    rule = ["", seg(ui.RULE_TEXT, ui.WHITE)]
    for n, slug, who, lit in LORDS:
        entry = {"type": "minecraft:item", "name": "minecraft:paper", "functions": [
            {"function": "minecraft:set_components", "components": {
                "minecraft:custom_name": ["", seg("[恶魔]", lit, True), seg("罪印碎片 · " + who, ui.WHITE)],
                "minecraft:lore": [rule, ["", seg("从", ui.GRAY), seg(who, lit, True), seg("麾下罪仆身上剥下的罪印", ui.GRAY)],
                                   ["", seg("锻造该柱罪器要 %d 片" % SHARDS, ui.GRAY)], rule],
                "minecraft:item_model": "rpg:world/sin_shard",
                "minecraft:custom_model_data": {"colors": [int(lit.lstrip("#"), 16)]},
                "minecraft:max_stack_size": 64}},
            {"function": "minecraft:set_custom_data", "tag": "{rpg_mat:\"sin_shard\",rpg_lord:%d}" % n}]}
        wj(os.path.join(LOOT, "world", "sin_shard_%d.json" % n), {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": [entry]}]})
        # 该柱 5 名罪仆各 30%
        mdir = os.path.join(LOOT, "minion", slug)
        if not os.path.isdir(mdir):
            continue
        for f in sorted(os.listdir(mdir)):
            p = os.path.join(mdir, f)
            doc = json.load(io.open(p, encoding="utf-8"))
            ref = "rpg:world/sin_shard_%d" % n
            if ref in json.dumps(doc):
                continue
            doc.setdefault("pools", []).append({"rolls": 1, "conditions": [
                {"condition": "minecraft:killed_by_player"}, {"condition": "minecraft:random_chance", "chance": 0.3}],
                "entries": [{"type": "minecraft:loot_table", "value": ref}]})
            wj(p, doc)
    # 转换产物：与世界掉落同一格式的 [锻造] 原料
    import add_world_loot as L
    for item in ("diamond", "netherite_ingot", "gold_ingot"):
        wj(os.path.join(LOOT, "world", "raw", item + ".json"),
           {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": [L.raw_entry(item, 1, 1)]}]})


# ============================================================================ 罪器锻造
def sin():
    fn("sin/do", [
        "# 罪器锻造的按钮：50 打开，51..57 选柱，58 开炉",
        "execute if score #do rpg_fg matches 50 run return run function rpg:forge/sin/open",
        "execute if score #do rpg_fg matches 51..57 run scoreboard players operation @s rpg_fg_arg = #do rpg_fg",
        "execute if score #do rpg_fg matches 51..57 run scoreboard players remove @s rpg_fg_arg 50",
        "execute if score #do rpg_fg matches 51..57 run return run function rpg:forge/sin/pick",
        "execute if score #do rpg_fg matches 58 run return run function rpg:forge/sin/start",
    ])
    count = []
    for n, slug, who, lit in LORDS:
        count += ["execute store result storage rpg:forge d.c%d int 1 run clear @s %s 0" % (n, CORE % n),
                  "execute store result storage rpg:forge d.s%d int 1 run clear @s %s 0" % (n, SHARD % n)]
    fn("sin/count", count)
    body = [tt("罪器是罪的形体。消灭恶魔取得的", T_BODY), tt("武器核心", T_NAME, True),
            tt("，配上同柱罪仆身上的罪印碎片，可以在魂火里重新凝结。", T_BODY), NL,
            tt("原质 %d 阶起可锻；锻成时魔化 +%d。" % (SEF, TAINT), T_MUTED), NL, NL]
    for n, slug, who, lit in LORDS:
        body += [tt(who, lit, True), tt("　核心 ", T_MUTED), tt("$(c%d)" % n, T_NAME, True),
                 tt("　碎片 ", T_MUTED), tt("$(s%d)" % n, T_NAME, True), tt("/%d" % SHARDS, T_MUTED), NL]
    fn("sin/open", ["function rpg:forge/sin/count", "function rpg:forge/sin/open_show with storage rpg:forge d"])
    fn("sin/open_show", ["$" + dialog("罪器锻造 · 选柱", body, [(who, lit, 50 + n) for n, slug, who, lit in LORDS])])
    # 需要多少：#need_s 碎片、#need_n 下界合金锭
    pick = ["# 选了第 rpg_fg_arg 柱",
            "execute unless score @s rpg_sef matches %d.. run return run %s" % (SEF, say("原质要到第 %d 阶（美丽阶）才能锻罪器" % SEF, T_WARN))]
    for n, slug, who, lit in LORDS:
        pick.append("execute if score @s rpg_fg_arg matches %d run return run function rpg:forge/sin/pick_%d" % (n, n))
    fn("sin/pick", pick)
    for n, slug, who, lit in LORDS:
        need = ["scoreboard players set #need_s rpg_fg %d" % SHARDS,
                "execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches %d run scoreboard players set #need_s rpg_fg %d" % (n, SHARDS_OWN),
                "scoreboard players set #need_n rpg_fg 1",
                "execute if score @s rpg_ident matches 2 run scoreboard players set #need_n rpg_fg 0",
                "execute store result storage rpg:forge d.ns int 1 run scoreboard players get #need_s rpg_fg",
                "execute store result storage rpg:forge d.nn int 1 run scoreboard players get #need_n rpg_fg"]
        fn("sin/need_%d" % n, need)
        check = ["# 核对第 %d 柱（%s）的材料：#ok 1 = 够" % (n, who),
                 "function rpg:forge/sin/need_%d" % n,
                 "scoreboard players set #ok rpg_fg 0",
                 'execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank"}] run return run %s' % say("主手要拿着器胚", T_WARN),
                 "execute store result score #c rpg_fg run clear @s %s 0" % (CORE % n),
                 "execute unless score #c rpg_fg matches 1.. run return run %s" % say("没有%s的武器核心（驱魔裁决选「消灭」取得）" % who, T_WARN),
                 "execute store result score #c rpg_fg run clear @s %s 0" % (SHARD % n),
                 "execute unless score #c rpg_fg >= #need_s rpg_fg run return run %s" % say("%s的罪印碎片不够" % who, T_WARN),
                 "execute store result score #c rpg_fg run clear @s %s 0" % NETH,
                 "execute unless score #c rpg_fg >= #need_n rpg_fg run return run %s" % say("下界合金锭不够", T_WARN),
                 "execute store result score #c rpg_fg run clear @s %s 0" % SOUL,
                 "execute unless score #c rpg_fg matches %d.. run return run %s" % (SOULS, say("残魂不够（要 %d 枚）" % SOULS, T_WARN)),
                 "scoreboard players set #ok rpg_fg 1"]
        fn("sin/check_%d" % n, check)
        conf = [tt("将锻造　", T_MUTED), tt("[恶魔]", lit, True), tt(who, T_NAME, True), NL,
                tt("消耗　", T_MUTED), tt("武器核心 ×1、罪印碎片 ×$(ns)、下界合金锭 ×$(nn)、器胚 ×1、残魂 ×%d" % SOULS, T_BODY), NL,
                tt("代价　", T_MUTED), tt("魔化 +%d（圣力者折成生命力与同化）" % TAINT, T_WARN), NL, NL,
                tt("罪器带着罪的影子。用得越久，越接近原本的主人。", T_MUTED)]
        fn("sin/pick_%d" % n, ["function rpg:forge/sin/check_%d" % n,
                               "execute unless score #ok rpg_fg matches 1 run return 0",
                               "function rpg:forge/sin/confirm_%d with storage rpg:forge d" % n])
        fn("sin/confirm_%d" % n, ["$" + dialog("罪器锻造 · 确认", conf, [("开炉", T_HOLY, 58)])])
        fn("sin/forge_%d" % n, [
            "# 扣料、给罪器（与驱魔「契约」结局给的是同一件）",
            "clear @s %s 1" % (CORE % n),
            "execute store result storage rpg:forge d.k int 1 run scoreboard players get #need_s rpg_fg",
            "function rpg:forge/sin/take_shard_%d with storage rpg:forge d" % n,
            "execute if score #need_n rpg_fg matches 1 run clear @s %s 1" % NETH,
            "clear @s %s %d" % (SOUL, SOULS),
            FO.CONSUME,
            "scoreboard players add @s rpg_taint %d" % TAINT,
            "function rpg:inquest/give/pact_weapon%d" % n,
            "execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.3 0.5 0.3 0.05 60",
            "execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:dust{color:%s,scale:1.4} ~ ~1 ~ 0.4 0.6 0.4 0 40" % rgb(lit),
            "playsound minecraft:block.end_portal.spawn player @s ~ ~ ~ 0.6 0.8",
            "playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 1 0.6",
            "tellraw @s " + FO.J(["", tt("[锻造]", S.C_FORGE, True), tt("　罪器在魂火里凝结：", T_BODY), tt("[恶魔]", lit, True),
                                  tt(who, T_NAME, True), tt("　魔化 +%d" % TAINT, T_WARN)]),
        ])
        fn("sin/take_shard_%d" % n, ["$clear @s %s $(k)" % (SHARD % n)])
    start = ["# 开炉：靠近灵魂火、再核对一遍",
             "scoreboard players operation #me rpg_fg = @s rpg_fg_id",
             "scoreboard players set #fire rpg_fg 0",
             "execute as @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8] if score @s rpg_fg_eo = #me rpg_fg at @s if block ~ ~ ~ #rpg:forge/soul_fire run scoreboard players set #fire rpg_fg 1",
             "execute if score #fire rpg_fg matches 0 run return run %s" % say("离灵魂火太远了，靠近些再开炉", T_WARN)]
    for n, slug, who, lit in LORDS:
        start += ["execute if score @s rpg_fg_arg matches %d run function rpg:forge/sin/check_%d" % (n, n),
                  "execute if score @s rpg_fg_arg matches %d if score #ok rpg_fg matches 1 run return run function rpg:forge/sin/forge_%d" % (n, n)]
    fn("sin/start", start)


def rgb(hexcol):
    h = hexcol.lstrip("#")
    return "[%.2f,%.2f,%.2f]" % tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


# ============================================================================ 材料转换
CONV = [  # (按钮, 名, 消耗 [(物品选择器, 数量, 名)], 产物 loot 表, 产物名)
    (61, "钻石", [("minecraft:iron_ingot[!minecraft:custom_data]", 32, "铁锭"), (SOUL, 4, "残魂")], "rpg:world/raw/diamond", "钻石 ×1"),
    (62, "下界合金锭", [("minecraft:diamond[!minecraft:custom_data]", 16, "钻石"), (SOUL, 8, "残魂")], "rpg:world/raw/netherite_ingot", "下界合金锭 ×1"),
    (63, "金锭", [("minecraft:gold_nugget[!minecraft:custom_data]", 9, "金粒")], "rpg:world/raw/gold_ingot", "金锭 ×1"),
    (64, "镀金箔", [("minecraft:gold_ingot[!minecraft:custom_data]", 4, "金锭")], "rpg:forge/item/gild_leaf", "镀金箔 ×1"),
]


def conv():
    do = ["# 材料转换：60 打开，61..64 换一次",
          "execute if score #do rpg_fg matches 60 run return run function rpg:forge/conv/open"]
    for b, name, cost, out, out_name in CONV:
        do.append("execute if score #do rpg_fg matches %d run return run function rpg:forge/conv/r%d" % (b, b))
        lines = ["# 换%s" % name]
        for sel, k, nm in cost:
            lines += ["execute store result score #c rpg_fg run clear @s %s 0" % sel,
                      "execute unless score #c rpg_fg matches %d.. run return run %s" % (k, say("%s不够（要 %d）" % (nm, k), T_WARN))]
        lines += ["clear @s %s %d" % (sel, k) for sel, k, nm in cost]
        lines += ["loot give @s loot %s" % out,
                  "playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 0.8 1.2",
                  "tellraw @s " + FO.J(["", tt("[锻造]", S.C_FORGE, True), tt("　换得 ", T_BODY), tt(out_name, T_NAME, True)]),
                  "function rpg:forge/conv/open"]
        fn("conv/r%d" % b, lines)
    fn("conv/do", do)
    count = ["execute store result storage rpg:forge d.vi int 1 run clear @s minecraft:iron_ingot[!minecraft:custom_data] 0",
             "execute store result storage rpg:forge d.vd int 1 run clear @s minecraft:diamond[!minecraft:custom_data] 0",
             "execute store result storage rpg:forge d.vg int 1 run clear @s minecraft:gold_ingot[!minecraft:custom_data] 0",
             "execute store result storage rpg:forge d.vn int 1 run clear @s minecraft:gold_nugget[!minecraft:custom_data] 0",
             "execute store result storage rpg:forge d.vs int 1 run clear @s %s 0" % SOUL]
    fn("conv/count", count)
    body = [tt("原版合成已经禁用，材料只能在魂火边换。比例故意很亏，只是保底。", T_BODY), NL, NL]
    for b, name, cost, out, out_name in CONV:
        body += [tt(name, T_NAME, True), tt("　" + " + ".join("%s ×%d" % (nm, k) for _s, k, nm in cost), T_BODY), NL]
    body += [NL, tt("背包里　", T_MUTED),
             tt("铁锭 $(vi)　钻石 $(vd)　金锭 $(vg)　金粒 $(vn)　残魂 $(vs)", T_NAME)]
    fn("conv/open", ["function rpg:forge/conv/count", "function rpg:forge/conv/show with storage rpg:forge d"])
    fn("conv/show", ["$" + dialog("材料转换", body, [("换" + name, T_HOLY, b) for b, name, *_r in CONV], exit_label="合上")])


def main():
    items()
    sin()
    conv()
    print("forge world: %d functions (sin forging for %d lords, %d conversions)" % (COUNT, len(LORDS), len(CONV)))


if __name__ == "__main__":
    main()
