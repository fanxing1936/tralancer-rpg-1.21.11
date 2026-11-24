# -*- coding: utf-8 -*-
"""原质等级、力条与生命力（方案书「原质等级与身份能力方案书」第三版，用户 2026-11-23 批准）。

这一步（里程碑 A）做的：
  * 原质十阶：王国 → 王冠。晋阶只看「综合能力」= 阅历（rpg_ex_xp）+ 装备分（四件护甲和主手的装备等级之和 × 10），
    不绑任何 Boss（开放世界）。唯一的门是达阿特：这一版到了慈悲阶直接放行，留接口 rpg:sephira/daath/start。
  * 每阶：生命 +4、技能点、力条上限、锻造材料；第 2 阶选主柱，主柱加成按柱给。
  * 旧角色等级（经验等级加血）拆掉；驱魔等级退出成长：rpg_ex_lvl 只剩驱魔内部的「驱魔熟练」，
    按裁决次数 rpg_ex_rites 算（1/3/6 次），驱魔里零碎的阅历改记到 rpg_ex_dxp，不再进原质。
  * 阅历来源：击杀（普通每天前 300 只 +1、精英 +5）、六个 Boss（首杀 +80、之后每天每个前 3 次 +15）、
    裁决 +10、驱逐 +3。
  * 力：圣力 / 魔力各一根条（rpg_mana，弥赛亚的魔力在 rpg_mana2）。圣力者魔化那一行换成生命力（rpg_vital）：
    沾上的每一点魔化变成 1 点生命力损失和 1 点同化（rpg_assim），握圣器每 30 秒 -1；同化满 100 堕入魔力，
    解约且魔化回到 0 就重回圣力（得新约的人可以直接回头）。生命力归零是燃尽，回到 30 才解除。
  * 状态行：力条在同一条 actionbar 里占一个新槽 e，排在魔化（a）之后、契约（b）之前，不挤别的槽。
技能、终式、身份能力、传承技能书在下一步（里程碑 B）。
"""
import io
import json
import os
import re
import sys

import rpg_ui_style as ui
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "sephira")
P = "rpg:sephira"
O = "rpg_sef"
DO = "rpg_sef_do"
COUNT = 0

C_MUTED = "#9C9A94"
C_BODY = "#E6DFCF"
C_GOLD = "#C9A646"
C_HOLY = "#FFD85A"
C_MANA = "#A276BE"
C_VITAL = "#E86A6A"
C_ASSIM = "#9B6BD6"

# (阶, 键, 中文, 拉丁, 希伯来, 颜色, 柱 0 中 1 严厉 2 慈悲)
TIERS = [
    (1, "malkuth", "王国", "Malkuth", "מלכות", "#C58A62", 0),
    (2, "yesod", "基础", "Yesod", "יסוד", "#D596F2", 0),
    (3, "hod", "光辉", "Hod", "הוד", "#FF8A4A", 1),
    (4, "netzach", "胜利", "Netzach", "נצח", "#70DB70", 2),
    (5, "tiphareth", "美丽", "Tiphareth", "תפארת", "#FFD85A", 0),
    (6, "geburah", "严厉", "Geburah", "גבורה", "#FF5A62", 1),
    (7, "chesed", "慈悲", "Chesed", "חסד", "#62B8F0", 2),
    (8, "binah", "理解", "Binah", "בינה", "#AAB4C3", 1),
    (9, "chokmah", "智慧", "Chokmah", "חכמה", "#C9CDD6", 2),
    (10, "kether", "王冠", "Kether", "כתר", "#FFF2A8", 0),
]
THR = {1: 0, 2: 60, 3: 160, 4: 300, 5: 480, 6: 700, 7: 950, 8: 1250, 9: 1600, 10: 2000}
SP = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 1, 7: 2, 8: 1, 9: 2, 10: 2}
MATS = {
    2: [("blank", 2), ("soul", 4)],
    3: [("blank", 2), ("soul", 6), ("wash_gem", 1)],
    4: [("soul", 8), ("forge_stone", 2), ("gild_leaf", 1)],
    5: [("blank", 4), ("soul", 10), ("wash_gem", 2), ("rune", 1)],
    6: [("soul", 12), ("forge_stone", 3), ("gild_leaf", 1)],
    7: [("blank", 4), ("soul", 14), ("wash_gem", 2), ("stone", 1)],
    8: [("soul", 16), ("forge_stone", 4), ("gild_leaf", 2)],
    9: [("blank", 6), ("soul", 18), ("wash_gem", 3), ("rune", 1), ("stone", 1)],
    10: [("soul", 24), ("forge_stone", 6), ("gild_leaf", 3), ("wash_gem", 3)],
}
MAT_NAME = {"blank": "器胚", "soul": "残魂", "wash_gem": "洗炼钻", "forge_stone": "铸造之石", "gild_leaf": "镀金箔",
            "rune": "随机符文", "stone": "随机符石"}
MAT_LOOT = {"rune": "rpg:forge/rune_any", "stone": "rpg:forge/stone_any"}
PILLAR = {1: ("严厉柱", "进攻", "#FF5A62"), 2: ("慈悲柱", "守护与续命", "#62B8F0"), 3: ("中柱", "控制与机动", "#FFD85A")}
# 第 n 阶落在哪根柱上 —— 主柱加成只在「这一阶在你的主柱上」时给（rpg_pillar：1 严厉 2 慈悲 3 中）
TIER_PILLAR = {2: 3, 3: 1, 4: 2, 5: 3, 6: 1, 7: 2, 8: 1, 9: 2, 10: 3}
MANA_BASE = 100
DAILY_KILLS = 300
# 六个 Boss：(键, 中文, 胜利函数目录, 场地中心标记；None = 原地结算)
BOSSES = [("pope", "教皇", "pope_fight", None), ("usurper", "篡夺者", "usurper_boss", "rpg.usb.center"),
          ("jacques", "雅克", "jacques_boss", "rpg.jqb.center"), ("saul", "扫罗", "saul_boss", "rpg.slb.center"),
          ("michael", "米迦勒", "michael_boss", "rpg.mkb.center"), ("lucifer", "路西法", "lucifer_boss", "rpg.lub.center")]
# 身份 → 力（0 无 1 圣力 2 魔力 3 两者）
IDENT_FORCE = {1: 0, 2: 2, 3: 1, 4: 2, 5: 1, 6: 1, 7: 3}
BAR = 8


def fn(name, lines):
    global COUNT
    path = os.path.join(OUT, name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT += 1


def J(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def t(text, colour=C_BODY, bold=False, italic=False):
    return {"text": text, "color": colour, "bold": bold, "italic": italic}


NL = t("\n")


def say(parts):
    return "tellraw @s " + J(["", t("[原质] ", C_GOLD, True)] + parts)


def trig(v):
    return {"type": "minecraft:run_command", "command": "/trigger %s set %d" % (DO, v)}


def dialog(title, body, actions, columns=None, escape=True):
    doc = {"type": "minecraft:multi_action", "title": ["", t(title, C_GOLD, True)],
           "body": {"type": "minecraft:plain_message", "width": 320, "contents": [""] + body},
           "actions": [{"label": t(lab, col, True), "action": (trig(v) if isinstance(v, int) else v)} for lab, col, v in actions],
           "columns": columns or (1 if len(actions) == 1 else 2),
           "can_close_with_escape": escape, "pause": False, "after_action": "close"}
    if escape:
        doc["exit_action"] = {"label": t("合上", C_MUTED)}
    return "dialog show @s " + J(doc)


def read(rel):
    return io.open(os.path.join(FUNC, rel), encoding="utf-8").read()


def write(rel, s):
    io.open(os.path.join(FUNC, rel), "w", encoding="utf-8", newline="\n").write(s)


def patch(rel, guard, text, where="top"):
    s = read(rel)
    if guard in s:
        return
    if where == "top":
        s = text + s
    elif where == "end":
        s = s.rstrip("\n") + "\n" + text
    else:
        assert where in s, "%s 里找不到 %r" % (rel, where)
        s = s.replace(where, text + where, 1)
    write(rel, s)


def tier_of(n):
    return TIERS[n - 1]


# ============================================================================ 核心
def core():
    objs = [O, "rpg_power", "rpg_gear", "rpg_pillar", "rpg_sp", "rpg_sef_mig", "rpg_sef_day", "rpg_sef_dk", "rpg_daath",
            "rpg_ex_rites", "rpg_ex_dxp", "rpg_sef_lcd",
            "rpg_force", "rpg_mana", "rpg_mana2", "rpg_mana_max", "rpg_mana_f", "rpg_vital", "rpg_assim",
            "rpg_fz_t", "rpg_fz_h", "rpg_fz_r", "rpg_fz_tp", "rpg_fz_b", "rpg_fz_mv0"]
    load = ["scoreboard objectives add %s dummy" % o for o in objs]
    load += ["scoreboard objectives add %s trigger" % DO,
             "scoreboard objectives add rpg_fz_dd minecraft.custom:minecraft.damage_dealt",
             "scoreboard objectives add rpg_fz_sl minecraft.custom:minecraft.sleep_in_bed",
             "scoreboard objectives add rpg_fz_mv minecraft.custom:minecraft.walk_one_cm"]
    load += ["scoreboard objectives add rpg_bk_%s dummy" % b for b, _n, _d, _c in BOSSES]
    load += ["scoreboard objectives add rpg_bkd_%s dummy" % b for b, _n, _d, _c in BOSSES]
    load += ["scoreboard players set #20 %s 20" % O, "scoreboard players set #40 %s 40" % O,
             "scoreboard players set #10 %s 10" % O, "scoreboard players set #2 %s 2" % O,
             "scoreboard players set #3 %s 3" % O, "scoreboard players set #8 %s %d" % (O, BAR),
             "scoreboard players set #115 %s 115" % O, "scoreboard players set #100 %s 100" % O,
             "data modify storage rpg:hud e set value '{\"text\":\"\"}'"]
    fn("load", load)
    fn("tick", [
        "scoreboard players add #t %s 1" % O,
        "execute as @a[scores={%s=1..}] at @s run function %s/press" % (DO, P),
        "scoreboard players operation #m %s = #t %s" % (O, O),
        "scoreboard players operation #m %s %%= #20 %s" % (O, O),
        "execute unless score #m %s matches 0 run return 0" % O,
        "scoreboard players operation #m2 %s = #t %s" % (O, O),
        "scoreboard players operation #m2 %s %%= #40 %s" % (O, O),
        "execute store result score #day %s run time query day" % O,
        "execute as @a[tag=!rpg.ob.hold,tag=!rpg.pr] at @s run function %s/sec" % P,
    ])
    fn("sec", [
        "# 每秒一次（as/at 玩家）",
        "scoreboard players enable @s %s" % DO,
        "execute unless score @s rpg_sef_mig matches 1 run function %s/mig/run" % P,
        "execute unless score @s rpg_sef_day = #day %s run function %s/day" % (O, P),
        "execute unless score @s rpg_force matches 0.. if score @s rpg_ident matches 1.. run function %s/force/assign" % P,
        "execute if score #m2 %s matches 0 run function %s/tier/check" % (O, P),
        "execute if score @s rpg_force matches 1.. run function %s/force/sec" % P,
        "execute if score @s rpg_sef_lcd matches 1.. run scoreboard players remove @s rpg_sef_lcd 1",
        "# 慈悲柱第 9 阶：6 格内友方抗性 I",
        "execute if score #m2 %s matches 0 if score @s rpg_pillar matches 2 if score @s %s matches 9.. run effect give @a[distance=..6,gamemode=!spectator] minecraft:resistance 3 0 true" % (O, O),
    ])
    fn("day", ["scoreboard players operation @s rpg_sef_day = #day %s" % O, "scoreboard players set @s rpg_sef_dk 0"] +
       ["scoreboard players set @s rpg_bkd_%s 0" % b for b, _n, _d, _c in BOSSES])


# ============================================================================ 阶位
def gear_lines():
    out = ["scoreboard players set #g %s 0" % O]
    for slot in ("armor.head", "armor.chest", "armor.legs", "armor.feet", "weapon.mainhand"):
        for lv in range(1, 11):
            out.append("execute if items entity @s %s *[minecraft:custom_data~{rpg_eq:{lv:%d}}] run scoreboard players add #g %s %d"
                       % (slot, lv, O, lv))
    out += ["scoreboard players operation @s rpg_gear = #g %s" % O,
            "scoreboard players operation @s rpg_gear *= #10 %s" % O]
    return out


def tiers():
    chk = ["# 每两秒（as/at 玩家）：算综合能力，够了就晋阶。新手开局没走完的人还没入王国。",
           "execute unless score @s rpg_ob_v matches 1.. run return 0",
           "execute unless score @s rpg_ob matches 100 run return 0",
           "scoreboard players add @s rpg_ex_xp 0"] + gear_lines() + [
           "scoreboard players operation @s rpg_power = @s rpg_ex_xp",
           "scoreboard players operation @s rpg_power += @s rpg_gear",
           "execute unless score @s %s matches 1.. run function %s/tier/up_1" % (O, P)]
    for n in range(2, 11):
        if n == 8:
            chk.append("execute if score @s %s matches 7 unless score @s rpg_daath matches 1 run function %s/daath/start" % (O, P))
            chk.append("execute if score @s %s matches 7 if score @s rpg_daath matches 1 if score @s rpg_power matches %d.. run function %s/tier/up_8"
                       % (O, THR[8], P))
        else:
            chk.append("execute if score @s %s matches %d if score @s rpg_power matches %d.. run function %s/tier/up_%d"
                       % (O, n - 1, THR[n], P, n))
    fn("tier/check", chk)
    for n, key, zh, la, he, col, _pl in TIERS:
        lines = ["# 晋入第 %d 阶 · %s" % (n, zh),
                 "scoreboard players set @s %s %d" % (O, n),
                 "scoreboard players add @s rpg_sp %d" % SP[n],
                 "function %s/bonus/apply" % P]
        got = ["技能点 +%d" % SP[n]]
        if n > 1:
            got.insert(0, "生命 +4")
        for mat, k in MATS.get(n, []):
            loot = MAT_LOOT.get(mat, "rpg:forge/item/" + mat)
            lines += ["loot give @s loot %s" % loot] * k
            got.append("%s ×%d" % (MAT_NAME[mat], k))
        if n in (4, 7, 9):
            got.append("力条 +20")
        if n == 5:
            got.append("技能可升到 2 级")
        if n == 8:
            got.append("技能可升到 3 级")
        if n == 10:
            got.append("终式解锁")
        lines += [
            "title @s times 10 60 20",
            "title @s subtitle %s" % J(t("%s · %s" % (la, he), col, italic=True)),
            "title @s title %s" % J(["", t("晋入 · ", C_MUTED), t(zh, col, True)]),
            "playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.8 %.2f" % (0.7 + n * 0.06),
            "playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.2",
            "particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.05 40",
            say([t("晋入第 %d 阶 " % n, C_MUTED), t(zh, col, True), t("　" + "、".join(got), C_BODY)]),
        ]
        if n == 2:
            lines.append("execute unless score @s rpg_pillar matches 1..3 run function %s/pillar/ask" % P)
        if n == 5:
            lines.append("execute if score @s rpg_force matches 0 run function %s/force/awaken_ask" % P)
        fn("tier/up_%d" % n, lines)
    # 达阿特：接口。以后的影子对决只换这个函数的内容（用户 2026-11-23：「先直接跳过留个接口」）。
    fn("daath/start", [
        "# 越过深渊。这一版直接放行；影子对决做好以后从这里进场，赢了再调 rpg:sephira/daath/pass。",
        "function %s/daath/pass" % P,
    ])
    fn("daath/pass", [
        "scoreboard players set @s rpg_daath 1",
        "scoreboard players add @s rpg_ex_xp 100",
        "scoreboard players add @s rpg_sp 1",
        "title @s times 10 60 20",
        "title @s subtitle %s" % J(t("Daath · דעת", "#AAB4C3", italic=True)),
        "title @s title %s" % J(["", t("越过深渊", "#E6DFCF", True)]),
        "playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.5 1.4",
        say([t("达阿特已越过：阅历 +100、技能点 +1。", C_BODY)]),
    ])


# ============================================================================ 生命与主柱加成
def bonus():
    lines = ["# 按当前阶位和主柱重挂全部修饰符（晋阶、选柱、迁移时调）",
             "attribute @s minecraft:max_health modifier remove rpg:sephira",
             "attribute @s minecraft:attack_damage modifier remove rpg:sef_dmg",
             "attribute @s minecraft:attack_speed modifier remove rpg:sef_spd",
             "attribute @s minecraft:armor modifier remove rpg:sef_arm"]
    for n in range(2, 11):
        lines.append("execute if score @s %s matches %d run attribute @s minecraft:max_health modifier add rpg:sephira %d add_value" % (O, n, 4 * (n - 1)))
    lines += [
        "# 严厉柱：第 3、6 阶伤害各 +5%，第 8 阶攻速 +10%",
        "execute if score @s rpg_pillar matches 1 if score @s %s matches 3..5 run attribute @s minecraft:attack_damage modifier add rpg:sef_dmg 0.05 add_multiplied_base" % O,
        "execute if score @s rpg_pillar matches 1 if score @s %s matches 6.. run attribute @s minecraft:attack_damage modifier add rpg:sef_dmg 0.10 add_multiplied_base" % O,
        "execute if score @s rpg_pillar matches 1 if score @s %s matches 8.. run attribute @s minecraft:attack_speed modifier add rpg:sef_spd 0.10 add_multiplied_base" % O,
        "# 慈悲柱：第 4、7 阶护甲各 +2",
        "execute if score @s rpg_pillar matches 2 if score @s %s matches 4..6 run attribute @s minecraft:armor modifier add rpg:sef_arm 2 add_value" % O,
        "execute if score @s rpg_pillar matches 2 if score @s %s matches 7.. run attribute @s minecraft:armor modifier add rpg:sef_arm 4 add_value" % O,
        "# 力条上限：100，第 4、7、9 阶各 +20，中柱第 10 阶再 +40",
        "scoreboard players set @s rpg_mana_max %d" % MANA_BASE,
        "execute if score @s %s matches 4.. run scoreboard players add @s rpg_mana_max 20" % O,
        "execute if score @s %s matches 7.. run scoreboard players add @s rpg_mana_max 20" % O,
        "execute if score @s %s matches 9.. run scoreboard players add @s rpg_mana_max 20" % O,
        "execute if score @s rpg_pillar matches 3 if score @s %s matches 10 run scoreboard players add @s rpg_mana_max 40" % O,
    ]
    fn("bonus/apply", lines)
    fn("bonus/last_stand", [
        "# 慈悲柱第 7 阶：受致命伤时 3 秒抗性 II，冷却 3 分钟（as 挨打的玩家）",
        "execute if score @s rpg_sef_lcd matches 1.. run return 0",
        "execute store result score #hp %s run data get entity @s Health" % O,
        "execute unless score #hp %s matches ..6 run return 0" % O,
        "effect give @s minecraft:resistance 3 1 true",
        "scoreboard players set @s rpg_sef_lcd 180",
        "playsound minecraft:item.shield.block player @s ~ ~ ~ 1 0.6",
    ])


# ============================================================================ 主柱
def pillar():
    body = [t("你站在生命之树的第二阶。选一根柱，它是你技能树里最熟的那一支：", C_BODY), NL, NL]
    for k in (1, 2, 3):
        name, what, col = PILLAR[k]
        body += [t(name, col, True), t("　" + what, C_MUTED), NL]
    body += [NL, t("主柱那一支的技能升到 3 级少花 1 点；各阶的主柱加成也按这根柱给。选了不能改。", C_MUTED)]
    fn("pillar/ask", [dialog("原质 · 选择主柱", body, [(PILLAR[k][0], PILLAR[k][2], k) for k in (1, 2, 3)], columns=3)])
    for k in (1, 2, 3):
        name, what, col = PILLAR[k]
        fn("pillar/set_%d" % k, [
            "execute if score @s rpg_pillar matches 1..3 run return 0",
            "execute unless score @s %s matches 2.. run return 0" % O,
            "scoreboard players set @s rpg_pillar %d" % k,
            "function %s/bonus/apply" % P,
            "playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1",
            say([t("主柱：", C_MUTED), t(name, col, True), t("　" + what, C_MUTED)]),
        ])


# ============================================================================ 按钮
def press():
    lines = ["scoreboard players operation #do %s = @s %s" % (O, DO), "scoreboard players set @s %s 0" % DO]
    for k in (1, 2, 3):
        lines.append("execute if score #do %s matches %d run function %s/pillar/set_%d" % (O, k, P, k))
    lines += [
        "execute if score #do %s matches 9 run function %s/pillar/ask" % (O, P),
        "execute if score #do %s matches 11 run function %s/force/awaken_1" % (O, P),
        "execute if score #do %s matches 12 run function %s/force/awaken_2" % (O, P),
        "execute if score #do %s matches 19 run function %s/force/awaken_ask" % (O, P),
        "execute if score #do %s matches 20 run function %s/page/open" % (O, P),
        "execute if score #do %s matches 21 if entity @s[tag=rpg.fallen] if score @s rpg_lt_divine matches 2 run function %s/force/rise" % (O, P),
    ]
    fn("press", lines)


# ============================================================================ 迁移
def migrate():
    fn("mig/run", [
        "# 新版本第一次见到这名玩家（as 玩家）：拆旧角色等级的血、按经验等级折阅历、驱魔等级换成裁决次数",
        "scoreboard players set @s rpg_sef_mig 1",
    ] + ["attribute @s minecraft:max_health modifier remove minecraft:%d" % k for k in (64, 32, 16, 8, 4, 2, 1, 0)] + [
        "scoreboard players set @s rpg_hp_level 0",
        "execute store result score #xl %s run experience query @s levels" % O,
        "scoreboard players operation #xl %s *= #3 %s" % (O, O),
        "execute if score #xl %s matches 101.. run scoreboard players set #xl %s 100" % (O, O),
        "scoreboard players operation @s rpg_ex_xp += #xl %s" % O,
        "execute if score #xl %s matches 1.. run %s" % (O, say([t("旧的角色等级已经并入原质：按经验等级折算阅历 +", C_BODY),
                                                               {"score": {"name": "#xl", "objective": O}, "color": C_GOLD}])),
        "execute unless score @s rpg_ex_rites matches 1.. if score @s rpg_ex_lvl matches 2 run scoreboard players set @s rpg_ex_rites 1",
        "execute unless score @s rpg_ex_rites matches 1.. if score @s rpg_ex_lvl matches 3..4 run scoreboard players set @s rpg_ex_rites 3",
        "execute unless score @s rpg_ex_rites matches 1.. if score @s rpg_ex_lvl matches 5.. run scoreboard players set @s rpg_ex_rites 6",
        "scoreboard players add @s rpg_ex_rites 0",
    ])


# ============================================================================ 阅历来源
def sources():
    fn("kill", [
        "# 锻造的三档击杀进度（rpg_fg_kx：1 普通 5 精英 50 Boss）顺路记阅历；Boss 的大头由胜利结算给",
        "execute if score @s rpg_fg_kx matches 1 if score @s rpg_sef_dk matches ..%d run scoreboard players add @s rpg_ex_xp 1" % (DAILY_KILLS - 1),
        "execute if score @s rpg_fg_kx matches 1 run scoreboard players add @s rpg_sef_dk 1",
        "execute if score @s rpg_fg_kx matches 5.. run scoreboard players add @s rpg_ex_xp 5",
        "# 魔力：击杀 +4；圣力：杀死精英（恶魔、亡灵首领）+5",
        "execute if score @s rpg_force matches 2 run scoreboard players add @s rpg_mana 4",
        "execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana2 4",
        "execute if score @s rpg_force matches 1 if score @s rpg_fg_kx matches 5.. run scoreboard players add @s rpg_mana 5",
        "execute if score @s rpg_force matches 3 if score @s rpg_fg_kx matches 5.. run scoreboard players add @s rpg_mana 5",
    ])
    for b, zh, d, centre in BOSSES:
        fn("boss/" + b, ["execute as @a[distance=..48,gamemode=!spectator] run function %s/boss/cr_%s" % (P, b)])
        fn("boss/cr_" + b, [
            "scoreboard players add @s rpg_bk_%s 1" % b,
            "execute if score @s rpg_bk_%s matches 1 run return run function %s/boss/first_%s" % (b, P, b),
            "execute if score @s rpg_bkd_%s matches 3.. run return 0" % b,
            "scoreboard players add @s rpg_bkd_%s 1" % b,
            "scoreboard players add @s rpg_ex_xp 15",
            say([t("击败%s · 阅历 +15" % zh, C_BODY)]),
        ])
        fn("boss/first_" + b, [
            "scoreboard players add @s rpg_bkd_%s 1" % b,
            "scoreboard players add @s rpg_ex_xp 80",
            "scoreboard players add @s rpg_sp 1",
            say([t("首次击败", C_MUTED), t(zh, C_GOLD, True), t(" · 阅历 +80 · 技能点 +1", C_BODY)]),
        ])
    fn("rite/verdict", [
        "# 一次驱魔裁决完成（封印 / 立约 / 消灭）",
        "scoreboard players add @s rpg_ex_rites 1",
        "scoreboard players add @s rpg_ex_xp 10",
        say([t("裁决完成 · 阅历 +10 · 驱魔熟练按裁决次数提升", C_BODY)]),
    ])
    fn("rite/banish", [
        "# 驱逐了一个空缺者",
        "scoreboard players add @s rpg_ex_rites 1",
        "scoreboard players add @s rpg_ex_xp 3",
    ])


# ============================================================================ 力
def bar_lines(score, maxsrc, key):
    """把 score/max 换成 BAR 格，写进 rpg:sephira h.<key>f / <key>e 两段字符串。"""
    out = ["scoreboard players operation #p %s = @s %s" % (O, score),
           "scoreboard players operation #p %s *= #8 %s" % (O, O),
           "scoreboard players operation #p %s /= %s" % (O, maxsrc)]
    for k in range(BAR + 1):
        out.append('execute if score #p %s matches %s run data modify storage rpg:sephira h.%s set value {f:"%s",e:"%s"}'
                   % (O, ("%d" % k) if k < BAR else "%d.." % BAR, key, "▰" * k, "▱" * (BAR - k)))
    return out


def force():
    names = {0: "无", 1: "圣力", 2: "魔力", 3: "圣力与魔力"}
    lines = ["# 按身份分配力（as 玩家）。无知者先没有，美丽阶觉醒时自选。"]
    for ident, f in IDENT_FORCE.items():
        lines.append("execute if score @s rpg_ident matches %d run scoreboard players set @s rpg_force %d" % (ident, f))
    lines += ["scoreboard players set @s rpg_vital 100", "scoreboard players set @s rpg_assim 0",
              "scoreboard players set @s rpg_mana 0", "scoreboard players set @s rpg_mana2 0",
              "scoreboard players operation @s rpg_fz_tp = @s rpg_taint",
              "execute unless score @s rpg_mana_max matches 1.. run scoreboard players set @s rpg_mana_max %d" % MANA_BASE]
    fn("force/assign", lines)
    # 觉醒（无知者，美丽阶）
    fn("force/awaken_ask", [
        "execute unless score @s rpg_force matches 0 run return 0",
        "execute unless score @s %s matches 5.. run return 0" % O,
        dialog("原质 · 觉醒", [
            t("你在美丽阶第一次感觉到了力。它向两个方向拉你：", C_BODY), NL, NL,
            t("圣力", C_HOLY, True), t("　拿命换。放圣力、握圣器都会扣生命力。", C_MUTED), NL,
            t("魔力", C_MANA, True), t("　拿魂换。放魔力会涨魔化。", C_MUTED), NL, NL,
            t("选了就是你的力。攒下的技能点留着，到时一次点掉。", C_MUTED)],
            [("圣力", C_HOLY, 11), ("魔力", C_MANA, 12)])])
    for k, nm, col in ((1, "圣力", C_HOLY), (2, "魔力", C_MANA)):
        fn("force/awaken_%d" % k, [
            "execute unless score @s rpg_force matches 0 run return 0",
            "execute unless score @s %s matches 5.. run return 0" % O,
            "scoreboard players set @s rpg_force %d" % k,
            "scoreboard players set @s rpg_vital 100",
            "scoreboard players add @s rpg_sp 2",
            "title @s times 10 50 20",
            "title @s title %s" % J(["", t("觉醒 · ", C_MUTED), t(nm, col, True)]),
            "playsound minecraft:block.respawn_anchor.charge master @s ~ ~ ~ 1 1",
            say([t("觉醒为", C_MUTED), t(nm, col, True), t(" · 技能点 +2", C_BODY)]),
        ])
    fn("force/sec", [
        "# 每秒（as/at 有力的玩家）：回力、生命力",
        "execute if score @s rpg_force matches 1 run function %s/force/holy_regen" % P,
        "execute if score @s rpg_force matches 3 run function %s/force/holy_regen" % P,
        "execute if score @s rpg_force matches 2 run function %s/force/mana_regen" % P,
        "execute if score @s rpg_force matches 3 run function %s/force/mana_regen" % P,
        "execute if score @s rpg_force matches 1 run function %s/force/vital_sec" % P,
        "execute if entity @s[tag=rpg.fallen,tag=!rpg.pact] if score @s rpg_taint matches 0 run function %s/force/rise" % P,
        "execute if score @s rpg_mana > @s rpg_mana_max run scoreboard players operation @s rpg_mana = @s rpg_mana_max",
        "execute if score @s rpg_mana2 > @s rpg_mana_max run scoreboard players operation @s rpg_mana2 = @s rpg_mana_max",
        "scoreboard players operation @s rpg_fz_mv0 = @s rpg_fz_mv",
        "scoreboard players set @s rpg_fz_dd 0",
    ])
    fn("force/holy_regen", [
        "# 圣力：每秒 +1，站着不动（祷告）+3，燃着的驱魔图腾 8 格内翻倍，中柱第 2 阶 +15%（按十分之一点累计）",
        "scoreboard players set #r %s 10" % O,
        "execute if score @s rpg_fz_mv = @s rpg_fz_mv0 run scoreboard players set #r %s 30" % O,
        "execute if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,distance=..8,limit=1] run scoreboard players operation #r %s *= #2 %s" % (O, O),
        "execute if score @s rpg_pillar matches 3 if score @s %s matches 2.. run function %s/force/central" % (O, P),
        "execute if entity @s[tag=rpg.burnt] run scoreboard players set #r %s 0" % O,
        "scoreboard players operation @s rpg_mana_f += #r %s" % O,
        "scoreboard players operation #q %s = @s rpg_mana_f" % O,
        "scoreboard players operation #q %s /= #10 %s" % (O, O),
        "scoreboard players operation @s rpg_mana += #q %s" % O,
        "scoreboard players operation @s rpg_mana_f %%= #10 %s" % O,
    ])
    fn("force/central", ["scoreboard players operation #r %s *= #115 %s" % (O, O), "scoreboard players operation #r %s /= #100 %s" % (O, O)])
    fn("force/mana_regen", [
        "# 魔力不会自己回：每造成 2 点伤害 +1（击杀 +4 在 rpg:sephira/kill，魔化每涨 1 点 +3 在魔化结算里）",
        "scoreboard players operation #q %s = @s rpg_fz_dd" % O,
        "scoreboard players operation #q %s /= #20 %s" % (O, O),
        "execute if score @s rpg_force matches 2 run scoreboard players operation @s rpg_mana += #q %s" % O,
        "execute if score @s rpg_force matches 3 run scoreboard players operation @s rpg_mana2 += #q %s" % O,
    ])
    fn("force/vital_sec", [
        "# 生命力（as/at 圣力者）：每分钟 +1；睡一觉 +40；灵魂营火旁休息每秒 +1",
        "scoreboard players add @s rpg_fz_r 1",
        "execute if score @s rpg_fz_r matches 60.. run scoreboard players add @s rpg_vital 1",
        "execute if score @s rpg_fz_r matches 60.. run scoreboard players set @s rpg_fz_r 0",
        "execute if score @s rpg_fz_sl matches 1.. run scoreboard players add @s rpg_vital 40",
        "scoreboard players set @s rpg_fz_sl 0",
        "execute if score @s rpg_vital matches ..99 run function %s/force/campfire" % P,
        "execute if score @s rpg_vital matches 101.. run scoreboard players set @s rpg_vital 100",
        "execute if score @s rpg_vital matches ..-1 run scoreboard players set @s rpg_vital 0",
        "# 燃尽：归零时圣力和圣器保护失效，回到 30 才解除",
        "execute if score @s rpg_vital matches 0 unless entity @s[tag=rpg.burnt] run function %s/force/burn" % P,
        "execute if score @s rpg_vital matches 30.. if entity @s[tag=rpg.burnt] run function %s/force/unburn" % P,
        "# 生命力越低，最大生命扣得越多（只在档位变了时重挂）",
        "scoreboard players set #b %s 0" % O,
        "execute if score @s rpg_vital matches 41..70 run scoreboard players set #b %s 1" % O,
        "execute if score @s rpg_vital matches 11..40 run scoreboard players set #b %s 2" % O,
        "execute if score @s rpg_vital matches ..10 run scoreboard players set #b %s 3" % O,
        "execute unless score @s rpg_fz_b = #b %s run function %s/force/band" % (O, P),
        "execute if score #b %s matches 2.. if predicate %s/sprinting run effect give @s minecraft:hunger 2 0 true" % (O, P),
    ])
    camp = ["# 5×5 内有点燃的灵魂营火：每秒 +1"]
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            camp.append("execute if block ~%d ~ ~%d minecraft:soul_campfire[lit=true] run return run scoreboard players add @s rpg_vital 1" % (dx, dz))
            camp.append("execute if block ~%d ~-1 ~%d minecraft:soul_campfire[lit=true] run return run scoreboard players add @s rpg_vital 1" % (dx, dz))
    fn("force/campfire", [c.replace("~0 ", "~ ").replace("~0", "~") for c in camp])
    fn("force/band", [
        "scoreboard players operation @s rpg_fz_b = #b %s" % O,
        "attribute @s minecraft:max_health modifier remove rpg:vital",
        "execute if score #b %s matches 1 run attribute @s minecraft:max_health modifier add rpg:vital -4 add_value" % O,
        "execute if score #b %s matches 2 run attribute @s minecraft:max_health modifier add rpg:vital -8 add_value" % O,
        "execute if score #b %s matches 3 run attribute @s minecraft:max_health modifier add rpg:vital -12 add_value" % O,
    ])
    fn("force/burn", [
        "tag @s add rpg.burnt",
        "title @s times 5 40 15",
        "title @s title %s" % J(t("燃尽", C_VITAL, True)),
        "title @s subtitle %s" % J(t("生命力回到 30 之前，圣力不会回应你", C_MUTED)),
        "playsound minecraft:block.fire.extinguish player @s ~ ~ ~ 1 0.6",
    ])
    fn("force/unburn", ["tag @s remove rpg.burnt", say([t("生命力回到 30，圣力重新回应你。", C_HOLY)])])
    # 魔化结算里的钩子（rpg:taint/step，每 2 秒）
    fn("force/holy_taint", [
        "# 圣力者（as 玩家）：沾上的每一点魔化 → 1 点生命力损失 + 1 点同化；圣子、圣灵减半",
        "scoreboard players operation #d %s = @s rpg_taint" % O,
        "scoreboard players set @s rpg_taint 0",
        "execute if score @s rpg_messiah matches 1 run scoreboard players operation #d %s /= #2 %s" % (O, O),
        "scoreboard players operation @s rpg_vital -= #d %s" % O,
        "scoreboard players operation @s rpg_assim += #d %s" % O,
        "# 握着圣器：每 30 秒扣 1 点生命力（弥赛亚不扣）",
        "execute if entity @s[tag=rpg.holy] unless score @s rpg_messiah matches 1 run scoreboard players add @s rpg_fz_h 1",
        "execute if score @s rpg_fz_h matches 15.. run scoreboard players remove @s rpg_vital 1",
        "execute if score @s rpg_fz_h matches 15.. run scoreboard players set @s rpg_fz_h 0",
        "# 不在契约里：同化每 10 分钟回落 1 点",
        "execute if entity @s[tag=!rpg.pact] if score @s rpg_assim matches 1.. run scoreboard players add @s rpg_fz_t 1",
        "execute if score @s rpg_fz_t matches 300.. run scoreboard players remove @s rpg_assim 1",
        "execute if score @s rpg_fz_t matches 300.. run scoreboard players set @s rpg_fz_t 0",
        "execute if score @s rpg_vital matches ..-1 run scoreboard players set @s rpg_vital 0",
        "execute if score @s rpg_assim matches 100.. run function %s/force/fall" % P,
    ])
    fn("force/mana_taint", [
        "# 魔力者（as 玩家）：魔化每涨 1 点，魔力 +3；弥赛亚的魔化增长减半",
        "scoreboard players operation #d %s = @s rpg_taint" % O,
        "scoreboard players operation #d %s -= @s rpg_fz_tp" % O,
        "execute if score #d %s matches 1.. if score @s rpg_messiah matches 1 run function %s/force/halve" % (O, P),
        "execute if score #d %s matches 1.. run scoreboard players operation #d %s *= #3 %s" % (O, O, O),
        "execute if score #d %s matches 1.. if score @s rpg_force matches 2 run scoreboard players operation @s rpg_mana += #d %s" % (O, O),
        "execute if score #d %s matches 1.. if score @s rpg_force matches 3 run scoreboard players operation @s rpg_mana2 += #d %s" % (O, O),
        "scoreboard players operation @s rpg_fz_tp = @s rpg_taint",
    ])
    fn("force/halve", [
        "scoreboard players operation #h %s = #d %s" % (O, O),
        "scoreboard players operation #h %s /= #2 %s" % (O, O),
        "scoreboard players operation @s rpg_taint -= #h %s" % O,
        "scoreboard players operation #d %s -= #h %s" % (O, O),
    ])
    fn("force/fall", [
        "# 同化满 100：堕入魔力",
        "scoreboard players set @s rpg_force 2",
        "tag @s add rpg.fallen",
        "tag @s remove rpg.burnt",
        "scoreboard players set @s rpg_assim 100",
        "scoreboard players set @s rpg_taint 60",
        "scoreboard players set @s rpg_fz_tp 60",
        "scoreboard players set @s rpg_mana 0",
        "attribute @s minecraft:max_health modifier remove rpg:vital",
        "scoreboard players set @s rpg_fz_b 0",
        "title @s times 10 70 20",
        "title @s title %s" % J(t("堕入魔力", C_MANA, True)),
        "title @s subtitle %s" % J(t("解掉所有契约、让魔化回到 0，就能回头", C_MUTED)),
        "playsound minecraft:entity.wither.spawn player @s ~ ~ ~ 0.5 1.4",
    ])
    fn("force/rise", [
        "# 回头：重回圣力，同化清零",
        "scoreboard players set @s rpg_force 1",
        "tag @s remove rpg.fallen",
        "scoreboard players set @s rpg_assim 0",
        "scoreboard players set @s rpg_taint 0",
        "scoreboard players set @s rpg_fz_tp 0",
        "scoreboard players set @s rpg_mana 0",
        "scoreboard players set @s rpg_fz_b -1",
        "title @s times 10 70 20",
        "title @s title %s" % J(t("重回圣力", C_HOLY, True)),
        "playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.2",
    ])


# ============================================================================ 状态行
def hud():
    """力条占状态行的 e 槽（排在魔化 a 之后）。e 自带前导空格，a 为空时不带。"""
    fn("hud/e", [
        "# rpg:hud/status 调用（as 玩家）",
        "scoreboard players set @s rpg_hud_on 1",
        "data modify storage rpg:sephira h set value {lead:\"　\",a:\"\",an:0}",
        "execute if data storage rpg:hud {a:'{\"text\":\"\"}'} run data modify storage rpg:sephira h.lead set value \"\"",
    ] + bar_lines("rpg_mana", "@s rpg_mana_max", "m") + [
        "execute if score @s rpg_force matches 1 run function %s/hud/holy" % P,
        "execute if score @s rpg_force matches 2 run function %s/hud/mana" % P,
        "execute if score @s rpg_force matches 3 run function %s/hud/both" % P,
    ])
    fn("hud/holy", bar_lines("rpg_vital", "#100 %s" % O, "v") + [
        "execute store result storage rpg:sephira h.an int 1 run scoreboard players get @s rpg_assim",
        "execute if score @s rpg_assim matches 1.. run function %s/hud/holy_a with storage rpg:sephira h" % P,
        "execute unless score @s rpg_assim matches 1.. run function %s/hud/holy_m with storage rpg:sephira h" % P,
    ])
    seg_holy = '{"text":"圣力 ","color":"gray","italic":false},{"text":"$(mf)","color":"%s","italic":false},{"text":"$(me)","color":"dark_gray","italic":false}' % C_HOLY
    seg_vital = '{"text":"　生命力 ","color":"gray","italic":false},{"text":"$(vf)","color":"%s","italic":false},{"text":"$(ve)","color":"dark_gray","italic":false}' % C_VITAL
    seg_mana = '{"text":"魔力 ","color":"gray","italic":false},{"text":"$(mf)","color":"%s","italic":false},{"text":"$(me)","color":"dark_gray","italic":false}' % C_MANA
    seg_mana2 = '{"text":" 魔力 ","color":"gray","italic":false},{"text":"$(nf)","color":"%s","italic":false},{"text":"$(ne)","color":"dark_gray","italic":false}' % C_MANA
    lead = '{"text":"$(lead)","italic":false}'
    # 宏里不能直接取嵌套字段：先拍平
    flat = ["data modify storage rpg:sephira h.mf set from storage rpg:sephira h.m.f",
            "data modify storage rpg:sephira h.me set from storage rpg:sephira h.m.e"]
    fn("hud/holy_m", flat + ["function %s/hud/holy_m2 with storage rpg:sephira h" % P])
    fn("hud/holy_a", flat + ["function %s/hud/holy_a2 with storage rpg:sephira h" % P])
    vflat = ["data modify storage rpg:sephira h.vf set from storage rpg:sephira h.v.f",
             "data modify storage rpg:sephira h.ve set from storage rpg:sephira h.v.e"]
    fn("hud/holy_m2", vflat + ["function %s/hud/holy_m3 with storage rpg:sephira h" % P])
    fn("hud/holy_a2", vflat + ["function %s/hud/holy_a3 with storage rpg:sephira h" % P])
    fn("hud/holy_m3", ["$data modify storage rpg:hud e set value '[\"\",%s,%s,%s]'" % (lead, seg_holy, seg_vital)])
    fn("hud/holy_a3", ["$data modify storage rpg:hud e set value '[\"\",%s,%s,%s,{\"text\":\" 同化$(an)%%\",\"color\":\"%s\",\"italic\":false}]'"
                       % (lead, seg_holy, seg_vital, C_ASSIM)])
    fn("hud/mana", flat + ["function %s/hud/mana2 with storage rpg:sephira h" % P])
    fn("hud/mana2", ["$data modify storage rpg:hud e set value '[\"\",%s,%s]'" % (lead, seg_mana)])
    fn("hud/both", bar_lines("rpg_mana2", "@s rpg_mana_max", "n") + flat + [
        "data modify storage rpg:sephira h.nf set from storage rpg:sephira h.n.f",
        "data modify storage rpg:sephira h.ne set from storage rpg:sephira h.n.e",
        "function %s/hud/both2 with storage rpg:sephira h" % P])
    fn("hud/both2", ["$data modify storage rpg:hud e set value '[\"\",%s,%s,%s]'" % (lead, seg_holy, seg_mana2)])


# ============================================================================ 面板
def panel():
    # 面板第一行：原质 · 阶名　综合能力 x / 下一阶　阅历　装备　技能点
    lines = ["# 玩家面板第一行（as 玩家；取代原来的「驱魔等级 / 阅历 / 侵蚀」一行）",
             "scoreboard players add @s %s 0" % O, "scoreboard players add @s rpg_power 0",
             "scoreboard players add @s rpg_gear 0", "scoreboard players add @s rpg_sp 0",
             "data modify storage rpg:sephira v set value {tn:\"未入阶\",tc:\"%s\",nx:\"—\",fl:\"\"}" % C_MUTED]
    for n, key, zh, la, he, col, _pl in TIERS:
        nx = str(THR[n + 1]) if n < 10 else "已至王冠"
        lines.append("execute if score @s %s matches %d run data modify storage rpg:sephira v merge value {tn:\"%s\",tc:\"%s\",nx:\"%s\"}"
                     % (O, n, zh, col, nx))
    lines.append("execute if score @s %s matches 7 unless score @s rpg_daath matches 1 run data modify storage rpg:sephira v.nx set value \"%d（先越过达阿特）\"" % (O, THR[8]))
    for k, sc in (("tier", O), ("pw", "rpg_power"), ("xp", "rpg_ex_xp"), ("gr", "rpg_gear"), ("sp", "rpg_sp"),
                  ("mn", "rpg_mana"), ("mn2", "rpg_mana2"), ("mx", "rpg_mana_max"), ("vt", "rpg_vital"), ("as", "rpg_assim"),
                  ("tt", "rpg_taint"), ("au", "rpg_lt_auth")):
        lines.append("execute store result storage rpg:sephira v.%s int 1 run scoreboard players get @s %s" % (k, sc))
    lines += ["function %s/panel/row1 with storage rpg:sephira v" % P,
              "execute if score @s rpg_force matches 1 run function %s/panel/row_holy with storage rpg:sephira v" % P,
              "execute if score @s rpg_force matches 2 run function %s/panel/row_mana with storage rpg:sephira v" % P,
              "execute if score @s rpg_force matches 3 run function %s/panel/row_both with storage rpg:sephira v" % P,
              "execute unless score @s rpg_force matches 1.. run function %s/panel/row_none with storage rpg:sephira v" % P,
              "execute if score @s rpg_lt_divine matches 2 run function %s/panel/row_auth with storage rpg:sephira v" % P,
              "data modify storage rpg:panel ui.actions append value %s" % J(
                  {"label": t("原质", C_GOLD, True), "action": trig(20)}),
              "execute if score @s %s matches 2.. unless score @s rpg_pillar matches 1..3 run data modify storage rpg:panel ui.actions append value %s"
              % (O, J({"label": t("选择主柱", "#FF8A4A", True), "action": trig(9)})),
              "execute if score @s %s matches 5.. if score @s rpg_force matches 0 run data modify storage rpg:panel ui.actions append value %s"
              % (O, J({"label": t("觉醒", C_HOLY, True), "action": trig(19)})),
              "execute if entity @s[tag=rpg.fallen] if score @s rpg_lt_divine matches 2 run data modify storage rpg:panel ui.actions append value %s"
              % J({"label": t("凭新约回头", C_HOLY, True), "action": trig(21)})]
    fn("panel/row", lines)

    def row(parts):
        return "$data modify storage rpg:panel ui.body append value %s" % J({"text": "", "extra": parts + [t("\n")]})
    fn("panel/row1", [row([t("原质 · ", C_MUTED), {"text": "$(tn)", "color": "$(tc)", "bold": True, "italic": False},
                           t("　综合能力 ", C_MUTED), t("$(pw)", C_GOLD, True), t(" / $(nx)", "#797979")]),
                      row([t("阅历 ", C_MUTED), t("$(xp)", C_GOLD, True), t("　装备分 ", C_MUTED), t("$(gr)", C_GOLD, True),
                           t("　技能点 ", C_MUTED), t("$(sp)", "#70DB70", True)])])
    fn("panel/row_holy", [row([t("圣力 ", C_MUTED), t("$(mn)", C_HOLY, True), t("/$(mx)", "#797979"),
                               t("　生命力 ", C_MUTED), t("$(vt)", C_VITAL, True), t("/100", "#797979"),
                               t("　同化 ", C_MUTED), t("$(as)%", C_ASSIM, True)])])
    fn("panel/row_mana", [row([t("魔力 ", C_MUTED), t("$(mn)", C_MANA, True), t("/$(mx)", "#797979"),
                               t("　魔化 ", C_MUTED), t("$(tt)", C_MANA, True), t("/100", "#797979")])])
    fn("panel/row_both", [row([t("圣力 ", C_MUTED), t("$(mn)", C_HOLY, True), t("　魔力 ", C_MUTED), t("$(mn2)", C_MANA, True),
                               t("/$(mx)", "#797979"), t("　魔化 ", C_MUTED), t("$(tt)", C_MANA, True), t("/100", "#797979")])])
    fn("panel/row_none", [row([t("力 ", C_MUTED), t("尚未觉醒", "#797979"), t("　魔化 ", C_MUTED), t("$(tt)", C_MANA, True),
                               t("/100", "#797979")])])
    fn("panel/row_auth", [row([t("权柄完整度 ", "#4E9FAD"), t("$(au)", "#E8F4FF", True), t("/100", "#797979")])])

    # 「原质」页：生命之树十阶
    page = ["# 原质页（as 玩家）",
            "function %s/tier/check" % P,
            "data modify storage rpg:panel ui set value {title:{text:\"\"},body:[],actions:[]}",
            "data modify storage rpg:panel ui.title set value %s" % J(["", t("原质", C_GOLD, True), t(" Sephirot", "#8F7430")])]
    for n, key, zh, la, he, col, pl in reversed(TIERS):
        thr = THR[n]
        # 希伯来文放在行尾：夹在中间会被双向排版挪位置
        reached = {"text": "", "extra": [t("● ", col), t("%d %s" % (n, zh), col, True), t("　%d　" % thr, "#797979"),
                                          t("%s %s" % (la, he), C_MUTED), t("\n")]}
        cur = {"text": "", "extra": [t("◆ ", col, True), t("%d %s" % (n, zh), col, True), t("　%d　" % thr, C_GOLD),
                                      t("%s %s" % (la, he), C_BODY), t("　← 你在这里", C_GOLD), t("\n")]}
        todo = {"text": "", "extra": [t("○ ", "#555555"), t("%d %s" % (n, zh), "#797979"), t("　%d　" % thr, "#555555"),
                                       t("%s %s" % (la, he), "#555555"), t("\n")]}
        page += ["execute if score @s %s matches %d run data modify storage rpg:panel ui.body append value %s" % (O, n, J(cur)),
                 "execute if score @s %s matches %d.. run data modify storage rpg:panel ui.body append value %s" % (O, n + 1, J(reached)),
                 "execute unless score @s %s matches %d.. run data modify storage rpg:panel ui.body append value %s" % (O, n, J(todo))]
        if n == 8:
            dz_ok = {"text": "", "extra": [t("┄ 深渊 达阿特 Daath · דעת　已越过", "#AAB4C3"), t("\n")]}
            dz_no = {"text": "", "extra": [t("┄ 深渊 达阿特 Daath · דעת　到慈悲阶后越过", "#555555"), t("\n")]}
            page += ["execute if score @s rpg_daath matches 1 run data modify storage rpg:panel ui.body append value %s" % J(dz_ok),
                     "execute unless score @s rpg_daath matches 1 run data modify storage rpg:panel ui.body append value %s" % J(dz_no)]
    page += ["data modify storage rpg:panel ui.body append value %s" % J({"text": "", "extra": [
        t("\n综合能力 = 阅历 + 装备分（四件护甲和主手的装备等级之和 × 10）。不指定打哪个 Boss，够了就晋阶。", "#797979"), t("\n")]}),
             "function %s/panel/row" % P,
             "data modify storage rpg:panel ui.actions set value []",
             "execute if score @s %s matches 2.. unless score @s rpg_pillar matches 1..3 run data modify storage rpg:panel ui.actions append value %s"
             % (O, J({"label": t("选择主柱", "#FF8A4A", True), "action": trig(9)})),
             "data modify storage rpg:panel ui.actions append value %s" % J(
                 {"label": t("返回面板", C_GOLD, True), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set 8"}}),
             "function rpg:panel/ui/show with storage rpg:panel ui"]
    for k in (1, 2, 3):
        name, what, col = PILLAR[k]
        page.insert(-5, "execute if score @s rpg_pillar matches %d run data modify storage rpg:panel ui.body append value %s"
                    % (k, J({"text": "", "extra": [t("主柱 ", C_MUTED), t(name, col, True), t("　" + what, C_MUTED), t("\n")]})))
    fn("page/open", page)


# ============================================================================ 管理员
def admin():
    fn("admin/info", [say([t("阶 ", C_MUTED), {"score": {"name": "@s", "objective": O}}, t("　综合 ", C_MUTED),
                           {"score": {"name": "@s", "objective": "rpg_power"}}, t("　阅历 ", C_MUTED),
                           {"score": {"name": "@s", "objective": "rpg_ex_xp"}}, t("　装备 ", C_MUTED),
                           {"score": {"name": "@s", "objective": "rpg_gear"}}, t("　力 ", C_MUTED),
                           {"score": {"name": "@s", "objective": "rpg_force"}}, t("　生命力 ", C_MUTED),
                           {"score": {"name": "@s", "objective": "rpg_vital"}}, t("　同化 ", C_MUTED),
                           {"score": {"name": "@s", "objective": "rpg_assim"}}])])
    fn("admin/xp100", ["scoreboard players add @s rpg_ex_xp 100", "function %s/tier/check" % P])
    fn("admin/reset", ["# 回到未入阶（技能点、主柱、达阿特一起清）",
                       "scoreboard players reset @s %s" % O, "scoreboard players reset @s rpg_sp",
                       "scoreboard players reset @s rpg_pillar", "scoreboard players reset @s rpg_daath",
                       "scoreboard players set @s %s 0" % O, "function %s/bonus/apply" % P,
                       "scoreboard players reset @s %s" % O])


# ============================================================================ 接到别的模块上
def wire():
    hook_tag(DP, "load", P + "/load", False)
    hook_tag(DP, "tick", P + "/tick", True)
    os.makedirs(os.path.join(DP, "data", "rpg", "predicate", "sephira"), exist_ok=True)
    io.open(os.path.join(DP, "data", "rpg", "predicate", "sephira", "sprinting.json"), "w", encoding="utf-8").write(J(
        {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"flags": {"is_sprinting": True}}}))

    # 旧角色等级：不再按经验等级加血
    s = read("command/tick.mcfunction")
    s = s.replace("function rpg:level/player\n", "# 旧角色等级已并入原质（add_sephira.py）\n")
    write("command/tick.mcfunction", s)

    # 击杀 → 阅历
    patch("forge/kill/credit.mcfunction", "rpg:sephira/kill", "function rpg:sephira/kill\n")
    # 慈悲柱第 7 阶
    patch("forge/hit/hurt_player.mcfunction", "rpg:sephira/bonus/last_stand",
          "execute if score @s rpg_pillar matches 2 if score @s rpg_sef matches 7.. run function rpg:sephira/bonus/last_stand\n", "end")
    # Boss 胜利结算
    for b, zh, d, centre in BOSSES:
        rel = "%s/victory.mcfunction" % d
        if centre:
            line = "execute at @e[type=minecraft:marker,tag=%s,limit=1] run function %s/boss/%s\n" % (centre, P, b)
        else:
            line = "function %s/boss/%s\n" % (P, b)
        patch(rel, "%s/boss/%s" % (P, b), "# 原质：记打过、给阅历（add_sephira.py）\n" + line)

    # 魔化结算：圣力者折成生命力与同化；魔力者涨魔力
    patch("taint/step.mcfunction", "rpg:sephira/force/holy_taint",
          "# 原质 · 力（add_sephira.py）：圣力者沾上的魔化变成生命力损失与同化；魔力者魔化涨，魔力跟着涨\n"
          "execute if score @s rpg_force matches 1 run function rpg:sephira/force/holy_taint\n"
          "execute if score @s rpg_force matches 2..3 run function rpg:sephira/force/mana_taint\n\n", "# 分档外显")

    # 状态行：新槽 e，所有拼 actionbar 的宏都带上它
    patch("hud/status.mcfunction", "rpg:sephira/hud/e",
          "data modify storage rpg:hud e set value '{\"text\":\"\"}'\n",
          "execute unless score @s rpg_lt_divine matches 2 if entity @s[scores={rpg_holy=1..}]")
    patch("hud/status.mcfunction", "rpg:sephira/hud/e",
          "execute if score @s rpg_force matches 1.. run function rpg:sephira/hud/e\n",
          "execute if entity @s[scores={rpg_pact=1..7}] run function rpg:hud/pact\n")
    patch("hud/taint.mcfunction", "rpg_force matches 1",
          "# 圣力者的魔化那一行显示为生命力（在力条槽里，add_sephira.py）\nexecute if score @s rpg_force matches 1 run return 0\n")
    n = 0
    for root, _d, files in os.walk(os.path.join(FUNC, "hud")):
        for f in files:
            if not f.endswith(".mcfunction"):
                continue
            path = os.path.join(root, f)
            s = io.open(path, encoding="utf-8").read()
            if "$(a),$(b),$(c),$(d)" in s:
                io.open(path, "w", encoding="utf-8", newline="\n").write(s.replace("$(a),$(b),$(c),$(d)", "$(a),$(e),$(b),$(c),$(d)"))
                n += 1
    assert n >= 2, "状态行渲染宏没找到"

    # 面板：第一行换成原质
    s = read("panel/pages/panel_open.mcfunction")
    out, done = [], False
    for ln in s.split("\n"):
        if "驱魔等级 " in ln and "ui.body append" in ln:
            if not done:
                out.append("function rpg:sephira/panel/row")
                done = True
            continue
        out.append(ln.replace('"text":"驱魔师档案"', '"text":"驱魔"'))
    assert done, "面板第一行没找到"
    write("panel/pages/panel_open.mcfunction", "\n".join(out))
    patch("panel/tick.mcfunction", "rpg:sephira", "scoreboard players enable @s %s\n" % DO)
    for f in ("player.json", "player_value.json"):
        path = os.path.join(DP, "data", "rpg", "item_modifier", "command", f)
        s = io.open(path, encoding="utf-8").read()
        s = s.replace('"player_level"', '"rpg_sef"').replace("等级 ", "原质阶 ").replace("驱魔原质阶 ", "驱魔熟练 ").replace("驱魔师档案", "驱魔")
        io.open(path, "w", encoding="utf-8", newline="\n").write(s)

    # 驱魔：零碎阅历改记到 rpg_ex_dxp；裁决、驱逐才进原质
    pat = re.compile(r"(players add [^\n]*?) rpg_ex_xp ([1-9]\d*)")
    for sub in ("inquest", os.path.join("divine", "ritual"), "minion"):
        for root, _d, files in os.walk(os.path.join(FUNC, sub)):
            for f in files:
                if f.endswith(".mcfunction"):
                    path = os.path.join(root, f)
                    s = io.open(path, encoding="utf-8").read()
                    s2 = pat.sub(r"\1 rpg_ex_dxp \2", s)
                    if s2 != s:
                        io.open(path, "w", encoding="utf-8", newline="\n").write(s2)
    for f, sel in (("seal_boss", "@a[tag=rpg.rite.chooser,distance=..14]"), ("pact_boss", "@a[tag=rpg.rite.chooser,distance=..14]"),
                   ("eliminate_boss", "@a[tag=rpg.rite.chooser,distance=..14]")):
        patch("inquest/outcome/%s.mcfunction" % f, "rpg:sephira/rite", "execute as %s run function rpg:sephira/rite/verdict\n" % sel, "end")
    patch("inquest/outcome/banish.mcfunction", "rpg:sephira/rite",
          "execute as @a[tag=rpg.rite.chooser,distance=..10] run function rpg:sephira/rite/banish\n", "end")
    write("inquest/career/sync.mcfunction", "\n".join([
        "# 驱魔熟练（原驱魔等级）：退出成长体系后按裁决次数算（add_sephira.py）",
        "scoreboard players operation @s rpg_ex_prev = @s rpg_ex_lvl",
        "scoreboard players add @s rpg_ex_rites 0",
        "scoreboard players set @s rpg_ex_lvl 1",
        "execute if score @s rpg_ex_rites matches 1.. run scoreboard players set @s rpg_ex_lvl 2",
        "execute if score @s rpg_ex_rites matches 3.. run scoreboard players set @s rpg_ex_lvl 4",
        "execute if score @s rpg_ex_rites matches 6.. run scoreboard players set @s rpg_ex_lvl 5",
        "execute if score @s rpg_ex_lvl > @s rpg_ex_prev if score @s rpg_ex_prev matches 1.. run function rpg:inquest/career/level_up",
        "execute if score @s rpg_ex_lvl > @s rpg_ex_prev if score @s rpg_ex_prev matches ..0 run function rpg:inquest/career/claim",
        "scoreboard players operation @s rpg_ex_seen = @s rpg_ex_rites",
    ]) + "\n")
    s = read("inquest/player_tick.mcfunction")
    s = s.replace("execute unless score @s rpg_ex_xp = @s rpg_ex_seen run function rpg:inquest/career/sync",
                  "scoreboard players add @s rpg_ex_rites 0\nexecute unless score @s rpg_ex_rites = @s rpg_ex_seen run function rpg:inquest/career/sync")
    assert "rpg_ex_rites = @s rpg_ex_seen" in s
    write("inquest/player_tick.mcfunction", s)
    s = read("inquest/career/level_up.mcfunction")
    write("inquest/career/level_up.mcfunction", s.replace("驱 魔 师 晋 阶", "驱 魔 熟 练 提 升"))
    s = read("panel/pages/inquest_career.mcfunction")
    s = s.replace('{"text":"阶位 "', '{"text":"驱魔熟练 "').replace('{"text":"　阅历 "', '{"text":"　裁决 "').replace("$(rpg_ex_xp)", "$(rpg_ex_rites)")
    write("panel/pages/inquest_career.mcfunction", s)
    patch("inquest/career.mcfunction", "v.rpg_ex_rites",
          "scoreboard players add @s rpg_ex_rites 0\nexecute store result storage rpg:panel v.rpg_ex_rites int 1 run scoreboard players get @s rpg_ex_rites\n",
          "function rpg:panel/pages/inquest_career with storage rpg:panel v")
    s = read("inquest/career.mcfunction").replace("data modify storage rpg:panel ui set value {title:{text:\"\"},body:[],actions:[]}\n", "")
    s = s.replace("function rpg:inquest/career/sync\n", "function rpg:inquest/career/sync\ndata modify storage rpg:panel ui set value {title:{text:\"\"},body:[],actions:[]}\n", 1)
    write("inquest/career.mcfunction", s)


def retire_path():
    """旧驱魔道路（审判/守护/秘仪）整体删除：不再选择，路线加成去掉，工具按熟练全给。"""
    for root, _d, files in os.walk(os.path.join(FUNC, "inquest")):
        for f in files:
            if not f.endswith(".mcfunction"):
                continue
            path = os.path.join(root, f)
            s = io.open(path, encoding="utf-8").read()
            if "rpg_ex_path=" not in s:
                continue
            s2 = "\n".join(l for l in s.split("\n") if "rpg_ex_path=" not in l)
            io.open(path, "w", encoding="utf-8", newline="\n").write(s2)
    # 选择按钮失效
    s = read("inquest/player_tick.mcfunction")
    s = "\n".join(l for l in s.split("\n")
                  if "career/choose" not in l and "rpg_ex_path" not in l)
    write("inquest/player_tick.mcfunction", s)
    for n in (1, 2, 3):
        write("inquest/career/choose%d.mcfunction" % n, "# 驱魔道路已删除（add_sephira.py）\nreturn 0\n")
    unlock = '"text":"〖驱魔熟练〗","color":"#C9A646","bold":true,"italic":false},{"text":"  %s","color":"#9C9A94","italic":false'
    write("inquest/career/claim.mcfunction", "\n".join([
        "execute if score @s rpg_ex_lvl matches 2.. unless entity @s[tag=rpg.ex.claim2] run function rpg:inquest/career/claim2",
        "execute if score @s rpg_ex_lvl matches 3.. unless entity @s[tag=rpg.ex.claim3] run function rpg:inquest/career/claim3",
        "execute if score @s rpg_ex_lvl matches 4.. unless entity @s[tag=rpg.ex.claim4] run function rpg:inquest/career/claim4",
        "execute if score @s rpg_ex_lvl matches 5.. unless entity @s[tag=rpg.ex.claim5] run function rpg:inquest/career/claim5",
    ]) + "\n")
    write("inquest/career/claim2.mcfunction", "\n".join([
        "tag @s add rpg.ex.claim2",
        "function rpg:inquest/give/bell",
        "function rpg:inquest/give/nail",
        "function rpg:inquest/give/incense",
        'tellraw @s ["",{%s}]' % (unlock % "获得告解铃、圣钉与净罪香。"),
    ]) + "\n")
    write("inquest/career/claim3.mcfunction", "\n".join([
        "tag @s add rpg.ex.claim3",
        "function rpg:inquest/give/chalk1",
        "function rpg:inquest/give/chalk2",
        "function rpg:inquest/give/chalk3",
        'tellraw @s ["",{%s}]' % (unlock % "获得三种仪式粉笔。"),
    ]) + "\n")
    # claim5 原样保留全套工具：旧路线玩家已领过 claim2/3 的标签，靠它补齐另两条路线的工具
    for rel in ("panel/pages/inquest_career.mcfunction", "inquest/career.mcfunction"):
        s = read(rel)
        s = "\n".join(l for l in s.split("\n") if "rpg_ex_path" not in l)
        write(rel, s)
    for root, _d, files in os.walk(FUNC):
        for f in files:
            if f.endswith(".mcfunction") and "debug" not in root:
                s = io.open(os.path.join(root, f), encoding="utf-8").read()
                assert "rpg_ex_path=" not in s and not re.search(r"rpg_ex_choice set 2[123]\b", s), os.path.join(root, f)


def main():
    import shutil
    shutil.rmtree(OUT, ignore_errors=True)
    core()
    tiers()
    bonus()
    pillar()
    press()
    migrate()
    sources()
    force()
    hud()
    panel()
    admin()
    wire()
    retire_path()
    print("sephira: %d functions" % COUNT)


if __name__ == "__main__":
    main()
