# -*- coding: utf-8 -*-
"""原作 Abomination Vine（Jungle Abomination 召出的藤蔓）：模型、动作和运行时接口。

从本体提取（Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/），
经 dungeons_conversion/generic.py 转换；对照图 lucifer_vine_ref/render_check.png。
战斗逻辑在 add_lucifer_fight.py，这里只提供三个入口：

    rpg:lucifer_vine/spawn    任意执行者，位置=根部：召出一根，播破土，之后待机。
                              新藤蔓的根带 rpg.luv.new，调用方记完编号后自己摘掉。
    rpg:lucifer_vine/retract  as 根：播消亡动作，播完清掉。
    rpg:lucifer_vine/clear    as 根：立刻清掉，不播动作。

根是不可攻击的标记盔甲架，部件骑在它上面。寿命分数 rpg_luv_l（默认 200 刻）
走到 0 时自动 retract；消亡播完再走到 0 时清掉，所以调用方可以只设寿命。
"""

import json
import os
import sys

from display_mob import Mob, build, snbt_components, wf, write_rig_runtime

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"
HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "lucifer_vine_ref")
F = "rpg:lucifer_vine"
ROOT = "type=minecraft:armor_stand,tag=rpg.luv.root"
LIFE = "rpg_luv_l"
DEFAULT_LIFE = 200
MODEL_SCALE = 7.1949189027950968          # 与二阶段同一系数：0.0086339 格/厘米
DEATH_TICKS = 35                           # AbominationVine_Death 1.742 秒

PARTS = json.load(open(os.path.join(REF, "parts.json"), encoding="utf-8"))
MOB = Mob(
    key="lucifer_vine", label="藤蔓", generator="add_lucifer_vine_model.py",
    bbmodel=os.path.join(REF, "lucifer_vine.bbmodel"),
    parts=[(p["name"], p["bones"]) for p in PARTS],
    glow=set(json.load(open(os.path.join(REF, "glow_bones.json"), encoding="utf-8"))),
    carrier="minecraft:armor_stand", seat=0.0, model_scale=MODEL_SCALE, face_rotation=True,
    tag="rpg.luv", score="rpg_luv",
    clips=[("idle", 1, True), ("walk", 1, True), ("burst", 1, False), ("death", 1, False)],
)


def write_datapack(baked):
    first = baked["burst"]["frames"][0][1]
    dress = ["# 藤蔓换装（as 根，at 根）：挂上部件，从破土的第一帧开始。",
             "tag @s add rpg.luv", "tag @s add rpg.luv.dressing"]
    for part, _ in MOB.parts:
        dress.append(
            'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.luv.part","rpg.luv.p.%s","rpg.luv.new_part"],'
            'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_vine/%s"}},'
            'item_display:"none",teleport_duration:1,interpolation_duration:1,view_range:2f,transformation:%s}'
            % (part, part, snbt_components(MOB, first[part])))
    dress += [
        "execute as @e[type=minecraft:item_display,tag=rpg.luv.new_part,distance=..1] run "
        "ride @s mount @e[%s,tag=rpg.luv.dressing,limit=1]" % ROOT,
        "tag @e[type=minecraft:item_display,tag=rpg.luv.new_part,distance=..1] remove rpg.luv.new_part",
        "tag @s remove rpg.luv.dressing",
        "function %s/anim/init" % F,
        "function %s/anim/enter/burst" % F,
    ]
    wf(os.path.join(MOB.func, "dress.mcfunction"), dress)
    wf(os.path.join(MOB.func, "spawn.mcfunction"), [
        "# 召出一根藤蔓（位置=根部）。朝向随机，免得一排藤蔓长得一模一样。",
        "summon minecraft:armor_stand ~ ~ ~ {Marker:1b,Invisible:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,"
        "Tags:[\"rpg.luv.root\",\"rpg.luv.new\",\"rpg.luv.spawning\"]}",
        "execute store result entity @e[%s,tag=rpg.luv.spawning,limit=1,sort=nearest] Rotation[0] float 1 "
        "run random value -180..179" % ROOT,
        "scoreboard players set @e[%s,tag=rpg.luv.spawning,limit=1,sort=nearest] %s %d" % (ROOT, LIFE, DEFAULT_LIFE),
        "execute as @e[%s,tag=rpg.luv.spawning,limit=1,sort=nearest] at @s run function %s/dress" % (ROOT, F),
        "tag @e[%s,tag=rpg.luv.spawning] remove rpg.luv.spawning" % ROOT,
    ])
    wf(os.path.join(MOB.func, "retract.mcfunction"), [
        "# as 根：缩回地下，播完消亡动作再清掉。",
        "execute if entity @s[tag=rpg.luv.dying] run return 0",
        "tag @s add rpg.luv.dying",
        "scoreboard players set @s %s %d" % (LIFE, DEATH_TICKS + 1),
        "function %s/anim/enter/death" % F,
    ])
    wf(os.path.join(MOB.func, "clear.mcfunction"), [
        "# as 根：立刻清掉，不播动作。",
        "execute on passengers run kill @s",
        "kill @s",
    ])
    wf(os.path.join(MOB.func, "life.mcfunction"), [
        "scoreboard players remove @s %s 1" % LIFE,
        "execute if score @s %s matches ..0 if entity @s[tag=rpg.luv.dying] run return run function %s/clear" % (LIFE, F),
        "execute if score @s %s matches ..0 run function %s/retract" % (LIFE, F),
    ])
    write_rig_runtime(MOB, [
        "# 藤蔓每刻：寿命倒数，部件跟随根。",
        "execute if entity @e[%s,limit=1] as @e[%s,tag=rpg.luv] at @s run function %s/follow" % (ROOT, ROOT, F),
        "execute if entity @e[%s,limit=1] as @e[%s,tag=rpg.luv] run function %s/life" % (ROOT, ROOT, F),
    ])
    load = os.path.join(MOB.func, "load.mcfunction")
    with open(load, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    wf(load, lines + ["scoreboard objectives add %s dummy" % LIFE])


def main():
    baked, _first = build(MOB, RP, DP)
    write_datapack(baked)


if __name__ == "__main__":
    main()
