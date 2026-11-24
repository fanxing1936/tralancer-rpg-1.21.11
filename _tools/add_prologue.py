# -*- coding: utf-8 -*-
"""《破碎大陆》序章（Claude Docs：《破碎大陆》序章 · 游戏化方案书 / 脚本书）。

    python add_prologue.py ../resourcepack ../rpg

1～4 人的独立副本，入口只有指令（管理员）：
    /function rpg:prologue/start     把执行位置 16 格内最多 4 名玩家送进序章维度 rpg:armageddon
    /function rpg:prologue/clear     中止并把所有人送回原处

流程（#state rpg_pr）：1 准备场地 → 2 大厅选角 → 3 场 1 开场旁白 → 4 三波天使（新手教程）→ 5 场 3 中央对话
→ 6 场 4 米迦勒降临 → 7 四人战米迦勒（米迦勒 Boss 的序章模式）→ 8 场 6 敌基督的本源 → 9 场 7 分离 → 回原处、发奖励。

与玩家存档隔离（方案书 · 技术实现）：进序章的人挂 rpg.pr；背包、经验、游戏模式和回程位置存起来（背包放进序章维度里
固定位置的木桶），出来时原样还回；挂 rpg.pr 的人不结算魔化；角色技能直接调七十二柱的招式函数，不碰玩家的契约分数；
副手放一件隐形的死亡保护，致命一击被它吃掉后改为旁观 5 秒、在场地西缘重新加入；中途掉线的人下次登录时由 rejoin 还原。

占位（素材到了再换）：天使士兵用圣卫；路西法演员用雅克的外观；角色装备用染色皮甲（Codex 的装备贴图到了换成 equippable）；
过场动作用现成动作（prologue_cut.CLIP）；配音按 vo/picks.json 自动接入，没有就只出字幕。
"""
import io
import json
import os
import re
import sys

import prologue_world as world
import prologue_text as text
import prologue_cut as cuts
from display_mob import hook_tag

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "prologue")
P = "rpg:prologue"
O = "rpg_pr"
DIM = "rpg:armageddon"
PR = "@a[tag=rpg.pr]"
GUARD = 'minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty",minecraft:custom_data={rpg_pr_guard:1b}]'

ROLES = {1: ("lucifer", "路西法", "[恶魔]路西法", 1, 0xF2E6B8),
         2: ("beelzebub", "别西卜", "[恶魔]别西卜", 4, 0x5A6B1E),
         3: ("belial", "贝利尔", "[恶魔]贝利尔", 6, 0x5B2C6F),
         4: ("mammon", "玛门", "[恶魔]玛门", 7, 0xB7950B)}
ALTAR_Z = {1: -6, 2: -2, 3: 2, 4: 6}
ALTAR_X = -9
LOBBY = (-15, 81, 0)
WEST = (-36, 0)          # 战斗时的出生点（x, z），y 取地表
VAULT = (30, 30, 30)     # 背包木桶：每人两只（30+2k, 30, 30) 与 (30+2k, 30, 32)
WHEEL_HP = 10
COUNT = 0


def fn(name, lines):
    global COUNT
    p = os.path.join(OUT, name + ".mcfunction")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT += 1


def wj(rel, obj):
    p = os.path.join(DP, "data", rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def js(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def give_line(name):
    """在发放函数里找到这件武器的 give 行，改成发给自己、并打上序章武器的标记。"""
    for f in os.listdir(os.path.join(FUNC, "command", "give")):
        for line in io.open(os.path.join(FUNC, "command", "give", f), encoding="utf-8"):
            m = re.match(r"give @a (\S+?)\[(custom_name=.*)\] ?(\d*)\s*$", line.strip())
            if not m:
                continue
            nm = "".join(re.findall(r'"text":"([^"]*)"', m.group(2).split("lore=")[0]))
            if nm == name:
                body = m.group(2)
                body = body.replace("custom_data={", "custom_data={rpg_pr_w:1b,", 1) if "custom_data={" in body \
                    else body + ",custom_data={rpg_pr_w:1b}"
                return "give @s %s[%s] 1" % (m.group(1), body)
    raise SystemExit("prologue: weapon not found: " + name)


def every_player(cmd):
    return "execute as %s at @s run %s" % (PR, cmd)


# ---------------------------------------------------------------------------- 场地
def build_arena():
    c = ["# 准备场地（in 序章维度）：中心广场压平到 y=80、石台与深坑、四座祭坛、背包木桶、场地装饰",
         "# 群系的「血迹」是红石线：先直接换成空气（fill 换掉不掉落），免得压平时失去支撑弹成满地红石粉",
         "fill -26 74 -26 26 85 26 minecraft:air replace minecraft:redstone_wire",
         "fill -26 86 -26 26 97 26 minecraft:air replace minecraft:redstone_wire"]
    R = 15
    for dx in range(-R, R + 1):
        dz = int((R * R - dx * dx) ** 0.5)
        c.append("fill %d 81 %d %d 118 %d minecraft:air" % (dx, -dz, dx, dz))
        c.append("fill %d 70 %d %d 79 %d minecraft:mud replace #minecraft:air" % (dx, -dz, dx, dz))
        c.append("fill %d 80 %d %d 80 %d minecraft:mud" % (dx, -dz, dx, dz))
    for dx in range(-R, R + 1, 3):
        for dz in range(-R, R + 1, 3):
            if dx * dx + dz * dz <= R * R and (dx * 7 + dz * 3) % 4 == 0:
                c.append("setblock %d 80 %d minecraft:muddy_mangrove_roots" % (dx, dz))
    # 石台下的大洞穴（用户 2026-11-22「无底坑应该是类似于大洞穴一样的东西」）：
    # 椭球形空腔，中心 (0, 52, 0)，水平半径 22、上下 34～72；外面裹一层黑石 / 玄武岩 / 深板岩的壳；
    # 洞口是石台下一口半径 4 的竖井（73～79）。洞底灵魂土，散着岩浆块、骨块和几洼岩浆，顶上挂着滴水石锥。
    import math
    import random
    rnd = random.Random(1515)
    shell = ("minecraft:blackstone", "minecraft:basalt", "minecraft:deepslate", "minecraft:blackstone", "minecraft:smooth_basalt")
    CY, RX, RY = 52, 22, 19
    for y in range(31, 76):
        t = (y - CY) / float(RY + 2.5)
        if abs(t) < 1:
            ro = int((RX + 2.5) * math.sqrt(1 - t * t))
            for dx in range(-ro, ro + 1):
                dz = int(math.sqrt(max(ro * ro - dx * dx, 0)))
                c.append("fill %d %d %d %d %d %d %s" % (dx, y, -dz, dx, y, dz, rnd.choice(shell)))
    top = {}
    for y in range(35, 73):
        t = (y - CY) / float(RY)
        if abs(t) < 1:
            ri = int(RX * math.sqrt(1 - t * t)) if y > 40 else RX - (41 - y)       # 底部放平：越往下越收一点
            for dx in range(-ri, ri + 1):
                dz = int(math.sqrt(max(ri * ri - dx * dx, 0)))
                c.append("fill %d %d %d %d %d %d minecraft:air" % (dx, y, -dz, dx, y, dz))
                for zz in range(-dz, dz + 1):
                    top[(dx, zz)] = y
    # 洞底
    for dx in range(-RX, RX + 1):
        dz = int(math.sqrt(max(RX * RX - dx * dx, 0)))
        c.append("fill %d 34 %d %d 34 %d minecraft:soul_soil replace #rpg:prologue_cave_shell" % (dx, -dz, dx, dz))
    for _ in range(26):
        x, z = rnd.randint(-17, 17), rnd.randint(-17, 17)
        if x * x + z * z > 17 * 17 or x * x + z * z < 9:
            continue
        c.append("setblock %d 34 %d %s" % (x, z, rnd.choice(("minecraft:magma_block", "minecraft:magma_block", "minecraft:bone_block",
                                                            "minecraft:soul_sand", "minecraft:crying_obsidian"))))
    for x, z in ((-11, 7), (9, -10), (13, 6), (-6, -13)):
        c.append("fill %d 34 %d %d 34 %d minecraft:lava" % (x - 1, z - 1, x + 1, z + 1))
    for _ in range(40):
        x, z = rnd.randint(-16, 16), rnd.randint(-16, 16)
        if x * x + z * z > 16 * 16 or x * x + z * z < 30:
            continue
        if (x, z) not in top:
            continue
        roof = top[(x, z)]
        n = rnd.randint(1, 4)
        for k in range(n):
            tip = "tip" if k == n - 1 else ("frustum" if k else "base")
            c.append("setblock %d %d %d minecraft:pointed_dripstone[vertical_direction=down,thickness=%s]" % (x, roof - k, z, tip))
    # 洞口竖井：石台下半径 4、73～79；井壁黑石
    for dx in range(-5, 6):
        dz5 = int((25 - dx * dx) ** 0.5 + 0.5)
        c.append("fill %d 70 %d %d 79 %d minecraft:blackstone" % (dx, -dz5, dx, dz5))
    for dx in range(-4, 5):
        dz = int((16 - dx * dx) ** 0.5 + 0.5)
        c.append("fill %d 70 %d %d 79 %d minecraft:air" % (dx, -dz, dx, dz))
        c.append("fill %d 80 %d %d 80 %d minecraft:polished_blackstone_bricks" % (dx, -dz, dx, dz))
    for a in range(0, 360, 15):
        import math
        x = int(round(4.2 * math.cos(math.radians(a))))
        z = int(round(4.2 * math.sin(math.radians(a))))
        c.append("setblock %d 80 %d minecraft:chiseled_polished_blackstone" % (x, z))
    # 四座祭坛
    c.append("kill @e[tag=rpg.pr.deco]")
    for k, (slug, zh, _, _, col) in ROLES.items():
        z = ALTAR_Z[k]
        u = "U%02d" % (k + 1)
        c.append("setblock %d 80 %d minecraft:lodestone" % (ALTAR_X, z))
        c.append("summon minecraft:marker %d 81 %d {Tags:[\"rpg.pr.altar\",\"rpg.pr.deco\",\"rpg.pr.ent\",\"rpg.pr.alt%d\"]}"
                 % (ALTAR_X, z, k))
        name = [{"translate": "rpg.prologue.%s.zh" % u, "fallback": LINES[u]["zh"], "color": "#%06X" % col, "bold": True},
                {"text": "\n"}, {"translate": "rpg.prologue.%s.en" % u, "fallback": LINES[u]["en"], "color": "#BFB8A8"}]
        c.append("summon minecraft:text_display %d.5 82.9 %d.5 {Tags:[\"rpg.pr.deco\",\"rpg.pr.ent\"],billboard:\"center\","
                 "background:1073741824,text:%s}" % (ALTAR_X, z, js(name)))
    # 背包木桶：已经是木桶就不动（上一次没还完的东西不会被冲掉），否则放一只（那里是地下，原本是石头）
    for k in range(1, 5):
        for dz in (0, 2):
            x, y, z = VAULT[0] + 2 * k, VAULT[1], VAULT[2] + dz
            c.append("execute unless block %d %d %d minecraft:barrel run setblock %d %d %d minecraft:barrel" % (x, y, z, x, y, z))
    # 中心广场补几处血迹与骸骨（和群系一样的装饰）
    for x, z in ((-11, 6), (9, -8), (12, 5), (-6, -11), (3, 12), (-13, -3)):
        c.append("place feature rpg:armageddon/blood_splatter %d 81 %d" % (x, z))
    for x, z in ((-12, 9), (11, -10), (6, 13)):
        c.append("place feature rpg:armageddon/skulls %d 81 %d" % (x, z))
    # 平铺在地上的大片血迹（Codex 画的 4 张，rpg:prologue_fx/blood_0..3）
    for i, (x, z, yaw, sc) in enumerate(((-9, 3, 20, 2.6), (7, -4, 110, 2.2), (10, 9, 200, 3.0), (-4, -9, 300, 2.4),
                                         (2, 10, 60, 2.0), (-12, -6, 150, 2.8), (13, -1, 250, 2.2), (-2, 6, 340, 1.8))):
        c.append("execute positioned %d 120 %d positioned over motion_blocking rotated %d 0 run summon minecraft:item_display ~ ~0.02 ~ "
                 "{Tags:[\"rpg.pr.deco\",\"rpg.pr.ent\"],Rotation:[%df,0f],item:{id:\"minecraft:paper\",count:1,components:"
                 "{\"minecraft:item_model\":\"rpg:prologue_fx/blood_%d\"}},item_display:\"fixed\",transformation:"
                 "{left_rotation:[-0.7071f,0f,0f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[%gf,%gf,%gf]}}"
                 % (x, z, yaw, yaw, i % 4, sc, sc, sc))
    fn("arena/build", c)
    fn("arena/sweep", ["# 每秒一次：清掉场地上弹出来的红石粉（群系血迹是红石线，压平地面、踩碎石台时会掉）",
                       "scoreboard players set #sweep %s 0" % O,
                       "# 顺带每秒补一次饱和（死亡重生等会清掉效果）",
                       "effect give @a[tag=rpg.pr] minecraft:saturation infinite 0 true",
                       "execute in %s positioned 0 60 0 as @e[type=minecraft:item,distance=..72] "
                       "if items entity @s contents minecraft:redstone run kill @s" % DIM])
    wj("rpg/tags/block/prologue_cave_shell.json", {"values": ["minecraft:blackstone", "minecraft:basalt", "minecraft:deepslate",
                                                             "minecraft:smooth_basalt", "minecraft:air"]})
    wj("rpg/tags/block/prologue_platform.json", {"values": ["minecraft:polished_blackstone_bricks",
                                                           "minecraft:chiseled_polished_blackstone"]})


# ---------------------------------------------------------------------------- 存档隔离
SLOTS = ["container.%d" % i for i in range(36)] + ["armor.head", "armor.chest", "armor.legs", "armor.feet", "weapon.offhand"]


def isolation():
    for k in range(1, 5):
        a = (VAULT[0] + 2 * k, VAULT[1], VAULT[2])
        b = (VAULT[0] + 2 * k, VAULT[1], VAULT[2] + 2)
        put, get = [], []
        for i, slot in enumerate(SLOTS):
            pos, j = (a, i) if i < 27 else (b, i - 27)
            put.append("execute in %s run item replace block %d %d %d container.%d from entity @s %s" % (DIM, pos[0], pos[1], pos[2], j, slot))
            get.append("execute in %s run item replace entity @s %s from block %d %d %d container.%d" % (DIM, slot, pos[0], pos[1], pos[2], j))
            get.append("execute in %s run item replace block %d %d %d container.%d with minecraft:air" % (DIM, pos[0], pos[1], pos[2], j))
        fn("iso/stash_%d" % k, ["# 背包存进第 %d 号木桶（as 玩家）" % k] + put)
        fn("iso/unstash_%d" % k, ["# 从第 %d 号木桶还回背包（as 玩家）" % k] + get)
    fn("iso/save", [
        "# 记下回程位置、游戏模式、经验，存背包（as 玩家，宏参数 id）",
        "$data modify storage rpg:pr r.p$(id).dim set from entity @s Dimension",
        "$execute store result storage rpg:pr r.p$(id).x double 0.01 run data get entity @s Pos[0] 100",
        "$execute store result storage rpg:pr r.p$(id).y double 0.01 run data get entity @s Pos[1] 100",
        "$execute store result storage rpg:pr r.p$(id).z double 0.01 run data get entity @s Pos[2] 100",
        "$execute store result storage rpg:pr r.p$(id).yaw float 0.01 run data get entity @s Rotation[0] 100",
        "$execute store result storage rpg:pr r.p$(id).xl int 1 run experience query @s levels",
        "$execute store result storage rpg:pr r.p$(id).xp int 1 run experience query @s points",
        "$data modify storage rpg:pr r.p$(id).gm set value \"survival\"",
        "$execute if entity @s[gamemode=creative] run data modify storage rpg:pr r.p$(id).gm set value \"creative\"",
        "$execute if entity @s[gamemode=adventure] run data modify storage rpg:pr r.p$(id).gm set value \"adventure\"",
        "$execute if entity @s[gamemode=spectator] run data modify storage rpg:pr r.p$(id).gm set value \"spectator\"",
    ])
    fn("iso/restore", [
        "# 还原一名玩家（as 玩家）",
        "execute store result storage rpg:pr tmp.id int 1 run scoreboard players get @s rpg_pr_id",
        "execute unless data storage rpg:pr r.p1 unless data storage rpg:pr r.p2 unless data storage rpg:pr r.p3 unless data storage rpg:pr r.p4 run return run tellraw @s {\"text\":\"[序章] 找不到你的回程记录\",\"color\":\"red\"}",
        "clear @s",
    ] + ["execute if score @s rpg_pr_id matches %d run function rpg:prologue/iso/unstash_%d" % (k, k) for k in range(1, 5)] + [
        "function rpg:prologue/iso/restore_m with storage rpg:pr tmp",
        "attribute @s minecraft:max_health modifier remove rpg:prologue/hp",
        "function rpg:prologue/role/avatar_off",
        "stopsound @s record",
        "tag @s remove rpg.pr",
        "tag @s remove rpg.pr.mh",
        "scoreboard players reset @s rpg_pr_role",
        "scoreboard players reset @s rpg_pr_id",
        "title @s reset",
    ])
    fn("iso/restore_m", [
        "$execute unless data storage rpg:pr r.p$(id) run return run tellraw @s {\"text\":\"[序章] 找不到你的回程记录\",\"color\":\"red\"}",
        "effect clear @s",
        "$function rpg:prologue/iso/back with storage rpg:pr r.p$(id)",
        "$data remove storage rpg:pr r.p$(id)",
    ])
    fn("iso/back", [
        "$gamemode $(gm) @s",
        "$experience set @s $(xl) levels",
        "$experience set @s $(xp) points",
        "$execute in $(dim) run tp @s $(x) $(y) $(z) $(yaw) 0",
        "effect give @s minecraft:instant_health 1 4 true",
    ])
    fn("rejoin", [
        "# 登录（as 刚登录的玩家）：序章已经结束而他还挂着 rpg.pr，就把他还原",
        "scoreboard players reset @s rpg_pr_lv",
        "execute if entity @s[tag=rpg.pr] unless score #state %s matches 1.. run function rpg:prologue/iso/restore" % O,
        "execute if entity @s[tag=rpg.pr] if score #state %s matches 3 run gamemode spectator @s" % O,
        "execute if entity @s[tag=rpg.pr] if score #state %s matches 5..6 run gamemode spectator @s" % O,
        "execute if entity @s[tag=rpg.pr] if score #state %s matches 8..9 run gamemode spectator @s" % O,
    ])


# ---------------------------------------------------------------------------- 加载与入口
def entry():
    fn("load", [
        "scoreboard objectives add %s dummy" % O,
        "scoreboard objectives add rpg_pr_role dummy",
        "scoreboard objectives add rpg_pr_id dummy",
        "scoreboard objectives add rpg_pr_cd1 dummy",
        "scoreboard objectives add rpg_pr_cd2 dummy",
        "scoreboard objectives add rpg_pr_av dummy",
        "scoreboard objectives add rpg_pr_down dummy",
        "scoreboard objectives add rpg_pr_done dummy",
        "scoreboard objectives add rpg_pr_lv minecraft.custom:minecraft.leave_game",
        "scoreboard players set #ten %s 10" % O,
        "scoreboard players set #hund %s 100" % O,
        "scoreboard players set #twenty %s 20" % O,
        "scoreboard objectives add rpg_pr_s1 dummy",
        "scoreboard objectives add rpg_pr_s2 dummy",
        "execute unless score #state %s matches 0.. run scoreboard players set #state %s 0" % (O, O),
        "bossbar add %s \"\"" % text.ZH_BAR,
        "bossbar add %s \"\"" % text.EN_BAR,
        "bossbar set %s color pink" % text.ZH_BAR,
        "bossbar set %s color pink" % text.EN_BAR,
        "bossbar set %s visible false" % text.ZH_BAR,
        "bossbar set %s visible false" % text.EN_BAR,
    ])
    fn("start", [
        "# 开始序章（管理员；在执行位置 16 格内最多 4 名玩家进入）",
        "execute if score #state %s matches 1.. run return run tellraw @s {\"text\":\"[序章] 序章正在进行；先用 /function rpg:prologue/clear 中止。\",\"color\":\"#E8D9B0\"}" % O,
        "tag @a remove rpg.pr.join",
        "tag @a[distance=..16,gamemode=!spectator,limit=4,sort=nearest] add rpg.pr.join",
        "execute unless entity @a[tag=rpg.pr.join] run return run tellraw @s {\"text\":\"[序章] 附近 16 格内没有可以进入序章的玩家。\",\"color\":\"#E8D9B0\"}",
        "execute if score #fight rpg_mk matches 1 run return run tellraw @s {\"text\":\"[序章] 有一场米迦勒战正在进行；先清场。\",\"color\":\"#E8D9B0\"}",
        "# 下雨、雷暴会把所有维度的天空一起压暗（实测）：序章期间放晴",
        "weather clear 1800s",
        "execute in %s run forceload add -64 -64 63 63" % DIM,
        "scoreboard players set #state %s 1" % O,
        "scoreboard players set #t %s 0" % O,
        "scoreboard players set #next %s 0" % O,
        "scoreboard players set #built %s 0" % O,
        "scoreboard players set #bt %s 0" % O,
        "tellraw @a[tag=rpg.pr.join] {\"text\":\"[序章] 正在准备战场…… Preparing the battlefield...\",\"color\":\"#E8D9B0\"}",
    ])
    fn("clear", [
        "# 中止序章：所有在线的人还原，清场",
        "execute as %s run function rpg:prologue/iso/restore" % PR,
        "function rpg:prologue/cleanup",
        "tellraw @s {\"text\":\"[序章] 已中止。\",\"color\":\"#E8D9B0\"}",
    ])
    fn("cleanup", [
        "scoreboard players set #state %s 0" % O,
        "scoreboard players set #cut %s 0" % O,
        "scoreboard players set #rift %s 0" % O,
        "scoreboard players set #aura %s 0" % O,
        "scoreboard players set #smoke %s 0" % O,
        "scoreboard players set #bgm %s 0" % O,
        "scoreboard players set #pro rpg_mk 0",
        "execute if score #fight rpg_mk matches 1 run function rpg:michael_boss/clear",
        "execute as @e[type=minecraft:vindicator,tag=rpg.pr.actor] run function rpg:prologue/cut/kill_actor",
        "execute as @e[tag=rpg.pr.foe] run function rpg:prologue/cut/kill_actor",
        "execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] run function rpg:prologue/cut/kill_actor",
        "kill @e[tag=rpg.pr.ent]",
        "function rpg:prologue/sub/clear",
        "bossbar set %s visible false" % text.ZH_BAR,
        "bossbar set %s visible false" % text.EN_BAR,
        "bossbar set %s players" % text.ZH_BAR,
        "bossbar set %s players" % text.EN_BAR,
        "execute in %s run forceload remove -64 -64 63 63" % DIM,
    ])


# ---------------------------------------------------------------------------- 每刻
def ticker():
    fn("tick", [
        "execute as @a[scores={rpg_pr_lv=1..}] run function rpg:prologue/rejoin",
        "execute unless score #state %s matches 1.. run return 0" % O,
        "scoreboard players add #t %s 1" % O,
        "execute if score #state %s matches 1 run function rpg:prologue/prep" % O,
        "execute if score #state %s matches 2 run function rpg:prologue/lobby/tick" % O,
        "execute if score #cut %s matches 1.. run function rpg:prologue/cut/tick" % O,
        "execute if score #state %s matches 4 run function rpg:prologue/wave/tick" % O,
        "execute if score #state %s matches 7 run function rpg:prologue/michael/tick" % O,
        "execute if score #state %s matches 10 run function rpg:prologue/finish" % O,
        "function rpg:prologue/sub/tick",
        "function rpg:prologue/music/tick",
        "# 场地上弹出来的红石粉（群系血迹是红石线，压平/踩碎石台时会掉）每秒清一次",
        "scoreboard players add #sweep %s 1" % O,
        "execute if score #sweep %s matches 20.. run function rpg:prologue/arena/sweep" % O,
        "execute as %s at @s run function rpg:prologue/player/tick" % PR,
        "execute if score #state %s matches 2.. unless entity %s run function rpg:prologue/cleanup" % (O, PR),
    ])
    loaded = " ".join("if loaded %d %d %d" % p for p in
                      ((VAULT[0] + 2, VAULT[1], VAULT[2]), (VAULT[0] + 8, VAULT[1], VAULT[2] + 2), (-16, 80, -16), (16, 80, 16),
                       (40, 80, 0), (WEST[0], 80, WEST[1]), (0, 40, 0)))
    fn("prep", [
        "# 等强制加载的区块真正载入（实测 2 秒不一定够，木桶会放不下去）：载入了再搭场地，再过 1 秒把人接进来",
        "execute if score #built %s matches 0 if score #t %s matches 20.. in %s %s positioned 0 80 0 run function rpg:prologue/arena/build_go" % (O, O, DIM, loaded),
        "execute if score #built %s matches 0 if score #t %s matches 600.. run function rpg:prologue/prep_fail" % (O, O),
        "execute if score #built %s matches 1 run scoreboard players add #bt %s 1" % (O, O),
        "execute if score #bt %s matches 20 as @a[tag=rpg.pr.join] run function rpg:prologue/join" % O,
        "execute if score #bt %s matches 21 if entity %s run function rpg:prologue/lobby/begin" % (O, PR),
    ])
    fn("arena/build_go", ["scoreboard players set #built %s 1" % O, "scoreboard players set #bt %s 0" % O,
                          "function rpg:prologue/arena/build"])
    fn("prep_fail", ["tellraw @a[tag=rpg.pr.join] {\"text\":\"[序章] 战场区块迟迟没有载入，已取消。Could not load the battlefield.\",\"color\":\"red\"}",
                     "tag @a remove rpg.pr.join", "function rpg:prologue/cleanup"])
    fn("join_fail", ["tag @s remove rpg.pr.join", "scoreboard players reset @s rpg_pr_id",
                     "tellraw @s {\"text\":\"[序章] 存放背包的位置没准备好，你没有被送进序章，背包没动。\",\"color\":\"red\"}"])
    fn("join", [
        "# 接一名玩家进序章（as 玩家）",
        "scoreboard players add #next %s 1" % O,
        "scoreboard players operation @s rpg_pr_id = #next %s" % O,
        "execute store result storage rpg:pr tmp.id int 1 run scoreboard players get @s rpg_pr_id",
        "# 木桶不在就不动背包（否则清空了也存不住）",
        "execute in %s unless block %d %d %d minecraft:barrel run return run function rpg:prologue/join_fail" % (DIM, VAULT[0] + 2, VAULT[1], VAULT[2]),
        "function rpg:prologue/iso/save with storage rpg:pr tmp",
    ] + ["execute if score @s rpg_pr_id matches %d run function rpg:prologue/iso/stash_%d" % (k, k) for k in range(1, 5)] + [
        "clear @s",
        "effect clear @s",
        "# 序章全程饱和（用户 2026-11-22），不掉饥饿；回程时 iso/restore_m 的 effect clear 会收回",
        "effect give @s minecraft:saturation infinite 0 true",
        "experience set @s 0 levels",
        "experience set @s 0 points",
        "tag @s remove rpg.pr.join",
        "tag @s add rpg.pr",
        "scoreboard players set @s rpg_pr_role 0",
        "gamemode adventure @s",
        "execute in %s run tp @s %d %d %d -90 0" % (DIM, LOBBY[0], LOBBY[1], LOBBY[2]),
        "item replace entity @s weapon.offhand with %s" % GUARD,
    ])


# ---------------------------------------------------------------------------- 大厅选角
def lobby():
    fn("lobby/begin", [
        "scoreboard players set #state %s 2" % O,
        "scoreboard players set #t %s 0" % O,
        "scoreboard players set #cd %s 0" % O,
    ] + ["scoreboard players set #taken%d %s 0" % (k, O) for k in ROLES] + [
        "bossbar set %s players %s" % (text.ZH_BAR, PR), "bossbar set %s players %s" % (text.EN_BAR, PR),
        "bossbar set %s visible true" % text.ZH_BAR, "bossbar set %s visible true" % text.EN_BAR,
        "function rpg:prologue/sub/u01",
        "function rpg:prologue/music/intro",
    ])
    t = ["# 大厅（每刻）：站上祭坛就选定；人齐倒数 3 秒；满 60 秒没选的自动分配"]
    for k in ROLES:
        t.append("execute if score #taken%d %s matches 0 as @e[type=minecraft:marker,tag=rpg.pr.alt%d] at @s as @a[tag=rpg.pr,distance=..0.9,scores={rpg_pr_role=0},limit=1] run function rpg:prologue/lobby/pick_%d"
                 % (k, O, k, k))
        t.append("execute if score #taken%d %s matches 1 if score #sub %s matches ..0 as @e[type=minecraft:marker,tag=rpg.pr.alt%d] at @s if entity @a[tag=rpg.pr,distance=..0.9,scores={rpg_pr_role=0}] run function rpg:prologue/sub/u06"
                 % (k, O, O, k))
        fn("lobby/pick_%d" % k, ["scoreboard players set @s rpg_pr_role %d" % k, "scoreboard players set #taken%d %s 1" % (k, O),
                                 "playsound minecraft:block.respawn_anchor.set_spawn master @s ~ ~ ~ 1 1.2",
                                 "particle minecraft:end_rod ~ ~1 ~ 0.3 0.8 0.3 0.05 30"])
    t += [
        "execute store result score #n %s if entity %s" % (O, PR),
        "execute store result score #r %s if entity @a[tag=rpg.pr,scores={rpg_pr_role=1..}]" % O,
        "execute if score #t %s matches 1200.. run function rpg:prologue/lobby/auto" % O,
        "execute if score #cd %s matches 0 if score #r %s = #n %s run function rpg:prologue/lobby/ready" % (O, O, O),
        "execute if score #cd %s matches 1.. run scoreboard players add #cd %s 1" % (O, O),
        "execute if score #cd %s matches 61.. run function rpg:prologue/lobby/go" % O,
    ]
    fn("lobby/tick", t)
    auto = ["# 满 60 秒：没选的人按 路西法 → 别西卜 → 贝利尔 → 玛门 的顺序补上空位"]
    for k in ROLES:
        auto.append("execute if score #taken%d %s matches 0 as @a[tag=rpg.pr,scores={rpg_pr_role=0},limit=1] run function rpg:prologue/lobby/pick_%d" % (k, O, k))
    fn("lobby/auto", auto)
    fn("lobby/ready", [
        "scoreboard players set #cd %s 1" % O,
        "function rpg:prologue/lobby/fix_lucifer",
        "execute if score #n %s matches ..3 run function rpg:prologue/sub/u08" % O,
        "execute if score #n %s matches 4.. run function rpg:prologue/sub/u07" % O,
    ])
    fn("lobby/fix_lucifer", [
        "# 路西法必须有人选：没人选时，编号最小的那位改成路西法（他原来的位子空出来）",
        "execute if score #taken1 %s matches 1 run return 0" % O,
        "execute as @a[tag=rpg.pr,scores={rpg_pr_id=1}] run function rpg:prologue/lobby/to_lucifer",
        "execute if score #taken1 %s matches 0 as @a[tag=rpg.pr,scores={rpg_pr_id=2}] run function rpg:prologue/lobby/to_lucifer" % O,
        "execute if score #taken1 %s matches 0 as @a[tag=rpg.pr,scores={rpg_pr_id=3}] run function rpg:prologue/lobby/to_lucifer" % O,
        "execute if score #taken1 %s matches 0 as @a[tag=rpg.pr,scores={rpg_pr_id=4}] run function rpg:prologue/lobby/to_lucifer" % O,
    ])
    fn("lobby/to_lucifer", [
        "execute if score @s rpg_pr_role matches 2 run scoreboard players set #taken2 %s 0" % O,
        "execute if score @s rpg_pr_role matches 3 run scoreboard players set #taken3 %s 0" % O,
        "execute if score @s rpg_pr_role matches 4 run scoreboard players set #taken4 %s 0" % O,
        "scoreboard players set @s rpg_pr_role 1",
        "scoreboard players set #taken1 %s 1" % O,
    ])
    fn("lobby/go", [
        "execute as %s run function rpg:prologue/role/kit" % PR,
        "kill @e[type=minecraft:marker,tag=rpg.pr.altar]",
        "kill @e[type=minecraft:text_display,tag=rpg.pr.deco]",
        "function rpg:prologue/sub/clear",
        "function rpg:prologue/flow/cut1",
    ])


# ---------------------------------------------------------------------------- 角色
def roles():
    kit = ["# 发角色装备（as 玩家）：清空、武器、护甲（皮甲底，equippable 套 rpg:prologue_<角色> 的盔甲层、腿甲层与翅膀层）、副手死亡保护、生命 +20",
           "clear @s",
           "attribute @s minecraft:max_health modifier remove rpg:prologue/hp",
           "attribute @s minecraft:max_health modifier add rpg:prologue/hp 20 add_value"]
    import rpg_ui_style as ui
    for k, (slug, zh, weapon, pillar, col) in ROLES.items():
        lines = [give_line(weapon)]
        # 物品规范（ART-STYLE §2，用户 2026-11-23「序章的装备也要和先前的物品一样规范化」）：
        # [序章] 前缀加粗、该柱亮色；本名白色；Lore 分隔线 + 题记 + 灰色正文；原版的「已染色」行藏起来
        lit = ui.pillar(pillar)["lit"]
        rule = js(["", {"text": ui.RULE_TEXT, "color": ui.WHITE, "italic": False}])
        lore = "[%s,%s,%s,%s]" % (rule, js(["", {"text": "[一千年前]", "color": lit, "bold": True, "italic": False}]),
                                  js(["", {"text": "哈米吉多顿一役，%s穿过的战甲" % zh, "color": ui.GRAY, "italic": False}]), rule)
        for slot, item, piece in (("armor.head", "leather_helmet", "头盔"), ("armor.chest", "leather_chestplate", "胸甲"),
                                  ("armor.legs", "leather_leggings", "护腿"), ("armor.feet", "leather_boots", "战靴")):
            name = js(["", {"text": "[序章]", "color": lit, "bold": True, "italic": False},
                       {"text": "%s的%s" % (zh, piece), "color": ui.WHITE, "bold": False, "italic": False}])
            lines.append("item replace entity @s %s with minecraft:%s[minecraft:dyed_color=%d,minecraft:unbreakable={},"
                         "minecraft:attribute_modifiers=[{type:\"minecraft:armor\",amount:%d,operation:\"add_value\","
                         "id:\"rpg:prologue/%s\",slot:\"%s\"}],minecraft:equippable={slot:\"%s\",asset_id:\"rpg:prologue_%s\"},"
                         "minecraft:tooltip_display={hidden_components:[\"minecraft:dyed_color\",\"minecraft:unbreakable\"]},"
                         "minecraft:custom_name=%s,minecraft:lore=%s]"
                         % (slot, item, col, 5 if "chest" in item else 3, slot.replace(".", "_"),
                            slot.split(".")[1], slot.split(".")[1], slug, name, lore))
        fn("role/kit_%d" % k, lines)
        kit.append("execute if score @s rpg_pr_role matches %d run function rpg:prologue/role/kit_%d" % (k, k))
    kit += ["item replace entity @s weapon.offhand with %s" % GUARD,
            "effect give @s minecraft:instant_health 1 9 true",
            "effect give @s minecraft:saturation 1 9 true",
            "scoreboard players set @s rpg_pr_cd1 0",
            "scoreboard players set @s rpg_pr_cd2 0"]
    fn("role/kit", kit)
    # 技能：F 释放角色技能（七十二柱魂誓招式），潜行 + F 放大招（化身招式）。F 键的判法同符石：
    # 上一刻主手是序章武器、这一刻它到了副手 -> 换回来并释放
    f = ["# F（as/at 玩家）：武器换回主手、死亡保护放回副手",
         "item replace entity @s weapon.mainhand from entity @s weapon.offhand",
         "item replace entity @s weapon.offhand with %s" % GUARD,
         "execute if predicate rpg:prologue/sneaking run return run function rpg:prologue/role/ult",
         "function rpg:prologue/role/skill"]
    fn("role/f", f)
    sk = ["execute if score @s rpg_pr_cd1 matches 1.. run return run playsound minecraft:block.note_block.bass master @s ~ ~ ~ 1 0.6",
          "scoreboard players set @s rpg_pr_cd1 240"]
    ul = ["execute if score @s rpg_pr_cd2 matches 1.. run return run playsound minecraft:block.note_block.bass master @s ~ ~ ~ 1 0.5",
          "scoreboard players set @s rpg_pr_cd2 1200", "scoreboard players set @s rpg_pr_av 400"]
    for k, (slug, zh, weapon, pillar, col) in ROLES.items():
        sk.append("execute if score @s rpg_pr_role matches %d run function rpg:pact/s/p%d" % (k, pillar))
        # 路西法的大招换成序章版「晨星加冕」（用户：白金为主，留一点蛇绿作特征色）；其余三位沿用七柱的化身招式
        ul.append("execute if score @s rpg_pr_role matches %d run function %s" % (
            k, "rpg:prologue/role/morning_star" if k == 1 else "rpg:pact/s/a%d" % pillar))
    ms = ["# 晨星加冕（as/at 路西法）：沿用万蛇加冕的伤害与增益，表现换成白金的星环与坠星，点缀一点蛇绿",
          "playsound minecraft:block.beacon.power_select player @a[distance=..32] ~ ~ ~ 1 1.4",
          "playsound minecraft:entity.evoker.cast_spell player @a[distance=..32] ~ ~ ~ 0.8 1.2",
          "particle minecraft:flash{color:[1.0,0.95,0.75,1.0]} ~ ~1 ~ 0 0 0 0 1",
          "particle minecraft:end_rod ~ ~1 ~ 4 1 4 0.08 80",
          "particle minecraft:dust{color:[0.37,0.84,0.55],scale:1.2} ~ ~0.3 ~ 4 0.2 4 0 24",
          "particle minecraft:firework ~ ~7 ~ 3.5 1 3.5 0 30"]
    for r, n in ((3, 16), (5, 24), (7, 32)):
        for i in range(n):
            ms.append("execute rotated %g 0 positioned ^ ^ ^%d run particle minecraft:dust{color:[1.0,0.9,0.55],scale:1.8} ~ ~0.2 ~ 0 0 0 0 1"
                      % (360.0 * i / n, r))
    ms += ["execute as @e[type=#rpg:seal_hostile,distance=..8] at @s run function rpg:prologue/role/morning_hit",
           "attribute @s minecraft:scale modifier remove rpg:pact/avatar",
           "attribute @s minecraft:attack_damage modifier remove rpg:pact/avatar",
           "attribute @s minecraft:scale modifier add rpg:pact/avatar 0.15 add_value",
           "attribute @s minecraft:attack_damage modifier add rpg:pact/avatar 6 add_value",
           "title @s times 5 50 15",
           "title @s subtitle %s" % js([{"text": "路西法 · 晨星  ", "color": "#F2CF7A", "bold": True, "italic": False},
                                        {"text": "Crown of the Morning Star", "color": "#BFB8A8", "italic": True}]),
           "title @s title %s" % js([{"text": "◆ ", "color": "#5FD68C", "bold": True, "italic": False},
                                     {"text": "晨星加冕", "color": "#FFF2C8", "bold": True, "italic": False},
                                     {"text": " ◆", "color": "#5FD68C", "bold": True, "italic": False}])]
    fn("role/morning_star", ms)
    fn("role/morning_hit", ["# 一颗坠星（as/at 被击中的敌人）",
                            "particle minecraft:end_rod ~ ~4 ~ 0.05 2 0.05 0.02 12",
                            "particle minecraft:flash{color:[1.0,0.92,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1",
                            "damage @s 12 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]"])
    fn("role/skill", sk)
    ul = ul[:3] + ["tag @s add rpg.pact.cast"] + ul[3:] + ["tag @s remove rpg.pact.cast"]
    sk = sk[:2] + ["tag @s add rpg.pact.cast"] + sk[2:] + ["tag @s remove rpg.pact.cast"]
    fn("role/skill", sk)
    fn("role/ult", ul)
    fn("role/avatar_off", ["attribute @s minecraft:%s modifier remove rpg:pact/avatar" % a for a in
                           ("armor", "armor_toughness", "attack_damage", "attack_speed", "luck", "max_health",
                            "movement_speed", "scale")] + ["scoreboard players set @s rpg_pr_av 0"])
    wj("rpg/predicate/prologue/sneaking.json", {"condition": "minecraft:entity_properties", "entity": "this",
                                                 "predicate": {"flags": {"is_sneaking": True}}})
    fn("player/tick", [
        "# 序章里的玩家每刻（as/at）",
        "execute if score @s rpg_pr_cd1 matches 1.. run scoreboard players remove @s rpg_pr_cd1 1",
        "execute if score @s rpg_pr_cd2 matches 1.. run scoreboard players remove @s rpg_pr_cd2 1",
        "execute if score @s rpg_pr_av matches 1.. run scoreboard players remove @s rpg_pr_av 1",
        "execute if score @s rpg_pr_av matches 0 run function rpg:prologue/role/avatar_off",
        "execute if score @s rpg_pr_down matches 1.. run function rpg:prologue/player/down",
        "execute unless entity @s[gamemode=adventure] run return 0",
        "scoreboard players operation #m %s = #t %s" % (O, O),
        "scoreboard players set #k %s 5" % O,
        "scoreboard players operation #m %s %%= #k %s" % (O, O),
        "execute if score #m %s matches 0 run function rpg:prologue/player/hud" % O,
        "execute if entity @s[tag=rpg.pr.mh] if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_pr_w:1b}] unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_pr_w:1b}] run function rpg:prologue/role/f",
        "tag @s remove rpg.pr.mh",
        "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_pr_w:1b}] run tag @s add rpg.pr.mh",
        "execute unless items entity @s weapon.offhand *[minecraft:custom_data~{rpg_pr_guard:1b}] unless items entity @s weapon.offhand *[minecraft:custom_data~{rpg_pr_w:1b}] run item replace entity @s weapon.offhand with %s" % GUARD,
        "execute in %s positioned 0 81 0 unless entity @s[distance=..70] run function rpg:prologue/player/to_west" % DIM,
    ])
    # 死亡保护被吃掉 = 倒下：旁观 5 秒，在场地西缘重新加入
    wj("rpg/advancement/prologue/fallen.json", {
        # 只挂触发器，不加条件（工程的 check_adv 只认原版写过的字段）；是不是序章里的人由奖励函数判断
        "criteria": {"t": {"trigger": "minecraft:used_totem"}},
        "rewards": {"function": "rpg:prologue/player/fallen"}})
    fn("player/fallen", [
        "advancement revoke @s only rpg:prologue/fallen",
        "execute unless entity @s[tag=rpg.pr] run return 0",
        "gamemode spectator @s",
        "scoreboard players set @s rpg_pr_down 100",
        "title @s times 5 70 10",
        "title @s subtitle %s" % js({"translate": "rpg.prologue.T10.en", "fallback": LINES["T10"]["en"], "color": "#BFB8A8"}),
        "title @s title %s" % js({"translate": "rpg.prologue.T10.zh", "fallback": LINES["T10"]["zh"], "color": "#E8D9B0"}),
    ])
    # 序章自己的状态栏（全局 HUD 对挂 rpg.pr 的人不绘制，见 exempt_hud）：技能与大招的冷却，中英对照
    ready = {"text": "就绪 Ready", "color": "#5FD68C", "italic": False}

    def left(sc):
        return [{"score": {"name": "@s", "objective": sc}, "color": "#FF805F", "italic": False},
                {"text": "s", "color": "#FF805F", "italic": False}]

    def line(k1, k2):
        return js(["", {"text": "F 技能 ", "color": "#E8D9B0", "bold": True, "italic": False},
                   {"text": "Skill ", "color": "#BFB8A8", "italic": False}] + k1 +
                  [{"text": "    ", "italic": False},
                   {"text": "潜行+F 大招 ", "color": "#E8D9B0", "bold": True, "italic": False},
                   {"text": "Ultimate ", "color": "#BFB8A8", "italic": False}] + k2)
    hud = ["scoreboard players operation @s rpg_pr_s1 = @s rpg_pr_cd1",
           "scoreboard players add @s rpg_pr_s1 19",
           "scoreboard players operation @s rpg_pr_s1 /= #twenty %s" % O,
           "scoreboard players operation @s rpg_pr_s2 = @s rpg_pr_cd2",
           "scoreboard players add @s rpg_pr_s2 19",
           "scoreboard players operation @s rpg_pr_s2 /= #twenty %s" % O]
    for c1, k1 in (("unless", [ready]), ("if", left("rpg_pr_s1"))):
        for c2, k2 in (("unless", [ready]), ("if", left("rpg_pr_s2"))):
            hud.append("execute %s score @s rpg_pr_cd1 matches 1.. %s score @s rpg_pr_cd2 matches 1.. run title @s actionbar %s"
                       % (c1, c2, line(k1, k2)))
    fn("player/hud", hud)
    fn("player/down", [
        "scoreboard players remove @s rpg_pr_down 1",
        "execute if score @s rpg_pr_down matches 0 if score #cut %s matches 0 run function rpg:prologue/player/rise" % O,
    ])
    fn("player/rise", ["gamemode adventure @s", "function rpg:prologue/player/to_west",
                       "effect give @s minecraft:instant_health 1 9 true",
                       "item replace entity @s weapon.offhand with %s" % GUARD])
    fn("player/to_west", ["execute in %s positioned %d 120 %d positioned over motion_blocking run tp @s ~ ~ ~ -90 0" % (DIM, WEST[0], WEST[1])])


# ---------------------------------------------------------------------------- 三波天使
def waves():
    def card(t_head, t_body):
        return ["title %s times 10 80 20" % PR,
                "title %s subtitle %s" % (PR, js({"translate": "rpg.prologue.%s.en" % t_head, "fallback": LINES[t_head]["en"], "color": "#BFB8A8", "italic": True})),
                "title %s title %s" % (PR, js({"translate": "rpg.prologue.%s.zh" % t_head, "fallback": LINES[t_head]["zh"], "color": "#E8D9B0", "bold": True})),
                "function rpg:prologue/sub/%s" % t_body.lower()]
    spawn = []
    for i in range(10):
        z = -12 + (i * 7) % 25
        x = 30 + (i * 5) % 9
        spawn.append("execute if score #k %s matches %d.. in %s positioned %d 120 %d positioned over motion_blocking run function rpg:prologue/wave/one"
                     % (O, i + 1, DIM, x, z))
    fn("wave/spawn", ["# 召 #k 名天使士兵，在场地东缘"] + spawn)
    fn("wave/one", [
        "# 天使士兵：隐身的卫道士载体套 rpg:prologue_angel（Sven 图集），手里是看不见的剑",
        "summon minecraft:vindicator ~ ~ ~ {Tags:[\"rpg.pr.foe\",\"rpg.pr.w.angel\",\"rpg.pr.angel\",\"rpg.pr.new\"],"
        "PersistenceRequired:1b,DeathLootTable:\"minecraft:empty\",Rotation:[90f,0f],Health:30f,"
        "attributes:[{id:\"max_health\",base:30d},{id:\"attack_damage\",base:5d},{id:\"follow_range\",base:48d}],"
        "equipment:{mainhand:{id:\"minecraft:iron_sword\",count:1,components:{\"minecraft:item_model\":\"rpg:empty\"}}},"
        "drop_chances:{mainhand:0f},active_effects:[{id:\"invisibility\",duration:-1,amplifier:0,show_particles:0b}]}",
        "execute as @e[type=minecraft:vindicator,tag=rpg.pr.new] at @s run function rpg:prologue_angel/dress",
        "tag @e[type=minecraft:vindicator,tag=rpg.pr.new] remove rpg.pr.new"])
    fn("wave/start1", ["scoreboard players set #wave %s 1" % O, "scoreboard players set #wt %s 0" % O] + card("T01", "T02") + [
        "scoreboard players operation #k %s = #n %s" % (O, O), "scoreboard players operation #k %s += #n %s" % (O, O),
        "scoreboard players add #k %s 4" % O, "function rpg:prologue/wave/spawn"])
    fn("wave/start2", ["scoreboard players set #wave %s 2" % O, "scoreboard players set #wt %s 0" % O] + card("T03", "T04") + [
        "scoreboard players operation #k %s = #n %s" % (O, O), "scoreboard players operation #k %s += #n %s" % (O, O),
        "scoreboard players add #k %s 4" % O, "function rpg:prologue/wave/spawn"])
    fn("wave/start3", ["scoreboard players set #wave %s 3" % O, "scoreboard players set #wt %s 0" % O] + card("T05", "T06") + [
        "execute in %s positioned 10 83 0 run function rpg:prologue/throne/summon" % DIM])
    fn("wave/tick", [
        "scoreboard players add #wt %s 1" % O,
        "execute if score #wave %s matches 0 if score #wt %s matches 20 run function rpg:prologue/wave/start1" % (O, O),
        "execute if score #wave %s matches 3 run function rpg:prologue/throne/tick" % O,
        "execute store result score #foe %s if entity @e[tag=rpg.pr.foe]" % O,
        "execute if score #wave %s matches 1..3 if score #wt %s matches 60.. if score #foe %s matches 0 run function rpg:prologue/wave/cleared" % (O, O, O),
        "execute if score #wave %s matches 11 if score #wt %s matches 80 run function rpg:prologue/wave/start2" % (O, O),
        "execute if score #wave %s matches 12 if score #wt %s matches 80 run function rpg:prologue/wave/start3" % (O, O),
        "execute if score #wave %s matches 13 if score #wt %s matches 40 run function rpg:prologue/sub/t09" % (O, O),
        "execute if score #wave %s matches 13 in %s positioned 0 81 0 if entity @a[tag=rpg.pr,gamemode=adventure,distance=..6] run function rpg:prologue/flow/cut3" % (O, DIM),
        "execute as @e[tag=rpg.pr.foe] at @s in %s positioned 0 81 0 unless entity @s[distance=..75] run function rpg:prologue/cut/kill_actor" % DIM,
    ])
    fn("wave/cleared", ["scoreboard players add #wave %s 10" % O, "scoreboard players set #wt %s 0" % O,
                        "function rpg:prologue/sub/t08",
                        "execute as %s at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6 1.2" % PR])
    # 座天使：一团悬空的眼（占位：放大的末影之眼），四只眼轮是四只隐形的史莱姆（近战和箭都打得到）。
    # 四只要在 3 秒内全打碎，否则合上复原；它每 2.5 秒朝一个人放一道圣光
    # 史莱姆（缩放 2.6，约 1.35 格高）脚底在眼轮中心下方 0.65 格，碰撞箱正好包住模型上的那只眼轮
    wheels = [(0, 2.2 - 0.65, 0), (0, -2.0 - 0.65, 0), (0, -0.65, 2.4), (0, -0.65, -2.4)]
    s = ["# 座天使（at 它的中心）",
         "summon minecraft:vindicator ~ ~ ~ {Tags:[\"rpg.pr.throne\",\"rpg.pr.ent\",\"rpg.pr.w.throne\",\"rpg.pr.new\"],NoAI:1b,NoGravity:1b,"
         "Silent:1b,Invulnerable:1b,PersistenceRequired:1b,Rotation:[0f,0f],"
         "active_effects:[{id:\"invisibility\",duration:-1,amplifier:0,show_particles:0b}]}",
         "execute as @e[type=minecraft:vindicator,tag=rpg.pr.new] at @s run function rpg:prologue_throne/dress",
         "tag @e[type=minecraft:vindicator,tag=rpg.pr.new] remove rpg.pr.new",
         "scoreboard players set #thr %s 0" % O, "scoreboard players set #first %s 0" % O]
    for i, (dx, dy, dz) in enumerate(wheels):
        s.append("summon minecraft:slime ~%g ~%g ~%g {Tags:[\"rpg.pr.foe\",\"rpg.pr.wheel\",\"rpg.pr.w%d\"],Size:0,NoAI:1b,NoGravity:1b,Silent:1b,"
                 "PersistenceRequired:1b,DeathLootTable:\"minecraft:empty\",Health:%df,attributes:[{id:\"max_health\",base:%df},{id:\"scale\",base:2.6}],"
                 "active_effects:[{id:\"invisibility\",duration:-1,amplifier:0,show_particles:0b}]}" % (dx, dy, dz, i, WHEEL_HP, WHEEL_HP))
    # 史莱姆读档时按体型重设最大生命（Size 0 只有 1 点），所以召出来以后再把血量设回去
    fix = ["execute as @e[type=minecraft:slime,tag=rpg.pr.wheel] run attribute @s minecraft:max_health base set %d" % WHEEL_HP,
           "execute as @e[type=minecraft:slime,tag=rpg.pr.wheel] run data merge entity @s {Health:%df}" % WHEEL_HP]
    fn("throne/summon", s + fix + ["playsound minecraft:block.beacon.activate master @a[tag=rpg.pr] ~ ~ ~ 2 1.4"])
    fn("throne/tick", [
        "# 被打碎的眼轮：模型上对应的那只换成空模型（史莱姆 rpg.pr.w<i> ↔ 眼轮 上/下/左/右）",
    ] + ["execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,tag=!rpg.pr.thb%d] unless entity @e[type=minecraft:slime,tag=rpg.pr.w%d] "
         "run function rpg:prologue/throne/break%d" % (i, i, i) for i in range(4)] + [
        "execute unless entity @e[type=minecraft:vindicator,tag=rpg.pr.throne] run return 0",
        "scoreboard players add #thr %s 1" % O,
        "execute store result score #wl %s if entity @e[type=minecraft:slime,tag=rpg.pr.wheel]" % O,
        "execute if score #first %s matches 0 if score #wl %s matches ..3 run scoreboard players operation #first %s = #thr %s" % (O, O, O, O),
        "execute if score #wl %s matches 0 run return run function rpg:prologue/throne/die" % O,
        "scoreboard players operation #m %s = #thr %s" % (O, O),
        "scoreboard players operation #m %s -= #first %s" % (O, O),
        "execute if score #first %s matches 1.. if score #m %s matches 60.. run function rpg:prologue/throne/close" % (O, O),
        "scoreboard players operation #m %s = #thr %s" % (O, O),
        "scoreboard players set #k %s 50" % O,
        "scoreboard players operation #m %s %%= #k %s" % (O, O),
        "execute if score #m %s matches 0 as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s as @r[tag=rpg.pr,gamemode=adventure,distance=..32] run function rpg:prologue/throne/beam" % O,
        "execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s run particle minecraft:end_rod ~ ~ ~ 1.2 1.2 1.2 0.01 2",
    ])
    fn("throne/beam", [
        "# 一道圣光（as 被瞄准的玩家，at 座天使）",
        "particle minecraft:flash{color:[1.0,0.9,0.6,1.0]} ~ ~ ~ 0 0 0 0 1",
        "execute facing entity @s eyes run function rpg:prologue/throne/beam_line",
        "damage @s 4 minecraft:magic",
        "playsound minecraft:entity.guardian.attack master @s ~ ~ ~ 1 1.4",
    ])
    fn("throne/beam_line", ["particle minecraft:end_rod ^ ^ ^%d 0 0 0 0 1" % d for d in range(1, 24, 2)])
    for i, w in enumerate(("up", "down", "right", "left")):          # 模型的 wheel_left 在世界 -Z 一侧
        fn("throne/break%d" % i, ["tag @s add rpg.pr.thb%d" % i, "function rpg:prologue_throne/wheel/%s" % w,
                                  "execute at @s run particle minecraft:end_rod ~ ~2 ~ 1 1 1 0.15 40",
                                  "execute at @s run playsound minecraft:block.glass.break master @a[tag=rpg.pr] ~ ~ ~ 1.5 0.6"])
    fn("throne/close", ["# 3 秒内没全打碎：眼轮合上复原",
                        "scoreboard players set #first %s 0" % O,
                        "kill @e[type=minecraft:slime,tag=rpg.pr.wheel]",
                        "execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s run function rpg:prologue/throne/rewheel",
                        "function rpg:prologue/sub/t07"])
    fn("throne/rewheel", [x for x in s[1:] if x.startswith("summon minecraft:slime")] + fix +
       ["tag @s remove rpg.pr.thb%d" % i for i in range(4)] +
       ["function rpg:prologue_throne/wheel/restore_%s" % w for w in ("up", "down", "left", "right")] +
       ["playsound minecraft:block.respawn_anchor.charge master @a[tag=rpg.pr] ~ ~ ~ 1.5 1.2"])
    fn("throne/die", ["execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s run particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1",
                      "execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s run particle minecraft:end_rod ~ ~ ~ 1.5 1.5 1.5 0.2 120",
                      "execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s run playsound minecraft:entity.generic.explode master @a[tag=rpg.pr] ~ ~ ~ 1.5 0.8",
                      "execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] run function rpg:prologue/cut/kill_actor"])


# ---------------------------------------------------------------------------- 序章里的米迦勒
def michael():
    fn("michael/start", [
        "scoreboard players set #state %s 7" % O,
        "scoreboard players set #t %s 0" % O,
        "scoreboard players set #l2 %s 0" % O, "scoreboard players set #l3 %s 0" % O,
        "scoreboard players set #l4 %s 0" % O, "scoreboard players set #l1 %s 0" % O,
        "scoreboard players set #pro rpg_mk 1",
        "execute in %s positioned 4 81 0 rotated 90 0 run function rpg:michael_boss/summon" % DIM,
    ])
    fn("michael/tick", [
        "execute if score #t %s matches 8400.. run function rpg:prologue/michael/end" % O,
        "execute if score #fight rpg_mk matches 0 run function rpg:prologue/michael/end",
    ])
    fn("michael/hp", [
        "# 序章模式的血线（as/at 米迦勒，每 4 刻一次，由 #rpg:michael_boss/prologue_hp 调用）",
        "execute unless score #state %s matches 7 run return 0" % O,
        "execute unless entity @s[tag=rpg.pr.hpset] run function rpg:prologue/michael/hp_set",
        "scoreboard players operation #pct %s = @s rpg_mk_h" % O,
        "scoreboard players operation #pct %s *= #hund %s" % (O, O),
        "scoreboard players operation #pct %s /= #mmax %s" % (O, O),
        "execute if score #l2 %s matches 0 if score #pct %s matches ..75 run function rpg:prologue/michael/line2" % (O, O),
        "execute if score #l3 %s matches 0 if score #pct %s matches ..50 run function rpg:prologue/michael/line3" % (O, O),
        "execute if score #l4 %s matches 0 if score #pct %s matches ..35 run function rpg:prologue/michael/line4" % (O, O),
        "execute if score #l1 %s matches 0 if score @s rpg_mk_sk matches 14..16 run function rpg:prologue/michael/line_l01" % O,
        "execute if score #pct %s matches ..25 run function rpg:prologue/michael/end" % O,
    ])
    fn("michael/hp_set", [
        "# 血池按人数：400 + 200×人数（1 人 600，4 人 1200）",
        "tag @s add rpg.pr.hpset",
        "scoreboard players operation #mmax %s = #n %s" % (O, O),
        "scoreboard players set #k %s 200" % O,
        "scoreboard players operation #mmax %s *= #k %s" % (O, O),
        "scoreboard players add #mmax %s 400" % O,
        "execute store result entity @s Health float 1 run scoreboard players get #mmax %s" % O,
        "execute store result storage rpg:pr tmp.hp int 1 run scoreboard players get #mmax %s" % O,
        "function rpg:prologue/michael/hp_attr with storage rpg:pr tmp",
        "scoreboard players operation @s rpg_mk_h = #mmax %s" % O,
        "execute store result bossbar rpg:michael_boss max run scoreboard players get #mmax %s" % O,
    ])
    fn("michael/hp_attr", ["$attribute @s minecraft:max_health base set $(hp)", "$data merge entity @s {Health:$(hp)f}"])
    for k, lid in ((2, "M02"), (3, "M03"), (4, "M04")):
        fn("michael/line%d" % k, ["scoreboard players set #l%d %s 1" % (k, O), "function rpg:prologue/sub/%s" % lid.lower()])
    fn("michael/line_l01", ["scoreboard players set #l1 %s 1" % O, "function rpg:prologue/sub/l01"])
    fn("michael/end", [
        "# 血量见底或打满 7 分钟：脚本接管，进入场 6",
        "scoreboard players set #pro rpg_mk 0",
        "function rpg:michael_boss/clear",
        "function rpg:prologue/sub/clear",
        "function rpg:prologue/flow/cut6",
    ])
    hook_tag = os.path.join(DP, "data", "rpg", "tags", "function", "michael_boss", "prologue_hp.json")
    d = {"values": []}
    if os.path.isfile(hook_tag):
        d = json.load(io.open(hook_tag, encoding="utf-8"))
    if "rpg:prologue/michael/hp" not in d["values"]:
        d["values"].append("rpg:prologue/michael/hp")
    wj(os.path.join("rpg", "tags", "function", "michael_boss", "prologue_hp.json"), d)


# ---------------------------------------------------------------------------- 流程衔接与结尾
def flow():
    def cut(n, state):
        return ["scoreboard players set #state %s %d" % (O, state), "scoreboard players set #t %s 0" % O,
                "scoreboard players set #cut %s %d" % (O, n), "function rpg:prologue/cut/begin"]
    fn("flow/cut1", cut(1, 3))
    fn("flow/cut3", cut(3, 5))
    fn("flow/cut6", ["execute as @e[tag=rpg.pr.foe] run function rpg:prologue/cut/kill_actor",
                     "function rpg:prologue/music/end"] + cut(6, 8))
    fn("cut/next", [
        "# 一段过场放完：接下一段，或回到玩家操作",
        "execute if score #cut %s matches 1 run return run function rpg:prologue/flow/after1" % O,
        "execute if score #cut %s matches 3 run return run function rpg:prologue/flow/after3" % O,
        "execute if score #cut %s matches 4 run return run function rpg:prologue/flow/after4" % O,
        "execute if score #cut %s matches 6 run return run function rpg:prologue/flow/after6" % O,
        "execute if score #cut %s matches 7 run return run function rpg:prologue/flow/after7" % O,
    ])
    back = ["kill @e[type=minecraft:item_display,tag=rpg.pr.cam]", "scoreboard players set #cut %s 0" % O,
            "gamemode adventure %s" % PR, "execute as %s run function rpg:prologue/player/to_west" % PR]
    fn("flow/after1", back + ["function rpg:prologue/music/waves", "scoreboard players set #state %s 4" % O, "scoreboard players set #wave %s 0" % O,
                              "scoreboard players set #wt %s 0" % O])
    fn("flow/after3", ["scoreboard players set #state %s 6" % O, "scoreboard players set #cut %s 4" % O,
                       "scoreboard players set #ct %s 0" % O])
    fn("flow/after4", ["kill @e[type=minecraft:item_display,tag=rpg.pr.cam]", "scoreboard players set #cut %s 0" % O,
                       "gamemode adventure %s" % PR,
                       "execute as %s in %s run tp @s -6 81 0 -90 0" % (PR, DIM),
                       "function rpg:prologue/michael/start"])
    fn("flow/after6", ["scoreboard players set #state %s 9" % O, "scoreboard players set #cut %s 7" % O,
                       "scoreboard players set #ct %s 0" % O])
    fn("flow/after7", ["kill @e[type=minecraft:item_display,tag=rpg.pr.cam]", "scoreboard players set #cut %s 0" % O,
                       "scoreboard players set #state %s 10" % O, "scoreboard players set #t %s 0" % O])
    feather = ('minecraft:paper[minecraft:item_model="rpg:prologue_feather",minecraft:max_stack_size=1,'
               'minecraft:custom_data={rpg_pr_feather:1b},minecraft:rarity="epic",minecraft:enchantment_glint_override=true,'
               'minecraft:custom_name=%s,minecraft:lore=[%s,%s,%s,%s,%s,%s,%s]]' % (
                   # 物品规范（ART-STYLE §2）：[序章] 前缀加粗圣金、本名白色；Lore 分隔线 + 题记 + 灰色正文，
                   # 英文原句作 MUTED 小字跟在中文下面
                   js(["", {"text": "[序章]", "color": "#FFD85A", "bold": True, "italic": False},
                       {"text": LINES["R01"]["zh"], "color": "#FFFFFF", "bold": False, "italic": False}]),
                   js(["", {"text": "+------------------+", "color": "#FFFFFF", "italic": False}]),
                   js(["", {"text": "[" + LINES["R03"]["zh"].rstrip("。") + "]", "color": "#FFD85A", "bold": True, "italic": False}]),
                   js(["", {"text": LINES["R03"]["en"], "color": "#797979", "italic": False}]),
                   js(["", {"text": LINES["R02"]["zh"], "color": "gray", "italic": False}]),
                   js(["", {"text": LINES["R02"]["en"], "color": "#797979", "italic": False}]),
                   js(["", {"text": LINES["R01"]["en"], "color": "#797979", "italic": False}]),
                   js(["", {"text": "+------------------+", "color": "#FFFFFF", "italic": False}])))
    fn("finish", [
        "# 结尾：送回原处；第一次通关的人得到米迦勒之羽",
        "execute if score #t %s matches 1 run function rpg:prologue/sub/u14" % O,
        "execute if score #t %s matches 40 as %s run function rpg:prologue/give_back" % (O, PR),
        "execute if score #t %s matches 41 run function rpg:prologue/cleanup" % O,
    ])
    fn("give_back", [
        "function rpg:prologue/iso/restore",
        "execute unless score @s rpg_pr_done matches 1.. run function rpg:prologue/reward",
        "scoreboard players set @s rpg_pr_done 1",
    ])
    fn("reward", ["give @s %s" % feather,
                  "title @s times 10 60 20",
                  "title @s subtitle %s" % js({"translate": "rpg.prologue.U15.en", "fallback": LINES["U15"]["en"], "color": "#BFB8A8"}),
                  "title @s title %s" % js({"translate": "rpg.prologue.U15.zh", "fallback": LINES["U15"]["zh"], "color": "#FFD85A"}),
                  "playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1"])


MUSIC = ["prologue_intro", "prologue_waves", "prologue_michael", "prologue_end"]


def music():
    """序章配乐（唱片机音量，同 Boss 战）：每首放完自己循环；进下一段就换曲。曲子登记在 add_boss_bgm.py。"""
    tick = ["execute unless score #bgm %s matches 1.. run return 0" % O, "scoreboard players remove #bgm %s 1" % O]
    for i, name in enumerate(MUSIC, 1):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bgm_ref", name + ".ogg")
        ticks = int(text.ogg_seconds(path) * 20) + 1 if os.path.isfile(path) else 1200
        fn("music/%s" % name.split("_")[1], [
            "stopsound %s record" % PR, "stopsound %s music" % PR,
            "execute as %s at @s run playsound rpg:bgm.%s record @s ~ ~ ~ 1 1" % (PR, name),
            "scoreboard players set #bgm %s %d" % (O, ticks), "scoreboard players set #bgmid %s %d" % (O, i)])
        tick.append("execute if score #bgm %s matches 0 if score #bgmid %s matches %d run function rpg:prologue/music/%s"
                    % (O, O, i, name.split("_")[1]))
    fn("music/tick", tick)


def exempt_taint():
    """挂 rpg.pr 的人不结算魔化（序章里握的是罪遗武器）。"""
    p = os.path.join(FUNC, "taint", "step.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    g = "# 序章里不结算魔化（add_prologue.py）\nexecute if entity @s[tag=rpg.pr] run return 0\n"
    if g not in s:
        io.open(p, "w", encoding="utf-8", newline="\n").write(g + s)


def exempt_hud():
    """全局 HUD（唯一的 actionbar 出口）对序章里的玩家不绘制：序章用自己的状态栏（player/hud）。"""
    p = os.path.join(FUNC, "hud", "hud.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    g = "# 序章里由 rpg:prologue/player/hud 绘制状态栏（add_prologue.py）\nexecute if entity @s[tag=rpg.pr] run return 0\n"
    if g not in s:
        io.open(p, "w", encoding="utf-8", newline="\n").write(g + s)


def main():
    global LINES
    LINES = text.load()
    nworld = world.write(DP)
    nlang = text.write_lang(RP, LINES)
    nvo = text.vo_sounds(RP, LINES)
    entry()
    ticker()
    isolation()
    build_arena()
    lobby()
    roles()
    waves()
    michael()
    flow()
    music()
    text.sub_functions(fn, LINES, P, O, PR)
    cuts.write(fn, LINES)
    hook_tag(DP, "load", P + "/load", False)
    hook_tag(DP, "tick", P + "/tick", True)
    exempt_taint()
    exempt_hud()
    print("prologue: %d functions, %d worldgen files, %d lang keys, %d voiced lines" % (COUNT, nworld, nlang, nvo))


LINES = {}
if __name__ == "__main__":
    main()
