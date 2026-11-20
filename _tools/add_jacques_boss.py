# -*- coding: utf-8 -*-
"""圣殿大团长雅克 Boss（docs/JACQUES-DESIGN.md）。只用指令召唤，规格对齐教皇战和篡夺者。

    python add_jacques_boss.py ../rpg

外观在 add_jacques_model.py（载体 rpg.jqb 换装为 rpg.jqm；大卫的幽灵 rpg.jqd 换装为 rpg.jqdm），
血条横幅在 add_jacques_boss_art.py，特效素材沿用篡夺者的（boss_fx.py）。

两段，每段 1000 血：一阶段「圣殿之誓」，变身「火刑柱」，二阶段「火刑柱」，击败后他倒下。
每段一池血，切段补满；副手放隐形的死亡保护，致命一击被它吃掉后由切段接手（同篡夺者）。
他是人：载体不带 rpg.demon（七罪契约打不到），也不带 rpg.demon.fly（新约技能打不到，设计稿第 9 节第 2 条）。
武器：常态只拿坟墓克星；弩招才换竖琴弩，上弦时依次换四个阶段（rpg:jacques/weapon/*）。每个招式的结束、
被打断、眩晕、切段和清场都换回坟墓克星。
二阶段每次起手大招，大卫的幽灵都甩出一颗石子，2 秒后命中，打断大招，他眩晕 3 秒、护甲归零（第 9 节第 3 条）。
没有幽灵时（调试）大招会完整放完。
"""

import json
import math
import os
import sys

import rpg_ui_style as ui
import add_jacques_boss_art as bar_art
from boss_fx import Fx, flat_sc, sc
from display_mob import hook_tag, wf

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "jacques_boss")
B = "rpg:jacques_boss"
LOOK = "rpg:jacques"
DAVID = "rpg:david"
O = "rpg_jq"
UNIT = "type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview"
GHOST = "type=minecraft:vindicator,tag=rpg.jqd"
SURV = "gamemode=!spectator,gamemode=!creative"
BAR = "rpg:jacques_boss"

ARENA = 40
BAR_RANGE = 48
EMPTY_LIMIT = 1200
STRIDE = 4
MAX = 1000
ARMOR = 10
GUARD = 'minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]'
BASIC_GAP = 10
BASICS_PER_SKILL = 3
BASIC_RANGE = 25
MELEE_R = 4.5
SHOT_R = 7
GUARD_CAP = 4

# 配色：圣殿骑士白底红十字；一阶段钢蓝，二阶段火
TEMPLAR_RED = "#C8102E"
TEMPLAR_WHITE = "#F2F2F2"
STEEL = "#8FA9BE"
GOLD = "#F0CF7A"
GOLD_I = 0xF0CF7A
PALE = "#FFF2C8"
EMBER = "#FF8A3D"
EMBER_I = 0xFF8A3D
FIRE_D = 0xC2361A
FIRE_DH = "#C2361A"
CHAR = 0x3A2A20
CURSE = "#8B0A14"
CURSE_I = 0x8B0A14
GHOST_C = "#D8ECFF"

STAGES = {
    # 段号: (名称, 英文小注, 大招血线, 大招时钟（刻）, 音乐, 音乐长度（刻）, 招式轮换)
    1: ("圣殿之誓", "The Grand Master", (625, 375), 900, "boss3", 2000, ["volley", "charge", "horn"]),
    2: ("火刑柱", "The Burning Oath", (667, 333), 1200, "boss1", 2943, ["leap", "volley", "curse", "horn"]),
}
SKILL_ID = {"slash1": 1, "slash2": 2, "sweep": 3, "shot": 4, "volley": 5, "charge": 6, "backshot": 7, "horn": 8,
            "cross": 9, "harp": 10, "stagger": 11, "leap": 12, "curse": 13, "stakes": 14, "last": 15}

# 招式数值（设计稿第 4 节）
SLASH_DMG, SWEEP_DMG, SHOT_DMG, VOLLEY_DMG, CHARGE_DMG, BACK_DMG = 7, 11, 5, 5, 10, 6
CROSS_W, CROSS_L, CROSS_DMG, CROSS_AT, CROSS_LEN = 3, 20, 18, 30, 62
HARP_N, HARP_GAP, HARP_DMG, HARP_FIRST, HARP_STEP, HARP_HALF = 12, 2.5, 12, 30, 5, 15
LEAP_R, LEAP_DMG, LEAP_MARK, LEAP_UP, LEAP_DOWN, LEAP_LEN = 4, 14, 8, 12, 28, 52
CURSE_TICKS, CURSE_R, CURSE_DMG = 160, 3, 12
STAKE_N, STAKE_R, STAKE_FIRST, STAKE_STEP, STAKE_PULL, STAKE_HIT, STAKE_DMG, WALL_DMG = 7, 9, 20, 12, 110, 125, 16, 4
LAST_ROLL, LAST_DMG, LAST_SWEEP = 10, 20, 4.5
STONE_AT = 40                         # 大招起手后 2 秒，大卫的石子命中
STUN = 60
FIRE_DMG = 2


def w(path, lines):
    wf(os.path.join(OUT, *path.split("/")) + ".mcfunction", lines)


fx = Fx(fn=B, tag="rpg.jqb.fx", life="rpg_jq_life", kind="rpg_jq_kd", writer=w, kinds={
    "sweep": dict(life=8, steps=[(7, 3, flat_sc(4.5)), (3, 3, flat_sc(5.5))]),
    "sweepw": dict(life=8, steps=[(7, 3, flat_sc(6)), (3, 3, flat_sc(7.5))]),
    "spinf": dict(extra=["tp @s ~ ~ ~ ~7 ~"]),
    # 地面光环向外扩开再收成线（出生时给起始尺寸）
    "ringm": dict(life=12, steps=[(11, 10, flat_sc(6))]),
    "ringx": dict(life=14, steps=[(13, 12, flat_sc(11))]),
    # 十字炸开的光臂：亮 12 刻后收细消失
    "armfade": dict(life=22, steps=[(10, 10, "scale:[0.01f,0.02f,20f]")]),
    # 光柱：落下后慢慢变细消失
    "pillarfade": dict(life=24, steps=[(23, 3, sc((0.75, 28, 0.75))), (12, 12, sc((0.02, 28, 0.02)))]),
    "pillarcore": dict(life=24, steps=[(23, 3, sc((0.3, 28, 0.3))), (14, 10, sc((0.01, 28, 0.01)))]),
})


def light_pillar(color, tags=()):
    """A beam of light from the sky onto here (28 blocks tall): snaps wide, then thins away over a second."""
    return ([fx.disp("beam", pos="~ ~ ~", scale=(0.2, 28, 0.2), color=color, trans=(0, 14, 0), tags=tags)] + fx.born(kind="pillarfade")
            + [fx.disp("beam", pos="~ ~ ~", scale=(0.1, 28, 0.1), color=0xFFFFFF, trans=(0, 14, 0), tags=tags)] + fx.born(kind="pillarcore")
            + ["particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force"])
NEW = "rpg.jqb.fxnew"


def say(text, gloss=None, name=None, stage=1):
    """〖雅克〗 播报：圣殿骑士的白底红十字（ART-STYLE.md §12 的格式）。"""
    parts = [ui.comp("〖", TEMPLAR_RED, True), ui.comp("雅克", TEMPLAR_WHITE if stage == 1 else EMBER, True),
             ui.comp("〗", TEMPLAR_RED, True)]
    if gloss:
        parts.append(ui.comp(" " + ui.fraktur(gloss), ui.BROADCAST_GLOSS))
    parts.append(ui.comp(ui.GAP, ui.BROADCAST_BODY))
    if name:
        parts.append(ui.comp(name, ui.BROADCAST_NAME))
    parts.append(ui.comp(text, ui.BROADCAST_BODY))
    return "tellraw @a[distance=..%d] %s" % (BAR_RANGE, ui.row(*parts))


def say_david(text):
    return "tellraw @a[distance=..%d] %s" % (BAR_RANGE, ui.row(
        ui.comp("〖大卫〗", GHOST_C, True), ui.comp(ui.GAP, ui.BROADCAST_BODY), ui.comp(text, ui.BROADCAST_NAME)))


def bar_title(stage, step=bar_art.STEPS):
    return "bossbar set %s name %s" % (BAR, json.dumps(
        {"text": bar_art.bar_text(stage, step), "font": bar_art.FONT}, ensure_ascii=True, separators=(",", ":")))


def anim(clip):
    return "function %s/anim/enter/%s" % (LOOK, clip)


def weapon(name):
    return "function %s/weapon/%s" % (LOOK, name)


def start(name, busy):
    return ["scoreboard players set @s rpg_jq_sk %d" % SKILL_ID[name], "scoreboard players set @s rpg_jq_t 0",
            "scoreboard players set @s rpg_jq_busy %d" % busy]


def face(r=BASIC_RANGE):
    return "execute facing entity @p[distance=..%s,%s] feet run tp @s ~ ~ ~ ~ 0" % (r, SURV)


def at(t, cmd):
    return "execute if score @s rpg_jq_t matches %d run %s" % (t, cmd)


def hurt_tagged(dmg, kind="minecraft:mob_attack"):
    """Damage everyone tagged rpg.jqb.hit by the fight, then untag (curse: a glaive hit sets it off early)."""
    return ["execute as @a[tag=rpg.jqb.hit] run damage @s %d %s by @e[%s,limit=1]" % (dmg, kind, UNIT),
            "execute as @a[tag=rpg.jqb.hit,tag=rpg.jqb.cursed] at @s run function %s/curse/pop" % B,
            "tag @a remove rpg.jqb.hit"]


def tag_near(r, pos="~ ~ ~"):
    return "execute positioned %s run tag @a[distance=..%s,%s] add rpg.jqb.hit" % (pos, r, SURV)


def line(kind, steps):
    """Tag everyone along a line from here, along the current rotation (line/<kind> steps 1.5 blocks)."""
    return ["scoreboard players set #d %s %d" % (O, steps), "function %s/line/%s" % (B, kind)]


def every(n, score="@s rpg_jq_t"):
    who, obj = score.split()
    return ["scoreboard players operation #m %s = %s %s" % (O, who, obj),
            "scoreboard players set #k %s %d" % (O, n),
            "scoreboard players operation #m %s %%= #k %s" % (O, O)]


def beam(color, size, trans, tags=(), tp=1):
    """A flat or thin box from the scrolling original beam (rpg:usurper_fx/beam), turned to the current
    rotation right after it is born (the next line is the tp)."""
    return [fx.disp("beam", pos="~ ~ ~", scale=size, color=color, trans=trans, tags=tags, tp=tp),
            "tp @e[tag=%s,limit=1] ~ ~ ~ ~ 0" % NEW]


# ---- 粒子形状（教皇战标准：形状用展示实体，能量用粒子；这里是能量层）
GOLD_DUST = "minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3}"
EMBER_DUST = "minecraft:dust_color_transition{from_color:[1.0,0.62,0.2],to_color:[0.35,0.04,0.0],scale:1.4}"
CURSE_DUST = "minecraft:dust{color:[0.6,0.03,0.08],scale:1.6}"


def ring(p, r, n, y=0.15, phase=0.0):
    """A still ring of particles around here."""
    out = []
    for i in range(n):
        a = 2 * math.pi * (i + phase) / n
        out.append("particle %s ~%.2f ~%.2f ~%.2f 0 0 0 0 1 force" % (p, r * math.cos(a), y, r * math.sin(a)))
    return out


def wave(p, n, speed, y=0.2, r0=0.4, up=0.0):
    """An expanding ring: count 0 makes the delta the velocity, so every particle flies straight out."""
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        out.append("particle %s ~%.2f ~%.2f ~%.2f %.3f %.3f %.3f %g 0 force" % (p, r0 * c, y, r0 * s, c, up, s, speed))
    return out


def fountain(p, n, speed, y=0.6, up=1.0):
    """A dome burst: particles fly out and up at n bearings, two heights."""
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        for k in (0.5, 1.0):
            out.append("particle %s ~ ~%.2f ~ %.3f %.3f %.3f %g 0 force" % (p, y, c * k, up * (1.2 - k * 0.6), s * k, speed))
    return out


def helix(p, phases, r, h0, h1, score, per=2):
    """One step of a rising spiral per tick: on phase k (score #m), `per` particles at evenly spaced bearings."""
    out = []
    for k in range(phases):
        y = h0 + (h1 - h0) * k / (phases - 1)
        for j in range(per):
            a = 2 * math.pi * (k / float(phases) + j / float(per))
            out.append("execute if score #m %s matches %d run particle %s ~%.2f ~%.2f ~%.2f 0 0.02 0 0.01 1" % (
                O, k, p, r * math.cos(a), y, r * math.sin(a)))
    return every(phases, score) + out


def along(p, length, step, y=0.2, spread=0.15, n=1, speed=0.0):
    """Particles every `step` blocks straight ahead (local ^ coordinates)."""
    out = []
    d = step
    while d <= length + 1e-6:
        out.append("particle %s ^ ^%.2f ^%.2f %s %s %s %g %d force" % (p, y, d, spread, spread * 0.5, spread, speed, n))
        d += step
    return out


# =====================================================================================
# 框架：召唤、每刻、血量、调度、切段、结算、清场、音乐
# =====================================================================================
def build():
    w("load", [
        "scoreboard objectives add %s dummy" % O,
        "scoreboard objectives add rpg_jq_h dummy",      # 当前血量
        "scoreboard objectives add rpg_jq_c dummy",      # 本段大招时钟
        "scoreboard objectives add rpg_jq_b dummy",      # 普攻计时
        "scoreboard objectives add rpg_jq_n dummy",      # 普攻计数
        "scoreboard objectives add rpg_jq_k dummy",      # 招式轮换序号
        "scoreboard objectives add rpg_jq_cb dummy",     # 坟墓克星三连走到第几下
        "scoreboard objectives add rpg_jq_busy dummy",   # 动作占用（刻）
        "scoreboard objectives add rpg_jq_sk dummy",     # 正在进行的招式
        "scoreboard objectives add rpg_jq_t dummy",      # 招式时间线（刻）
        "scoreboard objectives add rpg_jq_life dummy",   # 特效寿命（刻）
        "scoreboard objectives add rpg_jq_kd dummy",     # 特效种类
        "scoreboard objectives add rpg_jq_id dummy",     # 琴弦 / 火刑柱的序号
        "scoreboard objectives add rpg_jq_cu dummy",     # 诅咒印记剩余（玩家）
        "scoreboard objectives add rpg_jq_s dummy",      # 横幅当前档位
        "bossbar add %s \"雅克\"" % BAR,
        "# 粉色档的原版贴图已由教皇战改成全透明：只显示名字里的位图横幅。",
        "bossbar set %s color pink" % BAR,
        "bossbar set %s style notched_20" % BAR,
        "bossbar set %s visible false" % BAR,
    ])

    w("summon", [
        "# 在执行位置开战。同一时间只允许一场。",
        "execute if score #fight %s matches 1 run return run tellraw @s %s" % (
            O, ui.row(ui.comp("〖雅克〗", TEMPLAR_WHITE, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                      ui.comp("已经有一场雅克战；先用 /function %s/clear 清场。" % B, ui.BROADCAST_BODY))),
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.jqb.center\"]}",
        "summon minecraft:vindicator ~ ~ ~ {Tags:[\"rpg.jqb\",\"rpg.jqwear\",\"rpg.jqb.new\"],Silent:1b,PersistenceRequired:1b,"
        "CustomName:[{\"text\":\"[圣殿大团长]\",\"color\":\"%s\",\"bold\":true,\"italic\":false},"
        "{\"text\":\"雅克\",\"color\":\"%s\",\"bold\":false,\"italic\":false}],"
        "Health:%df,active_effects:[{id:\"invisibility\",duration:-1,amplifier:0,show_particles:0b}],"
        "attributes:[{id:\"max_health\",base:%df},{id:\"attack_damage\",base:1f},{id:\"armor\",base:%df},"
        "{id:\"follow_range\",base:48f},{id:\"knockback_resistance\",base:0.8f},{id:\"movement_speed\",base:0.33f}],"
        "drop_chances:{mainhand:0f,offhand:0f}}" % (TEMPLAR_RED, TEMPLAR_WHITE, MAX, MAX, ARMOR),
        "scoreboard players set @e[%s,tag=rpg.jqb.new] %s 1" % (UNIT, O),
        "scoreboard players set @e[%s,tag=rpg.jqb.new] rpg_jq_h %d" % (UNIT, MAX),
        "scoreboard players set @e[%s,tag=rpg.jqb.new] rpg_jq_c 0" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.jqb.new] rpg_jq_b 40" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.jqb.new] rpg_jq_n 0" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.jqb.new] rpg_jq_k 0" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.jqb.new] rpg_jq_cb 0" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.jqb.new] rpg_jq_sk 0" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.jqb.new] rpg_jq_busy 44" % UNIT,      # 英雄姿势登场
        "tag @e[%s,tag=rpg.jqb.new] remove rpg.jqb.new" % UNIT,
        "scoreboard players set #fight %s 1" % O,
        "scoreboard players set #stage %s 1" % O,
        "scoreboard players set #empty %s 0" % O,
        "scoreboard players set #tick %s 0" % O,
        bar_title(1),
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_jq_s %d" % (UNIT, bar_art.STEPS),
        "bossbar set %s max %d" % (BAR, MAX),
        "bossbar set %s value %d" % (BAR, MAX),
        "bossbar set %s visible true" % BAR,
        "function %s/music/1" % B,
        "particle minecraft:end_rod ~ ~1.5 ~ 0.6 1.2 0.6 0.04 40 force",
        "function %s/vfx/intro" % B,
        "playsound minecraft:event.raid.horn hostile @a[distance=..%d] ~ ~ ~ 2 1.2" % BAR_RANGE,
        say("圣殿骑士团，奉教皇之名。拔剑吧，年轻人。", gloss="The Grand Master"),
    ])

    w("tick", [
        "execute unless score #fight %s matches 1 run return 0" % O,
        "execute as @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] at @s run function %s/arena" % B,
    ])
    w("arena", [
        "# 战场（as/at 战场中心）。",
        "scoreboard players add #tick %s 1" % O,
        "execute if entity @a[distance=..%d,%s] run scoreboard players set #empty %s 0" % (ARENA, SURV, O),
        "execute unless entity @a[distance=..%d,%s] run scoreboard players add #empty %s 1" % (ARENA, SURV, O),
        "execute if score #empty %s matches %d.. run return run function %s/lose" % (O, EMPTY_LIMIT, B),
        "execute unless entity @e[%s,distance=..%d] run return run function %s/lost_unit" % (UNIT, ARENA * 3, B),
        "bossbar set %s players @a[distance=..%d]" % (BAR, BAR_RANGE),
        "execute as @e[%s,distance=..%d] at @s run function %s/unit" % (UNIT, ARENA * 3, B),
        "execute as @e[tag=rpg.jqb.fx,distance=..%d] at @s run function %s/fx/tick" % (ARENA * 3, B),
        "execute as @e[%s,distance=..%d] at @s run function %s/david/tick" % (GHOST, ARENA * 3, B),
        "execute as @a[tag=rpg.jqb.cursed] at @s run function %s/curse/tick" % B,
        "function %s/music/tick" % B,
    ])
    w("lost_unit", [
        "# 载体不见了：二阶段里按胜利结算；否则清场。",
        "execute if score #stage %s matches 2.. run return run function %s/victory" % (O, B),
        "function %s/clear" % B,
    ])
    w("unit", [
        "# 载体每刻（as/at 载体）。",
        "execute if entity @s[tag=rpg.jqb.end] run return run function %s/finale/tick" % B,
        "execute if entity @s[tag=!rpg.jqb.hp] run return run function %s/hp_init" % B,
        "scoreboard players operation #m %s = #tick %s" % (O, O),
        "scoreboard players set #k %s %d" % (O, STRIDE),
        "scoreboard players operation #m %s %%= #k %s" % (O, O),
        "execute if score #m %s matches 0 run function %s/read_hp" % (O, B),
        "execute if score @s %s matches 1 if score @s rpg_jq_h matches ..1 run return run function %s/stage/end1" % (O, B),
        "execute if score @s %s matches 2 if score @s rpg_jq_h matches ..1 run return run function %s/stage/end2" % (O, B),
        "execute if entity @s[tag=rpg.jqb.morph] run return run function %s/morph/tick" % B,
        "execute if score @s %s matches 2 run function %s/s2/burn" % (O, B),
        "scoreboard players add @s rpg_jq_c 1",
        "execute if score @s rpg_jq_sk matches 1.. run function %s/sk/tick" % B,
        "execute if score @s rpg_jq_busy matches 1.. run return run scoreboard players remove @s rpg_jq_busy 1",
        "function %s/schedule" % B,
    ])
    w("hp_init", ["tag @s add rpg.jqb.hp", "function %s/refill" % B])
    w("refill", [
        "# 补满本段血量，并补上副手的死亡保护（上一段的那件可能刚被吃掉）。",
        "attribute @s minecraft:max_health base set %d" % MAX,
        "data merge entity @s {Health:%df}" % MAX,
        "scoreboard players set @s rpg_jq_h %d" % MAX,
        "item replace entity @s weapon.offhand with %s" % GUARD,
    ])
    w("read_hp", [
        "execute store result score @s rpg_jq_h run data get entity @s Health 1",
        "execute store result bossbar %s value run scoreboard players get @s rpg_jq_h" % BAR,
        "# 横幅每 50 血一档，跨档才换图；变身期间停在空条",
        "execute if entity @s[tag=rpg.jqb.morph] run return 0",
        "scoreboard players operation #s %s = @s rpg_jq_h" % O,
        "scoreboard players add #s %s 49" % O,
        "scoreboard players set #k %s %d" % (O, MAX // bar_art.STEPS),
        "scoreboard players operation #s %s /= #k %s" % (O, O),
        "execute if score #s %s matches %d.. run scoreboard players set #s %s %d" % (O, bar_art.STEPS + 1, O, bar_art.STEPS),
        "execute if score #s %s matches ..-1 run scoreboard players set #s %s 0" % (O, O),
        "execute unless score #s %s = @s rpg_jq_s run function %s/bar_name" % (O, B),
    ])
    names = ["scoreboard players operation @s rpg_jq_s = #s %s" % O]
    for st in STAGES:
        names += ["execute if score @s %s matches %d if score #s %s matches %d run return run %s" % (O, st, O, k, bar_title(st, k))
                  for k in range(bar_art.STEPS + 1)]
    w("bar_name", names)

    # ---- 调度：普攻每 10 刻（贴身三连，远处单发弩），每三次普攻接一招；大招按血线或时钟插入
    w("schedule", [
        "execute unless entity @a[distance=..%d,%s] run return 0" % (BASIC_RANGE, SURV),
        "scoreboard players remove @s rpg_jq_b 1",
        "execute if score @s rpg_jq_b matches 1.. run return 0",
        "scoreboard players set @s rpg_jq_b %d" % BASIC_GAP,
        "execute if score @s rpg_jq_n matches %d.. run return run function %s/pick" % (BASICS_PER_SKILL, B),
        "execute if entity @a[distance=..%s,%s] run return run function %s/basic/melee" % (MELEE_R, SURV, B),
        "execute unless entity @a[distance=..%d,%s] run return run function %s/basic/shot" % (SHOT_R, SURV, B),
        "# 4.5～7 格：不出手，走近",
    ])
    pick = ["scoreboard players set @s rpg_jq_n 0", "scoreboard players set #ult %s 0" % O]
    for s, (_, _, ults, clock, *_r) in STAGES.items():
        for i, ln in enumerate(ults, 1):
            pick.append("execute if score @s %s matches %d if score @s rpg_jq_h matches ..%d unless entity @s[tag=rpg.jqb.u%d] "
                        "run scoreboard players set #ult %s %d" % (O, s, ln, i, O, i))
        pick.append("execute if score @s %s matches %d if score #ult %s matches 0 if score @s rpg_jq_c matches %d.. "
                    "run scoreboard players set #ult %s 9" % (O, s, O, clock, O))
    pick.append("execute if score #ult %s matches 1.. run return run function %s/ult/pick" % (O, B))
    for s, (*_h, rotation) in STAGES.items():
        n = len(rotation)
        pick.append("execute if score @s %s matches %d run scoreboard players operation #r %s = @s rpg_jq_k" % (O, s, O))
        for i, sk in enumerate(rotation):
            pick.append("execute if score @s %s matches %d if score #r %s matches %d run function %s/pick/%s" % (O, s, O, i, B, sk))
        pick.append("execute if score @s %s matches %d run scoreboard players add @s rpg_jq_k 1" % (O, s))
        pick.append("execute if score @s %s matches %d if score @s rpg_jq_k matches %d.. run scoreboard players set @s rpg_jq_k 0" % (O, s, n))
    w("pick", pick)
    # 每个轮换位按距离换招：被贴身时连弩、冲锋改成后撤射击；圣卫满了号角改成连弩
    w("pick/volley", [
        "execute if entity @a[distance=..4,%s] run return run function %s/skill/backshot" % (SURV, B),
        "function %s/skill/volley" % B])
    w("pick/charge", [
        "execute if entity @a[distance=..3,%s] run return run function %s/skill/backshot" % (SURV, B),
        "function %s/skill/charge" % B])
    w("pick/horn", [
        "execute store result score #n %s if entity @e[tag=rpg.jqb.guard]" % O,
        "execute if score #n %s matches %d.. run return run function %s/skill/volley" % (O, GUARD_CAP, B),
        "function %s/skill/horn" % B])
    w("pick/leap", ["function %s/skill/leap" % B])
    w("pick/curse", [
        "execute if entity @a[tag=rpg.jqb.cursed] run return run function %s/skill/leap" % B,
        "function %s/skill/curse" % B])

    w("ult/pick", [
        "execute if score #ult %s matches 1 run tag @s add rpg.jqb.u1" % O,
        "execute if score #ult %s matches 2 run tag @s add rpg.jqb.u2" % O,
        "scoreboard players set @s rpg_jq_c 0",
        "# 两招轮流：血线 1 / 时钟到点且上一招是 2 → 第一招；否则第二招",
        "execute if score #ult %s matches 9 if entity @s[tag=rpg.jqb.last1] run scoreboard players set #ult %s 2" % (O, O),
        "execute if score #ult %s matches 9 run scoreboard players set #ult %s 1" % (O, O),
        "execute if score @s %s matches 1 if score #ult %s matches 1 run function %s/ult/cross" % (O, O, B),
        "execute if score @s %s matches 1 if score #ult %s matches 2 run function %s/ult/harp" % (O, O, B),
        "execute if score @s %s matches 2 if score #ult %s matches 1 run function %s/ult/stakes" % (O, O, B),
        "execute if score @s %s matches 2 if score #ult %s matches 2 run function %s/ult/last" % (O, O, B),
        "execute if score #ult %s matches 1 run tag @s add rpg.jqb.last1" % O,
        "execute if score #ult %s matches 2 run tag @s remove rpg.jqb.last1" % O,
        "# 二阶段：大卫的幽灵甩出石子",
        "execute if score @s %s matches 2 run function %s/david/throw" % (O, B),
    ])

    w("sk/tick", ["scoreboard players add @s rpg_jq_t 1"] + [
        "execute if score @s rpg_jq_sk matches %d run return run function %s/sk/%s" % (i, B, n) for n, i in SKILL_ID.items()])
    w("sk/end", [
        "scoreboard players set @s rpg_jq_sk 0",
        "scoreboard players set @s rpg_jq_busy 0",
        "data merge entity @s {NoAI:0b,NoGravity:0b,Invulnerable:0b}",
        "attribute @s minecraft:armor base set %d" % ARMOR,
        weapon("glaive"),
    ])

    # ---- 线判定：从这里沿当前朝向每 1.5 格查一次
    for kind, r in (("wide", CROSS_W / 2.0 + 0.1), ("thin", 1.0), ("path", 1.4)):
        w("line/%s" % kind, [
            "tag @a[distance=..%s,%s] add rpg.jqb.hit" % (r, SURV),
            "scoreboard players remove #d %s 1" % O,
            "execute if score #d %s matches 1.. positioned ^ ^ ^1.5 run function %s/line/%s" % (O, B, kind),
        ])
    w("line/fire", [
        "# 火墙（沿墙走一遍）：粒子，碰到的人记下",
        "tag @a[distance=..1.1,%s] add rpg.jqb.hit" % SURV,
        "particle minecraft:flame ~ ~0.6 ~ 0.25 0.6 0.25 0.02 4",
        "particle minecraft:small_flame ~ ~1.6 ~ 0.2 0.5 0.2 0.01 2",
        "particle %s ~ ~1.2 ~ 0.2 0.6 0.2 0 1" % EMBER_DUST,
        "scoreboard players remove #d %s 1" % O,
        "execute if score #d %s matches 1.. positioned ^ ^ ^1.3 run function %s/line/fire" % (O, B),
    ])

    # ---- 阶段切换
    w("stage/end1", [
        "# 一阶段打完：变身（火刑柱）。无敌、站定，约 6 秒后进入二阶段。",
        "function %s/refill" % B,
        "tag @s add rpg.jqb.morph",
        "scoreboard players set @s rpg_jq_sk 0",
        "scoreboard players set @s rpg_jq_busy 0",
        "scoreboard players set @s rpg_jq_c 0",
        "attribute @s minecraft:armor base set %d" % ARMOR,
        "kill @e[tag=rpg.jqb.fx]",
        "data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}",
        weapon("glaive"),
        anim("kneel"),
        "bossbar set %s value %d" % (BAR, MAX),
        bar_title(1, 0),
        say("……主啊。若这是你的审判，我领受。", gloss="The Grand Master"),
    ])
    w("stage/begin2", [
        "tag @s remove rpg.jqb.morph",
        "tag @s remove rpg.jqb.u1",
        "tag @s remove rpg.jqb.u2",
        "tag @s remove rpg.jqb.last1",
        "data merge entity @s {NoAI:0b,Invulnerable:0b}",
        "scoreboard players set @s %s 2" % O,
        "scoreboard players set #stage %s 2" % O,
        "scoreboard players set @s rpg_jq_c 0",
        "scoreboard players set @s rpg_jq_n 0",
        "scoreboard players set @s rpg_jq_k 0",
        "scoreboard players set @s rpg_jq_cb 0",
        "scoreboard players set @s rpg_jq_b 20",
        "scoreboard players set @s rpg_jq_sk 0",
        bar_title(2),
        "scoreboard players set @s rpg_jq_s %d" % bar_art.STEPS,
        "function %s/music/2" % B,
        "particle minecraft:flash{color:16747069} ~ ~1.5 ~ 0 0 0 0 1 force",
        "playsound minecraft:item.firecharge.use hostile @a[distance=..%d] ~ ~ ~ 1.4 0.6" % BAR_RANGE,
        say("他们把我送上了火刑柱。可我还站着。", gloss="The Burning Oath", name="第二阶段 · ", stage=2),
    ])
    w("stage/end2", [
        "# 二阶段打完：倒下（原作倒地动作），火熄灭，约 7 秒后胜利。",
        "function %s/refill" % B,
        "tag @s add rpg.jqb.end",
        "scoreboard players set @s rpg_jq_c 0",
        "scoreboard players set @s rpg_jq_sk 0",
        "data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}",
        "attribute @s minecraft:armor base set %d" % ARMOR,
        "kill @e[tag=rpg.jqb.fx]",
        "execute as @e[tag=rpg.jqb.guard] run function rpg:holy_guard/remove",
        "execute as @a[tag=rpg.jqb.cursed] run function %s/curse/clear" % B,
        weapon("glaive"),
        anim("fall"),
        "playsound minecraft:entity.player.death hostile @a[distance=..%d] ~ ~ ~ 1.2 0.7" % BAR_RANGE,
        "playsound minecraft:block.fire.extinguish hostile @a[distance=..%d] ~ ~ ~ 1.2 0.6" % BAR_RANGE,
        "bossbar set %s value 0" % BAR,
        bar_title(2, 0),
    ])
    w("finale/tick", [
        "scoreboard players add @s rpg_jq_c 1",
        "execute if score @s rpg_jq_c matches 24 run " + anim("down"),
        "execute if score @s rpg_jq_c matches 1..40 run particle minecraft:large_smoke ~ ~0.6 ~ 0.6 0.3 0.6 0.02 3",
        "execute if score @s rpg_jq_c matches 1..20 run particle minecraft:flame ~ ~0.5 ~ 0.6 0.3 0.6 0.01 2",
        "execute if score @s rpg_jq_c matches 1 run function %s/vfx/fall" % B,
        "execute if score @s rpg_jq_c matches 20..120 run particle %s ~ ~0.6 ~ 0.6 0.4 0.6 0 1" % EMBER_DUST,
        "execute if score @s rpg_jq_c matches 20..120 run particle minecraft:white_ash ~ ~1.5 ~ 1 1 1 0.01 3",
        "execute if score @s rpg_jq_c matches 60 as @e[%s] at @s run function %s/vfx/david_hero" % (GHOST, B),
        "execute if score @s rpg_jq_c matches 40 run " + say("……我守了一辈子的，是谁？", stage=2),
        "execute if score @s rpg_jq_c matches 60 as @e[%s] at @s run %s" % (GHOST, "function %s/anim/enter/hero" % DAVID),
        "execute if score @s rpg_jq_c matches 140.. run function %s/victory" % B,
    ])

    quote = ui.row(ui.comp("〖撒母耳记上 17:45〗", ui.BROADCAST_HOLY, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                   ui.comp("你来攻击我，是靠着刀枪和铜戟；我来攻击你，是靠着万军之耶和华的名。", ui.BROADCAST_NAME))
    w("victory", [
        "execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run particle minecraft:flash{color:16774876} ~ ~2 ~ 0 0 0 0 1 force",
        "execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run particle minecraft:totem_of_undying ~ ~2 ~ 2 2 2 0.4 120 force",
        "execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run particle minecraft:end_rod ~ ~6 ~ 3 4 3 0.02 80 force",
        "execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run playsound minecraft:block.bell.resonate hostile @a[distance=..%d] ~ ~ ~ 1 0.8" % BAR_RANGE,
        "execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run tellraw @a[distance=..%d] %s" % (BAR_RANGE, quote),
        "# 圣殿誓约：战场里每个还没有的人各得一件，之后可以召友军雅克（add_jacques_ally.py）",
        "execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run function rpg:jacques_ally/reward",
        "function %s/clear" % B,
    ])
    w("lose", [
        "execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run %s" % say("退下吧。圣殿不追逃兵。").replace(
            "tellraw @a[distance=..%d]" % BAR_RANGE, "tellraw @a[distance=..%d]" % (BAR_RANGE * 2)),
        "function %s/clear" % B,
    ])
    w("clear", [
        "# 清除雅克战的全部实体：载体与部件、大卫的幽灵、召来的圣卫、特效；诅咒印记与血条一起收掉。",
        "execute as @a[tag=rpg.jqb.cursed] run function %s/curse/clear" % B,
        "tag @a remove rpg.jqb.hit",
        "tag @a remove rpg.jqb.rolled",
        "execute as @e[%s] run function %s/clear_unit" % (UNIT, B),
        "execute as @e[%s] run function %s/clear_unit" % (GHOST, B),
        "execute as @e[tag=rpg.jqb.guard] run function rpg:holy_guard/remove",
        "kill @e[type=minecraft:marker,tag=rpg.jqb.center]",
        "kill @e[tag=rpg.jqb.fx]",
        "bossbar set %s visible false" % BAR,
        "bossbar set %s players" % BAR,
    ] + ["stopsound @a record minecraft:%s" % m for m in sorted({v[4] for v in STAGES.values()})] + [
        "scoreboard players set #fight %s 0" % O,
        "scoreboard players set #stage %s 0" % O,
    ])
    w("clear_unit", ["execute on passengers run kill @s", "tp @s ~ -256 ~", "kill @s"])

    music = ["scoreboard players remove #bgm %s 1" % O]
    for s, v in STAGES.items():
        music.append("execute if score #bgm %s matches ..0 if score #stage %s matches %d run function %s/music/%d" % (O, O, s, B, s))
        w("music/%d" % s, ["stopsound @a[distance=..%d] record minecraft:%s" % (BAR_RANGE, m)
                           for m in sorted({x[4] for x in STAGES.values()})] + [
            "stopsound @a[distance=..%d] music" % BAR_RANGE,
            "execute as @a[distance=..%d] at @s run playsound minecraft:%s record @s ~ ~ ~ 1 1" % (BAR_RANGE, v[4]),
            "scoreboard players set #bgm %s %d" % (O, v[5]),
        ])
    w("music/tick", music)

    w("debug/stage2", [
        "# 召唤后直接打到一阶段底线，走正常的变身进入二阶段。",
        "function %s/summon" % B,
        "tag @e[%s,limit=1,sort=nearest] add rpg.jqb.hp" % UNIT,
        "execute as @e[%s,limit=1,sort=nearest] run function %s/refill" % (UNIT, B),
        "execute as @e[%s,limit=1,sort=nearest] run data merge entity @s {Health:1f}" % UNIT,
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_jq_h 1" % UNIT,
    ])
    w("debug/ult", [
        "# 调试：下一次选招就放大招（按本段的轮换）。",
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_jq_c 99999" % UNIT,
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_jq_n %d" % (UNIT, BASICS_PER_SKILL),
    ])
    for sk in ("volley", "charge", "backshot", "horn", "leap", "curse", "shot", "melee"):
        where = "basic" if sk in ("shot", "melee") else "skill"
        w("debug/skill/%s" % sk, ["# 调试：最近的雅克立刻出这一招。",
                                  "execute as @e[%s,limit=1,sort=nearest] at @s run function %s/%s/%s" % (UNIT, B, where, sk)])
    for u in ("cross", "harp", "stakes", "last"):
        w("debug/ult/%s" % u, ["# 调试：最近的雅克立刻放这个大招。",
                               "execute as @e[%s,limit=1,sort=nearest] at @s run function %s/ult/%s" % (UNIT, B, u)])


# =====================================================================================
# 招式（一阶段与二阶段共用的普攻与弩招，二阶段多火）
# =====================================================================================
def fire_patch(size=1.0, life=60):
    """A small fire on the ground here (marker + decal); fx/fire hurts whoever stands in it."""
    return ([fx.marker("~ ~ ~", "rpg.jqb.fire")] + fx.born(life)
            + fx.decal("glow", size * 2.4, EMBER_I, pos="~ ~0.04 ~", life=life))


def skills():
    # ---- 普攻：坟墓克星三连（原作坟墓克星连招，命中时刻取自原作事件）
    w("basic/melee", [
        "scoreboard players add @s rpg_jq_n 1",
        face(MELEE_R + 1),
        "execute if score @s rpg_jq_cb matches 0 run function %s/skill/slash1" % B,
        "execute if score @s rpg_jq_cb matches 1 run function %s/skill/slash2" % B,
        "execute if score @s rpg_jq_cb matches 2 run function %s/skill/sweep" % B,
        "scoreboard players add @s rpg_jq_cb 1",
        "execute if score @s rpg_jq_cb matches 3.. run scoreboard players set @s rpg_jq_cb 0",
    ])
    for name, hit_t, busy in (("slash1", 7, 18), ("slash2", 9, 22)):
        w("skill/%s" % name, start(name, busy) + ["data merge entity @s {NoAI:1b}", anim(name)])
        w("sk/%s" % name, [
            at(hit_t, "function %s/strike/front" % B),
            "execute if score @s rpg_jq_t matches %d.. run function %s/sk/end" % (busy - 2, B),
        ])
    w("strike/front", [
        "# 下劈（as/at 载体）：身前 2.3 格；金色弧光",
        tag_near(2.3, "^ ^ ^1.8"),
    ] + hurt_tagged(SLASH_DMG) + [
        "execute if score @s %s matches 1 run function %s/vfx/front1" % (O, B),
        "execute if score @s %s matches 2 run function %s/vfx/front2" % (O, B),
    ])
    w("skill/sweep", start("sweep", 20) + ["data merge entity @s {NoAI:1b}", anim("sweep")])
    w("sk/sweep", [
        at(3, "function %s/strike/sweep" % B),
        "execute if score @s rpg_jq_t matches 18.. run function %s/sk/end" % B,
    ])
    sweep = ["# 横扫（as/at 载体）：身前约 80°、4.5 格；原作弧光横贴在胸口高度", tag_near(3.2, "^ ^ ^1.4")] + hurt_tagged(SWEEP_DMG) + [
        "execute positioned ^ ^1.1 ^1.2 run %s" % fx.disp("crescent", color=GOLD_I),
        "execute as @e[tag=%s] positioned as @s run tp @s ~ ~ ~ ~ 0" % NEW,
    ] + fx.born(kind="sweep") + [
        "particle minecraft:sweep_attack ^ ^1 ^1.8 0.8 0.2 0.8 0 4",
        "execute if score @s %s matches 1 run function %s/vfx/sweep1" % (O, B),
        "execute if score @s %s matches 2 run function %s/vfx/sweep2" % (O, B),
        "execute if score @s %s matches 2 run function %s/strike/fireline" % (O, B),
    ]
    w("strike/sweep", sweep)
    fl = ["# 燃刃横扫在身前留下一道火线（3 秒）"]
    for x, z in ((-2, 1.5), (-1, 2.3), (0, 2.6), (1, 2.3), (2, 1.5)):
        fl += ["execute positioned ^%d ^ ^%s run function %s/fire/patch" % (x, z, B)]
    w("strike/fireline", fl)
    w("fire/patch", fire_patch(1.0, 60))
    w("fx/fire", [
        "# 地上的火（as/at 标记）：粒子；每 10 刻烧一次站在里面的人",
    ] + every(4, "@s rpg_jq_life") + [
        "execute if score #m %s matches 0 run particle minecraft:flame ~ ~0.2 ~ 0.4 0.1 0.4 0.01 4" % O,
        "execute if score #m %s matches 2 run particle minecraft:small_flame ~ ~0.5 ~ 0.3 0.3 0.3 0.01 2" % O,
        "execute if score #m %s matches 1 run particle %s ~ ~0.4 ~ 0.35 0.2 0.35 0 1" % (O, EMBER_DUST),
    ] + every(10, "@s rpg_jq_life") + [
        "execute if score #m %s matches 0 as @a[distance=..1.1,%s] run damage @s %d minecraft:in_fire" % (O, SURV, FIRE_DMG),
    ] + every(16, "@s rpg_jq_life") + [
        "execute if score #m %s matches 0 run particle minecraft:lava ~ ~0.2 ~ 0.3 0 0.3 0 1" % O,
    ])
    w("fx/firering", [
        "# 火圈（as/at 圆心）：环上的粒子；每 10 刻烧一次站在 3～4.5 格环上的人",
    ] + every(3, "@s rpg_jq_life") + [
        "execute if score #m %s matches 0 run function %s/vfx/firering" % (O, B),
    ] + every(10, "@s rpg_jq_life") + [
        "execute if score #m %s matches 0 as @a[distance=3..4.6,%s] run damage @s %d minecraft:in_fire" % (O, SURV, FIRE_DMG),
    ])
    w("fire/drop", [
        "# 往下找地面（最多 8 步），在那里点一小团火",
        "scoreboard players remove #d %s 1" % O,
        "execute if score #d %s matches 1.. if block ~ ~-0.5 ~ #minecraft:replaceable positioned ~ ~-0.5 ~ run return run function %s/fire/drop" % (O, B),
        "function %s/fire/patch" % B,
    ])

    # ---- 竖琴弩：上弦四个阶段（原作上弦动作 0.7 秒），再射
    def loading(t0):
        return [at(t0 + 4, weapon("harp2")), at(t0 + 8, weapon("harp3")), at(t0 + 12, weapon("harp4"))]

    w("basic/shot", start("shot", 26) + [
        "scoreboard players add @s rpg_jq_n 1",
        "data merge entity @s {NoAI:1b}", face(), weapon("harp1"), anim("load")])
    w("sk/shot", loading(0) + [
        at(14, face()),
        at(16, anim("shoot")),
        at(16, "function %s/vfx/muzzle" % B),
        at(16, "execute positioned ~ ~1.45 ~ facing entity @p[distance=..%d,%s] eyes positioned ^ ^ ^0.9 run function %s/arrow/a5"
           % (BASIC_RANGE + 2, SURV, B)),
        at(18, weapon("harp1")),
        "execute if score @s rpg_jq_t matches 24.. run function %s/sk/end" % B,
    ])
    for dmg in (5, 6):
        w("arrow/a%d" % dmg, [
            "# 一支弩箭（at 弩口，朝飞行方向）：原作光束拉成细箭，每刻前进 1 格",
            fx.disp("beam", scale=(0.07, 0.07, 1.3), color=GOLD_I, tags=("rpg.jqb.arrow", "rpg.jqb.a%d" % dmg)),
            "tp @e[tag=%s,limit=1] ~ ~ ~ ~ ~" % NEW,
            "execute if score #stage %s matches 2 run tag @e[tag=%s] add rpg.jqb.af" % (O, NEW),
            "execute if score #stage %s matches 2 as @e[tag=%s] run data modify entity @s item.components.\"minecraft:custom_model_data\".colors[0] set value %d" % (O, NEW, EMBER_I),
        ] + fx.born(30))
    w("fx/arrow", [
        "tp @s ^ ^ ^1",
        "execute positioned ~ ~-0.9 ~ if entity @a[distance=..1.2,%s] run return run function %s/fx/arrow_hit" % (SURV, B),
        "execute unless block ~ ~ ~ #minecraft:replaceable run return run function %s/fx/arrow_end" % B,
        "particle minecraft:end_rod ^ ^ ^-0.6 0 0 0 0 1",
        "execute if entity @s[tag=!rpg.jqb.af] run particle minecraft:electric_spark ^ ^ ^-0.3 0.03 0.03 0.03 0.02 1",
        "execute if entity @s[tag=!rpg.jqb.af] run particle %s ^ ^ ^-0.9 0 0 0 0 1" % GOLD_DUST,
        "execute if entity @s[tag=rpg.jqb.af] run particle minecraft:flame ^ ^ ^-0.6 0.02 0.02 0.02 0.01 2",
        "execute if entity @s[tag=rpg.jqb.af] run particle %s ^ ^ ^-1 0 0 0 0 1" % EMBER_DUST,
    ])
    w("fx/arrow_hit", [
        "execute if entity @s[tag=rpg.jqb.a5] positioned ~ ~-0.9 ~ as @a[distance=..1.2,%s,limit=1,sort=nearest] "
        "run damage @s %d minecraft:mob_projectile by @e[%s,limit=1]" % (SURV, VOLLEY_DMG, UNIT),
        "execute if entity @s[tag=rpg.jqb.a6] positioned ~ ~-0.9 ~ as @a[distance=..1.2,%s,limit=1,sort=nearest] "
        "run damage @s %d minecraft:mob_projectile by @e[%s,limit=1]" % (SURV, BACK_DMG, UNIT),
        "function %s/fx/arrow_end" % B,
    ])
    w("fx/arrow_end", fx.glyph("pop", 1.0, PALE, kind="pop") + fx.spark("~ ~ ~", GOLD, size=1.1) + [
        "particle minecraft:crit ~ ~ ~ 0.2 0.2 0.2 0.4 8",
        "execute if entity @s[tag=rpg.jqb.af] run particle minecraft:flame ~ ~ ~ 0.1 0.1 0.1 0.12 10",
        "execute if entity @s[tag=rpg.jqb.af] run particle minecraft:lava ~ ~ ~ 0 0 0 0 2",
        "playsound rpg:jacques.arrow hostile @a[distance=..16] ~ ~ ~ 0.6 1.2",
        "scoreboard players set #d %s 8" % O,
        "execute if entity @s[tag=rpg.jqb.af] run function %s/fire/drop" % B,
        "kill @s",
    ])

    # 竖琴连弩：扇形五连发，箭与箭之间有缝
    w("skill/volley", start("volley", 34) + [
        "data merge entity @s {NoAI:1b}", face(), weapon("harp1"), anim("load"),
        "execute if score @s %s matches 1 run %s" % (O, say("弦已上紧。", name="竖琴连弩 · ")),
        "execute if score @s %s matches 2 run %s" % (O, say("火，是从弦上来的。", name="燃火连弩 · ", stage=2)),
    ])
    fan = ["execute positioned ~ ~1.45 ~ facing entity @p[distance=..%d,%s] eyes rotated ~%d ~ positioned ^ ^ ^0.9 run function %s/arrow/a5"
           % (BASIC_RANGE + 2, SURV, a, B) for a in (-24, -12, 0, 12, 24)]
    w("volley/fire", fan + ["particle minecraft:end_rod ^ ^1.4 ^1 0.2 0.2 0.2 0.05 8",
                            "function %s/vfx/muzzle" % B])
    w("sk/volley", loading(0) + [
        at(14, face()),
        at(14, "particle minecraft:end_rod ~ ~1.4 ~ 0.3 0.3 0.3 0.02 10"),
        at(2, "function %s/vfx/volley_charge" % B),
        "execute if score @s rpg_jq_t matches 2..18 run particle minecraft:enchant ~ ~1.5 ~ 0.8 0.8 0.8 1 6",
        at(20, anim("shoot")),
        at(20, "function %s/volley/fire" % B),
        at(22, weapon("harp1")),
        "execute if score @s rpg_jq_t matches 32.. run function %s/sk/end" % B,
    ])

    # 圣殿冲锋：俯身（预警）→ 翻滚贴近 → 起身下劈
    w("skill/charge", start("charge", 38) + [
        "data merge entity @s {NoAI:1b}", face(),
        "particle minecraft:cloud ~ ~0.2 ~ 0.4 0.05 0.4 0.02 10",
        "playsound minecraft:entity.horse.gallop hostile @a[distance=..24] ~ ~ ~ 1 0.8",
        say("为了圣殿！", name="圣殿冲锋 · "),
    ])
    w("sk/charge", [
        at(6, anim("roll_f")),
        "execute if score @s rpg_jq_t matches 6..16 unless entity @a[distance=..1.6,%s] if block ^ ^0.5 ^0.9 #minecraft:replaceable "
        "if block ^ ^1.5 ^0.9 #minecraft:replaceable run tp @s ^ ^ ^0.7" % SURV,
        "execute if score @s rpg_jq_t matches 6..16 run particle minecraft:cloud ~ ~0.1 ~ 0.2 0 0.2 0.01 2",
        "execute if score @s rpg_jq_t matches 6..16 run particle %s ~ ~0.9 ~ 0.3 0.5 0.3 0 4" % GOLD_DUST,
        "execute if score @s rpg_jq_t matches 6..16 run particle minecraft:electric_spark ~ ~0.6 ~ 0.3 0.3 0.3 0.05 2",
        at(17, face(6)),
        at(17, anim("slash1")),
        at(24, "function %s/strike/charge" % B),
        "execute if score @s rpg_jq_t matches 36.. run function %s/sk/end" % B,
    ])
    w("strike/charge", [tag_near(2.5, "^ ^ ^1.8")] + hurt_tagged(CHARGE_DMG) + fx.slash("^ ^1.2 ^1.6", PALE, size=3)
      + fx.slash("^ ^1.3 ^1.7", GOLD, size=3.8, frame=1) + [
        "particle minecraft:crit ^ ^1 ^1.8 0.8 0.4 0.8 0.3 16",
        "execute positioned ^ ^ ^1.8 run function %s/vfx/impact" % B,
    ])

    # 后撤射击：被贴身时向后翻滚 5 格，落地补一箭（落地那一刻是破绽）
    w("skill/backshot", start("backshot", 30) + [
        "data merge entity @s {NoAI:1b}", face(), anim("roll_b")])
    w("sk/backshot", [
        "execute if score @s rpg_jq_t matches 1..9 if block ^ ^0.5 ^-0.9 #minecraft:replaceable if block ^ ^1.5 ^-0.9 "
        "#minecraft:replaceable run tp @s ^ ^ ^-0.55",
        "execute if score @s rpg_jq_t matches 1..9 run particle minecraft:cloud ~ ~0.1 ~ 0.2 0 0.2 0.01 2",
        at(10, weapon("harp4")),
        at(10, face()),
        at(14, anim("shoot")),
        at(14, "execute positioned ~ ~1.45 ~ facing entity @p[distance=..%d,%s] eyes positioned ^ ^ ^0.9 run function %s/arrow/a6"
           % (BASIC_RANGE + 2, SURV, B)),
        at(16, weapon("harp1")),
        "execute if score @s rpg_jq_t matches 28.. run function %s/sk/end" % B,
    ])

    # 圣殿号角：召圣卫（一阶段 2 名，二阶段 1 名；场上最多 4 名）
    w("skill/horn", start("horn", 30) + [
        "data merge entity @s {NoAI:1b}", anim("horn"), weapon("none"),
        say("圣殿的弟兄们，列阵！", name="圣殿号角 · ", stage=1),
    ])
    w("sk/horn", [
        at(10, "function %s/horn/call" % B),
        at(10, "function %s/vfx/horn" % B),
        "execute if score @s rpg_jq_t matches 28.. run function %s/sk/end" % B,
    ])
    w("horn/call", [
        "execute store result score #n %s if entity @e[tag=rpg.jqb.guard]" % O,
        "execute if score #n %s matches ..%d positioned ^3 ^ ^1 run function %s/horn/one" % (O, GUARD_CAP - 1, B),
        "execute if score @s %s matches 2 run return 0" % O,
        "execute store result score #n %s if entity @e[tag=rpg.jqb.guard]" % O,
        "execute if score #n %s matches ..%d positioned ^-3 ^ ^1 run function %s/horn/one" % (O, GUARD_CAP - 1, B),
    ])
    w("horn/one", [
        "# 一名圣卫（as 载体，at 落点）：塔卫、重盾、术士随机",
        "function rpg:holy_guard/summon",
        "tag @e[type=minecraft:vindicator,tag=rpg.hg,tag=!rpg.jqb.guard,distance=..2,limit=1,sort=nearest] add rpg.jqb.guard",
    ] + fx.decal("sigil", 2.6, TEMPLAR_RED, pos="~ ~0.06 ~", kind="spin", life=30)
      + fx.decal("sq_0", 3, 0xF2F2F2, pos="~ ~0.1 ~", kind="sq") + fx.ray("~ ~ ~", TEMPLAR_WHITE) + light_pillar(0xFFF2C8) + [
        "particle minecraft:end_rod ~ ~1 ~ 0.4 1 0.4 0.05 16",
        "particle minecraft:totem_of_undying ~ ~1 ~ 0.3 0.8 0.3 0.3 20",
    ] + wave("minecraft:end_rod", 16, 0.25))

    # ---- 眩晕 / 破绽：护甲归零，原作眩晕动作
    w("skill/stagger", start("stagger", STUN + 2) + [
        "data merge entity @s {NoAI:1b,Invulnerable:0b,NoGravity:0b}",
        "attribute @s minecraft:armor base set 0",
        weapon("glaive"), anim("stun"),
    ])
    w("sk/stagger", every(8) + [
        "execute if score #m %s matches 0 run function %s/stagger_star" % (O, B),
        "execute if score @s rpg_jq_t matches %d.. run function %s/stagger/end" % (STUN, B),
    ])
    w("stagger_star", fx.twinkle("~0.3 ~2.25 ~", PALE, frame=2) + fx.twinkle("~-0.3 ~2.1 ~0.2", PALE, frame=0))
    w("stagger/end", ["function %s/sk/end" % B, anim("idle")])


# =====================================================================================
# 一阶段大招：十字审判、竖琴之弦
# =====================================================================================
def ults1():
    # 十字审判：插刀，地上亮起十字（四臂各宽 3、长 20），1.5 秒后同时炸开；对角空档安全；之后 1.5 秒定身
    w("ult/cross", start("cross", CROSS_LEN + 2) + [
        "data merge entity @s {NoAI:1b}", face(), anim("mighty"),
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.jqb.fx\",\"rpg.jqb.crossc\",\"rpg.jqb.ult\"]}",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.jqb.crossc] rpg_jq_life %d" % (CROSS_AT + 4),
        "execute as @e[type=minecraft:marker,tag=rpg.jqb.crossc] run tp @s ~ ~ ~ ~ 0",
        "execute as @e[type=minecraft:marker,tag=rpg.jqb.crossc] at @s run function %s/cross/warn" % B,
        "playsound minecraft:block.anvil.land hostile @a[distance=..32] ~ ~ ~ 1 0.6",
        say("跪下，在十字之前。", gloss="The Grand Master", name="十字审判 · "),
    ])
    warn = ["# 十字预警（as/at 十字中心）：四条暗金臂，各宽 3 长 20"]
    for a in (0, 90, 180, 270):
        warn += ["execute rotated ~%d 0 positioned ~ ~0.05 ~ run function %s/cross/arm_warn" % (a, B)]
    warn += fx.decal("glow", 6, 0x8F7430, pos="~ ~0.03 ~", life=CROSS_AT)
    warn += fx.decal("sigil", 4, GOLD_I, pos="~ ~0.08 ~", kind="spin", life=CROSS_AT)
    warn += fx.decal("hexagram", 7, 0xC9A04A, pos="~ ~0.06 ~", kind="spinr", life=CROSS_AT)
    for a in (0, 90, 180, 270):
        warn += ["execute rotated ~%d 0 positioned ^ ^ ^%d run function %s/cross/tip" % (a, CROSS_L, B)]
    w("cross/warn", warn)
    w("cross/tip", fx.ray("~ ~ ~", GOLD, long=True, tags=("rpg.jqb.ult",)) + fx.decal("ring", 3, GOLD_I, pos="~ ~0.07 ~", kind="spin", life=CROSS_AT))
    pulse = ["# 预警脉冲（as/at 十字中心）：四臂中线上的金尘"]
    for a in (0, 90, 180, 270):
        pulse += ["execute rotated ~%d 0 run function %s/cross/pulse_arm" % (a, B)]
    w("cross/pulse", pulse)
    w("cross/pulse_arm", along(GOLD_DUST, CROSS_L, 2.0, y=0.25, spread=0.5, n=2))
    w("cross/arm_warn", beam(0x8F7430, (CROSS_W, 0.02, CROSS_L), (0, 0, CROSS_L / 2.0), tags=("rpg.jqb.crossv", "rpg.jqb.ult"))
      + fx.born(CROSS_AT))
    blast = ["# 十字炸开（as/at 十字中心）：四臂同时判定 18；四道光、冲击环"]
    for a in (0, 90, 180, 270):
        blast += ["execute rotated ~%d 0 positioned ~ ~0.6 ~ run function %s/cross/arm" % (a, B)]
    blast += hurt_tagged(CROSS_DMG, "minecraft:magic")
    blast += fx.decal("shock_0", 10, 0xFFF2C8, pos="~ ~0.12 ~", kind="shock") + fx.glyph("burst", 4, PALE, pos="~ ~1.2 ~", kind="burst")
    blast += fx.glyph("burst", 7, GOLD, pos="~ ~2.4 ~", frame=1, kind="burst") + fx.decal("ring", 4, 0xFFF2C8, pos="~ ~0.15 ~", kind="ringx")
    blast += fx.decal("hexagram", 9, 0xFFE9A8, pos="~ ~0.1 ~", kind="spinf", life=24) + light_pillar(0xFFF2C8)
    blast += ["particle minecraft:flash{color:%d} ~ ~1.5 ~ 0 0 0 0 1 force" % 0xFFF2C8,
              "particle minecraft:totem_of_undying ~ ~1 ~ 1 1.5 1 0.6 80 force"]
    blast += wave("minecraft:end_rod", 32, 0.7) + wave("minecraft:firework", 24, 0.5, y=0.6)
    blast += ["playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..40] ~ ~ ~ 1.4 0.8",
              "playsound minecraft:block.bell.use hostile @a[distance=..40] ~ ~ ~ 1.4 0.6",
              "kill @s"]
    w("cross/blast", blast)
    arm = line("wide", int(CROSS_L / 1.5) + 1)
    arm += ["execute positioned ~ ~-0.55 ~ run function %s/cross/arm_fx" % B]
    w("cross/arm", arm)
    armfx = beam(0xFFF2C8, (CROSS_W, 0.02, CROSS_L), (0, 0, CROSS_L / 2.0), tags=("rpg.jqb.ult",)) + fx.born(kind="armfade")
    armfx += beam(0xFFFFFF, (0.8, 0.03, CROSS_L), (0, 0.02, CROSS_L / 2.0), tags=("rpg.jqb.ult",)) + fx.born(kind="armfade")
    for d in (3, 8, 13, 18):
        armfx += fx.ray("^ ^ ^%d" % d, PALE)
        armfx += ["particle minecraft:end_rod ^ ^0.4 ^%d 0.8 0.3 0.8 0.05 6" % d]
    for d in (6, 12, 19):
        armfx += fx.bolt("^ ^ ^%d" % d, GOLD)
    armfx += along("minecraft:firework", CROSS_L, 2.5, y=0.4, spread=0.6, n=3, speed=0.08)
    armfx += along("minecraft:electric_spark", CROSS_L, 1.5, y=0.3, spread=0.8, n=2, speed=0.3)
    w("cross/arm_fx", armfx)
    w("sk/cross", every(5) + [
        "execute if score #m %s matches 0 if score @s rpg_jq_t matches ..%d as @e[type=minecraft:marker,tag=rpg.jqb.crossc] at @s "
        "run function %s/cross/pulse" % (O, CROSS_AT - 2, B),
        "execute if score @s rpg_jq_t matches ..%d run particle minecraft:end_rod ~ ~1.2 ~ 0.5 1 0.5 0.03 2" % CROSS_AT,
        at(10, "playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1 1.4"),
        at(20, "playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1 1.7"),
        "execute if score @s rpg_jq_t matches %d as @e[type=minecraft:marker,tag=rpg.jqb.crossc] at @s run function %s/cross/blast" % (CROSS_AT, B),
        "execute if score @s rpg_jq_t matches %d.. run function %s/stagger/end" % (CROSS_LEN, B),
    ])

    # 竖琴之弦：朝天连射，一排排平行的琴弦从他脚下一道一道扫向远处落下，弦与弦之间有缝
    w("ult/harp", start("harp", HARP_FIRST + HARP_STEP * HARP_N + 8) + [
        "data merge entity @s {NoAI:1b}", face(), weapon("harp4"), anim("showoff"),
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.jqb.fx\",\"rpg.jqb.harpc\",\"rpg.jqb.ult\"]}",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.jqb.harpc] rpg_jq_life 3",
        "execute as @e[type=minecraft:marker,tag=rpg.jqb.harpc] run tp @s ~ ~ ~ ~ 0",
        "execute as @e[type=minecraft:marker,tag=rpg.jqb.harpc] at @s run function %s/harp/lay" % B,
        say("听啊，这是圣殿的琴。", gloss="The Grand Master", name="竖琴之弦 · "),
    ])
    lay = ["# 铺弦（as/at 中心，朝他面向的方向）：%d 道，间距 %s 格，每道长 %d" % (HARP_N, HARP_GAP, HARP_HALF * 2)]
    for k in range(HARP_N):
        d = -4 + k * HARP_GAP
        life = HARP_FIRST + HARP_STEP * k + 6
        lay += ["execute positioned ^ ^ ^%s rotated ~90 0 run function %s/harp/string%d" % (d, B, k)]
        w("harp/string%d" % k, [
            fx.marker("~ ~ ~", "rpg.jqb.str", "rpg.jqb.ult"),
            "tp @e[tag=%s,limit=1] ~ ~ ~ ~ 0" % NEW,
            "scoreboard players set @e[tag=%s] rpg_jq_id %d" % (NEW, k),
        ] + fx.born(life) + beam(GOLD_I, (0.12, 0.02, HARP_HALF * 2), (0, 0.05, 0), tags=("rpg.jqb.strv", "rpg.jqb.ult")) + [
            "scoreboard players set @e[tag=%s] rpg_jq_id %d" % (NEW, k),
        ] + fx.born(life))
    w("harp/lay", lay)
    w("harp/fall", [
        "# 一道弦落下（as/at 弦的标记，朝弦的方向）：变粗变亮，弦上 1 格内 12",
        "execute positioned ^ ^0.6 ^-%d run function %s/harp/hit" % (HARP_HALF, B),
        "scoreboard players operation #i %s = @s rpg_jq_id" % O,
        "execute as @e[tag=rpg.jqb.strv] if score @s rpg_jq_id = #i %s run data merge entity @s {start_interpolation:0,"
        "interpolation_duration:2,transformation:{scale:[0.7f,0.3f,%df]}}" % (O, HARP_HALF * 2),
        "execute as @e[tag=rpg.jqb.strv] if score @s rpg_jq_id = #i %s run data modify entity @s "
        "item.components.\"minecraft:custom_model_data\".colors[0] set value %d" % (O, 0xFFF2C8),
        "particle minecraft:end_rod ~ ~0.3 ~ 0 0 0 0.12 12",
        "execute positioned ^ ^ ^-%d run function %s/harp/fall_fx" % (HARP_HALF, B),
        "playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 %s",
        "kill @s",
    ])
    w("harp/fall_fx", ["# 弦落下的光（at 弦的一端，朝弦的方向）"]
      + fx.bolt("^ ^ ^%d" % (HARP_HALF // 3), GOLD) + fx.bolt("^ ^ ^%d" % HARP_HALF, PALE) + fx.bolt("^ ^ ^%d" % (HARP_HALF * 5 // 3), GOLD)
      + along("minecraft:electric_spark", HARP_HALF * 2, 1.5, y=0.3, spread=0.15, n=3, speed=0.25)
      + along(GOLD_DUST, HARP_HALF * 2, 2.0, y=0.5, spread=0.2, n=1))
    w("harp/hit", line("thin", int(HARP_HALF * 2 / 1.5) + 1) + hurt_tagged(HARP_DMG, "minecraft:magic"))
    harp = [at(18, anim("shoot")),
            at(18, "particle minecraft:end_rod ~ ~2.2 ~ 0.2 2 0.2 0.1 30"),
            at(18, "function %s/vfx/harp_sky" % B),
            "execute if score @s rpg_jq_t matches 2..17 run particle minecraft:enchant ~ ~1.6 ~ 1 1 1 1 8",
            at(18, "playsound rpg:jacques.fire hostile @a[distance=..32] ~ ~ ~ 1.2 1")]
    for k in range(HARP_N):
        harp.append("execute if score @s rpg_jq_t matches %d as @e[type=minecraft:marker,tag=rpg.jqb.str,scores={rpg_jq_id=%d}] "
                    "at @s run function %s/harp/fall" % (HARP_FIRST + HARP_STEP * k, k, B))
    harp.append("execute if score @s rpg_jq_t matches %d.. run function %s/stagger/end" % (HARP_FIRST + HARP_STEP * HARP_N + 6, B))
    w("sk/harp", harp)


# =====================================================================================
# 变身：火刑柱（约 6 秒）
# =====================================================================================
def morph():
    w("morph/tick", [
        "# 变身演出（as/at 载体，约 6 秒）：跪下祈祷，火刑柱升起，火爬上身体，大卫的幽灵出现，他在火里站起",
        "scoreboard players add @s rpg_jq_c 1",
        "execute if score @s rpg_jq_c matches 2 run function %s/morph/stake" % B,
        "execute if score @s rpg_jq_c matches 20..40 run particle minecraft:flame ~ ~0.3 ~ 0.4 0.2 0.4 0.02 4",
        "execute if score @s rpg_jq_c matches 40..60 run particle minecraft:flame ~ ~1.1 ~ 0.4 0.4 0.4 0.02 5",
        "execute if score @s rpg_jq_c matches 60..90 run particle minecraft:flame ~ ~1.9 ~ 0.4 0.5 0.4 0.03 6",
        "execute if score @s rpg_jq_c matches 20..90 run particle minecraft:smoke ~ ~2.4 ~ 0.3 0.4 0.3 0.02 2",
        "execute if score @s rpg_jq_c matches 20..118 run function %s/morph/ring" % B,
        "execute if score @s rpg_jq_c matches 44..86 run function %s/morph/helix" % B,
        "execute if score @s rpg_jq_c matches 60..86 run particle %s ~ ~1.2 ~ 0.5 0.9 0.5 0 3" % EMBER_DUST,
        "execute if score @s rpg_jq_c matches 70..86 run particle minecraft:lava ~ ~0.5 ~ 0.5 0.2 0.5 0 1",
        "execute if score @s rpg_jq_c matches 86..118 run particle minecraft:flame ~ ~1.2 ~ 0.4 0.8 0.4 0.03 6",
        "execute if score @s rpg_jq_c matches 86..118 run particle minecraft:campfire_cosy_smoke ~ ~2.6 ~ 0.3 0.2 0.3 0.01 1",
        "execute if score @s rpg_jq_c matches 20 run playsound minecraft:block.fire.ambient hostile @a[distance=..32] ~ ~ ~ 2 0.7",
        "execute if score @s rpg_jq_c matches 50 run playsound minecraft:item.firecharge.use hostile @a[distance=..32] ~ ~ ~ 1.2 0.6",
        "execute if score @s rpg_jq_c matches 40 run " + anim("kneel"),
        "execute if score @s rpg_jq_c matches 30 run function %s/morph/david" % B,
        "execute if score @s rpg_jq_c matches 80 run " + anim("hero"),
        "execute if score @s rpg_jq_c matches 86 run function %s/morph/rise" % B,
        "execute if score @s rpg_jq_c matches 120.. run function %s/stage/begin2" % B,
    ])
    w("morph/stake", [
        "# 火刑柱（原作地卜师石柱，焦黑）在他身后升起，脚下一圈火",
        "execute positioned ^ ^ ^-0.9 run %s" % fx.disp("pillar", scale=(10, 7.4, 10), color=CHAR, trans=(0, -2.4, 0)),
    ] + fx.born(kind="rise") + fx.decal("glow", 5, FIRE_D, pos="~ ~0.03 ~", life=118) + fx.decal("cracks", 4, 0x2A0A04, pos="~ ~0.05 ~", life=118) + [
        "playsound minecraft:block.stone.place hostile @a[distance=..32] ~ ~ ~ 1 0.5",
    ])
    w("morph/david", [
        "# 大卫的幽灵出现在最近的玩家身后（原作英雄模型，白色半透明；不能被攻击）",
        "execute at @p[distance=..%d,%s] rotated as @p[distance=..1,%s] rotated ~ 0 positioned ^-1.3 ^ ^-1.6 run function %s/david/summon"
        % (ARENA, SURV, SURV, B),
        "execute unless entity @e[%s] positioned ^ ^ ^6 run function %s/david/summon" % (GHOST, B),
    ])
    w("david/summon", [
        "summon minecraft:vindicator ~ ~ ~ {Tags:[\"rpg.jqd\"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,"
        "CustomName:{\"text\":\"大卫的幽灵\",\"color\":\"%s\",\"italic\":false},"
        "active_effects:[{id:\"invisibility\",duration:-1,amplifier:0,show_particles:0b}]}" % GHOST_C,
        "scoreboard players set @e[%s,distance=..1] rpg_jq_t 0" % GHOST,
        "particle minecraft:end_rod ~ ~1 ~ 0.4 1 0.4 0.05 30",
        "playsound minecraft:block.amethyst_block.chime hostile @a[distance=..32] ~ ~ ~ 1.4 1.2",
        say_david("你不是第一个推石头的人。"),
    ])
    morph_ring = every(4, "@s rpg_jq_c")
    for k in range(4):
        morph_ring += ["execute if score #m %s matches %d run %s" % (O, k, c) for c in ring("minecraft:flame", 2.2, 10, y=0.15, phase=k / 4.0)]
    w("morph/ring", morph_ring)
    w("morph/helix", helix("minecraft:flame", 14, 0.8, 0.1, 2.6, "@s rpg_jq_c", per=3)
      + helix("minecraft:small_flame", 14, 1.1, 0.4, 2.9, "@s rpg_jq_c", per=2))
    w("morph/rise", fx.glyph("burst", 4, EMBER, pos="~ ~1.4 ~", kind="burst")
      + fx.glyph("burst", 7, "#FFD08A", pos="~ ~2.2 ~", frame=1, kind="burst")
      + fx.decal("shock_0", 9, EMBER_I, pos="~ ~0.1 ~", kind="shock")
      + fx.decal("ring", 4, EMBER_I, pos="~ ~0.14 ~", kind="ringx")
      + fx.decal("hexagram", 8, FIRE_D, pos="~ ~0.08 ~", kind="spinf", life=34)
      + light_pillar(EMBER_I) + fx.ray("~1.4 ~ ~", EMBER, long=True) + fx.ray("~-1.4 ~ ~0.6", EMBER, long=True)
      + fx.ray("~0.2 ~ ~-1.5", EMBER, long=True)
      + wave("minecraft:flame", 32, 0.55) + wave("minecraft:flame", 20, 0.35, y=1.0, up=0.2) + fountain("minecraft:lava", 6, 0.6) + [
        "particle minecraft:flash{color:%d} ~ ~1.5 ~ 0 0 0 0 1 force" % EMBER_I,
        "particle minecraft:large_smoke ~ ~1.6 ~ 0.8 0.8 0.8 0.04 20 force",
        "particle minecraft:flame ~ ~1.2 ~ 0.6 1 0.6 0.15 80",
        "particle minecraft:lava ~ ~1 ~ 0.6 0.6 0.6 0 12",
        "playsound minecraft:entity.blaze.shoot hostile @a[distance=..40] ~ ~ ~ 1.4 0.5",
    ])
    w("s2/burn", every(3, "#tick %s" % O) + [
        "# 二阶段：他身上一直在烧（盔甲边缘、坟墓克星）",
        "execute if score #m %s matches 0 run particle minecraft:flame ~ ~1.2 ~ 0.3 0.6 0.3 0.01 2" % O,
        "execute if score #m %s matches 1 run particle minecraft:small_flame ~ ~2 ~ 0.3 0.3 0.3 0.01 2" % O,
        "execute if score #m %s matches 2 run particle %s ~ ~1.4 ~ 0.35 0.7 0.35 0 2" % (O, EMBER_DUST),
    ] + helix("minecraft:flame", 10, 0.65, 0.1, 2.3, "#tick %s" % O, per=2) + every(14, "#tick %s" % O) + [
        "execute if score #m %s matches 0 run particle minecraft:lava ~ ~1 ~ 0.3 0.4 0.3 0 1" % O,
        "execute if score #m %s matches 7 run particle minecraft:large_smoke ~ ~2.3 ~ 0.2 0.1 0.2 0.01 1" % O,
    ])


# =====================================================================================
# 二阶段招式：火刑跃击、莫莱的诅咒；大招：七座火刑柱、最后的冲锋；大卫的投石
# =====================================================================================
def stage2():
    # 火刑跃击
    w("skill/leap", start("leap", LEAP_LEN + 2) + [
        "data merge entity @s {NoAI:1b}", face(), anim("leap"),
        say("从火里来。", name="火刑跃击 · ", stage=2),
    ])
    w("sk/leap", [
        "execute if score @s rpg_jq_t matches %d at @r[distance=..%d,%s] run function %s/leap/mark" % (LEAP_MARK, BASIC_RANGE, SURV, B),
        "execute if score @s rpg_jq_t matches %d unless entity @e[type=minecraft:marker,tag=rpg.jqb.land] run function %s/leap/mark" % (LEAP_MARK, B),
        at(LEAP_UP, "data merge entity @s {Invulnerable:1b,NoGravity:1b}"),
        at(LEAP_UP, "particle minecraft:flame ~ ~0.5 ~ 0.4 0.2 0.4 0.1 30"),
        at(LEAP_UP, "function %s/vfx/takeoff" % B),
        "execute if score @s rpg_jq_t matches %d at @e[type=minecraft:marker,tag=rpg.jqb.land,limit=1] run function %s/vfx/meteor" % (LEAP_DOWN - 5, B),
        at(LEAP_UP, "tp @s ~ ~14 ~"),
        "execute if score @s rpg_jq_t matches %d at @e[type=minecraft:marker,tag=rpg.jqb.land,limit=1] run tp @s ~ ~ ~" % LEAP_DOWN,
        at(LEAP_DOWN, anim("land")),
        "execute if score @s rpg_jq_t matches %d at @s run function %s/leap/land" % (LEAP_DOWN + 1, B),
        "execute if score @s rpg_jq_t matches %d.. run function %s/sk/end" % (LEAP_LEN, B),
    ])
    w("leap/mark", [
        "# 落点（at 目标脚下）：一圈火光，1 秒后他砸下来",
        fx.marker("~ ~ ~", "rpg.jqb.land")] + fx.born(LEAP_DOWN - LEAP_MARK + 6)
      + fx.decal("glow", LEAP_R * 2 + 1, FIRE_D, pos="~ ~0.03 ~", life=LEAP_DOWN - LEAP_MARK + 2, tags=("rpg.jqb.landv",))
      + fx.decal("ring", LEAP_R * 2, EMBER_I, pos="~ ~0.1 ~", life=LEAP_DOWN - LEAP_MARK + 2, tags=("rpg.jqb.landv",))
      + fx.decal("sigil", LEAP_R * 1.6, 0xFFB060, pos="~ ~0.12 ~", kind="spinf", life=LEAP_DOWN - LEAP_MARK + 2, tags=("rpg.jqb.landv",))
      + ring("minecraft:flame", LEAP_R, 18, y=0.2) + [
        "particle minecraft:flame ~ ~0.2 ~ %d 0.1 %d 0.02 30" % (LEAP_R - 1, LEAP_R - 1),
        "playsound minecraft:block.fire.ambient hostile @a[distance=..32] ~ ~ ~ 2 1.2",
    ])
    w("leap/land", [
        "# 砸地（at 落点）：4 格内 14，留下火圈 4 秒",
        "data merge entity @s {Invulnerable:0b,NoGravity:0b}",
        tag_near(LEAP_R),
    ] + hurt_tagged(LEAP_DMG, "minecraft:magic") + [
        "kill @e[tag=rpg.jqb.landv]",
        "kill @e[type=minecraft:marker,tag=rpg.jqb.land]",
        fx.marker("~ ~ ~", "rpg.jqb.firering"),
    ] + fx.born(80) + fx.decal("ring", 9, FIRE_D, pos="~ ~0.06 ~", life=80)
      + fx.decal("sq_0", LEAP_R * 2 + 2, EMBER_I, pos="~ ~0.1 ~", kind="sq")
      + fx.decal("shock_0", LEAP_R * 2 + 4, 0xFFD08A, pos="~ ~0.13 ~", kind="shock") + [
        "particle minecraft:flame ~ ~0.3 ~ 2 0.3 2 0.1 60",
        "function %s/vfx/land" % B,
        "playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1.2 0.7",
    ])

    # 莫莱的诅咒：最近的一名玩家打上印记 8 秒，到时以他为中心炸开；坟墓克星打中他会提前引爆
    w("skill/curse", start("curse", 24) + [
        "data merge entity @s {NoAI:1b}", face(), anim("curse"),
        say("我以火刑柱起誓——你也一样。", name="莫莱的诅咒 · ", stage=2),
    ])
    w("sk/curse", [
        at(8, "execute as @p[distance=..%d,%s] at @s run function %s/curse/mark" % (BASIC_RANGE, SURV, B)),
        at(4, "function %s/vfx/curse_cast" % B),
        "execute if score @s rpg_jq_t matches 22.. run function %s/sk/end" % B,
    ])
    w("curse/mark", [
        "tag @s add rpg.jqb.cursed",
        "scoreboard players set @s rpg_jq_cu %d" % CURSE_TICKS,
        "playsound minecraft:entity.wither.ambient hostile @a[distance=..24] ~ ~ ~ 0.8 1.4",
        "tellraw @s %s" % ui.row(ui.comp("〖莫莱的诅咒〗", ui.BROADCAST_WARN, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                                 ui.comp("8 秒后在你身上炸开——离开队友。", ui.BROADCAST_WARN)),
    ] + fx.glyph("burst", 1.6, CURSE, pos="~ ~1.2 ~", kind="burst") + fx.decal("sigil", 3, CURSE_I, pos="~ ~0.08 ~", kind="spinf", life=20)
      + fx.glyph("rune", 1.2, CURSE, pos="~ ~2.4 ~", life=20) + wave(CURSE_DUST, 16, 0.25, y=0.3) + [
        "particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.6 0.3 0.02 10",
    ])
    w("vfx/curse_cast", fx.glyph("rune", 1.6, CURSE, pos="~ ~2.8 ~", life=16) + fx.decal("sigil", 4, CURSE_I, pos="~ ~0.08 ~", kind="spinf", life=16)
      + ["particle %s ~ ~1.5 ~ 0.6 0.8 0.6 0 20" % CURSE_DUST])
    w("curse/tick", [
        "# 被诅咒的人（as/at 他）：暗红符文在头顶，倒数，到时炸开",
        "scoreboard players remove @s rpg_jq_cu 1",
        "execute if score @s rpg_jq_cu matches ..0 run return run function %s/curse/pop" % B,
        "particle minecraft:dust{color:[0.55,0.04,0.08],scale:1.2} ~ ~1 ~ 0.4 0.6 0.4 0 2",
    ] + helix(CURSE_DUST, 8, 0.9, 0.15, 0.15, "@s rpg_jq_cu", per=3) + every(20, "@s rpg_jq_cu") + [
        "execute if score #m %s matches 0 run function %s/curse/beat" % (O, B),
    ])
    w("curse/beat", fx.glyph("rune", 0.7, CURSE, pos="~ ~2.3 ~", life=16) + wave(CURSE_DUST, 12, 0.18, y=0.2) + [
        "playsound minecraft:block.note_block.basedrum hostile @a[distance=..16] ~ ~ ~ 1 0.6",
    ])
    w("curse/pop", [
        "# 印记炸开（as/at 被诅咒的人）：3 格内所有人 12",
        "function %s/curse/clear" % B,
        "tag @a[distance=..%d,%s] add rpg.jqb.chit" % (CURSE_R, SURV),
        "execute as @a[tag=rpg.jqb.chit] run damage @s %d minecraft:magic by @e[%s,limit=1]" % (CURSE_DMG, UNIT),
        "tag @a remove rpg.jqb.chit",
    ] + fx.glyph("burst", 3.4, CURSE, pos="~ ~1.2 ~", kind="burst") + fx.decal("shock_0", CURSE_R * 2 + 2, CURSE_I, pos="~ ~0.1 ~", kind="shock")
      + fx.decal("sigil", 2, CURSE_I, pos="~ ~0.12 ~", kind="ringm") + wave(CURSE_DUST, 24, 0.5, y=0.4) + wave("minecraft:flame", 16, 0.35, y=0.8) + [
        "particle minecraft:dust{color:[0.55,0.04,0.08],scale:2} ~ ~1 ~ 1.4 0.6 1.4 0 40",
        "particle minecraft:flash{color:%d} ~ ~1.2 ~ 0 0 0 0 1 force" % CURSE_I,
        "particle minecraft:large_smoke ~ ~1 ~ 0.6 0.6 0.6 0.05 16",
        "playsound minecraft:entity.generic.explode hostile @a[distance=..32] ~ ~ ~ 1 1.2",
    ])
    w("curse/clear", ["tag @s remove rpg.jqb.cursed", "scoreboard players reset @s rpg_jq_cu"])

    # ---- 大卫的幽灵：跟在最近的玩家身后；大招起手时甩石子，2 秒后命中，打断大招
    w("david/tick", [
        "# 大卫的幽灵（as/at 它）：站在最近的玩家身后，面朝雅克",
        "execute if score @s rpg_jq_t matches 1.. run scoreboard players remove @s rpg_jq_t 1",
        "execute if score @s rpg_jq_t matches 1.. facing entity @e[%s,limit=1] feet run return run tp @s ~ ~ ~ ~ 0" % UNIT,
        "execute at @p[distance=..%d,%s] rotated as @p[distance=..1,%s] rotated ~ 0 positioned ^-1.3 ^ ^-1.6 facing entity @e[%s,limit=1] feet "
        "run tp @s ~ ~ ~ ~ 0" % (ARENA, SURV, SURV, UNIT),
        "particle minecraft:end_rod ~ ~1.2 ~ 0.25 0.5 0.25 0.01 1",
        "particle minecraft:dust{color:[0.85,0.93,1.0],scale:1.1} ~ ~1 ~ 0.3 0.7 0.3 0 1",
    ])
    w("david/throw", [
        "# 甩出石子（as 雅克）：没有幽灵（调试）就不打断",
        "execute unless entity @e[%s] run return 0" % GHOST,
        "execute as @e[%s,limit=1] at @s run function %s/david/sling" % (GHOST, B),
    ])
    w("david/sling", [
        "scoreboard players set @s rpg_jq_t 30",
        "function %s/anim/enter/throw" % DAVID,
        "execute positioned ~ ~1.6 ~ run %s" % fx.glyph("star", 0.9, GHOST_C, frame=1, tags=("rpg.jqb.stone",), born_now=False)[0],
    ] + fx.born(STONE_AT + 4) + [
        "particle minecraft:end_rod ~ ~1.6 ~ 0.2 0.2 0.2 0.05 10",
    ] + fx.glyph("burst", 1.6, GHOST_C, pos="~ ~1.6 ~", kind="burst") + wave("minecraft:end_rod", 12, 0.15, y=1.6) + [
        say_david("……歌利亚也是这么高大。"),
    ])
    w("david/stone_up", [
        "# 石子先飞到他头顶上方（as 石子；召出后隔一刻再传送，客户端才会插值）",
        "data merge entity @s {teleport_duration:18}",
        "execute at @e[%s,limit=1] run tp @s ~ ~5 ~" % UNIT,
    ])
    w("david/stone_fall", [
        "# 石子从高处落向他（as 石子）",
        "data merge entity @s {teleport_duration:%d}" % (STONE_AT - 22),
        "execute at @e[%s,limit=1] run tp @s ~ ~1.7 ~" % UNIT,
    ])
    w("david/hit", [
        "# 石子命中（as/at 雅克）：打断大招，眩晕 3 秒、护甲归零",
        "kill @e[tag=rpg.jqb.stone]",
        "kill @e[tag=rpg.jqb.ult]",
        "kill @e[type=minecraft:marker,tag=rpg.jqb.stake]",
        "function %s/skill/stagger" % B,
    ] + fx.glyph("burst", 2.8, GHOST_C, pos="~ ~1.7 ~", kind="burst") + fx.glyph("pop", 1.6, TEMPLAR_WHITE, pos="~ ~1.7 ~", kind="pop") + [
        "particle minecraft:end_rod ~ ~1.7 ~ 0.3 0.3 0.3 0.2 30",
        "particle minecraft:flash{color:%d} ~ ~1.7 ~ 0 0 0 0 1 force" % 0xD8ECFF,
    ] + fx.decal("shock_0", 8, 0xD8ECFF, pos="~ ~0.1 ~", kind="shock") + wave("minecraft:end_rod", 24, 0.5, y=1.7)
      + wave("minecraft:firework", 12, 0.3, y=1.7, up=0.3) + [
        "playsound minecraft:block.stone.break hostile @a[distance=..40] ~ ~ ~ 1.4 0.6",
        "playsound minecraft:item.shield.break hostile @a[distance=..40] ~ ~ ~ 1.2 0.7",
        say("……石子？", stage=2),
        "# 石子只有一颗：打断这一次之后，大卫的幽灵就消散了（之后的大招不再被打断）",
        "execute as @e[%s] at @s run function %s/david/fade" % (GHOST, B),
    ])
    w("david/fade", [
        "# 大卫的幽灵消散（as/at 它）：一道天光，光点升起，然后移除",
    ] + light_pillar(0xD8ECFF) + fx.glyph("burst", 2.2, GHOST_C, pos="~ ~1.2 ~", kind="burst")
      + wave("minecraft:end_rod", 18, 0.25, y=1.0) + fountain("minecraft:end_rod", 16, 0.25, y=1.2, up=0.8) + [
        "particle minecraft:dust{color:[0.85,0.93,1.0],scale:1.4} ~ ~1 ~ 0.4 0.8 0.4 0 30",
        "particle minecraft:flash{color:%d} ~ ~1.2 ~ 0 0 0 0 1 force" % 0xD8ECFF,
        "playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..40] ~ ~ ~ 1.2 1.4",
        "playsound minecraft:block.beacon.deactivate hostile @a[distance=..40] ~ ~ ~ 1 1.2",
        say_david("剩下的，交给你了。"),
        "function %s/clear_unit" % B,
    ])
    stone_check = ["execute if score @s rpg_jq_t matches %d if entity @e[tag=rpg.jqb.stone] run return run function %s/david/hit" % (STONE_AT, B),
                   "execute if score @s rpg_jq_t matches 2 as @e[tag=rpg.jqb.stone] run function %s/david/stone_up" % B,
                   "execute if score @s rpg_jq_t matches 20 as @e[tag=rpg.jqb.stone] run function %s/david/stone_fall" % B]

    # 七座火刑柱：一圈七根，柱间依次连起火墙，最后整圈收拢；找最后才连上的那段缺口冲出去
    w("ult/stakes", start("stakes", STAKE_HIT + 4) + [
        "data merge entity @s {NoAI:1b}", face(), anim("gong"), weapon("none"),
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.jqb.fx\",\"rpg.jqb.stakec\",\"rpg.jqb.ult\"]}",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.jqb.stakec] rpg_jq_life %d" % (STAKE_HIT + 6),
        "execute as @e[type=minecraft:marker,tag=rpg.jqb.stakec] run tp @s ~ ~ ~ ~ 0",
        "execute as @e[type=minecraft:marker,tag=rpg.jqb.stakec] at @s run function %s/stakes/raise" % B,
        "playsound minecraft:block.bell.use hostile @a[distance=..40] ~ ~ ~ 2 0.5",
        "function %s/vfx/ult2" % B,
        say("七座火刑柱。教廷给我的，我还给你。", gloss="The Burning Oath", name="七座火刑柱 · ", stage=2),
    ])
    raise_ = ["# 七根火刑柱（as/at 圆心，朝他面向的方向）"]
    for i in range(STAKE_N):
        a = i * 360.0 / STAKE_N
        raise_ += ["execute rotated ~%s 0 positioned ^ ^ ^%d run function %s/stakes/one%d" % (round(a, 3), STAKE_R, B, i)]
        w("stakes/one%d" % i, [
            fx.marker("~ ~ ~", "rpg.jqb.stake", "rpg.jqb.ult"),
            "scoreboard players set @e[tag=%s] rpg_jq_id %d" % (NEW, i),
        ] + fx.born(STAKE_HIT + 2) + [
            fx.disp("pillar", scale=(8, 7.4, 8), color=CHAR, trans=(0, -2.4, 0), tags=("rpg.jqb.stakev", "rpg.jqb.ult"), tp=15),
        ] + fx.born(kind="rise") + [
            "particle minecraft:flame ~ ~1 ~ 0.3 1 0.3 0.02 12",
            "particle minecraft:large_smoke ~ ~0.3 ~ 0.6 0.1 0.6 0.03 8",
            "playsound minecraft:block.stone.place hostile @a[distance=..32] ~ ~ ~ 1 0.6",
        ] + fx.decal("glow", 3, FIRE_D, pos="~ ~0.05 ~", life=STAKE_HIT, tags=("rpg.jqb.ult",)))
    raise_ += fx.decal("glow", STAKE_R * 2 + 2, 0x5A1206, pos="~ ~0.03 ~", life=STAKE_HIT, tags=("rpg.jqb.ult",))
    w("stakes/raise", raise_)
    sk_st = list(stone_check)
    for i in range(STAKE_N):
        sk_st.append("execute if score @s rpg_jq_t matches %d as @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=%d}] "
                     "at @s run function %s/stakes/light" % (STAKE_FIRST + STAKE_STEP * i, i, B))
    sk_st += every(10) + [
        "execute if score #m %s matches 0 if score @s rpg_jq_t matches %d..%d as @e[type=minecraft:marker,tag=rpg.jqb.stake,tag=rpg.jqb.lit] "
        "at @s run function %s/stakes/wall" % (O, STAKE_FIRST, STAKE_PULL, B),
        "execute if score #m %s matches 0 if score @s rpg_jq_t matches %d..%d as @e[type=minecraft:marker,tag=rpg.jqb.stake,tag=rpg.jqb.lit] "
        "at @s run function %s/stakes/blaze" % (O, STAKE_FIRST, STAKE_PULL, B),
        at(STAKE_PULL, "function %s/stakes/pull" % B),
        "execute if score @s rpg_jq_t matches %d at @e[type=minecraft:marker,tag=rpg.jqb.stakec,limit=1] run function %s/stakes/close"
        % (STAKE_HIT, B),
        "execute if score @s rpg_jq_t matches %d.. run function %s/skill/stagger" % (STAKE_HIT + 2, B),
    ]
    w("sk/stakes", sk_st)
    w("stakes/light", [
        "# 第 i 根柱点燃，和下一根之间连起火墙（as/at 这根柱的标记）",
        "tag @s add rpg.jqb.lit",
        "particle minecraft:flame ~ ~1.5 ~ 0.3 1 0.3 0.05 20",
        "particle minecraft:flash{color:%d} ~ ~2 ~ 0 0 0 0 1 force" % EMBER_I,
        "function %s/stakes/light_fx" % B,
        "playsound minecraft:item.firecharge.use hostile @a[distance=..32] ~ ~ ~ 1 0.8",
        "function %s/stakes/wall_show" % B,
        "function %s/stakes/wall" % B,
    ])
    w("stakes/light_fx", fx.ray("~ ~ ~", EMBER, long=True, tags=("rpg.jqb.ult",)) + fx.glyph("burst", 2.4, EMBER, pos="~ ~2 ~", kind="burst")
      + fx.decal("ring", 2, EMBER_I, pos="~ ~0.1 ~", kind="ringm", tags=("rpg.jqb.ult",))
      + wave("minecraft:flame", 14, 0.3, y=0.3) + fountain("minecraft:lava", 4, 0.5, y=2.2))
    w("stakes/blaze", ["# 点燃的柱子一直在烧（as/at 柱的标记，每 10 刻）",
                       "particle minecraft:flame ~ ~1.6 ~ 0.25 1.4 0.25 0.02 10",
                       "particle %s ~ ~2.4 ~ 0.3 1 0.3 0 3" % EMBER_DUST,
                       "particle minecraft:lava ~ ~3 ~ 0.2 0.3 0.2 0 1",
                       "particle minecraft:campfire_cosy_smoke ~ ~4.2 ~ 0.2 0.1 0.2 0.01 1"])
    seg = 2 * STAKE_R * math.sin(math.pi / STAKE_N)
    for fn, then, note in (("wall", "burn", "沿墙每 1.3 格查一次，碰到的人烧 4"), ("wall_show", "show", "火墙的墙体")):
        nxt = ["# 火墙（as/at 柱 i，朝柱 i+1）：" + note]
        for i in range(STAKE_N):
            j = (i + 1) % STAKE_N
            nxt.append("execute if score @s rpg_jq_id matches %d facing entity @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=%d},limit=1] feet "
                       "positioned ~ ~0.4 ~ run function %s/stakes/%s" % (i, j, B, then))
        w("stakes/" + fn, nxt)
    wall_life = STAKE_PULL - STAKE_FIRST + 4
    w("stakes/show", ["# 火墙三层：暗红的底、橙色的墙、金白的芯"]
      + beam(FIRE_D, (0.7, 1.0, seg), (0, 0.1, seg / 2), tags=("rpg.jqb.ult", "rpg.jqb.wallv")) + fx.born(wall_life)
      + beam(EMBER_I, (0.3, 2.2, seg), (0, 0.7, seg / 2), tags=("rpg.jqb.ult", "rpg.jqb.wallv")) + fx.born(wall_life)
      + beam(0xFFE2A0, (0.1, 2.8, seg), (0, 0.9, seg / 2), tags=("rpg.jqb.ult", "rpg.jqb.wallv")) + fx.born(wall_life))
    w("stakes/burn", line("fire", 6) + hurt_tagged(WALL_DMG, "minecraft:in_fire"))
    w("stakes/pull", [
        "# 整圈向中心收拢（柱子插值滑向圆心）",
        "execute as @e[tag=rpg.jqb.stakev] run data merge entity @s {teleport_duration:15}",
        "execute as @e[tag=rpg.jqb.stakev] at @e[type=minecraft:marker,tag=rpg.jqb.stakec,limit=1] run tp @s ~ ~ ~",
        "tag @e[tag=rpg.jqb.stake] remove rpg.jqb.lit",
        "kill @e[tag=rpg.jqb.wallv]",
        "playsound minecraft:block.fire.ambient hostile @a[distance=..40] ~ ~ ~ 2 0.5",
        "execute at @e[type=minecraft:marker,tag=rpg.jqb.stakec,limit=1] run function %s/stakes/pull_fx" % B,
    ])
    pull = ["# 收拢（at 圆心）：一圈火向圆心卷进来"]
    for i in range(28):
        a = 2 * math.pi * i / 28
        c, sn = math.cos(a), math.sin(a)
        for y in (0.3, 1.4):
            pull.append("particle minecraft:flame ~%.2f ~%.1f ~%.2f %.3f 0 %.3f 0.55 0 force" % (STAKE_R * c, y, STAKE_R * sn, -c, -sn))
    pull += fx.decal("glow", STAKE_R * 2, FIRE_D, pos="~ ~0.04 ~", life=STAKE_HIT - STAKE_PULL + 2, tags=("rpg.jqb.ult",))
    w("stakes/pull_fx", pull)
    w("stakes/close", [
        "# 收拢（at 圆心）：圈里所有人 16",
        tag_near(STAKE_R + 0.5),
    ] + hurt_tagged(STAKE_DMG, "minecraft:magic") + [
        "kill @e[tag=rpg.jqb.stakev]",
        "kill @e[type=minecraft:marker,tag=rpg.jqb.stake]",
    ] + fx.decal("shock_0", STAKE_R * 2 + 4, EMBER_I, pos="~ ~0.12 ~", kind="shock") + fx.glyph("burst", 5, EMBER, pos="~ ~1.4 ~", kind="burst")
      + fx.glyph("burst", 9, "#FFD08A", pos="~ ~3 ~", frame=1, kind="burst") + fx.decal("ring", 5, 0xFFD08A, pos="~ ~0.15 ~", kind="ringx")
      + fx.decal("hexagram", 12, FIRE_D, pos="~ ~0.08 ~", kind="spinf", life=30) + fx.decal("cracks", 10, 0x2A0A04, pos="~ ~0.05 ~", life=80)
      + light_pillar(EMBER_I) + wave("minecraft:flame", 36, 0.8) + wave("minecraft:flame", 24, 0.5, y=1.2, up=0.25)
      + fountain("minecraft:lava", 8, 0.8) + [
        "particle minecraft:flash{color:%d} ~ ~1.5 ~ 0 0 0 0 1 force" % EMBER_I,
        "particle minecraft:large_smoke ~ ~1 ~ 2 0.6 2 0.05 40 force",
        "particle minecraft:flame ~ ~0.5 ~ %d 0.4 %d 0.2 120" % (STAKE_R - 2, STAKE_R - 2),
        "playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1.4 0.6",
    ])

    # 最后的冲锋：三次翻滚冲锋（每次转向最近的玩家），最后一记燃火横扫 20；之后喘息 3 秒
    w("ult/last", start("last", 3 * 22 + 30) + [
        "data merge entity @s {NoAI:1b}", face(),
        "function %s/vfx/ult2" % B,
        say("最后一次——为了圣殿。", gloss="The Burning Oath", name="最后的冲锋 · ", stage=2),
    ])
    last = list(stone_check)
    for k in range(3):
        t0 = LAST_ROLL + 22 * k
        last += [
            at(t0 - 6, face()),
            at(t0 - 6, "particle minecraft:flame ~ ~0.2 ~ 0.5 0.05 0.5 0.05 16"),
            at(t0, "function %s/vfx/dash_start" % B),
            at(t0 - 6, "playsound minecraft:entity.horse.gallop hostile @a[distance=..24] ~ ~ ~ 1 0.7"),
            at(t0, anim("roll_f")),
            at(t0, "tag @a remove rpg.jqb.rolled"),
            "execute if score @s rpg_jq_t matches %d..%d run function %s/last/dash" % (t0, t0 + 10, B),
        ]
    t3 = LAST_ROLL + 22 * 3
    last += [
        at(t3, face(8)),
        at(t3, anim("sweep")),
        at(t3 + 3, "function %s/last/sweep" % B),
        "execute if score @s rpg_jq_t matches %d.. run function %s/skill/stagger" % (t3 + 20, B),
    ]
    w("sk/last", last)
    w("last/dash", [
        "execute if block ^ ^0.5 ^0.9 #minecraft:replaceable if block ^ ^1.5 ^0.9 #minecraft:replaceable run tp @s ^ ^ ^0.8",
        "particle minecraft:flame ~ ~0.2 ~ 0.3 0.1 0.3 0.02 4",
        "particle minecraft:flame ~ ~1 ~ 0.3 0.6 0.3 0.04 6",
        "particle %s ~ ~1 ~ 0.35 0.6 0.35 0 4" % EMBER_DUST,
        "particle minecraft:large_smoke ~ ~0.4 ~ 0.2 0.2 0.2 0.01 1",
        "tag @a[distance=..1.6,%s,tag=!rpg.jqb.rolled] add rpg.jqb.hit" % SURV,
        "tag @a[tag=rpg.jqb.hit] add rpg.jqb.rolled",
    ] + hurt_tagged(CHARGE_DMG))
    w("last/sweep", [tag_near(LAST_SWEEP - 1, "^ ^ ^1.2")] + hurt_tagged(LAST_DMG) + [
        "execute positioned ^ ^1.1 ^1.2 run %s" % fx.disp("crescent", color=EMBER_I),
        "execute as @e[tag=%s] positioned as @s run tp @s ~ ~ ~ ~ 0" % NEW,
    ] + fx.born(kind="sweepw") + [
        "execute positioned ^ ^1.3 ^1.2 run %s" % fx.disp("crescent", color=0xFFD08A, scale=0.8),
        "execute as @e[tag=%s] positioned as @s run tp @s ~ ~ ~ ~ 0" % NEW,
    ] + fx.born(kind="sweep") + fx.glyph("burst", 5, EMBER, pos="^ ^1.2 ^2", kind="burst") + fx.slash("^ ^1.2 ^2", "#FFD08A", size=4.5) + [
        "execute positioned ^ ^ ^1.5 run function %s/vfx/land" % B,
        "function %s/strike/fireline" % B,
        "tag @a remove rpg.jqb.rolled",
        "particle minecraft:flame ^ ^1 ^2 1.6 0.3 1.6 0.1 60",
        "playsound minecraft:entity.blaze.shoot hostile @a[distance=..32] ~ ~ ~ 1.4 0.6",
    ])


# =====================================================================================
# 特效层（教皇战标准：形状用展示实体，能量用粒子）。一阶段金白，二阶段火
# =====================================================================================
def vfx():
    w("vfx/intro", ["# 登场（at 落点）：金光柱从天而降，脚下转动的红十字圣印与金色六芒星，光浪扫开"]
      + light_pillar(0xFFF2C8) + fx.decal("sigil", 4, TEMPLAR_RED, pos="~ ~0.06 ~", kind="spin", life=44)
      + fx.decal("hexagram", 6, GOLD_I, pos="~ ~0.04 ~", kind="spinr", life=44)
      + fx.decal("ring", 3, 0xFFF2C8, pos="~ ~0.1 ~", kind="ringx") + fx.glyph("burst", 5, GOLD, pos="~ ~2 ~", kind="burst")
      + wave("minecraft:end_rod", 28, 0.45) + wave("minecraft:firework", 16, 0.3, y=1.2, up=0.2) + [
        "particle minecraft:flash{color:%d} ~ ~2 ~ 0 0 0 0 1 force" % 0xFFF2C8,
        "particle minecraft:totem_of_undying ~ ~1.2 ~ 0.6 1 0.6 0.5 60 force",
    ])
    w("vfx/front1", ["# 坟墓克星下劈（as/at 他）：金色双层弧光、火花"]
      + fx.slash("^ ^1.2 ^1.6", GOLD) + fx.slash("^ ^1.25 ^1.7", PALE, size=1.8, frame=1) + fx.spark("^ ^1 ^2", PALE, size=1.2) + [
        "particle minecraft:crit ^ ^1 ^1.8 0.6 0.4 0.6 0.3 14",
        "particle minecraft:enchanted_hit ^ ^1.1 ^1.8 0.5 0.4 0.5 0.3 10",
        "particle minecraft:electric_spark ^ ^0.4 ^2 0.4 0.1 0.4 0.3 8",
    ])
    w("vfx/front2", ["# 燃刃下劈（as/at 他）：火色双层弧光、火星迸溅"]
      + fx.slash("^ ^1.2 ^1.6", EMBER) + fx.slash("^ ^1.25 ^1.7", "#FFD08A", size=1.8, frame=1) + fx.spark("^ ^1 ^2", "#FFD08A", size=1.2) + [
        "particle minecraft:crit ^ ^1 ^1.8 0.6 0.4 0.6 0.3 10",
        "particle minecraft:flame ^ ^1 ^1.8 0.5 0.4 0.5 0.06 16",
        "particle minecraft:lava ^ ^0.6 ^2 0.3 0.1 0.3 0 3",
        "particle %s ^ ^1 ^1.8 0.6 0.4 0.6 0 6" % EMBER_DUST,
    ])
    arc = []
    for deg in range(-60, 61, 15):
        a = math.radians(deg)
        arc.append((round(3.0 * math.sin(a), 2), round(3.0 * math.cos(a), 2), round(math.sin(a), 3), round(math.cos(a), 3)))
    w("vfx/sweep1", ["# 横扫（as/at 他）：弧线上的金光向外甩出"]
      + ["particle minecraft:end_rod ^%s ^1.1 ^%s 0.15 0.15 0.15 0.06 3 force" % (x, z) for x, z, _, _ in arc]
      + ["particle %s ^%s ^1.1 ^%s 0.1 0.1 0.1 0 2 force" % (GOLD_DUST, x, z) for x, z, _, _ in arc]
      + fx.decal("shock_0", 5, 0xFFF2C8, pos="^ ^0.1 ^1.5", kind="shock"))
    w("vfx/sweep2", ["# 燃刃横扫（as/at 他）：弧线上的火向外甩出"]
      + ["particle minecraft:flame ^%s ^1.1 ^%s 0.15 0.15 0.15 0.06 3 force" % (x, z) for x, z, _, _ in arc]
      + ["particle %s ^%s ^1.1 ^%s 0.1 0.1 0.1 0 2 force" % (EMBER_DUST, x, z) for x, z, _, _ in arc]
      + fx.decal("shock_0", 5, EMBER_I, pos="^ ^0.1 ^1.5", kind="shock"))
    w("vfx/firering", ["# 火圈环上一圈火舌（as/at 圆心）"] + ring("minecraft:flame", 3.8, 16, y=0.2)
      + ring("minecraft:small_flame", 3.4, 8, y=0.7, phase=0.5))
    w("vfx/muzzle", ["# 弩口（as/at 他）：闪光与火花"]
      + fx.spark("^ ^1.45 ^1.1", PALE, size=1.4) + [
        "execute if score @s %s matches 1 run particle minecraft:electric_spark ^ ^1.45 ^1.2 0.15 0.15 0.15 0.4 10" % O,
        "execute if score @s %s matches 1 run particle minecraft:firework ^ ^1.45 ^1.2 0.05 0.05 0.05 0.1 6" % O,
        "execute if score @s %s matches 2 run particle minecraft:flame ^ ^1.45 ^1.2 0.1 0.1 0.1 0.15 14" % O,
        "execute if score @s %s matches 2 run particle minecraft:lava ^ ^1.45 ^1.2 0 0 0 0 2" % O,
    ])
    w("vfx/volley_charge", ["# 连弩上弦（as/at 他）：脚下转动的法阵、头顶的星光"]
      + fx.decal("sigil", 3.2, GOLD_I, pos="~ ~0.06 ~", kind="spinf", life=20)
      + fx.decal("ring", 2.2, 0xFFF2C8, pos="~ ~0.08 ~", life=20) + [
        "execute if score @s %s matches 2 as @e[tag=rpg.jqb.fx,distance=..0.5,type=minecraft:item_display] run "
        "data modify entity @s item.components.\"minecraft:custom_model_data\".colors[0] set value %d" % (O, EMBER_I),
    ] + fx.twinkle("^0.5 ^2.1 ^0.6", PALE) + fx.twinkle("^-0.5 ^1.8 ^0.5", PALE, frame=2))
    w("vfx/impact", ["# 落刀冲击（at 落点）"]
      + fx.decal("shock_0", 5, 0xFFF2C8, pos="~ ~0.1 ~", kind="shock") + fx.glyph("burst", 2.4, PALE, pos="~ ~1 ~", kind="burst")
      + wave("minecraft:crit", 16, 0.5, y=0.3) + wave("minecraft:end_rod", 10, 0.2, y=0.4))
    w("vfx/horn", ["# 号角（as/at 他）：脚下红十字圣印，金色光浪与图腾光点"]
      + fx.decal("sigil", 4.5, TEMPLAR_RED, pos="~ ~0.06 ~", kind="spinf", life=24)
      + fx.decal("ring", 2, GOLD_I, pos="~ ~0.1 ~", kind="ringm") + fx.glyph("burst", 3.4, GOLD, pos="~ ~2.6 ~", kind="burst")
      + wave("minecraft:end_rod", 20, 0.35, y=1.6) + [
        "particle minecraft:totem_of_undying ~ ~1.6 ~ 0.4 0.6 0.4 0.5 40 force",
        "particle minecraft:flash{color:%d} ~ ~2.2 ~ 0 0 0 0 1 force" % GOLD_I,
    ])
    w("vfx/harp_sky", ["# 竖琴之弦（as/at 他）：朝天一箭化作金光柱，天上爆开"]
      + light_pillar(0xFFE9A8) + fx.glyph("burst", 6, GOLD, pos="~ ~9 ~", kind="burst") + fx.glyph("burst", 3, PALE, pos="~ ~9 ~", frame=1, kind="burst")
      + fx.decal("hexagram", 5, GOLD_I, pos="~ ~0.06 ~", kind="spinf", life=HARP_STEP * HARP_N + 12)
      + wave("minecraft:firework", 24, 0.4, y=9) + wave("minecraft:end_rod", 16, 0.3) + [
        "particle minecraft:flash{color:%d} ~ ~9 ~ 0 0 0 0 1 force" % 0xFFE9A8,
    ])
    w("vfx/takeoff", ["# 起跳（at 起跳点）：火浪与烟"]
      + fx.decal("shock_0", 5, EMBER_I, pos="~ ~0.1 ~", kind="shock") + wave("minecraft:flame", 20, 0.4)
      + wave("minecraft:large_smoke", 12, 0.25) + ["particle minecraft:flash{color:%d} ~ ~0.6 ~ 0 0 0 0 1 force" % EMBER_I])
    w("vfx/meteor", ["# 他从天上砸下来的前一刻（at 落点）：火柱"]
      + light_pillar(EMBER_I) + fx.ray("~ ~ ~", "#FFD08A") + [
        "particle minecraft:flame ~ ~8 ~ 0.3 6 0.3 0.02 60 force",
        "particle minecraft:lava ~ ~4 ~ 0.4 3 0.4 0 8 force",
    ])
    w("vfx/land", ["# 砸地（at 落点）：火的冲击波、岩浆溅起、裂地"]
      + fx.glyph("burst", 5, EMBER, pos="~ ~1.2 ~", kind="burst") + fx.glyph("burst", 3, "#FFD08A", pos="~ ~1.2 ~", frame=1, kind="burst")
      + fx.decal("ring", 2, 0xFFD08A, pos="~ ~0.16 ~", kind="ringm") + fx.decal("cracks", 7, 0x2A0A04, pos="~ ~0.04 ~", life=80)
      + wave("minecraft:flame", 28, 0.55) + wave("minecraft:large_smoke", 14, 0.3) + fountain("minecraft:lava", 6, 0.6) + [
        "particle minecraft:flash{color:%d} ~ ~1 ~ 0 0 0 0 1 force" % EMBER_I,
    ])
    w("vfx/ult2", ["# 二阶段大招起手（as/at 他）：火光冲天，脚下转动的火印"]
      + light_pillar(EMBER_I) + fx.decal("hexagram", 6, FIRE_D, pos="~ ~0.06 ~", kind="spinf", life=40)
      + fx.decal("sigil", 4, EMBER_I, pos="~ ~0.08 ~", kind="spinr", life=40) + fx.glyph("burst", 5, EMBER, pos="~ ~2.4 ~", kind="burst")
      + wave("minecraft:flame", 24, 0.45) + [
        "particle minecraft:flash{color:%d} ~ ~2 ~ 0 0 0 0 1 force" % EMBER_I,
    ])
    w("vfx/dash_start", ["# 每次翻滚冲锋起步（as/at 他）"]
      + fx.decal("shock_0", 4, EMBER_I, pos="~ ~0.1 ~", kind="shock") + wave("minecraft:flame", 14, 0.35)
      + ["particle minecraft:lava ~ ~0.4 ~ 0.3 0.1 0.3 0 3"])
    w("vfx/fall", ["# 倒下（as/at 他）：火从身上散去"]
      + fx.decal("glow", 4, FIRE_D, pos="~ ~0.04 ~", life=60) + wave("minecraft:flame", 20, 0.2, y=0.6)
      + wave("minecraft:large_smoke", 16, 0.15, y=1) + ["particle minecraft:campfire_cosy_smoke ~ ~1 ~ 0.4 0.4 0.4 0.01 8"])
    w("vfx/david_hero", ["# 大卫的幽灵摆出英雄姿势（as/at 它）：天光落在他身上"]
      + light_pillar(0xD8ECFF) + fx.decal("ring", 2, 0xD8ECFF, pos="~ ~0.1 ~", kind="ringm") + wave("minecraft:end_rod", 20, 0.3, y=1)
      + ["particle minecraft:totem_of_undying ~ ~1.2 ~ 0.4 1 0.4 0.3 30 force"])


def finish():
    fx.build(extra_tick=[
        "execute if entity @s[tag=rpg.jqb.arrow] run return run function %s/fx/arrow" % B,
        "execute if entity @s[tag=rpg.jqb.fire] run function %s/fx/fire" % B,
        "execute if entity @s[tag=rpg.jqb.firering] run function %s/fx/firering" % B,
    ])
    # 琴弦落下的音高随序号升高（C 大调琶音）
    path = os.path.join(OUT, "harp", "fall.mcfunction")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    pitches = [0.5, 0.56, 0.63, 0.67, 0.75, 0.84, 0.94, 1.0, 1.12, 1.26, 1.33, 1.5]
    lines = text.split("\n")
    i = [n for n, s in enumerate(lines) if "note_block.harp" in s][0]
    lines[i:i + 1] = ["execute if score #i %s matches %d run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 %s"
                      % (O, k, p) for k, p in enumerate(pitches)]
    wf(path, lines)


def main():
    build()
    skills()
    ults1()
    morph()
    stage2()
    vfx()
    finish()
    hook_tag(DP, "load", "%s/load" % B, False)
    hook_tag(DP, "tick", "%s/tick" % B, True)
    count = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("jacques_boss: %d functions; two stages of %d HP" % (count, MAX))


if __name__ == "__main__":
    main()
