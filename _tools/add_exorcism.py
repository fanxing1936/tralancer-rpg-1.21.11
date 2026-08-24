# -*- coding: utf-8 -*-
"""驱魔体系：魔化值、统一 HUD、空缺者、驱魔仪式、逆圣化。

几件事互相咬合：

* **魔化值** 让包里那条早就存在却只驱动粒子的圣/魔轴（`holy_weapon_tag` /
  `devil_weapon_tag`）第一次有了长期后果 —— 握着魔器会慢慢变成它的主人。
* **空缺者** 给驱魔一个可驱之物：外表与常人无异的空壳，只有持圣器时才显形。
  它不是靶子 —— 放着不管会蔓延，被识破会撕壳，被杀死会转移。
* **驱魔仪式** 是处置手段，也是唯一能把魔化值压下去的办法。
* **逆圣化** 是魔化值的终点。满值时点燃图腾，仪式不再净化而是引燃：
  熬过去，负与负相乘，污染反转成圣痕。

HUD 是这一版的架构重点。屏幕下方那条 actionbar 全局只有一份，
原本利维坦、熔火之锤、藤蔓之鞭各自直接往上写，谁最后写谁赢 —— 会互相打架。
现在改成**唯一出口**：技能只更新自己的分数并挂一个短时效的占用声明，
`rpg:hud/hud` 每刻按优先级挑一条渲染。蓄力条永远压过状态条，
蓄力一结束状态条自己回来。

模板一律走 `%` 取值而不是 `str.format`：命令里全是 `{}`（NBT、scores=、
粒子参数），用 format 就得把每一个花括号写成双份，抄错一个只有服务器
才会告诉你。`%` 不碰花括号。
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

# 驱魔图腾的模型位。totem_of_undying 上 1110001..1110006 已被占用。
TOTEM_CMD = 1110007
SEGMENTS = 10            # 进度条的格数
HUD_TTL = 3              # 技能占用 HUD 的时效（刻）

# HUD 占用编号
HUD_ANCHOR, HUD_FORGE, HUD_VINE, HUD_INVERT = 1, 2, 3, 4
HUD_MAMMON = 5           # 玛门的弓：满弓之后继续攒，攒满就是买断

LIT = 200                # 图腾点燃后的总时长（刻）
PULSES = [(200, 12, "1.0"), (160, 10, "0.88"), (120, 8, "0.74"),
          (80, 6, "0.58"), (40, 4, "0.40")]   # 刻 / 净化量 / 缩放
# 逆圣化的五道灼烧：刻 / 伤害 / 缩放。图腾越烧越小，光越烧越白。
BURNS = [(200, 3, "1.0"), (160, 3, "0.86"), (120, 4, "0.70"),
         (80, 4, "0.54"), (40, 5, "0.36")]
RITE_R = 6               # 作用半径
INV_R = 7                # 逆圣化必须站住的半径

HOLY_TICKS = 3600        # 圣痕持续 3 分钟
TEAR_AT = 60             # 被圣器照住多久，壳会裂开（刻）
SPREAD_EVERY = 400       # 蔓延的节拍（刻）
SPREAD_ODDS = 4          # 每拍 1/N 的概率向外伸手

OBJECTIVES = ["rpg_taint", "rpg_hud", "rpg_hud_p", "rpg_hud_t",
              "rpg_taint_t", "rpg_vac", "rpg_rite", "rpg_totem",
              "rpg_holy", "rpg_vac_x", "rpg_hud_on", "rpg_fall",
              "rpg_dm_cd", "rpg_dm_lord"]

# ---------------------------------------------------------------------------
# 堕落
# ---------------------------------------------------------------------------
# 满魔化之后的下坡路。走完就有东西从人身上挣出来。
#
# 拍子借魔化那口时钟（40 刻一拍），过半之后一拍两步 —— 堕落自己会加速。
# 所以 60 步不是 120 秒，是 90 秒。
FALL_MAX = 60

# 降临出来的那位。底子与特效沿用包里已有的恶魔 boss（见 demon_nbt）。
DEMON_HP = 120
DEMON_ATK = 11
DEMON_SEE = 48
DEMON_LIFE = 600         # 30 秒后自己散掉 —— 作者指定
BOSS_LIFE = 2400         # 空缺者那条路招出来的是来打架的，给两分钟
DEMON_CD = 70            # 出手间隔（刻）。30 秒里大约能放八次
DEMON_R = 12             # 多远之内有人才出手

# 下限 / 上限 / 攻击加成 / 颜色 / 档名
FALL_TIERS = [
    (1,  15, 1,  "gray",        "躁　动"),
    (16, 30, 3,  "dark_purple", "侵　蚀"),
    (31, 45, 6,  "red",         "夺　舍"),
    (46, 59, 10, "dark_red",    "临　界"),
]

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
    所以拆成一层调度 + 每种条各自一个函数：空闲一刻只评估几条落空的判定
    加一次递减，真正的分支只在该显示的时候才进去。
    """
    skills = [(HUD_ANCHOR, "沉　锚", "dark_aqua", "aqua"),
              (HUD_FORGE, "熔　流", "gold", "yellow"),
              (HUD_VINE, "缠　绕", "dark_green", "green"),
              (HUD_INVERT, "逆圣化", "dark_red", "gold"),
              (HUD_MAMMON, "买　断", "#7A5C00", "#FFD700")]

    # ---- 调度层 ----
    top = ["# 屏幕下方唯一的 actionbar 出口。技能不再各写各的 —— 它们只更新",
           "# rpg_hud / rpg_hud_p 并把 rpg_hud_t 顶到 %d，这里按优先级挑一条渲染。" % HUD_TTL,
           "# 蓄力条永远压过状态条；蓄力一结束，状态条自己就回来了。",
           "",
           "# 先把占用计时器坐实。scores= 只认已经存在的分数，没有这一行，",
           "# 从没蓄过力的玩家过不了下面 rpg_hud_t=..0 那一关，状态条永远不显示。",
           "scoreboard players add @s rpg_hud_t 0",
           ""]
    for hid, label, _dim, _lit in skills:
        top.append("execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=%d}] "
                   "run function rpg:hud/s%d" % (hid, hid))
    top += ["",
            "# 没有技能占用时才轮到持续状态行。魔化（或圣痕）与契约冷却在那一行里",
            "# **并排**显示 —— 它们都是状态，不该互相顶掉。",
            "execute if entity @s[scores={rpg_hud_t=..0}] run function rpg:hud/status",
            "",
            "execute if entity @s[scores={rpg_hud_t=1..}] run scoreboard players remove @s rpg_hud_t 1"]
    wf("hud/hud.mcfunction", "\n".join(top))

    total = len(top)

    # ---- 每个技能一条 ----
    for hid, label, dim, lit in skills:
        body = ["# %s 的进度条，%d 格。" % (label.replace("　", ""), SEGMENTS)]
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
    # 堕落开始之后这条位置改画堕落：魔化已经钉死在满值，没什么可看的了。
    disp.insert(0, "execute if entity @s[tag=rpg.taint.full] "
                   "run return run function rpg:hud/tfall")
    disp.insert(1, "")
    wf("hud/taint.mcfunction", "\n".join(disp))
    total += len(disp)

    for i, (_lo, _hi, colour, word) in enumerate(TAINT_TIERS, 1):
        body = ["# 魔化条 · %s" % word,
                "# 存进 storage 而不是直接写 actionbar —— 那一行还要和契约冷却",
                "# 并排显示，最后由 rpg:hud/render 一条宏拼起来。",
                "scoreboard players set @s rpg_hud_on 1"]
        for n in range(SEGMENTS + 1):
            comp = row(seg("魔化 ", "dark_gray"), *bar(n, SEGMENTS, colour),
                       seg("  " + word, colour))
            body.append("execute if entity @s[scores={rpg_hud_p=%d}] "
                        "run data modify storage rpg:hud a set value '%s'" % (n, comp))
        wf("hud/t%d.mcfunction" % i, "\n".join(body))
        total += len(body)

    # ---- 堕落条：魔化满了之后顶替它 ----
    body = ["# 堕落条。魔化钉死在满值之后，这条位置改报还剩多久。",
            "scoreboard players set @s rpg_hud_on 1",
            "scoreboard players operation @s rpg_hud_p = @s rpg_fall",
            "scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud",
            "scoreboard players operation @s rpg_hud_p /= #fall_max rpg_hud"]
    for n in range(SEGMENTS + 1):
        comp = row(seg("堕落 ", "dark_red"), *bar(n, SEGMENTS, "dark_red", "#3D2226"),
                   seg("  降临将至", "dark_red"))
        body.append("execute if entity @s[scores={rpg_hud_p=%d}] "
                    "run data modify storage rpg:hud a set value '%s'" % (n, comp))
    wf("hud/tfall.mcfunction", "\n".join(body))
    total += len(body)

    # ---- 圣痕条：魔化条的反面，同一个位置 ----
    body = ["# 圣痕条。逆圣化之后剩下的时间 —— 它走完，人就落回凡人。",
            "scoreboard players set @s rpg_hud_on 1",
            "scoreboard players operation @s rpg_hud_p = @s rpg_holy",
            "scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud",
            "scoreboard players operation @s rpg_hud_p /= #holy_full rpg_hud"]
    for n in range(SEGMENTS + 1):
        comp = row(seg("圣痕 ", "yellow"), *bar(n, SEGMENTS, "gold"),
                   seg("  逆圣化", "gold"))
        body.append("execute if entity @s[scores={rpg_hud_p=%d}] "
                    "run data modify storage rpg:hud a set value '%s'" % (n, comp))
    wf("hud/holy.mcfunction", "\n".join(body))
    total += len(body)

    # ---- 契约冷却：状态，不是蓄力 ----
    #
    # 原本它挂在蓄力条那一档（占用编号 5），于是每用一次柱中之力，
    # 魔化条就被顶掉整整 15 秒。它和魔化一样是持续状态，该并排而不是互相抢。
    body = ["# 契约冷却条。与魔化并排显示 —— 它是状态，不是蓄力。",
            "scoreboard players set @s rpg_hud_on 1",
            "scoreboard players operation @s rpg_hud_p = #pact_full rpg_hud",
            "scoreboard players operation @s rpg_hud_p -= @s rpg_pact_cd",
            "scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud",
            "scoreboard players operation @s rpg_hud_p /= #pact_full rpg_hud"]
    for n in range(SEGMENTS + 1):
        comp = row(seg("　│　", "dark_gray"), seg("契约 ", "dark_gray"),
                   *bar(n, SEGMENTS // 2, "#D4AF37"))
        body.append("execute if entity @s[scores={rpg_hud_p=%d}] "
                    "run data modify storage rpg:hud b set value '%s'" % (n, comp))
    wf("hud/pbar.mcfunction", "\n".join(body))
    total += len(body)

    # ---- 一行两半，拼起来 ----
    wf("hud/status.mcfunction", "\n".join([
        "# 屏幕下方的持续状态行：魔化（或圣痕）在左，契约冷却在右。",
        "#",
        "# 命令拼不了字符串，所以两半各自按分数选好自己那段存进 storage，",
        "# 最后由一条宏拼成一行。storage 是全局的，但整个计算与渲染",
        "# 发生在同一个玩家的同步执行里，中间插不进别人。",
        "scoreboard players set @s rpg_hud_on 0",
        "data modify storage rpg:hud a set value '{\"text\":\"\"}'",
        "data modify storage rpg:hud b set value '{\"text\":\"\"}'",
        "execute if entity @s[scores={rpg_holy=1..}] run function rpg:hud/holy",
        "execute if entity @s[scores={rpg_taint=1..}] run function rpg:hud/taint",
        "execute if entity @s[scores={rpg_pact_cd=1..}] run function rpg:hud/pbar",
        "execute if entity @s[scores={rpg_hud_on=1}] "
        "run function rpg:hud/render with storage rpg:hud"]))

    wf("hud/render.mcfunction",
       "# 唯一真正写 actionbar 的那一行。两半都是完整的文本组件，\n"
       "# 空的那半是 {\"text\":\"\"}，所以拼起来永远合法。\n"
       "$title @s actionbar [\"\",$(a),$(b)]")
    total += 2

    return total


# ---------------------------------------------------------------------------
# 魔化值
# ---------------------------------------------------------------------------
TAINT = """\
# 魔化：握着魔器慢慢沾染，握着圣器慢慢洗去。
# 每 40 刻结算一次 —— 逐刻结算既没必要也白费开销。
scoreboard players add @s rpg_taint_t 1
execute if entity @s[scores={rpg_taint_t=40..}] run function rpg:taint/step
execute if entity @s[scores={rpg_holy=1..}] run function rpg:taint/holy
"""

TAINT_STEP = """\
# 一次结算。魔器加、圣器减，两者都握着时互相抵消。
scoreboard players set @s rpg_taint_t 0

# 圣痕期间沾不上任何东西 —— 反转过的人，脏不了。
execute if entity @s[scores={rpg_holy=1..}] run return 0

execute if entity @s[tag=rpg.h.devil_tag1] run scoreboard players add @s rpg_taint 2
execute if entity @s[tag=rpg.h.devil_weapon_tag1] run scoreboard players add @s rpg_taint 1
execute if entity @s[tag=rpg.h.holy_weapon_tag1] run scoreboard players remove @s rpg_taint 1
execute if entity @s[scores={rpg_taint=%(MAXP)d..}] run scoreboard players set @s rpg_taint %(MAX)d
execute if entity @s[scores={rpg_taint=..-1}] run scoreboard players set @s rpg_taint 0

# 分档外显。低档只是身上泛起暗纹，越深越明显。
execute if entity @s[scores={rpg_taint=31..60}] at @s run particle dust{color:[0.32,0.16,0.42],scale:1} ~ ~1 ~ 0.35 0.6 0.35 0.01 4
execute if entity @s[scores={rpg_taint=61..90}] at @s run particle dust{color:[0.45,0.10,0.14],scale:2} ~ ~1 ~ 0.4 0.7 0.4 0.02 8
execute if entity @s[scores={rpg_taint=61..90}] at @s run particle sculk_soul ~ ~1.2 ~ 0.3 0.5 0.3 0.01 2

# 濒临魔化：力量上来了，但圣性之物开始灼手。
execute if entity @s[scores={rpg_taint=91..}] run effect give @s minecraft:strength 3 0 true
execute if entity @s[scores={rpg_taint=91..}] at @s run particle soul_fire_flame ~ ~1 ~ 0.4 0.7 0.4 0.01 6
execute if entity @s[scores={rpg_taint=91..},tag=rpg.h.holy_weapon_tag1] run damage @s 2 minecraft:magic
execute if entity @s[scores={rpg_taint=91..},tag=rpg.h.holy_weapon_tag1] run playsound minecraft:block.lava.extinguish player @s ~ ~ ~ 1 1.6

# 满值只报一次 —— 否则每两秒弹一遍标题，没人受得了。
execute if entity @s[scores={rpg_taint=%(MAX)d},tag=!rpg.taint.full] run function rpg:taint/full
execute if entity @s[scores={rpg_taint=..%(NEAR)d},tag=rpg.taint.full] run tag @s remove rpg.taint.full

# 到顶之后每一拍都往下掉一步。借的是同一口时钟，不另起。
execute if entity @s[tag=rpg.taint.full] run function rpg:taint/fall
"""

TAINT_FULL = """\
# 魔化到顶。这里**不给出路** —— 逆圣化还在，但不再有人告诉你它存在。
tag @s add rpg.taint.full
scoreboard players set @s rpg_fall 0
title @s times 10 70 25
title @s title ["",{"text":"堕 落 开 始","italic":false,"color":"dark_red","bold":true}]
title @s subtitle ["",{"text":"你手上的力量正在变大 —— 那不是你的","italic":false,"color":"dark_gray","italic":true}]
playsound minecraft:entity.wither.spawn master @s ~ ~ ~ 0.6 1.6
playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 1 0.5
execute at @s run particle sculk_charge_pop ~ ~1.2 ~ 0.4 0.6 0.4 0.05 30
"""

# ---------------------------------------------------------------------------
# 堕落的每一拍
# ---------------------------------------------------------------------------
FALL = """\
# 一拍堕落。过半之后一拍两步 —— 越往下掉得越快。
scoreboard players add @s rpg_fall 1
execute if entity @s[scores={rpg_fall=%(HALF)d..}] run scoreboard players add @s rpg_fall 1

# 走满了。return run：不加的话下面还会按最后一档再堆一次攻击。
execute if entity @s[scores={rpg_fall=%(MAX)d..}] at @s run return run function rpg:taint/advent

# 攻击加成整段重写。先摘再挂 —— 同一个 id 挂两次是会叠的。
attribute @s minecraft:attack_damage modifier remove rpg:fall
%(TIERS)s
"""

FALL_TIER = """\
# %(WORD)s —— 攻击 +%(ATK)d
attribute @s minecraft:attack_damage modifier add rpg:fall %(ATK)d add_value
execute at @s run particle dust{color:[%(RGB)s],scale:%(SCALE)s} ~ ~1 ~ 0.4 0.7 0.4 0.02 %(CNT)d
%(BODY)s
"""

# 「不可控」的那些手段。掷点用 random，一拍一掷。
FALL_YANK = """\
# 视角被扯一下。rotate 的角度只能是字面量，所以掷完点走一条宏。
execute store result storage rpg:fall yaw int 1 run random value -%(A)d..%(A)d
execute store result storage rpg:fall pit int 1 run random value -%(B)d..%(B)d
function rpg:taint/yank with storage rpg:fall
"""

FALL_YANK_DO = """\
# 相对旋转用 tp 而不是 rotate：两者都行，tp 的相对角度更早就有，稳。
$tp @s ~ ~ ~ ~$(yaw) ~$(pit)
"""

FALL_SWING = """\
# 不受控的一次挥砍。打的是身边的非玩家生物 —— 多人服里不该由堕落
# 替你决定去打谁。归属仍然记在本人头上：命令是单线程执行的，
# 这个标签在别人眼里从来不存在。
tag @s add rpg.fall.cast
execute at @s as @e[distance=..4.5,limit=1,sort=random,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display,type=!minecraft:text_display,type=!minecraft:marker] at @s run function rpg:taint/swing
tag @s remove rpg.fall.cast
"""

FALL_SWING_DO = """\
damage @s %(DMG)d minecraft:magic by @a[tag=rpg.fall.cast,limit=1]
particle sweep_attack ~ ~1 ~ 0.2 0.2 0.2 0 2
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..16] ~ ~ ~ 0.8 0.6
"""

# ---------------------------------------------------------------------------
# 降临
# ---------------------------------------------------------------------------
ADVENT = """\
# 走完了。有东西从这个人身上挣了出来。
tag @s remove rpg.taint.full
scoreboard players set @s rpg_fall 0
attribute @s minecraft:attack_damage modifier remove rpg:fall

# 掏空之后并不干净 —— 还剩这么多，下一轮从这里重新爬。
scoreboard players set @s rpg_taint %(LEFT)d
scoreboard players set @s rpg_taint_t 0

title @s times 10 80 30
title @s title ["",{"text":"降　临","italic":false,"color":"dark_red","bold":true}]
title @s subtitle ["",{"text":"它不再需要借你的手了","italic":false,"color":"gray","italic":true}]
effect give @s minecraft:weakness 12 1 true
effect give @s minecraft:slowness 12 1 true
effect give @s minecraft:nausea 10 0 true
execute unless entity @s[tag=rpg.holy] run effect give @s minecraft:blindness 3 0 true
damage @s 8 minecraft:magic

# 认主：签了哪一柱，挣出来的就是哪一位。没签的话是个无名的东西。
scoreboard players set #lord rpg_fall 0
execute if entity @s[tag=rpg.pact] run scoreboard players operation #lord rpg_fall = @s rpg_pact
execute at @s run function rpg:taint/advent_at
"""

ADVENT_AT = """\
particle explosion ~ ~1 ~ 0 0 0 0 1
particle sculk_soul ~ ~1 ~ 0.6 1 0.6 0.08 80
particle dust{color:[0.35,0.0,0.05],scale:3} ~ ~1 ~ 0.8 1.2 0.8 0.05 90
particle explosion_emitter ~ ~1 ~ 0 0 0 0 1
playsound minecraft:entity.wither.spawn hostile @a[distance=..48] ~ ~ ~ 1 0.6
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..48] ~ ~ ~ 1 0.5
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..48] ~ ~ ~ 0.8 0.7

# 这一行由 add_pact 改写成七柱分流 —— 那边才认识柱位。
function rpg:taint/lord
"""

# 没有契约的人招出来的东西。add_pact 会在它前面补上七位领主。
LORD_NONE = """\
# 无名者。没签过契约的人，身上挣出来的东西连名字都没有。
summon minecraft:vindicator ~ ~1 ~ %(NBT)s
function rpg:taint/advent_life
"""

# 降临的恶魔只待 30 秒。用记分板倒数 —— LifeTicks 那类字段只有特定实体才有，
# 而且 1.21.9 还改过名（LifeTicks -> life_ticks），不值得赌。
ADVENT_LIFE = """\
# 刚落地的那位开始倒数。标签在这一刻只可能挂在他一个身上。
#
# `#boss` 是一次性的开关：空缺者那条路在召唤前把它拨上，
# 于是同一套召唤能招出"来收账的"（30 秒）和"来打架的"（2 分钟）两种，
# 而不必写两份 NBT —— 两份迟早会写歪。
execute as @e[tag=rpg.advent.new] run scoreboard players set @s rpg_fall %(LIFE)d
execute if score #boss rpg_fall matches 1 as @e[tag=rpg.advent.new] run scoreboard players set @s rpg_fall %(BOSS)d
scoreboard players set #boss rpg_fall 0
tag @e[tag=rpg.advent.new] add rpg.advent.timed
tag @e[tag=rpg.advent.new] remove rpg.advent.new
"""

ADVENT_TICK = """\
# 降临者的一刻：寿命，以及他自己那一手。
# 场上没有这样的东西时，上层那道守卫会整段跳过。

# 没上过发条的先上发条 —— **不要**把它当成过期。
#
# 寿命是 advent_life 给的；任何一条召唤路径漏掉那一步（手抄一条 summon、
# 旧存档里遗留的实体、别处复制过去的 NBT……），它一进这里 rpg_fall 就是 0，
# 于是当场被自己人清掉 —— 表现就是"召唤出来立刻死"。
# 这一行把那条路堵死：认不出发条，就补一个，而不是判死刑。
execute if entity @s[tag=!rpg.advent.timed] run function rpg:taint/advent_arm

scoreboard players remove @s rpg_fall 1
execute if entity @s[scores={rpg_fall=..0}] at @s run return run function rpg:taint/advent_gone

# 出手。scores= 只认已经存在的分数，所以先把冷却坐实。
scoreboard players add @s rpg_dm_cd 0
execute if entity @s[scores={rpg_dm_cd=1..}] run return run scoreboard players remove @s rpg_dm_cd 1
execute at @s if entity @a[distance=..%(R)d,gamemode=!spectator,gamemode=!creative] run function rpg:taint/cast
"""

DEMON_CAST = """\
# 该他出手了。先上锁再分流 —— 归属靠这个标签认人，
# 命令是单线程的，同一刻不可能有第二个降临者挂着它。
scoreboard players set @s rpg_dm_cd %(CD)d
tag @s add rpg.dm.cast
function rpg:taint/skill
tag @s remove rpg.dm.cast
"""

# 这一行由 add_pact 改写成七柱分流 —— 那边才认识柱位。
SKILL_NONE = """\
# 无名者。没有名字的东西不会什么花样，只会一把把地掏。
particle sculk_soul ~ ~1 ~ 2 1 2 0.1 60
particle large_smoke ~ ~1 ~ 1.5 1 1.5 0.05 40
playsound minecraft:entity.warden.roar hostile @a[distance=..32] ~ ~ ~ 1 1.4
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk_none_hit
"""

SKILL_NONE_HIT = """\
damage @s 6 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @s minecraft:blindness 3 0 true
"""

ADVENT_ARM = """\
# 补发条。已经有寿命的不动（正规路径给的 600 / 2400 都算数），
# 只有真的没有才按默认值补。
tag @s add rpg.advent.timed
execute unless score @s rpg_fall matches 1.. run scoreboard players set @s rpg_fall %(LIFE)d
"""

ADVENT_GONE = """\
# 时候到了，它自己散掉 —— 不是被你打退的。
particle sculk_soul ~ ~1 ~ 0.5 0.9 0.5 0.08 60
particle large_smoke ~ ~1 ~ 0.4 0.8 0.4 0.05 40
particle squid_ink ~ ~1 ~ 0.4 0.8 0.4 0.05 30
playsound minecraft:entity.evoker.death hostile @a[distance=..32] ~ ~ ~ 1 0.6
kill @s
"""

TAINT_HOLY = """\
# 圣痕。逆圣化留下的那段时间：走到哪儿，空壳就散到哪儿。
# 属性增益在授予那一下就按整段时长给足了，这里只管计时、光晕和清场。
scoreboard players remove @s rpg_holy 1
particle end_rod ~ ~1.1 ~ 0.35 0.7 0.35 0.01 3
particle dust{color:[1.0,0.97,0.80],scale:1} ~ ~1 ~ 0.4 0.8 0.4 0.01 2
# 走到哪儿，空壳就散到哪儿 —— 本人就是一场行走的仪式。
# 这一行自己就是那次走查，前面再加一道同样的守卫只会白扫一遍。
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..6] at @s run function rpg:rite/free
execute if entity @s[scores={rpg_holy=..0}] run function rpg:taint/holy_end
"""

TAINT_HOLY_END = """\
# 圣痕淡去，人落回凡人。
scoreboard players set @s rpg_holy 0
effect clear @s minecraft:strength
effect clear @s minecraft:resistance
effect clear @s minecraft:regeneration
effect clear @s minecraft:fire_resistance
effect clear @s minecraft:absorption
particle end_rod ~ ~1 ~ 0.4 0.7 0.4 0.06 40
playsound minecraft:block.beacon.deactivate master @s ~ ~ ~ 0.8 1.2
title @s actionbar ["",{"text":"圣痕淡去","italic":true,"color":"gray"}]
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
# 空缺者的显形与反扑。两条走查，都带类型。
execute as @e[type=minecraft:villager,tag=rpg.vacant] at @s if entity @a[tag=rpg.h.holy_weapon_tag1,distance=..16] run function rpg:vacant/reveal
execute as @e[type=minecraft:villager,tag=rpg.vacant,tag=rpg.hurt] at @s run function rpg:vacant/lash
"""

VACANT_REVEAL = """\
# 被圣器照住。平时它和普通村民毫无分别，此刻藏不住了 ——
# 而照得越久，壳越撑不住。
effect give @s minecraft:glowing 2 0 true
particle sculk_soul ~ ~1.4 ~ 0.2 0.3 0.2 0.01 2
scoreboard players add @s rpg_vac_x 1
execute if entity @s[scores={rpg_vac_x=%(TEAR)d..},tag=!rpg.vac.torn] run function rpg:vacant/tear
"""

VACANT_LASH = """\
# 打它没有用 —— 罪落在动手的人身上，壳还会因此裂开。
execute on attacker run scoreboard players add @s rpg_taint 6
execute on attacker run title @s actionbar ["",{"text":"你打碎的只是空壳","italic":true,"color":"dark_gray"}]
execute if entity @s[tag=!rpg.vac.torn] run function rpg:vacant/tear
"""

VACANT_TEAR = """\
# 壳裂开了。村民还站在那儿，但里面的东西跑了出来。
tag @s add rpg.vac.torn
effect give @s minecraft:speed 30 1 true
particle sculk_charge_pop ~ ~1.2 ~ 0.4 0.5 0.4 0.1 30
particle soul ~ ~1.2 ~ 0.3 0.4 0.3 0.05 20
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..24] ~ ~ ~ 0.7 1.8
summon minecraft:vex ~ ~1 ~ {life_ticks:600,Tags:["rpg.vac.shard"],CustomName:[{"text":"空壳碎片","color":"dark_purple"}],Health:12f,attributes:[{id:"max_health",base:12f},{id:"attack_damage",base:4f},{id:"scale",base:0.75f}]}
summon minecraft:vex ~ ~1 ~ {life_ticks:600,Tags:["rpg.vac.shard"],CustomName:[{"text":"空壳碎片","color":"dark_purple"}],Health:12f,attributes:[{id:"max_health",base:12f},{id:"attack_damage",base:4f},{id:"scale",base:0.75f}]}
title @a[distance=..12] actionbar ["",{"text":"壳裂开了","italic":true,"color":"dark_purple"}]
"""

VACANT_SPREAD = """\
# 蔓延。放着不管，一个村子会慢慢烂掉。
# 每 %(EVERY)d 刻一拍，一拍只挑一个空缺者向外伸手 —— 绝不整场扫村民。
scoreboard players set #spread rpg_vac 0
execute as @e[type=minecraft:villager,tag=rpg.vacant,limit=1,sort=random] at @s run function rpg:vacant/creep
"""

VACANT_CREEP = """\
# 伸手不一定够得着。
execute store result score @s rpg_vac run random value 1..%(ODDS)d
execute if entity @s[scores={rpg_vac=1}] run function rpg:vacant/creep_do
"""

VACANT_CREEP_DO = """\
particle sculk_soul ~ ~1.2 ~ 0.3 0.4 0.3 0.03 12
execute as @e[type=minecraft:villager,tag=!rpg.vacant,distance=..8,limit=1,sort=nearest] at @s run function rpg:vacant/take
"""

VACANT_TAKE = """\
# 又空了一个。
tag @s add rpg.vacant
tag @s add rpg.vac.seen
scoreboard players set @s rpg_vac_x 0
particle sculk_charge_pop ~ ~1.2 ~ 0.3 0.4 0.3 0.05 16
particle soul ~ ~1.2 ~ 0.2 0.3 0.2 0.02 8
playsound minecraft:block.sculk_shrieker.shriek hostile @a[distance=..20] ~ ~ ~ 0.6 1.4
"""

VACANT_TRANSFER = """\
# 你杀死了一个空缺者 —— 由 rpg:item/vac_kill 在击杀那一刻触发。
# 但空壳不会因为躯体死掉就消失：它跳到最近的人身上。
# 这正是驱魔存在的理由 —— 剑解决不了它。
advancement revoke @s only rpg:item/vac_kill
scoreboard players add @s rpg_taint 8
execute at @s run particle soul ~ ~1 ~ 0.5 0.6 0.5 0.08 40
execute at @s run playsound minecraft:entity.vex.death hostile @a[distance=..24] ~ ~ ~ 1 0.6
execute at @s if entity @e[type=minecraft:villager,tag=!rpg.vacant,distance=..16,limit=1] run function rpg:vacant/jump
execute at @s unless entity @e[type=minecraft:villager,tag=!rpg.vacant,distance=..16,limit=1] run function rpg:vacant/loose
"""

VACANT_JUMP = """\
# 换了一具躯体，仅此而已。
execute as @e[type=minecraft:villager,tag=!rpg.vacant,distance=..16,limit=1,sort=nearest] at @s run function rpg:vacant/take
title @s times 10 50 20
title @s title ["",{"text":"它没有死","italic":false,"color":"dark_purple","bold":true}]
title @s subtitle ["",{"text":"空壳换了一个人","italic":false,"color":"gray"}]
"""

VACANT_LOOSE = """\
# 无处可去的东西不再散成碎片 —— 它自己找了一副躯体。
#
# @s 是那个动手的人。签了哪一柱，来的就是哪一位；没签过的是无名者 ——
# 与降临同一套分流，只是这一只是来打架的，所以寿命另算。
scoreboard players set #boss rpg_fall 1
scoreboard players set #lord rpg_fall 0
execute if entity @s[tag=rpg.pact] run scoreboard players operation #lord rpg_fall = @s rpg_pact
execute at @s run function rpg:taint/lord
"""

_VACANT_LOOSE_OLD = """\
# 附近没有第二具躯体可用。那东西只好赤裸地留在原地。
execute at @s run particle sculk_charge_pop ~ ~1 ~ 0.6 0.6 0.6 0.15 60
execute at @s run playsound minecraft:entity.warden.roar hostile @a[distance=..28] ~ ~ ~ 0.8 1.4
execute at @s run summon minecraft:vex ~ ~1 ~ {life_ticks:900,Tags:["rpg.vac.shard"],CustomName:[{"text":"无处可去者","color":"dark_purple"}],Health:16f,attributes:[{id:"max_health",base:16f},{id:"attack_damage",base:5f}]}
execute at @s run summon minecraft:vex ~ ~1 ~ {life_ticks:900,Tags:["rpg.vac.shard"],CustomName:[{"text":"无处可去者","color":"dark_purple"}],Health:16f,attributes:[{id:"max_health",base:16f},{id:"attack_damage",base:5f}]}
execute at @s run summon minecraft:vex ~ ~1 ~ {life_ticks:900,Tags:["rpg.vac.shard"],CustomName:[{"text":"无处可去者","color":"dark_purple"}],Health:16f,attributes:[{id:"max_health",base:16f},{id:"attack_damage",base:5f}]}
title @s times 10 50 20
title @s title ["",{"text":"无 处 可 去","italic":false,"color":"dark_purple","bold":true}]
"""


# ---------------------------------------------------------------------------
# 驱魔仪式
# ---------------------------------------------------------------------------
RITE_TRIGGER = """\
# 立图腾 —— 由 rpg:item/rite 在「以驱魔图腾右击方块」时触发。
# 图腾本体用 item_display：没有 AI、没有碰撞，只是一件立在那儿的东西。
advancement revoke @s only rpg:item/rite
execute if entity @s[scores={rpg_rite=1..}] run return 0

# 手里必须真的是驱魔图腾。item_used_on_block 天生promiscuous ——
# "对方块使用物品"把**放方块**也算在内，所以正确性不该全押在进度的断言上，
# 这里再验一道。
execute unless items entity @s weapon.mainhand minecraft:totem_of_undying[minecraft:custom_data~{totem_tag:1b}] run return 0

scoreboard players set @s rpg_rite 10
clear @s minecraft:totem_of_undying[minecraft:custom_data~{totem_tag:1b}] 1
execute at @s anchored eyes positioned ^ ^ ^2 run function rpg:rite/place
"""

RITE_PLACE = """\
# 图腾落地。此刻它还是熄的 —— 要等圣水浇上去。
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.totem"],item:{id:"minecraft:totem_of_undying",count:1,components:{"minecraft:custom_model_data":{floats:[%(TCMD)d.0f]}}},transformation:{translation:[0f,0.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f],right_rotation:[0f,0f,0f,1f]},billboard:"vertical",brightness:{sky:15,block:15}}
particle dust{color:[0.95,0.86,0.45],scale:1} ~ ~0.6 ~ 0.3 0.4 0.3 0.02 20
playsound minecraft:block.respawn_anchor.set_spawn player @a[distance=..16] ~ ~ ~ 1 1.4
title @a[distance=..6] actionbar ["",{"text":"图腾已立","color":"gold"},{"text":"　以驱魔圣水浇之","color":"gray","italic":true}]
"""

RITE_TICK = """\
# 图腾的一生：等圣水、点燃、按拍推进、收场。
# 由 rpg:exorcism 守卫调用 —— 场上没有图腾时整段跳过。
#
# 只有两条走查，都带类型。节拍不在这里展开：一支图腾一次调用，
# 剩下的分支全在 @s 上做 —— 那是自身作用域，不必再走一遍世界。

# 熄着的图腾等一朵圣水云。滞留药水落地留下的 area_effect_cloud 就是"浇上了"，
# 喷溅型落地即散，什么都留不下，所以驱魔圣水做成滞留型。
execute as @e[type=minecraft:item_display,tag=rpg.totem,tag=!rpg.totem.lit] at @s if entity @e[type=minecraft:area_effect_cloud,distance=..3] run function rpg:rite/light

# 点着的图腾走自己的节拍
execute as @e[type=minecraft:item_display,tag=rpg.totem.lit] at @s run function rpg:rite/beat
"""

RITE_LIGHT = """\
# 圣水浇上，图腾点燃。烧法取决于旁边站着谁 ——
# 一个魔化到顶的人在场，仪式就不再是净化，而是反转。
tag @s add rpg.totem.lit
scoreboard players set @s rpg_totem %(LIT)d
playsound minecraft:item.bottle.empty player @a[distance=..16] ~ ~ ~ 1 0.8
execute if entity @a[distance=..%(INV_R)d,scores={rpg_taint=%(MAX)d}] run function rpg:rite/light_inv
execute unless entity @a[distance=..%(INV_R)d,scores={rpg_taint=%(MAX)d}] run function rpg:rite/light_pure
"""

RITE_LIGHT_PURE = """\
particle end_rod ~ ~0.6 ~ 0.4 0.5 0.4 0.05 60
particle dust{color:[1.0,0.98,0.86],scale:2} ~ ~0.8 ~ 0.5 0.6 0.5 0.04 80
particle minecraft:flash{color:16777200} ~ ~0.8 ~ 0 0 0 0 1
playsound minecraft:block.beacon.activate player @a[distance=..24] ~ ~ ~ 1 1.2
title @a[distance=..8] actionbar ["",{"text":"驱　魔","color":"gold","bold":true},{"text":"　图腾开始燃尽","color":"gray"}]
"""

RITE_LIGHT_INV = """\
# 逆圣化点燃。图腾这次不往外净化 —— 它朝着那个人烧。
tag @s add rpg.totem.inv
tag @a[distance=..%(INV_R)d,scores={rpg_taint=%(MAX)d}] add rpg.inv.subject
particle minecraft:flash{color:6684672} ~ ~0.8 ~ 0 0 0 0 1
particle sculk_charge_pop ~ ~0.8 ~ 0.6 0.6 0.6 0.1 80
particle dust{color:[0.42,0.06,0.10],scale:3} ~ ~0.8 ~ 0.6 0.7 0.6 0.03 90
playsound minecraft:entity.wither.spawn master @a[distance=..40] ~ ~ ~ 1 0.7
playsound minecraft:block.end_portal.spawn master @a[distance=..40] ~ ~ ~ 0.6 1.6
title @a[tag=rpg.inv.subject] times 10 50 20
title @a[tag=rpg.inv.subject] title ["",{"text":"逆 圣 化","italic":false,"color":"dark_red","bold":true}]
title @a[tag=rpg.inv.subject] subtitle ["",{"text":"负与负相乘，站住别走","italic":false,"color":"gold"}]
"""

RITE_BEAT = """\
# 一支图腾一拍。净化与反转两套节拍，从这里分开。
execute if entity @s[tag=rpg.totem.inv] run function rpg:rite/beat_inv
execute unless entity @s[tag=rpg.totem.inv] run function rpg:rite/beat_pure
"""

RITE_BEAT_PURE = """\
# 净化的节拍：一拍比一拍弱。
%(PULSES)s
particle dust{color:[0.98,0.92,0.62],scale:1} ~ ~0.7 ~ 0.22 0.3 0.22 0.01 2
execute if entity @s[scores={rpg_totem=1..}] run scoreboard players remove @s rpg_totem 1
execute if entity @s[scores={rpg_totem=..0}] run function rpg:rite/burst
"""

RITE_BEAT_INV = """\
# 反转的节拍：图腾朝着受术者烧，一拍比一拍狠。
# 人必须站在圈里熬完 —— 走开或者倒下，仪式当场作废。
# return run：失败要连这支图腾余下的节拍一起掐掉，否则后面几条会对着
# 一个已经 kill 掉的 @s 继续跑。
execute unless entity @a[tag=rpg.inv.subject,distance=..%(INV_R)d] run return run function rpg:rite/inv_fail
scoreboard players operation #inv_now rpg_hud = @s rpg_totem
execute as @a[tag=rpg.inv.subject,distance=..%(INV_R)d] run function rpg:rite/inv_hud
%(BURNS)s
particle soul_fire_flame ~ ~0.8 ~ 0.45 0.55 0.45 0.02 3
particle dust{color:[0.42,0.06,0.10],scale:2} ~ ~0.8 ~ 0.5 0.6 0.5 0.01 2
execute if entity @s[scores={rpg_totem=1..}] run scoreboard players remove @s rpg_totem 1
execute if entity @s[scores={rpg_totem=..0}] run function rpg:rite/inv_burst
"""

RITE_INV_HUD = """\
# 交给统一 HUD 渲染。反转要看的是"熬过去多少"，所以进度反着算：
# 图腾烧掉的那部分，才是受术者已经撑住的部分。
scoreboard players set @s rpg_hud %(HID)d
scoreboard players set @s rpg_hud_t %(TTL)d
scoreboard players operation @s rpg_hud_p = #inv_full rpg_hud
scoreboard players operation @s rpg_hud_p -= #inv_now rpg_hud
scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud
scoreboard players operation @s rpg_hud_p /= #inv_full rpg_hud
"""

RITE_PULSE = """\
# 一拍净化。图腾每燃尽一分，效力就弱一分 —— 净化量由调用处给。
particle end_rod ~ ~0.5 ~ %(R_HALF)s 0.2 %(R_HALF)s 0.04 70
particle dust{color:[1.0,0.98,0.86],scale:2} ~ ~0.8 ~ %(R_HALF)s 0.4 %(R_HALF)s 0.03 60
playsound minecraft:block.conduit.ambient player @a[distance=..20] ~ ~ ~ 1 1.3
execute as @a[distance=..%(R)d] run scoreboard players remove @s rpg_taint %(AMOUNT)d
execute as @a[distance=..%(R)d,scores={rpg_taint=..-1}] run scoreboard players set @s rpg_taint 0
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..%(R)d] at @s run function rpg:rite/free
# 图腾随着燃尽一点点缩小
data merge entity @s {transformation:{translation:[0f,0.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[%(SCALE)sf,%(SCALE)sf,%(SCALE)sf],right_rotation:[0f,0f,0f,1f]}}
"""

RITE_BURN = """\
# 反转的第 %(N)d 道。灼烧越来越烈，光却越来越白 —— 那是它正在翻面。
particle minecraft:flash{color:%(FLASH)d} ~ ~0.9 ~ 0 0 0 0 1
particle end_rod ~ ~0.7 ~ 0.5 0.4 0.5 %(SPD)s %(CNT)d
particle dust{color:[%(DR)s,%(DG)s,%(DB)s],scale:2} ~ ~0.8 ~ 0.6 0.5 0.6 0.03 %(CNT)d
playsound minecraft:block.respawn_anchor.charge master @a[distance=..24] ~ ~ ~ 1 %(PITCH)s
execute as @a[tag=rpg.inv.subject,distance=..%(R)d] run damage @s %(DMG)d minecraft:magic
execute as @a[tag=rpg.inv.subject,distance=..%(R)d] run effect give @s minecraft:slowness 3 2 true
execute as @a[tag=rpg.inv.subject,distance=..%(R)d] at @s run particle soul_fire_flame ~ ~1 ~ 0.4 0.8 0.4 0.06 40
data merge entity @s {transformation:{translation:[0f,0.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[%(SCALE)sf,%(SCALE)sf,%(SCALE)sf],right_rotation:[0f,0f,0f,1f]}}
"""

RITE_BURST = """\
# 燃尽。图腾炸开 —— 最后一下把余威全部吐出来。
particle explosion ~ ~0.6 ~ 0.6 0.3 0.6 0 6
particle end_rod ~ ~0.6 ~ 1.2 0.6 1.2 0.35 140
particle dust{color:[1.0,0.94,0.70],scale:3} ~ ~0.8 ~ 1 0.6 1 0.2 120
particle minecraft:flash{color:16777200} ~ ~1 ~ 0 0 0 0 1
playsound minecraft:entity.generic.explode player @a[distance=..28] ~ ~ ~ 1 1.4
playsound minecraft:block.beacon.deactivate player @a[distance=..28] ~ ~ ~ 1 1.1

# 最后一击：范围内的空缺者一并驱出，敌意生物被震开
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..%(R)d] at @s run function rpg:rite/free
execute as @e[distance=0.1..%(R)d,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display,type=!minecraft:villager] at @s run damage @s 6 minecraft:magic
execute as @e[distance=0.1..%(R)d,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display,type=!minecraft:villager] at @s run data merge entity @s {Motion:[0d,0.6d,0d]}
title @a[distance=..10] actionbar ["",{"text":"图腾已尽","color":"gray","italic":true}]
kill @s
"""

RITE_INV_BURST = """\
# 反转完成。魔化没有被洗掉 —— 它被烧穿了，从另一面出来。
particle minecraft:flash{color:16777215} ~ ~1 ~ 0 0 0 0 1
particle end_rod ~ ~0.8 ~ 1.4 0.8 1.4 0.5 220
particle dust{color:[1.0,0.99,0.92],scale:4} ~ ~1 ~ 1.2 0.8 1.2 0.25 180
particle totem_of_undying ~ ~1 ~ 0.8 0.8 0.8 0.4 120
playsound minecraft:item.totem.use master @a[distance=..48] ~ ~ ~ 1 1
playsound minecraft:block.beacon.power_select master @a[distance=..48] ~ ~ ~ 1 0.8
execute as @a[tag=rpg.inv.subject,distance=..%(R)d] run function rpg:rite/inv_grant
kill @s
"""

RITE_INV_GRANT = """\
# 圣痕落定。增益一次性按整段时长给足，之后每刻只剩计时和光晕。
tag @s remove rpg.inv.subject
tag @s remove rpg.taint.full
scoreboard players set @s rpg_taint 0
# 堕落连同它堆起来的那点攻击一起作废 —— 反转是真的把人拽回来了。
scoreboard players set @s rpg_fall 0
attribute @s minecraft:attack_damage modifier remove rpg:fall
scoreboard players set @s rpg_holy %(HOLY)d
effect give @s minecraft:instant_health 1 2 true
effect give @s minecraft:strength %(SEC)d 1 true
effect give @s minecraft:resistance %(SEC)d 0 true
effect give @s minecraft:regeneration %(SEC)d 0 true
effect give @s minecraft:fire_resistance %(SEC)d 0 true
effect give @s minecraft:absorption %(SEC)d 1 true
title @s times 10 70 20
title @s title ["",{"text":"圣 痕","italic":false,"color":"gold","bold":true}]
title @s subtitle ["",{"text":"负与负相乘，污染发生反转","italic":false,"color":"yellow"}]
"""

RITE_INV_FAIL = """\
# 人走了，或者人倒了。图腾自己碎掉，罪一点没少。
particle large_smoke ~ ~0.7 ~ 0.5 0.5 0.5 0.05 60
particle campfire_signal_smoke ~ ~0.8 ~ 0.3 0.3 0.3 0.02 20
playsound minecraft:block.glass.break master @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:entity.blaze.death master @a[distance=..24] ~ ~ ~ 0.8 0.5
execute as @a[tag=rpg.inv.subject] run function rpg:rite/inv_abort
kill @s
"""

RITE_INV_ABORT = """\
# 反噬。没熬住的人，得把没烧完的那部分自己吞下去。
tag @s remove rpg.inv.subject
effect give @s minecraft:wither 5 0
effect give @s minecraft:blindness 3 0
playsound minecraft:entity.wither.hurt master @s ~ ~ ~ 1 0.6
title @s times 10 50 20
title @s title ["",{"text":"反 转 失 败","italic":false,"color":"dark_red","bold":true}]
title @s subtitle ["",{"text":"污染未曾松手","italic":false,"color":"gray"}]
"""

RITE_FREE = """\
# 空壳散去。村民留下，罪从他身上剥离；跑出来的碎片一并收走。
tag @s remove rpg.vacant
tag @s remove rpg.vac.torn
scoreboard players set @s rpg_vac_x 0
particle sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.06 40
particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.03 24
playsound minecraft:entity.evoker.celebrate hostile @a[distance=..20] ~ ~ ~ 1 1.3
effect give @s minecraft:glowing 4 0 true
kill @e[type=minecraft:vex,tag=rpg.vac.shard,distance=..12]
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
execute if entity @e[type=minecraft:item_display,tag=rpg.totem,limit=1] run function rpg:rite/tick
execute as @a[scores={rpg_rite=1..}] run scoreboard players remove @s rpg_rite 1

# 蔓延的节拍器。没有比一次记分板比较更便宜的守卫 ——
# 先数够 %(EVERY)d 刻，再去找村民。
scoreboard players add #spread rpg_vac 1
execute if score #spread rpg_vac matches %(EVERY)d.. run function rpg:vacant/spread
"""


def build_give():
    """两件东西：立起来的图腾，和浇上去的圣水。"""
    s = io.open(GIVE, encoding="utf-8").read()
    if "驱魔图腾" in s:
        return 0
    totem = ("give @a totem_of_undying["
             "custom_name=" + row(seg("[驱魔]", "#FFD700", True), seg("驱魔图腾", "white")) + ","
             "lore=[" + ",".join([
                 RULE,
                 row(seg("以"), seg("[圣座]", "#FFD700", True), seg("之木刻成")),
                 row(seg("长按右键立起，再以驱魔圣水浇之")),
                 RULE,
                 row(seg("🔱仪式", "white", True), seg("[驱魔]", "#FFD700", True)),
                 row(seg("点燃后每隔两秒净化一次，效力逐次递减")),
                 row(seg("燃尽时炸开，驱出范围内所有空缺者")),
                 RULE,
                 row(seg("🔱逆圣化", "white", True), seg("[满魔化]", "#FF3300", True)),
                 row(seg("魔化满值者在场时点燃，仪式转为反转")),
                 row(seg("站定十秒熬过灼烧，魔化尽去，留下圣痕")),
                 RULE]) + "],"
             # 不死图腾本身没有任何右键行为，所以得先给它一个「使用」动作，
             # using_item 才有东西可响。consume_seconds 取一个大到永远吃不完的
             # 数，与包里其余主动物品同一套写法。
             "food={nutrition:0,saturation:0f,can_always_eat:1b},"
             'consumable={consume_seconds:100140f,animation:"block",'
             'sound:"minecraft:block.respawn_anchor.charge",'
             "has_consume_particles:false,on_consume_effects:[]},"
             "max_stack_size=1,"
             "custom_model_data={floats:[%d.0f]}," % TOTEM_CMD +
             "custom_data={totem_tag:1b}]")
    # 必须是滞留型：喷溅药水落地即散，图腾没有任何东西可以感知；
    # 滞留药水会留下 area_effect_cloud，那才是"浇上了"的凭据。
    water = ("give @a lingering_potion["
             "custom_name=" + row(seg("[驱魔]", "#FFD700", True), seg("驱魔圣水", "white")) + ","
             "lore=[" + ",".join([
                 RULE,
                 row(seg("自"), seg("[圣座]", "#FFD700", True), seg("取来的水")),
                 row(seg("浇在驱魔图腾上以点燃仪式")),
                 RULE]) + "],"
             'potion_contents={custom_color:16777200,custom_effects:[{id:"minecraft:water_breathing",duration:100,amplifier:0}]},'
             'tooltip_display={hidden_components:["minecraft:potion_contents"]},'
             "custom_data={rite_tag:1b}]")
    io.open(GIVE, "w", encoding="utf-8", newline="\n").write(
        s.rstrip("\n") + "\n\n##驱魔仪式\n" + totem + "\n" + water + "\n")
    return 2


def build_functions():
    n = build_hud()

    # ---- 魔化 ----
    wf("taint/taint.mcfunction", TAINT)
    wf("taint/step.mcfunction",
       TAINT_STEP % {"MAX": TAINT_MAX, "MAXP": TAINT_MAX + 1, "NEAR": TAINT_MAX - 1})
    wf("taint/full.mcfunction", TAINT_FULL)
    build_fall()
    wf("taint/holy.mcfunction", TAINT_HOLY)
    wf("taint/holy_end.mcfunction", TAINT_HOLY_END)

    # ---- 空缺者 ----
    wf("vacant/mark.mcfunction", VACANT_MARK)
    wf("vacant/vacant.mcfunction", VACANT)
    wf("vacant/reveal.mcfunction", VACANT_REVEAL % {"TEAR": TEAR_AT})
    wf("vacant/lash.mcfunction", VACANT_LASH)
    wf("vacant/tear.mcfunction", VACANT_TEAR)
    wf("vacant/spread.mcfunction", VACANT_SPREAD % {"EVERY": SPREAD_EVERY})
    wf("vacant/creep.mcfunction", VACANT_CREEP % {"ODDS": SPREAD_ODDS})
    wf("vacant/creep_do.mcfunction", VACANT_CREEP_DO)
    wf("vacant/take.mcfunction", VACANT_TAKE)
    wf("vacant/transfer.mcfunction", VACANT_TRANSFER)
    wf("vacant/jump.mcfunction", VACANT_JUMP)
    wf("vacant/loose.mcfunction", VACANT_LOOSE)

    # ---- 仪式 ----
    wf("rite/trigger.mcfunction", RITE_TRIGGER)
    wf("rite/place.mcfunction", RITE_PLACE % {"TCMD": TOTEM_CMD})
    wf("rite/tick.mcfunction", RITE_TICK)
    wf("rite/light.mcfunction",
       RITE_LIGHT % {"LIT": LIT, "INV_R": INV_R, "MAX": TAINT_MAX})
    wf("rite/light_pure.mcfunction", RITE_LIGHT_PURE)
    wf("rite/light_inv.mcfunction",
       RITE_LIGHT_INV % {"INV_R": INV_R, "MAX": TAINT_MAX})
    wf("rite/beat.mcfunction", RITE_BEAT)

    pulses = []
    for i, (at, amount, scale) in enumerate(PULSES, 1):
        pulses.append("execute if entity @s[scores={rpg_totem=%d}] "
                      "run function rpg:rite/p%d" % (at, i))
        wf("rite/p%d.mcfunction" % i,
           RITE_PULSE % {"R": RITE_R, "R_HALF": "%.1f" % (RITE_R * 0.5),
                         "AMOUNT": amount, "SCALE": scale})
    wf("rite/beat_pure.mcfunction", RITE_BEAT_PURE % {"PULSES": "\n".join(pulses)})

    # 反转的五道：光从暗红一路走到纯白，声音一道比一道高。
    tints = [(0.42, 0.06, 0.10), (0.58, 0.14, 0.12), (0.76, 0.34, 0.16),
             (0.92, 0.62, 0.28), (1.00, 0.94, 0.72)]
    flashes = [0x4A0A0E, 0x7A1C14, 0xC05A22, 0xE8A64A, 0xFFF4C0]
    burns = []
    for i, (at, dmg, scale) in enumerate(BURNS, 1):
        burns.append("execute if entity @s[scores={rpg_totem=%d}] "
                     "run function rpg:rite/v%d" % (at, i))
        r, g, b = tints[i - 1]
        wf("rite/v%d.mcfunction" % i,
           RITE_BURN % {"N": i, "R": INV_R, "DMG": dmg, "SCALE": scale,
                        "FLASH": flashes[i - 1], "DR": r, "DG": g, "DB": b,
                        "CNT": 40 + i * 20, "SPD": "%.2f" % (0.05 + i * 0.03),
                        "PITCH": "%.2f" % (0.6 + i * 0.22)})
    wf("rite/beat_inv.mcfunction",
       RITE_BEAT_INV % {"INV_R": INV_R, "BURNS": "\n".join(burns)})
    wf("rite/inv_hud.mcfunction",
       RITE_INV_HUD % {"HID": HUD_INVERT, "TTL": HUD_TTL})

    wf("rite/burst.mcfunction", RITE_BURST % {"R": RITE_R})
    wf("rite/inv_burst.mcfunction", RITE_INV_BURST % {"R": INV_R})
    wf("rite/inv_grant.mcfunction",
       RITE_INV_GRANT % {"HOLY": HOLY_TICKS, "SEC": HOLY_TICKS // 20})
    wf("rite/inv_fail.mcfunction", RITE_INV_FAIL)
    wf("rite/inv_abort.mcfunction", RITE_INV_ABORT)
    wf("rite/free.mcfunction", RITE_FREE)

    root = ROOT % {"EVERY": SPREAD_EVERY}
    root += ("\n# 降临者的 30 秒寿命。带类型且过守卫 —— 场上没有就整段跳过。\n"
             "execute if entity @e[type=minecraft:vindicator,tag=rpg.advent,limit=1] "
             "run execute as @e[type=minecraft:vindicator,tag=rpg.advent] "
             "run function rpg:taint/advent_tick\n")
    wf("exorcism.mcfunction", root)

    # 走 using_item 而不是 item_used_on_block。后者有两个坑，而且是同一个
    # 根因的两面：它没有 `item` 字段（物品判定得塞进 location 的 match_tool），
    # 写错就等于没有条件，放任何方块都会触发；而它又只在交互**成功**时才响，
    # 不死图腾没有 useOn 行为，右击方块直接 PASS —— 拿着正主反而不响。
    # using_item 只认正在使用的那件物品，与包里其余主动物品同一条路。
    wj(os.path.join(ADV, "rite.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {"predicates": {
                "minecraft:custom_data": "{totem_tag:1b}"}}}}},
        "rewards": {"function": "rpg:rite/trigger"}})

    # 击杀空缺者 —— 生物死掉那一刻，原版只有这一个口子能通知到数据包。
    wj(os.path.join(ADV, "vac_kill.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:player_killed_entity",
            "conditions": {
                "entity": [{"condition": "minecraft:entity_properties",
                            "entity": "this",
                            "predicate": {"type": "minecraft:villager",
                                          "nbt": "{Tags:[\"rpg.vacant\"]}"}}]}}},
        "rewards": {"function": "rpg:vacant/transfer"}})

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

    # 换算用的常量
    p = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "#hud_seg" not in s:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n")
            + "\nscoreboard players set #hud_seg rpg_hud %d" % SEGMENTS
            + "\nscoreboard players set #hud_full rpg_hud 30"
            + "\nscoreboard players set #taint_max rpg_hud %d" % TAINT_MAX
            + "\nscoreboard players set #fall_max rpg_hud %d" % FALL_MAX
            + "\nscoreboard players set #inv_full rpg_hud %d" % LIT
            + "\nscoreboard players set #holy_full rpg_hud %d\n" % HOLY_TICKS)
    return edits


# 恶魔蒙不住带圣器的人。黑暗与失明整条去掉，其余 debuff 折半。
BLIND = ("blindness", "darkness")


def holy_variant(text):
    """派生出"对方带着圣器"的那一版。

    只动 `effect give`：黑暗与失明删掉，其余秒数折半（最少 1）。
    伤害与粒子原样保留 —— 圣器挡的是看不见，不是打不疼。
    """
    out = []
    for line in text.split("\n"):
        parts = line.split()
        # 只动落在**玩家自己**头上的那些。有些技能里的 effect give 是
        # 恶魔给自己回血（收割、点金），那与护体无关，不能碰。
        if (len(parts) >= 6 and parts[0] == "effect" and parts[1] == "give"
                and parts[2] == "@s"):
            eff = parts[3].split(":")[-1]
            if eff in BLIND:
                continue
            try:
                parts[4] = str(max(1, int(parts[4]) // 2))
                line = " ".join(parts)
            except ValueError:
                pass
        out.append(line)
    return "\n".join(out)


def wf_holy(rel, text):
    """写一对：原版，外加带圣器时走的那一版。

    没有任何 debuff 的函数不派生 —— 那种情况下两版一模一样。
    """
    # 变换之后和原文一样，就说明这个函数根本没有落在玩家身上的 debuff ——
    # 那就不必派生，也不必多一道判定。
    if holy_variant(text) == text:
        wf(rel, text)
        return
    name = rel[:-len(".mcfunction")]
    wf(name + "_holy.mcfunction",
       "# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。\n"
       + holy_variant(text))
    wf(rel,
       "# 身上带着圣器的人走另一条 —— 见 " + name.split("/")[-1] + "_holy。\n"
       "execute if entity @s[tag=rpg.holy] run return run function rpg:"
       + name + "_holy\n" + text)


def demon_nbt(name, accent, colour):
    """降临出来的那位。

    底子、姿态、特效全部沿用包里已有的恶魔 boss（`command/summon.mcfunction`
    里那只卫道士），不另起一套：

    * **卫道士**，`Johnny:1` —— 见谁打谁，不挑人；
    * **`devil` 标签**是关键。`entities/warden/warden/g0` 已经在为
      `@e[tag=devil]` 每刻续隐身、喷 large_smoke 与 squid_ink ——
      挂上这个标签，"保持隐身 + 那身烟"就自动到位，一行都不用抄。
    * `active_effects` 是 1.21.11 的正确字段名（作者原本的代码里就是它，
      老的 `ActiveEffects` 会被静默丢掉）。

    名牌仍用罪器那一套 [DEVIL] 前缀 —— 虽然隐身，被打时的伤害提示与
    死亡消息里还是认得出是哪一位。
    """
    return (
        '{Tags:["rpg.advent","rpg.demon","devil","rpg.advent.new"],'
        'Johnny:1,Silent:1b,PersistenceRequired:1b,'
        'CustomName:[{"text":"[DEVIL]","color":"%s","bold":true,"italic":false},'
        '{"text":"%s","color":"%s","italic":false}],'
        'Health:%df,'
        'active_effects:[{id:"invisibility",duration:-1,amplifier:0,'
        'show_particles:0b},{id:"speed",duration:-1,amplifier:1,'
        'show_particles:0b}],'
        'attributes:['
        '{id:"max_health",base:%df},'
        '{id:"attack_damage",base:%df},'
        '{id:"attack_knockback",base:2f},'
        '{id:"armor",base:8f},'
        '{id:"follow_range",base:%df},'
        '{id:"knockback_resistance",base:0.5f}],'
        'drop_chances:{mainhand:0f}}'
        % (accent, name, colour, DEMON_HP, DEMON_HP, DEMON_ATK, DEMON_SEE))


def build_fall():
    """堕落的每一档，加上降临。"""
    half = FALL_MAX // 2 + 1

    tiers = []
    for i, (lo, hi, atk, colour, word) in enumerate(FALL_TIERS, 1):
        tiers.append("execute if entity @s[scores={rpg_fall=%d..%d}] "
                     "run return run function rpg:taint/f%d" % (lo, hi, i))

        # 越往下，人越不听自己使唤
        body = []
        if i >= 2:
            body += ["effect give @s minecraft:nausea %d 0 true" % (2 + i),
                     "execute if predicate rpg:fall%d run function rpg:taint/yank_roll" % i]
        if i >= 3:
            body += ["# 脚步忽快忽慢 —— 不是你在走",
                     "execute if predicate rpg:fall%d run effect give @s minecraft:slowness 2 1 true" % i,
                     "execute unless predicate rpg:fall%d run effect give @s minecraft:speed 2 1 true" % i]
        if i >= 4:
            body += ["execute if predicate rpg:fall%d run effect give @s minecraft:darkness 3 0 true" % i,
                     "playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 1 0.6",
                     "# 最深一档：手自己动起来",
                     "execute if predicate rpg:fall%d run function rpg:taint/swing_roll" % i]
        else:
            body.append("playsound minecraft:entity.wither.ambient master @s ~ ~ ~ 0.%d 0.5" % (i + 2))

        rgb = {"gray": "0.45,0.45,0.48", "dark_purple": "0.32,0.10,0.42",
               "red": "0.62,0.09,0.12", "dark_red": "0.38,0.0,0.04"}[colour]
        wf("taint/f%d.mcfunction" % i, FALL_TIER % {
            "WORD": word.replace("\u3000", ""), "ATK": atk, "RGB": rgb,
            "SCALE": "%.1f" % (1 + i * 0.4), "CNT": 4 + i * 4,
            "BODY": "\n".join(body)})

    wf("taint/fall.mcfunction",
       FALL % {"HALF": half, "MAX": FALL_MAX, "TIERS": "\n".join(tiers)})
    wf("taint/yank_roll.mcfunction", FALL_YANK % {"A": 80, "B": 25})
    wf("taint/yank.mcfunction", FALL_YANK_DO)
    wf("taint/swing_roll.mcfunction", FALL_SWING)
    wf("taint/swing.mcfunction", FALL_SWING_DO % {"DMG": 5})
    wf("taint/advent.mcfunction", ADVENT % {"LEFT": 40})
    wf("taint/advent_at.mcfunction", ADVENT_AT)
    wf("taint/lord.mcfunction",
       LORD_NONE % {"NBT": demon_nbt("无名者", "#3D0000", "dark_gray")})
    wf("taint/advent_life.mcfunction",
       ADVENT_LIFE % {"LIFE": DEMON_LIFE, "BOSS": BOSS_LIFE})
    wf("taint/advent_tick.mcfunction", ADVENT_TICK % {"R": DEMON_R})
    wf("taint/cast.mcfunction", DEMON_CAST % {"CD": DEMON_CD})
    wf("taint/skill.mcfunction", SKILL_NONE)
    wf_holy("taint/sk_none_hit.mcfunction", SKILL_NONE_HIT)
    wf("taint/advent_arm.mcfunction", ADVENT_ARM % {"LIFE": DEMON_LIFE})
    wf("taint/advent_gone.mcfunction", ADVENT_GONE)

    # 掷点的赔率。档越深，失控越频繁。
    for i, odds in ((2, 4), (3, 3), (4, 2)):
        wj(os.path.join(DP, "data/rpg/predicate/fall%d.json" % i),
           {"condition": "minecraft:random_chance", "chance": round(1.0 / odds, 3)})


def build_totem_art(rp):
    """图腾的模型分派。贴图由 import_art 从作者的原图裁好。"""
    md = os.path.join(rp, "assets/rpg/models/item")
    if not os.path.isdir(md):
        os.makedirs(md)
    wj(os.path.join(md, "exorcism_totem.json"),
       {"parent": "item/generated",
        "textures": {"layer0": "rpg:item/exorcism_totem"}})

    p = os.path.join(rp, "assets/minecraft/items/totem_of_undying.json")
    doc = json.load(io.open(p, encoding="utf-8"))
    entries = doc["model"]["entries"]
    if any(e["threshold"] == TOTEM_CMD for e in entries):
        return 0
    entries.append({"threshold": TOTEM_CMD,
                    "model": {"type": "minecraft:model",
                              "model": "rpg:item/exorcism_totem"}})
    entries.sort(key=lambda e: e["threshold"])
    wj(p, doc)
    return 1


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
    rp = sys.argv[2] if len(sys.argv) > 2 else "../resourcepack"
    obj = add_objectives()
    n = build_functions()
    routed = route_actionbars()
    gave = build_give()
    print("exorcism: HUD %d branches, actionbar writers routed: %d" % (n, routed))
    art = build_totem_art(rp)
    print("exorcism: give +%d, objectives %s, 图腾模型 +%d"
          % (gave, obj or "-", art))


if __name__ == "__main__":
    main()
