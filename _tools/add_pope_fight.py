# -*- coding: utf-8 -*-
"""教皇战 (docs/POPE-DESIGN.md).  Three stages in one arena: the Holy Guards,
the Pope, then the Heart of Ender.  Started by command only.

Functions live under rpg:pope_fight/, because rpg:pope/ belongs to the model
generator (add_pope_model.py) and display_mob.py clears parts of it.

The Heart of Ender's rig rides a Marker armor stand, which cannot be hit.  So
the Heart is two entities: an invisible scaled vindicator takes the hits and
holds the health and the position, and the rig is teleported onto it.

Shapes are display entities and energy is particles.  A display entity gets
one `data merge` per move and the client interpolates: `data ... entity`
serialises the whole entity, so nothing here animates by rewriting per tick.
Light is a text_display glyph, ground decals and solid things are item_display:
add_pope_fx_art.py says why.
"""

import math
import os
import sys

import add_pope_fx_art as art
import rpg_ui_style as ui
import rpg_vfx as vfx
from add_heart_of_ender import GROUND_Y, MODEL_SCALE
from display_mob import hook_tag, wf

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "pope_fight")
F = "rpg:pope_fight"
O = "rpg_pf"
LIFE = "rpg_pf_l"

SURVIVORS = "gamemode=!spectator,gamemode=!creative"
CENTER = "type=minecraft:marker,tag=rpg.pf.center,limit=1"
UNIT = "type=minecraft:vindicator,tag=rpg.pf.unit"
SAC = "type=minecraft:vindicator,tag=rpg.pf.sac"
BOSS = "type=minecraft:vindicator,tag=rpg.pf.boss,limit=1"
HEART = "type=minecraft:vindicator,tag=rpg.pf.heart,limit=1"
RIG = "type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1"
TARGET = "tag=rpg.pf.tgt,limit=1"
FX = "tag=rpg.pope.fx"
NEW = "tag=rpg.pf.new"
GUARD_REMOVE = "rpg:tower_guard/ai/remove"

ARENA = 40              # players further than this have left the fight
BAR_RANGE = 48
EMPTY_SECONDS = 60
GUARDS = 4
WAVE_SIZE = 2
UNIT_CAP = 4
POPE_HEALTH = 1000
# the pack's own boss music, one piece per stage: sound event, length in ticks
BGM = [("boss3", 2000), ("boss2", 1876), ("boss1", 2943)]
BGM_SOURCE = "record"   # many players keep the music slider at 0 to mute the vanilla tracks
WAVE_LINES = (750, 500, 250)    # the first wave comes when he appears
TRANSFORM_AT = 40       # the Heart takes over a little before zero

BLAST_DAMAGE = 6
BLAST_SPEED = 0.7
BLAST_LIFE = 36         # 25 blocks
BLAST_SPREAD = 20       # degrees
MELEE_DAMAGE = 8
BLOOD_HEAL = 60
RECLAIM_TICKS = 300
BLOOD_REACH = 24

# ticks, from the model report: the release frame and the length of each clip
ATTACK_FIRE, ATTACK_END = 10, 25
SUMMON_FIRE, SUMMON_END = 13, 40
CAST_FIRE, CAST_END = 18, 50
TELEPORT = 18
APPEAR_END = 36
BREATHER = 30           # between two skills
PART_VIEW = "1.5f"      # view_range of the rig's parts, 0 hides them

# ^left ^up ^forward of the staff head at the release frame, from sockets.json
ATTACK_TIP = "^-0.05 ^0.09 ^2.22"
CAST_TIP = "^0.43 ^2.90 ^0.57"
COOLDOWNS = dict(tp=120, blood=400, reclaim=1200, enhance=400)

TRANSFORM_BURST = 140   # whirlwind is 7 s and converges on its last frame
TRANSFORM_END = 150
SPIRAL_FROM = 100
SKILLS = dict(attack=1, teleport=2, summon=3, blood=4, reclaim=5, enhance=6, appear=7, melee=8, ring=9, judge=10,
              basic=11, seals=12, doom=13)
# plain attacks: a quick bolt, or the staff when cornered.  Skills come every few of these.
BASIC_SPEED = 1.2
BASIC_GAP = 8
BASICS_PER_SKILL = 3
MELEE_REACH = 3.5
# ultimates: on a health line, or when the clock runs out, whichever is first
ULT_EVERY = 900
POPE_ULT_LINES = (625, 375)     # clear of the wave lines
SEAL_COUNT, SEAL_RING, SEAL_HEIGHT = 7, 7, 5
SEAL_FIRST, SEAL_GAP = 30, 18
SEAL_WARN, SEAL_ACTIVE = 22, 12
SEAL_REACH, SEAL_DAMAGE = 40, 14
SEALS_END = SEAL_FIRST + SEAL_COUNT * SEAL_GAP + SEAL_WARN + SEAL_ACTIVE
DOOM_TICKS, DOOM_RADIUS, DOOM_DAMAGE, DOOM_REST = 110, 30, 30, 70
REFUGE_RING, REFUGE_RADIUS = 13, 3.5
RING_SHOTS = 8          # two rings, the second turned half a gap
RING_DELAY = 8
JUDGE_DAMAGE = 12
JUDGE_RADIUS = 2.5
JUDGE_STRIKE = 14       # life left on the seal when the pillar lands: 26 ticks of warning

# the Heart of Ender
HEART_HEALTH = 1000
HITBOX_SCALE = 3.3      # a vindicator this size is 2 wide and 6.4 tall, the rig's body
SHELL_KEEP = 3          # tenths of a hit that get through the shell
DEATH_AT = 5
HEART_SPEED = 0.12      # blocks per tick
HEART_TURN = 3          # degrees per tick
STOP_NEAR, WALK_FAR = 4, 6
SINK_BEYOND = 20        # a target further than this gets the Heart coming up under them
HEART_BREATHER = 100    # crawling between two skills
BLEND = 6               # ticks to ease from one pose into the next clip
HEART_SKILLS = dict(rise=1, mortar=2, cross=3, sink=4, nova=5, vent=6, bite=7, spit=8, gaze=9,
                    faces=10, collapse=11, cata=12)
# plain attacks while it crawls.  It has no clip for them: the mortar clip from
# just before the mouth opens, cut short, reads as a snap.
BASIC_EVERY = 30
OPEN_FROM, OPEN_BLEND = 20, 4
BITE_HIT, BITE_END = 12, 14
BITE_NEAR, BITE_AHEAD, BITE_RADIUS, BITE_DAMAGE = 8, 4, 4.5, 8
SPIT_REACH, SPIT_SPEED, SPIT_LIFE, SPIT_DAMAGE = 26, 0.9, 30, 6
# ultimates, and the Arch-Visage: one run of its only clip is 98 ticks and it is
# fully underground by 74.  Mouth open 0.8 to 3.04 s.
HEART_ULT_LINES = (750, 500, 250)
HEART_ULT_EVERY = 1200
FACE_LIFE = 76
FACE_OPEN, FACE_THICK, FACE_CLOSE, FACE_GONE = 60, 50, 18, 14    # life left on the stand
FACE_REACH, FACE_DAMAGE, FACE_TURN = 24, 8, 1.5
FACE_SPIN = 1.2
GAZE_RING = 7
RING_FACES, RING_RADIUS = 6, 14
AV_MOUTH = "^1.31 ^1.97 ^3.00"  # sockets.json, while the mouth is open, at model_scale 3
FACE = "type=minecraft:armor_stand,tag=rpg.pf.face"
COLLAPSE_TICKS, COLLAPSE_RADIUS, COLLAPSE_DAMAGE, COLLAPSE_REST = 100, 15, 30, 70
NOVA_LIFE, NOVA_RADIUS, NOVA_DAMAGE = 40, 22, 10
NOVA_GAP = 22           # the second ring follows this many ticks later
VENT_COUNT, VENT_GAP, VENT_LIFE = 7, 5, 16
VENT_DAMAGE, VENT_RADIUS = 10, 2

# clip timing, from the model report: mouth open 1.2 to 2.4 s, the figure's
# Fourside 1 to 3 s, sink 2 s, rise 2.4 s, death 4 s
SHELL_FIRST = BLEND + 24
SHELL_GAP = 2
CLIP_END = BLEND + 80
SINK_END, SINK_WARN = BLEND + 40, 20
RISE_HIT, RISE_END = 24, 48
DEATH_BURST = 80
DEATH_END = 112

MARK_LIFE = 30          # warning on the ground before a shell lands
FALL_TICKS, FALL_STEP = 15, 1.2
MARK_RADIUS = 2.5
MARK_DAMAGE = 10
RISE_RADIUS = 4
RISE_DAMAGE = 14
BEAM_DAMAGE = 12
BEAM_REACH = 24
BEAM_STEP = 2
BEAM_LIFE = 60
BEAM_ACTIVE = 40        # the last ticks of its life, the first ones are the warning
BEAM_SPIN = 1.5         # degrees per tick: 60 degrees in all, so a third of each quarter is safe

# damage before the shell takes its 70%.  The contract skills are a percentage
# of max health with an execute line; on the Heart that would end the fight.
COVENANT_DAMAGE = dict(new=120, old=100, field=80, judgment=100)

# Rest offsets from the model report: mouth during `mortar`, the figure during
# `cross_beam`.  Model space (+x, up, -z forward) to ^left ^up ^forward blocks.
TO_BLOCKS = MODEL_SCALE / 16.0


def local(x, y, z):
    return "^%.2f ^%.2f ^%.2f" % (-x * TO_BLOCKS, (y - GROUND_Y) * TO_BLOCKS, -z * TO_BLOCKS)


MOUTH = local(5.6, 29.1, -5.7)
FIGURE = local(0.17, 5.85, 2.53)

SHELL_MODEL = "heart_of_ender/shell_head"
PILLAR_HEIGHT = 36
SEAL_LIFE, SEAL_SIZE, SEAL_SMALL = 40, 6, 3
BLAST_SIZE = 1.1
APPEAR_FX = 60
HALO_SIZE = 5.5
POP_LIFE = 10
FLIP_LIFE = 16
SLASH_LIFE = 12
VORTEX_WIDTH, VORTEX_HEIGHT = 7, 12
NOVA_STEP = 3
CHAIN_LIFE, CHAIN_WIDE, CHAIN_TIGHT = 40, 3.2, 1.3
LINE_WIDTH = 0.07
CHUNK_SIZE = 0.9
HOLY = ui.hex_of(ui.HOLY)
VOID = ui.hex_of(ui.RITUAL)


def dust_rgb(hexcolour):
    h = hexcolour.lstrip("#")
    return "[%.3ff,%.3ff,%.3ff]" % tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


HOLY_DUST = "dust{color:%s,scale:1.0}" % dust_rgb(HOLY)
HOLY_DUST_BIG = "dust{color:%s,scale:1.6}" % dust_rgb(ui.hex_of(ui.HOLY_LIGHT))
HOLY_FLASH = vfx.flash(ui.HOLY_LIGHT)
VOID_DUST = "dust{color:%s,scale:1.0}" % dust_rgb(VOID)
VOID_DUST_BIG = "dust{color:%s,scale:1.6}" % dust_rgb(VOID)
VOID_FLASH = vfx.flash(ui.RITUAL)


def w(path, lines):
    wf(os.path.join(OUT, *path.split("/")) + ".mcfunction", lines)


def line_of(text, who="教皇", gloss=False, name=None):
    """A broadcast (ART-STYLE.md §12): bold tag, blackletter gloss on the lines
    that carry the fight, two spaces, body.  polish_ui skips a tag already in 〖〗."""
    colour, english = ui.BOSS_VOICES[who]
    parts = [ui.comp("%s%s%s" % (ui.BRACKETS[0], who, ui.BRACKETS[1]), colour, True)]
    if gloss:
        parts.append(ui.comp(" " + ui.fraktur(english), ui.BROADCAST_GLOSS))
    parts.append(ui.comp(ui.GAP, ui.BROADCAST_BODY))
    if name:
        parts.append(ui.comp(name, ui.BROADCAST_NAME))
    parts.append(ui.comp(text, ui.BROADCAST_BODY))
    return ui.row(*parts)


def say(text, who="教皇", gloss=False, name=None):
    return "tellraw @a[distance=..%d] %s" % (BAR_RANGE, line_of(text, who, gloss, name))


def setv(name, value):
    return "scoreboard players set #%s %s %d" % (name, O, value)


def _tags(tags):
    return "".join(',"%s"' % t for t in tags)


def xf(q=(0, 0, 0, 1), t=(0, 0, 0), s=(1, 1, 1)):
    return ("left_rotation:[%gf,%gf,%gf,%gf],right_rotation:[0f,0f,0f,1f],"
            "translation:[%gf,%gf,%gf],scale:[%gf,%gf,%gf]" % (tuple(q) + tuple(t) + tuple(s)))


def sized(glyph, width, height):
    """Scale that makes a glyph this many blocks wide and high."""
    _, w, h = art.GLYPHS[glyph]
    return (round(width / (w * art.TEXT_UNIT), 4), round(height / (h * art.TEXT_UNIT), 4), 1)


def sprite(tags, glyph, transform, billboard="fixed", extra=""):
    """Unlit light: a text_display showing one glyph."""
    return ('summon minecraft:text_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new"%s],'
            'text:{text:"%s",font:"%s"},background:0,billboard:"%s",brightness:{sky:15,block:15},'
            'view_range:2f,%stransformation:{%s}}'
            % (_tags(tags), chr(art.GLYPHS[glyph][0]), art.FONT, billboard, extra, transform))


def prop(tags, model, transform, extra="", tint=None):
    """A decal or a solid thing: an item_display."""
    colours = ',"minecraft:custom_model_data":{colors:[%d]}' % tint if tint is not None else ""
    return ('summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new"%s],'
            'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:%s"%s}},'
            'brightness:{sky:15,block:15},view_range:2f,%stransformation:{%s}}'
            % (_tags(tags), model, colours, extra, transform))


def frame_lines(glyph):
    """Step a glyph through its frames: fonts do not animate, so the entity's text changes."""
    code = art.GLYPHS[glyph][0]
    count = art.SHEETS[glyph][1]
    return ['execute if score #f%d %s matches %d run data merge entity @s {text:{text:"%s",font:"%s"}}'
            % (count, O, i, chr(code + i), art.FONT) for i in range(count)]


def stepping(glyph):
    return "execute if score #go %s matches 1 run function %s/fx/frame_%s" % (O, F, glyph)


def bar_name(kind, step):
    return "bossbar set minecraft:pope name {\"text\":\"%s\",\"font\":\"%s\"}" % (art.bar_text(kind, step), art.FONT)


def merge(duration, scale):
    return ("data merge entity @s {start_interpolation:0,interpolation_duration:%d,"
            "transformation:{scale:[%gf,%gf,%gf]}}" % ((duration,) + tuple(scale)))


def move(condition, duration, scale):
    return "execute if score %s run %s" % (condition, merge(duration, scale))


def born(life):
    """Give what was just summoned here its lifetime."""
    return ["scoreboard players set @e[%s,distance=..1] %s %d" % (NEW, LIFE, life),
            "tag @e[%s,distance=..1] remove rpg.pf.new" % NEW]


def pp_sound(event, volume=1, pitch=1, radius=32):
    return "playsound rpg:pope.%s hostile @a[distance=..%d] ~ ~ ~ %g %g" % (event, radius, volume, pitch)


def he_sound(event, volume=1, pitch=1, radius=32):
    return "playsound rpg:heart_of_ender.%s hostile @a[distance=..%d] ~ ~ ~ %g %g" % (event, radius, volume, pitch)


def write_common():
    w("load", [
        "# 教皇战：计分板与专用血条。由 add_pope_fight.py 生成。",
        "scoreboard objectives add %s dummy" % O,
        "scoreboard objectives add %s dummy" % LIFE,
        "execute unless score #stage %s matches 0.. run %s" % (O, setv("stage", 0)),
        'bossbar add minecraft:pope {"text":""}',
        "bossbar set minecraft:pope color %s" % art.HIDDEN_BAR,
        "bossbar set minecraft:pope style progress",
        "scoreboard players set #fifty %s 50" % O,
        "scoreboard players set #keep %s %d" % (O, 10 - SHELL_KEEP),
        "scoreboard players set #ten %s 10" % O,
    ])
    hook_tag(DP, "load", F + "/load", False)
    hook_tag(DP, "tick", F + "/tick", True)
    w("tick", [
        "# 每刻入口：没开战时只有这一条分数判定。特效都活不过战斗，clear 会收走。",
        "execute unless score #stage %s matches 1.. run return 0" % O,
        "execute if entity @e[%s,limit=1] run function %s/fx/tick" % (FX, F),
        "execute as @e[%s] at @s run return run function %s/run" % (CENTER, F),
        "function %s/clear" % F,
    ])
    w("run", [
        "# 战场中心（as、at 标记）。",
        "scoreboard players add #t %s 1" % O,
        "scoreboard players add #s %s 1" % O,
        "execute if score #s %s matches 20.. run function %s/second" % (O, F),
        "scoreboard players remove #bgm %s 1" % O,
        "execute if score #bgm %s matches ..0 run function %s/bgm/again" % (O, F),
        "execute if score #stage %s matches 1 run return run function %s/stage1" % (O, F),
        "execute if score #stage %s matches 2 run return run function %s/stage2" % (O, F),
        "execute if score #stage %s matches 3 run return run function %s/stage3" % (O, F),
        "execute if score #stage %s matches 4 run return run function %s/stage4" % (O, F),
        "execute if score #stage %s matches 5 run return run function %s/stage5" % (O, F),
    ])
    w("second", [
        "# 每秒：刷新血条观众；战场没人满 %d 秒就判负清场。" % EMPTY_SECONDS,
        setv("s", 0),
        "bossbar set minecraft:pope players @a[distance=..%d]" % BAR_RANGE,
        "execute if entity @a[distance=..%d,gamemode=!spectator] run %s" % (ARENA, setv("e", 0)),
        "execute unless entity @a[distance=..%d,gamemode=!spectator] run scoreboard players add #e %s 1" % (ARENA, O),
        "execute if score #e %s matches %d.. run function %s/fail" % (O, EMPTY_SECONDS, F),
    ])
    # the bar is a picture of itself: swap it when the health crosses a step
    w("bar/hp", [
        "# #hp 换算成档位，变了才换图。",
        "scoreboard players operation #hud %s = #hp %s" % (O, O),
        "scoreboard players operation #hud %s /= #fifty %s" % (O, O),
        "execute if score #hud %s matches 0 if score #hp %s matches 1.. run %s" % (O, O, setv("hud", 1)),
        "execute unless score #hud %s = #hudl %s run function %s/bar/show" % (O, O, F),
    ])
    w("bar/show", [
        "scoreboard players operation #hudl %s = #hud %s" % (O, O),
        "execute if score #stage %s matches ..3 run return run function %s/bar/pope" % (O, F),
        "execute if score #weak %s matches 1 run return run function %s/bar/weak" % (O, F),
        "function %s/bar/heart" % F,
    ])
    for kind, (_, _, _, steps) in art.BANNERS.items():
        tail = ["scoreboard players operation #hudl %s = #hud %s" % (O, O)] if kind == "guard" else []
        w("bar/" + kind, tail + ["execute if score #hud %s matches %d run %s" % (O, i, bar_name(kind, i))
                                 for i in range(steps + 1)])

    # music: stereo, so it does not fade with distance; started on each player
    for i, (event, length) in enumerate(BGM):
        w("bgm/play_%d" % (i + 1), [
            "# 第 %d 段 Boss 音乐。先停掉原版配乐和上一段。" % (i + 1),
            "stopsound @a[distance=..%d] music" % BAR_RANGE,
        ] + ["stopsound @a[distance=..%d] %s minecraft:%s" % (BAR_RANGE, BGM_SOURCE, other) for other, _ in BGM] + [
            "execute as @a[distance=..%d] at @s run playsound minecraft:%s %s @s ~ ~ ~ 1 1" % (BAR_RANGE, event, BGM_SOURCE),
            setv("bgm", length), setv("track", i + 1),
        ])
    w("bgm/again", ["# 放完了：同一段再来一遍。"] + [
        "execute if score #track %s matches %d run return run function %s/bgm/play_%d" % (O, i + 1, F, i + 1)
        for i in range(len(BGM))])
    w("begin", [
        "# 开一场：记下战场中心。",
        "kill @e[type=minecraft:marker,tag=rpg.pf.center]",
        'summon minecraft:marker ~ ~ ~ {Tags:["rpg.pf.center"]}',
        setv("t", 0), setv("s", 0), setv("e", 0),
        "bossbar set minecraft:pope players @a[distance=..%d]" % BAR_RANGE,
        "bossbar set minecraft:pope color %s" % art.HIDDEN_BAR,
        "bossbar set minecraft:pope visible true",
    ])
    busy = "execute if score #stage %s matches 1.. run return run tellraw @s %s" % (
        O, line_of("已有一场教皇战；先用 /function rpg:pope_fight/clear 清场。"))
    w("summon", ["# 从圣卫战开始完整战斗。", busy, "function %s/begin" % F, "function %s/stage1_enter" % F])
    w("debug/boss1", ["# 调试：直接从 Boss 一阶段开始。", busy, "function %s/begin" % F, "function %s/stage2_enter" % F])
    w("debug/boss2", ["# 调试：直接从 Boss 二阶段开始。", busy, "function %s/begin" % F, "function %s/stage4_enter" % F])
    w("clear", [
        "# 清除教皇战的全部实体。",
        setv("stage", 0),
        "execute as @e[%s] run function %s" % (UNIT, GUARD_REMOVE),
        "execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss] run function %s/boss/remove" % F,
        "kill @e[type=minecraft:vindicator,tag=rpg.pf.heart]",
        "execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig] at @s run function rpg:heart_of_ender/internal/clear",
        "execute as @e[%s] at @s run function rpg:arch_visage/internal/clear" % FACE,
        "tag @a[tag=rpg.pf.tgt] remove rpg.pf.tgt",
        "kill @e[%s]" % FX,
    ] + ["stopsound @a %s minecraft:%s" % (BGM_SOURCE, event) for event, _ in BGM] + [
        "kill @e[type=minecraft:marker,tag=rpg.pf.center]",
        "bossbar set minecraft:pope players",
        "bossbar set minecraft:pope visible false",
    ])
    w("fail", [
        "# 战场空了：这一场作废，重新用指令召唤。",
        say("异端逃离了圣座。审判中止。", gloss=True),
        "function %s/clear" % F,
    ])


def write_fx():
    w("fx/tick", [
        "# 所有特效实体的寿命。动画每两刻走一帧：#go 为 1 的那一刻走。",
        "scoreboard players add #go %s 1" % O,
        "execute if score #go %s matches 2.. run function %s/fx/frame_clock" % (O, F),
        "execute as @e[%s] at @s run function %s/fx/one" % (FX, F),
    ])
    w("fx/frame_clock", [
        setv("go", 0),
        "scoreboard players add #f6 %s 1" % O,
        "execute if score #f6 %s matches 6.. run %s" % (O, setv("f6", 0)),
        "scoreboard players add #f8 %s 1" % O,
        "execute if score #f8 %s matches 8.. run %s" % (O, setv("f8", 0)),
    ])
    for glyph in art.SHEETS:
        w("fx/frame_" + glyph, frame_lines(glyph))
    w("fx/one", [
        "scoreboard players remove @s %s 1" % LIFE,
        "execute if entity @s[tag=rpg.pf.blast] run function %s/fx/blast" % F,
        "execute if entity @s[tag=rpg.pf.pillar] run function %s/fx/pillar_tick" % F,
        "execute if entity @s[tag=rpg.pf.seal] run function %s/fx/seal_tick" % F,
        "execute if entity @s[tag=rpg.pf.shard] run function %s/fx/shard_tick" % F,
        "execute if entity @s[tag=rpg.pf.up] run tp @s ^ ^ ^1.3",
        "execute if entity @s[tag=rpg.pf.fall] run function %s/fx/fall" % F,
        "execute if entity @s[tag=rpg.pf.mark] run function %s/fx/mark_tick" % F,
        "execute if entity @s[tag=rpg.pf.fill] run function %s/fx/fill_tick" % F,
        "execute if entity @s[tag=rpg.pf.beam] run function %s/fx/beam" % F,
        "execute if entity @s[tag=rpg.pf.flare] run function %s/fx/flare_tick" % F,
        "execute if entity @s[tag=rpg.pf.puddle] run function %s/fx/puddle_tick" % F,
        "execute if entity @s[tag=rpg.pf.pop] run function %s/fx/pop_tick" % F,
        "execute if entity @s[tag=rpg.pf.halo] run function %s/fx/halo_tick" % F,
        "execute if entity @s[tag=rpg.pf.chain] run function %s/fx/chain_tick" % F,
        "execute if entity @s[tag=rpg.pf.flip] run function %s/fx/flip_tick" % F,
        "execute if entity @s[tag=rpg.pf.vortex] run function %s/fx/vortex_tick" % F,
        "execute if entity @s[tag=rpg.pf.charge] run function %s/fx/charge_tick" % F,
        "execute if entity @s[tag=rpg.pf.judge] run function %s/fx/judge_tick" % F,
        "execute if entity @s[tag=rpg.pf.nova] run function %s/fx/nova_tick" % F,
        "execute if entity @s[tag=rpg.pf.vent] run function %s/fx/vent_tick" % F,
        "execute if entity @s[tag=rpg.pf.more] run function %s/fx/one_more" % F,
        "execute if score @s %s matches ..0 run kill @s" % LIFE,
    ])
    # behind one test, so most of the entities here pay for one tag check only
    w("fx/one_more", [
        "execute if entity @s[tag=rpg.pf.lance] run function %s/fx/lance_tick" % F,
        "execute if entity @s[tag=rpg.pf.sealed] run function %s/fx/sealed_tick" % F,
        "execute if entity @s[tag=rpg.pf.dooms] run function %s/fx/doom_tick" % F,
        "execute if entity @s[tag=rpg.pf.refuge] run function %s/fx/refuge_tick" % F,
        "execute if entity @s[tag=rpg.pf.refdisc] run function %s/fx/refdisc_tick" % F,
        "execute if entity @s[tag=rpg.pf.fbeam] run function %s/fx/fbeam_tick" % F,
        "execute if entity @s[tag=rpg.pf.pool] run function %s/fx/pool_tick" % F,
        "execute if entity @s[tag=rpg.pf.edge] run function %s/fx/edge_tick" % F,
        "execute if entity @s[tag=rpg.pf.gyre] run function %s/fx/gyre_tick" % F,
        "execute if entity @s[tag=rpg.pf.bolt] run function %s/fx/bolt" % F,
    ])
    write_more_fx()

    # light pillar: a thread of light that opens, holds, closes
    def column(width):
        return sized("column", width, PILLAR_HEIGHT)

    w("fx/pillar", [
        "# 落地光柱（at 落点）。",
        sprite(["rpg.pf.pillar"], "column", xf(t=(0, PILLAR_HEIGHT / 2.0, 0), s=column(0.1)), "vertical"),
    ] + born(30) + [
        "particle end_rod ~ ~0.5 ~ 0.4 2 0.4 0.03 24 normal",
        "particle %s ~ ~1 ~ 0.6 1 0.6 0.04 24 normal" % HOLY_DUST,
        "playsound minecraft:block.beacon.activate hostile @a[distance=..32] ~ ~ ~ 0.8 1.6",
    ])
    w("fx/pillar_tick", [
        stepping("column"),
        move("@s %s matches 29" % LIFE, 5, column(2.6)),
        move("@s %s matches 8" % LIFE, 8, column(0)),
    ])

    # ground seal: two discs turning against each other
    def seal(name, size_tag, spin):
        return prop(["rpg.pf.seal", size_tag, spin], "pope_fx/" + name,
                    xf(t=(0, 0.05, 0), s=(0.01, 1, 0.01)), "teleport_duration:1,")

    w("fx/seal", ["# 地面圣印（at 落点）。", seal("seal_outer", "rpg.pf.big", "rpg.pf.cw"),
                  seal("seal_inner", "rpg.pf.big", "rpg.pf.ccw")] + born(SEAL_LIFE))
    w("fx/seal_small", ["# 圣卫脚下的小圣印（at 圣卫）。", seal("seal_outer", "rpg.pf.small", "rpg.pf.cw"),
                        seal("seal_inner", "rpg.pf.small", "rpg.pf.ccw")] + born(SEAL_LIFE))
    w("fx/judge", ["# 天罚落点（at 地面）：圣印亮起，光柱随后落下。",
                   prop(["rpg.pf.seal", "rpg.pf.mid", "rpg.pf.cw", "rpg.pf.judge"], "pope_fx/seal_outer",
                        xf(t=(0, 0.05, 0), s=(0.01, 1, 0.01)), "teleport_duration:1,"),
                   seal("seal_inner", "rpg.pf.mid", "rpg.pf.ccw")] + born(SEAL_LIFE))
    w("fx/judge_tick", ["execute if score @s %s matches %d run function %s/fx/judge_strike" % (LIFE, JUDGE_STRIKE, F)])
    w("fx/judge_strike", [
        "# 光柱落下。判定只看距离。",
        "execute as @a[distance=..%s,%s] run damage @s %d minecraft:indirect_magic by @e[%s]"
        % (JUDGE_RADIUS + 0.3, SURVIVORS, JUDGE_DAMAGE, BOSS),
        "function %s/fx/pillar" % F,
        "execute positioned ~ ~1 ~ run function %s/fx/impact" % F,
    ])
    w("fx/seal_tick", [
        "execute if entity @s[tag=rpg.pf.cw] run tp @s ~ ~ ~ ~3 0",
        "execute if entity @s[tag=rpg.pf.ccw] run tp @s ~ ~ ~ ~-4 0",
        "execute if score @s %s matches %d if entity @s[tag=rpg.pf.big] run %s"
        % (LIFE, SEAL_LIFE - 1, merge(14, (SEAL_SIZE, 1, SEAL_SIZE))),
        "execute if score @s %s matches %d if entity @s[tag=rpg.pf.small] run %s"
        % (LIFE, SEAL_LIFE - 1, merge(14, (SEAL_SMALL, 1, SEAL_SMALL))),
        "execute if score @s %s matches %d if entity @s[tag=rpg.pf.mid] run %s"
        % (LIFE, SEAL_LIFE - 1, merge(8, (2 * JUDGE_RADIUS, 1, 2 * JUDGE_RADIUS))),
        move("@s %s matches 12" % LIFE, 12, (0, 1, 0)),
    ])

    # energy blast: a mote of light with a short trail
    w("fx/blast_one", [
        "# 一枚圣光弹（at 枪口，rotated 为飞行方向）。",
        sprite(["rpg.pf.blast"], "orb", xf(s=sized("orb", BLAST_SIZE, BLAST_SIZE)), "center", "teleport_duration:1,"),
        "tp @e[%s,distance=..1,limit=1] ~ ~ ~ ~ ~" % NEW,
    ] + born(BLAST_LIFE))
    w("fx/blast", [
        "# 飞行一刻（as、at 弹体）。",
        "tp @s ^ ^ ^%s" % BLAST_SPEED,
        "execute if entity @s[tag=rpg.pf.quick] run tp @s ^ ^ ^%s" % round(BASIC_SPEED - BLAST_SPEED, 2),
        stepping("orb"),
        "particle end_rod ~ ~ ~ 0.05 0.05 0.05 0.01 1 normal",
        "execute positioned ~ ~-0.6 ~ if entity @a[distance=..1.2,%s] run return run function %s/fx/blast_hit" % (SURVIVORS, F),
        "execute unless block ~ ~ ~ #minecraft:replaceable run function %s/fx/blast_burst" % F,
    ])
    w("fx/blast_hit", [
        "damage @a[distance=..2,%s,sort=nearest,limit=1] %d minecraft:indirect_magic by @e[%s]" % (SURVIVORS, BLAST_DAMAGE, BOSS),
        "function %s/fx/blast_burst" % F,
    ])
    w("fx/blast_burst", [
        "function %s/fx/impact" % F,
        "particle %s ~ ~ ~ 0.3 0.3 0.3 0.1 16 normal" % HOLY_DUST_BIG,
        "particle %s ~ ~ ~ 0 0 0 0 1 normal" % HOLY_FLASH,
        pp_sound("magic_impact", 0.5, 1, 24),
        "kill @s",
    ])

    # the Pope's coming: the halo opens behind his head
    w("fx/halo", [
        "# 光环（at 头顶）。",
        sprite(["rpg.pf.halo"], "halo", xf(s=sized("halo", 0.1, 0.1)), "center"),
    ] + born(APPEAR_FX))
    w("fx/halo_long", [
        "# 变身过场里一直亮着的光环，碎裂时由 fx/burst 收走。",
        sprite(["rpg.pf.halo"], "halo", xf(s=sized("halo", 0.1, 0.1)), "center"),
    ] + born(TRANSFORM_BURST + 10))
    # one-shot flipbooks: the frame comes from the entity's own remaining life
    w("fx/impact", ["# 圣光命中爆炸（at 爆点）。",
                    sprite(["rpg.pf.flip", "rpg.pf.gold"], "impact", xf(s=sized("impact", 3, 3)), "center")] + born(FLIP_LIFE))
    w("fx/impact_void", ["# 虚空落地爆炸（at 爆点）。",
                         sprite(["rpg.pf.flip", "rpg.pf.dark"], "impact_void", xf(s=sized("impact_void", 4, 4)), "center")] + born(FLIP_LIFE))

    def flip(glyph, life=FLIP_LIFE):
        code = art.GLYPHS[glyph][0]
        return ['execute if score @s %s matches %d run data merge entity @s {text:{text:"%s",font:"%s"}}'
                % (LIFE, life - 2 * i, chr(code + i), art.FONT) for i in range(1, art.SHEETS[glyph][1])]

    w("fx/slash", ["# 杖击的弧光（at 身前）。",
                   sprite(["rpg.pf.flip", "rpg.pf.arcs"], "slash", xf(s=sized("slash", 5, 5)), "center")] + born(SLASH_LIFE))
    w("fx/flip_gold", flip("impact"))
    w("fx/flip_dark", flip("impact_void"))
    w("fx/flip_arcs", flip("slash", SLASH_LIFE))
    w("fx/flip_tick", [
        "execute if entity @s[tag=rpg.pf.gold] run function %s/fx/flip_gold" % F,
        "execute if entity @s[tag=rpg.pf.dark] run function %s/fx/flip_dark" % F,
        "execute if entity @s[tag=rpg.pf.arcs] run function %s/fx/flip_arcs" % F,
    ])

    # light gathering on the staff before a cast is let go
    w("fx/charge", ["# 杖头聚能（at 杖头，出手帧的位置）。",
                    sprite(["rpg.pf.charge"], "orb", xf(s=sized("orb", 0.2, 0.2)), "center")] + born(CAST_FIRE))
    w("fx/charge_tick", [
        stepping("orb"),
        move("@s %s matches %d" % (LIFE, CAST_FIRE - 1), CAST_FIRE - 3, sized("orb", 2.4, 2.4)),
    ])

    # the whirlwind around the Pope while the staff takes him
    w("fx/vortex", ["# 变身旋风（at 教皇）。",
                    sprite(["rpg.pf.vortex"], "vortex",
                           xf(t=(0, VORTEX_HEIGHT / 2.0 - 0.5, 0), s=sized("vortex", 0.1, VORTEX_HEIGHT)), "vertical")]
      + born(TRANSFORM_BURST + 10))
    w("fx/vortex_tick", [
        stepping("vortex"),
        move("@s %s matches %d" % (LIFE, TRANSFORM_BURST + 9), 30, sized("vortex", VORTEX_WIDTH, VORTEX_HEIGHT)),
    ])

    w("fx/halo_tick", [
        stepping("halo"),
        move("@s %s matches %d" % (LIFE, APPEAR_FX - 1), 10, sized("halo", HALO_SIZE, HALO_SIZE)),
        move("@s %s matches %d" % (LIFE, TRANSFORM_BURST + 9), 10, sized("halo", HALO_SIZE, HALO_SIZE)),
        move("@s %s matches 10" % LIFE, 10, sized("halo", 0, 0)),
    ])

    # a ring of light where he leaves and lands; the same pop as a shell's shock
    w("fx/ring", [
        "# 瞬移光环（at 身前）。",
        sprite(["rpg.pf.pop", "rpg.pf.lit"], "halo", xf(s=sized("halo", 1, 1)), "center"),
    ] + born(POP_LIFE))
    w("fx/shock_big", [
        "# 破土冲击（at 地面）。",
        prop(["rpg.pf.pop", "rpg.pf.wide"], "pope_fx/mark_ring", xf(t=(0, 0.06, 0), s=(2, 1, 2))),
    ] + born(POP_LIFE))
    wide = 2 * RISE_RADIUS + 2
    w("fx/pop_tick", [
        "execute if score @s %s matches %d if entity @s[tag=rpg.pf.lit] run %s"
        % (LIFE, POP_LIFE - 1, merge(POP_LIFE - 3, sized("halo", 5, 5))),
        "execute if score @s %s matches %d if entity @s[tag=rpg.pf.wide] run %s"
        % (LIFE, POP_LIFE - 1, merge(POP_LIFE - 3, (wide, 1, wide))),
        "execute if score @s %s matches 2 run %s" % (LIFE, merge(2, (0, 0, 0))),
    ])

    # holy relics flung out when the Pope is taken: his crown, the staff's head, gold
    relics = [("pope/crown", 1.4), ("pope_fx/shard_a", 1.3), ("pope/staff_glow", 2), ("pope_fx/shard_b", 1.3),
              ("pope_fx/shard_c", 1.3), ("pope_fx/shard_a", 1), ("pope_fx/shard_b", 1), ("pope_fx/shard_c", 1)]
    lines = []
    for i, (model, size) in enumerate(relics):
        lines.append("execute rotated %.1f %d run function %s/fx/shard_%d" % (360.0 * i / len(relics), -20 - 15 * (i % 3), F, i))
        w("fx/shard_%d" % i, [
            prop(["rpg.pf.shard"], model, xf(s=(size, size, size)), "teleport_duration:1,"),
            "tp @e[%s,distance=..1,limit=1] ~ ~ ~ ~ ~" % NEW,
        ] + born(30))
    w("fx/burst", ["# 圣器碎裂：碎片向外炸开，光环裂成四段（at 中心）。", "kill @e[tag=rpg.pf.halo]", "kill @e[tag=rpg.pf.vortex]"] + lines + [
        "execute rotated %d -10 positioned ~ ~2.4 ~ run function %s/fx/arc" % (45 + 90 * i, F) for i in range(4)
    ] + ["particle %s ~ ~1 ~ 0 0 0 0 1 force" % HOLY_FLASH])
    w("fx/arc", [
        sprite(["rpg.pf.shard"], "halo_arc", xf(s=sized("halo_arc", 2.2, 2.2)), "center", "teleport_duration:1,"),
        "tp @e[%s,distance=..1,limit=1] ~ ~ ~ ~ ~" % NEW,
    ] + born(30))
    half = math.sqrt(0.5)
    w("fx/shard_tick", [
        "tp @s ^ ^ ^0.35",
        "execute if score @s %s matches 29 if entity @s[type=minecraft:item_display] run data merge entity @s "
        "{start_interpolation:0,interpolation_duration:17,transformation:{left_rotation:[%.4ff,0f,%.4ff,0f]}}" % (LIFE, half, half),
        "execute if score @s %s matches 12 run %s" % (LIFE, merge(12, (0, 0, 0))),
    ])

    # the chains that take a contract back, a pair per player
    def chain_pair(colour):
        tint = int(ui.hex_of(colour).lstrip("#"), 16)
        return [prop(["rpg.pf.chain", ring], "pope_fx/chain", xf(q=tilt, s=(CHAIN_WIDE, CHAIN_WIDE, CHAIN_WIDE)),
                     "teleport_duration:2,", tint)
                for ring, tilt in (("rpg.pf.lo", (0.09, 0, 0, 0.996)), ("rpg.pf.hi", (0, 0, 0.09, 0.996)))]

    w("fx/chain", ["# 收回契约：该柱颜色的锁链收紧（as、at 玩家）。"] + [
        "execute if score @s rpg_pact matches %d run return run function %s/fx/chain_%d" % (p["n"], F, p["n"])
        for p in ui.PILLARS
    ] + ["function %s/fx/chain_0" % F])
    for p in ui.PILLARS:
        w("fx/chain_%d" % p["n"], chain_pair(p["lit"]) + born(CHAIN_LIFE))
    w("fx/chain_0", chain_pair(ui.HOLY_DARK) + born(CHAIN_LIFE))
    w("fx/chain_tick", [
        "execute if entity @s[tag=rpg.pf.lo] at @a[distance=..8,sort=nearest,limit=1] run tp @s ~ ~0.6 ~ ~9 0",
        "execute if entity @s[tag=rpg.pf.hi] at @a[distance=..8,sort=nearest,limit=1] run tp @s ~ ~1.3 ~ ~-9 0",
        "execute if score @s %s matches %d run %s" % (LIFE, CHAIN_LIFE - 1, merge(10, (CHAIN_TIGHT, CHAIN_TIGHT, CHAIN_TIGHT))),
        "execute if score @s %s matches 8 run %s" % (LIFE, merge(8, (0, 0, 0))),
    ])

    # the blood rite's line: a thin box, stretched to the victim every beat
    w("fx/line", [
        "# 圣血祭的光线（at 杖头）。",
        prop(["rpg.pf.line"], "pope_fx/line", xf(s=(LINE_WIDTH, LINE_WIDTH, 0.01)), "teleport_duration:2,interpolation_duration:5,"),
    ] + born(CAST_END - CAST_FIRE + 2))

    # the Heart's shell: up out of the mouth and gone, then straight down onto
    # the warned spot.  The mark does the damage, the chunks are only seen.
    chunk = xf(s=(CHUNK_SIZE, CHUNK_SIZE, CHUNK_SIZE))
    w("fx/shell_up", [
        "# 迫击弹出口（at 嘴部，rotated 为飞行方向）。",
        prop(["rpg.pf.up"], SHELL_MODEL, chunk, "teleport_duration:1,"),
        "tp @e[%s,distance=..1,limit=1] ~ ~ ~ ~ ~" % NEW,
    ] + born(FALL_TICKS) + ["particle %s ~ ~ ~ 0.2 0.2 0.2 0.05 8 normal" % VOID_DUST])
    w("fx/mark_warn", [
        "# 落点预警（at 地面）：外圈先亮，内盘长满时弹体落地。",
        prop(["rpg.pf.mark"], "pope_fx/mark_ring", xf(t=(0, 0.05, 0), s=(0.01, 1, 0.01))),
    ] + born(MARK_LIFE) + [
        prop(["rpg.pf.fill"], "pope_fx/mark_fill", xf(t=(0, 0.04, 0), s=(0.01, 1, 0.01))),
    ] + born(MARK_LIFE) + ["particle %s ~ ~0.2 ~ 0.6 0 0.6 0 6 force" % VOID_DUST])
    full = 2 * MARK_RADIUS
    w("fx/mark_tick", [
        move("@s %s matches %d" % (LIFE, MARK_LIFE - 1), 4, (full, 1, full)),
        "execute if score @s %s matches %d positioned ~ ~%g ~ run function %s/fx/shell_down"
        % (LIFE, FALL_TICKS + 1, FALL_TICKS * FALL_STEP, F),
        "execute if score @s %s matches 1 run function %s/fx/mark_boom" % (LIFE, F),
    ])
    w("fx/fill_tick", [move("@s %s matches %d" % (LIFE, MARK_LIFE - 1), MARK_LIFE - 2, (full, 1, full))])
    w("fx/shell_down", [
        prop(["rpg.pf.fall"], SHELL_MODEL, chunk, "teleport_duration:1,"),
    ] + born(FALL_TICKS))
    w("fx/fall", [
        "# 下落一刻（as、at 弹体）。",
        "tp @s ~ ~-%s ~" % FALL_STEP,
        "particle %s ~ ~0.5 ~ 0.1 0.2 0.1 0 2 normal" % VOID_DUST,
    ])
    w("fx/mark_boom", [
        "# 弹体落地（at 落点）。",
        "execute as @a[distance=..%s,%s] run damage @s %d minecraft:indirect_magic by @e[%s]"
        % (MARK_RADIUS + 0.5, SURVIVORS, MARK_DAMAGE, HEART),
        "execute positioned ~ ~1.2 ~ run function %s/fx/impact_void" % F,
        "particle %s ~ ~0.3 ~ 0.8 0.2 0.8 0.1 16 normal" % VOID_DUST_BIG,
        "particle %s ~ ~0.3 ~ 0 0 0 0 1 normal" % VOID_FLASH,
        he_sound("mortar_land", 0.8),
        he_sound("mortar_explode", 0.6),
    ])

    # a ring of void running out along the ground; jump it.  Checked every
    # NOVA_STEP ticks, on a band as wide as the drawn ring.
    w("fx/nova", ["# 虚空震环（at 地面）。",
                  prop(["rpg.pf.nova"], "pope_fx/mark_ring", xf(t=(0, 0.08, 0), s=(1, 1, 1))),
                  ] + born(NOVA_LIFE) + [he_sound("mortar_explode", 0.8, 0.7)])
    band = []
    for age in range(NOVA_STEP, NOVA_LIFE - 2, NOVA_STEP):
        r = float(NOVA_RADIUS) * age / (NOVA_LIFE - 2)
        band.append("execute if score @s %s matches %d as @a[distance=%.1f..%.1f,%s] run function %s/fx/nova_hit"
                    % (LIFE, NOVA_LIFE - age, max(r - 1.6, 0), r + 1.6, SURVIVORS, F))
    w("fx/nova_tick", [
        "execute if score @s %s matches %d run %s" % (LIFE, NOVA_LIFE - 1, merge(NOVA_LIFE - 2, (2 * NOVA_RADIUS, 1, 2 * NOVA_RADIUS))),
    ] + band)
    w("fx/nova_hit", [
        "# 只打贴地的人：跳起来就能躲过去。as 玩家，at 环心。",
        "execute positioned ~-48 ~ ~-48 if entity @s[dx=96,dy=0,dz=96] run damage @s %d minecraft:indirect_magic by @e[%s]"
        % (NOVA_DAMAGE, HEART),
    ])

    # vents: a line of eruptions walking up to the target
    w("fx/vent", ["# 虚空喷涌的落点（at 地面）。",
                  prop(["rpg.pf.vent"], "pope_fx/mark_ring", xf(t=(0, 0.05, 0), s=(0.01, 1, 0.01)))] + born(VENT_LIFE))
    w("fx/vent_tick", [
        move("@s %s matches %d" % (LIFE, VENT_LIFE - 1), 4, (2 * VENT_RADIUS, 1, 2 * VENT_RADIUS)),
        "execute if score @s %s matches 1 run function %s/fx/vent_boom" % (LIFE, F),
    ])
    w("fx/vent_boom", [
        "execute as @a[distance=..%s,%s] run damage @s %d minecraft:indirect_magic by @e[%s]"
        % (VENT_RADIUS + 0.3, SURVIVORS, VENT_DAMAGE, HEART),
        "execute positioned ~ ~1.5 ~ run function %s/fx/impact_void" % F,
        "particle %s ~ ~0.3 ~ 0.6 0.2 0.6 0.1 12 normal" % VOID_DUST_BIG,
        he_sound("mortar_land", 0.6),
    ])

    # cross beam: yaw is what turns it, so one tp a tick and no NBT.  A glyph has
    # one visible side, so a beam is three planes: both faces of an upright one,
    # and a lid.  The first part of its life it is a thread showing where it
    # will sweep from.
    middle = BEAM_STEP + BEAM_REACH / 2.0
    thick, thin = 1.2, 0.09

    def beam_plane(tags, q):
        return sprite(["rpg.pf.beam"] + tags, "beam", xf(q=q, t=(0, 0, middle), s=sized("beam", BEAM_REACH, thin)),
                      "fixed", "teleport_duration:1,")

    r = math.sqrt(0.5)
    w("fx/beam_warn", [
        "# 一束光（at 体内小人，rotated 为朝向）：先是一条细线预警。第一片负责判定。",
        beam_plane(["rpg.pf.beamhit"], (0, r, 0, r)),
        beam_plane([], (0, -r, 0, r)),
        beam_plane([], (-0.5, 0.5, 0.5, 0.5)),
        "tp @e[%s,distance=..1] ~ ~ ~ ~ 0" % NEW,
    ] + born(BEAM_LIFE))
    w("fx/beam", [
        stepping("beam"),
        "execute if score @s %s matches %d run %s" % (LIFE, BEAM_ACTIVE, merge(3, sized("beam", BEAM_REACH, thick))),
        "execute if score @s %s matches 3 run %s" % (LIFE, merge(3, sized("beam", BEAM_REACH, 0))),
        "execute if score @s %s matches %d.. run return 0" % (LIFE, BEAM_ACTIVE + 1),
        "execute if score #dir %s matches 0 run tp @s ~ ~ ~ ~%s 0" % (O, BEAM_SPIN),
        "execute if score #dir %s matches 1 run tp @s ~ ~ ~ ~-%s 0" % (O, BEAM_SPIN),
        "execute if score @s %s matches 3.. if entity @s[tag=rpg.pf.beamhit] run function %s/fx/beam_sweep" % (LIFE, F),
    ])
    w("fx/beam_sweep", [
        setv("d", 0),
        "particle end_rod ^ ^-1.3 ^%d 0.3 0.1 0.3 0 1 normal" % (BEAM_REACH // 2),
        "execute positioned ^ ^-0.9 ^%d run function %s/fx/beam_step" % (BEAM_STEP, F),
    ])
    w("fx/beam_step", [
        "execute as @a[distance=..1.4,%s] run damage @s %d minecraft:indirect_magic by @e[%s]" % (SURVIVORS, BEAM_DAMAGE, HEART),
        "scoreboard players add #d %s 1" % O,
        "execute if score #d %s matches ..%d positioned ^ ^ ^%d run function %s/fx/beam_step"
        % (O, BEAM_REACH // BEAM_STEP - 1, BEAM_STEP, F),
    ])
    w("fx/flare", [
        "# 光束根部的光爆（at 体内小人）。",
        sprite(["rpg.pf.flare"], "flare", xf(s=sized("flare", 1, 1)), "center"),
    ] + born(BEAM_LIFE))
    w("fx/flare_burst", [
        "# 外壳碎裂时的光爆（at 中心）。",
        sprite(["rpg.pf.pop"], "flare", xf(s=sized("flare", 8, 8)), "center"),
    ] + born(POP_LIFE))
    w("fx/flare_tick", [
        stepping("flare"),
        "execute if score @s %s matches %d run %s" % (LIFE, BEAM_ACTIVE, merge(3, sized("flare", 7, 7))),
        "execute if score @s %s matches 4 run %s" % (LIFE, merge(4, sized("flare", 0, 0))),
    ])

    # the star-filled stain where the Heart goes under and comes up
    w("fx/puddle_warn", [
        "# 地面黑色拖痕（at 地面）。",
        prop(["rpg.pf.puddle"], "pope_fx/puddle", xf(t=(0, 0.03, 0), s=(0.01, 1, 0.01))),
    ] + born(SINK_WARN + RISE_HIT) + ["particle %s ~ ~0.2 ~ 1 0 1 0 12 force" % VOID_DUST])
    stain = 2 * RISE_RADIUS + 1
    w("fx/puddle_tick", [
        move("@s %s matches %d" % (LIFE, SINK_WARN + RISE_HIT - 1), SINK_WARN, (stain, 1, stain)),
        move("@s %s matches 8" % LIFE, 8, (0, 1, 0)),
    ])

    # when the Heart is destroyed
    count = 10
    w("fx/burst_void", ["# 外壳碎裂（at 中心）。", "function %s/fx/flare_burst" % F] + [
        "execute rotated %.1f %d run function %s/fx/shard_void" % (360.0 * i / count, -25 - 20 * (i % 3), F)
        for i in range(count)])
    w("fx/shard_void", [
        prop(["rpg.pf.shard"], SHELL_MODEL, xf(s=(1.3, 1.3, 1.3)), "teleport_duration:1,"),
        "tp @e[%s,distance=..1,limit=1] ~ ~ ~ ~ ~" % NEW,
    ] + born(30))


def write_more_fx():
    r = math.sqrt(0.5)
    planes = ((0, r, 0, r), (0, -r, 0, r), (-0.5, 0.5, 0.5, 0.5))

    # the quick bolt, a plain attack
    w("fx/blast_quick", [
        "# 普攻圣光弹（at 枪口，rotated 为飞行方向）。",
        sprite(["rpg.pf.blast", "rpg.pf.quick"], "orb", xf(s=sized("orb", 0.9, 0.9)), "center", "teleport_duration:1,"),
        "tp @e[%s,distance=..1,limit=1] ~ ~ ~ ~ ~" % NEW,
    ] + born(BLAST_LIFE))

    # Seven Seals: a halo opens in the air and fires down the line it warned of
    life = SEAL_WARN + SEAL_ACTIVE
    middle = SEAL_REACH / 2.0

    def lance_plane(tags, q):
        return sprite(["rpg.pf.more", "rpg.pf.lance"] + tags, "beam_gold",
                      xf(q=q, t=(0, 0, middle), s=sized("beam_gold", SEAL_REACH, 0.09)), "fixed")

    w("fx/lance_seal", [
        "# 一印（at 空中）：光环张开，锁定此刻玩家的位置。",
        sprite(["rpg.pf.more", "rpg.pf.sealed"], "halo", xf(s=sized("halo", 0.1, 0.1)), "center"),
    ] + born(life + 6) + [
        "execute facing entity @a[distance=..%d,%s,sort=random,limit=1] eyes run function %s/fx/lance_warn" % (BAR_RANGE, SURVIVORS, F),
        pp_sound("load_spell", 0.6, 1.3),
    ])
    w("fx/lance_warn", ["# 三片平面，第一片负责判定；先是一条细线。"] + [
        lance_plane(["rpg.pf.lancehit"] if i == 0 else [], q) for i, q in enumerate(planes)
    ] + ["tp @e[%s,distance=..1] ~ ~ ~ ~ ~" % NEW] + born(life))
    w("fx/sealed_tick", [
        stepping("halo"),
        move("@s %s matches %d" % (LIFE, life + 5), 8, sized("halo", 3.6, 3.6)),
        move("@s %s matches 6" % LIFE, 6, sized("halo", 0, 0)),
    ])
    w("fx/lance_tick", [
        stepping("beam_gold"),
        "execute if score @s %s matches %d run %s" % (LIFE, SEAL_ACTIVE, merge(2, sized("beam_gold", SEAL_REACH, 1.1))),
        "execute if score @s %s matches 3 run %s" % (LIFE, merge(3, sized("beam_gold", SEAL_REACH, 0))),
        "execute if score @s %s matches %d if entity @s[tag=rpg.pf.lancehit] run function %s/fx/lance_fire" % (LIFE, SEAL_ACTIVE, F),
        "execute if score @s %s matches %d if entity @s[tag=rpg.pf.lancehit] run function %s/fx/lance_ray" % (LIFE, SEAL_ACTIVE - 2, F),
        "execute if score @s %s matches %d if entity @s[tag=rpg.pf.lancehit] run function %s/fx/lance_ray" % (LIFE, SEAL_ACTIVE - 8, F),
    ])
    w("fx/lance_fire", [
        pp_sound("magic_impact", 1, 0.7, 48),
        "playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 0.6 1.6",
        "particle %s ~ ~ ~ 0 0 0 0 1 force" % HOLY_FLASH,
    ])
    w("fx/lance_ray", [setv("d", 0), "execute positioned ^ ^ ^2 run function %s/fx/lance_step" % F])
    w("fx/lance_step", [
        "execute positioned ~ ~-1 ~ as @a[distance=..1.6,%s] run damage @s %d minecraft:indirect_magic by @e[%s]"
        % (SURVIVORS, SEAL_DAMAGE, BOSS),
        "particle end_rod ~ ~ ~ 0.15 0.15 0.15 0.02 1 normal",
        "scoreboard players add #d %s 1" % O,
        "execute if score #d %s matches ..%d positioned ^ ^ ^2 run function %s/fx/lance_step" % (O, SEAL_REACH // 2 - 1, F),
    ])

    # Last Judgment: the whole floor is one seal, and three small ones are safe
    full = 2 * DOOM_RADIUS
    keep = DOOM_TICKS + 12

    def disc(name, spin):
        return prop(["rpg.pf.more", "rpg.pf.dooms", spin], "pope_fx/" + name, xf(t=(0, 0.07, 0), s=(0.01, 1, 0.01)), "teleport_duration:1,")

    w("fx/doom_seal", ["# 全场圣印（at 地面）：半透明，要看得见脚下和圣所。",
                       disc("doom_outer", "rpg.pf.cw"), disc("doom_inner", "rpg.pf.ccw")] + born(keep))
    w("fx/doom_tick", [
        "execute if entity @s[tag=rpg.pf.cw] run tp @s ~ ~ ~ ~1.5 0",
        "execute if entity @s[tag=rpg.pf.ccw] run tp @s ~ ~ ~ ~-2 0",
        "execute if score @s %s matches %d run %s" % (LIFE, keep - 1, merge(24, (full, 1, full))),
        move("@s %s matches 12" % LIFE, 12, (0, 1, 0)),
    ])
    wide = 2 * REFUGE_RADIUS
    w("fx/refuge", [
        "# 圣所（at 地面）：一根细光柱标出位置，老远就能看见。",
        sprite(["rpg.pf.more", "rpg.pf.refuge"], "column", xf(t=(0, PILLAR_HEIGHT / 2.0, 0), s=sized("column", 0.1, PILLAR_HEIGHT)), "vertical"),
    ] + born(DOOM_TICKS) + [
        prop(["rpg.pf.more", "rpg.pf.refdisc"], "pope_fx/seal_inner", xf(t=(0, 0.1, 0), s=(0.01, 1, 0.01)), "teleport_duration:1,"),
    ] + born(DOOM_TICKS))
    w("fx/refuge_tick", [
        stepping("column"),
        move("@s %s matches %d" % (LIFE, DOOM_TICKS - 1), 8, sized("column", 1.6, PILLAR_HEIGHT)),
        "execute if score #h %s matches 0 run particle end_rod ~ ~1 ~ 1.5 1 1.5 0.02 6 force" % O,
    ])
    w("fx/refdisc_tick", [
        "tp @s ~ ~ ~ ~4 0",
        "execute if score @s %s matches %d run %s" % (LIFE, DOOM_TICKS - 1, merge(8, (wide, 1, wide))),
    ])

    # the Arch-Visage's beam: the stand carries it, so this only keeps its shape
    span = FACE_OPEN - FACE_GONE
    thick = FACE_THICK - FACE_GONE
    closes = FACE_CLOSE - FACE_GONE

    def face_plane(q):
        return sprite(["rpg.pf.more", "rpg.pf.fbeam"], "beam", xf(q=q, t=(0, 0, FACE_REACH / 2.0), s=sized("beam", FACE_REACH, 0.09)),
                      "fixed", "teleport_duration:1,")

    w("fx/face_beam", ["# 面容的光束（at 嘴部，rotated 为面容朝向）：先是细线。"]
      + [face_plane(q) for q in planes] + ["tp @e[%s,distance=..1] ~ ~ ~ ~ 0" % NEW] + born(span))
    w("fx/fbeam_tick", [
        stepping("beam"),
        "execute if score @s %s matches %d run %s" % (LIFE, thick, merge(3, sized("beam", FACE_REACH, 1.0))),
        "execute if score @s %s matches %d run %s" % (LIFE, closes, merge(3, sized("beam", FACE_REACH, 0))),
    ])
    w("fx/face_step", [
        "execute as @a[distance=..1.4,%s] run damage @s %d minecraft:indirect_magic by @e[%s]" % (SURVIVORS, FACE_DAMAGE, HEART),
        "scoreboard players add #d %s 1" % O,
        "execute if score #d %s matches ..%d positioned ^ ^ ^2 run function %s/fx/face_step" % (O, FACE_REACH // 2 - 1, F),
    ])

    # Void Collapse: a stain spreading out to the line, and the storm over it
    last = COLLAPSE_TICKS + 8
    stain = 2 * COLLAPSE_RADIUS
    w("fx/collapse", [
        "# 虚空坍缩（at 地面）。",
        prop(["rpg.pf.more", "rpg.pf.pool"], "pope_fx/puddle", xf(t=(0, 0.05, 0), s=(0.01, 1, 0.01))),
    ] + born(last) + [
        prop(["rpg.pf.more", "rpg.pf.edge"], "pope_fx/mark_ring", xf(t=(0, 0.09, 0), s=(0.01, 1, 0.01))),
    ] + born(last) + [
        sprite(["rpg.pf.more", "rpg.pf.gyre"], "vortex_void", xf(t=(0, 7.5, 0), s=sized("vortex_void", 0.1, 16)), "vertical"),
    ] + born(last))
    w("fx/pool_tick", [
        "execute if score @s %s matches %d run %s" % (LIFE, last - 1, merge(30, (stain, 1, stain))),
        move("@s %s matches 8" % LIFE, 8, (0, 1, 0)),
    ])
    w("fx/edge_tick", [
        "execute if score @s %s matches %d run %s" % (LIFE, last - 1, merge(30, (stain, 1, stain))),
        "execute if score @s %s matches 8 run %s" % (LIFE, merge(8, (stain + 6, 1, stain + 6))),
    ])
    w("fx/gyre_tick", [
        stepping("vortex_void"),
        "execute if score @s %s matches %d run %s" % (LIFE, last - 1, merge(30, sized("vortex_void", 12, 16))),
        "execute if score @s %s matches 8 run %s" % (LIFE, merge(8, sized("vortex_void", 0, 16))),
    ])

    # the shell it spits as a plain attack
    w("fx/spit", [
        "# 虚空碎块（at 嘴部，rotated 为飞行方向）。",
        prop(["rpg.pf.more", "rpg.pf.bolt"], SHELL_MODEL, xf(s=(0.7, 0.7, 0.7)), "teleport_duration:1,"),
        "tp @e[%s,distance=..1,limit=1] ~ ~ ~ ~ ~" % NEW,
    ] + born(SPIT_LIFE) + ["particle %s ~ ~ ~ 0.2 0.2 0.2 0.05 8 normal" % VOID_DUST])
    w("fx/bolt", [
        "tp @s ^ ^ ^%s" % SPIT_SPEED,
        "particle %s ~ ~ ~ 0.1 0.1 0.1 0 2 normal" % VOID_DUST,
        "execute positioned ~ ~-0.6 ~ if entity @a[distance=..1.2,%s] run return run function %s/fx/bolt_hit" % (SURVIVORS, F),
        "execute unless block ~ ~ ~ #minecraft:replaceable run function %s/fx/bolt_burst" % F,
    ])
    w("fx/bolt_hit", [
        "damage @a[distance=..2,%s,sort=nearest,limit=1] %d minecraft:indirect_magic by @e[%s]" % (SURVIVORS, SPIT_DAMAGE, HEART),
        "function %s/fx/bolt_burst" % F,
    ])
    w("fx/bolt_burst", [
        "function %s/fx/impact_void" % F,
        "particle %s ~ ~ ~ 0.3 0.3 0.3 0.1 12 normal" % VOID_DUST_BIG,
        he_sound("mortar_land", 0.4, 1.4, 24),
        "kill @s",
    ])


def write_clips():
    for clip in ("idle", "attack", "summon", "cast", "appear", "teleport_in", "teleport_out", "whirlwind"):
        w("clip/" + clip, ["function rpg:pope/anim/enter/%s" % clip])


def write_stages():
    # stage 1: the Holy Guards alone
    offsets = [(6, 0), (-6, 0), (0, 6), (0, -6)][:GUARDS]

    def drop(target):
        return ["execute positioned ~%d ~ ~%d positioned over motion_blocking_no_leaves run function %s/%s"
                % (x, z, F, target) for x, z in offsets]

    w("stage1_enter", [
        "# 第一阶段：圣卫降临，教皇不在场。",
        setv("stage", 1), setv("t", 0),
        "function %s/bgm/play_1" % F,
        bar_name("guard", GUARDS),
        "bossbar set minecraft:pope max %d" % GUARDS,
        "bossbar set minecraft:pope value %d" % GUARDS,
        say("圣座已宣告：你是异端。", gloss=True),
    ] + drop("fx/pillar"))
    w("stage1", [
        "execute if score #t %s matches 20 run function %s/stage1_spawn" % (O, F),
        "execute if score #t %s matches ..20 run return 0" % O,
        "execute store result bossbar minecraft:pope value if entity @e[%s]" % UNIT,
        "execute store result score #hud %s if entity @e[%s]" % (O, UNIT),
        "execute unless score #hud %s = #hudl %s run function %s/bar/guard" % (O, O, F),
        "execute unless entity @e[%s,limit=1] run function %s/stage2_enter" % (UNIT, F),
    ])
    w("stage1_spawn", drop("spawn_guard"))
    w("spawn_guard", [
        "# 一名圣卫（at 落点），打上本场标签。",
        "function rpg:tower_guard/summon",
        "tag @e[type=minecraft:vindicator,tag=rpg.tg,tag=!rpg.pf.unit,distance=..2] add rpg.pf.unit",
    ])

    # stage 2: the Pope
    w("stage2_enter", [
        "# 第二阶段：教皇亲临。",
        setv("stage", 2), setv("t", 0),
        "function %s/bgm/play_2" % F,
        setv("sk", SKILLS["appear"]), setv("st", 0), setv("h", 0),
        setv("wave", 1), setv("next", WAVE_LINES[0]),
        setv("cd", 0), setv("tp", 0),
        setv("blood", 200), setv("reclaim", 600), setv("enhance", 100),
        setv("pb", 0), setv("ultq", 0), setv("ulti", 0), setv("ultcd", ULT_EVERY), setv("ultl", POPE_ULT_LINES[0]),
        bar_name("pope", 20), setv("hudl", 20),
        "bossbar set minecraft:pope max %d" % POPE_HEALTH,
        "bossbar set minecraft:pope value %d" % POPE_HEALTH,
        "function %s/fx/pillar" % F,
        "execute positioned ~ ~2.4 ~ run function %s/fx/halo" % F,
        "particle %s ~ ~1 ~ 0.8 1.2 0.8 0.08 64 force" % HOLY_DUST_BIG,
        "particle %s ~ ~1 ~ 0 0 0 0 1 force" % HOLY_FLASH,
        say("跪下。这片大地上的权柄，只有一个来源。", gloss=True),
        "function rpg:pope/summon",
        "tag @e[type=minecraft:vindicator,tag=rpg.pope,tag=!rpg.pf.boss,distance=..2] add rpg.pf.boss",
        "execute as @e[%s] run function %s/boss/init" % (BOSS, F),
    ])
    w("stage2", [
        "# 他倒下有两条路：血量到线，或一击打穿。后者靠这条兜底。",
        "execute unless entity @e[%s] run return run function %s/stage3_enter" % (BOSS, F),
        "execute as @e[%s] at @s run function %s/boss/tick" % (BOSS, F),
    ])

    # stage 3: the staff takes him
    spiral = []
    for i in range(8):
        a = math.radians(45 * i)
        spiral.append("particle %s ~%.2f ~%.1f ~%.2f 0 0 0 0 1 normal"
                      % (HOLY_DUST, 2.5 * math.cos(a), 0.3 * i, 2.5 * math.sin(a)))
    w("stage3_enter", [
        "# 过场：圣器反噬。人倒下了，圣力还在。旋风放完 7 秒才碎；他要是已被一击打穿，直接碎。",
        setv("stage", 3), setv("t", 0),
        "# 还没落下的天罚、光束、圣印到这里全部作废。",
        "kill @e[%s]" % FX,
        "execute as @e[%s] run function %s/boss/show" % (BOSS, F),
        "execute unless entity @e[%s] run %s" % (BOSS, setv("t", TRANSFORM_BURST - 1)),
        "execute as @e[%s] run function %s" % (UNIT, GUARD_REMOVE),
        "execute as @e[%s] run data merge entity @s {Invulnerable:1b}" % BOSS,
        "execute as @e[%s] run function %s/clip/whirlwind" % (BOSS, F),
        "execute as @e[%s] at @s run tp @e[%s] ~ ~ ~" % (BOSS, CENTER),
        bar_name("pope", 0),
        "execute as @e[%s] at @s positioned ~ ~2.4 ~ run function %s/fx/halo_long" % (BOSS, F),
        "execute as @e[%s] at @s run function %s/fx/vortex" % (BOSS, F),
        "bossbar set minecraft:pope value 0",
        say("圣器……在吃我……", gloss=True),
    ])
    w("stage3", [
        "execute if score #t %s matches %d..%d run function %s/stage3_spiral" % (O, SPIRAL_FROM, TRANSFORM_BURST, F),
        "execute if score #t %s matches %d run function %s/stage3_burst" % (O, TRANSFORM_BURST, F),
        "execute if score #t %s matches %d.. run function %s/stage4_enter" % (O, TRANSFORM_END, F),
    ])
    w("stage3_spiral", ["# 圣力回旋着收拢。"] + spiral)
    w("stage3_burst", [
        "execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss] run function %s/boss/remove" % F,
        "function %s/fx/burst" % F,
        "# 旋风原声 13 秒，比动作长，到这里收掉。",
        "stopsound @a[distance=..48] hostile rpg:pope.whirlwind",
        "playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 0.7",
    ])

    # stage 4: the Heart of Ender.  Its own logic is write_heart().
    w("stage4_enter", [
        "# Boss 二阶段：末影之心升起，教皇困在体内。",
        setv("stage", 4), setv("t", 0),
        "function %s/bgm/play_3" % F,
        bar_name("heart", 20), setv("hudl", 20),
        "bossbar set minecraft:pope max %d" % HEART_HEALTH,
        "bossbar set minecraft:pope value %d" % HEART_HEALTH,
        "particle %s ~ ~1 ~ 1.5 0.5 1.5 0.1 64 force" % VOID_DUST_BIG,
        "particle %s ~ ~1 ~ 0 0 0 0 1 force" % VOID_FLASH,
        say("圣力……从来就不是圣的。", "末影之心", True),
        "execute positioned over motion_blocking_no_leaves run function %s/heart/spawn" % F,
    ])
    w("stage4", [
        "# 判定体只会被一击打穿才没有；正常死亡走血量。",
        "execute unless entity @e[%s] run return run function %s/heart/die" % (HEART, F),
        "execute as @e[%s] at @s run function %s/heart/tick" % (HEART, F),
    ])
    w("stage5", [
        "# 末影之心倒下：死亡动作放完，外壳才碎。",
        "execute if score #bl %s matches 1.. run function %s/heart/blend_tick" % (O, F),
        "execute if score #t %s matches %d run function %s/heart/shatter" % (O, BLEND + DEATH_BURST, F),
        "execute if score #t %s matches %d.. run function %s/victory" % (O, BLEND + DEATH_END, F),
    ])
    w("victory", [
        "# 击败结算：清魔化，收束。",
        "scoreboard players set @a[distance=..%d] rpg_taint 0" % BAR_RANGE,
        say("「你们必晓得真理，真理必叫你们得以自由。」——《约翰福音》8:32", gloss=True),
        "playsound minecraft:ui.toast.challenge_complete player @a[distance=..%d] ~ ~ ~ 1 1" % BAR_RANGE,
        "function %s/clear" % F,
    ])


def write_boss():
    b = "boss/"
    w(b + "init", [
        "# 教皇：不走路，靠瞬移；不带 rpg.demon，所以上位契约打不到他。",
        "data merge entity @s {NoAI:1b}",
        "attribute @s minecraft:max_health base set %d" % POPE_HEALTH,
        "attribute @s minecraft:armor base set 10",
        "attribute @s minecraft:knockback_resistance base set 1",
        "data merge entity @s {Health:%d.0f}" % POPE_HEALTH,
        "function %s/clip/appear" % F,
    ])
    w(b + "remove", [
        "# 带着部件一起走。",
        "execute on passengers run kill @s",
        "kill @s",
    ])
    cds = ["execute if score #%s %s matches 1.. run scoreboard players remove #%s %s 1" % (n, O, n, O)
           for n in ("cd", "tp", "blood", "reclaim", "enhance", "ultcd")]

    def near(reach):
        return "@a[distance=..%s,%s]" % (reach, SURVIVORS)

    w(b + "tick", [
        "# 教皇一刻（as、at 教皇）。",
        "scoreboard players add #h %s 1" % O,
        "execute if score #h %s matches 5.. run function %s/boss/read" % (O, F),
    ] + cds + [
        "execute if score #stage %s matches 3 run return 0" % O,
        "execute if score #sk %s matches 1.. run return run function %s/boss/skill" % (O, F),
        "execute if score #wave %s matches 1 run return run function %s/boss/start_summon" % (O, F),
        "execute if score #tp %s matches 0 if entity %s run return run function %s/boss/start_teleport" % (O, near(3), F),
        "execute if score #cd %s matches 1.. run return 0" % O,
        "execute if score #ultq %s matches 1 run return run function %s/boss/start_ult" % (O, F),
        "execute if score #ultcd %s matches 0 if entity %s run return run function %s/boss/start_ult" % (O, near(32), F),
        "execute if entity %s run return run function %s/boss/start_melee" % (near(MELEE_REACH), F),
        "execute if score #blood %s matches 0 if entity @e[%s,limit=1] run return run function %s/boss/start_blood" % (O, UNIT, F),
        "execute if score #reclaim %s matches 0 if entity %s run return run function %s/boss/start_reclaim" % (O, near(25), F),
        "execute if score #enhance %s matches 0 if entity @e[%s,distance=..11,limit=1] run return run function %s/boss/start_enhance" % (O, UNIT, F),
        "execute if score #pb %s matches %d.. if entity %s run return run function %s/boss/start_ranged" % (O, BASICS_PER_SKILL, near(25), F),
        "execute if entity %s run function %s/boss/start_basic" % (near(32), F),
    ])
    w(b + "start_ult", [
        "# 大招：血量到线或时钟走完，先到先出。两招轮流。",
        setv("ultq", 0), setv("ultcd", ULT_EVERY),
        "scoreboard players add #ulti %s 1" % O,
        "execute if score #ulti %s matches 1 run return run function %s/boss/start_seals" % (O, F),
        setv("ulti", 0),
        "function %s/boss/start_doom" % F,
    ])
    w(b + "start_ranged", [
        "# 远程四拍轮换：扇形、天罚、扇形、圣环。",
        setv("pb", 0),
        "scoreboard players add #ps %s 1" % O,
        "execute if score #ps %s matches 4.. run %s" % (O, setv("ps", 0)),
        "execute if score #ps %s matches 1 run return run function %s/boss/start_judge" % (O, F),
        "execute if score #ps %s matches 3 run return run function %s/boss/start_ring" % (O, F),
        "function %s/boss/start_attack" % F,
    ])
    w(b + "read", [
        "# 每 5 刻读一次血量（一次 NBT），转身面向最近的玩家。",
        setv("h", 0),
        "execute store result score #hp %s run data get entity @s Health" % O,
        "execute store result bossbar minecraft:pope value run scoreboard players get #hp %s" % O,
        "function %s/bar/hp" % F,
        "execute if score #hp %s matches ..%d run return run function %s/stage3_enter" % (O, TRANSFORM_AT, F),
    ] + ["execute if score #next %s matches %d if score #hp %s matches ..%d run function %s/boss/wave_due"
         % (O, line, O, line, F) for line in WAVE_LINES] + [
        "execute if score #ultl %s matches %d if score #hp %s matches ..%d run function %s/boss/ult_due"
        % (O, line, O, line, F) for line in POPE_ULT_LINES] + [
        "execute if score #sk %s matches 0 facing entity @a[distance=..32,%s,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0" % (O, SURVIVORS),
    ])
    after = list(WAVE_LINES[1:]) + [0]
    w(b + "wave_due", [setv("wave", 1)] + [
        "execute if score #next %s matches %d run return run %s" % (O, line, setv("next", later))
        for line, later in zip(WAVE_LINES, after)])

    w(b + "ult_due", [setv("ultq", 1)] + [
        "execute if score #ultl %s matches %d run return run %s" % (O, line, setv("ultl", later))
        for line, later in zip(POPE_ULT_LINES, list(POPE_ULT_LINES[1:]) + [0])])

    def starter(name, clip):
        return [setv("sk", SKILLS[name]), setv("st", 0), "function %s/clip/%s" % (F, clip)]

    w(b + "start_attack", starter("attack", "attack"))
    w(b + "start_basic", starter("basic", "attack"))
    w(b + "do_basic", [
        "execute if score #st %s matches %d run function %s/boss/basic_fire" % (O, ATTACK_FIRE, F),
        "execute if score #st %s matches %d.. run function %s/boss/basic_end" % (O, ATTACK_END, F),
    ])
    w(b + "basic_fire", [
        "# 普攻：一发快弹。",
        "execute positioned %s facing entity @a[distance=..32,%s,sort=nearest,limit=1] eyes run function %s/fx/blast_quick"
        % (ATTACK_TIP, SURVIVORS, F),
        pp_sound("spell", 0.5, 1.4),
    ])
    w(b + "basic_end", [
        setv("sk", 0), setv("st", 0), setv("cd", BASIC_GAP),
        "scoreboard players add #pb %s 1" % O,
        "function %s/clip/idle" % F,
    ])
    write_pope_ults()
    w(b + "start_melee", starter("melee", "attack") + [pp_sound("hargh", 0.8)])
    w(b + "start_summon", [setv("wave", 0)] + starter("summon", "summon"))
    w(b + "start_teleport", [setv("tp", COOLDOWNS["tp"]), "data merge entity @s {Invulnerable:1b}"]
      + starter("teleport", "teleport_out"))
    charge = ["execute positioned %s run function %s/fx/charge" % (CAST_TIP, F), pp_sound("load_spell", 0.7)]
    w(b + "start_blood", [setv("blood", COOLDOWNS["blood"]),
                          "tag @e[%s,sort=nearest,limit=1] add rpg.pf.sac" % UNIT,
                          say("为圣座流血吧，孩子。")] + starter("blood", "cast") + charge)
    w(b + "start_reclaim", [setv("reclaim", COOLDOWNS["reclaim"])] + starter("reclaim", "cast") + charge)
    w(b + "start_enhance", [setv("enhance", COOLDOWNS["enhance"])] + starter("enhance", "cast") + charge)
    w(b + "start_ring", starter("ring", "cast") + charge)
    w(b + "start_judge", starter("judge", "summon") + [pp_sound("load_spell", 0.7)])

    w(b + "skill", [
        "# 招式进行中。",
        "scoreboard players add #st %s 1" % O,
    ] + ["execute if score #sk %s matches %d run return run function %s/boss/do_%s" % (O, sid, F, name)
         for name, sid in SKILLS.items()])
    w(b + "end", [
        setv("sk", 0), setv("st", 0), setv("cd", BREATHER),
        "function %s/clip/idle" % F,
    ])
    w(b + "do_appear", ["execute if score #st %s matches %d.. run function %s/boss/appear_done" % (O, APPEAR_END, F)])
    w(b + "appear_done", [pp_sound("intro_greetings", 1, 1, 48), "function %s/boss/end" % F])

    # three blasts in a fan
    w(b + "do_attack", [
        "execute if score #st %s matches %d run function %s/boss/fire" % (O, ATTACK_FIRE, F),
        "execute if score #st %s matches %d.. run function %s/boss/end" % (O, ATTACK_END, F),
    ])
    w(b + "fire", ["# 三连圣光弹。"] + [
        "execute positioned %s facing entity @a[distance=..25,%s,sort=nearest,limit=1] eyes "
        "rotated ~%d ~ run function %s/fx/blast_one" % (ATTACK_TIP, SURVIVORS, d, F)
        for d in (-BLAST_SPREAD, 0, BLAST_SPREAD)
    ])
    w(b + "do_melee", [
        "execute if score #st %s matches %d run function %s/boss/melee_hit" % (O, ATTACK_FIRE, F),
        "execute if score #st %s matches %d.. run function %s/boss/end" % (O, ATTACK_END, F),
    ])
    w(b + "melee_hit", [
        "# 杖击：普攻。",
        "execute positioned ^ ^1.4 ^1.8 run function %s/fx/slash" % F,
        "execute at @a[distance=..%s,%s,sort=nearest,limit=1] positioned ~ ~1 ~ run function %s/fx/impact" % (MELEE_REACH + 0.5, SURVIVORS, F),
        "damage @a[distance=..%s,%s,sort=nearest,limit=1] %d minecraft:indirect_magic by @s" % (MELEE_REACH + 0.5, SURVIVORS, MELEE_DAMAGE),
        "particle %s ~ ~1 ~ 0.8 0.5 0.8 0.1 24 normal" % HOLY_DUST_BIG,
    ])

    # a ring of blasts all round him: there is a gap to stand in, then it closes
    w(b + "do_ring", [
        "execute if score #st %s matches %d run function %s/boss/ring_one" % (O, CAST_FIRE, F),
        "execute if score #st %s matches %d run function %s/boss/ring_two" % (O, CAST_FIRE + RING_DELAY, F),
        "execute if score #st %s matches %d.. run function %s/boss/end" % (O, CAST_END, F),
    ])
    w(b + "ring_one", ["# 圣环第一圈。", pp_sound("spell", 0.8)] + [
        "execute positioned ~ ~1.2 ~ rotated %.1f 0 run function %s/fx/blast_one" % (360.0 * i / RING_SHOTS, F)
        for i in range(RING_SHOTS)])
    w(b + "ring_two", ["# 圣环第二圈，错开半格。", pp_sound("spell", 0.8, 1.2)] + [
        "execute positioned ~ ~1.2 ~ rotated %.1f 0 run function %s/fx/blast_one" % (360.0 * (i + 0.5) / RING_SHOTS, F)
        for i in range(RING_SHOTS)])

    # judgment: seals under the player, then the pillars come down
    w(b + "do_judge", [
        "execute if score #st %s matches %d run function %s/boss/judge_marks" % (O, SUMMON_FIRE, F),
        "execute if score #st %s matches %d.. run function %s/boss/end" % (O, SUMMON_END, F),
    ])
    w(b + "judge_marks", ["# 天罚：脚下一枚，走位方向各一枚。"] + [
        "execute at @a[distance=..48,%s,sort=nearest,limit=1] rotated ~ 0 positioned %s "
        "positioned over motion_blocking_no_leaves run function %s/fx/judge" % (SURVIVORS, where, F)
        for where in ("^ ^ ^", "^ ^ ^5", "^4 ^ ^-2", "^-4 ^ ^-2")
    ])

    # teleport: gone for a moment, back on a ring around the nearest player
    ring = []
    for i in range(8):
        a = math.radians(45 * i)
        ring.append("execute if score #r %s matches %d at @a[distance=..48,%s,sort=nearest,limit=1] positioned ~%.1f ~ ~%.1f "
                    "positioned over motion_blocking_no_leaves facing entity @a[distance=..16,%s,sort=nearest,limit=1] feet "
                    "rotated ~ 0 run tp @s ~ ~ ~ ~ 0"
                    % (O, i, SURVIVORS, 13.5 * math.cos(a), 13.5 * math.sin(a), SURVIVORS))
    w(b + "do_teleport", [
        "execute if score #st %s matches %d run function %s/boss/hide" % (O, TELEPORT - 1, F),
        "execute if score #st %s matches %d run function %s/boss/teleport_jump" % (O, TELEPORT, F),
        "execute if score #st %s matches %d run function %s/boss/show" % (O, TELEPORT + 3, F),
        "execute if score #st %s matches %d.. run function %s/boss/teleport_done" % (O, TELEPORT * 2, F),
    ])
    w(b + "hide", [
        "# 载体传送时客户端会滑行 3 刻，这几刻把部件藏起来，否则一路拖过去。",
        "execute on passengers run data merge entity @s {view_range:0f}",
    ])
    w(b + "show", ["execute on passengers run data merge entity @s {view_range:%s}" % PART_VIEW])
    w(b + "teleport_jump", [
        "# 瞬移打断加护，落点在最近玩家周围 13.5 格。",
        "effect clear @e[%s] minecraft:resistance" % UNIT,
        "particle %s ~ ~1 ~ 0 0 0 0 1 normal" % HOLY_FLASH,
        "particle end_rod ~ ~1 ~ 0.4 0.8 0.4 0.05 24 normal",
        "execute positioned ~ ~1.3 ~ run function %s/fx/ring" % F,
        "execute store result score #r %s run random value 0..7" % O,
    ] + ring + [
        "execute at @s run particle %s ~ ~1 ~ 0 0 0 0 1 normal" % HOLY_FLASH,
        "execute at @s run particle end_rod ~ ~1 ~ 0.4 0.8 0.4 0.05 24 normal",
        "execute at @s positioned ~ ~1.3 ~ run function %s/fx/ring" % F,
        "function %s/clip/teleport_in" % F,
    ])
    w(b + "teleport_done", [
        "# 落地立刻出手。",
        "data merge entity @s {Invulnerable:0b}",
        setv("sk", 0), setv("cd", 0),
        "function %s/boss/start_attack" % F,
    ])

    # waves of the Holy See around the nearest player
    def around(target):
        return ["execute if score #n %s matches ..%d at @a[distance=..48,%s,sort=nearest,limit=1] rotated %d 0 "
                "positioned ^ ^ ^5 positioned over motion_blocking_no_leaves run function %s/%s"
                % (O, UNIT_CAP - 1 - i, SURVIVORS, 180 * i, F, target) for i in range(WAVE_SIZE)]

    w(b + "do_summon", [
        "execute if score #st %s matches 1 run function %s/boss/wave_mark" % (O, F),
        "execute if score #st %s matches %d run function %s/boss/wave_drop" % (O, SUMMON_FIRE, F),
        "execute if score #st %s matches %d.. run function %s/boss/end" % (O, SUMMON_END, F),
    ])
    w(b + "wave_mark", [
        "# 教廷总动员：先在落点亮起圣印和光柱。",
        "execute store result score #n %s if entity @e[%s]" % (O, UNIT),
        say("教廷的军团，听我号令。"),
    ] + around("boss/wave_seal"))
    w(b + "wave_seal", ["function %s/fx/seal" % F, "function %s/fx/pillar" % F])
    w(b + "wave_drop", around("spawn_guard"))

    # blood rite: kill the victim first to break it
    w(b + "do_blood", [
        "execute unless entity @e[%s,limit=1] run return run function %s/boss/blood_broken" % (SAC, F),
        "execute if score #st %s matches %d.. run return run function %s/boss/blood_done" % (O, CAST_END, F),
        "execute if score #st %s matches %d positioned %s run function %s/fx/line" % (O, CAST_FIRE, CAST_TIP, F),
        "execute if score #st %s matches %d.. if score #h %s matches 0 run function %s/boss/blood_line" % (O, CAST_FIRE, O, F),
    ])
    w(b + "blood_line", [
        "# 光线从杖头连到祭品：量出距离，再把展示实体拉到这么长。",
        setv("d", 0),
        "execute positioned %s facing entity @e[%s,limit=1] eyes run function %s/boss/blood_step" % (CAST_TIP, SAC, F),
        "execute positioned %s facing entity @e[%s,limit=1] eyes run function %s/boss/blood_aim" % (CAST_TIP, SAC, F),
    ])
    w(b + "blood_aim", [
        "execute as @e[tag=rpg.pf.line,limit=1] run tp @s ~ ~ ~ ~ ~",
        "execute as @e[tag=rpg.pf.line,limit=1] store result entity @s transformation.scale[2] float 1 run scoreboard players get #d %s" % O,
        "execute as @e[tag=rpg.pf.line,limit=1] store result entity @s transformation.translation[2] float 0.5 run scoreboard players get #d %s" % O,
        "execute as @e[tag=rpg.pf.line,limit=1] run data merge entity @s {start_interpolation:0}",
    ])
    w(b + "blood_step", [
        "particle %s ~ ~ ~ 0 0 0 0 1 normal" % HOLY_DUST,
        "scoreboard players add #d %s 1" % O,
        "# 瞄的是眼睛，距离却从脚下算，所以这里先降到脚边再比。",
        "execute positioned ~ ~-1.6 ~ if entity @e[%s,distance=..1] run return 0" % SAC,
        "execute if score #d %s matches ..%d positioned ^ ^ ^1 run function %s/boss/blood_step" % (O, BLOOD_REACH, F),
    ])
    w(b + "blood_broken", [
        say("……圣血祭被打断了。"),
        "kill @e[tag=rpg.pf.line]",
        pp_sound("spell_disappear"),
        "function %s/boss/end" % F,
    ])
    w(b + "blood_done", [
        "# 祭品化为圣力。",
        "kill @e[tag=rpg.pf.line]",
        "execute as @e[%s] at @s run particle %s ~ ~1 ~ 0.5 1 0.5 0.1 24 normal" % (SAC, HOLY_DUST_BIG),
        "execute as @e[%s] run function %s" % (SAC, GUARD_REMOVE),
        "execute store result score #hp %s run data get entity @s Health" % O,
        "scoreboard players add #hp %s %d" % (O, BLOOD_HEAL),
        "execute if score #hp %s matches %d.. run %s" % (O, POPE_HEALTH + 1, setv("hp", POPE_HEALTH)),
        "execute store result entity @s Health float 1 run scoreboard players get #hp %s" % O,
        pp_sound("haha"),
        "function %s/boss/end" % F,
    ])

    w(b + "do_reclaim", [
        "execute if score #st %s matches %d run function %s/boss/reclaim_done" % (O, CAST_FIRE, F),
        "execute if score #st %s matches %d.. run function %s/boss/end" % (O, CAST_END, F),
    ])
    w(b + "reclaim_done", [
        "# 收回契约：七罪契约进入 15 秒冷却。",
        "scoreboard players set @a[distance=..%d,%s] rpg_pact_cd %d" % (ARENA, SURVIVORS, RECLAIM_TICKS),
        "scoreboard players set @a[distance=..%d,%s,scores={rpg_pact_cd2=..%d}] rpg_pact_cd2 %d" % (ARENA, SURVIVORS, RECLAIM_TICKS, RECLAIM_TICKS),
        "scoreboard players set @a[distance=..%d,%s,scores={rpg_pact_cd3=..%d}] rpg_pact_cd3 %d" % (ARENA, SURVIVORS, RECLAIM_TICKS, RECLAIM_TICKS),
        "execute as @a[distance=..%d,%s] at @s run particle enchant ~ ~1 ~ 0.5 1 0.5 0.5 24 normal" % (ARENA, SURVIVORS),
        "execute as @a[distance=..%d,%s] at @s run function %s/fx/chain" % (ARENA, SURVIVORS, F),
        say("你借来的力量，账本在我手里。"),
        pp_sound("laugh"),
    ])
    w(b + "do_enhance", [
        "execute if score #st %s matches %d run function %s/boss/enhance_done" % (O, CAST_FIRE, F),
        "execute if score #st %s matches %d.. run function %s/boss/end" % (O, CAST_END, F),
    ])
    w(b + "enhance_done", [
        "# 加护：11 格内的圣卫减伤加速，教皇一瞬移就断。",
        "effect give @e[%s,distance=..11] minecraft:resistance 10 1 true" % UNIT,
        "effect give @e[%s,distance=..11] minecraft:speed 10 1 true" % UNIT,
        "execute as @e[%s,distance=..11] at @s run function %s/fx/seal_small" % (UNIT, F),
    ])


def write_pope_ults():
    b = "boss/"

    def starter(name, clip):
        return [setv("sk", SKILLS[name]), setv("st", 0), "function %s/clip/%s" % (F, clip)]

    # Seven Seals: seven aimed lines, one after another, each warned first
    w(b + "start_seals", starter("seals", "summon") + [
        say("封印一个接一个打开，别站在线上。", gloss=True, name="七印开启："),
        pp_sound("load_spell", 1, 0.8, 48),
        "particle %s ~ ~1 ~ 0 0 0 0 1 force" % HOLY_FLASH,
    ])
    fires = ["execute if score #st %s matches %d rotated %.1f 0 positioned ^ ^%d ^%d run function %s/fx/lance_seal"
             % (O, SEAL_FIRST + i * SEAL_GAP, 360.0 * i / SEAL_COUNT, SEAL_HEIGHT, SEAL_RING, F) for i in range(SEAL_COUNT)]
    keep_casting = ["execute if score #st %s matches %d run function %s/clip/cast" % (O, t, F)
                    for t in range(SUMMON_END, SEALS_END - CAST_END, CAST_END)]
    w(b + "do_seals", fires + keep_casting + [
        "execute if score #st %s matches %d.. run function %s/boss/end" % (O, SEALS_END, F),
    ])

    # Last Judgment: he goes to the middle and the floor is lost, bar three seals
    refuges = []
    for k in range(4):
        for j in range(3):
            refuges.append("execute if score #r %s matches %d rotated %d 0 positioned ^ ^ ^%d positioned over motion_blocking_no_leaves "
                           "run function %s/fx/refuge" % (O, k, 30 * k + 120 * j, REFUGE_RING, F))
    w(b + "start_doom", starter("doom", "summon") + [
        say("圣所之外，皆是罪土。", gloss=True, name="最后的审判："),
        pp_sound("load_spell", 1, 0.6, 64),
        "particle %s ~ ~1 ~ 0 0 0 0 1 force" % HOLY_FLASH,
    ])
    w(b + "do_doom", [
        "execute if score #st %s matches 1 run function %s/boss/hide" % (O, F),
        "execute if score #st %s matches 2 at @e[%s] run tp @s ~ ~ ~" % (O, CENTER),
        "execute if score #st %s matches 2 run function %s/boss/doom_mark" % (O, F),
        "execute if score #st %s matches 5 run function %s/boss/show" % (O, F),
        "execute if score #st %s matches %d run function %s/clip/cast" % (O, SUMMON_END, F),
        "execute if score #st %s matches %d run function %s/boss/doom_toll" % (O, DOOM_TICKS - 40, F),
        "execute if score #st %s matches %d run function %s/boss/doom_toll" % (O, DOOM_TICKS - 20, F),
        "execute if score #st %s matches %d run function %s/boss/doom_strike" % (O, DOOM_TICKS, F),
        "execute if score #st %s matches %d.. run function %s/boss/doom_end" % (O, DOOM_TICKS + DOOM_REST, F),
    ])
    w(b + "doom_mark", [
        "# 全场圣印，加三处圣所；随机转一个角度。",
        "execute at @e[%s] positioned over motion_blocking_no_leaves run function %s/fx/doom_seal" % (CENTER, F),
        "execute store result score #r %s run random value 0..3" % O,
    ] + ["execute at @e[%s] %s" % (CENTER, line[len("execute "):]) for line in refuges])
    w(b + "doom_toll", ["playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 2 0.6"])
    pillars = 10
    w(b + "doom_strike", [
        "# 判定：全场玩家先记上，站在圣所里的再摘掉。",
        "execute at @e[%s] run tag @a[distance=..%d,%s] add rpg.pf.doomed" % (CENTER, DOOM_RADIUS, SURVIVORS),
        "execute as @e[type=minecraft:text_display,tag=rpg.pf.refuge] at @s run tag @a[distance=..%s] remove rpg.pf.doomed" % (REFUGE_RADIUS + 0.5),
        "execute as @a[tag=rpg.pf.doomed] at @s run function %s/boss/doom_hit" % F,
        "tag @a[tag=rpg.pf.doomed] remove rpg.pf.doomed",
        "kill @e[type=minecraft:text_display,tag=rpg.pf.refuge]",
        "kill @e[type=minecraft:item_display,tag=rpg.pf.refdisc]",
        "execute at @e[%s] run particle %s ~ ~1 ~ 0 0 0 0 1 force" % (CENTER, HOLY_FLASH),
        "playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..64] ~ ~ ~ 2 0.8",
        "playsound minecraft:entity.generic.explode hostile @a[distance=..64] ~ ~ ~ 1.5 0.7",
    ] + ["execute at @e[%s] rotated %d 0 positioned ^ ^ ^%d positioned over motion_blocking_no_leaves run function %s/fx/pillar"
         % (CENTER, 360 * i // pillars, 20, F) for i in range(pillars)] + [
        "# 他也耗尽了：这几秒没有护甲，也不出手。",
        "attribute @s minecraft:armor base set 0",
        "function %s/clip/idle" % F,
    ])
    w(b + "doom_hit", [
        "damage @s %d minecraft:indirect_magic by @e[%s]" % (DOOM_DAMAGE, BOSS),
        "execute positioned ~ ~1 ~ run function %s/fx/impact" % F,
    ])
    w(b + "doom_end", ["attribute @s minecraft:armor base set 10", "function %s/boss/end" % F])


def write_heart():
    h = "heart/"
    w(h + "spawn", [
        "# 判定体 + 模型（at 地面）。升起结束前打不到，也不算恶魔。",
        'summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.pf.heart"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,'
        'CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",CustomName:{text:"末影之心",color:"%s",bold:true},'
        'active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}' % VOID,
        "function rpg:heart_of_ender/spawn",
        "tag @e[type=minecraft:armor_stand,tag=rpg.he,tag=!rpg.pf.rig,distance=..1,limit=1] add rpg.pf.rig",
        "execute as @e[%s] run function %s/heart/init" % (HEART, F),
    ])
    w(h + "init", [
        "attribute @s minecraft:max_health base set %d" % HEART_HEALTH,
        "attribute @s minecraft:scale base set %s" % HITBOX_SCALE,
        "attribute @s minecraft:knockback_resistance base set 1",
        "data merge entity @s {Health:%d.0f}" % HEART_HEALTH,
        setv("last", HEART_HEALTH), setv("h", 0), setv("bl", 0),
        setv("seq", 0), setv("walking", 0), setv("weak", 0), setv("ba", 0),
        setv("ultq", 0), setv("ulti", 0), setv("ultcd", HEART_ULT_EVERY), setv("ultl", HEART_ULT_LINES[0]),
        "execute facing entity @a[distance=..%d,%s,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0" % (BAR_RANGE, SURVIVORS),
        "tp @e[%s] @s" % RIG,
        "function %s/heart/start_rise" % F,
    ])

    # a clip eases in from wherever the last one left the 21 parts
    for clip in ("idle", "walk", "mortar", "cross_beam", "sink", "death"):
        w(h + "clip/" + clip, [
            "execute as @e[%s] at @s run function rpg:heart_of_ender/anim/enter/%s" % (RIG, clip),
            "scoreboard players set @e[%s] rpg_he_run 0" % RIG,
            "execute as @e[%s] on passengers run data merge entity @s {interpolation_duration:%d}" % (RIG, BLEND),
            setv("bl", BLEND),
        ])
    w(h + "blend_tick", [
        "scoreboard players remove #bl %s 1" % O,
        "execute if score #bl %s matches 0 run scoreboard players set @e[%s] rpg_he_run 1" % (O, RIG),
    ])

    w(h + "tick", [
        "# 末影之心一刻（as、at 判定体）。",
        "scoreboard players add #h %s 1" % O,
        "execute if score #h %s matches 5.. run function %s/heart/read" % (O, F),
        "execute unless score #stage %s matches 4 run return 0" % O,
        "execute if score #bl %s matches 1.. run function %s/heart/blend_tick" % (O, F),
        "execute if score #cd %s matches 1.. run scoreboard players remove #cd %s 1" % (O, O),
        "execute if score #ultcd %s matches 1.. run scoreboard players remove #ultcd %s 1" % (O, O),
        "execute if entity @e[%s,limit=1] as @e[%s] at @s run function %s/heart/face_tick" % (FACE, FACE, F),
        "execute if score #sk %s matches 1.. run return run function %s/heart/skill" % (O, F),
        "execute unless entity @a[%s] run return run function %s/heart/stop" % (TARGET, F),
        "function %s/heart/free" % F,
    ])
    w(h + "read", [
        "# 每 5 刻读一次血量（一次 NBT），外壳把这段时间的伤害退回七成；再选目标。",
        setv("h", 0),
        "execute store result score #hp %s run data get entity @s Health" % O,
        "scoreboard players operation #lost %s = #last %s" % (O, O),
        "scoreboard players operation #lost %s -= #hp %s" % (O, O),
        "execute if score #lost %s matches 1.. run function %s/heart/hurt" % (O, F),
        "scoreboard players operation #last %s = #hp %s" % (O, O),
        "execute store result bossbar minecraft:pope value run scoreboard players get #hp %s" % O,
        "function %s/bar/hp" % F,
        "execute if score #hp %s matches ..%d run return run function %s/heart/die" % (O, DEATH_AT, F),
    ] + ["execute if score #ultl %s matches %d if score #hp %s matches ..%d run function %s/heart/ult_due"
         % (O, line, O, line, F) for line in HEART_ULT_LINES] + [
        "tag @a[tag=rpg.pf.tgt] remove rpg.pf.tgt",
        "tag @a[distance=..%d,%s,sort=nearest,limit=1] add rpg.pf.tgt" % (BAR_RANGE, SURVIVORS),
    ])
    w(h + "hurt", [
        "execute unless score #weak %s matches 1 run function %s/heart/refund" % (O, F),
        he_sound("hurt", 0.8, 1, 24),
        "particle %s ~ ~3 ~ 0.8 1.5 0.8 0.05 12 normal" % VOID_DUST,
    ])
    w(h + "refund", [
        "scoreboard players operation #lost %s *= #keep %s" % (O, O),
        "scoreboard players operation #lost %s /= #ten %s" % (O, O),
        "scoreboard players operation #hp %s += #lost %s" % (O, O),
        "execute store result entity @s Health float 1 run scoreboard players get #hp %s" % O,
        "# 血量涨回来不是挨打：对齐受伤基准，否则下一刻 rpg.hurt 又触发一次裁决。",
        "scoreboard players operation @s damage_timing = #hp %s" % O,
        "scoreboard players operation @s damage_action = #hp %s" % O,
    ])

    # crawling: a yaw limit so it swings round, and a half-plane test for the
    # side the target is on (a ball this big is flat where it matters).  Dead
    # ahead does nothing, dead behind has to pick a side.
    w(h + "steer", [
        "execute rotated ~ 0 positioned ^1000 ^ ^ if entity @a[%s,distance=..999.5] at @s run return run function %s/heart/turn_left" % (TARGET, F),
        "execute rotated ~ 0 positioned ^-1000 ^ ^ if entity @a[%s,distance=..999.5] at @s run return run function %s/heart/turn_right" % (TARGET, F),
        "execute rotated ~ 0 positioned ^ ^ ^-1000 if entity @a[%s,distance=..1000] at @s run function %s/heart/turn_right" % (TARGET, F),
    ])
    w(h + "free", [
        "function %s/heart/steer" % F,
        "execute if score #cd %s matches 0 run return run function %s/heart/choose" % (O, F),
        "scoreboard players add #ba %s 1" % O,
        "execute if score #ba %s matches %d.. run return run function %s/heart/basic" % (O, BASIC_EVERY, F),
        "execute if entity @a[%s,distance=..%d] run return run function %s/heart/stop" % (TARGET, STOP_NEAR, F),
        "execute unless entity @a[%s,distance=..%d] run function %s/heart/go" % (TARGET, WALK_FAR, F),
        "execute if score #walking %s matches 1 if score #bl %s matches 0 at @s positioned ^ ^ ^%s "
        "positioned over motion_blocking_no_leaves run function %s/heart/place" % (O, O, HEART_SPEED, F),
    ])
    w(h + "turn_left", ["tp @s ~ ~ ~ ~-%d 0" % HEART_TURN, "tp @e[%s] @s" % RIG])
    w(h + "turn_right", ["tp @s ~ ~ ~ ~%d 0" % HEART_TURN, "tp @e[%s] @s" % RIG])
    w(h + "place", ["tp @s ~ ~ ~", "tp @e[%s] @s" % RIG])
    w(h + "go", [
        "execute if score #walking %s matches 1 run return 0" % O,
        setv("walking", 1),
        "function %s/heart/clip/walk" % F,
    ])
    w(h + "stop", [
        "execute if score #walking %s matches 0 run return 0" % O,
        setv("walking", 0),
        "function %s/heart/clip/idle" % F,
    ])

    w(h + "choose", [
        "# 大招优先；目标跑远就潜地追上；否则六招轮换，破绽落在固定的位置上。",
        "execute if score #ultq %s matches 1 run return run function %s/heart/start_ult" % (O, F),
        "execute if score #ultcd %s matches 0 run return run function %s/heart/start_ult" % (O, F),
        "execute unless entity @a[%s,distance=..%d] run return run function %s/heart/start_sink" % (TARGET, SINK_BEYOND, F),
        "scoreboard players add #seq %s 1" % O,
        "execute if score #seq %s matches 6.. run %s" % (O, setv("seq", 0)),
        "execute if score #seq %s matches 1 run return run function %s/heart/start_mortar" % (O, F),
        "execute if score #seq %s matches 2 run return run function %s/heart/start_vent" % (O, F),
        "execute if score #seq %s matches 3 run return run function %s/heart/start_cross" % (O, F),
        "execute if score #seq %s matches 4 run return run function %s/heart/start_gaze" % (O, F),
        "execute if score #seq %s matches 5 run return run function %s/heart/start_nova" % (O, F),
        "function %s/heart/start_sink" % F,
    ])
    w(h + "ult_due", [setv("ultq", 1)] + [
        "execute if score #ultl %s matches %d run return run %s" % (O, line, setv("ultl", later))
        for line, later in zip(HEART_ULT_LINES, list(HEART_ULT_LINES[1:]) + [0])])
    w(h + "start_ult", [
        "# 大招：血量到线或时钟走完，先到先出。三招轮流。",
        setv("ultq", 0), setv("ultcd", HEART_ULT_EVERY),
        "scoreboard players add #ulti %s 1" % O,
        "execute if score #ulti %s matches 1 run return run function %s/heart/start_faces" % (O, F),
        "execute if score #ulti %s matches 2 run return run function %s/heart/start_collapse" % (O, F),
        setv("ulti", 0),
        "function %s/heart/start_cata" % F,
    ])
    w(h + "basic", [
        "# 普攻（爬行途中）：近了咬，远了吐。不打断下一招的计时。",
        setv("ba", 0),
        "execute if entity @a[%s,distance=..%d] run return run function %s/heart/start_bite" % (TARGET, BITE_NEAR, F),
        "execute if entity @a[%s,distance=..%d] run function %s/heart/start_spit" % (TARGET, SPIT_REACH, F),
    ])

    def starter(name, clip):
        return [setv("sk", HEART_SKILLS[name]), setv("st", 0), setv("walking", 0), "function %s/heart/clip/%s" % (F, clip)]

    w(h + "clip/snap", [
        "# 它没有普攻动作：迫击动作从张嘴前一点切入，再切回待机，看起来就是一口咬合。",
        "execute as @e[%s] at @s run function rpg:heart_of_ender/anim/enter/mortar" % RIG,
        "scoreboard players set @e[%s] rpg_he_t %d" % (RIG, OPEN_FROM),
        "execute as @e[%s] at @s run function rpg:heart_of_ender/anim/mortar/f%d" % (RIG, OPEN_FROM),
        "scoreboard players set @e[%s] rpg_he_run 0" % RIG,
        "execute as @e[%s] on passengers run data merge entity @s {interpolation_duration:%d}" % (RIG, OPEN_BLEND),
        setv("bl", OPEN_BLEND),
    ])
    w(h + "start_bite", starter("bite", "snap"))
    w(h + "start_spit", starter("spit", "snap"))
    w(h + "do_bite", [
        "execute if score #st %s matches %d run function %s/heart/bite_hit" % (O, BITE_HIT, F),
        "execute if score #st %s matches %d.. run function %s/heart/basic_end" % (O, BITE_END, F),
    ])
    w(h + "bite_hit", [
        "# 咬：身前一块。",
        "execute positioned ^ ^ ^%d as @a[distance=..%s,%s] run damage @s %d minecraft:indirect_magic by @e[%s]"
        % (BITE_AHEAD, BITE_RADIUS, SURVIVORS, BITE_DAMAGE, HEART),
        "execute positioned ^ ^2 ^%d run function %s/fx/impact_void" % (BITE_AHEAD, F),
        "particle %s ^ ^1 ^%d 1 0.5 1 0.1 16 normal" % (VOID_DUST_BIG, BITE_AHEAD),
        "playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..32] ~ ~ ~ 1 0.6",
    ])
    w(h + "do_spit", [
        "execute if score #st %s matches %d positioned %s facing entity @a[%s] eyes run function %s/fx/spit" % (O, BITE_HIT, MOUTH, TARGET, F),
        "execute if score #st %s matches %d.. run function %s/heart/basic_end" % (O, BITE_END, F),
    ])
    w(h + "basic_end", [
        "# 普攻不重置 #cd：下一招照常到点。",
        setv("sk", 0), setv("st", 0), setv("walking", 0),
        "function %s/heart/clip/idle" % F,
    ])
    write_heart_ults(starter)
    w(h + "start_mortar", starter("mortar", "mortar"))
    w(h + "start_cross", starter("cross", "cross_beam") + [
        "# 光束每次换方向，起手角也错开 45 度。",
        "scoreboard players add #dir %s 1" % O,
        "execute if score #dir %s matches 2.. run %s" % (O, setv("dir", 0)),
        "function %s/heart/weak_on" % F,
    ])
    w(h + "start_nova", starter("nova", "mortar"))
    w(h + "start_vent", starter("vent", "mortar"))
    w(h + "start_sink", starter("sink", "sink") + [
        "execute positioned over motion_blocking_no_leaves run function %s/fx/puddle_warn" % F,
    ])
    w(h + "start_rise", [
        setv("sk", HEART_SKILLS["rise"]), setv("st", 0), setv("walking", 0),
        "execute as @e[%s] at @s run function rpg:heart_of_ender/anim/enter/rise" % RIG,
    ])
    w(h + "skill", [
        "scoreboard players add #st %s 1" % O,
    ] + ["execute if score #sk %s matches %d run return run function %s/heart/do_%s" % (O, sid, F, name)
         for name, sid in HEART_SKILLS.items()])
    w(h + "end", [
        setv("sk", 0), setv("st", 0), setv("cd", HEART_BREATHER), setv("walking", 0),
        "function %s/heart/clip/idle" % F,
    ])

    w(h + "do_rise", [
        "execute if score #st %s matches %d run function %s/heart/rise_hit" % (O, RISE_HIT, F),
        "execute if score #st %s matches %d.. run function %s/heart/rise_done" % (O, RISE_END, F),
    ])
    w(h + "rise_hit", [
        "# 破土：离得太近的玩家被掀飞。",
        "execute as @a[distance=..%d,%s] run damage @s %d minecraft:indirect_magic by @e[%s]" % (RISE_RADIUS, SURVIVORS, RISE_DAMAGE, HEART),
        "function %s/fx/shock_big" % F,
        "particle %s ~ ~0.5 ~ 2 0.3 2 0.1 48 normal" % VOID_DUST_BIG,
    ])
    w(h + "rise_done", [
        "# 从这里起他就是恶魔了，契约技能重新生效。",
        "data merge entity @s {Invulnerable:0b}",
        "tag @s add rpg.demon",
        "function %s/heart/end" % F,
    ])

    # 13 shells around a player: one on them, a ring of 6 at 4, a ring of 6 at 8
    def mortar_lines():
        rings = [(0, 0)] + [(4, 60 * i) for i in range(6)] + [(8, 30 + 60 * i) for i in range(6)]
        lines = []
        for k, (r, a) in enumerate(rings):
            at = SHELL_FIRST + k * SHELL_GAP
            x, z = r * math.sin(math.radians(a)), r * math.cos(math.radians(a))
            lines.append("execute if score #st %s matches %d positioned %s rotated ~%d -65 run function %s/fx/shell_up"
                         % (O, at, MOUTH, a - 180, F))
            lines.append("execute if score #st %s matches %d at @a[distance=..%d,%s,sort=random,limit=1] rotated ~ 0 positioned ^%.1f ^ ^%.1f "
                         "positioned over motion_blocking_no_leaves run function %s/fx/mark_warn"
                         % (O, at, ARENA, SURVIVORS, x, z, F))
        return lines

    w(h + "do_mortar", ["# 十三发迫击：嘴里吐出去，落点先亮圈。"] + mortar_lines() + [
        "execute if score #st %s matches %d.. run function %s/heart/end" % (O, CLIP_END, F),
    ])

    w(h + "do_cross", [
        "execute if score #st %s matches %d run function %s/heart/cross_fire" % (O, BLEND, F),
        "execute if score #h %s matches 0 positioned %s run function %s/heart/weak_fx" % (O, FIGURE, F),
        "execute if score #st %s matches %d.. run function %s/heart/cross_done" % (O, CLIP_END, F),
    ])
    w(h + "cross_fire", ["# 四束光：先是细线，一秒后才变粗开始扫。",
                         "execute positioned %s run function %s/fx/flare" % (FIGURE, F)] + [
        "execute if score #dir %s matches %d positioned %s rotated ~%d 0 run function %s/fx/beam_warn"
        % (O, d, FIGURE, (1 - d) * 45 + 90 * i, F)
        for d in (0, 1) for i in range(4)
    ])
    w(h + "do_nova", [
        "execute if score #st %s matches %d positioned over motion_blocking_no_leaves run function %s/fx/nova" % (O, SHELL_FIRST, F),
        "execute if score #st %s matches %d positioned over motion_blocking_no_leaves run function %s/fx/nova" % (O, SHELL_FIRST + NOVA_GAP, F),
        "execute if score #st %s matches %d.. run function %s/heart/end" % (O, CLIP_END, F),
    ])
    w(h + "do_vent", [
        "execute if score #st %s matches %d facing entity @a[%s] feet rotated ~ 0 positioned ^ ^ ^%d "
        "positioned over motion_blocking_no_leaves run function %s/fx/vent" % (O, SHELL_FIRST + k * VENT_GAP, TARGET, 4 + 3 * k, F)
        for k in range(VENT_COUNT)
    ] + ["execute if score #st %s matches %d.. run function %s/heart/end" % (O, CLIP_END, F)])
    w(h + "cross_done", ["function %s/heart/weak_off" % F, "function %s/heart/end" % F])
    w(h + "weak_on", [
        "# 破绽：外壳减伤取消，血条转金，体内小人的轮廓透出来。",
        setv("weak", 1),
        setv("hudl", -1),
    ] + inner_glow(True))
    w(h + "weak_off", [
        setv("weak", 0),
        setv("hudl", -1),
    ] + inner_glow(False))
    w(h + "weak_fx", ["particle end_rod ~ ~ ~ 0.4 0.5 0.4 0.02 6 normal"])

    w(h + "do_sink", [
        "execute if score #st %s matches %d run function %s/heart/sink_under" % (O, SINK_END, F),
        "execute if score #st %s matches %d.. run function %s/heart/start_rise" % (O, SINK_END + SINK_WARN, F),
    ])
    w(h + "sink_under", [
        "# 在地下换位置：这段时间打不到，也算不上恶魔。",
        "data merge entity @s {Invulnerable:1b}",
        "tag @s remove rpg.demon",
        "execute at @a[%s] rotated ~ 0 positioned ^ ^ ^4 positioned over motion_blocking_no_leaves "
        "facing entity @a[%s] feet rotated ~ 0 run function %s/heart/sink_place" % (TARGET, TARGET, F),
    ])
    w(h + "sink_place", [
        "tp @s ~ ~ ~ ~ 0",
        "tp @e[%s] @s" % RIG,
        "function %s/fx/puddle_warn" % F,
    ])

    w(h + "die", [
        "# 倒下（判定体可能已被打穿）。模型留到动作放完。",
        "execute as @e[%s] at @s run tp @e[%s] ~ ~ ~" % (RIG, CENTER),
        "function %s/heart/weak_off" % F,
        "kill @e[type=minecraft:vindicator,tag=rpg.pf.heart]",
        "tag @a[tag=rpg.pf.tgt] remove rpg.pf.tgt",
        "execute as @e[%s] at @s run function rpg:arch_visage/internal/clear" % FACE,
        "kill @e[%s]" % FX,
        setv("stage", 5), setv("t", 0),
        "bossbar set minecraft:pope value 0",
        bar_name("heart", 0),
        "function %s/heart/clip/death" % F,
        say("……结束了……吗……", "末影之心", True),
    ])
    w(h + "shatter", [
        "execute positioned ~ ~3 ~ run function %s/fx/burst_void" % F,
        "particle %s ~ ~3 ~ 1.5 2 1.5 0.2 96 force" % VOID_DUST_BIG,
        "particle %s ~ ~3 ~ 0 0 0 0 1 force" % VOID_FLASH,
        "execute as @e[%s] at @s run function rpg:heart_of_ender/internal/clear" % RIG,
    ])

    # the covenants: a fixed hit instead of a share of max health
    for name, damage in COVENANT_DAMAGE.items():
        w(h + name + "_target", [
            "# 新约技能打到末影之心：固定 %d，没有斩杀线；外壳照常吃掉七成。" % damage,
            "scoreboard players set @s rpg_lt_max %d" % (damage * 100),
            "function rpg:divine/damage/apply_score",
            "particle minecraft:enchanted_hit ~ ~3 ~ 0.8 1.5 0.8 0.1 16 normal",
        ])


def write_heart_ults(starter):
    h = "heart/"

    def face(name, mark):
        w(h + name, [
            "# 一张面容（at 地面，rotated 为朝向）。只有一段动作：升起、张嘴、沉下去。",
            "function rpg:arch_visage/debug/spawn",
            "tag @e[type=minecraft:armor_stand,tag=rpg.av,tag=!rpg.pf.face,distance=..1] add %s" % mark,
            "execute as @e[type=minecraft:armor_stand,tag=%s,tag=!rpg.pf.face,distance=..1] run tp @s ~ ~ ~ ~ 0" % mark,
            "scoreboard players set @e[type=minecraft:armor_stand,tag=%s,tag=!rpg.pf.face,distance=..1] %s %d" % (mark, LIFE, FACE_LIFE),
            "tag @e[type=minecraft:armor_stand,tag=%s,tag=!rpg.pf.face,distance=..1] add rpg.pf.face" % mark,
        ])

    face("face_gaze", "rpg.pf.chase")
    face("face_cw", "rpg.pf.cw")
    face("face_ccw", "rpg.pf.ccw")
    sweeping = "execute if score @s %s matches %d..%d" % (LIFE, FACE_CLOSE, FACE_THICK)
    w(h + "face_tick", [
        "# 面容一刻（as、at 盔甲架）。光束由盔甲架带着走。",
        "scoreboard players remove @s %s 1" % LIFE,
        "execute if score @s %s matches %d at @s positioned %s run function %s/fx/face_beam" % (LIFE, FACE_OPEN, AV_MOUTH, F),
        "%s if entity @s[tag=rpg.pf.chase] run function %s/heart/face_chase" % (sweeping, F),
        "%s if entity @s[tag=rpg.pf.cw] at @s run tp @s ~ ~ ~ ~%s 0" % (sweeping, FACE_SPIN),
        "%s if entity @s[tag=rpg.pf.ccw] at @s run tp @s ~ ~ ~ ~-%s 0" % (sweeping, FACE_SPIN),
        "execute if score @s %s matches %d..%d at @s positioned %s as @e[type=minecraft:text_display,tag=rpg.pf.fbeam,distance=..3,limit=3] run tp @s ~ ~ ~ ~ 0"
        % (LIFE, FACE_GONE, FACE_OPEN, AV_MOUTH),
        "%s if score #h %s matches 0 at @s positioned %s run function %s/heart/face_ray" % (sweeping, O, AV_MOUTH, F),
        "execute if score @s %s matches ..0 run function rpg:arch_visage/internal/clear" % LIFE,
    ])
    w(h + "face_chase", [
        "# 凝视：光束慢慢转向目标，一直走动就追不上。",
        "execute at @s positioned %s rotated ~ 0 positioned ^1000 ^ ^ if entity @a[%s,distance=..999.5] at @s run return run tp @s ~ ~ ~ ~-%s 0"
        % (AV_MOUTH, TARGET, FACE_TURN),
        "execute at @s positioned %s rotated ~ 0 positioned ^-1000 ^ ^ if entity @a[%s,distance=..999.5] at @s run tp @s ~ ~ ~ ~%s 0"
        % (AV_MOUTH, TARGET, FACE_TURN),
    ])
    w(h + "face_ray", [setv("d", 0), "execute positioned ^ ^-0.9 ^2 run function %s/fx/face_step" % F])

    # the visage as a skill: three faces around the target, each chasing them
    w(h + "start_gaze", starter("gaze", "mortar"))
    w(h + "do_gaze", [
        "execute if score #st %s matches %d run function %s/heart/gaze_faces" % (O, BLEND + 4, F),
        "execute if score #st %s matches %d.. run function %s/heart/end" % (O, CLIP_END, F),
    ])
    w(h + "gaze_faces", ["# 末影面容：目标周围升起三张。"] + [
        "execute at @a[%s] rotated ~%d 0 positioned ^ ^ ^%d positioned over motion_blocking_no_leaves "
        "facing entity @a[%s] feet rotated ~ 0 run function %s/heart/face_gaze" % (TARGET, 120 * i, GAZE_RING, TARGET, F)
        for i in range(3)
    ] + [he_sound("mortar_explode", 0.5, 0.6)])

    # first ultimate: two rings of faces, their beams turning like spokes
    second = BLEND + 8 + FACE_LIFE - 2
    w(h + "start_faces", starter("faces", "mortar") + [
        say("这些都是被圣座吃掉的脸。别站到光束里。", "末影之心", True, "千面降临："),
        he_sound("mortar_explode", 1, 0.5, 48),
        "particle %s ~ ~3 ~ 0 0 0 0 1 force" % VOID_FLASH,
    ])
    w(h + "do_faces", [
        "execute if score #st %s matches %d run function %s/heart/faces_one" % (O, BLEND + 8, F),
        "execute if score #st %s matches %d run function %s/heart/clip/mortar" % (O, CLIP_END - 6, F),
        "execute if score #st %s matches %d run function %s/heart/faces_two" % (O, second, F),
        "execute if score #st %s matches %d.. run function %s/heart/end" % (O, second + FACE_LIFE, F),
    ])
    for name, spin, turn in (("faces_one", "face_cw", 0), ("faces_two", "face_ccw", 30)):
        w(h + name, ["# 一圈面容，朝向圈心，张嘴后一起转。"] + [
            "execute at @a[%s] rotated %d 0 positioned ^ ^ ^%d positioned over motion_blocking_no_leaves rotated ~180 0 run function %s/heart/%s"
            % (TARGET, turn + 360 * i // RING_FACES, RING_RADIUS, F, spin) for i in range(RING_FACES)
        ] + [he_sound("mortar_explode", 0.7, 0.6, 48)])

    # second ultimate: get out of the circle before it falls in
    boom = BLEND + COLLAPSE_TICKS
    w(h + "start_collapse", starter("collapse", "mortar") + [
        say("圣器的底，是空的。跑出那个圈。", "末影之心", True, "虚空坍缩："),
        "execute positioned over motion_blocking_no_leaves run function %s/fx/collapse" % F,
        he_sound("mortar_explode", 1, 0.5, 48),
    ])
    w(h + "do_collapse", [
        "execute if score #h %s matches 0 if score #st %s matches ..%d run function %s/heart/collapse_pull" % (O, O, boom, F),
        "execute if score #st %s matches %d run function %s/heart/clip/mortar" % (O, CLIP_END - 6, F),
        "execute if score #st %s matches %d run function %s/heart/collapse_boom" % (O, boom, F),
        "execute if score #st %s matches %d.. run function %s/heart/cross_done" % (O, boom + COLLAPSE_REST, F),
    ])
    w(h + "collapse_pull", [
        "# 圈里的人走不快；碎屑一路往中心吸。",
        "effect give @a[distance=..%d,%s] minecraft:slowness 1 0 true" % (COLLAPSE_RADIUS, SURVIVORS),
        "particle minecraft:portal ~ ~1 ~ %d 0.4 %d 0.8 60 force" % (COLLAPSE_RADIUS // 2, COLLAPSE_RADIUS // 2),
    ])
    w(h + "collapse_boom", [
        "# 外壳也炸开了：之后这几秒是破绽。",
        "execute as @a[distance=..%d,%s] run damage @s %d minecraft:indirect_magic by @e[%s]" % (COLLAPSE_RADIUS, SURVIVORS, COLLAPSE_DAMAGE, HEART),
        "execute positioned ~ ~3 ~ run function %s/fx/flare_burst" % F,
        "particle %s ~ ~1 ~ 6 1 6 0.3 96 force" % VOID_DUST_BIG,
        "particle %s ~ ~3 ~ 0 0 0 0 1 force" % VOID_FLASH,
        he_sound("mortar_explode", 1.5, 0.5, 64),
        "playsound minecraft:entity.generic.explode hostile @a[distance=..64] ~ ~ ~ 1.5 0.6",
        "function %s/heart/weak_on" % F,
        "function %s/heart/clip/idle" % F,
    ])

    # third ultimate: eight beams, there and back, with the shell open throughout
    back = BLEND + BEAM_LIFE + 4
    w(h + "start_cata", starter("cata", "cross_beam") + [
        say("跪下，对着这十字。贴近我，或者跟着光跑。", "末影之心", True, "十字灾变："),
        setv("dir", 0),
        "function %s/heart/weak_on" % F,
        he_sound("mortar_explode", 1, 0.5, 48),
    ])
    w(h + "do_cata", [
        "execute if score #st %s matches %d run function %s/heart/cata_fire" % (O, BLEND, F),
        "execute if score #st %s matches %d run function %s/heart/clip/cross_beam" % (O, back, F),
        "execute if score #st %s matches %d run function %s/heart/cata_back" % (O, back + BLEND, F),
        "execute if score #h %s matches 0 positioned %s run function %s/heart/weak_fx" % (O, FIGURE, F),
        "execute if score #st %s matches %d.. run function %s/heart/cross_done" % (O, back + CLIP_END, F),
    ])
    w(h + "cata_fire", ["# 八束光：比十字光束多一倍，缝隙比扫过的角度窄，站着不动躲不开。",
                        "execute positioned %s run function %s/fx/flare" % (FIGURE, F)] + [
        "execute positioned %s rotated ~%d 0 run function %s/fx/beam_warn" % (FIGURE, 45 * i, F) for i in range(8)
    ])
    w(h + "cata_back", [setv("dir", 1), "function %s/heart/cata_fire" % F])


def inner_glow(on):
    merge = "{Glowing:1b,glow_color_override:%d}" % int(HOLY.lstrip("#"), 16) if on else "{Glowing:0b}"
    return ["execute as @e[%s] on passengers if entity @s[tag=rpg.he.p.%s] run data merge entity @s %s" % (RIG, part, merge)
            for part in ("inner_body", "inner_head", "inner_arm_left", "inner_arm_right", "inner_leg_left", "inner_leg_right")]


def main():
    write_common()
    write_fx()
    write_stages()
    write_boss()
    write_heart()
    write_clips()


if __name__ == "__main__":
    main()
