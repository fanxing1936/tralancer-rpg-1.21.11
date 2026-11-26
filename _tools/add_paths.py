# -*- coding: utf-8 -*-
"""原质的二十二条路径（方案书「原质二十二路径与面板重构」，2026-11-26 用户「全部照默认」）。

规则
- 一条路径连两个原质；玩家升到较高那一端的阶，它就打开（状态 1）。
- 每条路径一场试炼。计数型试炼从打开那一刻算起（存起点 rpg_pb_<n>），不追溯。
- 走完（状态 4）：阅历 = 开它的那一阶到下一阶差额的 25%；碰到主柱上的原质再给技能点 1；
  一枚字母印记。之后在路径页选正位（2）或逆位（3），以后翻面花 1 颗洗炼钻。
- 升阶的门：综合能力够了、且连着当前阶的路径至少走完一条（状态 ≥2），才晋入下一阶。
  第 1→2 阶没有门；第 10 阶的三条路径不挡任何东西。
- 赐福全部同时生效：属性修饰符 rpg:pa_<n> 由 rpg:paths/bless/apply 重挂（挂在
  rpg:sephira/bonus/apply 末尾，晋阶、选柱、迁移时都会跑），其余接在已有的百分比钩子上。

和方案书总表的出入（无法计数或没有现成钩子的几处，见 PATHS 里的 note）也写进图鉴与方案书。

排在所有生成器之后（要往炼药、宝库、悬赏、精英、失乐园、达阿特的产物里接钩子）。
"""

import io
import json
import os
import re
import sys

import rpg_ui_style as ui
from add_sephira_tiers import TIERS

DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
RP = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else None
FUNC = os.path.join(DP, "data/rpg/function")
NS = "rpg:paths"
O = "rpg_pa"
DO = "rpg_pa_do"
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paths_ref")
GOLD, GLOSS, BODY, NAME, MUTED = ui.BROADCAST_HOLY, ui.BROADCAST_GLOSS, ui.BROADCAST_BODY, ui.BROADCAST_NAME, ui.MUTED
RITUAL = ui.RITUAL
TIER = {t[0]: t for t in TIERS}
PILLAR_TIERS = {1: (3, 6, 8), 2: (4, 7, 9), 3: (1, 2, 5, 10)}    # rpg_pillar：1 严厉 2 慈悲 3 中柱
COUNT = [0]

# (编号, 高端阶, 低端阶, 字母, 拉丁, 牌, 试炼, 目标, 正位, 逆位)
PATHS = [
    (32, 2, 1, "ת", "Tav", "世界", "走满 5000 格", 5000, "移动速度 +3%", "摔落伤害 −30%"),
    (31, 3, 1, "ש", "Shin", "审判", "完成 1 次驱魔裁决", 1, "对亡灵与恶魔 +4%", "复活后 10 秒抗性 I"),
    (30, 3, 2, "ר", "Resh", "太阳", "白天击杀 60 只怪", 60, "白天每 10 秒回 1 生命", "攻击速度 +3%"),
    (29, 4, 1, "ק", "Qoph", "月亮", "夜里击杀 5 只精英", 5, "夜里伤害 +5%", "夜里护甲 +2"),
    (28, 4, 2, "צ", "Tzaddi", "星星", "血月或血雨中击杀 20 只怪", 20, "水下呼吸更久、游得更快", "跳跃 +10%"),
    (27, 4, 3, "פ", "Peh", "塔", "打完失乐园任一河庭，或击杀 1 只首领精英", 1, "攻击伤害 +3%", "护甲韧性 +1"),
    (26, 5, 3, "ע", "Ayin", "恶魔", "立一份新的七罪契约；或魔化到 50 以上撑过 5 分钟不堕", 300, "魔化每分钟自退 1", "魔力技能消耗 −10%"),
    (25, 5, 2, "ס", "Samekh", "节制", "炼成 6 瓶药水", 6, "喝药、进食后回复 3 秒", "穿行难走的地面更快"),
    (24, 5, 4, "נ", "Nun", "死神", "击杀 150 只亡灵", 150, "击杀回 1 生命", "对亡灵 +6%"),
    (23, 6, 3, "מ", "Mem", "倒吊人", "生命低于 30% 时击杀 15 只怪", 15, "低于 30% 时抗性 I", "最大生命 +2"),
    (22, 6, 5, "ל", "Lamed", "正义", "完成 12 条悬赏", 12, "悬赏多 1 枚货币", "受近战伤时反伤 1 点"),
    (21, 7, 4, "כ", "Kaph", "命运之轮", "开 12 次宝库", 12, "宝库保底各快 1 次", "精英掉落 10% 再掉一份"),
    (20, 7, 5, "י", "Yod", "隐者", "在失乐园灰烬边境独处 15 分钟并活着出来", 900, "潜行速度 +30%", "力条上限 +10"),
    (19, 7, 6, "ט", "Teth", "力量", "不穿胸甲击杀 1 只首领精英", 1, "击退抵抗 +15%", "攻击速度 +4%"),
    (18, 8, 6, "ח", "Cheth", "战车", "疾跑累计 3000 格；或打完失乐园第三座河庭", 3000, "疾跑速度 +5%", "疾跑中出手 +15%"),
    (17, 8, 5, "ז", "Zayin", "恋人", "近战与弓弩各杀 1 只首领精英", 2, "副手有物时护甲 +2", "双持武器时伤害 +4%"),
    (16, 9, 7, "ו", "Vav", "教皇", "完成 8 次驱魔裁决", 8, "每 30 秒圣力 +3", "对下界生物 +5%"),
    (15, 9, 5, "ה", "Heh", "皇帝", "让 3 件装备升到 Lv.10", 3, "装备经验 20% 几率翻倍", "护甲 +2"),
    (14, 9, 8, "ד", "Daleth", "皇后", "冶炼、锻造或转换 30 次", 30, "幸运 +1", "最大生命 +2"),
    (13, 10, 5, "ג", "Gimel", "女祭司", "再赢一次达阿特", 1, "技能冷却 −8%", "力条上限 +20"),
    (12, 10, 8, "ב", "Beth", "魔术师", "把 4 个技能升到 3 级", 4, "力的消耗 −10%", "终式冷却 −20%"),
    (11, 10, 9, "א", "Aleph", "愚者", "只带一把武器打赢达阿特", 1, "免费翻面一次", "经验每 10 级攻击 +1%（最多 +5%）"),
]
P = {p[0]: p for p in PATHS}
# 和方案书总表不同的地方（图鉴与方案书照此改）
NOTES = {
    29: "逆位原为「夜里受到的伤害 −5%」：没有通用的受伤百分比钩子，改为夜里护甲 +2。",
    28: "试炼原为「拿到 8 种不同的遗物」，赐福原为「遗物掉率 +10% / 药水时长 +15%」：遗物没有种类计数、药水时长写死在物品里，改为血月血雨击杀与水下、跳跃。",
    26: "赐福原为「魔化积累 −10% / 魔力技能伤害 +6%」：改为魔化每分钟自退 1、魔力技能消耗 −10%。",
    25: "赐福原为「药水时长 +20% / 生命力恢复 +25%」：改为喝药进食后回复 3 秒、移动效率。",
    22: "原为「悬赏货币 +25% / 反伤 5%」：每条悬赏 3 枚，+1 枚；反伤取整为 1 点。",
    20: "正位原为「潜行时不被 16 格外的怪发现」：原版没有这种开关，改为潜行速度 +30%。",
    16: "原为「圣力恢复 +15% / 驱魔器具耗时 −20%」：改为每 30 秒圣力 +3、对下界生物 +5%。",
    14: "试炼原为「锻造或转换 30 件」，正位原为「锻造材料消耗 −10%」：计冶炼、锻造、转换的次数；正位改为幸运 +1。",
    27: "「河庭 5 层」即打完第一座河庭；打开路径前就打完过的，要另杀一只首领精英。",
    18: "「第 15 层」即打完第三座河庭；规则同上。",
}
STAT = {   # 计数型：来源分数（as 玩家，算进 #s）
    32: ["scoreboard players operation #s %s = @s rpg_pa_wk" % O, "scoreboard players operation #s %s /= #100 %s" % (O, O)],
    31: ["scoreboard players operation #s %s = @s rpg_ex_rites" % O],
    25: ["scoreboard players operation #s %s = @s rpg_alc_made" % O],
    22: ["scoreboard players operation #s %s = @s rpg_bt_total" % O],
    21: ["scoreboard players operation #s %s = @s rpg_vt_n" % O],
    18: ["scoreboard players operation #s %s = @s rpg_pa_sp" % O, "scoreboard players operation #s %s /= #100 %s" % (O, O)],
    16: ["scoreboard players operation #s %s = @s rpg_ex_rites" % O],
    14: ["scoreboard players operation #s %s = @s rpg_pa_fg" % O],
    13: ["scoreboard players operation #s %s = @s rpg_dt_win" % O],
}
OBJ_STATS = {"rpg_pa_wk": "minecraft.custom:minecraft.walk_one_cm", "rpg_pa_sp": "minecraft.custom:minecraft.sprint_one_cm",
             "rpg_pa_tsd": "minecraft.custom:minecraft.time_since_death"}
OBJ_DUMMY = ["rpg_pa", "rpg_pa_fg", "rpg_pa_ok", "rpg_pa_wt", "rpg_pa_wn", "rpg_pa_ct", "rpg_pa_ff", "rpg_pa_xl", "rpg_pa_t"]


def txt(s, c=BODY, b=False):
    return {"text": s, "color": c, "bold": b, "italic": False}


def dump(v):
    return json.dumps(ui.darken(v), ensure_ascii=False, separators=(",", ":"))


def chat(v):
    """聊天栏用亮色（不过 darken）。"""
    return json.dumps(v, ensure_ascii=False, separators=(",", ":"))


def tag_line(*parts):
    return "tellraw @s " + chat(["", txt("[路径] ", GOLD, True)] + list(parts))


def fn(rel, lines):
    p = os.path.join(FUNC, "paths", rel.replace("/", os.sep) + ".mcfunction")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as h:
        h.write("\n".join(lines).rstrip("\n") + "\n")
    COUNT[0] += 1


def jw(rel, doc):
    p = os.path.join(DP, "data", rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as h:
        json.dump(doc, h, ensure_ascii=False, indent=2)


def func_path(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep) + ".mcfunction")


def read(rel):
    return io.open(func_path(rel), encoding="utf-8").read()


def write(rel, s):
    with io.open(func_path(rel), "w", encoding="utf-8", newline="\n") as h:
        h.write(s)


def append(rel, lines, mark):
    s = read(rel)
    if mark in s:
        return
    write(rel, s.rstrip("\n") + "\n" + "\n".join(lines) + "\n")


def prepend(rel, lines, mark):
    s = read(rel)
    if mark in s:
        return
    write(rel, "\n".join(lines) + "\n" + s)


def hook_tag(name, entry):
    p = os.path.join(DP, "data/minecraft/tags/function", name + ".json")
    doc = json.load(io.open(p, encoding="utf-8"))
    if entry not in doc["values"]:
        doc["values"].append(entry)
    jw("minecraft/tags/function/%s.json" % name, doc)


def ps(n):
    return "rpg_ps_%d" % n


def pa(n):
    return "rpg_pa_%d" % n


def pb(n):
    return "rpg_pb_%d" % n


def tier_thresholds():
    """从 rpg:sephira/tier/check 读晋阶门槛（与 add_sephira 同步）。"""
    s = read("sephira/tier/check")
    thr = {1: 0}
    for t, x in re.findall(r"rpg_sef matches (\d+) (?:if score @s rpg_ps_\d+ matches 2\.\. )?(?:if score @s rpg_daath matches 1 )?if score @s rpg_power matches (\d+)\.\.", s):
        thr[int(t) + 1] = int(x)
    assert sorted(thr) == list(range(1, 11)), thr
    return thr


THR = {}


def step_xp(t):
    t = min(t, 9)
    return (THR[t + 1] - THR[t]) // 4


def pname(n):
    return "第 %d 路径「%s」" % (n, P[n][5])


def colour(n):
    """路径的颜色：两端原质色的中间。"""
    _, hi, lo = P[n][:3]
    return ui.mix(TIER[hi][5], TIER[lo][5], 0.5)


def seal_item(n):
    _, hi, lo, letter, latin, card = P[n][:6]
    return ("minecraft:paper[minecraft:item_model=\"rpg:paths/seal_%d\",minecraft:custom_name=%s,minecraft:lore=[%s,%s,%s],"
            "minecraft:custom_data={rpg_seal:%d},minecraft:max_stack_size=1]") % (
        n, chat(["", txt("[路径]", RITUAL, True), txt("%s · %s %s" % (card, latin, letter), ui.WHITE)]),
        chat(txt("第 %d 路径　%s — %s" % (n, TIER[hi][2], TIER[lo][2]), BODY)),
        chat(txt("走完这条路径的凭证", MUTED)), chat(txt("正位：%s　逆位：%s" % (P[n][8], P[n][9]), MUTED)), n)


# ---- 打开、计数、走完 ---------------------------------------------------------

def build_core():
    load = ["scoreboard objectives add %s trigger" % DO]
    load += ["scoreboard objectives add %s %s" % (k, v) for k, v in OBJ_STATS.items()]
    load += ["scoreboard objectives add %s dummy" % k for k in OBJ_DUMMY]
    for n in P:
        load += ["scoreboard objectives add %s dummy" % x for x in (ps(n), pa(n), pb(n))]
    load += ["scoreboard players set #%d %s %d" % (k, O, k) for k in (2, 8, 9, 10, 92, 100)]
    fn("load", load)
    hook_tag("load", NS + "/load")
    hook_tag("tick", NS + "/tick")

    # 打开
    for n, hi, lo, *_ in PATHS:
        L = ["# 打开%s（as 玩家）" % pname(n), "scoreboard players set @s %s 1" % ps(n), "scoreboard players set @s %s 0" % pa(n),
             "scoreboard players add #new %s 1" % O]
        if n in STAT:
            L += STAT[n] + ["scoreboard players operation @s %s = #s %s" % (pb(n), O)]
        if n in (27, 18):
            L += ["scoreboard players operation @s %s = @s rpg_pl_best" % pb(n)]
        if n == 26:
            L += ["scoreboard players operation @s %s = @s rpg_pact" % pb(n)]
        fn("open/%d" % n, L)

    # 更新进度（只算，不发奖）
    U = ["# 计数型与状态型试炼的进度（as 玩家）"]
    for n in STAT:
        sub = STAT[n] + ["scoreboard players operation @s %s = #s %s" % (pa(n), O), "scoreboard players operation @s %s -= @s %s" % (pa(n), pb(n))]
        fn("upd/%d" % n, sub)
        U.append("execute if score @s %s matches 1 run function %s/upd/%d" % (ps(n), NS, n))
    # 15：Lv.10 装备件数（状态，不计起点）
    fn("upd/15", ["execute store result score @s %s run clear @s *[minecraft:custom_data~{rpg_eq:{lv:10}}] 0" % pa(15)])
    U.append("execute if score @s %s matches 1 run function %s/upd/15" % (ps(15), NS))
    # 12：3 级技能个数
    fn("upd/12", ["scoreboard players set @s %s 0" % pa(12)] +
       ["execute if score @s rpg_k%02d matches 3.. run scoreboard players add @s %s 1" % (k, pa(12)) for k in range(1, 25)])
    U.append("execute if score @s %s matches 1 run function %s/upd/12" % (ps(12), NS))
    # 26：立了新契约就算走完
    U.append("execute if score @s %s matches 1 if score @s rpg_pact matches 1.. unless score @s rpg_pact = @s %s run scoreboard players set @s %s 300" % (ps(26), pb(26), pa(26)))
    # 27、18：打开以后才打完的河庭
    U.append("execute if score @s %s matches 1 if score @s %s matches ..4 if score @s rpg_pl_best matches 5.. run scoreboard players set @s %s 1" % (ps(27), pb(27), pa(27)))
    U.append("execute if score @s %s matches 1 if score @s %s matches ..14 if score @s rpg_pl_best matches 15.. run scoreboard players set @s %s 3000" % (ps(18), pb(18), pa(18)))
    fn("update", U)

    # 走完
    for n, hi, lo, letter, latin, card, trial, goal, up, down in PATHS:
        xp = step_xp(hi)
        L = ["# 走完%s" % pname(n), "scoreboard players set @s %s 4" % ps(n),
             "scoreboard players add @s rpg_ex_xp %d" % xp, "give @s " + seal_item(n)]
        sp_pillars = [k for k, ts in PILLAR_TIERS.items() if hi in ts or lo in ts]
        for k in sp_pillars:
            L.append("execute if score @s rpg_pillar matches %d run scoreboard players add @s rpg_sp 1" % k)
        L += ["title @s times 10 50 20",
              "title @s subtitle " + chat(txt("%s · %s %s　—　%s 与 %s" % (card, latin, letter, TIER[hi][2], TIER[lo][2]), colour(n))),
              "title @s title " + chat(["", txt("路径 · ", BODY), txt(card, colour(n), True)]),
              "playsound minecraft:block.end_portal_frame.fill master @s ~ ~ ~ 0.8 0.8",
              "playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.6 1.3",
              "particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.04 30",
              tag_line(txt("走完了"), txt(pname(n), colour(n), True), txt("　阅历 +%d" % xp, BODY))]
        for k in sp_pillars:
            L.append("execute if score @s rpg_pillar matches %d run " % k + tag_line(txt("路径碰到你的主柱：技能点 +1", BODY)))
        L.append(tag_line(txt("翻开这张牌，选正位或逆位：", BODY),
                          {"text": "[择位]", "color": GOLD, "bold": True, "italic": False,
                           "click_event": {"action": "run_command", "command": "/trigger %s set %d" % (DO, n)},
                           "hover_event": {"action": "show_text", "value": txt("正位：%s\n逆位：%s" % (up, down), NAME)}}))
        fn("done/%d" % n, L)

    # 每两秒（接在原质晋阶检查前）
    C = ["# 打开新路径、更新进度、发走完的奖（as 玩家；在 rpg:sephira/tier/check 里）", "scoreboard players set #new %s 0" % O]
    for n, hi, *_ in PATHS:
        C.append("execute if score @s rpg_sef matches %d.. unless score @s %s matches 1.. run function %s/open/%d" % (hi, ps(n), NS, n))
    C += ["execute if score #new %s matches 1.. run function %s/say_new" % (O, NS), "function %s/update" % NS]
    for n, *_r in PATHS:
        out = " unless entity @s[tag=rpg.pl.in]" if n == 20 else ""      # 隐者：要活着走出失乐园
        C.append("execute if score @s %s matches 1 if score @s %s matches %d..%s run function %s/done/%d" % (ps(n), pa(n), P[n][7], out, NS, n))
    fn("check", C)
    fn("say_new", ["execute store result storage rpg:paths v.n int 1 run scoreboard players get #new %s" % O, "function %s/say_new_m with storage rpg:paths v" % NS])
    fn("say_new_m", ["$" + tag_line(txt("新开了 "), txt("$(n)", GOLD, True), txt(" 条路径。"),
                                    {"text": "[看路径]", "color": GOLD, "bold": True, "italic": False,
                                     "click_event": {"action": "run_command", "command": "/trigger %s set 1" % DO}})])
    fn("wait", ["scoreboard players operation @s rpg_pa_wt = @s rpg_sef",
                tag_line(txt("综合能力已经够晋入下一阶，"), txt("先走完一条连着这一阶的路径", GOLD, True), txt("。"),
                         {"text": "[看路径]", "color": GOLD, "bold": True, "italic": False,
                          "click_event": {"action": "run_command", "command": "/trigger %s set 1" % DO}})])


def build_gate():
    """改 rpg:sephira/tier/check：第 2..9 阶升下一阶要多一条「连着这一阶的路径走完」。"""
    s = read("sephira/tier/check")
    if NS + "/check" in s:
        return
    by_tier = {}
    for n, hi, *_ in PATHS:
        by_tier.setdefault(hi, []).append(n)
    out = []
    for line in s.rstrip("\n").split("\n"):
        if line.startswith("execute unless score @s rpg_sef matches 1.. run function rpg:sephira/tier/up_1"):
            out.append("function %s/check" % NS)
        m = re.match(r"^execute if score @s rpg_sef matches (\d+) (.*run function rpg:sephira/tier/up_\d+)$", line)
        if m and int(m.group(1)) >= 2:
            t = int(m.group(1))
            for n in by_tier[t]:
                out.append("execute if score @s rpg_sef matches %d if score @s %s matches 2.. %s" % (t, ps(n), m.group(2)))
            continue
        out.append(line)
    for t in range(2, 10):
        extra = "if score @s rpg_daath matches 1 " if t == 7 else ""
        out.append("execute if score @s rpg_sef matches %d %sif score @s rpg_power matches %d.. unless score @s rpg_pa_wt matches %d run function %s/wait"
                   % (t, extra, THR[t + 1], t, NS))
    write("sephira/tier/check", "\n".join(out) + "\n")


# ---- 击杀与各处钩子 -----------------------------------------------------------

def build_hooks():
    # 每次击杀（as 击杀者，rpg_fg_kx：1 普通 5 精英 50 Boss）
    K = ["# 路径试炼与赐福的击杀钩子（as 击杀者；rpg:sephira/kill 末尾）",
         "execute if score @s %s matches 1 if predicate %s/day run scoreboard players add @s %s 1" % (ps(30), NS, pa(30)),
         "execute if score @s %s matches 1 if score @s rpg_fg_kx matches 5.. unless predicate %s/day run scoreboard players add @s %s 1" % (ps(29), NS, pa(29)),
         "execute if score @s %s matches 1 if entity @s[tag=rpg.pl.in] if score #moon rpg_pl matches 1.. run scoreboard players add @s %s 1" % (ps(28), pa(28)),
         "execute if score @s %s matches 1 if entity @s[tag=rpg.pl.in] unless score #moon rpg_pl matches 1.. if score #rain rpg_pl matches 1.. run scoreboard players add @s %s 1" % (ps(28), pa(28)),
         "execute if score @s %s matches 1 run function %s/low" % (ps(23), NS),
         "execute if score @s %s matches 2 run effect give @s minecraft:regeneration 2 1 true" % ps(24)]
    fn("kill", K)
    fn("low", ["execute store result score #h %s run data get entity @s Health 10" % O,
               "execute store result score #m %s run attribute @s minecraft:max_health get 3" % O,
               "execute if score #h %s < #m %s run scoreboard players add @s %s 1" % (O, O, pa(23))])
    append("sephira/kill", ["function %s/kill" % NS], NS + "/kill")
    # 亡灵
    jw("rpg/advancement/paths/kill_undead.json", {
        "criteria": {"k": {"trigger": "minecraft:player_killed_entity", "conditions": {
            "entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": "#minecraft:undead"}}]}}},
        "rewards": {"function": NS + "/undead"}})
    fn("undead", ["advancement revoke @s only rpg:paths/kill_undead",
                  "execute if score @s %s matches 1 run scoreboard players add @s %s 1" % (ps(24), pa(24))])
    # 首领精英
    fn("champ", ["# 杀了首领精英（as 玩家；接在 rpg:elite/kill/*_champion）",
                 "execute if score @s %s matches 1 run scoreboard players set @s %s 1" % (ps(27), pa(27)),
                 "execute if score @s %s matches 1 unless items entity @s armor.chest * run scoreboard players set @s %s 1" % (ps(19), pa(19)),
                 "execute if score @s %s matches 1 run function %s/champ17" % (ps(17), NS)])
    fn("champ17", ["# 近战记 1、弓弩记 2（rpg_pb_17 是位）",
                   "scoreboard players set #r %s 0" % O,
                   "execute if items entity @s weapon.mainhand minecraft:bow run scoreboard players set #r %s 1" % O,
                   "execute if items entity @s weapon.mainhand minecraft:crossbow run scoreboard players set #r %s 1" % O,
                   "execute if score #r %s matches 1 unless score @s %s matches 2.. run scoreboard players add @s %s 2" % (O, pb(17), pb(17)),
                   "execute if score #r %s matches 0 if items entity @s weapon.mainhand #rpg:daath/weapon run function %s/champ17m" % (O, NS),
                   "scoreboard players set @s %s 0" % pa(17),
                   "execute if score @s %s matches 1 run scoreboard players set @s %s 1" % (pb(17), pa(17)),
                   "execute if score @s %s matches 2 run scoreboard players set @s %s 1" % (pb(17), pa(17)),
                   "execute if score @s %s matches 3 run scoreboard players set @s %s 2" % (pb(17), pa(17))])
    fn("champ17m", ["scoreboard players operation #b %s = @s %s" % (O, pb(17)), "scoreboard players operation #b %s %%= #2 %s" % (O, O),
                    "execute if score #b %s matches 0 run scoreboard players add @s %s 1" % (O, pb(17))])
    elite_dir = os.path.join(FUNC, "elite/kill")
    n_elite = 0
    for f in sorted(os.listdir(elite_dir)):
        rel = "elite/kill/" + f[:-len(".mcfunction")]
        if f.endswith("_champion.mcfunction"):
            append(rel, ["function %s/champ" % NS], NS + "/champ")
        # 命运之轮逆位：10% 再掉一份精英掉落
        src = read(rel)
        m = re.search(r"^loot give @s loot (rpg:elite/\S+)$", src, re.M)
        assert m, rel
        append(rel, ["execute if score @s %s matches 3 if predicate {condition:\"minecraft:random_chance\",chance:0.1} run loot give @s loot %s" % (ps(21), m.group(1))],
               "%s matches 3 if predicate" % ps(21))
        n_elite += 1
    assert n_elite >= 14, n_elite
    # 失乐园河庭
    for k in (1, 2, 3, 4):
        rel = "pl/court/%d/done" % k
        if os.path.exists(func_path(rel)):
            append(rel, ["execute as @a[distance=..32,gamemode=!spectator] run function %s/court%s" % (NS, "_hi" if k >= 3 else "")], NS + "/court")
    fn("court", ["execute if score @s %s matches 1 run scoreboard players set @s %s 1" % (ps(27), pa(27))])
    fn("court_hi", ["function %s/court" % NS, "execute if score @s %s matches 1 run scoreboard players set @s %s 3000" % (ps(18), pa(18))])
    # 锻造计数
    for rel in ["quest/hook/smelt", "quest/hook/conv"] + ["forge/bp/" + f[:-11] for f in sorted(os.listdir(os.path.join(FUNC, "forge/bp"))) if f.startswith("make_")]:
        append(rel, ["scoreboard players add @s rpg_pa_fg 1"], "rpg_pa_fg")
    # 达阿特：开打时记武器件数，赢了看是不是只有一把
    s = read("daath_fight/pl/arrive")
    if "rpg_pa_wn" not in s:
        write("daath_fight/pl/arrive", "execute if score @s rpg_dt_pt matches 40 store result score @s rpg_pa_wn run clear @s #rpg:daath/weapon 0\n" + s)
    append("daath_fight/pl/won", ["execute if score @s %s matches 1 if score @s rpg_pa_wn matches 1 run scoreboard players set @s %s 1" % (ps(11), pa(11))], ps(11))
    # 悬赏、宝库、装备经验
    append("events/bt/reward", ["execute if score @s %s matches 2 run loot give @s loot rpg:world/currency" % ps(22)], ps(22))
    s = read("vault/roll")
    a = "scoreboard players add @a[tag=rpg.vt.op] rpg_vt_l 1\n"
    assert s.count(a) == 1
    if ps(21) not in s:
        s = s.replace(a, a + "scoreboard players add @a[tag=rpg.vt.op,scores={%s=2}] rpg_vt_e 1\nscoreboard players add @a[tag=rpg.vt.op,scores={%s=2}] rpg_vt_l 1\n" % (ps(21), ps(21)))
        write("vault/roll", s)
    s = read("forge/kill/credit")
    a = "scoreboard players operation #xa rpg_fg = @s rpg_fg_kx\n"
    assert s.count(a) == 1
    if ps(15) not in s:
        write("forge/kill/credit", s.replace(a, a + "execute if score @s %s matches 2 if predicate {condition:\"minecraft:random_chance\",chance:0.2} run scoreboard players operation #xa rpg_fg += #xa rpg_fg\n" % ps(15)))
    # 近战百分比（as 受击者，攻击者 rpg.fg.atk）
    A = "@a[tag=rpg.fg.atk,scores={%s=%d}]"
    M = ["# 路径赐福（add_paths.py）",
         "execute if entity %s if entity @s[type=#minecraft:undead] run scoreboard players add #pct rpg_fg 4" % (A % (ps(31), 2)),
         "execute if entity %s if entity @s[type=#rpg:wl_nether] run scoreboard players add #pct rpg_fg 4" % (A % (ps(31), 2)),
         "execute if entity %s unless predicate %s/day run scoreboard players add #pct rpg_fg 5" % (A % (ps(29), 2), NS),
         "execute if entity %s if entity @s[type=#minecraft:undead] run scoreboard players add #pct rpg_fg 6" % (A % (ps(24), 3)),
         "execute if entity @a[tag=rpg.fg.atk,scores={%s=3},predicate=%s/sprinting] run scoreboard players add #pct rpg_fg 15" % (ps(18), NS),
         "execute if entity %s if items entity @a[tag=rpg.fg.atk,limit=1] weapon.offhand #rpg:daath/weapon run scoreboard players add #pct rpg_fg 4" % (A % (ps(17), 3)),
         "execute if entity %s if entity @s[type=#rpg:wl_nether] run scoreboard players add #pct rpg_fg 5" % (A % (ps(16), 3))]
    append("forge/hit/melee", M, "路径赐福（add_paths.py）")
    # 力：冷却与消耗
    prepend("force/pay/cd", ["# 路径赐福（add_paths.py）",
                             "execute if score @s %s matches 2 run scoreboard players operation #c rpg_fo *= #92 %s" % (ps(13), O),
                             "execute if score @s %s matches 2 run scoreboard players operation #c rpg_fo /= #100 %s" % (ps(13), O)], "路径赐福（add_paths.py）")
    # 魔术师逆位：终式（技能 25 圣力、26 魔力与七罪领主终式）冷却 −20%
    for k in (25, 26):
        s = read("force/sk/%d/try" % k)
        a = "function rpg:force/pay/cd\n"
        assert s.count(a) == 1, k
        if ps(12) not in s:
            write("force/sk/%d/try" % k, s.replace(a, a + "execute if score @s %s matches 3 run scoreboard players operation #c rpg_fo *= #8 %s\n"
                                                    "execute if score @s %s matches 3 run scoreboard players operation #c rpg_fo /= #10 %s\n" % (ps(12), O, ps(12), O)))
    for rel, extra in (("force/pay/h", []), ("force/pay/m", [26])):
        L = ["# 路径赐福（add_paths.py）"]
        for n, st in [(12, 2)] + [(k, 3) for k in extra]:
            L += ["execute if score @s %s matches %d run scoreboard players operation #fc rpg_fo *= #9 %s" % (ps(n), st, O),
                  "execute if score @s %s matches %d run scoreboard players operation #fc rpg_fo /= #10 %s" % (ps(n), st, O)]
        prepend(rel, L, "路径赐福（add_paths.py）")
    # 反伤、喝药
    jw("rpg/advancement/paths/hurt.json", {"criteria": {"h": {"trigger": "minecraft:entity_hurt_player"}}, "rewards": {"function": NS + "/hurt"}})
    fn("hurt", ["advancement revoke @s only rpg:paths/hurt",
                "execute unless score @s %s matches 3 run return 0" % ps(22),
                "tag @s add rpg.pa.me",
                "execute on attacker if entity @s[distance=..5] run damage @s 1 minecraft:thorns by @p[tag=rpg.pa.me]",
                "tag @s remove rpg.pa.me"])
    jw("rpg/advancement/paths/consume.json", {"criteria": {"c": {"trigger": "minecraft:consume_item"}}, "rewards": {"function": NS + "/consume"}})
    fn("consume", ["advancement revoke @s only rpg:paths/consume",
                   "execute if score @s %s matches 2 run effect give @s minecraft:regeneration 3 0 true" % ps(25)])
    # 判定
    jw("rpg/predicate/paths/day.json", {"condition": "minecraft:time_check", "value": {"min": 0, "max": 12999}, "period": 24000})
    jw("rpg/predicate/paths/sprinting.json", {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"flags": {"is_sprinting": True}}})


# ---- 赐福 ---------------------------------------------------------------------

MODS = [  # (路径, 状态, 属性, 值, 方式, 后缀)
    (32, 2, "movement_speed", 0.03, "add_multiplied_base", ""),
    (32, 3, "fall_damage_multiplier", -0.3, "add_multiplied_base", ""),
    (30, 3, "attack_speed", 0.03, "add_multiplied_base", ""),
    (28, 2, "oxygen_bonus", 1, "add_value", ""),
    (28, 2, "water_movement_efficiency", 0.2, "add_value", ""),
    (28, 3, "jump_strength", 0.1, "add_multiplied_base", ""),
    (27, 2, "attack_damage", 0.03, "add_multiplied_base", ""),
    (27, 3, "armor_toughness", 1, "add_value", ""),
    (25, 3, "movement_efficiency", 0.3, "add_value", ""),
    (23, 3, "max_health", 2, "add_value", ""),
    (20, 2, "sneaking_speed", 0.09, "add_value", ""),
    (19, 2, "knockback_resistance", 0.15, "add_value", ""),
    (19, 3, "attack_speed", 0.04, "add_multiplied_base", ""),
    (15, 3, "armor", 2, "add_value", ""),
    (14, 2, "luck", 1, "add_value", ""),
    (14, 3, "max_health", 2, "add_value", ""),
]
TOGGLES = [(29, "armor", "n"), (18, "movement_speed", "s"), (17, "armor", "o"), (11, "attack_damage", "x")]
MANA = [(20, 3, 10), (13, 3, 20)]


def build_bless():
    seen = set()
    L = ["# 重挂路径赐福（as 玩家；rpg:sephira/bonus/apply 末尾，走完、翻面后也调）"]
    for n, _, attr, *_r in MODS:
        if (n, attr) not in seen:
            seen.add((n, attr))
            L.append("attribute @s minecraft:%s modifier remove rpg:pa_%d" % (attr, n))
    for n, attr, suf in TOGGLES:
        L.append("attribute @s minecraft:%s modifier remove rpg:pa_%d%s" % (attr, n, suf))
    L.append("scoreboard players set @s rpg_pa_xl -1")
    for n, st, attr, val, op, _ in MODS:
        L.append("execute if score @s %s matches %d run attribute @s minecraft:%s modifier add rpg:pa_%d %s %s" % (ps(n), st, attr, n, val, op))
    for n, st, v in MANA:
        L.append("execute if score @s %s matches %d run scoreboard players add @s rpg_mana_max %d" % (ps(n), st, v))
    # 有走完的路径就挂上每秒的赐福
    L += ["tag @s remove rpg.pa.any"] + ["execute if score @s %s matches 2..3 run tag @s add rpg.pa.any" % ps(n) for n in P]
    fn("bless/apply", L)
    append("sephira/bonus/apply", ["function %s/bless/apply" % NS], NS + "/bless/apply")

    S = ["# 每秒（as/at 玩家）：开关式与定时的赐福",
         "scoreboard players add @s rpg_pa_t 1",
         "execute if score @s rpg_pa_t matches 60.. run scoreboard players set @s rpg_pa_t 0",
         # 30 正：白天每 10 秒回 1
         "scoreboard players operation #q %s = @s rpg_pa_t" % O, "scoreboard players operation #q %s %%= #10 %s" % (O, O),
         "execute if score @s %s matches 2 if score #q %s matches 0 if predicate %s/day run effect give @s minecraft:regeneration 2 1 true" % (ps(30), O, NS),
         # 31 逆：复活后 10 秒抗性 I
         "execute if score @s %s matches 3 if score @s rpg_pa_tsd matches ..40 unless entity @s[tag=rpg.pa.rs] run effect give @s minecraft:resistance 10 0 true" % ps(31),
         "execute if score @s %s matches 3 if score @s rpg_pa_tsd matches ..40 run tag @s add rpg.pa.rs" % ps(31),
         "execute if score @s rpg_pa_tsd matches 41.. run tag @s remove rpg.pa.rs",
         # 29 逆：夜里护甲 +2
         "execute if score @s %s matches 3 unless predicate %s/day run attribute @s minecraft:armor modifier add rpg:pa_29n 2 add_value" % (ps(29), NS),
         "execute if score @s %s matches 3 if predicate %s/day run attribute @s minecraft:armor modifier remove rpg:pa_29n" % (ps(29), NS),
         # 26 正：魔化每分钟退 1
         "execute if score @s %s matches 2 if score @s rpg_pa_t matches 0 if score @s rpg_taint matches 1.. run scoreboard players remove @s rpg_taint 1" % ps(26),
         # 23 正：低于 30% 抗性 I
         "execute if score @s %s matches 2 run function %s/low_res" % (ps(23), NS),
         # 17 正：副手有物护甲 +2
         "execute if score @s %s matches 2 if items entity @s weapon.offhand * run attribute @s minecraft:armor modifier add rpg:pa_17o 2 add_value" % ps(17),
         "execute if score @s %s matches 2 unless items entity @s weapon.offhand * run attribute @s minecraft:armor modifier remove rpg:pa_17o" % ps(17),
         # 16 正：每 30 秒圣力 +3
         "scoreboard players operation #q %s = @s rpg_pa_t" % O, "scoreboard players operation #q %s %%= #30 %s" % (O, O),
         "execute if score @s %s matches 2 if score #q %s matches 0 if score @s rpg_force matches 1 run function %s/holy" % (ps(16), O, NS),
         "execute if score @s %s matches 2 if score #q %s matches 0 if score @s rpg_force matches 3 run function %s/holy" % (ps(16), O, NS),
         # 11 逆：经验等级
         "execute if score @s %s matches 3 run function %s/xl" % (ps(11), NS)]
    fn("bless/sec", S)
    fn("low_res", ["execute store result score #h %s run data get entity @s Health 10" % O,
                   "execute store result score #m %s run attribute @s minecraft:max_health get 3" % O,
                   "execute if score #h %s < #m %s run effect give @s minecraft:resistance 2 0 true" % (O, O)])
    fn("holy", ["scoreboard players add @s rpg_mana 3", "execute if score @s rpg_mana > @s rpg_mana_max run scoreboard players operation @s rpg_mana = @s rpg_mana_max"])
    fn("xl", ["execute store result score #l %s run experience query @s levels" % O, "scoreboard players operation #l %s /= #10 %s" % (O, O),
              "execute if score #l %s matches 6.. run scoreboard players set #l %s 5" % (O, O),
              "execute if score #l %s = @s rpg_pa_xl run return 0" % O,
              "scoreboard players operation @s rpg_pa_xl = #l %s" % O,
              "attribute @s minecraft:attack_damage modifier remove rpg:pa_11x",
              "execute store result storage rpg:paths x.v float 0.01 run scoreboard players get #l %s" % O,
              "function %s/xl_m with storage rpg:paths x" % NS])
    fn("xl_m", ["$attribute @s minecraft:attack_damage modifier add rpg:pa_11x $(v) add_multiplied_base"])

    T = ["# 每刻：路径按钮；战车正位的疾跑加速；放技能后的窗口",
         "execute as @a[scores={%s=1..}] at @s run function %s/press" % (DO, NS),
         "execute as @a[scores={%s=2},predicate=%s/sprinting] run attribute @s minecraft:movement_speed modifier add rpg:pa_18s 0.05 add_multiplied_base" % (ps(18), NS),
         "execute as @a[scores={%s=2},predicate=!%s/sprinting] run attribute @s minecraft:movement_speed modifier remove rpg:pa_18s" % (ps(18), NS)]
    fn("tick", T)
    # 每秒（挂在 rpg:sephira/sec）
    fn("sec", ["scoreboard players enable @s %s" % DO,
               "execute if score @s rpg_pa_ct matches 1.. run scoreboard players remove @s rpg_pa_ct 1",
               "execute if entity @s[tag=rpg.pa.any] run function %s/bless/sec" % NS,
               "execute if score @s %s matches 1 run function %s/hermit" % (ps(20), NS),
               "execute if score @s %s matches 1 if score #m2 rpg_sef matches 0 run function %s/taint" % (ps(26), NS)])
    s = read("sephira/sec")
    if NS + "/sec" not in s:
        write("sephira/sec", s.rstrip("\n") + "\nfunction %s/sec\n" % NS)
    load_const = ["scoreboard players set #30 %s 30" % O]
    s = read("paths/load")
    write("paths/load", s + "\n".join(load_const) + "\n")
    # 20：灰烬边境独处；死了重来
    fn("hermit", ["execute if score @s rpg_pa_tsd matches ..40 if score @s %s matches 1..899 run function %s/hermit_dead" % (pa(20), NS),
                  "execute if score @s %s matches 900.. run return 0" % pa(20),
                  "execute unless entity @s[tag=rpg.pl.in] run return 0",
                  "execute if entity @a[distance=0.1..48,gamemode=!spectator] run return 0",
                  "execute in rpg:paradise_lost positioned 0 83 0 if entity @s[distance=561..] run scoreboard players add @s %s 1" % pa(20),
                  "execute if score @s %s matches 900 run " % pa(20) + tag_line(txt("隐者的十五分钟够了，"), txt("活着走出失乐园", GOLD, True), txt("就算走完。"))])
    fn("hermit_dead", ["scoreboard players set @s %s 0" % pa(20), tag_line(txt("死在了失乐园，隐者的路要从头走。", ui.WARN))])
    # 26：魔化 ≥ 50 撑够 5 分钟（每两秒 +2），堕了重来
    fn("taint", ["execute if entity @s[tag=rpg.fallen] run return run scoreboard players set @s %s 0" % pa(26),
                 "execute if score @s rpg_taint matches 50.. run scoreboard players add @s %s 2" % pa(26)])


# ---- 页面与选择 ---------------------------------------------------------------

def bar_text(key):
    return {"text": "$(%s)" % key, "font": "rpg:pbar", "color": "#FFFFFE", "italic": False, "bold": False}


def build_pages():
    # 按钮：1 路径页；11..32 某条路径；100+n 问正位，200+n 问逆位；300+n 定正位，400+n 定逆位
    L = ["# 路径按钮（as/at 玩家）", "scoreboard players operation #do %s = @s %s" % (O, DO), "scoreboard players set @s %s 0" % DO,
         "scoreboard players enable @s %s" % DO,
         "execute if score #do %s matches 1 run return run function %s/page/list" % (O, NS)]
    for n in P:
        L.append("execute if score #do %s matches %d run return run function %s/page/%d" % (O, n, NS, n))
        for base, what in ((100, "ask_up"), (200, "ask_down"), (300, "set_up"), (400, "set_down")):
            L.append("execute if score #do %s matches %d run return run function %s/%s/%d" % (O, base + n, NS, what, n))
    fn("press", L)

    # 列表页
    hdr = ["# 路径页（as 玩家）", "function %s/update" % NS,
           "data modify storage rpg:panel ui set value {title:{text:\"\"},body:[],actions:[],tab:2,bw:420}",
           "data modify storage rpg:panel ui.title set value " + dump(["", txt("路径", GOLD, True), txt(" " + ui.fraktur("Paths"), GLOSS)])]
    for n in P:
        hdr += ["scoreboard players operation #i %s = @s %s" % (O, pa(n)), "scoreboard players operation #i %s *= #9 %s" % (O, O),
                "scoreboard players set #g %s %d" % (O, P[n][7]), "scoreboard players operation #i %s /= #g %s" % (O, O),
                "execute if score #i %s matches 10.. run scoreboard players set #i %s 9" % (O, O),
                "execute store result storage rpg:paths v.b%d int 1 run scoreboard players get #i %s" % (n, O),
                "execute store result storage rpg:paths v.p%d int 1 run scoreboard players get @s %s" % (n, pa(n))]
    hdr += ["scoreboard players set #c %s 0" % O] + ["execute if score @s %s matches 2.. run scoreboard players add #c %s 1" % (ps(n), O) for n in P]
    hdr += ["execute store result storage rpg:paths v.c int 1 run scoreboard players get #c %s" % O,
            "function %s/page/list_body with storage rpg:paths v" % NS,
            "data modify storage rpg:panel ui.actions append value " + dump({"label": txt("‹ 生命之树", BODY), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set 8"}}),
            "function rpg:panel/ui/show with storage rpg:panel ui"]
    fn("page/list", hdr)
    B = []
    by_tier = {}
    for p in PATHS:
        by_tier.setdefault(p[1], []).append(p)
    # 左对齐：对话框只会居中，每行按原版字体量宽、补到同一宽度（mc_textwidth）
    import mc_textwidth as MW
    fonts = {"rpg:pbar": {str(i): 51.0 for i in range(10)}, MW.PAD_FONT: {chr(cp): float(v) for cp, v in MW.PAD_BITS}}
    aligned = MW.table() is not None

    def gap(px):
        return (MW.pad(px) if aligned else None) or txt(" ", BODY)

    def wid(parts):
        """宏 $(x) 量宽时按一个数字算（进度条是一格，计数是一两位）。"""
        import re as _re
        fixed = json.loads(_re.sub(r"\$\([a-z0-9]+\)", "0", json.dumps(parts, ensure_ascii=False)))
        return MW.width(fixed, fonts) or 0.0
    name_w = max(wid([txt(p[5], NAME, True)]) for p in PATHS)
    let_w = max(wid([txt(p[3], NAME)]) for p in PATHS)
    rows = [("$", [txt("走完 ", BODY), txt("$(c)", GOLD, True), txt(" / 22 条。每阶连着的路径至少走完一条才能晋入下一阶；", BODY)], None),
            ("", [txt("所有走完的路径，赐福同时生效。", BODY)], None)]          # (命令前缀, 组件列表, 附加属性)
    for t in sorted(by_tier):
        rows.append(("execute if score @s rpg_sef matches %d.. run " % t,
                     [{"text": "\n"}, txt("◆ ", GLOSS), txt("第 %d 阶 · %s" % (t, TIER[t][2]), TIER[t][5], True), txt(" " + ui.fraktur(TIER[t][3]), GLOSS)], None))
        for n, hi, lo, letter, latin, card, trial, goal, up, down in by_tier[t]:
            click = {"action": "run_command", "command": "/trigger %s set %d" % (DO, n)}
            nm, lt = txt(card, colour(n), True), txt(letter, colour(n))
            head = [gap(12), nm, gap(name_w - wid([nm]) + 6), lt, gap(let_w - wid([lt]) + 8)]
            hover = {"action": "show_text", "value": ["", txt("%s · %s %s\n" % (card, latin, letter), colour(n), True),
                                                       txt("%s — %s\n" % (TIER[hi][2], TIER[lo][2]), BODY),
                                                       txt("试炼：%s\n" % trial, BODY), txt("进度 $(p%d) / %d" % (n, goal), MUTED)]}
            body = {1: [bar_text("b%d" % n), gap(6), txt(trial, BODY)],
                    4: [txt("走完了 · 点这里择位", GOLD, True)],
                    2: [txt("正位", GLOSS), gap(6), txt(up, NAME)],
                    3: [txt("逆位", GLOSS), gap(6), txt(down, NAME)]}
            for st, parts in body.items():
                rows.append(("$execute if score @s %s matches %d run " % (ps(n), st), head + parts, {"click_event": click, "hover_event": hover}))
    for t in sorted(by_tier):
        if t > 2:
            rows.append(("execute if score @s rpg_sef matches %d run " % (t - 1),
                         [{"text": "\n"}, txt("到第 %d 阶 · %s 再开 %d 条。" % (t, TIER[t][2], len(by_tier[t])), MUTED)], None))
    full = max(wid(r[1]) for r in rows)
    for pre, parts, extra in rows:
        tail = [gap(full - wid(parts))] if aligned else []
        comp = dict({"text": "", "extra": parts + tail + [{"text": "\n"}]}, **(extra or {}))
        B.append(pre + "data modify storage rpg:panel ui.body append value " + dump(comp))
    nxt = []
    fn("page/list_body", B + nxt)

    for n, hi, lo, letter, latin, card, trial, goal, up, down in PATHS:
        col = colour(n)
        title = ["", txt("路径 · ", GOLD, True), txt("%s · %s %s" % (card, latin, letter), col, True), txt(" " + ui.fraktur(latin), GLOSS)]
        card_el = {"type": "minecraft:item", "item": {"id": "minecraft:paper", "count": 1, "components": {"minecraft:item_model": "rpg:paths/seal_%d" % n}},
                   "description": {"contents": ["", txt("第 %d 路径　%s — %s\n" % (n, TIER[hi][2], TIER[lo][2]), NAME, True),
                                                txt("试炼　" + trial, BODY)], "width": 240},
                   "show_decorations": False, "show_tooltip": False, "width": 16, "height": 16}
        if has_card(n):      # Codex 的路径牌：逆位就倒着摆
            card_el["item"]["components"]["minecraft:item_model"] = "rpg:paths/card_%d" % n
        card_rev = json.loads(json.dumps(card_el))
        if has_card(n):
            card_rev["item"]["components"]["minecraft:item_model"] = "rpg:paths/card_%d_r" % n
        L = ["# %s 的页（as 玩家）" % pname(n), "function %s/update" % NS,
             "data modify storage rpg:panel ui set value {title:{text:\"\"},body:[],actions:[],tab:2,cards:[]}",
             "data modify storage rpg:panel ui.title set value " + dump(title),
             "execute unless score @s %s matches 3 run data modify storage rpg:panel ui.cards append value %s" % (ps(n), dump(card_el)),
             "execute if score @s %s matches 3 run data modify storage rpg:panel ui.cards append value %s" % (ps(n), dump(card_rev)),
             "scoreboard players operation #i %s = @s %s" % (O, pa(n)), "scoreboard players operation #i %s *= #9 %s" % (O, O),
             "scoreboard players set #g %s %d" % (O, goal), "scoreboard players operation #i %s /= #g %s" % (O, O),
             "execute if score #i %s matches 10.. run scoreboard players set #i %s 9" % (O, O),
             "execute store result storage rpg:paths d.b int 1 run scoreboard players get #i %s" % O,
             "execute store result storage rpg:paths d.p int 1 run scoreboard players get @s %s" % pa(n),
             "function %s/page/%d_m with storage rpg:paths d" % (NS, n)]
        nav = {"label": txt("‹ 路径", BODY), "action": {"type": "minecraft:run_command", "command": "/trigger %s set 1" % DO}}

        def act(label, base, tip):
            return {"label": txt(label, GOLD, True), "tooltip": txt(tip, BODY),
                    "action": {"type": "minecraft:run_command", "command": "/trigger %s set %d" % (DO, base + n)}}
        L += ["execute if score @s %s matches 4 run data modify storage rpg:panel ui.actions append value %s" % (ps(n), dump(act("取正位", 100, up))),
              "execute if score @s %s matches 4 run data modify storage rpg:panel ui.actions append value %s" % (ps(n), dump(act("取逆位", 200, down))),
              "execute if score @s %s matches 2 run data modify storage rpg:panel ui.actions append value %s" % (ps(n), dump(act("翻到逆位", 200, "花 1 颗洗炼钻：" + down))),
              "execute if score @s %s matches 3 run data modify storage rpg:panel ui.actions append value %s" % (ps(n), dump(act("翻到正位", 100, "花 1 颗洗炼钻：" + up))),
              "data modify storage rpg:panel ui.actions append value " + dump(nav),
              "function rpg:panel/ui/show with storage rpg:panel ui"]
        fn("page/%d" % n, L)

        def side(mark, name, text, on):
            return ["", txt(mark + " ", GOLD if on else MUTED), txt(name + "　", GOLD if on else BODY, on), txt(text, NAME if on else BODY), {"text": "\n"}]
        M = ["$execute if score @s %s matches 0 run data modify storage rpg:panel ui.body append value %s" % (ps(n), dump(["", txt("还没开：到第 %d 阶 · %s 时打开。\n" % (hi, TIER[hi][2]), MUTED)])),
             "$execute if score @s %s matches 1 run data modify storage rpg:panel ui.body append value %s" % (ps(n), dump(["", txt("进度　", BODY), bar_text("b"), txt("　$(p) / %d\n" % goal, MUTED)])),
             "$execute if score @s %s matches 2.. run data modify storage rpg:panel ui.body append value %s" % (ps(n), dump(["", txt("已走完\n", GOLD, True)]))]
        M = [m if "$(" in m else m[1:] for m in M]
        for st, a, b in ((2, True, False), (3, False, True)):
            M.append("execute if score @s %s matches %d run data modify storage rpg:panel ui.body append value %s" % (ps(n), st, dump(["", {"text": "\n"}] + side("☀", "正位", up, a)[1:])))
            M.append("execute if score @s %s matches %d run data modify storage rpg:panel ui.body append value %s" % (ps(n), st, dump(side("☾", "逆位", down, b))))
        for st in (0, 1, 4):
            M.append("execute if score @s %s matches %d run data modify storage rpg:panel ui.body append value %s" % (ps(n), st, dump(["", {"text": "\n"}] + side("☀", "正位", up, False)[1:])))
            M.append("execute if score @s %s matches %d run data modify storage rpg:panel ui.body append value %s" % (ps(n), st, dump(side("☾", "逆位", down, False))))
        fn("page/%d_m" % n, M)

        # 确认
        for base, what, name, text, st, other in ((100, "ask_up", "正位", up, 2, 3), (200, "ask_down", "逆位", down, 3, 2)):
            dlg = lambda body, cost: {
                "type": "minecraft:confirmation", "title": title,
                "body": {"type": "minecraft:plain_message", "width": 300, "contents": body},
                "yes": {"label": txt("确定", GOLD, True), "action": {"type": "minecraft:run_command", "command": "/trigger %s set %d" % (DO, base + 200 + n)}},
                "no": {"label": txt("再想想", BODY), "action": {"type": "minecraft:run_command", "command": "/trigger %s set %d" % (DO, n)}},
                "can_close_with_escape": True, "pause": False, "after_action": "close"}
            first = dlg(["", txt("取%s：" % name, BODY), txt(text, NAME, True), txt("\n\n以后想翻面，要花 1 颗洗炼钻。", MUTED)], False)
            flip = dlg(["", txt("花 ", BODY), txt("1 颗洗炼钻", GOLD, True), txt(" 翻到%s：" % name, BODY), txt(text, NAME, True),
                        txt("\n\n另一面的赐福随之失效。", MUTED)], True)
            free = dlg(["", txt("愚者的正位：这一次翻面不花洗炼钻。\n翻到%s：" % name, BODY), txt(text, NAME, True)], True)
            fn("%s/%d" % (what, n), [
                "execute if score @s %s matches 4 run return run dialog show @s %s" % (ps(n), dump(first)),
                "execute if score @s %s matches %d run return run function %s/page/%d" % (ps(n), st, NS, n),
                "execute if score @s %s matches %d if score @s %s matches 2 unless score @s rpg_pa_ff matches 1 run return run dialog show @s %s" % (ps(n), other, ps(11), dump(free)),
                "execute if score @s %s matches %d run return run dialog show @s %s" % (ps(n), other, dump(flip)),
                "function %s/page/%d" % (NS, n)])
            fn("%s/%d" % (what.replace("ask", "set"), n), [
                "execute unless score @s %s matches 2..4 run return run function %s/page/%d" % (ps(n), NS, n),
                "execute if score @s %s matches %d run return run function %s/page/%d" % (ps(n), st, NS, n),
                "execute if score @s %s matches 4 run return run function %s/take {n:%d,s:%d}" % (ps(n), NS, n, st),
                "execute if score @s %s matches 2 unless score @s rpg_pa_ff matches 1 run return run function %s/take_free {n:%d,s:%d}" % (ps(11), NS, n, st),
                "execute store result score #g %s run clear @s *[minecraft:custom_data~{rpg_mat:\"wash_gem\"}] 0" % O,
                "execute if score #g %s matches 0 run return run function %s/no_gem {n:%d}" % (O, NS, n),
                "clear @s *[minecraft:custom_data~{rpg_mat:\"wash_gem\"}] 1",
                "function %s/take {n:%d,s:%d}" % (NS, n, st)])
    fn("take", ["$scoreboard players set @s rpg_ps_$(n) $(s)", "function rpg:sephira/bonus/apply",
                "playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8", "playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.8 1.3",
                "$scoreboard players set #pn %s $(n)" % O, "function %s/page/any" % NS])
    fn("page/any", ["execute if score #pn %s matches %d run return run function %s/page/%d" % (O, n, NS, n) for n in P])
    fn("take_free", ["scoreboard players set @s rpg_pa_ff 1", "$function %s/take {n:$(n),s:$(s)}" % NS])
    fn("no_gem", [tag_line(txt("没有洗炼钻，翻不了面。", ui.WARN)), "$scoreboard players set #pn %s $(n)" % O, "function %s/page/any" % NS])


# ---- 资源包：字母印记、进度条 ---------------------------------------------------

def has_card(n):
    return os.path.exists(os.path.join(REF, "art", "card_%d.png" % n))


def build_rp():
    if not RP:
        return
    from PIL import Image, ImageDraw, ImageFont
    base = os.path.join(RP, "assets/rpg")
    tex = os.path.join(base, "textures/item/paths")
    os.makedirs(tex, exist_ok=True)
    os.makedirs(os.path.join(base, "items/paths"), exist_ok=True)
    os.makedirs(os.path.join(base, "models/item/paths"), exist_ok=True)
    font = None
    for f in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(f):
            font = ImageFont.truetype(f, 11)
            break
    art = os.path.join(REF, "art")
    for n, hi, lo, letter, *_ in PATHS:
        out = os.path.join(tex, "seal_%d.png" % n)
        src = os.path.join(art, "seal_%d.png" % n)
        if os.path.exists(src):        # Codex 的正式图
            im = Image.open(src).convert("RGBA")
            if im.size != (16, 16):
                import add_daath_art as DA      # 同原质法阵：方框滤波、硬边、减色
                im = DA.colour(im, 16).convert("RGBA")
            im.save(out)
        else:                          # 占位：暗金圆印 + 希伯来字母
            im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.ellipse([0, 0, 15, 15], fill=(16, 0, 16, 255),
                      outline=tuple(int(c * 255) for c in ui.rgb(GLOSS)) + (255,))
            d.ellipse([2, 2, 13, 13], outline=tuple(int(c * 255) for c in ui.rgb(GOLD)) + (120,))
            if font:
                layer = Image.new("L", (16, 16), 0)
                ImageDraw.Draw(layer).text((8, 8), letter, font=font, fill=255, anchor="mm")
                layer = layer.point(lambda v: 255 if v > 110 else 0)
                c = tuple(int(x * 255) for x in ui.rgb(colour(n)))
                im.paste(Image.new("RGBA", (16, 16), c + (255,)), (0, 0), layer)
            im.save(out)
        if has_card(n):      # 路径牌 32×32；_r 是逆位（界面里倒过来）
            import add_daath_art as DA
            DA.colour(Image.open(os.path.join(art, "card_%d.png" % n)), 32).convert("RGBA").save(os.path.join(tex, "card_%d.png" % n))
            for suf, disp in (("", {}), ("_r", {"display": {"gui": {"rotation": [0, 0, 180], "scale": [1, 1, 1]}}})):
                with io.open(os.path.join(base, "items/paths/card_%d%s.json" % (n, suf)), "w", encoding="utf-8") as h:
                    json.dump({"model": {"type": "minecraft:model", "model": "rpg:item/paths/card_%d%s" % (n, suf)}}, h)
                with io.open(os.path.join(base, "models/item/paths/card_%d%s.json" % (n, suf)), "w", encoding="utf-8") as h:
                    json.dump(dict({"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/paths/card_%d" % n}}, **disp), h)
        with io.open(os.path.join(base, "items/paths/seal_%d.json" % n), "w", encoding="utf-8") as h:
            json.dump({"model": {"type": "minecraft:model", "model": "rpg:item/paths/seal_%d" % n}}, h)
        with io.open(os.path.join(base, "models/item/paths/seal_%d.json" % n), "w", encoding="utf-8") as h:
            json.dump({"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/paths/seal_%d" % n}}, h)
    # 进度条：数字 0..9 → 十格条（宏把分数写成一个数字，字体换成条）
    W, H = 50, 7
    fdir = os.path.join(base, "textures/font/panel")
    os.makedirs(fdir, exist_ok=True)
    sheet = Image.new("RGBA", (W * 10, H), (0, 0, 0, 0))
    frame = tuple(int(c * 255) for c in ui.rgb(GLOSS)) + (255,)
    fill = tuple(int(c * 255) for c in ui.rgb(GOLD)) + (255,)
    lit = tuple(int(c * 255) for c in ui.rgb(ui.HOLY_LIGHT)) + (255,)
    empty = (40, 30, 44, 255)
    for i in range(10):
        d = ImageDraw.Draw(sheet)
        x0 = i * W
        d.rectangle([x0, 0, x0 + W - 1, H - 1], outline=frame, fill=empty)
        w = 0 if i == 0 else round((W - 4) * i / 9)
        if w:
            d.rectangle([x0 + 2, 2, x0 + 1 + w, H - 3], fill=fill)
            d.line([x0 + 2, 2, x0 + 1 + w, 2], fill=lit)
    sheet.save(os.path.join(fdir, "pbar.png"))
    import mc_textwidth as MW             # 左对齐用的补白字体
    with io.open(os.path.join(base, "font/pad.json"), "w", encoding="utf-8") as h:
        json.dump(MW.pad_font(), h, ensure_ascii=False)
    with io.open(os.path.join(base, "font/pbar.json"), "w", encoding="utf-8") as h:
        json.dump({"providers": [{"type": "bitmap", "file": "rpg:font/panel/pbar.png", "ascent": 7, "height": H,
                                  "chars": ["0123456789"]}]}, h)


def main():
    THR.update(tier_thresholds())
    assert step_xp(2) == 30 and step_xp(9) == 3840, (step_xp(2), step_xp(9))
    build_core()
    build_gate()
    build_hooks()
    build_bless()
    build_pages()
    build_rp()
    print("paths: 22 paths, %d functions" % COUNT[0])


if __name__ == "__main__":
    main()
