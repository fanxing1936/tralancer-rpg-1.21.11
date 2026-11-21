# -*- coding: utf-8 -*-
"""疯人王扫罗 Boss（docs/SAUL-DESIGN.md）。只用指令召唤，规格对齐教皇战、篡夺者、雅克。

    python add_saul_boss.py ../rpg

外观在 add_saul_model.py（载体 rpg.slb 换装为 rpg.slm；对着空气练剑时的老战友幻影 rpg.slg 换装为 rpg.slgm），
血条横幅在 add_saul_boss_art.py，特效素材沿用篡夺者的（boss_fx.py）。

两段，每段 1000 血：一阶段「十字军大元帅」，甲碎，二阶段「疯人王」，击败后他笑着跪下。
每段一池血，切段补满；副手放隐形的死亡保护，致命一击被它吃掉后由切段接手（同雅克）。
他是人：载体不带 rpg.demon（七罪契约打不到），也不带 rpg.demon.fly（新约打不到）。整场只有剑，不召唤、不放法术。

招架与坚毅（设计稿第 4 节）：玩家打到他时（player_hurt_entity 进度，as 玩家）当场判定怎么算；
原版在这之后才把这一下记进玩家的伤害统计（minecraft.custom:damage_dealt，十分之一点），所以下一刻
按统计的增量结算（hit/settle）：
  招架中、从正面打    → 整下退回，并立刻反击；
  一阶段、从正面打    → 30% 被坚毅铠甲弹开，整下退回；
  「最后一课」被躲开后 → 他跪地，这一下再多扣一半。
正面 = 攻击者在他身前 2 格那一点的 3.2 格内（约 ±60°）。友军打他不算（只认玩家）。
"""

import json
import math
import os
import sys

import rpg_ui_style as ui
import add_saul_boss_art as bar_art
from boss_fx import Fx, flat_sc, sc
from display_mob import hook_tag, wf, wj

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "saul_boss")
B = "rpg:saul_boss"
LOOK = "rpg:saul"
PHANTOM = "rpg:saul_ghost"
O = "rpg_sl"
UNIT = "type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview"
GHOST = "type=minecraft:vindicator,tag=rpg.slg"
CENTER = "type=minecraft:marker,tag=rpg.slb.center,limit=1"
SURV = "gamemode=!spectator,gamemode=!creative"
BAR = "rpg:saul_boss"

ARENA = 40
BAR_RANGE = 48
EMPTY_LIMIT = 1200
STRIDE = 4
MAX = 1000
ARMOR1, ARMOR2 = 14, 6
SPEED1, SPEED2 = 0.33, 0.38
GUARD_ITEM = 'minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]'
GAP1, GAP2 = 10, 7                  # 千刀「攻速 +30%」：二阶段普攻间隔 10 → 7 刻
BASICS_PER_SKILL = 3
BASIC_RANGE = 25
MELEE_R = 4
FAR = 6                             # 被拉开到这么远就优先突刺

# 配色：一阶段旧元帅的银，二阶段暗红与蛛网灰
SILVER = "#D8DEE6"
SILVER_I = 0xD8DEE6
STEEL_D = "#8C96A2"
BLADE = "#EEF4FA"
BLADE_I = 0xEEF4FA
GOLD = "#E6C060"
BLOOD = "#C9505A"
BLOOD_I = 0xC9505A
BLOOD_D = 0x6A1018
WEB = "#B8B8B0"
WEB_I = 0xB8B8B0
PHANTOM_C = "#E6ECF6"

STAGES = {
    # 段号: (名称, 英文小注, 大招血线, 大招时钟（刻）, 音乐, 音乐长度（刻）, 招式轮换)
    1: ("十字军大元帅", "The Marshal", (750, 500, 250), 900, "rpg:bgm.saul1", 2171, ["lunge", "guard", "flash", "shadow", "echo", "lunge"]),
    2: ("疯人王", "The Mad King", (750, 500, 250), 1100, "rpg:bgm.saul2", 2241, ["lunge3", "thrusts", "web", "step", "guard", "feint"]),
}
# 每段三个大招，按血线或时钟轮流（第 9 节之后用户要求加强：2026-11-16）
ULTS = {1: ["line", "circle", "echoes"], 2: ["cuts", "rain", "last"]}
DANCE_AT = 150                      # 二阶段血量到这里，只放一次的「疯王之舞」
SKILL_ID = {"thrust": 1, "left": 2, "right": 3, "double": 4, "final": 5, "lunge": 6, "guard": 7, "counter": 8,
            "shadow": 9, "line": 10, "circle": 11, "stagger": 12, "lunge3": 13, "web": 14, "feint": 15, "cuts": 16,
            "last": 17, "flash": 18, "echo": 19, "thrusts": 20, "step": 21, "echoes": 22, "rain": 23, "dance": 24}
FLASH_DMG, ECHO_DMG, THRUST_DMG, STEP_DMG, ECHOES_DMG, RAIN_DMG, RAIN_BIG, DANCE_DMG, DANCE_X = 12, 8, 3, 11, 12, 10, 18, 8, 16

# 招式数值（设计稿第 4 节）
STAB_DMG, FINAL_DMG, LUNGE_DMG, COUNTER_DMG, COUNTER3_DMG = 6, 9, 10, 12, 5
LINE_N, LINE_L, LINE_DMG, LINE_FIRST, LINE_STEP, LINE_WARN = 5, 30, 14, 30, 14, 20
CIRCLE_BANDS = ((1.0, 3.5, 30), (5.5, 7.5, 45), (9.5, 11.5, 60))   # (内半径, 外半径, 斩下的刻)
CIRCLE_DMG = 12
WEB_LIFE, WEB_R = 160, 1.4
CUTS_N, CUTS_FROM, CUTS_EVERY, CUTS_WARN, CUTS_DMG, CUTS_BACK, CUTS_FINAL = 24, 14, 3, 12, 8, 88, 16
LAST_AIM, LAST_BACK, LAST_DMG, LAST_STEPS, LAST_KNEEL = 40, 15, 24, 9, 80
STUN = 40
DIZZY = 40


def w(path, lines):
    wf(os.path.join(OUT, *path.split("/")) + ".mcfunction", lines)


fx = Fx(fn=B, tag="rpg.slb.fx", life="rpg_sl_life", kind="rpg_sl_kd", writer=w, kinds={
    "spinf": dict(extra=["tp @s ~ ~ ~ ~7 ~"]),
    "ringm": dict(life=12, steps=[(11, 10, flat_sc(6))]),
    "ringx": dict(life=14, steps=[(13, 12, flat_sc(11))]),
    "pillarfade": dict(life=24, steps=[(23, 3, sc((0.75, 28, 0.75))), (12, 12, sc((0.02, 28, 0.02)))]),
    "pillarcore": dict(life=24, steps=[(23, 3, sc((0.3, 28, 0.3))), (14, 10, sc((0.01, 28, 0.01)))]),
    # 刺出的光：一闪变细（长度在出生时给）
    "stabfade": dict(life=8, steps=[(6, 6, "scale:[0.01f,0.01f,%gf]" % 3.2)]),
    "linefade": dict(life=16, steps=[(10, 10, "scale:[0.02f,0.02f,%gf]" % LINE_L)]),
    "cutfade": dict(life=10, steps=[(7, 7, "scale:[0.02f,0.02f,4f]")]),
    "lastfade": dict(life=20, steps=[(14, 14, "scale:[0.02f,0.02f,20f]")]),
})
NEW = "rpg.slb.fxnew"


def light_pillar(color, tags=()):
    return ([fx.disp("beam", pos="~ ~ ~", scale=(0.2, 28, 0.2), color=color, trans=(0, 14, 0), tags=tags)] + fx.born(kind="pillarfade")
            + [fx.disp("beam", pos="~ ~ ~", scale=(0.1, 28, 0.1), color=0xFFFFFF, trans=(0, 14, 0), tags=tags)] + fx.born(kind="pillarcore")
            + ["particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force"])


def say(text, gloss=None, name=None, stage=1):
    """〖扫罗〗 播报：没有头衔，只叫名字（ART-STYLE.md §12 的格式）。"""
    parts = [ui.comp("〖", STEEL_D, True), ui.comp("扫罗", SILVER if stage == 1 else BLOOD, True), ui.comp("〗", STEEL_D, True)]
    if gloss:
        parts.append(ui.comp(" " + ui.fraktur(gloss), ui.BROADCAST_GLOSS))
    parts.append(ui.comp(ui.GAP, ui.BROADCAST_BODY))
    if name:
        parts.append(ui.comp(name, ui.BROADCAST_NAME))
    parts.append(ui.comp(text, ui.BROADCAST_BODY))
    return "tellraw @a[distance=..%d] %s" % (BAR_RANGE, ui.row(*parts))


def say_s(text, gloss=None, name=None):
    """Stage-aware line (as Saul): the stage-2 colour when he is in stage 2."""
    return ["execute if score @s %s matches 1 run %s" % (O, say(text, gloss, name, 1)),
            "execute if score @s %s matches 2.. run %s" % (O, say(text, gloss, name, 2))]


def bar_title(stage, step=bar_art.STEPS):
    return "bossbar set %s name %s" % (BAR, json.dumps(
        {"text": bar_art.bar_text(stage, step), "font": bar_art.FONT}, ensure_ascii=True, separators=(",", ":")))


def anim(clip):
    return "function %s/anim/enter/%s" % (LOOK, clip)


def start(name, busy):
    return ["scoreboard players set @s rpg_sl_sk %d" % SKILL_ID[name], "scoreboard players set @s rpg_sl_t 0",
            "scoreboard players set @s rpg_sl_busy %d" % busy]


def face(r=BASIC_RANGE):
    return "execute facing entity @p[distance=..%s,%s] feet run tp @s ~ ~ ~ ~ 0" % (r, SURV)


def at(t, cmd):
    return "execute if score @s rpg_sl_t matches %d run %s" % (t, cmd)


def span(t0, t1, cmd):
    return "execute if score @s rpg_sl_t matches %d..%d run %s" % (t0, t1, cmd)


def hurt_tagged(dmg, kind="minecraft:mob_attack"):
    return ["execute as @a[tag=rpg.slb.hit] run damage @s %d %s by @e[%s,limit=1]" % (dmg, kind, UNIT),
            "tag @a[tag=rpg.slb.hit] add rpg.slb.failed",
            "tag @a remove rpg.slb.hit"]


def tag_near(r, pos="~ ~ ~"):
    return "execute positioned %s run tag @a[distance=..%s,%s] add rpg.slb.hit" % (pos, r, SURV)


def line(kind, steps):
    return ["scoreboard players set #d %s %d" % (O, steps), "function %s/line/%s" % (B, kind)]


def every(n, score="@s rpg_sl_t"):
    who, obj = score.split()
    return ["scoreboard players operation #m %s = %s %s" % (O, who, obj),
            "scoreboard players set #k %s %d" % (O, n),
            "scoreboard players operation #m %s %%= #k %s" % (O, O)]


def beam(color, size, trans, tags=(), tp=1):
    return [fx.disp("beam", pos="~ ~ ~", scale=size, color=color, trans=trans, tags=tags, tp=tp),
            "tp @e[tag=%s,limit=1] ~ ~ ~ ~ ~" % NEW]


def ring(p, r, n, y=0.15, phase=0.0):
    out = []
    for i in range(n):
        a = 2 * math.pi * (i + phase) / n
        out.append("particle %s ~%.2f ~%.2f ~%.2f 0 0 0 0 1 force" % (p, r * math.cos(a), y, r * math.sin(a)))
    return out


def wave(p, n, speed, y=0.2, r0=0.4, up=0.0):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        out.append("particle %s ~%.2f ~%.2f ~%.2f %.3f %.3f %.3f %g 0 force" % (p, r0 * c, y, r0 * s, c, up, s, speed))
    return out


def along(p, length, step, y=0.2, spread=0.15, n=1, speed=0.0):
    out = []
    d = step
    while d <= length + 1e-6:
        out.append("particle %s ^ ^%.2f ^%.2f %s %s %s %g %d force" % (p, y, d, spread, spread * 0.5, spread, speed, n))
        d += step
    return out


SILVER_DUST = "minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1}"
BLOOD_DUST = "minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2}"
WEB_DUST = "minecraft:dust{color:[0.78,0.78,0.74],scale:0.8}"


# =====================================================================================
# 框架：召唤、每刻、血量、调度、切段、结算、清场、音乐
# =====================================================================================
def build():
    w("load", [
        "scoreboard objectives add %s dummy" % O,
        "scoreboard objectives add rpg_sl_h dummy",      # 当前血量
        "scoreboard objectives add rpg_sl_c dummy",      # 本段大招时钟
        "scoreboard objectives add rpg_sl_b dummy",      # 普攻计时
        "scoreboard objectives add rpg_sl_n dummy",      # 普攻计数
        "scoreboard objectives add rpg_sl_k dummy",      # 招式轮换序号
        "scoreboard objectives add rpg_sl_cb dummy",     # 普攻连招走到第几下
        "scoreboard objectives add rpg_sl_busy dummy",   # 动作占用（刻）
        "scoreboard objectives add rpg_sl_sk dummy",     # 正在进行的招式
        "scoreboard objectives add rpg_sl_t dummy",      # 招式时间线（刻）
        "scoreboard objectives add rpg_sl_life dummy",   # 特效寿命（刻）
        "scoreboard objectives add rpg_sl_kd dummy",     # 特效种类
        "scoreboard objectives add rpg_sl_i dummy",      # 斩痕 / 直线的序号
        "scoreboard objectives add rpg_sl_s dummy",      # 横幅当前档位
        "scoreboard objectives add rpg_sl_dd minecraft.custom:minecraft.damage_dealt",   # 玩家造成的伤害（十分之一点）
        "scoreboard objectives add rpg_sl_dd0 dummy",    # 上一刻的 rpg_sl_dd
        "scoreboard objectives add rpg_sl_v dummy",      # 这一下怎么算：1 坚毅弹开，2 招架，3 跪地多扣
        "scoreboard objectives add rpg_sl_ur dummy",     # 时钟触发的大招轮到第几个
        "bossbar add %s \"扫罗\"" % BAR,
        "# 粉色档的原版贴图已由教皇战改成全透明：只显示名字里的位图横幅。",
        "bossbar set %s color pink" % BAR,
        "bossbar set %s style notched_20" % BAR,
        "bossbar set %s visible false" % BAR,
    ])

    w("summon", [
        "# 在执行位置开战。同一时间只允许一场。",
        "execute if score #fight %s matches 1 run return run tellraw @s %s" % (
            O, ui.row(ui.comp("〖扫罗〗", SILVER, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                      ui.comp("已经有一场扫罗战；先用 /function %s/clear 清场。" % B, ui.BROADCAST_BODY))),
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.slb.center\"]}",
        "summon minecraft:vindicator ~ ~ ~ {Tags:[\"rpg.slb\",\"rpg.slwear\",\"rpg.slb.new\"],Silent:1b,PersistenceRequired:1b,"
        "CustomName:{\"text\":\"扫罗\",\"color\":\"%s\",\"bold\":true,\"italic\":false},"
        "Health:%df,active_effects:[{id:\"invisibility\",duration:-1,amplifier:0,show_particles:0b}],"
        "attributes:[{id:\"max_health\",base:%df},{id:\"attack_damage\",base:1f},{id:\"armor\",base:%df},"
        "{id:\"follow_range\",base:48f},{id:\"knockback_resistance\",base:0.8f},{id:\"movement_speed\",base:%gf}],"
        "drop_chances:{mainhand:0f,offhand:0f}}" % (SILVER, MAX, MAX, ARMOR1, SPEED1),
        "scoreboard players set @e[%s,tag=rpg.slb.new] %s 1" % (UNIT, O),
        "scoreboard players set @e[%s,tag=rpg.slb.new] rpg_sl_h %d" % (UNIT, MAX),
    ] + ["scoreboard players set @e[%s,tag=rpg.slb.new] %s 0" % (UNIT, s) for s in ("rpg_sl_c", "rpg_sl_n", "rpg_sl_k", "rpg_sl_cb", "rpg_sl_sk")] + [
        "scoreboard players set @e[%s,tag=rpg.slb.new] rpg_sl_b 40" % UNIT,
        "scoreboard players set @e[%s,tag=rpg.slb.new] rpg_sl_busy 44" % UNIT,      # 英雄姿势登场
        "tag @e[%s,tag=rpg.slb.new] remove rpg.slb.new" % UNIT,
        "scoreboard players set #fight %s 1" % O,
        "scoreboard players set #stage %s 1" % O,
        "scoreboard players set #empty %s 0" % O,
        "scoreboard players set #tick %s 0" % O,
        "execute as @a run scoreboard players operation @s rpg_sl_dd0 = @s rpg_sl_dd",
        bar_title(1),
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_sl_s %d" % (UNIT, bar_art.STEPS),
        "bossbar set %s max %d" % (BAR, MAX),
        "bossbar set %s value %d" % (BAR, MAX),
        "bossbar set %s visible true" % BAR,
        "function %s/music/1" % B,
        "function %s/vfx/intro" % B,
        "playsound minecraft:item.trident.return hostile @a[distance=..%d] ~ ~ ~ 2 0.7" % BAR_RANGE,
        say("……斯塔福德？是你吗，老伙计？好，好！拔剑，让我看看你荒废了多少。", gloss="The Marshal"),
    ])

    w("tick", [
        "execute unless score #fight %s matches 1 run return 0" % O,
        "execute as @e[%s] at @s run function %s/arena" % (CENTER, B),
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
        "execute as @e[tag=rpg.slb.fx,distance=..%d] at @s run function %s/fx/tick" % (ARENA * 3, B),
        "# 上一刻被判了格挡 / 多扣的那一下：伤害统计这时才记上，按增量结算；然后所有人的统计基准对齐到这一刻",
        "execute as @a[tag=rpg.slb.pend] run function %s/hit/settle" % B,
        "execute as @a run scoreboard players operation @s rpg_sl_dd0 = @s rpg_sl_dd",
        "function %s/music/tick" % B,
    ])
    w("lost_unit", [
        "# 载体不见了：二阶段里按胜利结算；否则清场。",
        "execute if score #stage %s matches 2.. run return run function %s/victory" % (O, B),
        "function %s/clear" % B,
    ])
    w("unit", [
        "# 载体每刻（as/at 载体）。",
        "execute if entity @s[tag=rpg.slb.end] run return run function %s/finale/tick" % B,
        "execute if entity @s[tag=!rpg.slb.hp] run return run function %s/hp_init" % B,
        "# 保险：离场地中心太远或掉到下面（冲出空岛边缘）就拉回中心；千刀里藏到地下的那段除外",
        "execute unless entity @s[tag=rpg.slb.hidden] at @e[%s] unless entity @s[distance=..36] run function %s/safety/back" % (CENTER, B),
        "execute unless entity @s[tag=rpg.slb.hidden] at @e[%s] positioned ~-48 ~-80 ~-48 if entity @s[dx=96,dy=72,dz=96] run function %s/safety/back" % (CENTER, B),
        "scoreboard players operation #m %s = #tick %s" % (O, O),
        "scoreboard players set #k %s %d" % (O, STRIDE),
        "scoreboard players operation #m %s %%= #k %s" % (O, O),
        "execute if score #m %s matches 0 run function %s/read_hp" % (O, B),
        "execute if score @s %s matches 1 if score @s rpg_sl_h matches ..1 run return run function %s/stage/end1" % (O, B),
        "execute if score @s %s matches 2 if score @s rpg_sl_h matches ..1 run return run function %s/stage/end2" % (O, B),
        "execute if entity @s[tag=rpg.slb.morph] run return run function %s/morph/tick" % B,
        "execute if score @s %s matches 2 run function %s/s2/aura" % (O, B),
        "scoreboard players add @s rpg_sl_c 1",
        "execute if score @s rpg_sl_sk matches 1.. run function %s/sk/tick" % B,
        "execute if score @s rpg_sl_busy matches 1.. run return run scoreboard players remove @s rpg_sl_busy 1",
        "function %s/schedule" % B,
    ])
    w("hp_init", ["tag @s add rpg.slb.hp", "function %s/refill" % B])
    w("safety/back", ["# 拉回场地中心（as 他）", "tp @s @e[%s]" % CENTER,
                      "execute at @s run particle %s ~ ~1 ~ 0.4 0.7 0.4 0 20" % SILVER_DUST,
                      "execute at @s run playsound minecraft:entity.enderman.teleport hostile @a[distance=..32] ~ ~ ~ 1 0.6"])
    w("refill", [
        "# 补满本段血量，并补上副手的死亡保护（上一段的那件可能刚被吃掉）。",
        "attribute @s minecraft:max_health base set %d" % MAX,
        "data merge entity @s {Health:%df}" % MAX,
        "scoreboard players set @s rpg_sl_h %d" % MAX,
        "item replace entity @s weapon.offhand with %s" % GUARD_ITEM,
    ])
    w("read_hp", [
        "execute store result score @s rpg_sl_h run data get entity @s Health 1",
        "execute store result bossbar %s value run scoreboard players get @s rpg_sl_h" % BAR,
        "execute if entity @s[tag=rpg.slb.morph] run return 0",
        "scoreboard players operation #s %s = @s rpg_sl_h" % O,
        "scoreboard players add #s %s 49" % O,
        "scoreboard players set #k %s %d" % (O, MAX // bar_art.STEPS),
        "scoreboard players operation #s %s /= #k %s" % (O, O),
        "execute if score #s %s matches %d.. run scoreboard players set #s %s %d" % (O, bar_art.STEPS + 1, O, bar_art.STEPS),
        "execute if score #s %s matches ..-1 run scoreboard players set #s %s 0" % (O, O),
        "execute unless score #s %s = @s rpg_sl_s run function %s/bar_name" % (O, B),
    ])
    names = ["scoreboard players operation @s rpg_sl_s = #s %s" % O]
    for st in STAGES:
        names += ["execute if score @s %s matches %d if score #s %s matches %d run return run %s" % (O, st, O, k, bar_title(st, k))
                  for k in range(bar_art.STEPS + 1)]
    w("bar_name", names)

    # ---- 调度：普攻（一阶段每 10 刻，二阶段每 7 刻），每三次普攻接一招；大招按血线或时钟插入
    w("schedule", [
        "execute unless entity @a[distance=..%d,%s] run return 0" % (BASIC_RANGE, SURV),
        "scoreboard players remove @s rpg_sl_b 1",
        "execute if score @s rpg_sl_b matches 1.. run return 0",
        "execute if score @s %s matches 1 run scoreboard players set @s rpg_sl_b %d" % (O, GAP1),
        "execute if score @s %s matches 2 run scoreboard players set @s rpg_sl_b %d" % (O, GAP2),
        "execute if score @s rpg_sl_n matches %d.. run return run function %s/pick" % (BASICS_PER_SKILL, B),
        "execute if entity @a[distance=..%s,%s] run return run function %s/basic/melee" % (MELEE_R, SURV, B),
        "# 拉开了：远处不出普攻，走近；太远就直接突刺",
        "execute unless entity @a[distance=..%d,%s] run function %s/pick" % (FAR, SURV, B),
    ])
    pick = ["scoreboard players set @s rpg_sl_n 0", "scoreboard players set #ult %s 0" % O,
            "# 二阶段血量到 %d：只放一次的疯王之舞" % DANCE_AT,
            "execute if score @s %s matches 2 if score @s rpg_sl_h matches ..%d unless entity @s[tag=rpg.slb.danced] run return run function %s/ult/dance"
            % (O, DANCE_AT, B)]
    for s, (_, _, ults, clock, *_r) in STAGES.items():
        for i, ln in enumerate(ults, 1):
            pick.append("execute if score @s %s matches %d if score @s rpg_sl_h matches ..%d unless entity @s[tag=rpg.slb.u%d] "
                        "run scoreboard players set #ult %s %d" % (O, s, ln, i, O, i))
        pick.append("execute if score @s %s matches %d if score #ult %s matches 0 if score @s rpg_sl_c matches %d.. "
                    "run scoreboard players set #ult %s 9" % (O, s, O, clock, O))
    pick.append("execute if score #ult %s matches 1.. run return run function %s/ult/pick" % (O, B))
    pick.append("# 被拉开到 %d 格外：优先突刺" % FAR)
    pick.append("execute if score @s %s matches 1 unless entity @a[distance=..%d,%s] run return run function %s/skill/lunge" % (O, FAR, SURV, B))
    pick.append("execute if score @s %s matches 2 unless entity @a[distance=..%d,%s] run return run function %s/skill/lunge3" % (O, FAR, SURV, B))
    for s, (*_h, rotation) in STAGES.items():
        n = len(rotation)
        pick.append("execute if score @s %s matches %d run scoreboard players operation #r %s = @s rpg_sl_k" % (O, s, O))
        for i, sk in enumerate(rotation):
            pick.append("execute if score @s %s matches %d if score #r %s matches %d run function %s/skill/%s" % (O, s, O, i, B, sk))
        pick.append("execute if score @s %s matches %d run scoreboard players add @s rpg_sl_k 1" % (O, s))
        pick.append("execute if score @s %s matches %d if score @s rpg_sl_k matches %d.. run scoreboard players set @s rpg_sl_k 0" % (O, s, n))
    w("pick", pick)

    upick = [
        "scoreboard players set @s rpg_sl_c 0",
        "# 三招轮流：血线各放一次；时钟到点放下一个（rpg_sl_ur 记着轮到第几个）",
        "execute if score #ult %s matches 9 run scoreboard players add @s rpg_sl_ur 1" % O,
        "execute if score #ult %s matches 9 if score @s rpg_sl_ur matches 4.. run scoreboard players set @s rpg_sl_ur 1" % O,
        "execute if score #ult %s matches 9 run scoreboard players operation #ult %s = @s rpg_sl_ur" % (O, O),
        "scoreboard players operation @s rpg_sl_ur = #ult %s" % O,
    ]
    for k in (1, 2, 3):
        upick.append("execute if score #ult %s matches %d run tag @s add rpg.slb.u%d" % (O, k, k))
    for s, names in ULTS.items():
        for k, n in enumerate(names, 1):
            upick.append("execute if score @s %s matches %d if score #ult %s matches %d run function %s/ult/%s" % (O, s, O, k, B, n))
    w("ult/pick", upick)

    w("sk/tick", ["scoreboard players add @s rpg_sl_t 1"] + [
        "execute if score @s rpg_sl_sk matches %d run return run function %s/sk/%s" % (i, B, n) for n, i in SKILL_ID.items()])
    w("sk/end", [
        "scoreboard players set @s rpg_sl_sk 0",
        "scoreboard players set @s rpg_sl_busy 0",
        "tag @s remove rpg.slb.guard",
        "tag @s remove rpg.slb.weak",
        "tag @s remove rpg.slb.hidden",
        "data merge entity @s {NoAI:0b,NoGravity:0b,Invulnerable:0b}",
        "execute if score @s %s matches 1 run attribute @s minecraft:armor base set %d" % (O, ARMOR1),
        "execute if score @s %s matches 2 run attribute @s minecraft:armor base set %d" % (O, ARMOR2),
        "execute as @e[%s] run function %s/clear_unit" % (GHOST, B),
    ])

    # ---- 线判定：从这里沿当前朝向每 1.5 格查一次
    for kind, r in (("thin", 1.1), ("path", 1.4)):
        w("line/%s" % kind, [
            "tag @a[distance=..%s,%s] add rpg.slb.hit" % (r, SURV),
            "scoreboard players remove #d %s 1" % O,
            "execute if score #d %s matches 1.. positioned ^ ^ ^1.5 run function %s/line/%s" % (O, B, kind),
        ])

    # ---- 招架与坚毅：玩家打到他（as 玩家）
    wj(os.path.join(DP, "data", "rpg", "advancement", "saul_boss", "hit.json"), {
        "criteria": {"hit": {"trigger": "minecraft:player_hurt_entity", "conditions": {"entity": [
            {"condition": "minecraft:entity_properties", "entity": "this",
             "predicate": {"type": "minecraft:vindicator", "nbt": "{Tags:[\"rpg.slb\"]}"}}]}}},
        "rewards": {"function": "%s/hit/player" % B}})
    wj(os.path.join(DP, "data", "rpg", "predicate", "saul_boss", "stalwart.json"),
       {"condition": "minecraft:random_chance", "chance": 0.3})
    w("hit/player", [
        "# 玩家打到了扫罗（as 玩家）。原版在这之后才把这一下记进伤害统计，所以这里只判定怎么算，下一刻再按增量结算。",
        "advancement revoke @s only rpg:saul_boss/hit",
        "scoreboard players set @s rpg_sl_v 0",
        "tag @s add rpg.slb.att",
        "execute as @e[%s,distance=..24,limit=1,sort=nearest] at @s run function %s/hit/unit" % (UNIT, B),
        "tag @s remove rpg.slb.att",
        "execute if score @s rpg_sl_v matches 1.. run tag @s add rpg.slb.pend",
    ])
    w("hit/unit", [
        "# 他被打到（as/at 他；攻击者带 rpg.slb.att）：判定这一下怎么算，记在攻击者的 rpg_sl_v 上。",
        "execute if entity @s[tag=rpg.slb.end] run return 0",
        "execute if entity @s[tag=rpg.slb.morph] run return 0",
        "tag @s remove rpg.slb.front",
        "execute positioned ^ ^ ^2 if entity @a[tag=rpg.slb.att,distance=..3.2] run tag @s add rpg.slb.front",
        "execute if entity @s[tag=rpg.slb.guard,tag=rpg.slb.front] run return run function %s/hit/parry" % B,
        "execute if score @s %s matches 1 if entity @s[tag=rpg.slb.front] if predicate rpg:saul_boss/stalwart run return run function %s/hit/negate" % (O, B),
        "execute if entity @s[tag=rpg.slb.weak] run scoreboard players set @a[tag=rpg.slb.att] rpg_sl_v 3",
    ])
    w("hit/settle", [
        "# 结算上一刻那一下（as 玩家）：增量 = 统计 - 上一刻的基准",
        "tag @s remove rpg.slb.pend",
        "scoreboard players operation #dd %s = @s rpg_sl_dd" % O,
        "scoreboard players operation #dd %s -= @s rpg_sl_dd0" % O,
        "execute if score #dd %s matches ..0 run return 0" % O,
        "execute if score @s rpg_sl_v matches 1..2 as @e[%s,distance=..24,limit=1,sort=nearest] run function %s/hit/refund" % (UNIT, B),
        "execute if score @s rpg_sl_v matches 3 as @e[%s,distance=..24,limit=1,sort=nearest] run function %s/hit/extra" % (UNIT, B),
    ])
    w("hit/refund", [
        "# 把这一下整下退回（as 他）",
        "execute store result score #h %s run data get entity @s Health 10" % O,
        "scoreboard players operation #h %s += #dd %s" % (O, O),
        "execute if score #h %s matches %d.. run scoreboard players set #h %s %d" % (O, MAX * 10, O, MAX * 10),
        "execute store result entity @s Health float 0.1 run scoreboard players get #h %s" % O,
    ])
    w("hit/negate", [
        "# 坚毅铠甲：甲片弹开了这一下（as/at 他；下一刻退回伤害）",
        "scoreboard players set @a[tag=rpg.slb.att] rpg_sl_v 1",
    ] + fx.spark("^ ^1.4 ^0.6", SILVER, size=1.2) + [
        "particle minecraft:crit ^ ^1.3 ^0.7 0.3 0.4 0.3 0.4 12",
        "particle minecraft:electric_spark ^ ^1.3 ^0.7 0.2 0.3 0.2 0.3 6",
        "playsound minecraft:item.shield.block hostile @a[distance=..24] ~ ~ ~ 1 1.3",
        "playsound minecraft:block.anvil.land hostile @a[distance=..24] ~ ~ ~ 0.3 1.8",
    ])
    w("hit/parry", [
        "# 招架中被正面打到：格开，立刻反击（as/at 他；下一刻退回伤害）",
        "scoreboard players set @a[tag=rpg.slb.att] rpg_sl_v 2",
        "tag @s remove rpg.slb.guard",
    ] + fx.glyph("burst", 2.2, BLADE, pos="^ ^1.4 ^0.8", kind="burst") + [
        "particle minecraft:flash{color:%d} ^ ^1.4 ^0.8 0 0 0 0 1 force" % BLADE_I,
        "particle minecraft:crit ^ ^1.3 ^0.8 0.3 0.4 0.3 0.6 20",
        "playsound minecraft:item.shield.block hostile @a[distance=..24] ~ ~ ~ 1.2 1.6",
        "playsound minecraft:block.chain.break hostile @a[distance=..24] ~ ~ ~ 1 1.4",
        "function %s/skill/counter" % B,
    ])
    w("hit/extra", [
        "# 「最后一课」被躲开、他跪地时：这一下再多扣一半（as 他）",
        "execute store result score #h %s run data get entity @s Health 10" % O,
        "scoreboard players operation #dd %s /= #two %s" % (O, O),
        "scoreboard players operation #h %s -= #dd %s" % (O, O),
        "execute if score #h %s matches ..10 run scoreboard players set #h %s 10" % (O, O),
        "execute store result entity @s Health float 0.1 run scoreboard players get #h %s" % O,
        "particle minecraft:damage_indicator ~ ~1.4 ~ 0.3 0.3 0.3 0.2 6",
    ])

    # ---- 阶段切换：甲碎
    w("stage/end1", [
        "# 一阶段打完：甲碎。无敌、站定，约 5 秒后进入二阶段。",
        "function %s/refill" % B,
        "function %s/sk/end" % B,
        "tag @s add rpg.slb.morph",
        "scoreboard players set @s rpg_sl_c 0",
        "kill @e[tag=rpg.slb.fx]",
        "data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}",
        "function %s/armor/broken" % LOOK,
        "# 碎甲也是特效实体：给它寿命，不然特效计时器把没有分数的实体当成已到期",
        "scoreboard players set @e[tag=rpg.slb.shard,distance=..8] rpg_sl_life 20000",
        "scoreboard players set @e[tag=rpg.slb.shard,distance=..8] rpg_sl_kd 0",
        "function %s/vfx/shatter" % B,
        anim("kneel"),
        "bossbar set %s value %d" % (BAR, MAX),
        bar_title(1, 0),
    ])
    shard = ["# 碎甲抛飞（as 碎甲）：按序号往外、往下飞，最后落在地上"]
    # 头盔从约 1.7 格高（玩家身高）往后上方飞出，落到地上（合计下落 1.5）；左臂甲往左飞，下落 1.1
    helmet = [(-0.25, 0.35, -0.5), (-0.25, 0.15, -0.5), (-0.25, -0.05, -0.45), (-0.2, -0.25, -0.4), (-0.2, -0.4, -0.35),
              (-0.15, -0.5, -0.3), (-0.1, -0.5, -0.2), (-0.05, -0.3, -0.1)]
    pauld = [(0.5, 0.25, -0.1), (0.5, 0.1, -0.1), (0.45, -0.1, -0.1), (0.4, -0.25, -0.1), (0.3, -0.35, -0.05),
             (0.2, -0.4, 0.0), (0.1, -0.35, 0.0)]
    for name, path in (("helmet", helmet), ("l_pauldron", pauld)):
        for k, (dx, dy, dz) in enumerate(path):
            shard.append("execute if score #c %s matches %d if entity @s[tag=rpg.slb.shard.%s] rotated as @e[%s,limit=1] "
                         "positioned as @s run tp @s ^%s ^%s ^%s" % (O, 2 + 2 * k, name, UNIT, dx, dy, dz))
    shard.append("execute if score #c %s matches 2..14 at @s run tp @s ~ ~ ~ ~31 ~" % O)
    shard.append("execute if score #c %s matches 16 positioned ~ ~-0.2 ~ run particle minecraft:block{block_state:\"minecraft:iron_block\"} ~ ~ ~ 0.3 0.1 0.3 0 8" % O)
    w("morph/shard", shard)
    w("morph/tick", [
        "scoreboard players add @s rpg_sl_c 1",
        "scoreboard players operation #c %s = @s rpg_sl_c" % O,
        "execute if score @s rpg_sl_c matches 1..16 as @e[tag=rpg.slb.shard,distance=..8] run function %s/morph/shard" % B,
        "execute if score @s rpg_sl_c matches 1..30 run particle %s ~ ~1.6 ~ 0.4 0.5 0.4 0 2" % WEB_DUST,
        at_c(16, "playsound minecraft:block.anvil.land hostile @a[distance=..32] ~ ~ ~ 0.8 0.7"),
        at_c(20, say("……", gloss="The Mad King", stage=2)),
        at_c(40, anim("hero")),
        at_c(40, "function %s/vfx/rise" % B),
        at_c(44, "playsound rpg:saul.laugh hostile @a[distance=..40] ~ ~ ~ 1.4 0.7"),
        at_c(44, say("斯塔福德……你又来了？哈哈哈……那就再来！", gloss="The Mad King", name="第二阶段 · ", stage=2)),
        at_c(86, "function %s/stage/begin2" % B),
    ])
    w("stage/begin2", [
        "tag @s remove rpg.slb.morph",
        "tag @s remove rpg.slb.u1",
        "tag @s remove rpg.slb.u2",
        "tag @s remove rpg.slb.u3",
        "scoreboard players set @s rpg_sl_ur 0",
        "data merge entity @s {NoAI:0b,Invulnerable:0b}",
        "attribute @s minecraft:armor base set %d" % ARMOR2,
        "attribute @s minecraft:movement_speed base set %g" % SPEED2,
        "scoreboard players set @s %s 2" % O,
        "scoreboard players set #stage %s 2" % O,
    ] + ["scoreboard players set @s %s 0" % s for s in ("rpg_sl_c", "rpg_sl_n", "rpg_sl_k", "rpg_sl_cb", "rpg_sl_sk")] + [
        "scoreboard players set @s rpg_sl_b 14",
        bar_title(2),
        "scoreboard players set @s rpg_sl_s %d" % bar_art.STEPS,
        "function %s/music/2" % B,
    ])
    w("s2/aura", ["# 二阶段常驻（as/at 他）：身上挂着的蛛丝，红眼一点暗红"] + every(6, "#tick %s" % O) + [
        "execute if score #m %s matches 0 run particle %s ~ ~1.2 ~ 0.35 0.7 0.35 0 1" % (O, WEB_DUST),
        "execute if score #m %s matches 3 run particle %s ^ ^1.72 ^0.2 0.08 0.04 0.08 0 1" % (O, BLOOD_DUST),
    ])

    w("stage/end2", [
        "# 二阶段打完：剑从手里滑落，他笑着跪下；约 7 秒后胜利。",
        "function %s/refill" % B,
        "function %s/sk/end" % B,
        "tag @s add rpg.slb.end",
        "scoreboard players set @s rpg_sl_c 0",
        "data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}",
        "kill @e[tag=rpg.slb.fx]",
        anim("kneel"),
        "playsound minecraft:entity.player.death hostile @a[distance=..%d] ~ ~ ~ 1 0.6" % BAR_RANGE,
        "bossbar set %s value 0" % BAR,
        bar_title(2, 0),
    ])
    w("finale/tick", [
        "# 死亡（as/at 他）：剑落、跪下、倒地、躺下，在天光里沉入地面、散成白灰，然后结算",
        "scoreboard players add @s rpg_sl_c 1",
        at_c(10, "function %s/finale/drop" % B),
        at_c(20, say("……好剑。", stage=2)),
        at_c(44, anim("fall")),
        at_c(44, "playsound minecraft:entity.player.big_fall hostile @a[distance=..32] ~ ~ ~ 1 0.8"),
        at_c(68, anim("down")),
        at_c(70, say("斯塔福德，你终于……赢了我一次。", stage=2)),
        "execute if score @s rpg_sl_c matches 1..160 run particle %s ~ ~1 ~ 0.6 0.6 0.6 0 1" % WEB_DUST,
        at_c(90, "function %s/vfx/fall" % B),
        at_c(110, "function %s/vfx/death" % B),
        at_c(110, say("……老伙计，等等我。", stage=2)),
        "execute if score @s rpg_sl_c matches 112..150 run tp @s ~ ~-0.04 ~",
        "execute if score @s rpg_sl_c matches 112..150 run particle minecraft:white_ash ~ ~0.8 ~ 0.6 0.4 0.6 0.02 8",
        "execute if score @s rpg_sl_c matches 112..150 run particle %s ~ ~0.6 ~ 0.5 0.3 0.5 0 2" % SILVER_DUST,
        "execute if score @s rpg_sl_c matches 112..150 run particle minecraft:soul ~ ~0.6 ~ 0.4 0.2 0.4 0.02 1",
        at_c(150, "particle minecraft:flash{color:%d} ~ ~0.5 ~ 0 0 0 0 1 force" % SILVER_I),
        at_c(150, "playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..40] ~ ~ ~ 1.2 0.6"),
        "execute if score @s rpg_sl_c matches 156.. run function %s/victory" % B,
    ])
    w("finale/drop", [
        "# 千刀从手里滑落，插在他身前（as/at 他）",
        'execute on passengers if entity @s[tag=rpg.slm.p.rapier] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"',
        'execute positioned ^ ^ ^1.1 run summon minecraft:item_display ~ ~0.7 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:saul/rapier"}},item_display:"none",'
        'brightness:{sky:15,block:12},view_range:1.5f}',
        "execute as @e[tag=%s] at @s run function %s/finale/blade" % (NEW, B),
    ] + fx.born(400) + [
        "playsound minecraft:block.chain.place hostile @a[distance=..24] ~ ~ ~ 1 1.4",
        "particle minecraft:crit ^ ^0.3 ^1.1 0.2 0.1 0.2 0.2 10",
    ])
    w("finale/blade", [
        "# 剑尖朝下插进地里：千刀的物品模型本来是剑尖朝上的单件，这里绕 X 转半圈",
        "data merge entity @s {transformation:{left_rotation:[1f,0f,0f,0f],translation:[0f,0f,0f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}",
    ])

    quote = ui.row(ui.comp("〖撒母耳记下 1:27〗", ui.BROADCAST_HOLY, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                   ui.comp("英雄何竟仆倒！战具何竟灭没！", ui.BROADCAST_NAME))
    w("victory", [
        "execute at @e[%s] run particle minecraft:flash{color:%d} ~ ~2 ~ 0 0 0 0 1 force" % (CENTER, SILVER_I),
        "execute at @e[%s] run particle minecraft:end_rod ~ ~4 ~ 3 3 3 0.02 60 force" % CENTER,
        "execute at @e[%s] run playsound minecraft:block.bell.resonate hostile @a[distance=..%d] ~ ~ ~ 1 0.6" % (CENTER, BAR_RANGE),
        "execute at @e[%s] run tellraw @a[distance=..%d] %s" % (CENTER, BAR_RANGE, quote),
        "function %s/clear" % B,
    ])
    w("lose", [
        "execute at @e[%s] run %s" % (CENTER, say("……又跑了。斯塔福德，你从来都跑得比我快。").replace(
            "tellraw @a[distance=..%d]" % BAR_RANGE, "tellraw @a[distance=..%d]" % (BAR_RANGE * 2))),
        "function %s/clear" % B,
    ])
    w("clear", [
        "# 清除扫罗战的全部实体：载体与部件、幻影、碎甲、蛛网与特效；血条与音乐一起收掉。",
        "tag @a remove rpg.slb.hit",
        "tag @a remove rpg.slb.failed",
        "tag @a remove rpg.slb.att",
        "execute as @e[%s] run function %s/clear_unit" % (UNIT, B),
        "execute as @e[%s] run function %s/clear_unit" % (GHOST, B),
        "kill @e[type=minecraft:marker,tag=rpg.slb.center]",
        "kill @e[tag=rpg.slb.fx]",
        "bossbar set %s visible false" % BAR,
        "bossbar set %s players" % BAR,
    ] + ["stopsound @a record %s" % m for m in sorted({v[4] for v in STAGES.values()})] + [
        "scoreboard players set #fight %s 0" % O,
        "scoreboard players set #stage %s 0" % O,
    ])
    w("clear_unit", ["execute on passengers run kill @s", "tp @s ~ -256 ~", "kill @s"])

    music = ["scoreboard players remove #bgm %s 1" % O]
    for s, v in STAGES.items():
        music.append("execute if score #bgm %s matches ..0 if score #stage %s matches %d run function %s/music/%d" % (O, O, s, B, s))
        w("music/%d" % s, ["stopsound @a[distance=..%d] record %s" % (BAR_RANGE, m)
                           for m in sorted({x[4] for x in STAGES.values()})] + [
            "stopsound @a[distance=..%d] music" % BAR_RANGE,
            "execute as @a[distance=..%d] at @s run playsound %s record @s ~ ~ ~ 1 1" % (BAR_RANGE, v[4]),
            "scoreboard players set #bgm %s %d" % (O, v[5]),
        ])
    w("music/tick", music)

    w("debug/stage2", [
        "# 召唤后直接打到一阶段底线，走正常的甲碎进入二阶段。",
        "function %s/summon" % B,
        "tag @e[%s,limit=1,sort=nearest] add rpg.slb.hp" % UNIT,
        "execute as @e[%s,limit=1,sort=nearest] run function %s/refill" % (UNIT, B),
        "execute as @e[%s,limit=1,sort=nearest] run data merge entity @s {Health:1f}" % UNIT,
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_sl_h 1" % UNIT,
    ])
    w("debug/ult", [
        "# 调试：下一次选招就放大招（按本段的轮换）。",
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_sl_c 99999" % UNIT,
        "scoreboard players set @e[%s,limit=1,sort=nearest] rpg_sl_n %d" % (UNIT, BASICS_PER_SKILL),
    ])
    for sk in ("lunge", "guard", "shadow", "flash", "echo", "lunge3", "thrusts", "web", "step", "feint", "melee"):
        where = "basic" if sk == "melee" else "skill"
        w("debug/skill/%s" % sk, ["# 调试：最近的扫罗立刻出这一招。",
                                  "execute as @e[%s,limit=1,sort=nearest] at @s run function %s/%s/%s" % (UNIT, B, where, sk)])
    for u in ("line", "circle", "echoes", "cuts", "rain", "last", "dance"):
        w("debug/ult/%s" % u, ["# 调试：最近的扫罗立刻放这个大招。",
                               "execute as @e[%s,limit=1,sort=nearest] at @s run function %s/ult/%s" % (UNIT, B, u)])


def at_c(t, cmd):
    return "execute if score @s rpg_sl_c matches %d run %s" % (t, cmd)


# =====================================================================================
# 招式
# =====================================================================================
def stab_fx(pos="^ ^1.35 ^0.9", length=3.2, color=BLADE_I):
    """A thrust of light straight ahead: a thin beam that snaps out and thins away."""
    return (["execute positioned %s run %s" % (pos, fx.disp("beam", pos="~ ~ ~", scale=(0.12, 0.12, length), color=color,
                                                             trans=(0, 0, length / 2.0)))]
            + ["execute positioned %s run tp @e[tag=%s,limit=1] ~ ~ ~ ~ ~" % (pos, NEW)] + fx.born(kind="stabfade")
            + ["particle minecraft:crit %s 0.15 0.15 0.15 0.3 4" % pos.replace("^0.9", "^%.1f" % (length + 0.6))])


def skills():
    # ---- 普攻：细剑连招（原作细剑 RapierCombo 的几段）。一阶段刺、刺、前冲收剑；二阶段左右与双刺随机
    w("basic/melee", [
        "scoreboard players add @s rpg_sl_n 1",
        face(MELEE_R + 1),
        "execute if score @s %s matches 2 run return run function %s/basic/mad" % (O, B),
        "execute if score @s rpg_sl_cb matches 0 run function %s/skill/thrust" % B,
        "execute if score @s rpg_sl_cb matches 1 run function %s/skill/right" % B,
        "execute if score @s rpg_sl_cb matches 2 run function %s/skill/final" % B,
        "scoreboard players add @s rpg_sl_cb 1",
        "execute if score @s rpg_sl_cb matches 3.. run scoreboard players set @s rpg_sl_cb 0",
    ])
    w("basic/mad", [
        "# 二阶段：顺序随机",
        "execute store result score #r %s run random value 0..2" % O,
        "execute if score #r %s matches 0 run function %s/skill/left" % (O, B),
        "execute if score #r %s matches 1 run function %s/skill/right" % (O, B),
        "execute if score #r %s matches 2 run function %s/skill/double" % (O, B),
    ])
    for name, hits, busy in (("thrust", (4,), 9), ("left", (3,), 7), ("right", (3,), 8), ("double", (3, 6), 9)):
        w("skill/%s" % name, start(name, busy) + ["data merge entity @s {NoAI:1b}", anim(name)])
        w("sk/%s" % name, [at(t, "function %s/strike/stab" % B) for t in hits] + [
            "execute if score @s rpg_sl_t matches %d.. run function %s/sk/end" % (busy - 1, B)])
    w("strike/stab", ["# 一刺（as/at 他）：身前 3 格", tag_near(1.5, "^ ^ ^2.2")] + hurt_tagged(STAB_DMG)
      + stab_fx() + ["particle %s ^ ^1.3 ^2 0.2 0.1 0.2 0 3" % SILVER_DUST])
    w("skill/final", start("final", 24) + ["data merge entity @s {NoAI:1b}", anim("final")])
    w("sk/final", [
        span(3, 9, "execute unless entity @a[distance=..1.4,%s] if block ^ ^0.5 ^0.8 #minecraft:replaceable "
                   "if block ^ ^1.5 ^0.8 #minecraft:replaceable unless block ^ ^-0.5 ^0.8 #minecraft:replaceable run tp @s ^ ^ ^0.35" % SURV),
        at(10, "function %s/strike/final" % B),
        "execute if score @s rpg_sl_t matches 22.. run function %s/sk/end" % B,
    ])
    w("strike/final", ["# 前冲收剑（as/at 他）：身前 3.5 格", tag_near(1.8, "^ ^ ^2.3")] + hurt_tagged(FINAL_DMG)
      + stab_fx(length=4.0) + fx.slash("^ ^1.3 ^1.8", BLADE, size=2.6) + [
        "particle minecraft:sweep_attack ^ ^1.2 ^2 0.4 0.1 0.4 0 2",
        "particle %s ^ ^1.3 ^2.4 0.4 0.2 0.4 0 6" % SILVER_DUST,
    ])

    # ---- 突刺：地上先亮一条 10 格细线，0.8 秒后沿线冲出去
    w("skill/lunge", start("lunge", 34) + [
        "data merge entity @s {NoAI:1b}", face(),
    ] + ["execute positioned ~ ~0.05 ~ run %s" % s for s in beam(0x8C96A2, (0.6, 0.02, 10), (0, 0, 5), tags=("rpg.slb.lungewarn",))]
      + fx.born(18) + [
        "particle %s ^ ^1.4 ^0.8 0.1 0.1 0.1 0 6" % SILVER_DUST,
        "playsound minecraft:item.trident.riptide_1 hostile @a[distance=..24] ~ ~ ~ 0.8 1.4",
    ])
    w("sk/lunge", lunge_body(16, LUNGE_DMG) + ["execute if score @s rpg_sl_t matches 33.. run function %s/sk/end" % B])
    w("strike/lunge", ["# 突刺刺中（as/at 他）"] + hurt_tagged(LUNGE_DMG) + stab_fx(length=3.6) + [
        "particle minecraft:crit ^ ^1.2 ^1.5 0.4 0.3 0.4 0.4 16",
    ])

    # ---- 招架：举剑横在身前 1.5 秒；正面打他会被格开并立刻反击（hit/parry）
    w("skill/guard", start("guard", 32) + [
        "data merge entity @s {NoAI:1b}", face(), anim("showoff"), "tag @s add rpg.slb.guard",
        "playsound minecraft:item.armor.equip_chain hostile @a[distance=..24] ~ ~ ~ 1.2 0.8",
    ] + say_s("来，打过来。", name="招架 · "))
    w("sk/guard", every(4) + [
        "execute if score #m %s matches 0 run particle minecraft:end_rod ^0.3 ^1.5 ^0.6 0.05 0.25 0.05 0 2" % O,
        "execute if score #m %s matches 2 run particle %s ^ ^1.5 ^0.7 0.2 0.3 0.1 0 2" % (O, SILVER_DUST),
        at(2, "function %s/vfx/guard" % B),
        "execute if score @s rpg_sl_t matches 30.. run function %s/sk/end" % B,
    ])
    w("skill/counter", start("counter", 18) + ["data merge entity @s {NoAI:1b}", face(6), anim("double")] + say_s("太慢了！", name="反击 · "))
    w("sk/counter", [
        at(3, "function %s/strike/counter" % B),
        at(6, "function %s/strike/counter" % B),
        "execute if score @s %s matches 2 run %s" % (O, at(9, anim("thrust"))),
        "execute if score @s %s matches 2 run %s" % (O, at(12, "function %s/strike/counter" % B)),
        "execute if score @s rpg_sl_t matches 17.. run function %s/sk/end" % B,
    ])
    w("strike/counter", [tag_near(1.8, "^ ^ ^2.2")]
      + ["execute if score @s %s matches 1 as @a[tag=rpg.slb.hit] run damage @s %d minecraft:mob_attack by @e[%s,limit=1]" % (O, COUNTER_DMG // 2, UNIT),
         "execute if score @s %s matches 2 as @a[tag=rpg.slb.hit] run damage @s %d minecraft:mob_attack by @e[%s,limit=1]" % (O, COUNTER3_DMG, UNIT),
         "tag @a[tag=rpg.slb.hit] add rpg.slb.failed", "tag @a remove rpg.slb.hit"]
      + stab_fx(color=0xFFFFFF) + ["particle minecraft:crit ^ ^1.3 ^2 0.3 0.3 0.3 0.5 10"])

    # ---- 对着空气练剑：疯病发作，转向空处跟看不见的老战友过招 2.5 秒；不出手、护甲减半（破绽）
    w("skill/shadow", start("shadow", 60) + [
        "data merge entity @s {NoAI:1b}",
        "tp @s ~ ~ ~ ~110 0",
        anim("shadow"),
        "attribute @s minecraft:armor base set %d" % (ARMOR1 // 2),
        "execute at @s positioned ^ ^ ^2.6 rotated ~180 0 run function %s/shadow/phantom" % B,
    ] + say_s("老伙计，再来一次！……对，就是这样……", name="对着空气练剑 · "))
    w("shadow/phantom", [
        "# 老战友的幻影（at 他身前 2.6 格，朝他）：只是演出，不参与判定",
        'summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.slg","rpg.slb.ghostnew"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,'
        'CustomName:{"text":"老战友","color":"%s","italic":true},active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}],'
        'attributes:[{id:"scale",base:1.1f}]}' % PHANTOM_C,
        "execute as @e[type=minecraft:vindicator,tag=rpg.slb.ghostnew] run tp @s ~ ~ ~ ~ 0",
        "tag @e[type=minecraft:vindicator,tag=rpg.slb.ghostnew] remove rpg.slb.ghostnew",
        "particle minecraft:end_rod ~ ~1 ~ 0.3 0.8 0.3 0.02 12",
    ])
    w("sk/shadow", [
        at(2, "execute as @e[%s,distance=..4] run function %s/anim/enter/shadow" % (GHOST, PHANTOM)),
        "execute if score @s rpg_sl_t matches 2..60 as @e[%s,distance=..4] at @s run particle %s ~ ~1.2 ~ 0.3 0.6 0.3 0 1" % (GHOST, SILVER_DUST),
        at(14, "playsound minecraft:item.shield.block hostile @a[distance=..20] ~ ~ ~ 0.5 1.6"),
        at(34, "playsound minecraft:item.shield.block hostile @a[distance=..20] ~ ~ ~ 0.5 1.4"),
        "execute if score @s rpg_sl_t matches 59.. run function %s/sk/end" % B,
    ])

    # ---- 眩晕 / 破绽：护甲归零，原作眩晕动作
    w("skill/stagger", start("stagger", STUN + 2) + [
        "data merge entity @s {NoAI:1b,Invulnerable:0b,NoGravity:0b}",
        "attribute @s minecraft:armor base set 0", anim("stun")])
    w("sk/stagger", every(8) + [
        "execute if score #m %s matches 0 run function %s/stagger_star" % (O, B),
        "execute if score @s rpg_sl_t matches %d.. run function %s/stagger/end" % (STUN, B),
    ])
    w("stagger_star", fx.twinkle("~0.3 ~2.25 ~", SILVER, frame=2) + fx.twinkle("~-0.3 ~2.1 ~0.2", SILVER, frame=0))
    w("stagger/end", ["function %s/sk/end" % B, anim("idle")])

    # ---- 二阶段：三连突刺、蛛网、错招
    w("skill/lunge3", start("lunge3", 3 * 20 + 6) + ["data merge entity @s {NoAI:1b}"]
      + say_s("一、二、三！", name="三连突刺 · "))
    l3 = []
    for k in range(3):
        t0 = 20 * k
        l3 += [at(t0 + 1, face()),
               at(t0 + 1, "execute positioned ~ ~0.05 ~ run function %s/lunge/warn" % B)]
        l3 += ["execute if score @s rpg_sl_t matches %d..%d run function %s/lunge/step" % (t0 + 8, t0 + 15, B),
               at(t0 + 8, anim("roll_f")),
               at(t0 + 15, anim("thrust")),
               at(t0 + 16, "function %s/strike/lunge" % B)]
    w("sk/lunge3", l3 + ["execute if score @s rpg_sl_t matches %d.. run function %s/sk/end" % (3 * 20 + 4, B)])
    w("lunge/warn", beam(BLOOD_D, (0.5, 0.02, 9), (0, 0, 4.5)) + fx.born(10))
    w("lunge/step", [
        "# 冲刺一格（as/at 他）：沿途碰到的人记下",
        "execute if block ^ ^0.5 ^1.2 #minecraft:replaceable if block ^ ^1.5 ^1.2 #minecraft:replaceable unless block ^ ^-0.5 ^1.2 #minecraft:replaceable run tp @s ^ ^ ^1.2",
        "tag @a[distance=..1.4,%s] add rpg.slb.hit" % SURV,
        "particle %s ~ ~1 ~ 0.25 0.5 0.25 0 3" % SILVER_DUST,
        "particle minecraft:cloud ~ ~0.1 ~ 0.2 0 0.2 0.01 1",
    ])

    w("skill/web", start("web", 20) + ["data merge entity @s {NoAI:1b}", face(), anim("web")]
      + say_s("别动……网会抓住你的。", name="蛛网 · "))
    w("sk/web", [
        at(7, "execute at @p[distance=..%d,%s] run function %s/web/place" % (BASIC_RANGE, SURV, B)),
        at(7, "playsound minecraft:entity.spider.ambient hostile @a[distance=..24] ~ ~ ~ 1 0.6"),
        "execute if score @s rpg_sl_t matches 19.. run function %s/sk/end" % B,
    ])
    w("web/place", [
        "# 三张蛛网（at 玩家）：脚下、和他的走位方向",
        "function %s/web/one" % B,
        "execute rotated as @p positioned ^ ^ ^3 run function %s/web/one" % B,
        "execute rotated as @p positioned ^2.5 ^ ^1.5 run function %s/web/one" % B,
    ])
    w("web/one", [
        "# 一张蛛网（at 落点）：贴地的原版蛛网，不改方块",
        fx.marker("~ ~ ~", "rpg.slb.web"),
    ] + fx.born(WEB_LIFE) + [
        'summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:cobweb",count:1},'
        'brightness:{sky:15,block:12},view_range:2f,transformation:{translation:[0f,0f,0f],'
        'left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[2.8f,2.8f,2.8f],right_rotation:[0f,0f,0f,1f]}}',
    ] + fx.born(WEB_LIFE) + [
        "particle %s ~ ~0.3 ~ 0.8 0.1 0.8 0 16" % WEB_DUST,
        "particle minecraft:item{item:\"minecraft:cobweb\"} ~ ~0.4 ~ 0.5 0.2 0.5 0.05 8",
    ])
    w("fx/web", ["# 地上的蛛网（as/at 标记）：踩上去缓慢"] + every(10, "@s rpg_sl_life") + [
        "execute if score #m %s matches 0 as @a[distance=..%s,%s] run effect give @s minecraft:slowness 3 2" % (O, WEB_R, SURV),
        "execute if score #m %s matches 5 run particle %s ~ ~0.2 ~ 0.6 0.05 0.6 0 2" % (O, WEB_DUST),
    ])

    w("skill/feint", start("feint", 46) + [
        "data merge entity @s {NoAI:1b}",
        "execute store result score #r %s run random value 0..1" % O,
        "execute if score #r %s matches 0 run tp @s ~ ~ ~ ~75 0" % O,
        "execute if score #r %s matches 1 run tp @s ~ ~ ~ ~-75 0" % O,
        anim("final"),
    ] + say_s("在那儿！……咦？", name="错招 · "))
    w("sk/feint", [
        "execute if score @s rpg_sl_t matches 2..10 run function %s/lunge/step" % B,
        "tag @a remove rpg.slb.hit",
        at(11, "function %s/strike/feint" % B),
        at(14, "attribute @s minecraft:armor base set 0"),
        at(14, anim("stun")),
        "execute if score @s rpg_sl_t matches 14..44 run particle minecraft:end_rod ~ ~2.15 ~ 0.2 0.05 0.2 0.01 1",
        "execute if score @s rpg_sl_t matches 44.. run function %s/stagger/end" % B,
    ])
    w("strike/feint", ["# 刺空（as/at 他）：一刺扎进空处，踉跄"] + stab_fx(length=3.6, color=BLOOD_I) + [
        "particle minecraft:crit ^ ^1.2 ^2.6 0.3 0.3 0.3 0.2 6",
        "playsound minecraft:entity.player.attack.nodamage hostile @a[distance=..24] ~ ~ ~ 1 0.7",
    ])


def lunge_body(t_dash, dmg):
    """The lunge timeline: a warning line (born at t 0), roll at t_dash, 10 steps, the stab."""
    return [
        "execute if score @s rpg_sl_t matches 1..%d run %s" % (t_dash - 2, face()),
        "execute if score @s rpg_sl_t matches 1..%d as @e[tag=rpg.slb.lungewarn,distance=..2] positioned as @s rotated as @e[%s,limit=1] run tp @s ~ ~ ~ ~ ~"
        % (t_dash - 2, UNIT),
        at(t_dash, anim("roll_f")),
        at(t_dash, "playsound rpg:saul.roll hostile @a[distance=..24] ~ ~ ~ 1 1"),
        "execute if score @s rpg_sl_t matches %d..%d run function %s/lunge/step" % (t_dash, t_dash + 8, B),
        at(t_dash + 9, anim("thrust")),
        at(t_dash + 10, "function %s/strike/lunge" % B),
    ]


# =====================================================================================
# 一阶段大招：第一课·直线、第二课·圆
# =====================================================================================
def ults1():
    # 第一课·直线：回到中心，依次朝五个方向刺出 30 格的直线；站进刚刺过的那条线上
    total = LINE_FIRST + LINE_STEP * (LINE_N - 1) + 14
    w("ult/line", start("line", total + 42) + [
        "data merge entity @s {NoAI:1b}",
        "tp @s @e[%s]" % CENTER,
        "execute at @s run function %s/line/begin" % B,
    ])
    w("line/begin", [
        "# 站回中心之后（as/at 他）",
        face(ARENA), anim("mighty"),
        "tag @a remove rpg.slb.failed",
        "playsound minecraft:block.bell.use hostile @a[distance=..40] ~ ~ ~ 1.2 0.8",
        say("看好了，斯塔福德。剑走直线。", gloss="The Marshal", name="第一课 · 直线 · "),
    ] + fx.decal("sigil", 4, SILVER_I, pos="~ ~0.06 ~", kind="spin", life=total))
    lines = []
    for k in range(LINE_N):
        yaw = 72 * k
        t_warn = LINE_FIRST + LINE_STEP * k - LINE_WARN
        t_hit = LINE_FIRST + LINE_STEP * k
        lines += [at(t_warn, "execute rotated ~%d 0 positioned ~ ~0.05 ~ run function %s/line/warn" % (yaw, B)),
                  at(t_hit, "execute rotated ~%d 0 run function %s/line/strike" % (yaw, B)),
                  at(t_hit, anim("thrust"))]
    lines += [at(total, "function %s/lesson/end" % B),
              "execute if score @s rpg_sl_t matches %d.. run function %s/sk/end" % (total + 40, B)]
    w("sk/line", lines)
    w("line/warn", beam(0x8C96A2, (1.6, 0.02, LINE_L), (0, 0, LINE_L / 2.0)) + fx.born(LINE_WARN)
      + beam(0x5A626C, (0.3, 0.03, LINE_L), (0, 0.01, LINE_L / 2.0)) + fx.born(LINE_WARN)
      + ["playsound minecraft:block.note_block.chime hostile @a[distance=..40] ~ ~ ~ 0.8 0.7"])
    w("line/strike", ["# 刺出一道直线（as/at 他，朝这个方向）：沿线判定 14"]
      + ["execute positioned ~ ~0.6 ~ run function %s/line/hits" % B]
      + hurt_tagged(LINE_DMG, "minecraft:mob_attack")
      + ["execute positioned ~ ~0.06 ~ run %s" % s for s in beam(BLADE_I, (1.4, 0.03, LINE_L), (0, 0, LINE_L / 2.0))] + fx.born(kind="linefade")
      + ["execute positioned ~ ~1.3 ~ run %s" % s for s in beam(0xFFFFFF, (0.18, 0.18, LINE_L), (0, 0, LINE_L / 2.0))] + fx.born(kind="linefade")
      + along("minecraft:crit", LINE_L, 2.0, y=0.6, spread=0.3, n=2, speed=0.2) + along(SILVER_DUST, LINE_L, 3.0, y=1.2, spread=0.2)
      + ["playsound minecraft:item.trident.throw hostile @a[distance=..40] ~ ~ ~ 1.3 1.2",
         "playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1 1.5"])
    w("line/hits", line("thin", int(LINE_L / 1.5) + 1))
    w("lesson/end", [
        "# 一课结束：躲对了他叫好（as 他）",
        "execute unless entity @a[tag=rpg.slb.failed] run function %s/lesson/good" % B,
        "execute if entity @a[tag=rpg.slb.failed] run function %s/lesson/again" % B,
        "tag @a remove rpg.slb.failed",
        anim("idle"),
    ])
    w("lesson/good", say_s("好！就是这样，斯塔福德。你还记得。"))
    w("lesson/again", say_s("……不对。再看一遍，老伙计。"))

    # 第二课·圆：原地旋身，从内到外依次扫出三圈剑环，圈与圈之间留空隙
    last_t = CIRCLE_BANDS[-1][2]
    w("ult/circle", start("circle", last_t + 12 + DIZZY) + [
        "data merge entity @s {NoAI:1b}", anim("twirl"),
        "tag @a remove rpg.slb.failed",
        say("剑也走圆。站对地方。", gloss="The Marshal", name="第二课 · 圆 · "),
    ] + ["execute positioned ~ ~0.05 ~ run function %s/circle/warn%d" % (B, i) for i in range(len(CIRCLE_BANDS))])
    circ = []
    for i, (r0, r1, t) in enumerate(CIRCLE_BANDS):
        circ += [at(t, "function %s/circle/band%d" % (B, i))]
        w("circle/warn%d" % i, fx.decal("ring", r1 * 2 + 0.6, 0x8C96A2, pos="~ ~0.05 ~", life=t) +
          fx.decal("ring", r0 * 2 + 0.4, 0x5A626C, pos="~ ~0.06 ~", life=t))
        w("circle/band%d" % i, [
            "# 第 %d 圈剑环（as/at 他）：%.1f～%.1f 格" % (i + 1, r0, r1),
            "tag @a[distance=%s..%s,%s] add rpg.slb.hit" % (r0, r1, SURV),
        ] + hurt_tagged(CIRCLE_DMG) + fx.decal("ring", r1 * 2, BLADE_I, pos="~ ~0.08 ~", kind="ringm")
          + fx.decal("shock_0", r1 * 2, SILVER_I, pos="~ ~0.1 ~", kind="shock")
          + ring("minecraft:sweep_attack", (r0 + r1) / 2.0, 10, y=1.0) + ring(SILVER_DUST, r1, 24, y=0.4)
          + ring("minecraft:crit", (r0 + r1) / 2.0, 16, y=0.8)
          + ["playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.2 %.2f" % (1.4 - 0.2 * i)])
    circ += [at(last_t + 8, "function %s/lesson/end" % B),
             at(last_t + 12, "attribute @s minecraft:armor base set 0"),
             at(last_t + 12, anim("stun")),
             "execute if score @s rpg_sl_t matches %d..%d run particle minecraft:end_rod ~ ~2.2 ~ 0.25 0.05 0.25 0.01 1" % (last_t + 12, last_t + 12 + DIZZY),
             "execute if score @s rpg_sl_t matches %d.. run function %s/stagger/end" % (last_t + 12 + DIZZY, B)]
    w("sk/circle", circ)


# =====================================================================================
# 二阶段大招：第三课·千刀、最后一课
# =====================================================================================
CUT_SPOTS = [(round(r * math.cos(math.radians(a)), 1), round(r * math.sin(math.radians(a)), 1), (a * 7) % 180)
             for r, a in ((0, 0), (2.5, 30), (2.5, 150), (2.5, 270), (4, 0), (4, 90), (4, 180), (4, 270),
                          (1.5, 60), (1.5, 200), (3.5, 120), (3.5, 320), (0, 0), (2, 100), (2, 220), (2, 340),
                          (5, 45), (5, 135), (5, 225), (5, 315), (1, 10), (3, 260), (3, 80), (0, 0))]


def ults2():
    # 第三课·千刀：化作剑风消失，场上依次亮起二十四道斩痕，最后在中心现身一刺；之后喘息 3 秒
    end = CUTS_BACK + 16
    w("ult/cuts", start("cuts", end + STUN + 4) + [
        "data merge entity @s {NoAI:1b}", face(), anim("vanish"),
        "tag @a remove rpg.slb.failed",
        say("第四课，叫千刀。", gloss="The Mad King", name="第四课 · 千刀 · ", stage=2),
        "function %s/vfx/ult2" % B,
    ])
    cuts = [at(12, "function %s/cuts/hide" % B)]
    for k in range(CUTS_N):
        t = CUTS_FROM + CUTS_EVERY * k
        dx, dz, yaw = CUT_SPOTS[k]
        cuts.append(at(t, "execute at @e[%s] at @p[distance=..%d,%s] positioned ~%s ~ ~%s rotated %d 0 run function %s/cuts/mark"
                       % (CENTER, ARENA, SURV, dx, dz, yaw, B)))
    cuts += [at(CUTS_BACK, "function %s/cuts/back" % B),
             at(CUTS_BACK + 6, anim("final")),
             at(CUTS_BACK + 12, "function %s/cuts/final" % B),
             at(end, "function %s/lesson/end" % B),
             at(end, "function %s/skill/stagger" % B)]
    w("sk/cuts", cuts)
    w("cuts/hide", [
        "# 化作剑风（as 他）：藏到地下，部件跟着；无敌",
        "data merge entity @s {Invulnerable:1b,NoGravity:1b}",
        "tag @s add rpg.slb.hidden",
        "particle %s ~ ~1 ~ 0.6 1 0.6 0 30 force" % SILVER_DUST,
        "particle minecraft:sweep_attack ~ ~1 ~ 0.8 0.6 0.8 0 6 force",
        "playsound minecraft:entity.breeze.wind_burst hostile @a[distance=..40] ~ ~ ~ 1 1.4",
        "tp @s ~ ~-40 ~",
    ])
    w("cuts/mark", [
        "# 一道斩痕（at 落点，朝向随机）：亮 0.6 秒后斩下",
        fx.marker("~ ~ ~", "rpg.slb.cut"),
        "execute as @e[tag=%s] run tp @s ~ ~ ~ ~ 0" % NEW,
    ] + fx.born(CUTS_WARN + 1) + ["execute positioned ~ ~0.05 ~ run %s" % s for s in beam(BLOOD_D, (0.5, 0.02, 4.4), (0, 0, 0))]
      + fx.born(CUTS_WARN) + ["playsound minecraft:block.note_block.hat hostile @a[distance=..24] ~ ~ ~ 0.6 1.6"])
    w("fx/cut", [
        "# 斩痕（as/at 标记）：到时斩下",
        "execute if score @s rpg_sl_life matches 1 run function %s/cuts/strike" % B,
    ])
    w("cuts/strike", [
        "# 斩下（as/at 斩痕）：痕上三点各 1.3 格",
        "execute positioned ^ ^ ^-1.5 run tag @a[distance=..1.3,%s] add rpg.slb.hit" % SURV,
        "tag @a[distance=..1.3,%s] add rpg.slb.hit" % SURV,
        "execute positioned ^ ^ ^1.5 run tag @a[distance=..1.3,%s] add rpg.slb.hit" % SURV,
        "execute as @a[tag=rpg.slb.hit] run damage @s %d minecraft:mob_attack" % CUTS_DMG,
        "tag @a[tag=rpg.slb.hit] add rpg.slb.failed",
        "tag @a remove rpg.slb.hit",
    ] + ["execute positioned ~ ~0.08 ~ run %s" % s for s in beam(BLADE_I, (0.4, 0.04, 4.4), (0, 0, 0))] + fx.born(kind="cutfade")
      + fx.slash("~ ~1 ~", BLOOD, size=2.6) + [
        "particle minecraft:sweep_attack ~ ~0.6 ~ 0.6 0.1 0.6 0 2",
        "particle minecraft:crit ~ ~0.5 ~ 0.8 0.2 0.8 0.3 8",
        "playsound minecraft:entity.player.attack.sweep hostile @a[distance=..24] ~ ~ ~ 0.8 1.7",
    ])
    w("cuts/back", [
        "# 在中心现身（as 他），朝最近的人",
        "tp @s @e[%s]" % CENTER,
        "tag @s remove rpg.slb.hidden",
        "execute at @s run %s" % face(ARENA),
        "data merge entity @s {Invulnerable:0b,NoGravity:0b}",
        anim("land"),
        "execute at @s run particle minecraft:flash{color:%d} ~ ~1.4 ~ 0 0 0 0 1 force" % BLADE_I,
        "execute at @s run particle minecraft:sweep_attack ~ ~1 ~ 1 0.6 1 0 8 force",
        "execute at @s run playsound minecraft:entity.breeze.wind_burst hostile @a[distance=..40] ~ ~ ~ 1 0.8",
    ])
    w("cuts/final", ["# 最后一刺（as/at 他）：身前 6 格"] + line("path", 4) + hurt_tagged(CUTS_FINAL)
      + stab_fx(length=6.0, color=0xFFFFFF) + fx.glyph("burst", 3, BLADE, pos="^ ^1.3 ^3", kind="burst")
      + ["particle minecraft:flash{color:%d} ^ ^1.3 ^3 0 0 0 0 1 force" % BLADE_I])

    # 最后一课：退到 15 格外，剑举平指向你，2 秒内地上一条线跟着你转；全速一刺 24。躲开了他冲过去跪地 4 秒
    after = LAST_AIM + LAST_STEPS + 4
    w("ult/last", start("last", after + LAST_KNEEL + 4) + [
        "data merge entity @s {NoAI:1b}",
        "execute at @p[distance=..%d,%s] facing entity @s feet positioned ^ ^ ^%d if block ~ ~0.5 ~ #minecraft:replaceable "
        "if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~" % (ARENA, SURV, LAST_BACK),
        "execute at @s run %s" % face(ARENA), anim("mighty"),
        "tag @a remove rpg.slb.failed",
        say("最后一课，斯塔福德。看清楚。", gloss="The Mad King", name="最后一课 · ", stage=2),
        "execute at @s positioned ~ ~0.05 ~ run function %s/last/aim" % B,
        "execute at @s run function %s/vfx/ult2" % B,
    ])
    w("last/aim", beam(0x8C96A2, (0.8, 0.02, 20), (0, 0, 10), tags=("rpg.slb.aim",)) + fx.born(LAST_AIM + 2))
    w("sk/last", [
        "execute if score @s rpg_sl_t matches 1..%d run %s" % (LAST_AIM - 1, face(ARENA)),
        "execute if score @s rpg_sl_t matches 1..%d as @e[tag=rpg.slb.aim,distance=..2] positioned as @s rotated as @e[%s,limit=1] run tp @s ~ ~ ~ ~ ~"
        % (LAST_AIM - 1, UNIT),
        "execute if score @s rpg_sl_t matches 1..%d run particle %s ^ ^1.4 ^1.2 0.05 0.05 0.05 0 2" % (LAST_AIM, SILVER_DUST),
        at(LAST_AIM - 10, "playsound minecraft:item.trident.riptide_3 hostile @a[distance=..40] ~ ~ ~ 1 0.8"),
        at(LAST_AIM, anim("roll_f")),
        "execute if score @s rpg_sl_t matches %d..%d run function %s/last/step" % (LAST_AIM, LAST_AIM + LAST_STEPS - 1, B),
        at(LAST_AIM + LAST_STEPS, anim("final")),
        at(LAST_AIM + LAST_STEPS + 1, "function %s/last/strike" % B),
        "execute if score @s rpg_sl_t matches %d.. run function %s/sk/end" % (after + LAST_KNEEL, B),
    ])
    w("last/step", [
        "# 全速冲两格（as/at 他）",
        "execute if block ^ ^0.5 ^1 #minecraft:replaceable if block ^ ^1.5 ^1 #minecraft:replaceable unless block ^ ^-0.5 ^1 #minecraft:replaceable run tp @s ^ ^ ^1",
        "tag @a[distance=..1.5,%s] add rpg.slb.hit" % SURV,
        "execute at @s if block ^ ^0.5 ^1 #minecraft:replaceable if block ^ ^1.5 ^1 #minecraft:replaceable unless block ^ ^-0.5 ^1 #minecraft:replaceable run tp @s ^ ^ ^1",
        "execute at @s run tag @a[distance=..1.5,%s] add rpg.slb.hit" % SURV,
        "execute at @s run particle %s ~ ~1 ~ 0.3 0.5 0.3 0 6 force" % SILVER_DUST,
        "execute at @s run particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.3 0.3 0 1",
    ])
    w("last/strike", [
        "# 刺出（as/at 他）：打中了就是一下 24；没打中他冲过去跪地",
        "execute if entity @a[tag=rpg.slb.hit] run return run function %s/last/hit" % B,
        "function %s/last/miss" % B,
    ])
    w("last/hit", hurt_tagged(LAST_DMG) + stab_fx(length=5.0, color=0xFFFFFF) + [
        "particle minecraft:flash{color:%d} ^ ^1.3 ^2 0 0 0 0 1 force" % BLADE_I,
        "playsound minecraft:entity.player.attack.crit hostile @a[distance=..40] ~ ~ ~ 1.4 0.8",
    ] + say_s("……你还是没看清。", name="最后一课 · ") + ["scoreboard players set @s rpg_sl_t %d" % (after + LAST_KNEEL - 20)])
    w("last/miss", [
        "# 躲开了：他冲过头，整个人跪倒；4 秒护甲归零，伤害 +50%（hit/extra）",
        anim("kneel"),
        "attribute @s minecraft:armor base set 0",
        "tag @s add rpg.slb.weak",
        "particle minecraft:flash{color:%d} ~ ~1 ~ 0 0 0 0 1 force" % BLOOD_I,
        "particle minecraft:block{block_state:\"minecraft:gravel\"} ~ ~0.2 ~ 0.6 0.1 0.6 0 20",
        "playsound minecraft:entity.player.attack.nodamage hostile @a[distance=..40] ~ ~ ~ 1.4 0.6",
    ] + say_s("……好。好！看清了。") + fx.decal("ring", 3, BLOOD_I, pos="~ ~0.05 ~", kind="ringm"))


# =====================================================================================
# 特效
# =====================================================================================
def vfx():
    w("vfx/intro", ["# 登场（as/at 战场中心）：天光、银色剑环"]
      + light_pillar(SILVER_I) + fx.decal("ring", 2, BLADE_I, pos="~ ~0.08 ~", kind="ringx")
      + fx.decal("sigil", 3.6, SILVER_I, pos="~ ~0.06 ~", kind="spinf", life=40)
      + ring("minecraft:sweep_attack", 2.4, 8, y=1.0) + wave("minecraft:end_rod", 16, 0.3, y=1)
      + ["particle minecraft:flash{color:%d} ~ ~1.5 ~ 0 0 0 0 1 force" % SILVER_I])
    w("vfx/guard", ["# 招架起手（as/at 他）：剑身一道银光"]
      + fx.glyph("burst", 1.6, BLADE, pos="^0.2 ^1.5 ^0.7", kind="burst") + fx.twinkle("^0.3 ^1.9 ^0.6", BLADE)
      + ["particle minecraft:end_rod ^ ^1.5 ^0.7 0.1 0.3 0.1 0.02 6"])
    w("vfx/shatter", ["# 甲碎（as/at 他）：火花、碎屑、白光"]
      + fx.glyph("burst", 3, SILVER, pos="~ ~1.55 ~", kind="burst") + fx.glyph("pop", 2, BLADE, pos="~ ~1.7 ~", kind="pop")
      + wave("minecraft:crit", 24, 0.6, y=1.8) + [
        "particle minecraft:flash{color:%d} ~ ~2 ~ 0 0 0 0 1 force" % SILVER_I,
        "particle minecraft:block{block_state:\"minecraft:iron_block\"} ~ ~2 ~ 0.5 0.5 0.5 0 30",
        "playsound minecraft:item.shield.break hostile @a[distance=..40] ~ ~ ~ 1.4 0.7",
        "playsound minecraft:entity.iron_golem.damage hostile @a[distance=..40] ~ ~ ~ 1.2 0.6",
    ])
    w("vfx/rise", ["# 他大笑着站起来（as/at 他）：蛛丝炸开、暗红的光"]
      + fx.decal("shock_0", 6, BLOOD_I, pos="~ ~0.1 ~", kind="shock") + fx.decal("ring", 2, BLOOD_I, pos="~ ~0.08 ~", kind="ringm")
      + wave(WEB_DUST, 24, 0.4, y=1.2) + wave(BLOOD_DUST, 16, 0.3, y=0.6) + [
        "particle minecraft:item{item:\"minecraft:cobweb\"} ~ ~1.4 ~ 0.6 0.8 0.6 0.08 24",
        "particle minecraft:flash{color:%d} ~ ~2 ~ 0 0 0 0 1 force" % BLOOD_I,
    ])
    w("vfx/ult2", ["# 二阶段大招起手（as/at 他）：暗红剑印与蛛丝"]
      + fx.decal("hexagram", 5, BLOOD_D, pos="~ ~0.06 ~", kind="spinf", life=40)
      + fx.decal("sigil", 3.4, BLOOD_I, pos="~ ~0.08 ~", kind="spinr", life=40)
      + wave(BLOOD_DUST, 20, 0.35) + wave(WEB_DUST, 12, 0.25, y=1.2)
      + ["particle minecraft:flash{color:%d} ~ ~2 ~ 0 0 0 0 1 force" % BLOOD_I])
    w("vfx/fall", ["# 倒下（as/at 他）：蛛丝散开、白灰飘起"]
      + fx.decal("glow", 3, 0x6A6A70, pos="~ ~0.04 ~", life=60) + wave(WEB_DUST, 20, 0.15, y=0.6)
      + ["particle minecraft:white_ash ~ ~1.5 ~ 1 1 1 0.01 30"])


def finish():
    w("load2", ["scoreboard players set #two %s 2" % O])
    with open(os.path.join(OUT, "load.mcfunction"), encoding="utf-8") as fh:
        text = fh.read().rstrip("\n")
    wf(os.path.join(OUT, "load.mcfunction"), text.split("\n") + ["function %s/load2" % B])
    fx.build(extra_tick=[
        "execute if entity @s[tag=rpg.slb.cut] run return run function %s/fx/cut" % B,
        "execute if entity @s[tag=rpg.slb.web] run function %s/fx/web" % B,
        "execute if entity @s[tag=rpg.slb.rain] run return run function %s/fx/rain" % B,
        "execute if entity @s[tag=rpg.slb.rainsword] run function %s/fx/rainsword" % B,
        "execute if entity @s[tag=rpg.slb.bigsword] run function %s/fx/bigsword" % B,
    ])



# =====================================================================================
# 加强（用户 2026-11-16「技能太少，不符合史上最强的逼格」）：四个新招、每段第三个大招、疯王之舞
# =====================================================================================
def echo_at(tags=()):
    """A white echo of Saul (the saul_ghost look, rapier in hand) here, facing the current rotation."""
    extra = "".join(',"%s"' % x for x in tags)
    return ['summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.slg","rpg.slb.echo","rpg.slb.ghostnew"%s],NoAI:1b,Invulnerable:1b,'
            'Silent:1b,PersistenceRequired:1b,CustomName:{"text":"残影","color":"%s","italic":true},'
            'active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}' % (extra, PHANTOM_C),
            "execute as @e[type=minecraft:vindicator,tag=rpg.slb.ghostnew] run tp @s ~ ~ ~ ~ 0",
            "tag @e[type=minecraft:vindicator,tag=rpg.slb.ghostnew] remove rpg.slb.ghostnew",
            "particle %s ~ ~1 ~ 0.3 0.7 0.3 0 12" % SILVER_DUST,
            "particle minecraft:end_rod ~ ~1 ~ 0.25 0.6 0.25 0.02 6"]


def echo_anim(sel, clip):
    return "execute as @e[%s] run function %s/anim/enter/%s" % (sel, PHANTOM, clip)


def skills_more():
    # ---- 一闪（一阶段）：收剑蓄势，瞬间穿过你、停在你身后；身后留下一道剑痕，0.5 秒后斩开
    w("skill/flash", start("flash", 42) + [
        "data merge entity @s {NoAI:1b}", face(), anim("showoff"),
        "playsound minecraft:item.armor.equip_chain hostile @a[distance=..24] ~ ~ ~ 1 0.6",
    ] + say_s("看清了吗？", name="一闪 · "))
    w("sk/flash", [
        "execute if score @s rpg_sl_t matches 1..13 run %s" % face(),
        "execute if score @s rpg_sl_t matches 1..13 run particle %s ^ ^1.3 ^0.6 0.6 0.6 0.6 0 3" % SILVER_DUST,
        at(6, "function %s/vfx/gather" % B),
        at(14, "function %s/flash/go" % B),
        at(15, anim("final")),
        at(18, face()),
        at(24, "function %s/flash/cut" % B),
        "execute if score @s rpg_sl_t matches 40.. run function %s/sk/end" % B,
    ])
    w("flash/go", [
        "# 瞬身（as/at 他）：起点留一个标记，落到最近那人身后 2.5 格；起点到落点画剑痕",
        fx.marker("~ ~ ~", "rpg.slb.flasha"),
    ] + fx.born(30) + [
        "execute as @e[tag=rpg.slb.flasha,limit=1,sort=nearest] run tp @s ~ ~ ~ ~ 0",
        "execute at @p[distance=..14,%s] facing entity @s feet positioned ^ ^ ^-2.5 if block ~ ~0.5 ~ #minecraft:replaceable "
        "if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~" % SURV,
        "scoreboard players set #d %s 10" % O,
        "execute as @e[tag=rpg.slb.flasha,limit=1,sort=nearest] at @s facing entity @e[%s,limit=1] feet run function %s/flash/trail" % (UNIT, B),
        "kill @e[tag=rpg.slb.flasha]",
        "playsound minecraft:entity.breeze.wind_burst hostile @a[distance=..32] ~ ~ ~ 1 1.6",
        "playsound minecraft:item.trident.riptide_2 hostile @a[distance=..32] ~ ~ ~ 1 1.4",
    ])
    w("flash/trail", [
        "# 剑痕的一节（at 这一节，朝落点）",
        fx.marker("~ ~ ~", "rpg.slb.flashseg"),
    ] + fx.born(12) + ["execute positioned ~ ~1 ~ run %s" % s for s in beam(BLADE_I, (0.16, 0.16, 1.6), (0, 0, 0.75))] + fx.born(12) + [
        "particle minecraft:end_rod ~ ~1 ~ 0.2 0.2 0.2 0.02 2",
        "scoreboard players remove #d %s 1" % O,
        "execute if score #d %s matches 1.. unless entity @e[%s,distance=..1.6] positioned ^ ^ ^1.5 run function %s/flash/trail" % (O, UNIT, B),
    ])
    w("flash/cut", [
        "# 剑痕斩开（as 他）：每一节 1.4 格内的人都挨一下",
        "execute as @e[tag=rpg.slb.flashseg] at @s run tag @a[distance=..1.4,%s] add rpg.slb.hit" % SURV,
    ] + hurt_tagged(FLASH_DMG) + [
        "execute as @e[tag=rpg.slb.flashseg] at @s run function %s/flash/burst" % B,
        "kill @e[tag=rpg.slb.flashseg]",
        "playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.4 1.8",
        "playsound minecraft:block.glass.break hostile @a[distance=..40] ~ ~ ~ 1 1.6",
    ])
    w("flash/burst", fx.slash("~ ~1 ~", BLADE, size=2.2) + [
        "particle minecraft:sweep_attack ~ ~1 ~ 0.2 0.2 0.2 0 1",
        "particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.4 6",
    ])

    # ---- 残影剑阵（一阶段）：三个残影围住你，各亮一条线，1 秒后同时刺过来
    w("skill/echo", start("echo", 50) + [
        "data merge entity @s {NoAI:1b}", face(), anim("mighty"),
        "execute at @p[distance=..%d,%s] run function %s/echo/ring" % (BASIC_RANGE, SURV, B),
    ] + say_s("看好了——这是三个我。", name="残影剑阵 · "))
    ring3 = ["# 三个残影（at 玩家）：120° 一个，5 格外，朝着玩家"]
    for a in (0, 120, 240):
        ring3.append("execute rotated as @e[%s,limit=1] rotated ~%d 0 positioned ^ ^ ^-5 facing entity @p feet rotated ~ 0 run function %s/echo/one"
                     % (UNIT, a, B))
    w("echo/ring", ring3)
    w("echo/one", echo_at() + ["execute positioned ~ ~0.05 ~ run %s" % s for s in beam(0x8C96A2, (0.6, 0.02, 9), (0, 0, 4.5))] + fx.born(22))
    w("sk/echo", [
        at(3, echo_anim(GHOST + ",tag=rpg.slb.echo", "idle")),
        at(22, echo_anim(GHOST + ",tag=rpg.slb.echo", "thrust")),
        at(24, "execute as @e[%s,tag=rpg.slb.echo] at @s run function %s/echo/strike" % (GHOST, B)),
        at(36, "execute as @e[%s,tag=rpg.slb.echo] at @s run function %s/echo/fade" % (GHOST, B)),
        "execute if score @s rpg_sl_t matches 48.. run function %s/sk/end" % B,
    ])
    w("echo/strike", ["# 一个残影刺出（as/at 它）：9 格的线"] + ["execute positioned ~ ~0.6 ~ run function %s/echo/line" % B]
      + ["execute as @a[tag=rpg.slb.hit] run damage @s %d minecraft:mob_attack by @e[%s,limit=1]" % (ECHO_DMG, UNIT),
         "tag @a[tag=rpg.slb.hit] add rpg.slb.failed", "tag @a remove rpg.slb.hit"]
      + stab_fx(length=6.0, color=0xFFFFFF) + ["playsound minecraft:item.trident.throw hostile @a[distance=..24] ~ ~ ~ 1 1.5"])
    w("echo/line", line("thin", 6))
    w("echo/fade", ["# 残影散去（as/at 它）"] + wave(SILVER_DUST, 12, 0.2, y=1) + [
        "particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.04 10",
        "function %s/clear_unit" % B,
    ])

    # ---- 血之千刺（二阶段）：站定，1.5 秒内朝前方扇形乱刺十五下；绕到他身后
    w("skill/thrusts", start("thrusts", 44) + ["data merge entity @s {NoAI:1b}", face()]
      + say_s("千刺！看得见吗！", name="血之千刺 · "))
    yaws = [-22, 10, -6, 24, -16, 4, 18, -26, 0, 14, -10, 26, -20, 8, -2]
    th = []
    for k, y in enumerate(yaws):
        tk = 4 + 2 * k
        th.append(at(tk, anim(("left", "right", "double")[k % 3])))
        th.append(at(tk, "execute rotated ~%d 0 run function %s/thrusts/stab" % (y, B)))
    th.append("execute if score @s rpg_sl_t matches 2..36 run particle %s ^ ^1.2 ^1.5 0.6 0.4 0.6 0 2" % BLOOD_DUST)
    th.append("execute if score @s rpg_sl_t matches 43.. run function %s/sk/end" % B)
    w("sk/thrusts", th)
    w("thrusts/stab", ["# 一刺（as/at 他，朝这一刺的方向）：7.5 格的细线"] + ["execute positioned ~ ~0.6 ~ run function %s/echo/line" % B]
      + ["execute as @a[tag=rpg.slb.hit] run damage @s %d minecraft:mob_attack by @e[%s,limit=1]" % (THRUST_DMG, UNIT),
         "tag @a[tag=rpg.slb.hit] add rpg.slb.failed", "tag @a remove rpg.slb.hit"]
      + stab_fx(length=6.5, color=BLOOD_I) + ["playsound minecraft:entity.player.attack.strong hostile @a[distance=..24] ~ ~ ~ 0.6 1.8"])

    # ---- 影步斩（二阶段）：消失，出现在你身后，回身一记双斩；落点先亮 0.4 秒
    w("skill/step", start("step", 34) + ["data merge entity @s {NoAI:1b}", face(), anim("vanish")]
      + say_s("在你身后。", name="影步斩 · "))
    w("sk/step", [
        at(3, "execute at @p[distance=..%d,%s] rotated as @p rotated ~ 0 positioned ^ ^ ^-2.4 run function %s/step/mark" % (BASIC_RANGE, SURV, B)),
        at(11, "function %s/step/go" % B),
        at(12, face(6)),
        at(12, anim("double")),
        at(15, "function %s/step/strike" % B),
        "execute if score @s rpg_sl_t matches 32.. run function %s/sk/end" % B,
    ])
    w("step/mark", [
        "# 落点（at 你身后 2.4 格）：一个暗红的印",
        fx.marker("~ ~ ~", "rpg.slb.stepto"),
    ] + fx.born(14) + fx.decal("sigil", 2.4, BLOOD_I, pos="~ ~0.06 ~", kind="spinf", life=12) + [
        "particle %s ~ ~1 ~ 0.3 0.6 0.3 0 10" % BLOOD_DUST,
        "playsound minecraft:block.note_block.basedrum hostile @a[distance=..24] ~ ~ ~ 1 0.6",
    ])
    w("step/go", [
        "# 影步（as/at 他）：原处散成蛛丝，到印上现身",
    ] + wave(WEB_DUST, 12, 0.25, y=1) + [
        "execute as @e[tag=rpg.slb.stepto,limit=1,sort=nearest] at @s if block ~ ~0.5 ~ #minecraft:replaceable "
        "if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @e[%s,limit=1,sort=nearest] ~ ~ ~" % UNIT,
        "kill @e[tag=rpg.slb.stepto]",
        "execute at @s run particle minecraft:flash{color:%d} ~ ~1.2 ~ 0 0 0 0 1 force" % BLOOD_I,
        "execute at @s run playsound minecraft:entity.enderman.teleport hostile @a[distance=..24] ~ ~ ~ 1 0.7",
    ])
    w("step/strike", ["# 回身双斩（as/at 他）：身前 3 格", tag_near(2.2, "^ ^ ^1.6")] + hurt_tagged(STEP_DMG)
      + ["execute positioned ^ ^1.1 ^1.2 run %s" % fx.disp("crescent", color=BLOOD_I),
         "execute as @e[tag=%s] positioned as @s run tp @s ~ ~ ~ ~ 0" % NEW] + fx.born(10)
      + fx.slash("^ ^1.3 ^1.6", BLADE, size=3) + [
        "particle minecraft:sweep_attack ^ ^1 ^1.8 0.8 0.2 0.8 0 3",
        "particle %s ^ ^1.2 ^1.8 0.6 0.3 0.6 0 8" % BLOOD_DUST,
    ])


def ults_more():
    # ---- 第三课·残影（一阶段）：四个残影站在场地四方，轮流冲过中心，最后四个一齐冲；对角线是安全的
    first, gap = 16, 18
    final_warn = first + gap * 4
    final_hit = final_warn + 20
    end = final_hit + 16
    w("ult/echoes", start("echoes", end + STUN + 4) + [
        "data merge entity @s {NoAI:1b}",
        "tp @s @e[%s]" % CENTER,
        "execute at @s run function %s/echoes/begin" % B,
    ])
    begin = ["# 站回中心（as/at 他）：四个残影站到东南西北 10 格外，朝着中心", anim("mighty"),
             "tag @a remove rpg.slb.failed",
             say("第三课。剑没有定形——看清每一个我。", gloss="The Marshal", name="第三课 · 残影 · ")]
    for k, a in enumerate((0, 90, 180, 270)):
        begin.append("execute rotated %d 0 positioned ^ ^ ^10 rotated ~180 0 run function %s/echoes/one%d" % (a, B, k))
        w("echoes/one%d" % k, echo_at(("rpg.slb.echo%d" % k,)))
    begin += fx.decal("sigil", 4, SILVER_I, pos="~ ~0.06 ~", kind="spin", life=end)
    w("echoes/begin", begin)
    ec = []
    for k in range(4):
        sel = GHOST + ",tag=rpg.slb.echo%d" % k
        tw, td = first + gap * k, first + gap * k + 14
        ec += [at(tw, "execute as @e[%s] at @s positioned ~ ~0.05 ~ run function %s/echoes/warn" % (sel, B)),
               at(td, echo_anim(sel, "roll_f")),
               "execute if score @s rpg_sl_t matches %d..%d as @e[%s] at @s run function %s/echoes/dash" % (td, td + 9, sel, B),
               at(td + 10, "execute as @e[%s] at @s run function %s/echoes/hurt" % (sel, B)),
               at(td + 10, echo_anim(sel, "thrust"))]
    allsel = GHOST + ",tag=rpg.slb.echo"
    ec += [at(final_warn - 2, "execute as @e[%s] at @s facing entity @e[%s] feet run tp @s ~ ~ ~ ~ 0" % (allsel, CENTER)),
           at(final_warn, "execute as @e[%s] at @s positioned ~ ~0.05 ~ run function %s/echoes/warn" % (allsel, B)),
           at(final_warn, say("一起来！", gloss="The Marshal")),
           at(final_hit, echo_anim(allsel, "roll_f")),
           "execute if score @s rpg_sl_t matches %d..%d as @e[%s] at @s run function %s/echoes/dash" % (final_hit, final_hit + 9, allsel, B),
           at(final_hit + 10, "execute as @e[%s] at @s run function %s/echoes/hurt" % (allsel, B)),
           at(final_hit + 10, echo_anim(allsel, "final")),
           at(end, "execute as @e[%s] at @s run function %s/echo/fade" % (allsel, B)),
           at(end, "function %s/lesson/end" % B),
           at(end + 2, "function %s/skill/stagger" % B)]
    w("sk/echoes", ec)
    w("echoes/warn", beam(0x8C96A2, (1.2, 0.02, 20), (0, 0, 10)) + fx.born(16)
      + ["playsound minecraft:block.note_block.chime hostile @a[distance=..40] ~ ~ ~ 0.8 0.9"])
    w("echoes/dash", [
        "# 残影冲一步（as/at 它）：每刻 2 格，碰到的人记下",
        "tp @s ^ ^ ^2",
        "execute at @s run tag @a[distance=..1.4,%s] add rpg.slb.hit" % SURV,
        "execute at @s run particle %s ~ ~1 ~ 0.3 0.5 0.3 0 6 force" % SILVER_DUST,
        "execute at @s run particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.3 0.3 0 1",
    ])
    w("echoes/hurt", ["execute as @a[tag=rpg.slb.hit] run damage @s %d minecraft:mob_attack by @e[%s,limit=1]" % (ECHOES_DMG, UNIT),
                      "tag @a[tag=rpg.slb.hit] add rpg.slb.failed", "tag @a remove rpg.slb.hit",
                      "playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1 1.3"])

    # ---- 第五课·万剑（二阶段）：天上落下成排的千刀，最后一把巨剑砸在中心；之后喘息
    rain_from, rain_every, rain_n = 10, 4, 16
    big_warn = rain_from + rain_every * rain_n + 4
    big_hit = big_warn + 18
    rend = big_hit + 14
    w("ult/rain", start("rain", rend + STUN + 4) + [
        "data merge entity @s {NoAI:1b}",
        "tp @s @e[%s]" % CENTER,
        "execute at @s run function %s/rain/begin" % B,
    ])
    w("rain/begin", [anim("mighty"), "tag @a remove rpg.slb.failed",
                     say("第五课。抬头——天上全是剑。", gloss="The Mad King", name="第五课 · 万剑 · ", stage=2)]
      + light_pillar(BLOOD_I) + fx.decal("hexagram", 6, BLOOD_D, pos="~ ~0.06 ~", kind="spinf", life=rend))
    rn = []
    for k in range(rain_n):
        dx, dz, _ = CUT_SPOTS[(k * 5) % len(CUT_SPOTS)]
        rn.append(at(rain_from + rain_every * k, "execute at @e[%s] at @p[distance=..%d,%s] positioned ~%s ~ ~%s run function %s/rain/one"
                     % (CENTER, ARENA, SURV, dx, dz, B)))
    rn += [at(big_warn, "execute at @e[%s] run function %s/rain/bigwarn" % (CENTER, B)),
           at(big_warn, say("……最后一把。", gloss="The Mad King", stage=2)),
           at(big_hit, "execute at @e[%s] run function %s/rain/bighit" % (CENTER, B)),
           at(rend, "function %s/lesson/end" % B),
           at(rend + 2, "function %s/skill/stagger" % B)]
    w("sk/rain", rn)
    w("rain/one", [
        "# 一把落剑（at 落点）：地上一圈预警，剑从 10 格高处插下来",
        fx.marker("~ ~ ~", "rpg.slb.rain"),
    ] + fx.born(15) + fx.decal("ring", 3.2, BLOOD_I, pos="~ ~0.06 ~", life=14) + [
        'summon minecraft:item_display ~ ~10 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.rainsword"],'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:saul/rapier"}},item_display:"none",'
        'brightness:{sky:15,block:15},teleport_duration:0,view_range:2f,transformation:{translation:[0f,0f,0f],'
        'left_rotation:[1f,0f,0f,0f],scale:[1.6f,1.6f,1.6f],right_rotation:[0f,0f,0f,1f]}}',
    ] + fx.born(24) + ["particle minecraft:end_rod ~ ~10 ~ 0.2 0.3 0.2 0.02 6"])
    w("fx/rainsword", [
        "# 落剑（as/at 它）：出生 3 刻后用 10 刻插到地上",
        "execute if score @s rpg_sl_life matches 21 run data merge entity @s {teleport_duration:10}",
        "execute if score @s rpg_sl_life matches 21 run tp @s ~ ~-9.2 ~",
        "execute if score @s rpg_sl_life matches 12..20 run particle minecraft:end_rod ~ ~0.5 ~ 0.05 0.3 0.05 0 1",
    ])
    w("fx/rain", ["execute if score @s rpg_sl_life matches 1 run function %s/rain/hit" % B])
    w("rain/hit", [
        "# 落剑着地（as/at 标记）：1.6 格内 10",
        "execute as @a[distance=..1.6,%s] run damage @s %d minecraft:mob_attack" % (SURV, RAIN_DMG),
        "tag @a[distance=..1.6,%s] add rpg.slb.failed" % SURV,
    ] + fx.decal("shock_0", 3.4, BLADE_I, pos="~ ~0.1 ~", kind="shock") + fx.decal("cracks", 2.4, 0x2A2A30, pos="~ ~0.04 ~", life=60) + [
        "particle minecraft:crit ~ ~0.4 ~ 0.5 0.2 0.5 0.4 10",
        "particle minecraft:block{block_state:\"minecraft:stone\"} ~ ~0.2 ~ 0.4 0.1 0.4 0 8",
        "playsound minecraft:item.trident.hit_ground hostile @a[distance=..32] ~ ~ ~ 1 0.8",
    ])
    w("rain/bigwarn", ["# 巨剑预警（at 中心）：5 格的圈"] + fx.decal("ring", 10, BLOOD_I, pos="~ ~0.06 ~", life=18)
      + fx.decal("glow", 10, BLOOD_D, pos="~ ~0.04 ~", life=18) + [
        'summon minecraft:item_display ~ ~22 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.bigsword"],'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:saul/rapier"}},item_display:"none",'
        'brightness:{sky:15,block:15},teleport_duration:0,view_range:4f,transformation:{translation:[0f,0f,0f],'
        'left_rotation:[1f,0f,0f,0f],scale:[7f,7f,7f],right_rotation:[0f,0f,0f,1f]}}',
    ] + fx.born(60) + ["playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 1.4 0.5"])
    w("fx/bigsword", [
        "execute if score @s rpg_sl_life matches 56 run data merge entity @s {teleport_duration:14}",
        "execute if score @s rpg_sl_life matches 56 run tp @s ~ ~-20 ~",
    ])
    w("rain/bighit", [
        "# 巨剑砸地（at 中心）：5 格内 18",
        "execute as @a[distance=..5,%s] run damage @s %d minecraft:mob_attack" % (SURV, RAIN_BIG),
        "tag @a[distance=..5,%s] add rpg.slb.failed" % SURV,
    ] + fx.decal("shock_0", 14, BLADE_I, pos="~ ~0.1 ~", kind="shock") + fx.decal("cracks", 9, 0x1A1A20, pos="~ ~0.04 ~", life=100)
      + fx.decal("ring", 2, BLOOD_I, pos="~ ~0.08 ~", kind="ringx") + fx.glyph("burst", 6, BLADE, pos="~ ~1.5 ~", kind="burst")
      + wave("minecraft:crit", 32, 0.8, y=0.4) + wave(BLOOD_DUST, 24, 0.5, y=0.6) + [
        "particle minecraft:flash{color:%d} ~ ~1 ~ 0 0 0 0 1 force" % BLADE_I,
        "playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1.2 0.6",
        "playsound minecraft:block.anvil.land hostile @a[distance=..48] ~ ~ ~ 1.4 0.5",
    ])

    # ---- 疯王之舞（二阶段血量到 150，只一次）：围着你六次穿刺，留下六道剑痕；最后所有剑痕同时斩开，交汇处是死地
    d_first, d_gap = 16, 14
    d_burst = d_first + d_gap * 6 + 10
    d_end = d_burst + 70
    w("ult/dance", start("dance", d_end + 4) + [
        "tag @s add rpg.slb.danced",
        "data merge entity @s {NoAI:1b,Invulnerable:1b}",
        anim("hero"),
        "execute as @a[distance=..%d,%s] run effect give @s minecraft:darkness 6 0 true" % (ARENA, SURV),
        "function %s/vfx/ult2" % B,
        say("……还没完。还没完！斯塔福德，看——这是我最后的剑！", gloss="The Mad King", name="疯王之舞 · ", stage=2),
        "playsound minecraft:entity.warden.roar hostile @a[distance=..48] ~ ~ ~ 1 1.4",
    ])
    dn = []
    for k in range(6):
        tw = d_first + d_gap * k
        dn += [at(tw, "execute at @p[distance=..%d,%s] rotated %d 0 positioned ^ ^ ^7 if block ~ ~0.5 ~ #minecraft:replaceable "
                      "if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~" % (ARENA, SURV, 60 * k)),
               at(tw, "execute at @s run %s" % face(ARENA)),
               at(tw + 1, "execute at @s positioned ~ ~0.05 ~ run function %s/dance/warn" % B),
               at(tw + 1, anim("roll_f")),
               "execute if score @s rpg_sl_t matches %d..%d run function %s/dance/step" % (tw + 7, tw + 13, B),
               at(tw + 13, anim("final")),
               at(tw + 13, "playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.2 %.2f" % (0.8 + 0.12 * k))]
        dn.append(at(tw + 14, "execute as @a[tag=rpg.slb.hit] run damage @s %d minecraft:mob_attack by @e[%s,limit=1]" % (DANCE_DMG, UNIT)))
        dn.append(at(tw + 14, "tag @a remove rpg.slb.hit"))
    dn += [at(d_burst - 12, "function %s/dance/glow" % B),
           at(d_burst - 12, say("……斩！", stage=2)),
           at(d_burst, "function %s/dance/burst" % B),
           at(d_burst + 1, "execute as @a[tag=rpg.slb.hit] run damage @s %d minecraft:mob_attack by @e[%s,limit=1]" % (DANCE_X, UNIT)),
           at(d_burst + 1, "tag @a remove rpg.slb.hit"),
           at(d_burst + 4, "data merge entity @s {Invulnerable:0b}"),
           at(d_burst + 4, anim("kneel")),
           at(d_burst + 4, "attribute @s minecraft:armor base set 0"),
           at(d_burst + 4, "tag @s add rpg.slb.weak"),
           at(d_burst + 6, say("……哈。哈哈……真是，老了。", stage=2)),
           "execute if score @s rpg_sl_t matches %d.. run function %s/sk/end" % (d_end, B)]
    w("sk/dance", ["execute unless entity @a[distance=..%d,%s] run return run function %s/dance/abort" % (ARENA + 8, SURV, B)] + dn)
    w("dance/abort", ["# 没人可以围着转了：收招（as 他）", "kill @e[tag=rpg.slb.danceseg]", "kill @e[tag=rpg.slb.dancebeam]",
                      "function %s/sk/end" % B, anim("idle")])
    w("dance/warn", beam(0x8C96A2, (0.7, 0.02, 14), (0, 0, 7)) + fx.born(8))
    w("dance/step", [
        "# 穿刺一步（as/at 他）：每刻 2 格；沿途留下一节剑痕（到最后一起斩开）",
        "execute if block ^ ^0.5 ^2 #minecraft:replaceable if block ^ ^1.5 ^2 #minecraft:replaceable unless block ^ ^-0.5 ^2 #minecraft:replaceable run tp @s ^ ^ ^2",
        "execute at @s run tag @a[distance=..1.4,%s] add rpg.slb.hit" % SURV,
        "execute at @s run function %s/dance/seg" % B,
        "execute at @s run particle %s ~ ~1 ~ 0.3 0.5 0.3 0 6 force" % BLOOD_DUST,
    ])
    w("dance/seg", [fx.marker("~ ~ ~", "rpg.slb.danceseg")] + fx.born(400)
      + ["execute positioned ~ ~0.08 ~ run %s" % s for s in beam(BLOOD_D, (0.35, 0.03, 2.2), (0, 0, -1.0), tags=("rpg.slb.dancebeam",))]
      + fx.born(400))
    w("dance/glow", ["# 剑痕发亮（as 他）：快斩开了",
                     "execute as @e[tag=rpg.slb.dancebeam] run data modify entity @s item.components.\"minecraft:custom_model_data\".colors[0] set value %d" % BLADE_I,
                     "execute as @e[tag=rpg.slb.danceseg] at @s run particle minecraft:end_rod ~ ~0.4 ~ 0.3 0.1 0.3 0.01 2",
                     "playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 1 1.6"])
    w("dance/burst", [
        "# 所有剑痕同时斩开（as 他）",
        "execute as @e[tag=rpg.slb.danceseg] at @s run tag @a[distance=..1.3,%s] add rpg.slb.hit" % SURV,
        "execute as @e[tag=rpg.slb.danceseg] at @s run function %s/flash/burst" % B,
        "kill @e[tag=rpg.slb.danceseg]",
        "kill @e[tag=rpg.slb.dancebeam]",
        "particle minecraft:flash{color:%d} ~ ~1 ~ 0 0 0 0 1 force" % BLOOD_I,
        "playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 1.4",
        "playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 1.4 0.8",
    ])


def vfx_more():
    w("vfx/gather", ["# 收剑蓄势（as/at 他）：银光向剑上收拢"]
      + fx.decal("sigil", 2.6, SILVER_I, pos="~ ~0.06 ~", kind="spinf", life=10) + fx.twinkle("^0.3 ^1.6 ^0.5", BLADE)
      + ["particle minecraft:end_rod ~ ~1 ~ 1.2 0.8 1.2 0 12"])
    w("vfx/death", ["# 他沉入地面之前（as/at 他）：一道天光落下"]
      + light_pillar(SILVER_I) + fx.decal("ring", 2, BLADE_I, pos="~ ~0.06 ~", kind="ringm")
      + wave("minecraft:end_rod", 20, 0.15, y=0.8) + ["particle minecraft:totem_of_undying ~ ~1 ~ 0.5 0.6 0.5 0.2 20"])

def main():
    build()
    skills()
    skills_more()
    ults1()
    ults2()
    ults_more()
    vfx()
    vfx_more()
    finish()
    hook_tag(DP, "load", "%s/load" % B, False)
    hook_tag(DP, "tick", "%s/tick" % B, True)
    count = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("saul_boss: %d functions; two stages of %d HP" % (count, MAX))


if __name__ == "__main__":
    main()
