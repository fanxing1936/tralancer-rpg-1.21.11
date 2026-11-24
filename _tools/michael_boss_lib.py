# -*- coding: utf-8 -*-
"""米迦勒战的共用常量与小工具（add_michael_boss.py 及 michael_boss_*.py 共用）。"""


import json
import math
import os
import sys

import rpg_ui_style as ui
import add_michael_boss_art as art
import add_michael_fx_art as mart
from boss_fx import Fx, flat_sc, sc
from display_mob import hook_tag, wf, wj

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "michael_boss")
B = "rpg:michael_boss"
LOOK = "rpg:michael"
WLOOK = "rpg:watchling"
O = "rpg_mk"
UNIT = "type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview"
WATCH = "type=minecraft:vindicator,tag=rpg.mkb.w"
CENTER = "type=minecraft:marker,tag=rpg.mkb.center,limit=1"
LAG = "type=minecraft:marker,tag=rpg.mkb.lag,limit=1"
LAST = "type=minecraft:marker,tag=rpg.mkb.last,limit=1"   # 他最后的位置（每次读血时挪过去），载体意外死掉时补放死亡特效
SURV = "gamemode=!spectator,gamemode=!creative"
BAR = "rpg:michael_boss"

ARENA = 40
BAR_RANGE = 48
EMPTY_LIMIT = 1200
STRIDE = 4
MAX = 1200
ARMOR1, ARMOR2 = 12, 8
SPEED1, SPEED2 = 0.30, 0.36
GUARD_ITEM = 'minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]'
GAP1, GAP2 = 10, 7
BASICS_PER_SKILL = 3
BASIC_RANGE = 25
MELEE1, MELEE2 = 5, 3.5
FAR = 8
WATCH_MAX = {1: 2, 2: 3}
WATCH_HP = 60
WATCH_HIT, WATCH_HEAVY = 6, 10

# 配色：灵体的暖白与珊瑚，二阶段的圣焰橙红（与模型一致）
WHITE = "#FFF5EE"
WHITE_I = 0xFFF5EE
PEACH = "#FFD0BD"
PEACH_I = 0xFFD0BD
CORAL = "#FF805F"
CORAL_I = 0xFF805F
FIRE = "#FF3300"
FIRE_I = 0xFF3300
FIRE_D = 0x8A1A00
BONE_I = 0xF2E6D8

STAGES = {
    # 段号: (名称, 小注, 大招血线, 大招时钟（刻）, 音乐, 音乐长度（刻）, 招式轮换)
    1: ("天使长", "Quis ut Deus", (900, 600, 300), 900, "rpg:bgm.michael1", 1647, ["watch", "quis", "feather", "gaze", "dive", "fold"]),
    2: ("炽天使", "The Seraph", (900, 600, 300), 1100, "rpg:bgm.michael2", 2917, ["watch", "dash", "cross", "gaze", "rain", "dash"]),
}
ULTS = {1: ["who", "sanctus", "trumpet"], 2: ["bones", "seraph", "stars"]}
BURN_AT = 150
SKILL_ID = {"slash1": 1, "slash2": 2, "sweep": 3, "quis": 4, "dive": 5, "fold": 6, "feather": 7, "watch": 8, "gaze": 9,
            "rslash": 10, "dash": 11, "cross": 12, "rain": 13, "who": 14, "sanctus": 15, "trumpet": 16, "bones": 17,
            "seraph": 18, "stars": 19, "burn": 20}

# 数值（设计稿第 4 节）
SLASH_DMG, SWEEP_DMG, QUIS_DMG, DIVE_DMG, DIVE_EDGE, FOLD_DMG, FEATHER_DMG = 7, 10, 12, 14, 6, 8, 6
GAZE_BASE, GAZE_PER = 12, 6
RIB_DMG, FLAME_DMG, DASH_DMG, TRAIL_DMG, CROSS_DMG, RAIN_DMG = 5, 10, 10, 3, 11, 6
WHO_DMG, SANCTUS_DMG, TRUMPET_DMG = 12, 12, 10
BONES_DMG, BONES_DASH, SERAPH_FIRE, STAR_DMG, STAR_BIG, BURN_DMG = 10, 8, 6, 8, 18, 12
SOLID_WIN = 40                      # 大招收招后显形的刻数
STUN = 40


def w(path, lines):
    wf(os.path.join(OUT, *path.split("/")) + ".mcfunction", lines)


HOT = {FIRE, FIRE_I, CORAL, CORAL_I, FIRE_D}
MNS = mart.NS


def fly(dx, dy, dz, life=14):
    return dict(life=life, frames=("glyph", "fburn", 6, 2), steps=[(life - 1, life - 2, "translation:[%gf,%gf,%gf]" % (dx, dy, dz))])


FLY = [(round(4.5 * math.cos(math.radians(a)), 2), 1.2 + 0.6 * (i % 2), round(4.5 * math.sin(math.radians(a)), 2))
       for i, a in enumerate(range(0, 360, 45))]


class MichaelFx(Fx):
    """米迦勒的贴图（add_michael_fx_art.py，颜色烘焙在贴图里）。旧的调用照旧写，名字和颜色在这里换成米迦勒自己的：
    ring/glow/sigil/cracks/crescent/shock_0 → 米迦勒的圆环、光晕、炽天使圣印、焦痕、冲击环；
    暖色（白、桃）走一阶段的白金，热色（橙红、珊瑚、暗红）走二阶段的圣焰。"""

    def decal(self, name, size, color, pos="~ ~0.05 ~", kind=None, life=None, tags=(), yaw=None):
        hot = color in HOT
        mapped = {"ring": "ring_r" if color == FIRE_D else ("ring_f" if hot else "ring_h"),
                  "glow": "glow_f" if hot else "glow_h", "sigil": "seal_seraph", "cracks": "scorch",
                  "crescent": "ring_h", "shock_0": "shock_0" if hot else "shockh_0"}.get(name)
        if name == "shock_0" and kind == "shock":
            kind = "mshock" if mapped == "shock_0" else "mshockh"
        if mapped or name in mart.DECALS or name in mart.ANIMATED:
            return [self.disp("%s/%s" % (MNS, mapped or name), pos=pos, scale=(size, 1, size), color=0xFFFFFF, tags=tags,
                              yaw=yaw)] + self.born(life, kind)
        return Fx.decal(self, name, size, color, pos, kind, life, tags, yaw)

    def glyph(self, name, blocks, color, pos="~ ~ ~", frame=0, kind=None, life=None, tags=(), billboard="center",
              trans=(0, 0, 0), start=None, born_now=True, tpd=1, lrot=None, view=2):
        if name in mart.glyph_table():
            if color in HOT and name + "f" in mart.glyph_table():
                name = name + "f"
                kind = {"burst": "burstf"}.get(kind, kind)
            color = "white"
        return Fx.glyph(self, name, blocks, color, pos, frame, kind, life, tags, billboard, trans, start, born_now, tpd, lrot, view)

    def slash(self, pos, color, size=2.4, frame=0, roll=0):
        hot = color in HOT
        return Fx.glyph(self, "arcf" if hot else "arc", size, "white", pos=pos, kind="arcffx" if hot else "arcfx",
                        lrot=zrot(roll) if roll else None)


def zrot(deg):
    a = math.radians(deg) / 2
    return "[0f,0f,%.5ff,%.5ff]" % (math.sin(a), math.cos(a))


KINDS = {
    "spinf": dict(extra=["tp @s ~ ~ ~ ~7 ~"]),
    "spins": dict(extra=["tp @s ~ ~ ~ ~1.5 ~"]),
    "ringm": dict(life=12, steps=[(11, 10, flat_sc(6))]),
    "ringx": dict(life=14, steps=[(13, 12, flat_sc(11))]),
    "ringgrow": dict(life=60, steps=[(59, 58, flat_sc(61))]),
    "seraphring": dict(life=22, steps=[(21, 20, flat_sc(80))]),
    "pillarfade": dict(life=24, steps=[(23, 3, sc((0.75, 28, 0.75))), (12, 12, sc((0.02, 28, 0.02)))]),
    "pillarcore": dict(life=24, steps=[(23, 3, sc((0.3, 28, 0.3))), (14, 10, sc((0.01, 28, 0.01)))]),
    # 骨刺：一根骨色的方柱从地里长出来再缩回（用户 2026-11-18「骨刺回复之前的样子（那个立方体样子）」）
    "spike": dict(life=12, steps=[(11, 2, sc((0.35, 1.8, 0.35))), (5, 5, sc((0.02, 0.4, 0.02)))]),
    "stabfade": dict(life=8, steps=[(6, 6, "scale:[0.01f,0.01f,4f]")]),
    "linefade": dict(life=16, steps=[(10, 10, "scale:[0.02f,0.02f,30f]")]),
    "crossfade": dict(life=10, steps=[(7, 7, "scale:[0.02f,0.02f,9f]")]),
    "eye": dict(life=200),
    # 二阶段冲刺的火路：原版火方块的展示实体（用户 2026-11-21「冲刺路径的火焰改成火焰方块的展示实体」），
    # 窜起、烧着、最后矮下去；缩放时平移一起插值，火才不会偏离中心
    "fireblk": dict(life=60, steps=[(59, 3, "translation:[-0.6f,0f,-0.6f],scale:[1.2f,1.5f,1.2f]"),
                                    (8, 8, "translation:[-0.45f,0f,-0.45f],scale:[0.9f,0.01f,0.9f]")]),
    # 米迦勒的序列帧
    "arcfx": dict(life=12, frames=("glyph", "arc", 6, 2)),
    "arcffx": dict(life=12, frames=("glyph", "arcf", 6, 2)),
    "arcwfx": dict(life=12, frames=("glyph", "arcw", 6, 2)),
    "burstf": dict(life=16, frames=("glyph", "burstf", 8, 2)),
    "wings": dict(life=14, frames=("glyph", "wings", 6, 2)),
    "fburn": dict(life=12, frames=("glyph", "fburn", 6, 2)),
    "xslash": dict(life=12, frames=("glyph", "xslash", 6, 2)),
    "smoke": dict(life=12, frames=("glyph", "smoke", 6, 2)),
    "tongue": dict(life=8, frames=("glyph", "tongue", 4, 2)),
    "drop": dict(life=8, frames=("glyph", "drop", 4, 2)),
    "eyeopen": dict(life=14, frames=("glyph", "eye", 6, 2)),
    "mshock": dict(life=16, frames=("item", MNS + "/shock", 8, 2)),
    "mshockh": dict(life=16, frames=("item", MNS + "/shockh", 8, 2)),
    # 火簇常常一次几十个：每 3 刻才换一帧（一次 data modify），省一半开销（2026-11-18 探针：圣哉段 4.8 ms/刻）
    "fireloop": dict(life=60, loop=("glyph", "fire", 8, 3)),
    "firehloop": dict(life=60, loop=("glyph", "fireh", 8, 3)),
    "columnloop": dict(life=24, loop=("glyph", "column", 6, 2)),
    "haloloop": dict(life=120, loop=("glyph", "halo", 6, 3)),
    "gazeloop": dict(life=40, loop=("glyph", "gaze", 4, 3)),
    "meteorloop": dict(life=16, loop=("glyph", "meteor", 4, 2)),
    "doverise": dict(life=60, loop=("glyph", "dove", 8, 2), steps=[(58, 56, "translation:[0f,12f,0f]")]),
    "rayup": dict(life=30, steps=[(29, 4, "scale:[%gf,%gf,%gf]" % (3.2, 18, 3.2)), (10, 10, "scale:[0.01f,18f,0.01f]")]),
    # 死亡时头顶的光环：小一些、高一些，别挡住跪着烧翼的他
    "halodeath": dict(life=120, loop=("glyph", "halo", 6, 3), steps=[(118, 10, "scale:[3.2f,3.2f,3.2f]"),
                                                                (10, 10, "scale:[0.01f,0.01f,0.01f]")]),
    "haloin": dict(life=120, loop=("glyph", "halo", 6, 3), steps=[(118, 8, "scale:[7.5f,7.5f,7.5f]"),
                                                             (8, 8, "scale:[0.01f,0.01f,0.01f]")]),
}
for _i, _v in enumerate(FLY):
    KINDS["fly%d" % _i] = fly(*_v)

fx = MichaelFx(fn=B, tag="rpg.mkb.fx", life="rpg_mk_life", kind="rpg_mk_kd", writer=w, arts=[(mart, mart.FONT)], kinds=KINDS)


def mglyph(name, blocks, pos="~ ~ ~", kind=None, life=None, billboard="center", trans=(0, 0, 0), start=None, tags=(),
           lrot=None, view=3, frame=0):
    """A Michael glyph (baked colours)."""
    return fx.glyph(name, blocks, "white", pos=pos, kind=kind, life=life, billboard=billboard, trans=trans, start=start,
                    tags=tags, lrot=lrot, view=view, frame=frame)


def mdecal(name, size, pos="~ ~0.06 ~", kind=None, life=None, tags=(), yaw=None):
    return fx.decal(name, size, 0xFFFFFF, pos=pos, kind=kind, life=life, tags=tags, yaw=yaw)


def godray(pos="~ ~ ~", hot=False):
    """A god ray standing on pos: the original light shaft grown up, then thinned out (vertical billboard).
    The ray glyph is 32 px: scale k makes it k * 0.8 blocks; 18 -> 14.4 blocks tall, 3.2 -> 2.6 wide."""
    return mglyph("rayf" if hot else "ray", 1.0, pos=pos, kind="rayup", billboard="vertical",
                  start=(0.6, 18, 0.6), trans=(0, 7.0, 0))


def impact(pos="~ ~1 ~", hot=False, size=4.0):
    """A hit: the ring burst flipbook and a star glint."""
    return (mglyph("burstf" if hot else "burst", size, pos=pos, kind="burstf" if hot else "burst")
            + mglyph("starf" if hot else "star", size * 0.5, pos=pos, kind="twinkle", start=0.01, frame=2))


def wingburst(pos="~ ~1.6 ~", size=6.0):
    return mglyph("wings", size, pos=pos, kind="wings")


def feathers_out(pos="~ ~1.4 ~", n=8):
    """Burning feathers flung outward in n directions (each a fburn flipbook sliding out by interpolation)."""
    out = []
    for i in range(0, 8, 8 // n):
        out += mglyph("fburn", 1.4, pos=pos, kind="fly%d" % i)
    return out


def flame_at(pos="~ ~ ~", size=2.0, life=40, hot=True):
    """A standing flame (fire flipbook loop) on the ground."""
    return mglyph("fire" if hot else "fireh", size, pos=pos, kind="fireloop" if hot else "firehloop", life=life,
                  billboard="vertical", trans=(0, size * 0.5 - 0.1, 0))


def fire_block(pos="~ ~ ~", life=60):
    """A vanilla fire block as a block_display (grows in, burns, sinks), random yaw; never a real fire block."""
    return ['summon minecraft:block_display %s {Tags:["%s","%s"],block_state:{Name:"minecraft:fire"},'
            'brightness:{sky:15,block:15},view_range:2f,transformation:{translation:[-0.05f,0f,-0.05f],'
            'left_rotation:[0f,0f,0f,1f],scale:[0.1f,0.1f,0.1f],right_rotation:[0f,0f,0f,1f]}}' % (pos, fx.tag, fx.new),
            "execute as @e[tag=%s,limit=1] store result entity @s Rotation[0] float 1 run random value 0..359" % fx.new
            ] + fx.born(life, "fireblk")


def smoke_puff(pos="~ ~1 ~", size=2.2):
    return mglyph("smoke", size, pos=pos, kind="smoke")


# A text_display laid flat face-up, the glyph's top toward the entity's facing: -90 deg about X (face up,
# top to local -z), then 180 deg about Y (top to local +z).  Measured in the client 2026-11-18: a text_display at
# yaw phi shows local +z toward its facing; an item_display is the other way round (the sector decal needed +180).
FLAT = "[0f,0.70711f,0.70711f,0f]"


def flat_glyph(name, blocks, pos="~ ~0.3 ~", kind=None, life=None, yaw="~"):
    """A glyph lying on the ground plane (visible from above), turned to `yaw` (default: the executor's)."""
    return (fx.glyph(name, blocks, "white", pos=pos, kind=kind, life=life, billboard="fixed", lrot=FLAT, born_now=False, view=3)
            + ["tp @e[tag=%s,limit=1] %s %s 0" % (NEW, pos, yaw)] + fx.born(life, kind))


def full_title(name, frame, times, who="@a[distance=..%d]" % (ARENA + 8)):
    """A full-screen title from a Michael glyph (two copies side by side)."""
    txt = json.dumps({"text": mart.full_text(name, frame), "font": mart.FONT, "color": "white"}, ensure_ascii=False)
    return ["title %s times %d %d %d" % ((who,) + times), "title %s title %s" % (who, txt)]


NEW = "rpg.mkb.fxnew"
FIRE_DUST = "minecraft:dust_color_transition{from_color:[1.0,0.5,0.32],to_color:[1.0,0.2,0.0],scale:1.1}"
WHITE_DUST = "minecraft:dust{color:[1.0,0.96,0.93],scale:0.9}"
ASH_DUST = "minecraft:dust{color:[0.12,0.1,0.1],scale:1.0}"


def say(text, gloss=None, name=None, stage=1):
    """〖天使长 米迦勒〗 / 〖炽天使 米迦勒〗 播报（ART-STYLE.md §12 的格式）。"""
    title = STAGES[stage][0]
    parts = [ui.comp("〖", CORAL, True), ui.comp(title + " ", PEACH if stage == 1 else CORAL, True),
             ui.comp("米迦勒", WHITE if stage == 1 else FIRE, True), ui.comp("〗", CORAL, True)]
    if gloss:
        parts.append(ui.comp(" " + ui.fraktur(gloss), ui.BROADCAST_GLOSS))
    parts.append(ui.comp(ui.GAP, ui.BROADCAST_BODY))
    if name:
        parts.append(ui.comp(name, ui.BROADCAST_NAME))
    parts.append(ui.comp(text, ui.BROADCAST_BODY))
    # 序章模式里不播中文播报：台词由序章的双语字幕负责
    return "execute unless score #pro %s matches 1 run tellraw @a[distance=..%d] %s" % (O, BAR_RANGE, ui.row(*parts))


def say_s(text, gloss=None, name=None):
    return ["execute if score @s %s matches 1 run %s" % (O, say(text, gloss, name, 1)),
            "execute if score @s %s matches 2.. run %s" % (O, say(text, gloss, name, 2))]


def bar_title(stage, step=art.STEPS):
    return "bossbar set %s name %s" % (BAR, json.dumps(
        {"text": art.bar_text(stage, step), "font": art.FONT}, ensure_ascii=True, separators=(",", ":")))


def anim(clip):
    return "function %s/anim/enter/%s" % (LOOK, clip)


def wanim(clip):
    return "function %s/anim/enter/%s" % (WLOOK, clip)


def start(name, busy):
    return ["scoreboard players set @s rpg_mk_sk %d" % SKILL_ID[name], "scoreboard players set @s rpg_mk_t 0",
            "scoreboard players set @s rpg_mk_busy %d" % busy]


def face(r=BASIC_RANGE):
    return "execute facing entity @p[distance=..%s,%s] feet run tp @s ~ ~ ~ ~ 0" % (r, SURV)


def at(t, cmd):
    return "execute if score @s rpg_mk_t matches %d run %s" % (t, cmd)


def at_c(t, cmd):
    return "execute if score @s rpg_mk_c matches %d run %s" % (t, cmd)


def span(t0, t1, cmd):
    return "execute if score @s rpg_mk_t matches %d..%d run %s" % (t0, t1, cmd)


def hurt_tagged(dmg, flame=False, by=True):
    src = " by @e[%s,limit=1]" % UNIT if by else ""
    out = ["execute as @a[tag=rpg.mkb.hit] run damage @s %d minecraft:mob_attack%s" % (dmg, src)]
    if flame:
        out.append("execute if score #stage %s matches 2 as @a[tag=rpg.mkb.hit] run function %s/flame/add" % (O, B))
    return out + ["tag @a remove rpg.mkb.hit"]


def tag_near(r, pos="~ ~ ~"):
    return "execute positioned %s run tag @a[distance=..%s,%s] add rpg.mkb.hit" % (pos, r, SURV)


def line(kind, steps):
    return ["scoreboard players set #d %s %d" % (O, steps), "function %s/line/%s" % (B, kind)]


def every(n, score="@s rpg_mk_t"):
    who, obj = score.split()
    return ["scoreboard players operation #m %s = %s %s" % (O, who, obj),
            "scoreboard players set #k %s %d" % (O, n),
            "scoreboard players operation #m %s %%= #k %s" % (O, O)]


def beam(color, size, trans, tags=(), tp=1):
    """A line.  Flat ones (ground telegraphs) are Michael's lane strip; standing ones stay the beam box."""
    if size[1] <= 0.05:
        lane = "lane_r" if color == FIRE_D else ("lane_f" if color in HOT else "lane_h")
        return [fx.disp("%s/%s" % (MNS, lane), pos="~ ~ ~", scale=(size[0] * 1.6, 1, size[2]), color=0xFFFFFF, trans=trans,
                        tags=tags, tp=tp),
                "tp @e[tag=%s,limit=1] ~ ~ ~ ~ ~" % NEW]
    return [fx.disp("%s/core" % MNS, pos="~ ~ ~", scale=size, color=0xFFFFFF, trans=trans, tags=tags, tp=tp),
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


def ground(cmd, pos="~ ~ ~"):
    """Run cmd only where a carrier can stand (two free blocks over a solid one)."""
    return ("execute positioned %s if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable "
            "unless block ~ ~-0.5 ~ #minecraft:replaceable run %s" % (pos, cmd))


def aimed(cmd):
    """Run cmd at the aim point: the nearest player while a watcher still sees them, otherwise where they were ~1 s ago."""
    return ["execute if score #w %s matches 1.. at @p[distance=..%d,%s] run %s" % (O, ARENA, SURV, cmd),
            "execute if score #w %s matches ..0 at @e[%s] run %s" % (O, LAG, cmd)]


def solid(ticks):
    return ["scoreboard players set @s rpg_mk_so %d" % ticks, "function %s/solid/on" % B]


def light_pillar(color, tags=()):
    """A shaft of light: the original god ray (glyph) around a thin white core, end_rod motes rising.
    The first line is the core beam (callers that re-place one pillar use [0])."""
    return ([fx.disp("%s/core" % MNS, pos="~ ~ ~", scale=(0.1, 28, 0.1), color=0xFFFFFF, trans=(0, 14, 0), tags=tags)]
            + fx.born(kind="pillarcore")
            + godray("~ ~ ~", color in HOT)
            + ["particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force"])


SPIKE = (["particle minecraft:block{block_state:\"minecraft:bone_block\"} ~ ~0.5 ~ 0.2 0.4 0.2 0 6",
          "particle %s ~ ~0.7 ~ 0.15 0.5 0.15 0 3" % FIRE_DUST]
         + [fx.disp("beam", pos="~ ~ ~", scale=(0.05, 0.2, 0.05), color=BONE_I, trans=(0, 0.9, 0), tp=0)] + fx.born(kind="spike"))
