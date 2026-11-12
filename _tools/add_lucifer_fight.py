# -*- coding: utf-8 -*-
"""路西法二阶段「知善恶树」的战斗逻辑（docs/LUCIFER-P2-DESIGN.md）。

外形属于 add_lucifer_p2_model.py（rpg:lucifer_p2/，GPT 的生成器，它只读
tag rpg.lu.phase2）。这里写 rpg:lucifer_fight/：何时变身、变身演出、
五招一罪约、普攻、破绽与捆绑时的动作。驱魔系统的阈值（420 镇压、175 保护线）
一行不改，这里只在它们外面工作。

接入点全部由本生成器插入，每一处都先确认锚点存在，找不到就让构建失败：
* taint/advent_tick：紧跟 `function rpg:inquest/boss_tick` 之后调用本阶段 tick，
  这样捆绑和罪约蓄势的提前 return 都跳不过它；
* taint/sk1、ult1_warn、ult1_charge、ult1：开头分流到本阶段（sk1_1..5 不动，
  那几个文件归一阶段外观的接入）。

生成物（藤蔓、果核、预警标记）带领主编号 rpg_l2_id 与寿命 rpg_l2_t，
由全局 tick 倒数清掉；领主没了它们也会自己消失。召来的罪仆每秒检查一次主人。
"""

import math
import os
import sys

import add_lucifer_p2_fx_art as art
import add_lucifer_props as props
import add_pact
import rpg_ui_style as ui
from display_mob import hook_tag, wf

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "lucifer_fight")
F = "rpg:lucifer_fight"
CLIP = "rpg:lucifer_p2/play/jungleabomination_"

# ---------------------------------------------------------------------------
# 可调常量
# ---------------------------------------------------------------------------
FINAL_TAG = "rpg.lub"     # 最终 Boss 路西法的载体标签（docs/LUCIFER-BOSS-DESIGN.md）；领主没有它，不会变身
P2_AT = 580             # 生命值降到这里以下变成树（总量 700）
P3_AT = 420             # 预留：三阶段古龙（tag rpg.lu.phase3），目前不触发
SCALE = 2.5             # 二阶段体型；载体座位实测随之从 2.0 升到 5.0
SLOW = -0.4             # 二阶段移速倍率修正
GAP = 30                # 每招结束后到下一招的最短间隔（刻）
MELEE_CD = 70           # 普攻「碾」的冷却
MELEE_RANGE = 6
MORPH_SWAP = 40         # 变身第几刻换成树
MORPH_END = 100

SURV = "gamemode=!spectator,gamemode=!creative"
LORD = "type=minecraft:vindicator,tag=rpg.lu2"
BY = "by @e[tag=rpg.dm.cast,limit=1]"
FORM = add_pact.LUCIFER_FORMS[2]

LIT = ui.pillar(1)["lit"]
DUST = ui.pillar_transition(1, 1.6)
DUST_BIG = ui.pillar_transition(1, 2.4)
DUST_SMALL = ui.pillar_transition(1, 1.2)
MOSS = "block{block_state:{Name:\"minecraft:moss_block\"}}"
ROOT = "block{block_state:{Name:\"minecraft:rooted_dirt\"}}"


def w(path, lines):
    if isinstance(lines, str):
        lines = lines.strip("\n").split("\n")
    wf(os.path.join(OUT, *path.split("/")) + ".mcfunction", lines)


def notice(name, phrase, ultimate=False):
    return add_pact._notice(FORM, name, phrase, ultimate)


def say(text, gloss=False):
    """〖路西法〗 播报（ART-STYLE.md §12）：柱中间色加粗标签，阶段切换带哥特小注。"""
    parts = [ui.comp("%s路西法%s" % ui.BRACKETS, ui.pillar_mid(1), True)]
    if gloss:
        parts.append(ui.comp(" " + ui.fraktur("Lucifer"), ui.BROADCAST_GLOSS))
    parts.append(ui.comp(ui.GAP, ui.BROADCAST_BODY))
    parts.append(ui.comp(text, ui.BROADCAST_BODY))
    return "tellraw @a[distance=..32] %s" % ui.row(*parts)


def clue(n):
    # 罪证只属于驱魔调查，也就是降临的恶魔领主；最终 Boss 复用这些招式时不记。
    return ("execute if entity @s[tag=rpg.advent] at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] "
            "run function rpg:inquest/clue/1_%d" % n)


def at(t, line):
    return "execute if score @s rpg_l2_t matches %d run %s" % (t, line)


def holy_pair(name, base, holy):
    """命中函数：持圣器者走减半分支（黑暗、失明不落，其余 debuff 减半）。"""
    w(name, ["# 身上带着圣器的人走另一条 —— 见 %s_holy。" % name.split("/")[-1],
             "execute if entity @s[tag=rpg.holy] run return run function %s/%s_holy" % (F, name)]
      + base)
    w(name + "_holy", ["# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。"] + holy)


def hit_lines(dmg, effects, kind="minecraft:magic"):
    out = []
    if kind == "minecraft:magic":
        out.append("function rpg:inquest/seal/ability/record_magic")
    out.append("damage @s %s %s %s" % (dmg, kind, BY))
    for eff, sec, amp in effects:
        out.append("effect give @s minecraft:%s %d %d true" % (eff, sec, amp))
    return out


def hit(name, dmg, effects, kind="minecraft:magic", extra=()):
    holy = [(e, max(1, (s + 1) // 2), a) for e, s, a in effects if e not in ("blindness", "darkness")]
    holy_pair(name, hit_lines(dmg, effects, kind) + list(extra), hit_lines(dmg, holy, kind) + list(extra))


def push_back(dist):
    """沿远离领主的方向退开，落点要有两格空间才挪。"""
    return ("execute at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet "
            "if block ^ ^ ^-%s #minecraft:replaceable if block ^ ^1 ^-%s #minecraft:replaceable "
            "run tp @s ^ ^ ^-%s" % (dist, dist, dist))


# ---------------------------------------------------------------------------
# 展示实体特效（§5）：贴花与实物是 item_display，发光体是 text_display 字形。
# 每个特效召出时记下种类 rpg_l2_k 与寿命 rpg_l2_t；全局 tick 只在寿命走到
# 预定的那一刻发一次 data merge，剩下的交给客户端插值。
# ---------------------------------------------------------------------------
GAZE_AT = 30


def xf(t=(0, 0, 0), s=(1, 1, 1), q=(0, 0, 0, 1)):
    return ("left_rotation:[%gf,%gf,%gf,%gf],right_rotation:[0f,0f,0f,1f],"
            "translation:[%gf,%gf,%gf],scale:[%gf,%gf,%gf]" % (tuple(q) + tuple(t) + tuple(s)))


def flat(size, y=0.05):
    return xf(t=(0, y, 0), s=(size, 1, size))


def ascale(size):
    return "scale:[%gf,1f,%gf]" % (size, size)


def amove(t):
    return "translation:[%gf,%gf,%gf]" % tuple(t)


# 种类：名称 -> (寿命, [(寿命走到几时, 插值刻数, 变换片段)])
ANIMS = {
    "sigil": (110, [(109, 20, ascale(9)), (8, 8, ascale(0.01))]),
    "eden": (120, [(119, 15, ascale(20)), (8, 8, ascale(0.01))]),
    "vmark": (24, [(23, 4, ascale(2.2))]),
    "smark": (20, [(19, 4, ascale(2.5)), (5, 5, ascale(0.01))]),
    "fmark": (70, [(69, 8, ascale(11))]),
    "crack": (40, [(6, 6, ascale(0.01))]),
    "shock6": (9, [(8, 6, ascale(6.4))]),
    "shock11": (9, [(8, 6, ascale(11))]),
    "shard": (14, [(13, 12, amove((0, 1.5, 4)))]),
    "spike": (34, [(33, 3, amove((0, 0, 0))), (5, 4, amove((0, -3.9, 0)))]),
    "line": (20, []),
    "gline": (10, []),
    # 一阶段
    "trail": (18, []),
    "tmark": (14, []),
    "cring": (26, [(25, 10, ascale(16)), (4, 4, ascale(0.01))]),
    "cring12": (20, [(19, 6, ascale(12)), (4, 4, ascale(0.01))]),
    "scrown": (52, [(51, 20, ascale(20)), (6, 6, ascale(0.01))]),
    "fmark16": (24, [(23, 8, ascale(16))]),
    "feather": (22, [(21, 20, amove((0, -6, 0)))]),
    "shock12": (9, [(8, 5, ascale(12))]),
    "shock16": (9, [(8, 6, ascale(16))]),
    "shock20": (10, [(9, 7, ascale(20))]),
}
# 字形逐帧：名称 -> (方式, 每帧刻数, 初始寿命)；一次性的按剩余寿命取帧，循环的按寿命取模。
FRAMES = {"burst": ("once", 2, 16), "juice": ("once", 2, 12), "eye": ("once", 5, GAZE_AT + 12),
          "fruit": ("loop", 3, None), "pollen": ("loop", 3, 95),
          "glint": ("once", 2, 8), "spear_beam": ("once", 2, 12), "crown": ("loop", 3, 30),
          "slash": ("once", 2, 12)}
KINDS = list(ANIMS) + list(FRAMES)


def kind_id(name):
    return KINDS.index(name) + 1


def born(name, life=None):
    """刚召出的特效：记种类与寿命。用独立的新生标签，免得撞上同刻召出的预警标记。"""
    if life is None:
        life = ANIMS[name][0] if name in ANIMS else FRAMES[name][2]
    return ["scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k %d" % kind_id(name),
            "scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t %d" % life,
            "tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew"]


def prop(name, model, transform, extra="", tags=()):
    """贴花或实物：一个 item_display。"""
    anim = ',"rpg.lu2f.anim"' if ANIMS.get(name, (0, []))[1] else ""
    return ['summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew"%s%s],'
            'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:%s/%s"}},'
            'brightness:{sky:15,block:15},view_range:2f,%stransformation:{%s}}'
            % (anim, "".join(',"%s"' % t for t in tags), *(model.split(":", 1)[1].split("/", 1) if ":" in model else (art.NS, model)),
               extra, transform)] + born(name)


def sprite(name, transform, extra="", tags=(), life=None, billboard="center"):
    """发光体：一个 text_display 字形，默认朝向相机。"""
    return ['summon minecraft:text_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"%s],'
            'text:{text:"%s",font:"%s"},background:0,billboard:"%s",brightness:{sky:15,block:15},'
            'view_range:2f,%stransformation:{%s}}'
            % ("".join(',"%s"' % t for t in tags), art.glyph_text(name), art.FONT, billboard, extra, transform)] + born(name, life)


def glyph_scale(name, blocks):
    """让字形宽这么多格的缩放。"""
    return round(blocks / (art.GLYPHS[name][1] * 0.025), 4)


def build_fx():
    w("fx/anim", ["execute if score @s rpg_l2_k matches %d run return run function %s/fx/k/%s" % (kind_id(n), F, n)
                  for n in KINDS if (n in ANIMS and ANIMS[n][1]) or n in FRAMES])
    for name, (_, steps) in ANIMS.items():
        if steps:
            w("fx/k/" + name, ["execute if score @s rpg_l2_t matches %d run data merge entity @s "
                               "{start_interpolation:0,interpolation_duration:%d,transformation:{%s}}" % s
                               for s in steps])
    for name, (mode, step, life) in FRAMES.items():
        count = art.GLYPHS[name][4]
        text = lambda i: 'data merge entity @s {text:{text:"%s",font:"%s"}}' % (art.glyph_text(name, i), art.FONT)
        if mode == "once":
            w("fx/k/" + name, ["execute if score @s rpg_l2_t matches %d run %s" % (life - i * step, text(i))
                               for i in range(1, count)])
        else:
            w("fx/k/" + name, ["scoreboard players operation #f rpg_l2_v = @s rpg_l2_t",
                               "scoreboard players operation #f rpg_l2_v %%= #c%d rpg_l2_v" % (count * step)] +
              ["execute if score #f rpg_l2_v matches %d run %s" % (i * step, text(i)) for i in range(count)])

    # 连线（诱惑之线、知善恶的视线）：执行者是被连的玩家，位置是起点并朝向玩家。
    for kind, width in (("line", 0.16), ("gline", 0.1)):
        w("fx/%s" % kind, [
            "scoreboard players set #d rpg_l2_v 0",
            "function %s/fx/line_step" % F,
        ] + prop(kind, "lure", xf(s=(width, width, 0.01)), "teleport_duration:0,interpolation_duration:3,",
                 tags=("rpg.lu2f.aim",)) + [
            "execute as @e[tag=rpg.lu2f.aim,limit=1] run tp @s ~ ~ ~ ~ ~",
            "execute as @e[tag=rpg.lu2f.aim,limit=1] store result entity @s transformation.scale[2] float 1 run scoreboard players get #d rpg_l2_v",
            "execute as @e[tag=rpg.lu2f.aim,limit=1] store result entity @s transformation.translation[2] float 0.5 run scoreboard players get #d rpg_l2_v",
            "tag @e[tag=rpg.lu2f.aim] remove rpg.lu2f.aim",
        ])
    w("fx/line_step", [
        "scoreboard players add #d rpg_l2_v 1",
        "execute if entity @s[distance=..1.3] run return 0",
        "execute positioned ~ ~-1.6 ~ if entity @s[distance=..1.3] run return 0",
        "execute if score #d rpg_l2_v matches ..24 positioned ^ ^ ^1 run function %s/fx/line_step" % F,
    ])
    w("fx/shards", ["# 六片碎片向外抛出（at 爆点）：每片按自己的朝向飞，变换在实体的本地坐标里。"] + sum(
        [prop("shard", "shard_scale", xf(s=(0.8, 0.8, 0.8)),
              "Rotation:[%gf,0f]," % (i * 60 - 180), tags=("rpg.lu2f.sh",)) for i in range(6)], []))
    w("fx/debris", ["# 落地碎屑：树皮与枯叶（at 落点）。"] + sum(
        [prop("shard", "shard_%s" % ("bark", "leaf")[i % 2], xf(s=(0.9, 0.9, 0.9)),
              "Rotation:[%gf,0f]," % (i * 60 - 150)) for i in range(6)], []))


# ---------------------------------------------------------------------------
# 入口：tick、全局生成物、变身
# ---------------------------------------------------------------------------
def build_core():
    w("load", [
        "scoreboard objectives add rpg_l2_st dummy",
        "scoreboard objectives add rpg_l2_sk dummy",
        "scoreboard objectives add rpg_l2_t dummy",
        "scoreboard objectives add rpg_l2_mc dummy",
        "scoreboard objectives add rpg_l2_id dummy",
        "scoreboard objectives add rpg_l2_v dummy",
        "scoreboard objectives add rpg_l2_k dummy",
    ] + ["scoreboard players set #c%d rpg_l2_v %d" % (n, n) for n in sorted(
        {art.GLYPHS[g][4] * FRAMES[g][1] for g in FRAMES if FRAMES[g][0] == "loop"})])
    # 状态：2 自由、3 出招、4 破绽、5 捆绑。变身期间挂 rpg.lu2f.morph。
    w("tick", [
        "# 路西法每刻（as 领主 at 领主，由 taint/advent_tick 在 inquest/boss_tick 之后调用）。",
        "scoreboard players add @s rpg_l2_st 0",
        "execute if entity @s[tag=!rpg.lu.phase2,tag=!rpg.lu2f.morph] run function %s/morph/check" % F,
        "execute if entity @s[tag=rpg.lu2f.morph] run return run function %s/morph/tick" % F,
        "execute unless entity @s[tag=rpg.lu.phase2] run return run function %s/p1/tick" % F,
        "execute if entity @s[tag=!rpg.lu2f.big] run function %s/grow" % F,
        "execute unless score @s rpg_l2_id matches 1.. run function %s/new_id" % F,
        "# 自己射出的果核不论处于什么状态都要飞完。",
        "scoreboard players operation #id rpg_l2_id = @s rpg_l2_id",
        "tag @s add rpg.dm.cast",
        "execute as @e[type=minecraft:item_display,tag=rpg.lu2f.dart] if score @s rpg_l2_id = #id rpg_l2_id at @s run function %s/dart/step" % F,
        "tag @s remove rpg.dm.cast",
        "execute if score @s rpg_ex_stage matches 2..4 run return run function %s/bound/tick" % F,
        "execute if entity @s[tag=rpg.lu2f.bound] run function %s/bound/leave" % F,
        "# 忙碌时把出招冷却压在 %d 以上：招与招之间至少隔这么久，中间穿插普攻。" % GAP,
        "execute unless score @s rpg_l2_st matches 2 if score @s rpg_dm_cd matches ..%d run scoreboard players set @s rpg_dm_cd %d" % (GAP - 1, GAP),
        "execute if score @s rpg_l2_st matches 3 run return run function %s/skill/tick" % F,
        "execute if score @s rpg_l2_st matches 4 run return run function %s/vuln/tick" % F,
        "scoreboard players set @s rpg_l2_st 2",
        "execute if score @s rpg_l2_mc matches 1.. run scoreboard players remove @s rpg_l2_mc 1",
        "execute if score @s rpg_l2_mc matches ..0 if score @s rpg_dm_ult matches ..0 "
        "if entity @a[distance=..%d,%s] run function %s/melee/start" % (MELEE_RANGE, SURV, F),
    ])
    w("new_id", ["scoreboard players add #next rpg_l2_id 1",
                 "scoreboard players operation @s rpg_l2_id = #next rpg_l2_id"])
    w("grow", [
        "# 二阶段体型。手动挂 rpg.lu.phase2 调试时也会走到这里。",
        "tag @s add rpg.lu2f.big",
        "attribute @s minecraft:scale base set %s" % SCALE,
        "effect clear @s minecraft:speed",
        "attribute @s minecraft:movement_speed modifier remove rpg:lu2f_slow",
        "attribute @s minecraft:movement_speed modifier add rpg:lu2f_slow %s add_multiplied_total" % SLOW,
        "# 原版近战归零：伤害全部来自对得上动作的「碾」。",
        "attribute @s minecraft:attack_damage modifier remove rpg:lu2f_melee",
        "attribute @s minecraft:attack_damage modifier add rpg:lu2f_melee -1 add_multiplied_total",
        "attribute @s minecraft:knockback_resistance modifier remove rpg:lu2f_root",
        "attribute @s minecraft:knockback_resistance modifier add rpg:lu2f_root 1 add_value",
    ])
    w("hold", ["attribute @s minecraft:movement_speed modifier remove rpg:lu2f_hold",
               "attribute @s minecraft:movement_speed modifier add rpg:lu2f_hold -1 add_multiplied_total"])
    w("free", [
        "# 一招结束：回到自由状态。",
        "scoreboard players set @s rpg_l2_st 2",
        "scoreboard players set @s rpg_l2_sk 0",
        "scoreboard players set @s rpg_l2_t 0",
        "attribute @s minecraft:movement_speed modifier remove rpg:lu2f_hold",
        "attribute @s minecraft:armor modifier remove rpg:lu2f_open",
        "tag @a remove rpg.lu2f.hit",
    ])
    w("cancel", [
        "# 打断正在进行的招式：只收预警标记，已破土的藤蔓、飞出的果核按寿命自然消失。",
        "scoreboard players operation #id rpg_l2_id = @s rpg_l2_id",
        "execute as @e[type=minecraft:marker,tag=rpg.lu2f.mark] if score @s rpg_l2_id = #id rpg_l2_id run kill @s",
        "function %s/free" % F,
    ])

    # 全局：生成物寿命与罪仆归属。
    w("global", [
        "execute if entity @e[tag=rpg.lu2f.fx,limit=1] as @e[tag=rpg.lu2f.fx] run function %s/fx_life" % F,
        "scoreboard players add #clock rpg_l2_t 1",
        "execute if score #clock rpg_l2_t matches 20.. run function %s/minion/sweep" % F,
    ])
    w("fx_life", [
        "scoreboard players remove @s rpg_l2_t 1",
        "execute if score @s rpg_l2_t matches ..0 run return run kill @s",
        "execute if entity @s[type=minecraft:block_display,tag=rpg.lu2f.vine] run function %s/vine/life" % F,
        "execute if entity @s[tag=rpg.lu2f.anim] run function %s/fx/anim" % F,
    ])
    w("minion/sweep", [
        "scoreboard players set #clock rpg_l2_t 0",
        "execute as @e[tag=rpg.lu2f.minion] at @s run function %s/minion/check" % F,
    ])
    w("minion/check", [
        "scoreboard players operation #id rpg_l2_id = @s rpg_l2_id",
        "scoreboard players set #alive rpg_l2_v 0",
        "execute as @e[%s] if score @s rpg_l2_id = #id rpg_l2_id run scoreboard players set #alive rpg_l2_v 1" % LORD,
        "execute if score #alive rpg_l2_v matches 1 run return 0",
        "particle %s ~ ~1 ~ 0.4 0.8 0.4 0.02 18" % DUST_SMALL,
        "particle %s ~ ~0.5 ~ 0.4 0.4 0.4 0.1 16" % MOSS,
        "tp @s ~ -256 ~",
        "kill @s",
    ])

    # 变身。
    w("morph/check", [
        "# 只有最终 Boss 路西法会变身；七罪恶魔领主路西法是常规的单阶段（用户 2026-11-09）。",
        "execute unless entity @s[tag=%s] run return 0" % FINAL_TAG,
        "# 打到 %d 以下就变身；一击打穿 420、当刻进了镇压也照样变。" % P2_AT,
        "execute if score @s rpg_ex_stage matches 0 if score @s rpg_ex_hp matches ..%d run return run function %s/morph/start" % (P2_AT, F),
        "execute if score @s rpg_ex_stage matches 1.. run function %s/morph/start" % F,
    ])
    w("morph/start", [
        "function %s/cancel" % F,
        "tag @s add rpg.lu2f.morph",
        "scoreboard players set @s rpg_l2_t 0",
        "scoreboard players set @s rpg_dm_ult 0",
        "function %s/hold" % F,
        "effect give @s minecraft:resistance 6 4 true",
        "execute unless score @s rpg_l2_id matches 1.. run function %s/new_id" % F,
        "function rpg:lucifer_lord/play/laugh",
        say("蛇回到了树上。", gloss=True),
        "playsound rpg:lucifer_p2.intro_foley hostile @a[distance=..48] ~ ~ ~ 1.4 1",
        "particle %s ~ ~1 ~ 1 1.2 1 0.04 40" % DUST_BIG,
    ] + prop("sigil", "root_sigil", flat(0.01)))
    w("morph/tick", [
        "scoreboard players add @s rpg_l2_t 1",
        "scoreboard players set @s rpg_dm_ult 0",
        "execute if score @s rpg_dm_cd matches ..%d run scoreboard players set @s rpg_dm_cd %d" % (GAP - 1, GAP),
        "# 苔藓与孢子向他收拢，地下有根须翻动。",
        "execute if score @s rpg_l2_t matches ..%d run particle spore_blossom_air ~ ~2 ~ 4 2 4 0 6" % (MORPH_SWAP - 1),
        "execute if score @s rpg_l2_t matches ..%d run particle %s ~ ~0.2 ~ 3 0.1 3 0.1 6" % (MORPH_SWAP - 1, ROOT),
        at(10, "particle %s ~ ~1.5 ~ 1.5 1.5 1.5 0.05 30" % DUST),
        at(20, "playsound minecraft:block.rooted_dirt.break hostile @a[distance=..32] ~ ~ ~ 1.4 0.5"),
        at(30, "particle %s ~ ~1.5 ~ 1 2 1 0.08 40" % DUST_BIG),
        at(MORPH_SWAP, "function %s/morph/swap" % F),
        at(MORPH_SWAP + 1, "function %s/morph/land" % F),
        at(MORPH_END, "function %s/morph/end" % F),
    ])
    w("morph/swap", [
        "# 换成树：挂上外观只读的 rpg.lu.phase2，当刻直接换装，不等下一刻。",
        "tag @s add rpg.lu.phase2",
        "function %s/grow" % F,
        "function rpg:lucifer_p2/dress",
        say("伊甸的树重新长了出来。"),
        "particle %s ~ ~3 ~ 2.5 3 2.5 0.1 80" % MOSS,
        "particle %s ~ ~3 ~ 2 3 2 0.05 60" % DUST_BIG,
        "particle spore_blossom_air ~ ~4 ~ 3 3 3 0 60",
        "execute positioned ~ ~3.5 ~ run function %s/morph/burst" % F,
    ])
    w("morph/burst", sprite("burst", xf(s=(glyph_scale("burst", 7),) * 3)) + ["function %s/fx/shards" % F])
    w("morph/land", [
        "function %sland" % CLIP,
        "tag @s add rpg.dm.cast",
        "execute as @a[distance=..6,%s] run function %s/morph/shock" % (SURV, F),
        "tag @s remove rpg.dm.cast",
        "particle %s ~ ~0.3 ~ 3 0.2 3 0.15 90" % ROOT,
        "particle %s ~ ~0.5 ~ 3 0.3 3 0.05 50" % DUST,
    ])
    hit("morph/shock", 6, [], extra=[push_back(2.5)])
    w("morph/end", [
        "tag @s remove rpg.lu2f.morph",
        "effect clear @s minecraft:resistance",
        "function %s/free" % F,
        "scoreboard players set @s rpg_l2_mc 30",
        "scoreboard players set @s rpg_dm_cd %d" % GAP,
    ])


# ---------------------------------------------------------------------------
# 出招分流（taint/sk1 与 ult1_* 开头会跳到这里）
# ---------------------------------------------------------------------------
SKILLS = [  # (编号, 目录, 罪证号, 名称, 短语)
    (1, "vine", 1), (2, "fruit", 2), (3, "tempt", 3), (4, "fall", 4), (5, "gaze", 5),
]


def build_dispatch():
    w("cast", [
        "# 五招掷一招，撞上一招就顺延（同一阶段的 sk1 规则）。",
        "execute store result score #pick rpg_l2_v run random value 1..5",
        "execute if score #pick rpg_l2_v = @s rpg_dm_last run scoreboard players add #pick rpg_l2_v 1",
        "execute if score #pick rpg_l2_v matches 6.. run scoreboard players set #pick rpg_l2_v 1",
        "scoreboard players operation @s rpg_dm_last = #pick rpg_l2_v",
        "scoreboard players set @s rpg_l2_st 3",
        "scoreboard players set @s rpg_l2_t 0",
        "scoreboard players operation @s rpg_l2_sk = #pick rpg_l2_v",
        "function %s/hold" % F,
        "scoreboard players set @s rpg_dm_cd %d" % GAP,
    ] + ["execute if score #pick rpg_l2_v matches %d run return run function %s/%s/start" % (n, F, d)
         for n, d, _ in SKILLS])
    w("skill/tick", ["scoreboard players add @s rpg_l2_t 1"] +
      ["execute if score @s rpg_l2_sk matches %d run return run function %s/%s/tick" % (n, F, d)
       for n, d, _ in SKILLS] +
      ["execute if score @s rpg_l2_sk matches 6 run return run function %s/ult/tick" % F,
       "execute if score @s rpg_l2_sk matches 9 run return run function %s/melee/tick" % F,
       "function %s/free" % F])
    w("ult/warn", [
        add_pact._notice(FORM, FORM["ultimate"], FORM["ult_text"], True, 18),
        "function %s/cancel" % F,
        "scoreboard players set @s rpg_l2_st 3",
        "scoreboard players set @s rpg_l2_sk 6",
        "scoreboard players set @s rpg_l2_t 0",
        "function %s/hold" % F,
        "function %sprojectileattack_start" % CLIP,
        "particle %s ~ ~3 ~ 2 2 2 0.04 50" % DUST_BIG,
        "playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..32] ~ ~ ~ 1 0.6",
    ] + prop("eden", "eden_faint", flat(0.01, 0.03)))


# ---------------------------------------------------------------------------
# 招式
# ---------------------------------------------------------------------------
def build_melee():
    # 碾：左臂连同村民雕像一起砸下。attack 的粒子通知在 1.536 秒，第 31 刻。
    w("melee/start", [
        "scoreboard players set @s rpg_l2_st 3",
        "scoreboard players set @s rpg_l2_sk 9",
        "scoreboard players set @s rpg_l2_t 0",
        "scoreboard players set @s rpg_l2_mc %d" % MELEE_CD,
        "function %s/hold" % F,
        "function %sattack" % CLIP,
    ])
    w("melee/tick", [
        at(31, "function %s/melee/impact" % F),
        at(50, "function %s/free" % F),
    ])
    w("melee/impact", [
        "tag @s add rpg.dm.cast",
        "execute positioned ^ ^ ^3 as @a[distance=..3.2,%s] run function %s/melee/hit" % (SURV, F),
        "tag @s remove rpg.dm.cast",
        "execute positioned ^ ^ ^3 run particle %s ~ ~0.3 ~ 1.6 0.2 1.6 0.15 60" % ROOT,
        "execute positioned ^ ^ ^3 run particle %s ~ ~0.5 ~ 1.2 0.3 1.2 0.05 30" % DUST,
        "execute positioned ^ ^ ^3 run particle explosion ~ ~0.5 ~ 0.6 0.2 0.6 0 2",
        "execute positioned ^ ^ ^3 run function %s/melee/fx" % F,
    ])
    w("melee/fx", prop("crack", "crack", flat(3.5, 0.04)) + prop("shock6", "shock_ring", flat(0.5, 0.06)))
    hit("melee/hit", 11, [("poison", 5, 0)], kind="minecraft:mob_attack")


def mark(tag_extra, life):
    return ("summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.lu2f.fx\",\"rpg.lu2f.mark\",\"rpg.lu2f.new\"%s]}"
            % "".join(',"%s"' % t for t in tag_extra), life)


def own_new(life):
    """刚召出的生成物：记领主编号与寿命。"""
    return ["scoreboard players operation @e[tag=rpg.lu2f.new] rpg_l2_id = @s rpg_l2_id",
            "scoreboard players set @e[tag=rpg.lu2f.new] rpg_l2_t %d" % life,
            "tag @e[tag=rpg.lu2f.new] remove rpg.lu2f.new"]


VINE = ('summon minecraft:block_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.vine","rpg.lu2f.new"],'
        'block_state:{Name:"minecraft:twisting_vines_plant"},teleport_duration:0,'
        'transformation:{translation:[-0.75f,-4.2f,-0.75f],left_rotation:[0f,0f,0f,1f],'
        'scale:[1.5f,4.2f,1.5f],right_rotation:[0f,0f,0f,1f]}}')
VINE_LIFE = 34


def build_vines():
    # 藤蔓本体：召出后下一刻升起，寿命剩 5 刻时缩回地下。
    w("vine/life", [
        "execute if score @s rpg_l2_t matches %d run data merge entity @s "
        "{start_interpolation:0,interpolation_duration:3,transformation:{translation:[-0.75f,0f,-0.75f],"
        "left_rotation:[0f,0f,0f,1f],scale:[1.5f,4.2f,1.5f],right_rotation:[0f,0f,0f,1f]}}" % (VINE_LIFE - 1),
        "execute if score @s rpg_l2_t matches 5 run data merge entity @s "
        "{start_interpolation:0,interpolation_duration:4,transformation:{translation:[-0.75f,-4.2f,-0.75f],"
        "left_rotation:[0f,0f,0f,1f],scale:[1.5f,4.2f,1.5f],right_rotation:[0f,0f,0f,1f]}}",
    ])
    w("vine/erupt", [
        "# as 预警标记 at 标记：原作藤蔓破土（add_lucifer_vine_model.py），并结算附近的人（领主此刻挂着 rpg.dm.cast）。",
        "# 藤蔓自带寿命：到点播消亡动作再清掉，领主没了也照样收场。",
        "function rpg:lucifer_vine/spawn",
        "scoreboard players set @e[type=minecraft:armor_stand,tag=rpg.luv.new,distance=..1] rpg_luv_l %d" % VINE_LIFE,
        "tag @e[type=minecraft:armor_stand,tag=rpg.luv.new,distance=..1] remove rpg.luv.new",
        "particle %s ~ ~0.3 ~ 0.6 0.2 0.6 0.12 24" % ROOT,
        "particle %s ~ ~1 ~ 0.4 1 0.4 0.03 10" % DUST,
    ] + prop("crack", "crack", flat(2.4, 0.04)) + [
        "execute positioned ~ ~1 ~ as @a[distance=..1.6,tag=!rpg.lu2f.hit,%s] run function %s/vine/hit_once" % (SURV, F),
        "kill @s",
    ])
    w("vine/hit_once", ["tag @s add rpg.lu2f.hit", "scoreboard players set #hit rpg_l2_v 1",
                        "function %s/vine/hit" % F])
    hit("vine/hit", 8, [("poison", 3, 0)], extra=["effect give @s minecraft:levitation 1 0 true"])
    w("vine/warn", [
        "# as 预警标记：地面上一圈苔绿，提示一秒后从这里破土。",
        "particle %s ~ ~0.15 ~ 0.55 0 0.55 0 6" % DUST_SMALL,
        "particle %s ~ ~0.1 ~ 0.5 0.05 0.5 0.05 4" % MOSS,
    ])
    w("vine/mark_player", [
        "# as 玩家 at 玩家：脚下一根，外加三角三根。",
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.lu2f.fx\",\"rpg.lu2f.mark\",\"rpg.lu2f.vmark\",\"rpg.lu2f.new\"]}",
        "summon minecraft:marker ~2.2 ~ ~ {Tags:[\"rpg.lu2f.fx\",\"rpg.lu2f.mark\",\"rpg.lu2f.vmark\",\"rpg.lu2f.new\"]}",
        "summon minecraft:marker ~-1.1 ~ ~1.9 {Tags:[\"rpg.lu2f.fx\",\"rpg.lu2f.mark\",\"rpg.lu2f.vmark\",\"rpg.lu2f.new\"]}",
        "summon minecraft:marker ~-1.1 ~ ~-1.9 {Tags:[\"rpg.lu2f.fx\",\"rpg.lu2f.mark\",\"rpg.lu2f.vmark\",\"rpg.lu2f.new\"]}",
        "function %s/vine/mark_fx" % F,
        "execute positioned ~2.2 ~ ~ run function %s/vine/mark_fx" % F,
        "execute positioned ~-1.1 ~ ~1.9 run function %s/vine/mark_fx" % F,
        "execute positioned ~-1.1 ~ ~-1.9 run function %s/vine/mark_fx" % F,
    ])
    w("vine/mark_fx", prop("vmark", "vine_mark", flat(0.01)))

    # 缠枝：右臂抽进地里，四到十根藤蔓从玩家脚下破土；全部落空就露出破绽。
    n = SKILLS[0][2]
    w("vine/start", [
        clue(n), notice(*FORM["skills"][0]),
        "function %svineattack" % CLIP,
        "scoreboard players set @s rpg_l2_v 0",
        "scoreboard players set #hit rpg_l2_v 0",
        "tag @a remove rpg.lu2f.hit",
        "execute as @a[distance=..16,%s,limit=4,sort=nearest] at @s run function %s/vine/mark_player" % (SURV, F),
    ] + own_new(30))
    w("vine/tick", [
        "scoreboard players operation #id rpg_l2_id = @s rpg_l2_id",
        "execute if score @s rpg_l2_t matches 1 run function %s/vine/warn_all" % F,
        "execute if score @s rpg_l2_t matches 5 run function %s/vine/warn_all" % F,
        "execute if score @s rpg_l2_t matches 9 run function %s/vine/warn_all" % F,
        "execute if score @s rpg_l2_t matches 13 run function %s/vine/warn_all" % F,
        "execute if score @s rpg_l2_t matches 17 run function %s/vine/warn_all" % F,
        at(22, "function %s/vine/burst" % F),
        at(38, "function %svineattackidle" % CLIP),
        "execute if score @s rpg_l2_t matches 58 if score @s rpg_l2_v matches 1 run function %svineattacksucessful" % CLIP,
        "execute if score @s rpg_l2_t matches 58 unless score @s rpg_l2_v matches 1 run function %svineattackunsucessful" % CLIP,
        "execute if score @s rpg_l2_t matches 95 if score @s rpg_l2_v matches 1 run return run function %s/free" % F,
        "execute if score @s rpg_l2_t matches 88 unless score @s rpg_l2_v matches 1 run function %s/vuln/start" % F,
    ])
    w("vine/warn_all", ["execute as @e[type=minecraft:marker,tag=rpg.lu2f.vmark] if score @s rpg_l2_id = #id rpg_l2_id at @s run function %s/vine/warn" % F])
    w("vine/burst", [
        "tag @s add rpg.dm.cast",
        "execute as @e[type=minecraft:marker,tag=rpg.lu2f.vmark] if score @s rpg_l2_id = #id rpg_l2_id at @s run function %s/vine/erupt" % F,
        "tag @s remove rpg.dm.cast",
        "playsound rpg:lucifer_p2.vine_burst_new hostile @a[distance=..32] ~ ~ ~ 1.2 1",
        "scoreboard players operation @s rpg_l2_v = #hit rpg_l2_v",
        "tag @a remove rpg.lu2f.hit",
    ])


DART_SPEED = 0.9
DART_LIFE = 24


def dart_summons(count, offset_deg, y=1.4):
    """原作毒刺弹（add_lucifer_props.py 的 quill），刺尖转到飞行方向。"""
    out = []
    for i in range(count):
        yaw = (offset_deg + 360.0 * i / count) % 360 - 180
        out.append('summon minecraft:item_display ~ ~%s ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.dart","rpg.lu2f.new"],'
                   'Rotation:[%.1ff,0f],teleport_duration:1,brightness:{sky:15,block:15},view_range:2f,'
                   'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_props/quill"}},'
                   'transformation:{%s}}'
                   % (y, yaw, xf(q=props.QUILL_ROTATION, s=(props.SCALE,) * 3)))
    return out


def build_fruit():
    # 禁果：原作的两圈毒镖，每圈十二枚。
    w("dart/step", [
        "tp @s ^ ^ ^%s" % DART_SPEED,
        "particle %s ~ ~ ~ 0.05 0.05 0.05 0 1" % DUST_SMALL,
        "execute unless block ~ ~ ~ #minecraft:replaceable run return run function %s/dart/pop" % F,
        "execute positioned ~ ~-0.9 ~ if entity @a[distance=..1,%s] run function %s/dart/strike" % (SURV, F),
    ])
    w("dart/strike", [
        "execute positioned ~ ~-0.9 ~ as @a[distance=..1,%s,limit=1,sort=nearest] run function %s/dart/hit" % (SURV, F),
        "function %s/dart/pop" % F,
    ])
    w("dart/pop", ["particle %s ~ ~ ~ 0.15 0.15 0.15 0.05 6" % DUST_SMALL] +
      sprite("burst", xf(s=(glyph_scale("burst", 1.2),) * 3)) + ["kill @s"])
    hit("dart/hit", 4, [("poison", 5, 0)])
    n = SKILLS[1][2]
    w("fruit/start", [clue(n), notice(*FORM["skills"][1]), "function %sprojectileattack_start" % CLIP])
    w("fruit/tick", [
        at(23, "function %sprojectileattack_loop" % CLIP),
        at(23, "function %s/fruit/ring1" % F),
        at(40, "function %s/fruit/ring2" % F),
        at(57, "function %sprojectileattack_end" % CLIP),
        at(68, "function %s/free" % F),
    ])
    for ring, off in (("ring1", 0), ("ring2", 15)):
        w("fruit/" + ring, dart_summons(12, off) + own_new(DART_LIFE) + [
            "playsound minecraft:entity.llama.spit hostile @a[distance=..32] ~ ~ ~ 1.2 0.6",
            "particle %s ~ ~1.5 ~ 1.2 0.6 1.2 0.05 24" % DUST,
        ])


SPIRITS = ["bael", "agares", "vassago", "samigina", "marbas"]


def build_tempt():
    # 诱惑：从根下唤出罪仆，近处的人被拉向树。
    n = SKILLS[2][2]
    w("tempt/start", [clue(n), notice(*FORM["skills"][2]), "function %ssummon" % CLIP])
    w("tempt/tick", [
        at(13, "function %s/tempt/call" % F),
        at(36, "function %s/free" % F),
    ])
    w("tempt/call", [
        "scoreboard players operation #id rpg_l2_id = @s rpg_l2_id",
        "scoreboard players set #n rpg_l2_v 0",
        "execute as @e[tag=rpg.lu2f.minion] if score @s rpg_l2_id = #id rpg_l2_id run scoreboard players add #n rpg_l2_v 1",
        "execute if score #n rpg_l2_v matches ..2 positioned ^2 ^ ^1 run function %s/tempt/one" % F,
        "execute if score #n rpg_l2_v matches ..1 positioned ^-2 ^ ^1 run function %s/tempt/one" % F,
        "tag @s add rpg.dm.cast",
        "execute as @a[distance=..12,%s] at @e[tag=rpg.dm.cast,limit=1] positioned ~ ~4.5 ~ facing entity @s eyes run function %s/fx/line" % (SURV, F),
        "execute as @a[distance=..12,%s] at @s run function %s/tempt/pull" % (SURV, F),
        "tag @s remove rpg.dm.cast",
        "particle %s ~ ~0.3 ~ 3 0.2 3 0.1 50" % ROOT,
    ])
    w("tempt/one", [
        "execute store result score #s rpg_l2_v run random value 1..5",
    ] + ["execute if score #s rpg_l2_v matches %d run function rpg:minion/summon/lucifer/%s" % (i, s)
         for i, s in enumerate(SPIRITS, 1)] + [
        "tag @e[tag=rpg.demon.minion,tag=!rpg.lu2f.minion,distance=..2,limit=1,sort=nearest] add rpg.lu2f.new_minion",
        "scoreboard players operation @e[tag=rpg.lu2f.new_minion] rpg_l2_id = #id rpg_l2_id",
        "tag @e[tag=rpg.lu2f.new_minion] add rpg.lu2f.minion",
        "tag @e[tag=rpg.lu2f.new_minion] remove rpg.lu2f.new_minion",
        "particle %s ~ ~0.4 ~ 0.6 0.3 0.6 0.1 30" % ROOT,
    ] + prop("smark", "vine_mark", flat(0.01)))
    w("tempt/pull", [
        "execute facing entity @e[tag=rpg.dm.cast,limit=1] feet if block ^ ^ ^1.5 #minecraft:replaceable "
        "if block ^ ^1 ^1.5 #minecraft:replaceable run tp @s ^ ^ ^1.5",
        "function %s/tempt/hit" % F,
    ])
    holy_pair("tempt/hit", ["effect give @s minecraft:nausea 4 0 true"],
              ["effect give @s minecraft:nausea 2 0 true"])


def build_fall():
    # 坠天：锁定最近的人跃起，空中摆 fall，落地 land 冲击。
    n = SKILLS[3][2]
    w("fall/start", [
        clue(n), notice(*FORM["skills"][3]),
        "scoreboard players set @s rpg_l2_v 0",
        "execute at @a[distance=..20,%s,limit=1,sort=nearest] run summon minecraft:marker ~ ~ ~ "
        "{Tags:[\"rpg.lu2f.fx\",\"rpg.lu2f.mark\",\"rpg.lu2f.lmark\",\"rpg.lu2f.new\"]}" % SURV,
    ] + own_new(90) + [
        "execute at @a[distance=..20,%s,limit=1,sort=nearest] run function %s/fall/mark_fx" % (SURV, F),
        "function %sfall" % CLIP])
    w("fall/mark_fx", prop("fmark", "fall_mark", flat(0.01), tags=("rpg.lu2f.fm",)))
    w("fall/tick", [
        "scoreboard players operation #id rpg_l2_id = @s rpg_l2_id",
        "execute if score @s rpg_l2_t matches ..60 as @e[type=minecraft:marker,tag=rpg.lu2f.lmark] if score @s rpg_l2_id = #id rpg_l2_id at @s run function %s/fall/warn" % F,
        at(8, "function %s/fall/leap" % F),
        "execute if score @s rpg_l2_t matches 15..60 if score @s rpg_l2_v matches 0 if predicate %s run function %s/fall/land" % (
            "rpg:lucifer_fight/on_ground", F),
        "execute if score @s rpg_l2_t matches 61 if score @s rpg_l2_v matches 0 run function %s/fall/land" % F,
        "execute if score @s rpg_l2_t matches 15..60 if score @s rpg_l2_v matches 0 if score @s rpg_l2_t matches 15 run function %sfall" % CLIP,
        "execute if score @s rpg_l2_t matches 15..60 if score @s rpg_l2_v matches 0 if score @s rpg_l2_t matches 22 run function %sfall" % CLIP,
        "execute if score @s rpg_l2_t matches 15..60 if score @s rpg_l2_v matches 0 if score @s rpg_l2_t matches 29 run function %sfall" % CLIP,
        "execute if score @s rpg_l2_v matches 1.. run scoreboard players add @s rpg_l2_v 1",
        "execute if score @s rpg_l2_v matches 60.. run function %s/free" % F,
    ])
    w("fall/warn", ["particle %s ~ ~0.15 ~ 2.6 0 2.6 0 10" % DUST_SMALL,
                    "particle %s ~ ~0.1 ~ 2.4 0.05 2.4 0.05 4" % MOSS])
    w("fall/leap", [
        "# 水平初速按落点距离算：空中约 26 刻，横向阻力 0.91，总位移约为初速的 10.15 倍。",
        "scoreboard players set @s rpg_l2_v 0",
        "execute store result score #bx rpg_l2_v run data get entity @s Pos[0] 100",
        "execute store result score #bz rpg_l2_v run data get entity @s Pos[2] 100",
        "scoreboard players set #mx rpg_l2_v 0",
        "scoreboard players set #mz rpg_l2_v 0",
        "scoreboard players operation #mx rpg_l2_v = #bx rpg_l2_v",
        "scoreboard players operation #mz rpg_l2_v = #bz rpg_l2_v",
        "execute as @e[type=minecraft:marker,tag=rpg.lu2f.lmark] if score @s rpg_l2_id = #id rpg_l2_id store result score #mx rpg_l2_v run data get entity @s Pos[0] 100",
        "execute as @e[type=minecraft:marker,tag=rpg.lu2f.lmark] if score @s rpg_l2_id = #id rpg_l2_id store result score #mz rpg_l2_v run data get entity @s Pos[2] 100",
        "scoreboard players operation #mx rpg_l2_v -= #bx rpg_l2_v",
        "scoreboard players operation #mz rpg_l2_v -= #bz rpg_l2_v",
        "execute if score #mx rpg_l2_v matches 1401.. run scoreboard players set #mx rpg_l2_v 1400",
        "execute if score #mx rpg_l2_v matches ..-1401 run scoreboard players set #mx rpg_l2_v -1400",
        "execute if score #mz rpg_l2_v matches 1401.. run scoreboard players set #mz rpg_l2_v 1400",
        "execute if score #mz rpg_l2_v matches ..-1401 run scoreboard players set #mz rpg_l2_v -1400",
        "attribute @s minecraft:movement_speed modifier remove rpg:lu2f_hold",
        "execute store result entity @s Motion[0] double 0.000985 run scoreboard players get #mx rpg_l2_v",
        "execute store result entity @s Motion[2] double 0.000985 run scoreboard players get #mz rpg_l2_v",
        "data modify entity @s Motion[1] set value 1.1d",
        "function %s/hold" % F,
        "playsound minecraft:entity.ender_dragon.flap hostile @a[distance=..40] ~ ~ ~ 1.4 0.6",
        "particle %s ~ ~0.3 ~ 2 0.2 2 0.15 50" % ROOT,
    ])
    w("fall/land", [
        "scoreboard players set @s rpg_l2_v 1",
        "function %sland" % CLIP,
        "scoreboard players operation #id rpg_l2_id = @s rpg_l2_id",
        "execute as @e[type=minecraft:marker,tag=rpg.lu2f.lmark] if score @s rpg_l2_id = #id rpg_l2_id run kill @s",
        "tag @s add rpg.dm.cast",
        "execute as @a[distance=..5.5,%s] run function %s/fall/hit" % (SURV, F),
        "tag @s remove rpg.dm.cast",
        "particle %s ~ ~0.3 ~ 3 0.2 3 0.2 120" % ROOT,
        "particle %s ~ ~0.6 ~ 3 0.4 3 0.06 60" % DUST_BIG,
        "particle explosion_emitter ~ ~0.5 ~ 0 0 0 0 1",
        "playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1 0.6",
        "kill @e[type=minecraft:item_display,tag=rpg.lu2f.fm,distance=..16]",
    ] + prop("shock11", "shock_ring", flat(0.5, 0.06)) + prop("crack", "crack", flat(6, 0.04)) + [
        "execute positioned ~ ~1 ~ run function %s/fx/debris" % F])
    hit("fall/hit", 12, [("slowness", 3, 1)], extra=[push_back(3)])


def build_gaze():
    # 知善恶：树睁开眼；结算时正在看它的人受罚，移开视线就没事。
    n = SKILLS[4][2]
    w("gaze/start", [
        clue(n), notice(*FORM["skills"][4]),
        "function %svineattackidle" % CLIP,
        "playsound minecraft:block.sculk_shrieker.shriek hostile @a[distance=..32] ~ ~ ~ 0.9 0.6",
        "execute positioned ~ ~8.4 ~ run function %s/gaze/eye" % F,
    ])
    w("gaze/eye", sprite("eye", xf(s=(glyph_scale("eye", 4.8),) * 3)))
    w("gaze/tick", [
        "execute if score @s rpg_l2_t matches ..%d run particle %s ~ ~4.6 ~ 0.6 0.25 0.6 0 3" % (GAZE_AT - 1, DUST_SMALL),
        at(15, "playsound minecraft:block.sculk_shrieker.shriek hostile @a[distance=..32] ~ ~ ~ 1 0.75"),
        at(GAZE_AT, "function %s/gaze/judge" % F),
        at(GAZE_AT, "function %svineattacksucessful" % CLIP),
        at(GAZE_AT + 37, "function %s/free" % F),
    ])
    # 视线检测：从玩家眼睛往前每 2 格取一点，落进领主身周 3×6×3 的盒子就算在看。
    ray = ["execute positioned ^ ^ ^%d positioned ~-1.5 ~-5 ~-1.5 if entity @e[tag=rpg.dm.cast,dx=2,dy=5,dz=2] run tag @s add rpg.lu2f.saw" % d
           for d in range(2, 22, 2)]
    w("gaze/look", ray)
    w("gaze/judge", [
        "tag @s add rpg.dm.cast",
        "tag @a remove rpg.lu2f.saw",
        "execute as @a[distance=..22,%s] at @s anchored eyes run function %s/gaze/look" % (SURV, F),
        "execute as @a[tag=rpg.lu2f.saw] positioned ~ ~8.4 ~ facing entity @s eyes run function %s/fx/gline" % F,
        "execute as @a[tag=rpg.lu2f.saw] run function %s/gaze/hit" % F,
        "tag @a remove rpg.lu2f.saw",
        "tag @s remove rpg.dm.cast",
        "particle flash{color:%d} ~ ~4.5 ~ 0 0 0 0 1" % int(LIT.lstrip("#"), 16),
        "particle %s ~ ~4.5 ~ 1 0.5 1 0.1 40" % DUST,
        "playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..32] ~ ~ ~ 0.8 0.7",
    ])
    hit("gaze/hit", 7, [("blindness", 3, 0), ("slowness", 3, 1)])


ULT_RINGS = [(12, 3, 8), (18, 6, 10), (24, 9, 12)]   # 刻、半径、根数


def build_ult():
    # 失乐园：蓄 30 刻，先一圈 24 枚果核，再从近到远破土三圈藤蔓。
    w("ult/tick", [
        "scoreboard players operation #id rpg_l2_id = @s rpg_l2_id",
        at(23, "function %sprojectileattack_loop" % CLIP),
        "execute if score @s rpg_l2_t matches ..29 run particle %s ~ ~3 ~ 1.5 1.5 1.5 0.03 4" % DUST_BIG,
        at(30, "function %s/ult/resolve" % F),
        "execute if score @s rpg_l2_t matches 31..53 run function %s/ult/warn_rings" % F,
    ] + [at(30 + t, "function %s/ult/ring%d" % (F, i)) for i, (t, _, _) in enumerate(ULT_RINGS, 1)] + [
        at(68, "function %svineattackidle" % CLIP),
        at(80, "function %svineattacksucessful" % CLIP),
        at(117, "function %s/free" % F),
    ])
    w("ult/resolve", dart_summons(16, 11.25) + own_new(DART_LIFE) + [
        "function %svineattack" % CLIP,
        "playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..40] ~ ~ ~ 0.9 0.6",
        "particle %s ~ ~1 ~ 5 1 5 0.04 120" % ui.pillar_transition(1, 2.8),
    ] + ["summon minecraft:marker ^%.2f ^ ^%.2f {Tags:[\"rpg.lu2f.fx\",\"rpg.lu2f.mark\",\"rpg.lu2f.r%d\",\"rpg.lu2f.new\"]}"
         % (r * math.sin(2 * math.pi * k / c), r * math.cos(2 * math.pi * k / c), i)
         for i, (_, r, c) in enumerate(ULT_RINGS, 1) for k in range(c)] + own_new(60))
    w("ult/warn_rings", [
        "execute if score @s rpg_l2_t matches 31 run function %s/ult/warn_all" % F,
        "execute if score @s rpg_l2_t matches 36 run function %s/ult/warn_all" % F,
        "execute if score @s rpg_l2_t matches 41 run function %s/ult/warn_all" % F,
        "execute if score @s rpg_l2_t matches 46 run function %s/ult/warn_all" % F,
    ])
    w("ult/warn_all", ["execute as @e[type=minecraft:marker,tag=rpg.lu2f.mark,tag=!rpg.lu2f.vmark,tag=!rpg.lu2f.lmark] "
                       "if score @s rpg_l2_id = #id rpg_l2_id at @s run function %s/vine/warn" % F])
    for i in range(1, len(ULT_RINGS) + 1):
        w("ult/ring%d" % i, [
            "tag @a remove rpg.lu2f.hit",
            "tag @s add rpg.dm.cast",
            "execute as @e[type=minecraft:marker,tag=rpg.lu2f.r%d] if score @s rpg_l2_id = #id rpg_l2_id at @s run function %s/ult/erupt" % (i, F),
            "tag @s remove rpg.dm.cast",
            "tag @a remove rpg.lu2f.hit",
            "playsound rpg:lucifer_p2.vine_burst_new hostile @a[distance=..40] ~ ~ ~ 1.3 %s" % ("1", "0.9", "0.8")[i - 1],
        ])
    w("ult/erupt", ["# 原作藤臂（add_lucifer_props.py 的 spike）从地下升起，约 3.7 格。"] +
      prop("spike", "rpg:lucifer_props/spike", xf(t=(0, -3.9, 0), s=(props.SCALE,) * 3), "Rotation:[%gf,0f]," % 37) + [
        "particle %s ~ ~0.3 ~ 0.6 0.2 0.6 0.12 16" % ROOT,
        "execute positioned ~ ~1 ~ as @a[distance=..1.8,tag=!rpg.lu2f.hit,%s] run function %s/ult/hit_once" % (SURV, F),
        "kill @s",
    ])
    w("ult/hit_once", ["tag @s add rpg.lu2f.hit", "function %s/ult/hit" % F])
    hit("ult/hit", 10, [("poison", 2, 0)], extra=["effect give @s minecraft:levitation 1 1 true"])


def build_states():
    # 破绽：缠枝全部落空时花心张开。倒下与晕眩期间护甲归零，起身时恢复。
    w("vuln/start", [
        "scoreboard players set @s rpg_l2_st 4",
        "scoreboard players set @s rpg_l2_t 0",
        "attribute @s minecraft:armor modifier remove rpg:lu2f_open",
        "attribute @s minecraft:armor modifier add rpg:lu2f_open -1 add_multiplied_total",
        "function %svulnerablefall" % CLIP,
        say("根须落空，花心张开了。"),
        "execute positioned ~ ~5 ~ run function %s/vuln/pollen" % F,
    ])
    w("vuln/pollen", sprite("pollen", xf(s=(glyph_scale("pollen", 3),) * 3)))
    w("vuln/tick", [
        "scoreboard players add @s rpg_l2_t 1",
        at(36, "function %svulnerablestuncycle" % CLIP),
        at(96, "attribute @s minecraft:armor modifier remove rpg:lu2f_open"),
        at(96, "function %svulnerablegetup" % CLIP),
        at(173, "function %s/free" % F),
    ])
    # 捆绑：驱魔法阵按住它时倒地并循环晕眩，离开捆绑后起身。
    w("bound/tick", [
        "execute unless entity @s[tag=rpg.lu2f.bound] run function %s/bound/enter" % F,
        "scoreboard players add @s rpg_l2_t 1",
        at(36, "function %svulnerablestuncycle" % CLIP),
    ])
    w("bound/enter", [
        "function %s/cancel" % F,
        "tag @s add rpg.lu2f.bound",
        "scoreboard players set @s rpg_l2_st 5",
        "scoreboard players set @s rpg_l2_t 0",
        "function %svulnerablefall" % CLIP,
    ])
    w("bound/leave", [
        "tag @s remove rpg.lu2f.bound",
        "scoreboard players set @s rpg_l2_st 4",
        "scoreboard players set @s rpg_l2_t 95",
    ])


# ---------------------------------------------------------------------------
# 一阶段「晨星之蛇」（docs/LUCIFER-P2-DESIGN.md §6）
# 招式名、罪证、HUD 提示和伤害数值沿用原来的 sk1_1..5 与 ult1；这里给它们加上
# 预警、对准动作的出手时刻和展示实体特效。原命中函数 taint/sk1b_hit 等直接复用，
# 它们已经带圣器减半分支与 record_magic。
#
# GPT 的一阶段动作里 attack、strong、cast 从出手那一帧开始（裁掉了起手），
# 所以预警由特效承担，伤害落在动作第 0 刻；slash 有完整起手，第 8 刻扫到。
# ---------------------------------------------------------------------------
P1 = "%s/p1" % F
LORD_CLIP = "rpg:lucifer_lord/play/"
DUI = add_pact.DEMON_UI[1]
P1_MELEE_CD = 50
P1_MELEE_RANGE = 4
SLASH_HIT = 8
# 平面字形的朝向：长边沿实体前方（+z）。两片竖直面分朝左右，一片水平面朝上。
Q_SIDE_A = (0, -0.7071068, 0, 0.7071068)
Q_SIDE_B = (0, 0.7071068, 0, 0.7071068)
Q_LID = (-0.5, -0.5, -0.5, 0.5)
P1_SKILLS = [(11, "sin", 1), (12, "spear", 2), (13, "high", 3), (14, "fall", 4), (15, "throne", 5)]
ALONG = ("execute as @e[type=minecraft:marker,tag=rpg.lu1f.aim] if score @s rpg_l2_id = #id rpg_l2_id "
         "rotated as @s as @e[tag=rpg.lu1f.self,limit=1] at @s rotated ~ 0 run function %s/%s")


def p1_notice(i):
    name, phrase = DUI["skills"][i - 1]
    return add_pact._notice(DUI, name, phrase)


def oriented(lines):
    """把刚召出的、带 rpg.lu1f.orient 的特效转到当前执行朝向（只看 yaw）。"""
    return lines + ["execute as @e[tag=rpg.lu1f.orient] run tp @s ~ ~ ~ ~ 0",
                    "tag @e[tag=rpg.lu1f.orient] remove rpg.lu1f.orient"]


def with_self(lines):
    """沿锁定方向执行：领主临时挂 rpg.lu1f.self，好让 ALONG 回到领主身上。"""
    return (["scoreboard players operation #id rpg_l2_id = @s rpg_l2_id", "tag @s add rpg.lu1f.self"] + lines +
            ["tag @s remove rpg.lu1f.self"])


def along(fn):
    return ALONG % (P1, fn)


def build_p1_core():
    w("p1/tick", [
        "# 一阶段每刻（as 领主）。原版近战归零：普攻改由对得上动作的「刺」。",
        "execute if entity @s[tag=!rpg.lu1f.init] run function %s/init" % P1,
        "execute unless score @s rpg_l2_id matches 1.. run function %s/new_id" % F,
        "execute unless score @s rpg_l2_st matches 2 if score @s rpg_dm_cd matches ..%d run scoreboard players set @s rpg_dm_cd %d" % (GAP - 1, GAP),
        "execute if score @s rpg_l2_st matches 3 run return run function %s/skill" % P1,
        "scoreboard players set @s rpg_l2_st 2",
        "execute if score @s rpg_l2_mc matches 1.. run scoreboard players remove @s rpg_l2_mc 1",
        "execute if score @s rpg_l2_mc matches ..0 if score @s rpg_dm_ult matches ..0 "
        "if entity @a[distance=..%d,%s] run function %s/jab/start" % (P1_MELEE_RANGE, SURV, P1),
    ])
    w("p1/init", [
        "tag @s add rpg.lu1f.init",
        "attribute @s minecraft:attack_damage modifier remove rpg:lu2f_melee",
        "attribute @s minecraft:attack_damage modifier add rpg:lu2f_melee -1 add_multiplied_total",
    ])
    w("p1/cast", [
        "# 五招掷一招，撞上一招就顺延。",
        "execute store result score #pick rpg_l2_v run random value 1..5",
        "execute if score #pick rpg_l2_v = @s rpg_dm_last run scoreboard players add #pick rpg_l2_v 1",
        "execute if score #pick rpg_l2_v matches 6.. run scoreboard players set #pick rpg_l2_v 1",
        "scoreboard players operation @s rpg_dm_last = #pick rpg_l2_v",
        "function %s/begin" % P1,
        "scoreboard players set @s rpg_dm_cd %d" % GAP,
    ] + ["execute if score #pick rpg_l2_v matches %d run return run function %s/%s/start" % (c, P1, d)
         for _, d, c in P1_SKILLS])
    w("p1/begin", [
        "scoreboard players set @s rpg_l2_st 3",
        "scoreboard players set @s rpg_l2_t 0",
        "scoreboard players operation @s rpg_l2_sk = #pick rpg_l2_v",
        "scoreboard players add @s rpg_l2_sk 10",
        "function %s/hold" % F,
    ])
    w("p1/skill", ["scoreboard players add @s rpg_l2_t 1"] +
      ["execute if score @s rpg_l2_sk matches %d run return run function %s/%s/tick" % (n, P1, d) for n, d, _ in P1_SKILLS] +
      ["execute if score @s rpg_l2_sk matches 16 run return run function %s/ult/tick" % P1,
       "execute if score @s rpg_l2_sk matches 19 run return run function %s/jab/tick" % P1,
       "function %s/free" % F])
    # 锁定方向：一个记着朝向的 marker，之后的预警和出手都沿它。
    w("p1/aim", [
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.lu2f.fx\",\"rpg.lu2f.mark\",\"rpg.lu1f.aim\",\"rpg.lu2f.new\"]}",
        "execute as @e[type=minecraft:marker,tag=rpg.lu2f.new,tag=rpg.lu1f.aim] at @s "
        "facing entity @a[distance=..24,%s,limit=1,sort=nearest] feet run tp @s ~ ~ ~ ~ 0" % SURV,
    ] + own_new(60))
    w("p1/fx/glint", sprite("glint", xf(s=(glyph_scale("glint", 0.9),) * 3)))
    w("p1/fx/crown", sprite("crown", xf(s=(glyph_scale("crown", 1.8),) * 3)))
    w("p1/fx/burst_small", sprite("burst", xf(s=(glyph_scale("burst", 2.4),) * 3)))
    w("p1/fx/slash", sprite("slash", xf(s=(glyph_scale("slash", 3.6),) * 3)))


def build_p1_skills():
    glint = "execute positioned ^-0.4 ^2.1 ^0.9 run function %s/fx/glint" % P1

    # 刺（普攻）：寒光一闪，第 5 刻刺出
    w("p1/jab/start", [
        "scoreboard players set @s rpg_l2_st 3", "scoreboard players set @s rpg_l2_sk 19",
        "scoreboard players set @s rpg_l2_t 0", "scoreboard players set @s rpg_l2_mc %d" % P1_MELEE_CD,
        "function %s/hold" % F, glint,
    ])
    w("p1/jab/tick", [
        at(5, "function %sattack" % LORD_CLIP),
        at(5, "function %s/jab/hit" % P1),
        at(20, "function %s/free" % F),
    ])
    w("p1/jab/hit", [
        "tag @s add rpg.dm.cast",
        "execute positioned ^ ^ ^1.8 as @a[distance=..1.8,%s] run function %s/jab/dmg" % (SURV, P1),
        "tag @s remove rpg.dm.cast",
        "execute positioned ^ ^1.2 ^1.8 run particle %s ~ ~ ~ 0.3 0.3 0.3 0.05 10" % DUST,
        "execute positioned ^ ^1.2 ^1.8 run particle crit ~ ~ ~ 0.3 0.3 0.3 0.2 8",
    ])
    w("p1/jab/dmg", hit_lines(9, [], "minecraft:mob_attack"))

    # 原罪：蛇行预警带 → 第 12 刻矛插地 → 一路尖牙
    w("p1/sin/start", [clue(1), p1_notice(1), "function %s/aim" % P1] + with_self([along("sin/warn")]))
    w("p1/sin/warn", ["execute positioned ^ ^ ^4.5 run function %s/sin/trail" % P1])
    w("p1/sin/trail", oriented(prop("trail", "serpent_trail", xf(t=(0, 0.05, 0), s=(1.6, 1, 9)), tags=("rpg.lu1f.orient",))))
    w("p1/sin/tick", [at(12, "function %sstrong" % LORD_CLIP)] +
      [at(12, l) for l in with_self([along("sin/fire")])] + [at(32, "function %s/free" % F)])
    w("p1/sin/fire", [
        "data modify storage rpg:demon uuid set from entity @s UUID",
        "function rpg:taint/sk1_line with storage rpg:demon",
        "playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..32] ~ ~ ~ 1 0.7",
        "particle %s ~ ~1 ~ 0.6 0.8 0.6 0.05 30" % DUST,
    ] + prop("crack", "crack", flat(2.4, 0.04)))

    # 蛇矛：矛尖寒光与贯穿预警 → 第 12 刻刺出，光带贯穿 9 格
    w("p1/spear/start", [clue(2), p1_notice(2), "function %s/aim" % P1, glint] + with_self([along("spear/warn")]))
    w("p1/spear/warn", ["execute positioned ^ ^ ^5 run function %s/spear/mark" % P1])
    w("p1/spear/mark", oriented(prop("tmark", "thrust_mark", xf(t=(0, 0.05, 0), s=(1.4, 1, 9)), tags=("rpg.lu1f.orient",))))
    w("p1/spear/tick", [at(12, "function %sattack" % LORD_CLIP)] +
      [at(12, l) for l in with_self([along("spear/fire")])] + [at(30, "function %s/free" % F)])
    w("p1/spear/fire", [
        "tag @s add rpg.dm.cast",
        "execute positioned ^ ^1.2 ^ run function rpg:taint/sk1b_thrust",
        "tag @s remove rpg.dm.cast",
        "playsound minecraft:entity.breeze.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.6",
        "execute positioned ^ ^1.3 ^5 run function %s/spear/beam" % P1,
    ])
    beam = []
    for q in (Q_SIDE_A, Q_SIDE_B, Q_LID):
        beam += sprite("spear_beam", xf(q=q, s=(glyph_scale("spear_beam", 9), 1.4, 1)), billboard="fixed",
                       tags=("rpg.lu1f.orient",))
    w("p1/spear/beam", oriented(beam))

    # 高踞：头顶晨星王冠、脚下王冠圈 → 第 18 刻众生被举起
    w("p1/high/start", [clue(3), p1_notice(3), "execute positioned ~ ~3.1 ~ run function %s/fx/crown" % P1] +
      prop("cring", "crown_ring", flat(0.01)))
    w("p1/high/tick", [
        at(18, "function %scast" % LORD_CLIP),
        at(18, "function %s/high/fire" % P1),
        at(34, "function %s/free" % F),
    ])
    w("p1/high/fire", [
        "tag @s add rpg.dm.cast",
        "execute as @a[distance=..8,%s] run function rpg:taint/sk1c_lift" % SURV,
        "tag @s remove rpg.dm.cast",
        "execute as @a[distance=..8,%s] at @s run function %s/fx/burst_small" % (SURV, P1),
        "playsound minecraft:entity.illusioner.prepare_blindness hostile @a[distance=..32] ~ ~ ~ 1 0.6",
        "particle end_rod ~ ~1 ~ 3 1 3 0.1 40",
        "particle %s ~ ~1 ~ 3 1 3 0.05 30" % DUST,
    ])

    # 失坠：折断的羽毛从天落下 → 第 20 刻矛砸地
    feathers = []
    for k in range(8):
        a = 2 * math.pi * k / 8
        feathers.append("execute positioned ~%.2f ~6.5 ~%.2f run function %s/fall/feather"
                        % (3.5 * math.sin(a), 3.5 * math.cos(a), P1))
    w("p1/fall/start", [clue(4), p1_notice(4)] + prop("fmark16", "fall_mark", flat(0.01)) + feathers +
      ["playsound minecraft:entity.phantom.flap hostile @a[distance=..32] ~ ~ ~ 1 0.55"])
    w("p1/fall/feather", prop("feather", "feather", xf(s=(1.2, 1.2, 1.2)), "Rotation:[30f,0f],"))
    w("p1/fall/tick", [
        at(20, "function %sstrong" % LORD_CLIP),
        at(20, "function %s/fall/fire" % P1),
        at(40, "function %s/free" % F),
    ])
    w("p1/fall/fire", [
        "tag @s add rpg.dm.cast",
        "execute as @a[distance=..8,%s] run function rpg:taint/sk1d_fall" % SURV,
        "tag @s remove rpg.dm.cast",
        "playsound minecraft:entity.ender_dragon.flap hostile @a[distance=..32] ~ ~ ~ 0.7 1.45",
        "particle %s ~ ~0.3 ~ 3 0.2 3 0.15 60" % ROOT,
        "particle dragon_breath ~ ~1.5 ~ 3 1.2 3 0.08 40",
    ] + prop("shock16", "shock_ring", flat(0.5, 0.06)) + prop("crack", "crack", flat(5, 0.04)))

    # 王座回绝：横扫（slash 第 8 刻扫到），近身者被推开
    w("p1/throne/start", [clue(5), p1_notice(5), "function %sslash" % LORD_CLIP] + prop("cring12", "crown_ring", flat(0.01)))
    w("p1/throne/tick", [at(SLASH_HIT, "function %s/throne/fire" % P1), at(22, "function %s/free" % F)])
    w("p1/throne/fire", [
        "tag @s add rpg.dm.cast",
        "execute as @a[distance=..6,%s] at @s run function rpg:taint/sk1e_reject" % SURV,
        "tag @s remove rpg.dm.cast",
        "playsound minecraft:block.beacon.deactivate hostile @a[distance=..32] ~ ~ ~ 1 0.55",
        "particle end_rod ~ ~1.5 ~ 2.5 1 2.5 0.08 30",
        "particle %s ~ ~1 ~ 2.5 0.6 2.5 0.05 30" % DUST,
        "execute positioned ^ ^1.4 ^1.5 run function %s/fx/slash" % P1,
    ] + prop("shock12", "shock_ring", flat(0.5, 0.06)))

    # 万蛇加冕（罪约）：大笑蓄势、地面万蛇法阵 → 第 30 刻三圈蛇牙同时破土
    w("p1/ult/warn", [
        add_pact._notice(DUI, DUI["ultimate"], DUI["ult_text"], True, 18),
        "function %s/cancel" % F,
        "scoreboard players set @s rpg_l2_st 3",
        "scoreboard players set @s rpg_l2_sk 16",
        "scoreboard players set @s rpg_l2_t 0",
        "function %s/hold" % F,
        "function %slaugh" % LORD_CLIP,
        "particle %s ~ ~1 ~ 1.4 1 1.4 0.04 42 force" % ui.pillar_transition(1, 2.6),
        "playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..32] ~ ~ ~ 1 0.65",
        "execute positioned ~ ~3.3 ~ run function %s/ult/crown" % P1,
    ] + prop("scrown", "serpent_crown", flat(0.01, 0.03)))
    w("p1/ult/crown", sprite("crown", xf(s=(glyph_scale("crown", 2.6),) * 3), life=52))
    w("p1/ult/tick", [
        "execute if score @s rpg_l2_t matches ..29 run particle %s ~ ~1 ~ 0.55 0.75 0.55 0.02 3" % DUST_SMALL,
        "execute if score @s rpg_l2_t matches 10 run function %s/ult/warn_rings" % P1,
        "execute if score @s rpg_l2_t matches 20 run function %s/ult/warn_rings" % P1,
        at(30, "function %sstrong" % LORD_CLIP),
        at(30, "function %s/ult/fire" % P1),
        at(52, "function %s/free" % F),
    ])
    w("p1/ult/warn_rings", ["particle %s ~%d ~0.15 ~%d 0.2 0 0.2 0 2 force" % (DUST_SMALL, x, z)
                            for r in (2, 4, 6) for x, z in ((r, 0), (-r, 0), (0, r), (0, -r),
                                                             (r, r), (r, -r), (-r, r), (-r, -r))])
    w("p1/ult/fire", [
        "data modify storage rpg:demon uuid set from entity @s UUID",
        "function rpg:taint/ult1_fangs with storage rpg:demon",
        "tag @s add rpg.dm.cast",
        "execute as @a[distance=..10,%s] run function rpg:taint/ult1_hit" % SURV,
        "tag @s remove rpg.dm.cast",
        "particle %s ~ ~1 ~ 5 1 5 0.04 72" % ui.pillar_transition(1, 3),
        "particle end_rod ~ ~2 ~ 2.5 1.5 2.5 0.05 60",
        "playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..32] ~ ~ ~ 1.2 0.55",
        "playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..40] ~ ~ ~ 0.8 0.7",
        "execute positioned ~ ~2 ~ run function %s/ult/burst" % P1,
    ] + prop("shock20", "shock_ring", flat(0.5, 0.06)))
    w("p1/ult/burst", sprite("burst", xf(s=(glyph_scale("burst", 6),) * 3)))


def build_p1():
    build_p1_core()
    build_p1_skills()


def write_predicate():
    path = os.path.join(DP, "data", "rpg", "predicate", "lucifer_fight", "on_ground.json")
    wf(path, ['{"condition":"minecraft:entity_properties","entity":"this",'
              '"predicate":{"flags":{"is_on_ground":true}}}'])


# ---------------------------------------------------------------------------
# 接入现有路径
# ---------------------------------------------------------------------------
MARK = "# 路西法二阶段（add_lucifer_fight.py）"


def _path(rel):
    return os.path.join(FUNC, *rel.split("/")) + ".mcfunction"


def insert_after(rel, anchor, new):
    path = _path(rel)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    if MARK in lines:
        return
    if anchor not in lines:
        raise AssertionError("%s: anchor line missing: %s" % (rel, anchor))
    i = lines.index(anchor) + 1
    lines[i:i] = [MARK, new]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))


def prepend(rel, new):
    path = _path(rel)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    if MARK in lines:
        return
    if not os.path.isfile(path) or not any(l.strip() and not l.startswith("#") for l in lines):
        raise AssertionError("%s: nothing to hook" % rel)
    i = 0
    while i < len(lines) and lines[i].startswith("#"):
        i += 1
    lines[i:i] = [MARK, new]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))


NL = chr(10)


def hook():
    insert_after("taint/advent_tick", "function rpg:inquest/boss_tick",
                 "execute if score @s rpg_dm_lord matches 1 run function %s/tick" % F)
    prepend("taint/sk1", NL.join(["execute if entity @s[tag=rpg.lu.phase2] run return run function %s/cast" % F,
                                  "return run function %s/p1/cast" % F]))
    prepend("taint/ult1_warn", NL.join(["execute if entity @s[tag=rpg.lu.phase2] run return run function %s/ult/warn" % F,
                                        "return run function %s/p1/ult/warn" % F]))
    # 两个形态的罪约都由各自的时间线结算；原来的蓄势表现与结算不再走。
    prepend("taint/ult1_charge", "return 0")
    prepend("taint/ult1", "return 0")
    hook_tag(DP, "load", "%s/load" % F, False)
    hook_tag(DP, "tick", "%s/global" % F, True)


def main():
    build_core()
    build_fx()
    build_dispatch()
    build_melee()
    build_vines()
    build_fruit()
    build_tempt()
    build_fall()
    build_gaze()
    build_ult()
    build_states()
    build_p1()
    write_predicate()
    hook()
    count = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("lucifer_fight: %d functions; tree form at %d HP, scale %s" % (count, P2_AT, SCALE))


if __name__ == "__main__":
    main()
