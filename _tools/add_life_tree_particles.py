# -*- coding: utf-8 -*-
"""Generate a persistent, ground-flat particle Tree of Life.

Each Sephirah is a one-block diameter ring.  The ten visible Sephiroth, the
dashed Daath ring and the traditional twenty-two paths are redrawn every ten
ticks from a marker whose yaw is copied from the placing player.
"""

import io
import math
import os
import sys

import rpg_ui_style as ui


DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")

NODES = {
    "kether": (0.00, -3.60, (1.00, 0.98, 0.88), "王冠"),
    "chokmah": (1.45, -2.55, (0.62, 0.64, 0.68), "智慧"),
    "binah": (-1.45, -2.55, (0.08, 0.08, 0.10), "理解"),
    "daath": (0.00, -1.58, (0.42, 0.56, 0.68), "知识"),
    "chesed": (1.45, -0.86, (0.12, 0.52, 0.82), "慈悲"),
    "geburah": (-1.45, -0.86, (0.78, 0.15, 0.18), "严厉"),
    "tiphareth": (0.00, 0.00, (0.96, 0.78, 0.23), "美丽"),
    "netzach": (1.45, 1.28, (0.25, 0.68, 0.28), "胜利"),
    "hod": (-1.45, 1.28, (0.92, 0.38, 0.16), "光辉"),
    "yesod": (0.00, 2.43, (0.52, 0.22, 0.68), "基础"),
    "malkuth": (0.00, 3.86, (0.48, 0.27, 0.19), "王国"),
}

# The canonical 22 paths.  Daath is shown as the hidden circle but is not a
# separate path endpoint, matching the reference diagram's translucent ring.
PATHS = [
    ("kether", "chokmah"), ("kether", "binah"), ("kether", "tiphareth"),
    ("chokmah", "binah"), ("chokmah", "chesed"), ("chokmah", "tiphareth"),
    ("binah", "geburah"), ("binah", "tiphareth"),
    ("chesed", "geburah"), ("chesed", "tiphareth"), ("chesed", "netzach"),
    ("geburah", "tiphareth"), ("geburah", "hod"),
    ("tiphareth", "netzach"), ("tiphareth", "hod"), ("tiphareth", "yesod"),
    ("netzach", "hod"), ("netzach", "yesod"), ("netzach", "malkuth"),
    ("hod", "yesod"), ("hod", "malkuth"), ("yesod", "malkuth"),
]


def fpath(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep))


def read(rel):
    with io.open(fpath(rel), encoding="utf-8") as handle:
        return handle.read()


def write(rel, content):
    target = fpath(rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content.rstrip("\n") + "\n")


def fmt(value):
    if abs(value) < 0.0005:
        value = 0.0
    return "%.3f" % value


def dust(color, x, z, scale=0.72, y=0.07):
    rgb = ",".join("%.2f" % channel for channel in color)
    return "particle dust{color:[%s],scale:%.2f} ^%s ^%.3f ^%s 0 0 0 0 1" % (rgb, scale, fmt(x), y, fmt(z))


def path_color(a, b):
    ax, _, _, _ = NODES[a]
    bx, _, _, _ = NODES[b]
    if ax == 0 and bx == 0:
        return (0.96, 0.76, 0.30)
    if ax > 0 and bx > 0:
        return (0.20, 0.66, 0.86)
    if ax < 0 and bx < 0:
        return (0.76, 0.18, 0.25)
    return (0.72, 0.72, 0.78)


def build_draw():
    lines = [
        "# 卡巴拉生命之树：贴地约 4×8.5 格，所有圆直径 1.00 格。",
        "# 粒子高度固定在锚点上方 0.06—0.08 格；锚点俯仰恒为零。",
    ]
    for start, end in PATHS:
        x1, z1, _, _ = NODES[start]
        x2, z2, _, _ = NODES[end]
        dx, dz = x2 - x1, z2 - z1
        length = math.hypot(dx, dz)
        ux, uz = dx / length, dz / length
        # Keep paths outside the one-block circles so ring silhouettes stay crisp.
        sx, sz = x1 + ux * 0.54, z1 + uz * 0.54
        ex, ez = x2 - ux * 0.54, z2 - uz * 0.54
        visible = math.hypot(ex - sx, ez - sz)
        count = max(2, int(math.ceil(visible / 0.22)) + 1)
        lines.append("# PATH %s -> %s samples=%d" % (start, end, count))
        color = path_color(start, end)
        for index in range(count):
            t = index / float(count - 1)
            lines.append(dust(color, sx + (ex - sx) * t, sz + (ez - sz) * t, 0.48, 0.058))

    for key, (cx, cz, color, label) in NODES.items():
        dashed = key == "daath"
        points = 12 if dashed else 24
        lines.append("# NODE %s / %s center=(%s,%s) diameter=1.00 points=%d%s" % (key, label, fmt(cx), fmt(cz), points, " dashed" if dashed else ""))
        for index in range(points):
            if dashed and index % 2:
                continue
            angle = 2.0 * math.pi * index / points
            lines.append(dust(color, cx + math.cos(angle) * 0.50, cz + math.sin(angle) * 0.50, 0.92, 0.075))
        if not dashed:
            rgb = ",".join("%.2f" % channel for channel in color)
            lines.append("particle dust{color:[%s],scale:0.60} ^%s ^0.068 ^%s 0.30 0 0.30 0 7" % (rgb, fmt(cx), fmt(cz)))
            lines.append("particle enchant ^%s ^0.082 ^%s 0.10 0.01 0.10 0.01 2" % (fmt(cx), fmt(cz)))
    write("ritual/life_tree/draw.mcfunction", "\n".join(lines))


def patch_runtime():
    rel = "command/soreboard.mcfunction"
    src = "\n".join(line for line in read(rel).splitlines() if "rpg_lt_tick" not in line).rstrip()
    src += "\nscoreboard objectives add rpg_lt_tick dummy"
    write(rel, src)

    rel = "exorcism.mcfunction"
    lines = [line for line in read(rel).splitlines() if "生命之树粒子阵" not in line and "function rpg:ritual/life_tree/tick" not in line]
    lines += [
        "",
        "# 生命之树粒子阵：有锚点时才推进十刻刷新。",
        "execute if entity @e[type=minecraft:marker,tag=rpg.ritual.life_tree,limit=1] run function rpg:ritual/life_tree/tick",
    ]
    write(rel, "\n".join(lines))


def build_controls():
    write("ritual/life_tree/tick.mcfunction", """scoreboard players add #life_tree rpg_lt_tick 1
execute if score #life_tree rpg_lt_tick matches 10.. run scoreboard players set #life_tree rpg_lt_tick 0
execute if score #life_tree rpg_lt_tick matches 0 run execute as @e[type=minecraft:marker,tag=rpg.ritual.life_tree] at @s run function rpg:ritual/life_tree/draw
""")
    write("ritual/life_tree/place.mcfunction", """# 由玩家执行：阵心落在脚下，美丽/Tiphereth 位于中心，朝玩家视线前方展开。
execute unless entity @s[type=minecraft:player] run return 0
execute if entity @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..2,limit=1] run tellraw @s %(EXISTS)s
execute if entity @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..2,limit=1] run return 0
summon minecraft:marker ~ ~0.02 ~ {Tags:["rpg.ritual.life_tree","rpg.ritual.life_tree.new"],CustomName:'{"text":"生命之树 · 粒子阵锚","color":"#D596F2","italic":false}'}
execute store result entity @e[type=minecraft:marker,tag=rpg.ritual.life_tree.new,distance=..2,limit=1,sort=nearest] Rotation[0] float 1 run data get entity @s Rotation[0] 1
data modify entity @e[type=minecraft:marker,tag=rpg.ritual.life_tree.new,distance=..2,limit=1,sort=nearest] Rotation[1] set value 0.0f
tag @e[type=minecraft:marker,tag=rpg.ritual.life_tree.new,distance=..2,limit=1,sort=nearest] remove rpg.ritual.life_tree.new
scoreboard players set #life_tree rpg_lt_tick 0
execute as @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..2,limit=1,sort=nearest] at @s run function rpg:ritual/life_tree/draw
playsound minecraft:block.beacon.activate ambient @s ~ ~ ~ 0.55 1.35
tellraw @s %(PLACED)s
""" % {
        "EXISTS": ui.prefix_message("[秘仪] ", ui.RITUAL,
                                    "此处已有生命之树阵心。"),
        "PLACED": ui.prefix_message("[秘仪] ", ui.RITUAL,
                                    "生命之树已沿你的朝向平铺于地面。",
                                    ui.HOLY_LIGHT),
    })
    write("ritual/life_tree/clear.mcfunction", """# 清除执行位置十二格内的阵心；残留粒子会在一秒内自然消散。
kill @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..12]
tellraw @s %(CLEARED)s
""" % {"CLEARED": ui.prefix_message("[秘仪] ", ui.RITUAL,
                                           "附近的生命之树归于沉寂。",
                                           ui.GRAY)})
    write("ritual/life_tree/clear_all.mcfunction", """kill @e[type=minecraft:marker,tag=rpg.ritual.life_tree]
""")


def main():
    patch_runtime()
    build_draw()
    build_controls()
    print("life tree: 10 Sephiroth + dashed Daath / 22 paths / 1-block rings / 10-tick refresh")


if __name__ == "__main__":
    main()
