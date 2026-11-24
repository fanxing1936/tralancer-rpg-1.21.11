# -*- coding: utf-8 -*-
"""力与技能（方案书第三版「技能树」一节，里程碑 B 第一步：技能框架 + 圣力 12 + 魔力 12）。

  * 圣徽（圣力）/ 罪印（魔力）：拿在主手或副手（用户 2026-11-23 改键）：
      右键 → I 号槽；潜行右键 → II 号槽（按住不连发）；F → III 号槽；Shift+F → 技能页。
      F 键：上一刻两只手里的东西这一刻对调了、其中有圣徽/罪印 -> 换回来再放（fkey）。
  * 技能页：每棵树三支（严厉 / 慈悲 / 中），每支 4 个，按顺序解锁；每个 3 级，
    2 级要美丽阶、3 级要理解阶；价格 1 / 1 / 2（主柱那一支的 3 级只要 1）。
  * 代价：每次放扣力条；圣力另扣生命力（神职者 −30%，同化 50 起 +50%，弥赛亚不扣），
    魔力另涨魔化（弥赛亚减半由 rpg:sephira/force/mana_taint 结算）。燃尽时圣力技能放不出。
  * 冷却按游戏刻记在 rpg_kcNN（到期时刻），不用每刻递减。
  * 堕入魔力 → 圣力树的点全部退回；重回圣力 → 魔力树的点退回。灵魂营火旁花 5 个残魂洗点。
  * 特效：粒子之外用 Boss 的贴图特效（用户 2026-11-23「也可以像 boss 一样用贴图当作特效」）——
    圣力走米迦勒那套烘焙好的白金贴图（add_michael_fx_art），魔力走篡夺者那套白图、运行时染成紫 / 血红（add_usurper_fx_art），
    引擎是 boss_fx.Fx（text_display 字形 + item_display 贴花，带寿命与帧动画）。
终式、身份能力、七位领主终式、Boss 传承技在下一步。
在 build.sh 里跑在 add_sephira.py 之后。
"""
import io
import json
import os
import sys

import rpg_ui_style as ui

import add_michael_fx_art as mart
import boss_fx
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "force")
P = "rpg:force"
O = "rpg_fo"
DO = "rpg_fo_do"
COUNT = 0

C_MUTED = "#9C9A94"
C_BODY = "#E6DFCF"
C_GOLD = "#C9A646"
C_HOLY = "#FFD85A"
C_MANA = "#A276BE"
C_LOCK = "#5A5852"

ENEMY = "type=#rpg:seal_hostile,tag=!rpg.ally"
BOSS_TAGS = ["rpg.pope", "rpg.mkb", "rpg.jqb", "rpg.lub", "rpg.slb", "rpg.usb"]
NOBOSS = ",".join("tag=!" + b for b in BOSS_TAGS)
# 圣光对它们加成
UNHOLY = ["type=#minecraft:undead", "tag=rpg.demon", "tag=rpg.demon.minion"]

TREES = {1: ("圣力", C_HOLY, "圣徽"), 2: ("魔力", C_MANA, "罪印")}
BRANCH = {
    1: {1: ("严厉", "审判", "#FF5A62"), 2: ("慈悲", "守护", "#62B8F0"), 3: ("中柱", "秘仪", "#FFD85A")},
    2: {1: ("严厉", "毁灭", "#FF5A62"), 2: ("慈悲", "续命", "#62B8F0"), 3: ("中柱", "诡道", "#FFD85A")},
}
ROMAN = {1: "Ⅰ", 2: "Ⅱ", 3: "Ⅲ"}

# (编号, 树, 支, 名, 描述, 力 [1,2,3 级], 生命力或魔化 [..], 冷却秒 [..], 被动)
SKILLS = [
    (1, 1, 1, "圣光矛", "前方 20 格穿透的光矛，伤害 6/9/12，对恶魔与亡灵 ×1.5", [20, 20, 18], [1, 1, 1], [5, 4, 3], False),
    (2, 1, 1, "断罪印", "标记准星上的敌人 8 秒，它受到的伤害 +15/25/35%", [20, 20, 20], [1, 1, 1], [12, 10, 8], False),
    (3, 1, 1, "炽天之怒", "以自身为圆心 5 格圣焰，伤害 6/8/10 并点燃", [30, 30, 28], [2, 2, 2], [14, 12, 10], False),
    (4, 1, 1, "火焰之剑", "10 秒内近战附带圣焰 +2/3/4，对恶魔与亡灵翻倍", [30, 30, 30], [2, 2, 2], [30, 26, 22], False),
    (5, 1, 2, "祝福", "治疗准星上的队友（没有就治疗自己）4/6/8 点生命", [20, 18, 16], [1, 1, 1], [8, 7, 6], False),
    (6, 1, 2, "庇护所", "原地 4 格光罩 8 秒：罩内友方抗性 I，2 级起另加生命恢复，3 级抗性 II", [35, 35, 35], [3, 3, 2], [30, 26, 22], False),
    (7, 1, 2, "洁净", "解除自己和 6 格内友方的负面效果，魔化 −5/10/15", [25, 25, 25], [1, 1, 1], [20, 17, 14], False),
    (8, 1, 2, "殉道", "10 秒内 8 格内队友抗性 III，被挡下的伤害 60/50/40% 由你承受", [40, 40, 40], [4, 4, 3], [60, 50, 40], False),
    (9, 1, 3, "显形", "16 格内的隐身者、空缺者显形并发光 6/8/10 秒", [15, 15, 15], [1, 1, 1], [15, 12, 10], False),
    (10, 1, 3, "圣链", "束缚准星上的敌人 2/3/4 秒", [25, 25, 25], [2, 2, 2], [14, 12, 10], False),
    (11, 1, 3, "圣言", "8 格内恶魔与亡灵 2/3/4 秒动弹不得、无力（Boss 改为减速）", [35, 35, 35], [3, 3, 3], [30, 26, 22], False),
    (12, 1, 3, "升天", "向前上方冲出 8/10/12 格，落地无伤", [20, 20, 20], [1, 1, 1], [12, 10, 8], False),
    (13, 2, 1, "暗焰", "投出一团暗火，命中处 2.5 格爆燃，伤害 5/7/9 并点燃", [20, 20, 18], [2, 2, 2], [5, 4, 3], False),
    (14, 2, 1, "血刃", "5/6/7 秒内近战附带凋零 II", [25, 25, 25], [3, 3, 3], [20, 17, 14], False),
    (15, 2, 1, "蚀骨", "前方 6 格锥形，护甲 −4/−6/−8 持续 6 秒，并受 3 点伤害", [25, 25, 25], [3, 3, 3], [14, 12, 10], False),
    (16, 2, 1, "深渊之口", "准星处裂开深渊 4 秒，把 3 格内敌人往里拖，每秒伤害 2/3/4", [40, 40, 40], [5, 5, 4], [30, 26, 22], False),
    (17, 2, 2, "血肉护壳", "涨 10 点魔化，换 8/12/16 点伤害吸收（20 秒）", [0, 0, 0], [10, 10, 10], [30, 26, 22], False),
    (18, 2, 2, "汲取", "吸取准星目标 4/6/8 点生命", [25, 25, 25], [3, 3, 3], [10, 9, 8], False),
    (19, 2, 2, "献祭", "扣 6 点生命，换 40/50/60 魔力", [0, 0, 0], [2, 2, 2], [30, 26, 22], False),
    (20, 2, 2, "不死", "被动：受致命伤时以残血撑 3 秒，冷却 180/150/120 秒（每次魔化 +6）", [0, 0, 0], [6, 6, 6], [180, 150, 120], True),
    (21, 2, 3, "影步", "向前瞬移 8/10/12 格", [15, 15, 15], [2, 2, 2], [8, 7, 6], False),
    (22, 2, 3, "恐惧", "6 格内的敌人被逼退、无力 2/3/4 秒（Boss 不受影响）", [30, 30, 30], [4, 4, 4], [25, 22, 18], False),
    (23, 2, 3, "傀儡", "唤出傀儡为你作战 20 秒（生命 40/60/80）", [45, 45, 45], [6, 6, 5], [60, 50, 40], False),
    (24, 2, 3, "借柱", "免费放一次你所签契约的力量，不占契约冷却", [40, 35, 30], [4, 4, 4], [90, 75, 60], False),
]
SK = {s[0]: s for s in SKILLS}

# 王冠终式与 Boss 传承技（force_ext.py）：(编号, 类, 名, 描述, 力, 生命力或魔化, 冷却秒, Boss)
#   类 h = 圣力终式（只进圣徽的槽）、m = 魔力终式（只进罪印的槽）、l = 传承技（两边的槽都能放，按放进的那棵树付代价）
EXTRA = [
    (25, "h", "哈利路亚", "12 格内的敌人受圣光审判，伤害 16（对恶魔与亡灵 ×1.5）；队友回满生命", 80, 6, 180, None),
    (26, "m", "堕天", "化身 10 秒：期间放魔力技能不耗力、不涨魔化；结束时魔化 +20", 50, 0, 180, None),
    (31, "l", "信条", "8 格内友方 10 秒抗性 I，力的回复翻倍", 30, 2, 45, "pope"),
    (32, "l", "篡夺", "偷走准星目标一个增益效果，并让它 5 秒动弹不得、无力（Boss 只偷增益）", 35, 3, 30, "usurper"),
    (33, "l", "圣殿誓约", "召大团长雅克的残影协战 20 秒", 30, 2, 90, "jacques"),
    (34, "l", "千刀", "2 秒内对前方连斩 8 次，每次 3 点", 30, 3, 20, "saul"),
    (35, "l", "注视", "召 3 只守望者盯住 16 格内最近的 3 个敌人 8 秒：它们受到的伤害 +20%", 35, 3, 40, "michael"),
    (36, "l", "晨星", "从天上砸下一颗晨星：准星处 1 秒后爆开，5 格内伤害 14 并点燃", 50, 5, 60, "lucifer"),
]
EX = {e[0]: e for e in EXTRA}


def kk(n):
    return "rpg_k%02d" % n


def kc(n):
    return "rpg_kc%02d" % n


def slot_obj(tree, s):
    return "rpg_fs_%s%d" % ("h" if tree == 1 else "m", s)


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
    return "tellraw @s " + J(["", t("[力] ", C_GOLD, True)] + parts)


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


def per_level(lines_by_lv):
    """[(lv, cmd)] → 带等级判断的命令"""
    return ["execute if score #lv %s matches %d run %s" % (O, lv, c) for lv, c in lines_by_lv]


def tree_ok(tree):
    """返回「这棵树不能用」的条件前缀（unless … unless …）"""
    return ("unless score @s rpg_force matches 1 unless score @s rpg_force matches 3" if tree == 1 else
            "unless score @s rpg_force matches 2 unless score @s rpg_force matches 3")


def sigil_item(tree):
    name, col, item = TREES[tree]
    rule = t(ui.RULE_TEXT, ui.WHITE)
    lore = [rule, t("拿在主手或副手：", ui.GRAY),
            t("右键 · Ⅰ 号槽", ui.GRAY), t("潜行右键 · Ⅱ 号槽", ui.GRAY),
            t("F · Ⅲ 号槽", ui.GRAY), t("Shift+F · 技能页", ui.GRAY),
            t("圣力扣生命力；燃尽时不回应" if tree == 1 else "魔力会涨魔化", ui.MUTED), rule]
    model = "rpg:force/holy_sigil" if tree == 1 else "rpg:force/sin_sigil"      # Codex 画的图标（force_ext.art）
    return ("minecraft:paper[custom_name=%s,lore=%s,item_model=\"%s\",max_stack_size=1,"
            "enchantment_glint_override=true,"
            "food={nutrition:0,saturation:0f,can_always_eat:1b},"
            "consumable={consume_seconds:100120f,animation:\"none\",sound:\"minecraft:intentionally_empty\","
            "has_consume_particles:false,on_consume_effects:[]},"
            "custom_data={rpg_sigil:%d,rpg_sigil_tag:1b}]"
            % (J(["", t("[%s]" % name, col, True), t(item, ui.WHITE)]), J(lore), model, tree))


# ============================================================================ 核心
def core():
    objs = [O, "rpg_fo_last", "rpg_fo_pm", "rpg_fo_po", "rpg_fo_pg", "rpg_fo_msg", "rpg_fo_sh", "rpg_fo_sm", "rpg_fo_vf",
            "rpg_fo_buf", "rpg_fo_bk", "rpg_fo_blv", "rpg_fo_mt", "rpg_fo_mlv", "rpg_fo_und",
            "rpg_fo_hp", "rpg_fo_end", "rpg_fo_mk", "rpg_fo_lv", "rpg_fo_k", "rpg_fo_life", "rpg_fo_kd", "rpg_fo_fl"]
    objs += [kk(n) for n in list(SK) + list(EX)] + [kc(n) for n in list(SK) + list(EX)]
    objs += [slot_obj(tr, s) for tr in (1, 2) for s in (1, 2, 3)]
    load = ["scoreboard objectives add %s dummy" % o for o in objs]
    load += ["scoreboard objectives add %s trigger" % DO,
             "scoreboard objectives add rpg_fo_dd minecraft.custom:minecraft.damage_dealt",
             "scoreboard objectives add rpg_fo_dr minecraft.custom:minecraft.damage_resisted"]
    for c in (2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 100, 105, 125, 150, 1000):
        load.append("scoreboard players set #%d %s %d" % (c, O, c))
    fn("load", load)
    fn("tick", [
        "execute store result score #now %s run time query gametime" % O,
        "execute as @a[scores={%s=1..}] at @s run function %s/press" % (DO, P),
        "execute as @a at @s run function %s/fkey" % P,
        "execute as @a[scores={rpg_fo_buf=1..}] at @s run function %s/buff/tick" % P,
        "execute as @a[scores={rpg_fo_mt=1..}] at @s run function %s/sk/8/tick" % P,
        "execute as @e[tag=rpg.fo.mk] at @s run function %s/sk/2/tick" % P,
        "execute as @e[type=minecraft:marker,tag=rpg.fo.zone] at @s run function %s/zone/tick" % P,
        "execute as @e[tag=rpg.fo.hfx] at @s run function %s/h/fx/tick" % P,
        "execute as @e[tag=rpg.fo.mfx] at @s run function %s/m/fx/tick" % P,
        "scoreboard players operation #m %s = #now %s" % (O, O),
        "scoreboard players operation #m %s %%= #20 %s" % (O, O),
        "execute unless score #m %s matches 0 run return 0" % O,
        "execute as @e[tag=rpg.fo.timed] run function %s/timed" % P,
        "execute as @a at @s run function %s/sec" % P,
    ])
    fn("sec", [
        "# 每秒（as/at 玩家）",
        "scoreboard players enable @s %s" % DO,
        "execute unless score @s rpg_ob matches 100 run return 0",
        "execute if score @s rpg_force matches 1 unless entity @s[tag=rpg.fo.g1] run function %s/give/first_1" % P,
        "execute if score @s rpg_force matches 3 unless entity @s[tag=rpg.fo.g1] run function %s/give/first_1" % P,
        "execute if score @s rpg_force matches 2..3 unless entity @s[tag=rpg.fo.g2] run function %s/give/first_2" % P,
        "# 神职者：祝福生来 1 级（不花点，洗点后也还在）",
        "execute if score @s rpg_ident matches 3 if score @s rpg_force matches 1 unless score @s %s matches 1.. run scoreboard players set @s %s 1" % (kk(5), kk(5)),
    ])
    fn("timed", [
        "# 带时限的效果（as 实体）：到时撤掉",
        "execute if score @s rpg_fo_end > #now %s run return 0" % O,
        "attribute @s minecraft:armor modifier remove rpg:fo_rot",
        "execute if entity @s[tag=rpg.fo.pup] at @s run particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.03 20",
        "execute if entity @s[tag=rpg.fo.pup] run tp @s ~ -400 ~",
        "execute if entity @s[tag=rpg.fo.pup] run kill @s",
        "tag @s remove rpg.fo.timed",
    ])
    for tr in (1, 2):
        name, col, item = TREES[tr]
        fn("give/first_%d" % tr, [
            "tag @s add rpg.fo.g%d" % tr,
            "give @s %s" % sigil_item(tr),
            say([t("你得到了", C_MUTED), t(item, col, True), t("。拿着它按 Shift+F，打开技能页。", C_BODY)]),
            "playsound minecraft:item.armor.equip_gold player @s ~ ~ ~ 1 1.2",
        ])
        fn("give/reissue_%d" % tr, [
            "execute %s run return run function %s/fail/say {m:\"你没有%s\"}" % (tree_ok(tr), P, name),
            "execute if items entity @s container.* *[minecraft:custom_data~{rpg_sigil:%d}] run return run function %s/fail/say {m:\"%s就在你身上\"}" % (tr, P, item),
            "execute if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:%d}] run return run function %s/fail/say {m:\"%s就在你身上\"}" % (tr, P, item),
            "give @s %s" % sigil_item(tr),
            "playsound minecraft:item.armor.equip_gold player @s ~ ~ ~ 1 1.2",
        ])
    fn("fail/say", [
        "# 失败提示（有节流，按住也不刷屏）",
        "execute if score @s rpg_fo_msg > #now %s run return 0" % O,
        "scoreboard players operation @s rpg_fo_msg = #now %s" % O,
        "scoreboard players add @s rpg_fo_msg 10",
        "playsound minecraft:block.dispenser.fail player @s ~ ~ ~ 0.6 1.4",
        "$tellraw @s [\"\",{\"text\":\"[力] \",\"color\":\"%s\",\"bold\":true,\"italic\":false},{\"text\":\"$(m)\",\"color\":\"%s\",\"italic\":false}]" % (C_GOLD, C_MUTED),
    ])


# ============================================================================ 施放
def cast():
    fn("use", [
        "# 圣徽 / 罪印被按下（rpg:force/use 进度，按住期间每刻都响：只认按下的那一刻）",
        "advancement revoke @s only rpg:force/use",
        "execute store result score #now %s run time query gametime" % O,
        "scoreboard players operation #g %s = #now %s" % (O, O),
        "scoreboard players remove #g %s 1" % O,
        "execute if score @s rpg_fo_last >= #g %s run return run scoreboard players operation @s rpg_fo_last = #now %s" % (O, O),
        "scoreboard players operation @s rpg_fo_last = #now %s" % O,
        "scoreboard players set #tree %s 0" % O,
        "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_sigil:1}] run scoreboard players set #tree %s 1" % O,
        "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_sigil:2}] run scoreboard players set #tree %s 2" % O,
        "execute if score #tree %s matches 0 if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:1}] run scoreboard players set #tree %s 1" % (O, O),
        "execute if score #tree %s matches 0 if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:2}] run scoreboard players set #tree %s 2" % (O, O),
        "execute if score #tree %s matches 0 run return 0" % O,
        "scoreboard players set #slot %s 1" % O,
        "execute if predicate rpg:sneaking run scoreboard players set #slot %s 2" % O,
        "function %s/cast" % P,
    ])
    # F 键（as/at 每个玩家每刻）：#fm/#fo = 这一刻主手/副手是哪种印（0 不是）
    sig = "if items entity @s weapon.%s *[minecraft:custom_data~{rpg_sigil:%d}]"
    fn("fkey", [
        "scoreboard players set #fm %s 0" % O,
        "scoreboard players set #fo %s 0" % O,
        "execute %s run scoreboard players set #fm %s 1" % (sig % ("mainhand", 1), O),
        "execute %s run scoreboard players set #fm %s 2" % (sig % ("mainhand", 2), O),
        "execute %s run scoreboard players set #fo %s 1" % (sig % ("offhand", 1), O),
        "execute %s run scoreboard players set #fo %s 2" % (sig % ("offhand", 2), O),
        "# 契约之书算第 3 种（化身 / 打开契约，rpg:pact/fkey）",
        "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact_tag:1b}] run scoreboard players set #fm %s 3" % O,
        "execute if items entity @s weapon.offhand *[minecraft:custom_data~{pact_tag:1b}] run scoreboard players set #fo %s 3" % O,
        "execute if score @s rpg_fo_pm matches 0.. if score @s rpg_fo_po matches 0.. "
        "unless score @s rpg_fo_pm = @s rpg_fo_po if score #fm %s = @s rpg_fo_po if score #fo %s = @s rpg_fo_pm "
        "run function %s/fpress" % (O, O, P),
        "scoreboard players operation @s rpg_fo_pm = #fm %s" % O,
        "scoreboard players operation @s rpg_fo_po = #fo %s" % O,
    ])
    fn("fpress", [
        "# 按了 F：两只手换回来（哪一边都可能是锻造武器，原样放回），再放 Ⅲ 号槽 / Shift+F 开技能页",
        "summon minecraft:item_display ~ ~ ~ {Tags:[\"rpg.fo.tmp\"]}",
        "item replace entity @e[type=minecraft:item_display,tag=rpg.fo.tmp,limit=1,sort=nearest] contents from entity @s weapon.mainhand",
        "item replace entity @s weapon.mainhand from entity @s weapon.offhand",
        "item replace entity @s weapon.offhand from entity @e[type=minecraft:item_display,tag=rpg.fo.tmp,limit=1,sort=nearest] contents",
        "kill @e[type=minecraft:item_display,tag=rpg.fo.tmp]",
        "scoreboard players operation #fm %s = @s rpg_fo_pm" % O,
        "scoreboard players operation #fo %s = @s rpg_fo_po" % O,
        "scoreboard players operation #tree %s = #fm %s" % (O, O),
        "execute if score #tree %s matches 0 run scoreboard players operation #tree %s = #fo %s" % (O, O, O),
        "execute if score #tree %s matches 3 run return run function rpg:pact/fkey" % O,
        "execute if predicate rpg:sneaking run return run function %s/page/by_tree" % P,
        "scoreboard players set #slot %s 3" % O,
        "function %s/cast" % P,
    ])
    lines = ["# 按 #tree / #slot 找到槽里的技能并施放（as/at 玩家）",
             "scoreboard players set #k %s 0" % O]
    for tr in (1, 2):
        for s in (1, 2, 3):
            lines.append("execute if score #tree %s matches %d if score #slot %s matches %d run scoreboard players operation #k %s = @s %s"
                         % (O, tr, O, s, O, slot_obj(tr, s)))
    lines += [
        "execute if score #tree %s matches 1 %s run return run function %s/fail/say {m:\"你没有圣力，圣徽不回应你\"}" % (O, tree_ok(1), P),
        "execute if score #tree %s matches 2 %s run return run function %s/fail/say {m:\"你没有魔力，罪印不回应你\"}" % (O, tree_ok(2), P),
        "execute if score #tree %s matches 1 if entity @s[tag=rpg.burnt] run return run function %s/fail/say {m:\"燃尽：生命力回到 30 之前，圣力不会回应你\"}" % (O, P),
        "execute unless score #k %s matches 1.. run return run function %s/fail/say {m:\"这个槽是空的：拿着它按 Shift+F 打开技能页，把技能放进槽里\"}" % (O, P),
    ]
    for n in list(SK) + list(EX):
        lines.append("execute if score #k %s matches %d run return run function %s/sk/%d/try" % (O, n, P, n))
    fn("cast", lines)
    fn("cd_say", [
        "# #s = 剩余秒数",
        "execute if score @s rpg_fo_msg > #now %s run return 0" % O,
        "scoreboard players operation @s rpg_fo_msg = #now %s" % O,
        "scoreboard players add @s rpg_fo_msg 10",
        "playsound minecraft:block.dispenser.fail player @s ~ ~ ~ 0.6 1.4",
        "tellraw @s " + J(["", t("[力] ", C_GOLD, True), t("还在冷却：", C_MUTED),
                           {"score": {"name": "#s", "objective": O}, "color": C_BODY}, t(" 秒", C_MUTED)]),
    ])
    pay()
    for n, tr, br, name, desc, fc, xc, cd, passive in SKILLS:
        try_ = ["# %s（as/at 施放者）" % name,
                "scoreboard players operation #lv %s = @s %s" % (O, kk(n)),
                "execute unless score #lv %s matches 1.. run return run function %s/fail/say {m:\"还没学会%s\"}" % (O, P, name)]
        if passive:
            fn("sk/%d/try" % n, try_ + ["function %s/fail/say {m:\"%s是被动，学会就生效，不用放进槽里\"}" % (P, name)])
            continue
        cool = "execute if score @s %s > #now %s run " % (kc(n), O)
        try_ += [
            cool + "scoreboard players operation #s %s = @s %s" % (O, kc(n)),
            cool + "scoreboard players operation #s %s -= #now %s" % (O, O),
            cool + "scoreboard players add #s %s 19" % O,
            cool + "scoreboard players operation #s %s /= #20 %s" % (O, O),
            cool + "return run function %s/cd_say" % P,
        ]
        try_ += per_level([(i + 1, "scoreboard players set #fc %s %d" % (O, fc[i])) for i in range(3)])
        if n == 24:
            try_.append("execute unless entity @s[tag=rpg.pact] run return run function %s/fail/say {m:\"你没有契约可借\"}" % P)
        if n == 19:
            try_ += ["execute store result score #h %s run data get entity @s Health" % O,
                     "execute unless score #h %s matches 8.. run return run function %s/fail/say {m:\"生命不够献祭\"}" % (O, P)]
        if tr == 1:
            try_ += per_level([(i + 1, "scoreboard players set #vc %s %d" % (O, xc[i] * 10)) for i in range(3)])
            try_ += ["function %s/pay/h" % P, "execute unless score #ok %s matches 1 run return 0" % O]
        else:
            try_ += per_level([(i + 1, "scoreboard players set #xc %s %d" % (O, xc[i])) for i in range(3)])
            try_ += ["function %s/pay/m" % P, "execute unless score #ok %s matches 1 run return 0" % O]
        try_ += per_level([(i + 1, "scoreboard players set #c %s %d" % (O, cd[i] * 20)) for i in range(3)])
        try_ += ["function %s/pay/cd" % P,
                 "scoreboard players operation @s %s = #now %s" % (kc(n), O),
                 "scoreboard players operation @s %s += #c %s" % (kc(n), O),
                 "tag @s add rpg.fo.me",
                 "function %s/sk/%d/do" % (P, n),
                 "tag @s remove rpg.fo.me"]
        fn("sk/%d/try" % n, try_)


def pay():
    """付代价（as 施放者）：#fc 力；圣力 #vc 生命力（十分之一点）；魔力 #xc 魔化。成功时 #ok = 1。"""
    fn("pay/h", [
        "scoreboard players set #ok %s 0" % O,
        "execute unless score @s rpg_mana >= #fc %s run return run function %s/fail/say {m:\"圣力不够\"}" % (O, P),
        "scoreboard players operation @s rpg_mana -= #fc %s" % O,
        "# 生命力：神职者 −30%（美丽阶起 −60%），同化 50 起 +50%，弥赛亚不扣",
        "execute if score @s rpg_ident matches 3 unless score @s rpg_sef matches 5.. run scoreboard players operation #vc %s *= #7 %s" % (O, O),
        "execute if score @s rpg_ident matches 3 if score @s rpg_sef matches 5.. run scoreboard players operation #vc %s *= #4 %s" % (O, O),
        "execute if score @s rpg_ident matches 3 run scoreboard players operation #vc %s /= #10 %s" % (O, O),
        "execute if score @s rpg_assim matches 50.. run scoreboard players operation #vc %s *= #15 %s" % (O, O),
        "execute if score @s rpg_assim matches 50.. run scoreboard players operation #vc %s /= #10 %s" % (O, O),
        "execute if score @s rpg_messiah matches 1 run scoreboard players set #vc %s 0" % O,
        "scoreboard players operation @s rpg_fo_vf += #vc %s" % O,
        "scoreboard players operation #q %s = @s rpg_fo_vf" % O,
        "scoreboard players operation #q %s /= #10 %s" % (O, O),
        "scoreboard players operation @s rpg_vital -= #q %s" % O,
        "scoreboard players operation @s rpg_fo_vf %%= #10 %s" % O,
        "execute if score @s rpg_vital matches ..-1 run scoreboard players set @s rpg_vital 0",
        "scoreboard players set #ok %s 1" % O,
    ])
    fn("pay/m", [
        "scoreboard players set #ok %s 0" % O,
        "# 堕天期间：魔力技能不耗力、不涨魔化",
        "execute if score @s rpg_fo_fl > #now %s run return run scoreboard players set #ok %s 1" % (O, O),
        "execute if score @s rpg_force matches 2 unless score @s rpg_mana >= #fc %s run return run function %s/fail/say {m:\"魔力不够\"}" % (O, P),
        "execute if score @s rpg_force matches 3 unless score @s rpg_mana2 >= #fc %s run return run function %s/fail/say {m:\"魔力不够\"}" % (O, P),
        "execute if score @s rpg_force matches 2 run scoreboard players operation @s rpg_mana -= #fc %s" % O,
        "execute if score @s rpg_force matches 3 run scoreboard players operation @s rpg_mana2 -= #fc %s" % O,
        "scoreboard players operation @s rpg_taint += #xc %s" % O,
        "scoreboard players set #ok %s 1" % O,
    ])
    fn("pay/cd", [
        "# 冷却修正（#c 刻）：边缘者放魔力技能 −10%（美丽阶起 −20%）",
        "execute unless score #tree %s matches 2 run return 0" % O,
        "execute unless score @s rpg_ident matches 2 run return 0",
        "execute unless score @s rpg_sef matches 5.. run scoreboard players operation #c %s *= #9 %s" % (O, O),
        "execute if score @s rpg_sef matches 5.. run scoreboard players operation #c %s *= #8 %s" % (O, O),
        "scoreboard players operation #c %s /= #10 %s" % (O, O),
    ])


# ============================================================================ 通用：伤害、射线、位移
def lv3(vals, fmt):
    """[v1,v2,v3] + 'cmd %d' → 按等级的三行"""
    return per_level([(i + 1, fmt % vals[i]) for i in range(3)])


def helpers():
    fn("unholy", ["scoreboard players set #u %s 0" % O] +
       ["execute if entity @s[%s] run scoreboard players set #u %s 1" % (u, O) for u in UNHOLY])
    fn("hit", [
        "# as/at 目标：#dmg = 伤害（十分之一点），#hm = 对恶魔与亡灵的倍率（十分之一）",
        "scoreboard players operation #d %s = #dmg %s" % (O, O),
        "function %s/unholy" % P,
        "execute if score #u %s matches 1 run scoreboard players operation #d %s *= #hm %s" % (O, O, O),
        "execute if score #u %s matches 1 run scoreboard players operation #d %s /= #10 %s" % (O, O, O),
        "execute if entity @a[tag=rpg.fo.me,limit=1] run function %s/x/id/spell_mod" % P,
        "execute store result storage rpg:force h.d float 0.1 run scoreboard players get #d %s" % O,
        "execute if entity @a[tag=rpg.fo.me,limit=1] run return run function %s/hit_by with storage rpg:force h" % P,
        "function %s/hit_no with storage rpg:force h" % P,
    ])
    fn("hit_by", ["$damage @s $(d) rpg:force by @a[tag=rpg.fo.me,limit=1]"])
    fn("hit_no", ["$damage @s $(d) rpg:force"])


def ray(key, steps, particle, sel, on_hit, pierce=False, on_end=None):
    """从施放者眼睛向前的射线（每步 0.5 格）。on_hit 以命中的实体为 as/at；on_end 在射线终点执行。"""
    base = "%s/ray/%s" % (P, key)
    fn("ray/%s/go" % key, [
        "scoreboard players set #r %s %d" % (O, steps),
        "scoreboard players set #stop %s 0" % O,
        "execute anchored eyes positioned ^ ^ ^0.6 run function %s/step" % base,
        "tag @e[tag=rpg.fo.hit] remove rpg.fo.hit",
    ])
    end = ("function %s/end" % base) if on_end else "scoreboard players set #stop %s 1" % O
    lim = "" if pierce else ",limit=1,sort=nearest"
    fn("ray/%s/step" % key, [
        "execute if score #r %s matches ..%d run %s" % (O, steps - 3, particle.replace("particle ", "particle ", 1)),
        "execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[%s,dx=0,dy=0,dz=0,tag=!rpg.fo.hit%s] at @s run function %s/hit" % (sel, lim, base),
        "execute if score #stop %s matches 1 run return run %s" % (O, end),
        "scoreboard players remove #r %s 1" % O,
        "execute unless block ~ ~ ~ #rpg:force/pass run return run %s" % end,
        "execute if score #r %s matches ..0 run return run %s" % (O, end),
        "execute positioned ^ ^ ^0.5 run function %s/step" % base,
    ])
    fn("ray/%s/hit" % key, ["tag @s add rpg.fo.hit"] + ([] if pierce else ["scoreboard players set #stop %s 1" % O]) + on_hit)
    if on_end:
        fn("ray/%s/end" % key, on_end)


def ground(name, lines):
    """从当前位置往下找地面（最多 6 格），在地面上执行 lines（贴花、法阵标记）。"""
    base = "%s/ground/%s" % (P, name)
    fn("ground/%s/go" % name, ["scoreboard players set #gd %s 12" % O, "function %s/step" % base])
    fn("ground/%s/step" % name, [
        "scoreboard players remove #gd %s 1" % O,
        "execute if score #gd %s matches 1.. if block ~ ~-0.3 ~ #rpg:force/pass positioned ~ ~-0.5 ~ run return run function %s/step" % (O, base),
        "execute align y run function %s/at" % base,
    ])
    fn("ground/%s/at" % name, lines)


def blink():
    fn("blink/step", [
        "execute positioned ^ ^ ^0.5 if block ~ ~ ~ #rpg:force/pass if block ~ ~1 ~ #rpg:force/pass run function %s/blink/move" % P,
    ])
    fn("blink/move", [
        "tp @a[tag=rpg.fo.me,limit=1] ~ ~ ~",
        "particle minecraft:$(p) ~ ~1 ~ 0.15 0.3 0.15 0 2".replace("$(p)", "end_rod"),
        "scoreboard players remove #r %s 1" % O,
        "execute if score #r %s matches 1.. run function %s/blink/step" % (O, P),
    ])
    fn("blink/move_m", [
        "tp @a[tag=rpg.fo.me,limit=1] ~ ~ ~",
        "particle minecraft:large_smoke ~ ~1 ~ 0.15 0.3 0.15 0 2",
        "scoreboard players remove #r %s 1" % O,
        "execute if score #r %s matches 1.. run function %s/blink/step_m" % (O, P),
    ])
    fn("blink/step_m", [
        "execute positioned ^ ^ ^0.5 if block ~ ~ ~ #rpg:force/pass if block ~ ~1 ~ #rpg:force/pass run function %s/blink/move_m" % P,
    ])


# ============================================================================ 技能效果
HOLY_LINE = "particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1 force"
GOLD_DUST = "particle minecraft:dust{color:[1.0,0.85,0.35],scale:1.0} ~ ~ ~ 0.02 0.02 0.02 0 1 force"
MANA_LINE = "particle minecraft:soul_fire_flame ~ ~ ~ 0.02 0.02 0.02 0 1 force"
BLOOD_DUST = "particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.1} ~ ~ ~ 0.02 0.02 0.02 0 1 force"
NEGATIVE = ["poison", "wither", "slowness", "weakness", "blindness", "nausea", "hunger", "mining_fatigue",
            "darkness", "levitation", "unluck", "infested", "oozing", "weaving", "wind_charged"]


def skills():
    hit = "function %s/hit" % P
    # ---------------------------------------------------------------- 圣力 · 严厉
    ray("spear", 40, HOLY_LINE, ENEMY,
        lv3([60, 90, 120], "scoreboard players set #dmg " + O + " %d") +
        ["scoreboard players set #hm %s 15" % O, hit, "particle minecraft:end_rod ~ ~1.2 ~ 0.15 0.3 0.15 0.12 8"],
        pierce=True)
    fn("sk/1/do", ["playsound minecraft:item.trident.throw player @a[distance=..16] ~ ~ ~ 1 1.6",
                   "playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 0.5 2",
                   "function %s/ray/spear/go" % P])

    ray("mark", 40, GOLD_DUST, ENEMY, [
        "tag @s add rpg.fo.mk",
        "scoreboard players operation @s rpg_fo_end = #now %s" % O,
        "scoreboard players add @s rpg_fo_end 160",
    ] + lv3([15, 25, 35], "scoreboard players set @s rpg_fo_mk %d") + [
        "execute store result score @s rpg_fo_hp run data get entity @s Health 10",
        "effect give @s minecraft:glowing 8 0 true",
        "playsound minecraft:block.anvil.land hostile @a[distance=..16] ~ ~ ~ 0.4 1.8",
        "particle minecraft:enchanted_hit ~ ~1.2 ~ 0.3 0.5 0.3 0.2 20"])
    fn("sk/2/do", ["playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.7", "function %s/ray/mark/go" % P])
    fn("sk/2/tick", [
        "# 断罪印（as/at 被标记的实体，每刻）：比上一刻少掉的血 × 加成，补一刀",
        "execute if score @s rpg_fo_end <= #now %s run return run function %s/sk/2/off" % (O, P),
        "particle minecraft:wax_off ~ ~2.3 ~ 0.1 0.05 0.1 0 1",
        "execute store result score #h %s run data get entity @s Health 10" % O,
        "execute if score #h %s >= @s rpg_fo_hp run return run scoreboard players operation @s rpg_fo_hp = #h %s" % (O, O),
        "scoreboard players operation #dmg %s = @s rpg_fo_hp" % O,
        "scoreboard players operation #dmg %s -= #h %s" % (O, O),
        "scoreboard players operation #dmg %s *= @s rpg_fo_mk" % O,
        "scoreboard players operation #dmg %s /= #100 %s" % (O, O),
        "scoreboard players set #hm %s 10" % O,
        "execute if score #dmg %s matches 1.. run function %s/hit" % (O, P),
        "execute if score #dmg %s matches 1.. run particle minecraft:crit ~ ~1.2 ~ 0.3 0.4 0.3 0.2 8" % O,
        "execute store result score @s rpg_fo_hp run data get entity @s Health 10",
    ])
    fn("sk/2/off", ["tag @s remove rpg.fo.mk", "effect clear @s minecraft:glowing"])

    fn("sk/3/do", [
        "playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 1 0.8",
        "playsound minecraft:block.beacon.activate player @a[distance=..16] ~ ~ ~ 0.6 1.8",
        "particle minecraft:flame ~ ~0.3 ~ 2.6 0.2 2.6 0.03 160",
        "particle minecraft:end_rod ~ ~1 ~ 0.4 0.4 0.4 0.25 50",
    ] + lv3([60, 80, 100], "scoreboard players set #dmg " + O + " %d") + [
        "scoreboard players set #hm %s 10" % O,
        "execute as @e[%s,distance=..5] at @s run function %s/sk/3/one" % (ENEMY, P),
    ])
    fn("sk/3/one", [hit, "data merge entity @s {Fire:80s}"])

    fn("sk/4/do", [
        "scoreboard players operation @s rpg_fo_buf = #now %s" % O,
        "scoreboard players add @s rpg_fo_buf 200",
        "scoreboard players set @s rpg_fo_bk 4",
        "scoreboard players operation @s rpg_fo_blv = #lv %s" % O,
        "scoreboard players set @s rpg_fo_dd 0",
        "playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 1 1.3",
        "particle minecraft:flame ~ ~1 ~ 0.3 0.6 0.3 0.05 40",
    ])
    fn("buff/tick", [
        "# 火焰之剑 / 血刃（as/at 玩家，每刻）",
        "execute if score @s rpg_fo_buf <= #now %s run return run scoreboard players set @s rpg_fo_buf 0" % O,
        "execute if score @s rpg_fo_bk matches 4 run particle minecraft:flame ^-0.35 ^1.1 ^0.45 0.05 0.08 0.05 0.01 1",
        "execute if score @s rpg_fo_bk matches 14 run particle minecraft:dust{color:[0.65,0.05,0.12],scale:0.9} ^-0.35 ^1.1 ^0.45 0.06 0.08 0.06 0 1",
        "execute unless score @s rpg_fo_dd matches 1.. run return 0",
        "scoreboard players set @s rpg_fo_dd 0",
        "scoreboard players operation #lv %s = @s rpg_fo_blv" % O,
        "tag @s add rpg.fo.me",
        "execute if score @s rpg_fo_bk matches 4 as @e[%s,tag=rpg.hurt,distance=..6,limit=1,sort=nearest] at @s run function %s/sk/4/proc" % (ENEMY, P),
        "execute if score @s rpg_fo_bk matches 14 as @e[%s,tag=rpg.hurt,distance=..6,limit=1,sort=nearest] at @s run function %s/sk/14/proc" % (ENEMY, P),
        "tag @s remove rpg.fo.me",
    ])
    fn("sk/4/proc", lv3([20, 30, 40], "scoreboard players set #dmg " + O + " %d") + [
        "scoreboard players set #hm %s 20" % O, hit, "data merge entity @s {Fire:60s}",
        "particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.04 14"])

    # ---------------------------------------------------------------- 圣力 · 慈悲
    ray("bless", 32, "particle minecraft:wax_on ~ ~ ~ 0 0 0 0 1 force", "type=player,tag=!rpg.fo.me,gamemode=!spectator",
        ["function %s/sk/5/heal" % P])
    fn("sk/5/do", [
        "playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 1 1.4",
        "function %s/ray/bless/go" % P,
        "execute unless score #stop %s matches 1 run function %s/sk/5/heal" % (O, P),
    ])
    fn("sk/5/heal", lv3([0, 0, 1], "effect give @s minecraft:instant_health 1 %d true") + [
        "execute if score #lv %s matches 2 run effect give @s minecraft:regeneration 3 1 true" % O,
        "particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 6",
        "particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.04 20"])

    fn("sk/6/do", [
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.fo.zone\",\"rpg.fo.znew\"]}",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_k 6",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_lv = #lv %s" % O,
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end = #now %s" % O,
        "scoreboard players add @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end 160",
        "tag @e[type=minecraft:marker,tag=rpg.fo.znew] remove rpg.fo.znew",
        "playsound minecraft:block.beacon.activate player @a[distance=..16] ~ ~ ~ 1 1.5",
        "particle minecraft:end_rod ~ ~1 ~ 1.5 1 1.5 0.02 60",
    ])
    fn("zone/tick", [
        "# 地上的法阵（as/at 标记，每刻）",
        "execute if score @s rpg_fo_end <= #now %s run return run kill @s" % O,
        "scoreboard players operation #zt %s = @s rpg_fo_end" % O,
        "scoreboard players operation #zt %s -= #now %s" % (O, O),
        "scoreboard players operation #zt %s %%= #10 %s" % (O, O),
        "scoreboard players operation #lv %s = @s rpg_fo_lv" % O,
        "execute if score @s rpg_fo_k matches 6 run function %s/zone/sanct" % P,
        "execute if score @s rpg_fo_k matches 16 run function %s/zone/abyss" % P,
    ])
    fn("zone/sanct", [
        "tp @s ~ ~ ~ ~15 0",
        "particle minecraft:end_rod ^ ^0.1 ^4 0 0 0 0 1 force",
        "particle minecraft:end_rod ^ ^0.1 ^-4 0 0 0 0 1 force",
        "particle minecraft:end_rod ^4 ^0.1 ^ 0 0 0 0 1 force",
        "particle minecraft:end_rod ^-4 ^0.1 ^ 0 0 0 0 1 force",
        "particle minecraft:wax_on ~ ~1.5 ~ 2.5 1 2.5 0 2",
        "execute unless score #zt %s matches 0 run return 0" % O,
        "execute if score #lv %s matches ..2 run effect give @a[distance=..4,gamemode=!spectator] minecraft:resistance 1 0 true" % O,
        "execute if score #lv %s matches 3 run effect give @a[distance=..4,gamemode=!spectator] minecraft:resistance 1 1 true" % O,
        "execute if score #lv %s matches 2.. run effect give @a[distance=..4,gamemode=!spectator] minecraft:regeneration 2 0 true" % O,
    ])

    fn("sk/7/do", [
        "playsound minecraft:block.bubble_column.upwards_inside player @a[distance=..16] ~ ~ ~ 1 1.2",
        "playsound minecraft:block.amethyst_block.resonate player @a[distance=..16] ~ ~ ~ 1 1.4",
        "particle minecraft:end_rod ~ ~1 ~ 3 0.6 3 0.01 60",
        "execute as @a[distance=..6,gamemode=!spectator] at @s run function %s/sk/7/one" % P,
    ])
    fn("sk/7/one", ["effect clear @s minecraft:%s" % e for e in NEGATIVE] +
       lv3([5, 10, 15], "scoreboard players remove @s rpg_taint %d") +
       ["execute if score @s rpg_taint matches ..-1 run scoreboard players set @s rpg_taint 0",
        "particle minecraft:wax_on ~ ~0.15 ~ 0.4 0.05 0.4 0 6"])

    fn("sk/8/do", [
        "scoreboard players operation @s rpg_fo_mt = #now %s" % O,
        "scoreboard players add @s rpg_fo_mt 200",
        "scoreboard players operation @s rpg_fo_mlv = #lv %s" % O,
        "scoreboard players set @a[distance=..8] rpg_fo_dr 0",
        "playsound minecraft:block.bell.use player @a[distance=..16] ~ ~ ~ 1 0.7",
        "particle minecraft:end_rod ~ ~1 ~ 4 0.5 4 0 60",
    ])
    fn("sk/8/tick", [
        "# 殉道（as/at 施放者，每刻）：8 格内队友的抗性挡下多少，按比例算到施放者头上",
        "execute if score @s rpg_fo_mt <= #now %s run return run scoreboard players set @s rpg_fo_mt 0" % O,
        "particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.5 0.3 0 1",
        "tag @s add rpg.fo.mtc",
        "scoreboard players operation #zt %s = #now %s" % (O, O),
        "scoreboard players operation #zt %s %%= #10 %s" % (O, O),
        "execute if score #zt %s matches 0 run effect give @a[distance=..8,tag=!rpg.fo.mtc,gamemode=!spectator] minecraft:resistance 1 2 true" % O,
        "execute if score #zt %s matches 0 as @a[distance=..8,tag=!rpg.fo.mtc,gamemode=!spectator] at @s run particle minecraft:end_rod ~ ~2.2 ~ 0.1 0.1 0.1 0 1" % O,
        "scoreboard players set #x %s 0" % O,
        "execute as @a[distance=..8,tag=!rpg.fo.mtc,scores={rpg_fo_dr=1..}] run function %s/sk/8/sum" % P,
        "tag @s remove rpg.fo.mtc",
        "execute unless score #x %s matches 1.. run return 0" % O,
        "scoreboard players operation #dmg %s = #x %s" % (O, O),
        "execute if score @s rpg_fo_mlv matches 1 run scoreboard players set #pc %s 60" % O,
        "execute if score @s rpg_fo_mlv matches 2 run scoreboard players set #pc %s 50" % O,
        "execute if score @s rpg_fo_mlv matches 3 run scoreboard players set #pc %s 40" % O,
        "scoreboard players operation #dmg %s *= #pc %s" % (O, O),
        "scoreboard players operation #dmg %s /= #100 %s" % (O, O),
        "scoreboard players set #hm %s 10" % O,
        "execute if score #dmg %s matches 1.. run function %s/hit" % (O, P),
    ])
    fn("sk/8/sum", ["scoreboard players operation #x %s += @s rpg_fo_dr" % O, "scoreboard players set @s rpg_fo_dr 0"])

    # ---------------------------------------------------------------- 圣力 · 中柱
    fn("sk/9/do", [
        "playsound minecraft:block.beacon.power_select player @a[distance=..24] ~ ~ ~ 1 1.6",
        "particle minecraft:end_rod ~ ~1 ~ 8 1.5 8 0 120",
        "execute as @e[type=!player,distance=..16] run effect clear @s minecraft:invisibility",
    ] + lv3([6, 8, 10], "effect give @e[" + ENEMY + ",distance=..16] minecraft:glowing %d 0 true") +
       lv3([6, 8, 10], "effect give @e[tag=rpg.vacant,distance=..16] minecraft:glowing %d 0 true"))

    ray("chain", 32, GOLD_DUST, ENEMY,
        lv3([2, 3, 4], "effect give @s minecraft:slowness %d 9 true") +
        lv3([2, 3, 4], "effect give @s minecraft:jump_boost %d 250 true") +
        lv3([2, 3, 4], "effect give @s minecraft:weakness %d 1 true") +
        ["particle minecraft:dust{color:[1.0,0.85,0.35],scale:1.2} ~ ~1 ~ 0.4 0.7 0.4 0 40",
         "playsound minecraft:block.chain.place hostile @a[distance=..16] ~ ~ ~ 1 0.6"])
    fn("sk/10/do", ["playsound minecraft:block.chain.break player @a[distance=..16] ~ ~ ~ 1 1.2", "function %s/ray/chain/go" % P])

    fn("sk/11/do", [
        "playsound minecraft:block.bell.resonate player @a[distance=..24] ~ ~ ~ 1 1.3",
        "particle minecraft:end_rod ~ ~1 ~ 4 0.6 4 0.02 80",
        "execute as @e[%s,distance=..8] at @s run function %s/sk/11/one" % (ENEMY, P),
    ])
    fn("sk/11/one", [
        "function %s/unholy" % P,
        "execute unless score #u %s matches 1 run return 0" % O,
        "scoreboard players set #b %s 0" % O,
    ] + ["execute if entity @s[tag=%s] run scoreboard players set #b %s 1" % (b, O) for b in BOSS_TAGS] + [
        "execute if score #b %s matches 1 run return run effect give @s minecraft:slowness 2 1 true" % O,
    ] + lv3([2, 3, 4], "effect give @s minecraft:slowness %d 9 true") +
        lv3([2, 3, 4], "effect give @s minecraft:jump_boost %d 250 true") +
        lv3([2, 3, 4], "effect give @s minecraft:weakness %d 4 true") +
        ["particle minecraft:wax_off ~ ~2 ~ 0.3 0.2 0.3 0 6"])

    fn("sk/12/do", [
        "playsound minecraft:entity.phantom.flap player @a[distance=..16] ~ ~ ~ 1 1.4",
        "playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 0.5 2",
        "particle minecraft:end_rod ~ ~0.5 ~ 0.6 0.2 0.6 0.05 30",
    ] + lv3([16, 20, 24], "scoreboard players set #r " + O + " %d") + [
        "execute rotated ~ -28 run function %s/blink/step" % P,
        "effect give @s minecraft:slow_falling 4 0 true",
    ])

    # ---------------------------------------------------------------- 魔力 · 严厉
    ray("dark", 40, MANA_LINE, ENEMY, [], on_end=[
        "particle minecraft:soul_fire_flame ~ ~0.5 ~ 1.2 0.6 1.2 0.05 60",
        "particle minecraft:large_smoke ~ ~0.5 ~ 1 0.4 1 0.02 20",
        "playsound minecraft:entity.blaze.shoot hostile @a[distance=..16] ~ ~ ~ 1 0.6",
    ] + lv3([50, 70, 90], "scoreboard players set #dmg " + O + " %d") + [
        "scoreboard players set #hm %s 10" % O,
        "execute as @e[%s,distance=..2.5] at @s run function %s/sk/3/one" % (ENEMY, P),
    ])
    fn("sk/13/do", ["playsound minecraft:entity.ghast.shoot player @a[distance=..16] ~ ~ ~ 0.6 0.7", "function %s/ray/dark/go" % P])

    fn("sk/14/do", [
        "scoreboard players operation @s rpg_fo_buf = #now %s" % O,
    ] + lv3([100, 120, 140], "scoreboard players add @s rpg_fo_buf %d") + [
        "scoreboard players set @s rpg_fo_bk 14",
        "scoreboard players operation @s rpg_fo_blv = #lv %s" % O,
        "scoreboard players set @s rpg_fo_dd 0",
        "playsound minecraft:entity.wither.ambient player @a[distance=..16] ~ ~ ~ 0.5 1.6",
        "particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.2} ~ ~1 ~ 0.3 0.6 0.3 0 40",
    ])
    fn("sk/14/proc", ["effect give @s minecraft:wither 3 1 true",
                      "particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.2} ~ ~1 ~ 0.3 0.5 0.3 0 12"])

    fn("sk/15/do", [
        "playsound minecraft:entity.skeleton.hurt player @a[distance=..16] ~ ~ ~ 1 0.5",
        "playsound minecraft:block.sculk.spread player @a[distance=..16] ~ ~ ~ 1 0.8",
        "particle minecraft:dust{color:[0.55,0.5,0.38],scale:1.4} ^ ^1 ^3 1.6 0.6 1.6 0 50",
        "particle minecraft:squid_ink ^ ^1 ^3 1.2 0.4 1.2 0.02 4",
        "execute positioned ^ ^ ^2 as @e[%s,distance=..2,tag=!rpg.fo.hit] at @s run function %s/sk/15/one" % (ENEMY, P),
        "execute positioned ^ ^ ^4.5 as @e[%s,distance=..2.5,tag=!rpg.fo.hit] at @s run function %s/sk/15/one" % (ENEMY, P),
        "tag @e[tag=rpg.fo.hit] remove rpg.fo.hit",
    ])
    fn("sk/15/one", [
        "tag @s add rpg.fo.hit",
        "attribute @s minecraft:armor modifier remove rpg:fo_rot",
    ] + lv3([-4, -6, -8], "attribute @s minecraft:armor modifier add rpg:fo_rot %d add_value") + [
        "tag @s add rpg.fo.timed",
        "scoreboard players operation @s rpg_fo_end = #now %s" % O,
        "scoreboard players add @s rpg_fo_end 120",
        "scoreboard players set #dmg %s 30" % O,
        "scoreboard players set #hm %s 10" % O,
        hit,
    ])

    ray("abyss", 40, "particle minecraft:reverse_portal ~ ~ ~ 0.02 0.02 0.02 0 1 force", ENEMY, [], on_end=["function %s/ground/abyss/go" % P])
    ground("abyss", [
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.fo.zone\",\"rpg.fo.znew\"]}",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_k 16",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_lv = #lv %s" % O,
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end = #now %s" % O,
        "scoreboard players add @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end 80",
        "tag @e[type=minecraft:marker,tag=rpg.fo.znew] remove rpg.fo.znew",
        "playsound minecraft:block.end_portal.spawn hostile @a[distance=..24] ~ ~ ~ 0.4 1.6",
    ])
    fn("sk/16/do", ["playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 1 0.5", "function %s/ray/abyss/go" % P])
    fn("zone/abyss", [
        "tp @s ~ ~ ~ ~-20 0",
        "particle minecraft:reverse_portal ^ ^0.1 ^2.5 0 0 0 0.02 3 force",
        "particle minecraft:reverse_portal ^ ^0.1 ^-2.5 0 0 0 0.02 3 force",
        "particle minecraft:squid_ink ~ ~0.1 ~ 0.6 0 0.6 0.01 2",
        "particle minecraft:sculk_soul ~ ~0.3 ~ 1.5 0.1 1.5 0.01 1",
        "execute as @e[%s,%s,distance=0.8..3.5] at @s facing entity @e[type=minecraft:marker,tag=rpg.fo.zone,limit=1,sort=nearest] feet run tp @s ^ ^ ^0.18" % (ENEMY, NOBOSS),
        "execute unless score #zt %s matches 0 run return 0" % O,
        "scoreboard players operation #zt %s = @s rpg_fo_end" % O,
        "scoreboard players operation #zt %s -= #now %s" % (O, O),
        "scoreboard players operation #zt %s %%= #20 %s" % (O, O),
        "execute unless score #zt %s matches 0 run return 0" % O,
    ] + lv3([20, 30, 40], "scoreboard players set #dmg " + O + " %d") + [
        "scoreboard players set #hm %s 10" % O,
        "execute as @e[%s,distance=..3.5] at @s run function %s/hit" % (ENEMY, P),
        "effect give @e[%s,distance=..3.5] minecraft:slowness 1 1 true" % ENEMY,
    ])

    # ---------------------------------------------------------------- 魔力 · 慈悲
    fn("sk/17/do", lv3([1, 2, 3], "effect give @s minecraft:absorption 20 %d true") + [
        "playsound minecraft:entity.slime.squish_small player @a[distance=..16] ~ ~ ~ 1 0.5",
        "playsound minecraft:item.armor.equip_netherite player @s ~ ~ ~ 1 0.6",
        "particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.3} ~ ~1 ~ 0.4 0.7 0.4 0 40"])

    ray("drain", 32, BLOOD_DUST, ENEMY,
        lv3([40, 60, 80], "scoreboard players set #dmg " + O + " %d") +
        ["scoreboard players set #hm %s 10" % O, hit,
         "particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.3} ~ ~1 ~ 0.3 0.5 0.3 0 20",
         "execute as @a[tag=rpg.fo.me,limit=1] at @s run function %s/sk/18/heal" % P])
    fn("sk/18/do", ["playsound minecraft:entity.warden.heartbeat player @a[distance=..16] ~ ~ ~ 1 1.4", "function %s/ray/drain/go" % P])
    fn("sk/18/heal", lv3([0, 0, 1], "effect give @s minecraft:instant_health 1 %d true") + [
        "execute if score #lv %s matches 2 run effect give @s minecraft:regeneration 3 1 true" % O,
        "particle minecraft:damage_indicator ~ ~1.5 ~ 0.3 0.3 0.3 0 4"])

    fn("sk/19/do", [
        "damage @s 6 rpg:force",
    ] + lv3([40, 50, 60], "execute if score @s rpg_force matches 2 run scoreboard players add @s rpg_mana %d") +
        lv3([40, 50, 60], "execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana2 %d") + [
        "playsound minecraft:entity.player.hurt_sweet_berry_bush player @s ~ ~ ~ 1 0.6",
        "playsound minecraft:block.respawn_anchor.charge player @a[distance=..16] ~ ~ ~ 0.6 0.6",
        "particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.5} ~ ~1 ~ 0.3 0.6 0.3 0 50",
        "particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.04 15"])

    fn("sk/20/check", [
        "# 不死（as 刚挨打的玩家；rpg:forge/hit/hurt_player 里调）",
        "execute unless score @s rpg_force matches 2..3 run return 0",
        "execute if score @s rpg_fo_und > #now %s run return 0" % O,
        "execute store result score #h %s run data get entity @s Health" % O,
        "execute unless score #h %s matches ..5 run return 0" % O,
        "effect give @s minecraft:resistance 3 4 true",
        "effect give @s minecraft:regeneration 3 2 true",
        "scoreboard players add @s rpg_taint 6",
        "scoreboard players operation @s rpg_fo_und = #now %s" % O,
        "execute if score @s %s matches 1 run scoreboard players add @s rpg_fo_und 3600" % kk(20),
        "execute if score @s %s matches 2 run scoreboard players add @s rpg_fo_und 3000" % kk(20),
        "execute if score @s %s matches 3 run scoreboard players add @s rpg_fo_und 2400" % kk(20),
        "playsound minecraft:item.totem.use player @a[distance=..16] ~ ~ ~ 0.5 0.6",
        "particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.05 40",
        say([t("不死：", C_MANA, True), t("你在致命的一击里撑住了。", C_BODY)]),
    ])

    # ---------------------------------------------------------------- 魔力 · 中柱
    fn("sk/21/do", [
        "playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 1 0.8",
        "particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 30",
    ] + lv3([16, 20, 24], "scoreboard players set #r " + O + " %d") + [
        "execute rotated ~ 0 run function %s/blink/step_m" % P,
        "effect give @s minecraft:invisibility 1 0 true",
        "execute at @s run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 30",
    ])

    fn("sk/22/do", [
        "playsound minecraft:entity.ravager.roar player @a[distance=..24] ~ ~ ~ 0.7 0.6",
        "particle minecraft:sculk_soul ~ ~1 ~ 3 0.5 3 0.02 50",
        "particle minecraft:squid_ink ~ ~0.3 ~ 2.5 0.1 2.5 0.02 6",
        "execute as @e[%s,%s,distance=..6] at @s run function %s/sk/22/one" % (ENEMY, NOBOSS, P),
    ])
    push = "execute at @s facing entity @a[tag=rpg.fo.me,limit=1] feet rotated ~ 0 if block ^ ^ ^-0.5 #rpg:force/pass if block ^ ^1 ^-0.5 #rpg:force/pass run tp @s ^ ^ ^-0.5"
    fn("sk/22/one", [push] * 6 + lv3([2, 3, 4], "effect give @s minecraft:weakness %d 1 true") +
       lv3([2, 3, 4], "effect give @s minecraft:slowness %d 1 true") +
       ["execute at @s run particle minecraft:smoke ~ ~1.8 ~ 0.2 0.2 0.2 0.02 8"])

    golem = ("summon minecraft:iron_golem ^ ^ ^2 {Tags:[\"rpg.fo.pup\",\"rpg.fo.timed\",\"rpg.fo.pnew\",\"rpg.ally\"],"
             "CustomName:{text:\"傀儡\",color:\"%s\",italic:false},CustomNameVisible:1b,PlayerCreated:1b,"
             "DeathLootTable:\"minecraft:empty\",Health:%df,attributes:[{id:\"minecraft:max_health\",base:%dd}]}")
    fn("sk/23/do", per_level([(i + 1, golem % (C_MANA, hp, hp)) for i, hp in enumerate((40, 60, 80))]) + [
        "scoreboard players operation @e[tag=rpg.fo.pnew] rpg_fo_end = #now %s" % O,
        "scoreboard players add @e[tag=rpg.fo.pnew] rpg_fo_end 400",
        "execute as @e[tag=rpg.fo.pnew] at @s run particle minecraft:soul ~ ~1 ~ 0.5 1 0.5 0.03 40",
        "tag @e[tag=rpg.fo.pnew] remove rpg.fo.pnew",
        "playsound minecraft:entity.zombie_villager.cure player @a[distance=..16] ~ ~ ~ 0.6 0.6",
    ])

    fn("sk/24/do", [
        "playsound minecraft:block.end_portal_frame.fill player @a[distance=..16] ~ ~ ~ 1 0.6",
        "particle minecraft:sculk_charge_pop ~ ~1 ~ 0.5 0.8 0.5 0.05 30",
        "tag @s add rpg.pact.cast",
    ] + ["execute if score @s rpg_pact matches %d run function rpg:pact/p%d" % (k, k) for k in range(1, 8)] + [
        "tag @s remove rpg.pact.cast",
    ])


# ============================================================================ 贴图特效
MV = "rpg:michael_vfx/"
PURPLE, VIOLET, BLOOD, BONE, GOLD = "#5B2A86", "#A276BE", "#8B0A1E", "#B8A88A", "#FFD85A"


def fx_engines():
    fade = dict(life=8, steps=[(4, 4, boss_fx.sc(0.01))])
    hk = {"fade": fade, "fadel": dict(life=16, steps=[(8, 8, boss_fx.sc(0.01))]),
          "burstf": dict(life=16, frames=("glyph", "burstf", 8, 2)),
          "eyeopen": dict(life=14, frames=("glyph", "eye", 6, 2)),
          "wings": dict(life=14, frames=("glyph", "wings", 6, 2)),
          "fburn": dict(life=12, frames=("glyph", "fburn", 6, 2)),
          "tongue": dict(life=16, frames=("glyph", "tongue", 8, 2)),
          "smoke": dict(life=12, frames=("glyph", "smoke", 6, 2)),
          "halo": dict(life=24, loop=("glyph", "halo", 6, 2)),
          "doverise": dict(life=40, loop=("glyph", "dove", 8, 2), steps=[(38, 36, "translation:[0f,6f,0f]")]),
          "mshock": dict(life=16, frames=("item", MV + "shock", 8, 2)),
          "mshockh": dict(life=16, frames=("item", MV + "shockh", 8, 2))}
    w = lambda pre: (lambda path, lines: fn(pre + "/" + path, lines))
    fxh = boss_fx.Fx(fn=P + "/h", tag="rpg.fo.hfx", life="rpg_fo_life", kind="rpg_fo_kd", writer=w("h"),
                     kinds=hk, arts=[(mart, mart.FONT)])
    fxm = boss_fx.Fx(fn=P + "/m", tag="rpg.fo.mfx", life="rpg_fo_life", kind="rpg_fo_kd", writer=w("m"),
                     kinds={"fade": fade})
    return fxh, fxm


def add_lines(name, lines, before=None):
    path = os.path.join(OUT, name + ".mcfunction")
    s = io.open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    if before:
        at = next(i for i, l in enumerate(s) if before in l)
        s[at:at] = lines
    else:
        s += lines
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(s) + "\n")


def vfx():
    h, m = fx_engines()
    hd = lambda name, size, kind=None, life=None, pos="~ ~0.06 ~": h.decal(MV + name, size, 0xFFFFFF, pos=pos, kind=kind, life=life)
    trail = lambda key, lines, steps: add_lines("ray/%s/step" % key, ["scoreboard players operation #rm %s = #r %s" % (O, O),
                                                                       "scoreboard players operation #rm %s %%= #4 %s" % (O, O)] +
                                                ["execute if score #rm %s matches 0 if score #r %s matches ..%d run %s" % (O, O, steps - 4, l)
                                                 for l in lines], before="positioned ^ ^ ^0.5")
    # 圣力 · 严厉
    trail("spear", h.glyph("star", 0.7, "white", kind="fade"), 40)
    add_lines("ray/spear/hit", h.glyph("burst", 1.8, "white", pos="~ ~1 ~", kind="burst"))
    add_lines("ray/mark/hit", h.glyph("eye", 1.6, "white", pos="~ ~2.7 ~", kind="eyeopen"))
    add_lines("sk/3/do", hd("shock_0", 11, kind="mshock") + hd("scorch", 7, life=60) +
              h.glyph("burstf", 3.0, "white", pos="^ ^0.8 ^2.2", kind="burstf"))
    add_lines("sk/4/do", h.glyph("tongue", 1.3, "white", pos="^-0.4 ^1.2 ^0.5", kind="tongue"))
    add_lines("sk/4/proc", h.glyph("fburn", 1.4, "white", pos="~ ~1 ~", kind="fburn"))
    # 圣力 · 慈悲
    add_lines("sk/5/heal", h.glyph("halo", 1.1, "white", pos="~ ~2.3 ~", kind="halo") +
              h.glyph("feather", 0.8, "white", pos="~0.4 ~1.6 ~", kind="fadel"))
    add_lines("sk/6/do", ["execute align y run " + l for l in hd("seal_seraph", 8, life=160, kind="spin")[:1]] +
              hd("seal_seraph", 8, life=160, kind="spin")[1:] + hd("ring_h", 8.6, life=160))
    add_lines("sk/7/do", hd("shockh_0", 12, kind="mshockh") + h.glyph("dove", 1.6, "white", pos="^ ^1.6 ^1.6", kind="doverise"))
    add_lines("sk/8/do", h.glyph("wings", 3.2, "white", pos="^ ^1.5 ^-0.7", kind="wings") + hd("ring_h", 16, life=200))
    # 圣力 · 中柱
    add_lines("sk/9/do", hd("shockh_0", 30, kind="mshockh") + h.glyph("eye", 2.2, "white", pos="^ ^2.8 ^2.5", kind="eyeopen"))
    add_lines("ray/chain/hit", hd("xmark", 2.2, life=60) + hd("ring_h", 2.6, life=60))
    add_lines("sk/11/do", hd("shockh_0", 16, kind="mshockh") + h.glyph("burst", 2.6, "white", pos="^ ^1.2 ^2", kind="burst"))
    add_lines("sk/11/one", h.glyph("ray", 1.4, "white", pos="~ ~1 ~", kind="fadel", billboard="vertical"),
              before="particle minecraft:wax_off")
    add_lines("sk/12/do", h.glyph("wings", 3.0, "white", pos="^ ^1.4 ^-0.7", kind="wings"), before="scoreboard players set #r")
    # 魔力 · 严厉
    trail("dark", m.spark("~ ~ ~", VIOLET), 40)
    add_lines("ray/dark/end", m.glyph("burst", 2.8, PURPLE, pos="~ ~ ~", kind="burst") + ["function %s/ground/dark/go" % P])
    ground("dark", m.decal("cracks", 4, 0x3A1F4F, life=60))
    add_lines("sk/14/do", m.slash("^ ^1.2 ^1.2", BLOOD, size=1.8))
    add_lines("sk/14/proc", m.slash("~ ~1 ~", BLOOD, size=1.6))
    add_lines("sk/15/do", m.slash("^ ^1.2 ^3", BONE, size=3.2) + m.decal("cracks", 5, 0x4A3F2A, pos="^ ^0.06 ^3", life=60))
    add_lines("ground/abyss/at", m.decal("swirl", 6, 0x3B1458, kind="spin", life=80) +
              m.decal("hexagram", 7.5, 0xA276BE, pos="~ ~0.08 ~", kind="spinr", life=80))
    # 魔力 · 慈悲
    add_lines("sk/17/do", m.glyph("burst", 1.8, BLOOD, pos="^ ^1 ^1.4", kind="burst") + m.decal("hexagon", 2.6, 0x8B0A1E, life=30))
    trail("drain", m.spark("~ ~ ~", "#C0303C"), 32)
    add_lines("ray/drain/hit", m.glyph("burst", 1.6, BLOOD, pos="~ ~1 ~", kind="burst"))
    add_lines("sk/19/do", m.decal("sigil", 3.2, 0x8B0A1E, life=30) + m.glyph("burst", 1.8, BLOOD, pos="^ ^1 ^1.4", kind="burst"))
    # 魔力 · 中柱
    add_lines("sk/21/do", h.glyph("smoke", 2.2, "white", pos="~ ~1 ~", kind="smoke"), before="scoreboard players set #r")
    add_lines("sk/21/do", ["execute at @s run " + l for l in h.glyph("smoke", 2.2, "white", pos="^ ^1 ^-1", kind="smoke")])
    add_lines("sk/22/do", m.decal("shock_0", 12, 0x5B2A86, kind="shock") + m.glyph("burst", 2.4, PURPLE, pos="^ ^1.2 ^2", kind="burst"))
    add_lines("sk/23/do", ["execute positioned ^ ^ ^2 run " + l for l in m.decal("hexagon", 3, 0xA276BE, life=40)[:1]] +
              m.decal("hexagon", 3, 0xA276BE, life=40)[1:] +
              ["execute positioned ^ ^ ^2 run " + l for l in m.ray("~ ~ ~", VIOLET)[:1]] + m.ray("~ ~ ~", VIOLET)[1:])
    add_lines("sk/24/do", m.decal("sigil", 4, 0xA276BE, life=30) + m.glyph("burst", 2.0, VIOLET, pos="^ ^1.2 ^1.6", kind="burst"))
    h.build()
    m.build()


# ============================================================================ 技能页、学习、槽位、洗点
def page_no(tr, br):
    return (tr - 1) * 3 + br


def branch_skills(tr, br):
    return [s for s in SKILLS if s[1] == tr and s[2] == br]


def cost_text(s):
    n, tr, br, name, desc, fc, xc, cd, passive = s
    j = lambda v: "/".join(str(x) for x in v)
    if passive:
        return "冷却 %s 秒 · 魔化 +%s" % (j(cd), j(xc))
    extra = ("生命力 %s" % j(xc)) if tr == 1 else ("魔化 +%s" % j(xc))
    return "力 %s · %s · 冷却 %s 秒" % (j(fc), extra, j(cd))


def trig(v):
    return {"type": "minecraft:run_command", "command": "/trigger %s set %d" % (DO, v)}


def pages():
    # 填页面要的数据
    fill = ["# 技能页数据（as 玩家）→ storage rpg:force p",
            "data modify storage rpg:force p set value {}",
            "scoreboard players add @s rpg_sp 0",
            "execute store result storage rpg:force p.sp int 1 run scoreboard players get @s rpg_sp"]
    for n, tr, br, name, desc, fc, xc, cd, passive in SKILLS:
        fill.append("scoreboard players add @s %s 0" % kk(n))
        fill.append("execute store result storage rpg:force p.l%02d int 1 run scoreboard players get @s %s" % (n, kk(n)))
        fill.append("data modify storage rpg:force p.c%02d set value \"%s\"" % (n, C_LOCK))
        prev = [s for s in branch_skills(tr, br) if s[0] < n]
        cond = ("if score @s %s matches 1.. " % kk(prev[-1][0])) if prev else ""
        forces = (1, 3) if tr == 1 else (2, 3)
        for f in forces:
            fill.append("execute if score @s rpg_force matches %d %srun data modify storage rpg:force p.c%02d set value \"%s\"" % (f, cond, n, C_BODY))
        fill.append("execute if score @s %s matches 1.. run data modify storage rpg:force p.c%02d set value \"%s\"" % (kk(n), n, TREES[tr][1]))
    fill.append("function %s/x/page/fill" % P)
    for tr in (1, 2):
        for s in (1, 2, 3):
            key = "%s%d" % ("h" if tr == 1 else "m", s)
            fill.append("data modify storage rpg:force p.%s set value \"—\"" % key)
            for e in EXTRA:
                if e[1] == "l" or e[1] == ("h" if tr == 1 else "m"):
                    fill.append("execute if score @s %s matches %d run data modify storage rpg:force p.%s set from storage rpg:force p.n%d" % (slot_obj(tr, s), e[0], key, e[0]))
            for sk in SKILLS:
                if sk[1] == tr and not sk[8]:
                    fill.append("execute if score @s %s matches %d run data modify storage rpg:force p.%s set value \"%s\"" % (slot_obj(tr, s), sk[0], key, sk[3]))
    fn("page/fill", fill)
    fn("page/show", ["function %s/page/fill" % P] +
       ["execute if score @s rpg_fo_pg matches %d run return run function %s/page/p%d with storage rpg:force p" % (k, P, k) for k in range(1, 9)] +
       ["function %s/page/p1 with storage rpg:force p" % P])
    fn("page/by_tree", [
        "# 从圣徽 / 罪印打开：翻到那棵树（已经在那棵树上就留在原来那一支）",
        "execute if score #tree %s matches 1 unless score @s rpg_fo_pg matches 1..3 run scoreboard players set @s rpg_fo_pg 1" % O,
        "execute if score #tree %s matches 2 unless score @s rpg_fo_pg matches 4..6 run scoreboard players set @s rpg_fo_pg 4" % O,
        "function %s/page/show" % P,
    ])
    fn("page/default", [
        "# 从原质页打开：魔力者翻到魔力树",
        "execute unless score @s rpg_fo_pg matches 1..6 run scoreboard players set @s rpg_fo_pg 1",
        "execute if score @s rpg_force matches 2 unless score @s rpg_fo_pg matches 4..6 run scoreboard players set @s rpg_fo_pg 4",
        "function %s/page/show" % P,
    ])
    for tr in (1, 2):
        tname, tcol, item = TREES[tr]
        for br in (1, 2, 3):
            bname, bsub, bcol = BRANCH[tr][br]
            sk = branch_skills(tr, br)
            sl = "h" if tr == 1 else "m"
            body = [t("技能点 ", C_MUTED), t("$(sp)", C_GOLD, True),
                    t("　　槽位　Ⅰ ", C_MUTED), t("$(%s1)" % sl, tcol), t("　Ⅱ ", C_MUTED), t("$(%s2)" % sl, tcol),
                    t("　Ⅲ ", C_MUTED), t("$(%s3)" % sl, tcol), NL,
                    t("点技能名学习或升级，点 Ⅰ Ⅱ Ⅲ 放进槽。同一支按顺序学；2 级要美丽阶，3 级要理解阶。", "#797979"), NL]
            actions = []
            for s in sk:
                n, _tr, _br, name, desc, fc, xc, cd, passive = s
                body += [NL, {"text": name, "color": "$(c%02d)" % n, "bold": True, "italic": False},
                         t("  $(l%02d)/3" % n, C_MUTED), t("　被动" if passive else "", "#797979"), NL,
                         t(desc, C_BODY), NL, t(cost_text(s), "#797979"), NL]
                tip = ["", t(name, tcol, True), t("\n" + desc, C_BODY), t("\n" + cost_text(s), C_MUTED),
                       t("\n价格 1 / 1 / 2 点（主柱那一支的 3 级只要 1 点）", "#797979")]
                actions.append({"label": {"text": "%s $(l%02d)/3 ＋" % (name, n), "color": "$(c%02d)" % n, "bold": True, "italic": False},
                                "tooltip": tip, "width": 150, "action": trig(100 + n)})
                for slot in (1, 2, 3):
                    actions.append({"label": t("·" if passive else ROMAN[slot], C_MUTED if passive else tcol, True),
                                    "tooltip": t("被动，不用放进槽" if passive else "放进 %s 号槽" % ROMAN[slot], C_MUTED),
                                    "width": 74, "action": trig(1000 + n * 10 + slot)})
            for b2 in (1, 2, 3):
                nm, sub, col = BRANCH[tr][b2]
                actions.append({"label": t(("◆ " if b2 == br else "") + nm, col, True), "tooltip": t(sub, C_MUTED),
                                "width": 150 if b2 == 1 else 74, "action": trig(page_no(tr, b2))})
            other = 3 - tr
            actions.append({"label": t(TREES[other][0] + "树", TREES[other][1], True), "width": 74, "action": trig(page_no(other, 1))})
            actions.append({"label": t("洗点", "#797979", True), "width": 150,
                            "tooltip": t("站在点燃的灵魂营火旁，花 5 个残魂，退回两棵树的全部技能点", C_MUTED), "action": trig(7)})
            actions.append({"label": t("补领" + item, tcol, True), "width": 74, "action": trig(80 + tr)})
            actions.append({"label": t("返回原质", C_GOLD, True), "width": 74,
                            "action": {"type": "minecraft:run_command", "command": "/trigger rpg_sef_do set 20"}})
            actions.append({"label": t("王冠 · 传承", C_GOLD, True), "width": 74,
                            "tooltip": t("王冠阶的终式与 Boss 传承技", C_MUTED), "action": trig(10 + tr)})
            doc = {"type": "minecraft:multi_action",
                   "title": ["", t("技能 · ", C_MUTED), t(tname, tcol, True), t(" · ", C_MUTED), t(bname, bcol, True),
                             t("（%s）" % bsub, C_MUTED)],
                   "body": {"type": "minecraft:plain_message", "width": 330, "contents": [""] + body},
                   "actions": actions, "columns": 4, "can_close_with_escape": True, "pause": False,
                   "after_action": "close", "exit_action": {"label": t("合上", C_MUTED)}}
            fn("page/p%d" % page_no(tr, br), ["$dialog show @s " + J(doc)])

    # 按钮
    press = ["scoreboard players operation #do %s = @s %s" % (O, DO),
             "scoreboard players set @s %s 0" % DO,
             "scoreboard players enable @s %s" % DO,
             "execute if score #do %s matches 1..6 run scoreboard players operation @s rpg_fo_pg = #do %s" % (O, O),
             "execute if score #do %s matches 1..6 run return run function %s/page/show" % (O, P),
             "execute if score #do %s matches 9 run return run function %s/page/default" % (O, P),
             "execute if score #do %s matches 11 run scoreboard players set @s rpg_fo_pg 7" % O,
             "execute if score #do %s matches 12 run scoreboard players set @s rpg_fo_pg 8" % O,
             "execute if score #do %s matches 11..12 run return run function %s/page/show" % (O, P),
             "execute if score #do %s matches 2000.. run function %s/x/press" % (O, P),
             "execute if score #do %s matches 7 run function %s/wash" % (O, P),
             "execute if score #do %s matches 81 run function %s/give/reissue_1" % (O, P),
             "execute if score #do %s matches 82 run function %s/give/reissue_2" % (O, P)]
    for n in SK:
        press.append("execute if score #do %s matches %d run function %s/learn/%d" % (O, 100 + n, P, n))
        for s in (1, 2, 3):
            press.append("execute if score #do %s matches %d run function %s/slot/%d_%d" % (O, 1000 + n * 10 + s, P, n, s))
    press.append("function %s/page/show" % P)
    fn("press", press)

    for n, tr, br, name, desc, fc, xc, cd, passive in SKILLS:
        tname, tcol, item = TREES[tr]
        prev = [s for s in branch_skills(tr, br) if s[0] < n]
        spent = "rpg_fo_sh" if tr == 1 else "rpg_fo_sm"
        L = ["# 学习 / 升级 %s" % name,
             "execute %s run return run function %s/fail/say {m:\"你没有%s，学不了%s树\"}" % (tree_ok(tr), P, tname, tname)]
        if prev:
            L.append("execute unless score @s %s matches 1.. run return run function %s/fail/say {m:\"先学会「%s」\"}" % (kk(prev[-1][0]), P, prev[-1][3]))
        L += [
            "execute if score @s %s matches 3.. run return run function %s/fail/say {m:\"「%s」已经满级\"}" % (kk(n), P, name),
            "execute if score @s %s matches 1 unless score @s rpg_sef matches 5.. run return run function %s/fail/say {m:\"2 级要到美丽阶（第 5 阶）\"}" % (kk(n), P),
            "execute if score @s %s matches 2 unless score @s rpg_sef matches 8.. run return run function %s/fail/say {m:\"3 级要到理解阶（第 8 阶）\"}" % (kk(n), P),
            "scoreboard players set #c %s 1" % O,
            "execute if score @s %s matches 2 run scoreboard players set #c %s 2" % (kk(n), O),
            "execute if score @s %s matches 2 if score @s rpg_pillar matches %d run scoreboard players set #c %s 1" % (kk(n), br, O),
            "execute unless score @s rpg_sp >= #c %s run return run function %s/fail/say {m:\"技能点不够\"}" % (O, P),
            "scoreboard players operation @s rpg_sp -= #c %s" % O,
            "scoreboard players operation @s %s += #c %s" % (spent, O),
            "scoreboard players add @s %s 1" % kk(n),
        ]
        if not passive:
            L.append("execute if score @s %s matches 1 run function %s/slot/auto_%d" % (kk(n), P, n))
        L += ["playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 1.2",
              "tellraw @s " + J(["", t("[力] ", C_GOLD, True), t(name, tcol, True), t(" 升到 ", C_MUTED),
                                 {"score": {"name": "@s", "objective": kk(n)}, "color": C_BODY}, t(" 级", C_MUTED)])]
        fn("learn/%d" % n, L)
        if passive:
            for s in (1, 2, 3):
                fn("slot/%d_%d" % (n, s), ["function %s/fail/say {m:\"%s是被动，学会就生效\"}" % (P, name)])
            continue
        fn("slot/auto_%d" % n, ["execute unless score @s %s matches 1.. run return run scoreboard players set @s %s %d" % (slot_obj(tr, s), slot_obj(tr, s), n)
                                for s in (1, 2, 3)])
        for s in (1, 2, 3):
            fn("slot/%d_%d" % (n, s), [
                "execute unless score @s %s matches 1.. run return run function %s/fail/say {m:\"先学会「%s」\"}" % (kk(n), P, name)] +
                ["execute if score @s %s matches %d run scoreboard players set @s %s 0" % (slot_obj(tr, s2), n, slot_obj(tr, s2)) for s2 in (1, 2, 3) if s2 != s] +
                ["scoreboard players set @s %s %d" % (slot_obj(tr, s), n),
                 "playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4"])

    for tr in (1, 2):
        spent = "rpg_fo_sh" if tr == 1 else "rpg_fo_sm"
        tname, tcol, item = TREES[tr]
        fn("refund_%s" % ("h" if tr == 1 else "m"), [
            "# 退回%s树的全部技能点" % tname,
            "scoreboard players add @s %s 0" % spent,
            "execute if score @s %s matches 1.. run %s" % (spent, say([t("%s树的技能点退回 " % tname, C_MUTED),
                                                                     {"score": {"name": "@s", "objective": spent}, "color": C_GOLD}])),
            "scoreboard players operation @s rpg_sp += @s %s" % spent,
            "scoreboard players set @s %s 0" % spent,
        ] + ["scoreboard players set @s %s 0" % kk(s[0]) for s in SKILLS if s[1] == tr] +
            ["scoreboard players set @s %s 0" % slot_obj(tr, s) for s in (1, 2, 3)])
    near = []
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            for dy in (0, -1):
                pos = "~%s ~%s ~%s" % (dx or "", dy or "", dz or "")
                near.append("execute if block %s minecraft:soul_campfire[lit=true] run return run scoreboard players set #ok %s 1" % (pos, O))
    fn("wash/near", near)
    fn("wash", [
        "scoreboard players set #ok %s 0" % O,
        "function %s/wash/near" % P,
        "execute unless score #ok %s matches 1 run return run function %s/fail/say {m:\"洗点要站在点燃的灵魂营火旁\"}" % (O, P),
        "execute store result score #n %s run clear @s *[minecraft:custom_data~{rpg_mat:\"soul\"}] 0" % O,
        "execute unless score #n %s matches 5.. run return run function %s/fail/say {m:\"洗点要 5 个残魂\"}" % (O, P),
        "clear @s *[minecraft:custom_data~{rpg_mat:\"soul\"}] 5",
        "function %s/refund_h" % P,
        "function %s/refund_m" % P,
        "playsound minecraft:block.soul_sand.break player @s ~ ~ ~ 1 0.6",
        "particle minecraft:soul ~ ~1 ~ 0.4 0.6 0.4 0.03 30",
        say([t("洗点完成：花了 5 个残魂，两棵树的点都退回了。", C_BODY)]),
    ])


# ============================================================================ 管理员
def admin():
    fn("admin/sp", ["scoreboard players add @s rpg_sp 10", say([t("技能点 +10（管理员）", C_MUTED)])])
    fn("admin/full", ["# 力条加满、冷却清空", "scoreboard players operation @s rpg_mana = @s rpg_mana_max",
                      "scoreboard players operation @s rpg_mana2 = @s rpg_mana_max"] +
       ["scoreboard players set @s %s 0" % kc(n) for n in list(SK) + list(EX)] +
       ["scoreboard players set @s rpg_fo_und 0", "scoreboard players set @s rpg_fo_3d 0"])
    fn("admin/give", ["give @s %s" % sigil_item(1), "give @s %s" % sigil_item(2)])
    fn("admin/reset", ["function %s/refund_h" % P, "function %s/refund_m" % P,
                       "tag @s remove rpg.fo.g1", "tag @s remove rpg.fo.g2"])


# ============================================================================ 接到别的模块上
def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)


def tag_add(kind, name, value):
    path = os.path.join(DP, "data", "minecraft", "tags", kind, name + ".json")
    doc = {"replace": False, "values": []}
    if os.path.exists(path):
        doc = json.load(io.open(path, encoding="utf-8"))
    if value not in doc["values"]:
        doc["values"].append(value)
    wj(path, doc)


def wire():
    hook_tag(DP, "load", P + "/load", False)
    hook_tag(DP, "tick", P + "/tick", True)
    d = os.path.join(DP, "data", "rpg")
    wj(os.path.join(d, "advancement", "force", "use.json"), {
        "criteria": {"requirement": {"trigger": "minecraft:using_item", "conditions": {
            "item": {"predicates": {"minecraft:custom_data": "{rpg_sigil_tag:1b}"}}}}},
        "rewards": {"function": P + "/use"}})
    wj(os.path.join(d, "tags", "block", "force", "pass.json"), {"values": [
        "#minecraft:replaceable", "#minecraft:flowers", "#minecraft:saplings", "minecraft:torch", "minecraft:wall_torch",
        "minecraft:soul_torch", "minecraft:soul_wall_torch", "minecraft:redstone_wire", "minecraft:rail",
        "minecraft:tripwire", "minecraft:sugar_cane", "minecraft:pink_petals", "minecraft:moss_carpet"]})
    wj(os.path.join(d, "damage_type", "force.json"), {"message_id": "magic", "scaling": "never", "exhaustion": 0.0})
    for tg in ("bypasses_cooldown", "bypasses_armor", "no_knockback"):
        tag_add("damage_type", tg, "rpg:force")
    patch("forge/hit/hurt_player.mcfunction", "rpg:force/sk/20/check",
          "execute if score @s %s matches 1.. run function rpg:force/sk/20/check\n" % kk(20), "end")
    patch("sephira/force/fall.mcfunction", "rpg:force/refund_h", "function rpg:force/refund_h\n", "end")
    patch("sephira/force/rise.mcfunction", "rpg:force/refund_m", "function rpg:force/refund_m\n", "end")
    # 原质页加「技能」按钮（放在「返回面板」之前）
    s = read("sephira/page/open.mcfunction")
    if "rpg_fo_do set 9" not in s:
        lines = s.split("\n")
        at = next(i for i, l in enumerate(lines) if "返回面板" in l and "ui.actions append" in l)
        btn = {"label": t("技能", C_HOLY, True), "action": {"type": "minecraft:run_command", "command": "/trigger %s set 9" % DO}}
        lines.insert(at, "execute if score @s rpg_force matches 1.. run data modify storage rpg:panel ui.actions append value " + J(btn))
        write("sephira/page/open.mcfunction", "\n".join(lines))


def validate():
    for k in range(1, 7):
        body = io.open(os.path.join(OUT, "page", "p%d.mcfunction" % k), encoding="utf-8").read()
        assert body.startswith("$dialog show @s "), k
        doc = json.loads(body[len("$dialog show @s "):].strip())
        assert len(doc["actions"]) == 24, (k, len(doc["actions"]))
    for n in SK:
        assert os.path.exists(os.path.join(OUT, "sk", "%d" % n, "try.mcfunction")), n
        if not SK[n][8]:
            assert os.path.exists(os.path.join(OUT, "sk", "%d" % n, "do.mcfunction")), n
    assert "rpg:force/sk/20/check" in read("forge/hit/hurt_player.mcfunction")
    assert "rpg_fo_do set 9" in read("sephira/page/open.mcfunction")


def main():
    import shutil
    shutil.rmtree(OUT, ignore_errors=True)
    core()
    cast()
    helpers()
    blink()
    skills()
    vfx()
    pages()
    admin()
    wire()
    import force_ext
    force_ext.run(sys.modules[__name__])
    validate()
    print("force: %d functions, %d skills" % (COUNT, len(SKILLS)))


if __name__ == "__main__":
    main()
