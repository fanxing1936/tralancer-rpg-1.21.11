# -*- coding: utf-8 -*-
"""驱魔体系：魔化值、统一 HUD、空缺者、驱魔仪式。

三件事互相咬合：

* **魔化值** 让包里那条早就存在却只驱动粒子的圣/魔轴（`holy_weapon_tag` /
  `devil_weapon_tag`）第一次有了长期后果 —— 握着魔器会慢慢变成它的主人。
* **空缺者** 给驱魔一个可驱之物：外表与常人无异的空壳，只有持圣器时才显形。
* **驱魔仪式** 是处置手段，也是唯一能把魔化值压下去的办法。

HUD 是这一版的架构重点。屏幕下方那条 actionbar 全局只有一份，
原本利维坦、熔火之锤、藤蔓之鞭各自直接往上写，谁最后写谁赢 —— 会互相打架。
现在改成**唯一出口**：技能只更新自己的分数并挂一个短时效的占用声明，
`rpg:hud/hud` 每刻按优先级挑一条渲染。蓄力条永远压过魔化条，
蓄力一结束魔化条自己回来。
"""

import io
import json
import os
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement/item")
GIVE = os.path.join(FUNC, "command/give/item.mcfunction")

TAINT_MAX = 100
SEGMENTS = 10            # 魔化条的格数
HUD_TTL = 3              # 技能占用 HUD 的时效（刻）

# HUD 占用编号
HUD_ANCHOR, HUD_FORGE, HUD_VINE = 1, 2, 3

OBJECTIVES = ["rpg_taint", "rpg_hud", "rpg_hud_p", "rpg_hud_t",
              "rpg_taint_t", "rpg_vac", "rpg_rite"]

RULE = '["",{"text":"+------------------+","italic":false,"color":"white"}]'


def seg(t, c="white", b=False):
    return '{"text":"%s","italic":false,"color":"%s"%s}' % (t, c, ',"bold":true' if b else "")


def row(*s):
    return '["",%s]' % ",".join(s)


def wf(rel, text):
    p = os.path.join(FUNC, rel)
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text.rstrip("\n") + "\n")


def wj(p, doc):
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


# ---------------------------------------------------------------------------
# HUD：屏幕下方唯一的一条 actionbar
# ---------------------------------------------------------------------------
def bar(filled, total, on_colour, off_colour="dark_gray"):
    """▰ 已填 / ▱ 未填，两段拼一条。"""
    parts = []
    if filled:
        parts.append(seg("▰" * filled, on_colour))
    if total - filled:
        parts.append(seg("▱" * (total - filled), off_colour))
    return parts


TAINT_TIERS = [
    (0, 30, "gray", "尚可自持"),
    (31, 60, "dark_purple", "侵蚀渐深"),
    (61, 90, "red", "近乎失守"),
    (91, TAINT_MAX, "dark_red", "濒临魔化"),
]


def build_hud():
    """屏幕下方唯一的 actionbar 出口。

    渲染一条进度条要按格数分支，全摊在一个函数里就是一百多条命令，
    而它每刻、每个玩家都要过一遍 —— 空闲时全部落空，纯属浪费。
    所以拆成一层调度 + 每种条各自一个函数：空闲一刻只评估四条落空的判定
    加一次递减，真正的分支只在该显示的时候才进去。
    """
    skills = [(HUD_ANCHOR, "沉　锚", "dark_aqua", "aqua"),
              (HUD_FORGE, "熔　流", "gold", "yellow"),
              (HUD_VINE, "缠　绕", "dark_green", "green")]

    # ---- 调度层 ----
    top = ["# 屏幕下方唯一的 actionbar 出口。技能不再各写各的 —— 它们只更新",
           "# rpg_hud / rpg_hud_p 并把 rpg_hud_t 顶到 %d，这里按优先级挑一条渲染。" % HUD_TTL,
           "# 蓄力条永远压过魔化条；蓄力一结束，魔化条自己就回来了。",
           ""]
    for hid, label, _dim, _lit in skills:
        top.append("execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=%d}] "
                   "run function rpg:hud/s%d" % (hid, hid))
    top += ["",
            "# 没有技能占用、且确实有魔化时，才轮到魔化条",
            "execute if entity @s[scores={rpg_hud_t=..0,rpg_taint=1..}] run function rpg:hud/taint",
            "",
            "execute if entity @s[scores={rpg_hud_t=1..}] run scoreboard players remove @s rpg_hud_t 1"]
    wf("hud/hud.mcfunction", "\n".join(top))

    total = len(top)

    # ---- 每个技能一条 ----
    for hid, label, dim, lit in skills:
        body = ["# %s 的蓄力条，%d 格。" % (label.replace("　", ""), SEGMENTS)]
        for n in range(SEGMENTS + 1):
            comp = row(seg(label + " ", dim), *bar(n, SEGMENTS, lit),
                       seg("  %d%%" % (n * 100 // SEGMENTS), "gray"))
            body.append("execute if entity @s[scores={rpg_hud_p=%d}] run title @s actionbar %s"
                        % (n, comp))
        wf("hud/s%d.mcfunction" % hid, "\n".join(body))
        total += len(body)

    # ---- 魔化条：先按档分流，再按格渲染 ----
    disp = ["# 先把魔化换算成格数，再按档分流 —— 每档的颜色与措辞不同。",
            "scoreboard players operation @s rpg_hud_p = @s rpg_taint",
            "scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud",
            "scoreboard players operation @s rpg_hud_p /= #taint_max rpg_hud",
            ""]
    for i, (lo, hi, colour, word) in enumerate(TAINT_TIERS, 1):
        disp.append("execute if entity @s[scores={rpg_taint=%d..%d}] run function rpg:hud/t%d"
                    % (max(lo, 1), hi, i))
    wf("hud/taint.mcfunction", "\n".join(disp))
    total += len(disp)

    for i, (_lo, _hi, colour, word) in enumerate(TAINT_TIERS, 1):
        body = ["# 魔化条 · %s" % word]
        for n in range(SEGMENTS + 1):
            comp = row(seg("魔化 ", "dark_gray"), *bar(n, SEGMENTS, colour),
                       seg("  " + word, colour))
            body.append("execute if entity @s[scores={rpg_hud_p=%d}] run title @s actionbar %s"
                        % (n, comp))
        wf("hud/t%d.mcfunction" % i, "\n".join(body))
        total += len(body)

    return total


# ---------------------------------------------------------------------------
# 魔化值
# ---------------------------------------------------------------------------
TAINT = """\
# 魔化：握着魔器慢慢沾染，握着圣器慢慢洗去。
# 每 40 刻结算一次 —— 逐刻结算既没必要也白费开销。
scoreboard players add @s rpg_taint_t 1
execute if entity @s[scores={{rpg_taint_t=40..}}] run function rpg:taint/step
"""

TAINT_STEP = """\
# 一次结算。魔器加、圣器减，两者都握着时互相抵消。
scoreboard players set @s rpg_taint_t 0
execute if entity @s[tag=rpg.h.devil_tag1] run scoreboard players add @s rpg_taint 2
execute if entity @s[tag=rpg.h.devil_weapon_tag1] run scoreboard players add @s rpg_taint 1
execute if entity @s[tag=rpg.h.holy_weapon_tag1] run scoreboard players remove @s rpg_taint 1
execute if entity @s[scores={{rpg_taint={MAXP}..}}] run scoreboard players set @s rpg_taint {MAX}
execute if entity @s[scores={{rpg_taint=..-1}}] run scoreboard players set @s rpg_taint 0

# 分档外显。低档只是身上泛起暗纹，越深越明显。
execute if entity @s[scores={{rpg_taint=31..60}}] at @s run particle dust{{color:[0.32,0.16,0.42],scale:1}} ~ ~1 ~ 0.35 0.6 0.35 0.01 4
execute if entity @s[scores={{rpg_taint=61..90}}] at @s run particle dust{{color:[0.45,0.10,0.14],scale:2}} ~ ~1 ~ 0.4 0.7 0.4 0.02 8
execute if entity @s[scores={{rpg_taint=61..90}}] at @s run particle sculk_soul ~ ~1.2 ~ 0.3 0.5 0.3 0.01 2

# 濒临魔化：力量上来了，但圣性之物开始灼手，也更怕魔法伤害。
execute if entity @s[scores={{rpg_taint=91..}}] run effect give @s minecraft:strength 3 0 true
execute if entity @s[scores={{rpg_taint=91..}}] at @s run particle soul_fire_flame ~ ~1 ~ 0.4 0.7 0.4 0.01 6
execute if entity @s[scores={{rpg_taint=91..}},tag=rpg.h.holy_weapon_tag1] run damage @s 2 minecraft:magic
execute if entity @s[scores={{rpg_taint=91..}},tag=rpg.h.holy_weapon_tag1] run playsound minecraft:block.lava.extinguish player @s ~ ~ ~ 1 1.6
"""


# ---------------------------------------------------------------------------
# 空缺者
# ---------------------------------------------------------------------------
VACANT_MARK = """\
# 空缺者：外表与常人无异的空壳。
# 新出现的村民里抽一部分标记，每刻只处理少量，避免村庄载入时集中掷点。
tag @e[type=minecraft:villager,tag=!rpg.vac.seen,limit=3] add rpg.vac.new
execute as @e[tag=rpg.vac.new] store result score @s rpg_vac run random value 1..6
execute as @e[tag=rpg.vac.new,scores={rpg_vac=1}] run tag @s add rpg.vacant
tag @e[tag=rpg.vac.new] add rpg.vac.seen
tag @e[tag=rpg.vac.new] remove rpg.vac.new
"""

VACANT = """\
# 空缺者的显形与代价。
# 只有附近有人持圣器时才现形 —— 平时它和普通村民毫无分别。
execute as @e[type=minecraft:villager,tag=rpg.vacant] at @s if entity @a[tag=rpg.h.holy_weapon_tag1,distance=..16] run effect give @s minecraft:glowing 2 0 true
execute as @e[type=minecraft:villager,tag=rpg.vacant] at @s if entity @a[tag=rpg.h.holy_weapon_tag1,distance=..16] run particle sculk_soul ~ ~1.4 ~ 0.2 0.3 0.2 0.01 2

# 杀掉空缺者不算驱魔 —— 罪落在动手的人身上。
execute as @e[type=minecraft:villager,tag=rpg.vacant,tag=rpg.hurt] at @s on attacker run scoreboard players add @s rpg_taint 6
execute as @e[type=minecraft:villager,tag=rpg.vacant,tag=rpg.hurt] at @s on attacker run title @s actionbar ["",{"text":"你打碎的只是空壳","italic":true,"color":"dark_gray"}]
"""


# ---------------------------------------------------------------------------
# 驱魔仪式
# ---------------------------------------------------------------------------
RITE_TRIGGER = """\
# 驱魔仪式 —— 由 rpg:item/rite 在「以圣水右击灵魂灯笼」时触发。
# 阵型：以被点的灵魂灯笼为心，四正方向各三格处再各有一盏。
advancement revoke @s only rpg:item/rite
execute if entity @s[scores={rpg_rite=1..}] run return 0
execute at @s run function rpg:rite/check
"""

RITE_CHECK = """\
# 验阵。四盏都在才算数，缺一不成。
scoreboard players set @s rpg_rite 60
execute unless block ~3 ~ ~ minecraft:soul_lantern run function rpg:rite/fail
execute unless block ~-3 ~ ~ minecraft:soul_lantern run function rpg:rite/fail
execute unless block ~ ~ ~3 minecraft:soul_lantern run function rpg:rite/fail
execute unless block ~ ~ ~-3 minecraft:soul_lantern run function rpg:rite/fail
execute if block ~3 ~ ~ minecraft:soul_lantern if block ~-3 ~ ~ minecraft:soul_lantern if block ~ ~ ~3 minecraft:soul_lantern if block ~ ~ ~-3 minecraft:soul_lantern run function rpg:rite/purge
"""

RITE_FAIL = """\
particle smoke ~ ~1 ~ 0.3 0.3 0.3 0.02 12
playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 0.8
title @s actionbar ["",{"text":"阵不成 ","color":"dark_gray"},{"text":"四方各三格需各置一盏灵魂灯笼","color":"gray","italic":true}]
"""

RITE_PURGE = """\
# 净化。圣光沿四方连线走一圈，然后收束到阵心。
particle end_rod ~ ~0.3 ~ 3 0.1 3 0.02 90
particle dust{color:[1.0,0.98,0.86],scale:2} ~ ~1 ~ 2.6 0.6 2.6 0.04 120
particle minecraft:flash{color:16777200} ~ ~1 ~ 0 0 0 0 1
playsound minecraft:block.beacon.activate player @a[distance=..24] ~ ~ ~ 1 1.2
playsound minecraft:block.conduit.deactivate player @a[distance=..24] ~ ~ ~ 1 1.4

# 一、洗去施术者自己的魔化
execute as @a[distance=..4] run scoreboard players remove @s rpg_taint 25
execute as @a[distance=..4,scores={rpg_taint=..-1}] run scoreboard players set @s rpg_taint 0
execute as @a[distance=..4] run effect give @s minecraft:regeneration 6 0 true
execute as @a[distance=..4] run title @s actionbar ["",{"text":"驱　魔","color":"gold","bold":true},{"text":"　魔化已被洗去一分","color":"gray"}]

# 二、驱出阵内的空缺者：空壳散去，人回来
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..6] at @s run function rpg:rite/free
"""

RITE_FREE = """\
# 空壳散去。村民留下，罪从他身上剥离。
tag @s remove rpg.vacant
particle sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.06 40
particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.03 24
playsound minecraft:entity.evoker.celebrate hostile @a[distance=..20] ~ ~ ~ 1 1.3
effect give @s minecraft:glowing 4 0 true
execute as @a[distance=..8] run scoreboard players remove @s rpg_taint 5
execute at @s run summon minecraft:experience_orb ~ ~1 ~ {Value:24}
"""


# ---------------------------------------------------------------------------
# 入口与调度
# ---------------------------------------------------------------------------
ROOT = """\
# 驱魔体系每刻入口。
# 魔化与 HUD 是玩家侧的，走 @a 一次；空缺者那一支带类型且过守卫。
execute as @a at @s run function rpg:taint/taint
execute as @a run function rpg:hud/hud
execute if entity @e[type=minecraft:villager,tag=!rpg.vac.seen,limit=1] run function rpg:vacant/mark
execute if entity @a[tag=rpg.h.holy_weapon_tag1] run function rpg:vacant/vacant
execute unless entity @a[tag=rpg.h.holy_weapon_tag1] if entity @e[type=minecraft:villager,tag=rpg.vacant,tag=rpg.hurt,limit=1] run function rpg:vacant/vacant
execute as @a[scores={rpg_rite=1..}] run scoreboard players remove @s rpg_rite 1
"""


def build_give():
    """一件仪式用的圣水：右击灵魂灯笼起阵。"""
    s = io.open(GIVE, encoding="utf-8").read()
    if "驱魔圣水" in s:
        return 0
    item = ("give @a splash_potion["
            "custom_name=" + row(seg("[驱魔]", "#FFD700", True), seg("驱魔圣水", "white")) + ","
            "lore=[" + ",".join([
                RULE,
                row(seg("自"), seg("[圣座]", "#FFD700", True), seg("取来的水")),
                row(seg("以此水右击灵魂灯笼起阵")),
                RULE,
                row(seg("🔱仪式", "white", True), seg("[驱魔]", "#FFD700", True)),
                row(seg("四正方向各三格需各置一盏灵魂灯笼")),
                row(seg("成阵可洗去魔化，并驱出阵中的空缺者")),
                RULE]) + "],"
            'potion_contents={custom_color:16777200,custom_effects:[{id:"minecraft:water_breathing",duration:200,amplifier:0}]},'
            'tooltip_display={hidden_components:["minecraft:potion_contents"]},'
            "custom_data={rite_tag:1b}]")
    io.open(GIVE, "w", encoding="utf-8", newline="\n").write(
        s.rstrip("\n") + "\n\n##驱魔仪式\n" + item + "\n")
    return 1


def build_functions():
    n = build_hud()
    wf("taint/taint.mcfunction", TAINT.format())
    wf("taint/step.mcfunction", TAINT_STEP.format(MAX=TAINT_MAX, MAXP=TAINT_MAX + 1))
    wf("vacant/mark.mcfunction", VACANT_MARK)
    wf("vacant/vacant.mcfunction", VACANT)
    wf("rite/trigger.mcfunction", RITE_TRIGGER)
    wf("rite/check.mcfunction", RITE_CHECK)
    wf("rite/fail.mcfunction", RITE_FAIL)
    wf("rite/purge.mcfunction", RITE_PURGE)
    wf("rite/free.mcfunction", RITE_FREE)
    wf("exorcism.mcfunction", ROOT)

    wj(os.path.join(ADV, "rite.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:item_used_on_block",
            "conditions": {
                "item": {"predicates": {"minecraft:custom_data": "{rite_tag:1b}"}},
                "location": [{"condition": "minecraft:block_state_property",
                              "block": "minecraft:soul_lantern"}]}}},
        "rewards": {"function": "rpg:rite/trigger"}})

    tick = os.path.join(FUNC, "command/tick.mcfunction")
    s = io.open(tick, encoding="utf-8").read()
    if "rpg:exorcism" not in s:
        s = s.replace("function rpg:item/epic/epics",
                      "function rpg:item/epic/epics\nfunction rpg:exorcism")
        io.open(tick, "w", encoding="utf-8", newline="\n").write(s)
    return n


def route_actionbars():
    """把三处直接写 actionbar 的技能改成只更新 HUD 分数。

    原本它们各写各的，谁最后写谁赢；现在统一由 rpg:hud/hud 渲染。
    """
    edits = 0
    plans = [
        ("item/extra/leviathan_trigger.mcfunction", HUD_ANCHOR, "rpg_levi_charge", 30),
        ("item/epic/forge_trigger.mcfunction", HUD_FORGE, "rpg_forge_chg", 30),
    ]
    for rel, hid, score, full in plans:
        p = os.path.join(FUNC, rel)
        if not os.path.isfile(p):
            continue
        out = []
        for line in io.open(p, encoding="utf-8").read().split("\n"):
            if "actionbar" in line:
                continue                      # HUD 接手，这里不再直接写
            out.append(line)
        out += [
            "",
            "# 交给统一 HUD 渲染：声明占用，并把进度换算成 %d 格" % SEGMENTS,
            "scoreboard players set @s rpg_hud %d" % hid,
            "scoreboard players set @s rpg_hud_t %d" % HUD_TTL,
            "scoreboard players operation @s rpg_hud_p = @s %s" % score,
            "scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud",
            "scoreboard players operation @s rpg_hud_p /= #hud_full rpg_hud",
            "execute if entity @s[scores={rpg_hud_p=%d..}] run scoreboard players set @s rpg_hud_p %d"
            % (SEGMENTS, SEGMENTS),
        ]
        io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
        edits += 1

    # 藤蔓之鞭那条只是一句命中提示，占用一刻即可
    p = os.path.join(FUNC, "item/extra/vine.mcfunction")
    if os.path.isfile(p):
        s = io.open(p, encoding="utf-8").read()
        if "actionbar" in s:
            out = [l for l in s.split("\n") if "actionbar" not in l]
            io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
            edits += 1

    # 换算用的两个常量
    p = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "#hud_seg" not in s:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n")
            + "\nscoreboard players set #hud_seg rpg_hud %d" % SEGMENTS
            + "\nscoreboard players set #hud_full rpg_hud 30"
            + "\nscoreboard players set #taint_max rpg_hud %d\n" % TAINT_MAX)
    return edits


def add_objectives():
    p = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    add = [n for n in OBJECTIVES if n not in s]
    if add:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n"
            + "\n".join("scoreboard objectives add %s dummy" % n for n in add) + "\n")
    return add


def main():
    obj = add_objectives()
    n = build_functions()
    routed = route_actionbars()
    gave = build_give()
    print("exorcism: HUD %d branches, actionbar writers routed: %d" % (n, routed))
    print("exorcism: give +%d, objectives %s" % (gave, obj or "-"))


if __name__ == "__main__":
    main()
