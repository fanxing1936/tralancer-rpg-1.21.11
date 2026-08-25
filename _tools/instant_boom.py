# -*- coding: utf-8 -*-
"""把旧版“瞬爆苦力怕”迁移成不会破坏地形的伪爆炸。

原包用 ``Fuse:0`` 苦力怕表达武器/技能瞬爆；旧迁移曾把它们换成
``fuse:0`` TNT。TNT 虽然真正瞬发，却会炸坏地图。现在改成粒子、声音与
两段距离伤害：仍有爆炸的可读性、衰减和击退方向，但世界里不再生成任何
爆炸实体，所以不会修改方块。

只处理这里明确识别出的 ``summon creeper ... {ExplosionRadius, Fuse:0}``。
普通 TNT、非零引信、TNT 矿车和玩家放置的 TNT 都不在本脚本范围内。

多人归属：胸甲殉爆和疾风弓分别绑定穿戴者/箭矢 origin；Boss 的近身爆发、
逐玩家爆发和二阶段侍从爆发都先锁定当前 Boss，再结算伤害。无可靠施法者的
旧入口使用位置型爆炸伤害，不伪造击杀归属。
"""
from __future__ import print_function

import io
import os
import re
import sys


ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(ROOT, "data/rpg/function")
POWERS = (1, 2, 3, 4, 5, 8)
SOURCE_TAG = "rpg.pseudo_boom.source"
CENTER_TAG = "rpg.pseudo_boom.center"
MINION_NEW_TAG = "rpg.pseudo_boom.minion_new"

CALL = re.compile(
    r"summon\s+(?:minecraft:)?creeper\s+(?P<pos>\S+\s+\S+\s+\S+)\s*"
    r"\{(?P<nbt>[^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")
RADIUS = re.compile(r'"?ExplosionRadius"?\s*:\s*([0-9.]+)')


def path(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep))


def write(rel, body):
    p = path(rel)
    parent = os.path.dirname(p)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    io.open(p, "w", encoding="utf-8", newline="\n").write(
        body.rstrip("\n") + "\n")


def power_of(match):
    found = RADIUS.search(match.group("nbt"))
    power = float(found.group(1)) if found else 4.0
    rounded = int(round(power))
    if abs(power - rounded) > 0.0001 or rounded not in POWERS:
        raise AssertionError("unsupported pseudo explosion power: %s" % power)
    return rounded


def positioned_call(pos, target):
    return "execute positioned %s run function rpg:effect/pseudo_explosion/%s" % (
        pos, target)


def convert_for(rel, line, match):
    """Convert one known legacy instant blast without widening the boundary."""
    power = power_of(match)
    pos = match.group("pos")

    if rel == "entities/warden/warden.mcfunction":
        if "devil matches 50 " in line and power == 8:
            return positioned_call(pos, "owned_p8")
        # These two need the Boss executor that exists before the old command
        # switches to a player/minion. They are replaced as whole tails below.
        return positioned_call(pos, "p%d" % power)

    if rel == "item/chestplate/off.mcfunction" and power == 5:
        return positioned_call(pos, "owned_p5")

    if rel == "item/bow/speed.mcfunction" and power == 3:
        # The helper prefers the real origin but falls back to an unowned blast
        # if that shooter has logged out or its entity is no longer available.
        return positioned_call(pos, "bow_p3")

    # Retired copies can still be present before the later legacy moderniser.
    # Preserve their spatial effect without inventing an unreliable owner.
    return positioned_call(pos, "p%d" % power)


def damage_lines(power, sourced):
    radius = power * 2.0
    inner = float(power)
    inner_damage = max(4, power * 4)
    outer_damage = max(2, power * 2)
    source = ((" by @e[type=minecraft:marker,tag=%s,distance=..0.1,limit=1]"
               " from @e[tag=%s,limit=1]") % (CENTER_TAG, SOURCE_TAG)
              if sourced else " at ~ ~ ~")
    exclude = ",tag=!%s" % SOURCE_TAG if sourced else ""
    return [
        ("execute as @e[distance=..%g%s] if data entity @s Health run damage "
         "@s %d minecraft:explosion%s") %
        (inner, exclude, inner_damage, source),
        ("execute as @e[distance=%g..%g%s] if data entity @s Health run damage "
         "@s %d minecraft:explosion%s") %
        (inner + 0.01, radius, exclude, outer_damage, source),
    ]


def visual_lines(power):
    spread = max(0.4, power * 0.22)
    count = 12 + power * 5
    pitch = max(0.55, 1.12 - power * 0.055)
    return [
        "# 伪爆炸：只有表现与伤害，不生成会改方块的爆炸实体。",
        "particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 force",
        "particle minecraft:large_smoke ~ ~0.4 ~ %g %g %g 0.08 %d force" %
        (spread, spread, spread, count),
        ("playsound minecraft:entity.generic.explode hostile "
         "@a[distance=..48] ~ ~ ~ 1 %g") % pitch,
    ]


def emit_functions():
    for power in POWERS:
        write("effect/pseudo_explosion/p%d.mcfunction" % power,
              "\n".join(visual_lines(power) + damage_lines(power, False)))
        write("effect/pseudo_explosion/sourced_p%d.mcfunction" % power,
              "\n".join([
                  "# 爆心 marker 只活在这次同步调用内：by=爆心保证击退方向，from=施法者保留归属。",
                  "kill @e[type=minecraft:marker,tag=%s]" % CENTER_TAG,
                  "summon minecraft:marker ~ ~ ~ {Tags:[\"%s\"]}" % CENTER_TAG,
              ] + visual_lines(power) + damage_lines(power, True) + [
                  "kill @e[type=minecraft:marker,tag=%s,distance=..0.1]" % CENTER_TAG,
              ]))
        write("effect/pseudo_explosion/owned_p%d.mcfunction" % power, """
# 调用时 @s 是真实施法者；同步临时标签不会跨玩家、跨刻泄漏。
tag @e[tag=%(TAG)s] remove %(TAG)s
tag @s add %(TAG)s
function rpg:effect/pseudo_explosion/sourced_p%(P)d
tag @s remove %(TAG)s
""" % {"TAG": SOURCE_TAG, "P": power})

    write("effect/pseudo_explosion/bow_p3.mcfunction", """
# 保持箭矢爆心。origin 存在时归属射手；射手已不可用时仍结算无主冲击。
execute on origin run return run function rpg:effect/pseudo_explosion/owned_p3
function rpg:effect/pseudo_explosion/p3
""")

    write("entities/warden/pseudo_burst_players.mcfunction", """
# @s=当前二阶段 Boss，执行位置=Boss。逐位玩家生成独立爆心，击杀归 Boss。
tag @e[tag=%(TAG)s] remove %(TAG)s
tag @s add %(TAG)s
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] at @s run function rpg:effect/pseudo_explosion/sourced_p3
tag @s remove %(TAG)s
""" % {"TAG": SOURCE_TAG})

    write("entities/warden/pseudo_burst_minions.mcfunction", """
# 只结算属于当前 Boss 唯一 id 的二阶段侍从。第一行的距离仅用于给升级前
# 没有 id 的近身旧侍从补归属；已有 id 后即使追出十二格，也会按时收尾。
tag @e[tag=%(TAG)s] remove %(TAG)s
tag @s add %(TAG)s
execute as @e[tag=devil2,tag=tick,distance=..12] unless score @s rpg_boom_id matches 1.. run scoreboard players operation @s rpg_boom_id = @e[tag=%(TAG)s,limit=1] rpg_boom_id
execute as @e[tag=devil2,tag=tick] if score @s rpg_boom_id = @e[tag=%(TAG)s,limit=1] rpg_boom_id at @s run function rpg:effect/pseudo_explosion/sourced_p4
execute as @e[tag=devil2,tag=tick] if score @s rpg_boom_id = @e[tag=%(TAG)s,limit=1] rpg_boom_id at @s run particle squid_ink ~1 ~1 ~1 -2 -1 -2 1 100
execute as @e[tag=devil2,tag=tick] if score @s rpg_boom_id = @e[tag=%(TAG)s,limit=1] rpg_boom_id run kill @s
tag @s remove %(TAG)s
""" % {"TAG": SOURCE_TAG})

    write("entities/warden/pseudo_id.mcfunction", """
# Boss 唯一 id 独立于四槽血条；即使四槽已满，近邻战斗也不会串侍从。
scoreboard players add #boom_seq rpg_boom_id 1
scoreboard players operation @s rpg_boom_id = #boom_seq rpg_boom_id
""")

    write("entities/warden/pseudo_minion_stamp.mcfunction", """
# @s 仍是召唤它的 Boss，执行位置是本次新侍从脚下。
scoreboard players operation @e[type=minecraft:vindicator,tag=%(NEW)s,distance=..1,limit=1,sort=nearest] rpg_boom_id = @s rpg_boom_id
tag @e[type=minecraft:vindicator,tag=%(NEW)s,distance=..1] remove %(NEW)s
""" % {"NEW": MINION_NEW_TAG})

    scoreboard = path("command/soreboard.mcfunction")
    body = io.open(scoreboard, encoding="utf-8").read().rstrip("\n")
    if "scoreboard objectives add rpg_boom_id " not in body:
        body += ("\n\n# 伪爆炸：Boss 与二阶段侍从的稳定归属\n"
                 "scoreboard objectives add rpg_boom_id dummy")
        io.open(scoreboard, "w", encoding="utf-8", newline="\n").write(body + "\n")


def patch_warden_relations(text):
    lines = text.splitlines()
    out = [
        "# 伪爆炸 Boss/侍从归属；唯一 id 与四槽血条容量无关。",
        "execute as @e[tag=boss] unless score @s rpg_boom_id matches 1.. run function rpg:entities/warden/pseudo_id",
    ]
    players = minions = stamps = companions = 0
    for line in lines:
        if ("devil matches 250 " in line and "ExplosionRadius" in line and
                "as @a[distance=..10]" in line):
            line = (line[:line.index("as @a[distance=..10]")] +
                    "run function rpg:entities/warden/pseudo_burst_players")
            players += 1
        elif ("devil matches 390 " in line and "ExplosionRadius" in line and
              "tag=devil2" in line and "tag=tick" in line):
            line = (line[:line.index("run execute as @e")] +
                    "run function rpg:entities/warden/pseudo_burst_minions")
            minions += 1
        elif ("devil matches 390 " in line and
              "execute as @e[tag=devil2,tag=tick]" in line):
            # Particle and kill now live in pseudo_burst_minions beside the id
            # comparison; leaving either global companion would reintroduce
            # the exact cross-battle bug this pass removes.
            companions += 1
            continue
        elif ("devil matches 390 " in line and "run summon vindicator" in line and
              'Tags:["devil2","tick"]' in line):
            pos_match = re.search(r"run summon vindicator (?P<pos>\S+\s+\S+\s+\S+)", line)
            assert pos_match, "warden minion summon position missing"
            line = line.replace('Tags:["devil2","tick"]',
                                'Tags:["devil2","tick","%s"]' % MINION_NEW_TAG)
            out.append(line)
            prefix = line[:line.index("run summon vindicator")]
            out.append(prefix + "positioned %s run function rpg:entities/warden/pseudo_minion_stamp" %
                       pos_match.group("pos"))
            stamps += 1
            continue
        out.append(line)
    if players != 1 or minions != 1 or stamps != 4 or companions != 2:
        raise AssertionError("warden pseudo burst hooks not found exactly once")
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def main():
    emit_functions()
    hits = 0
    files = 0
    for base, _dirs, names in os.walk(FUNC):
        for name in names:
            if not name.endswith(".mcfunction"):
                continue
            p = os.path.join(base, name)
            rel = os.path.relpath(p, FUNC).replace("\\", "/")
            source = io.open(p, encoding="utf-8").read()
            if rel == "entities/warden/warden.mcfunction" and "ExplosionRadius" in source:
                source = patch_warden_relations(source)

            def repl(match):
                start = source.rfind("\n", 0, match.start()) + 1
                end = source.find("\n", match.end())
                if end < 0:
                    end = len(source)
                return convert_for(rel, source[start:end], match)

            target, count = CALL.subn(repl, source)
            if count:
                io.open(p, "w", encoding="utf-8", newline="\n").write(target)
                hits += count
                files += 1

    print("pseudo boom: %d 处瞬爆改成无地形破坏效果（%d 个文件）" %
          (hits, files))


if __name__ == "__main__":
    main()
