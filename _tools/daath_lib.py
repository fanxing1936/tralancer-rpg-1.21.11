# -*- coding: utf-8 -*-
"""达阿特试炼的共用常量与小工具（add_daath.py、daath_world.py、daath_frame.py、daath_moves.py、daath_ults.py）。

和前六场 Boss 不同，这里每个挑战者一块场地、一套状态：
  * 状态分数全记在载体身上（不用全局假玩家），场地之间隔 512 格，选择器都带 distance；
  * 载体每刻开头给自己的挑战者挂 rpg.dt.me、给自己挂 rpg.dt.it，结尾摘掉。
"""
import io
import json
import math
import os
import sys

import rpg_ui_style as ui
import add_daath_fx_art as dart
import add_michael_fx_art as mart
from boss_fx import Fx, flat_sc, sc
from display_mob import hook_tag, wf, wj

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "daath_ref")
DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
RP = sys.argv[2] if len(sys.argv) > 2 else "../resourcepack"
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "daath_fight")
B = "rpg:daath_fight"
LOOK = "rpg:daath"
O = "rpg_dt"
DIM = "rpg:daath"
SLOTS = 16
GAP = 512
FLOOR = 64                 # 人站的高度
R = 24                     # 场地半径
LAMP_R = 19.5              # 十盏灯的半径
POOL_R = 14.0              # 光落在地上的圆心半径
LIGHT_R = 6                # 光圈半径
UNIT = "type=minecraft:vindicator,tag=rpg.dtb"
ME = "@a[tag=rpg.dt.me,limit=1]"
NEAR = "tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative"
CENTER = "type=minecraft:marker,tag=rpg.dt.c,distance=..70,limit=1,sort=nearest"
GUARD = 'minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]'
SIL, WHITE, DARK, MID, LIGHTC = "#AAB4C3", "#FFFFFF", "#2A2E38", "#7C8593", "#FFF2A8"
SIL_I, WHITE_I, DARK_I = 0xAAB4C3, 0xFFFFFF, 0x2A2E38
DUST = "minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1}"
DUST_D = "minecraft:dust_color_transition{from_color:[0.29,0.31,0.36],to_color:[0.04,0.05,0.06],scale:1.3}"
INK = "minecraft:squid_ink"
DRIP = "minecraft:falling_dust{block_state:{Name:\"minecraft:black_concrete\"}}"
PILLAR_COL = {1: "#FF5A62", 2: "#62B8F0", 3: "#FFD85A"}
COUNT = [0]


def w(path, lines):
    COUNT[0] += 1
    # 宏行必须有变量，没有的去掉 $
    lines = [ln[1:] if ln.startswith("$") and "$(" not in ln else ln for ln in lines]
    wf(os.path.join(OUT, *path.split("/")) + ".mcfunction", lines)


fx = Fx(fn=B, tag="rpg.dt.fx", life="rpg_dt_life", kind="rpg_dt_kd", writer=w, arts=[(dart, dart.FONT), (mart, "rpg:michael_vfx")], kinds={
    "spinf": dict(extra=["tp @s ~ ~ ~ ~7 ~"]),
    "ringm": dict(life=12, steps=[(11, 10, flat_sc(6))]),
    "ringx": dict(life=16, steps=[(15, 14, flat_sc(14))]),
    "ringw": dict(life=34, steps=[(33, 32, flat_sc(50))]),
    "pillarfade": dict(life=24, steps=[(23, 3, sc((0.75, 28, 0.75))), (12, 12, sc((0.02, 28, 0.02)))]),
    "stabfade": dict(life=8, steps=[(6, 6, "scale:[0.01f,0.01f,4.2f]")]),
    "linefade": dict(life=12, steps=[(8, 8, "scale:[0.02f,0.02f,16f]")]),
    "shard": dict(life=30, steps=[(29, 28, "translation:[0f,2.6f,0f],scale:[0.01f,0.01f,0.01f]")]),
    "inkup": dict(life=12, steps=[(11, 4, "scale:[0.9f,3f,0.9f]"), (6, 6, "scale:[0.05f,0.05f,0.05f]")]),
    "fadeup": dict(life=40, steps=[(39, 38, "translation:[0f,1.2f,0f]")]),
    "tile": dict(life=26, steps=[(25, 6, "left_rotation:[0.7071f,0f,0f,0.7071f]"), (10, 8, "left_rotation:[0f,0f,0f,1f]")]),
    "ghost": dict(life=10, steps=[(9, 8, sc(0.01))]),
    # Codex 的序列帧
    "kslash": dict(life=12, frames=("glyph", "d_slash", 6, 2)), "kaxe": dict(life=12, frames=("glyph", "d_axe", 6, 2)), "kthrust": dict(life=12, frames=("glyph", "d_thrust", 6, 2)),
    "kclash": dict(life=18, frames=("glyph", "d_clash", 6, 3)), "kshards": dict(life=18, frames=("glyph", "d_shards", 6, 3)), "kink": dict(life=18, frames=("glyph", "d_ink", 6, 3)),
    "ksplash": dict(life=18, frames=("glyph", "d_splash", 6, 3)), "kgrab": dict(life=18, frames=("glyph", "d_grab", 6, 3)), "keye": dict(life=24, frames=("glyph", "d_eye", 6, 4)),
    "ksmash": dict(life=18, frames=("item", "rpg:daath_fx/smash", 6, 3)), "kchain": dict(life=40, loop=("glyph", "d_chain", 4, 3)), "kmotes": dict(life=40, loop=("glyph", "d_motes", 4, 4)),
    "kshard": dict(life=32, loop=("glyph", "d_shard", 4, 3), steps=[(31, 30, "translation:[0f,2.4f,0f]")]),
})
NEW = "rpg.dt.fxnew"


def at(t, cmd):
    return "execute if score @s rpg_dt_t matches %d run %s" % (t, cmd)


def span(a, b, cmd):
    return "execute if score @s rpg_dt_t matches %d..%d run %s" % (a, b, cmd)


def every(n, score="rpg_dt_t"):
    """接在后面的 execute 用 #m 判断：#m = 分数 % n"""
    return ["scoreboard players operation #m %s = @s %s" % (O, score), "scoreboard players set #k %s %d" % (O, n),
            "scoreboard players operation #m %s %%= #k %s" % (O, O)]


def anim(clip):
    return "function %s/anim/enter/%s" % (LOOK, clip)


def face(extra=""):
    """只转水平（挑战者在 80 格内）。"""
    return "execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~"


def step(d):
    """往前挪 d 格，不出水面边缘（as/at 载体）。"""
    return "execute rotated ~ 0 positioned ^ ^ ^%s if entity @e[%s,distance=..%s] run tp @s ~ ~ ~" % (d, "type=minecraft:marker,tag=rpg.dt.c", R - 1)


def snd(ev, vol=1.0, pitch=1.0, rng=48, pos="~ ~ ~", src="hostile"):
    ev = ev if ":" in ev else "minecraft:" + ev
    return "playsound %s %s @a[distance=..%d] %s %g %g" % (ev, src, rng, pos, vol, pitch)


def ring(p, r, n, y=0.15, phase=0.0, force=True):
    out = []
    for i in range(n):
        a = 2 * math.pi * (i + phase) / n
        out.append("particle %s ~%.2f ~%.2f ~%.2f 0 0 0 0 1%s" % (p, r * math.cos(a), y, r * math.sin(a), " force" if force else ""))
    return out


def wave(p, n, speed, y=0.2, r0=0.4, up=0.0):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        out.append("particle %s ~%.2f ~%.2f ~%.2f %.3f %.3f %.3f %g 0 force" % (p, r0 * c, y, r0 * s, c, up, s, speed))
    return out


def along(p, length, stepd, y=0.2, spread=0.15, n=1, speed=0.0):
    out, d = [], stepd
    while d <= length + 1e-6:
        out.append("particle %s ^ ^%.2f ^%.2f %s %s %s %g %d force" % (p, y, d, spread, spread * 0.5, spread, speed, n))
        d += stepd
    return out


def beam(color, size, trans, tags=(), tp=1):
    return [fx.disp("beam", pos="~ ~ ~", scale=size, color=color, trans=trans, tags=tags, tp=tp), "tp @e[tag=%s,limit=1] ~ ~ ~ ~ ~" % NEW]


def light_pillar(color):
    return ([fx.disp("beam", pos="~ ~ ~", scale=(0.2, 28, 0.2), color=color, trans=(0, 14, 0))] + fx.born(kind="pillarfade")
            + ["particle minecraft:end_rod ~ ~5 ~ 0.15 5 0.15 0.01 30 force"])


def seq(name, size, pos="~ ~1.2 ~", billboard="center", trans=(0, 0, 0)):
    """Codex 的一套序列帧（名字去掉 d_ 前缀）。"""
    return fx.glyph("d_" + name, size, WHITE, pos=pos, kind="k" + name, billboard=billboard, trans=trans)


def dec(name, size, pos="~ ~0.06 ~", life=30, kind=None, color=WHITE, yaw=None, tags=()):
    """Codex 的地面贴花。"""
    return fx.decal("rpg:daath_fx/" + name, size, color, pos=pos, life=life, kind=kind, yaw=yaw, tags=tags)


def shock(color=SIL, size=6):
    return fx.decal("shock_0", size, color, kind="shock")


def ripple(size=1.0, kind="ringm"):
    return fx.decal("ring", size, MID, pos="~ ~0.06 ~", kind=kind)


def burst(pos="~ ~1.2 ~", size=2.4, color=SIL):
    return seq("clash", size * 1.15, pos)


def shards(n=8, y=1.2, rad=0.6):
    """碎镜片：几片小三角往上飘散。"""
    out = seq("shards", 2.6, "~ ~%.2f ~" % y)
    for i in range(n):
        a = 2 * math.pi * i / n
        out += fx.glyph("d_shard", 0.45 + 0.15 * (i % 3), WHITE, pos="~%.2f ~%.2f ~%.2f" % (rad * math.cos(a), y + 0.25 * (i % 3), rad * math.sin(a)), frame=i % 4, kind="kshard")
    return out


def voice():
    """配音 take：daath_ref/vo/picks.json 里挑好的，没有就只有字幕。"""
    p = os.path.join(REF, "vo", "picks.json")
    if not os.path.isfile(p):
        return {}
    pk = json.load(io.open(p, encoding="utf-8"))
    out = {}
    for k, v in pk.items():
        f = os.path.join(REF, "vo", "takes", "%s_%d.ogg" % (k, v))
        if os.path.isfile(f):
            out[k] = f
    return out


LINES = {x["id"]: x for x in json.load(io.open(os.path.join(REF, "lines.json"), encoding="utf-8"))["lines"]}
VOICE = voice()


def lang_key(lid):
    return "rpg.daath.%s" % lid.lower()


def line(lid, stage=1):
    """影子说一句（as/at 载体）：中文一行，英文一行，有配音就放。"""
    x = LINES[lid]
    who = [ui.comp("〖", DARK if False else MID, True), ui.comp("影", SIL, True) if stage == 1 else {"selector": ME, "color": WHITE, "bold": True, "italic": False},
           ui.comp("〗", MID, True), ui.comp(ui.GAP, ui.BROADCAST_BODY)]
    out = ["tellraw %s %s" % (ME, ui.row(*(who + [ui.comp(x["zh"], ui.BROADCAST_NAME), ui.comp("　" + x["en"], ui.BROADCAST_GLOSS, False, True)])))]
    if lid in VOICE:
        out.append("execute as %s at @s run playsound rpg:vo.daath.%s voice @s ~ ~ ~ 1 1 1" % (ME, lid.lower()))
    return out


def lines_at(t, lid, stage=1):
    return [at(t, c) for c in line(lid, stage)]


def title(text, gloss, color=SIL):
    return ["title %s times 5 35 12" % ME, "title %s subtitle %s" % (ME, ui.row(ui.comp(ui.fraktur(gloss), ui.BROADCAST_GLOSS))),
            "title %s title %s" % (ME, ui.row(ui.comp(text, color, True)))]


def msg(parts, to="@s"):
    return "tellraw %s %s" % (to, ui.row(*([ui.comp("[原质] ", "#C9A646", True)] + parts)))


def txt(s, c="#E6DFCF", b=False):
    return ui.comp(s, c, b)


def dummy(tags):
    """一个站着不动的黑影（六块身体，没有眼睛），summon 在它脚下 +2 格处。"""
    idle = json.load(io.open(os.path.join(REF, "idle.json"), encoding="utf-8"))
    out = []
    for part, tr in idle.items():
        out.append('summon minecraft:item_display ~ ~ ~ {Tags:[%s],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:daath/%s"}},'
                   'item_display:"none",brightness:{block:0,sky:0},teleport_duration:3,view_range:2f,transformation:%s}'
                   % (",".join('"%s"' % x for x in tags), "head_blank" if part == "head" else part, tr))
    return out
