# -*- coding: utf-8 -*-
"""把包里原有的三件驱魔道具接进驱魔体系。

它们早就写着驱魔的文案，却谁也没接上：

* **替死人偶**　Lore 写「可以抵挡恶魔的人偶，恶魔攻击其会使祂显形」——
  实际上只是召出一只发光不动的悦灵，**一行逻辑都没有**
* **圣水**　同样零逻辑。更糟的是驱魔仪式那边只判「附近有没有 area_effect_cloud」，
  于是**任何**滞留药水都能点燃图腾——一瓶滞留伤害药水也行
* **天启星**　有逻辑，但只照 `devil` / `devil2` 标签、半径 7 格，
  与魔化值、空缺者、仪式全都不相干

三件各补一条与体系咬合的作用，并且都顺着各自的 Lore：

**替死人偶 —— 替死 + 显形。**
立在那儿时，12 格内的空缺者不必持圣器也会显形（这正是「使祂显形」）；
而 16 格内的雇主每一轮沾上的魔化，改由人偶承受——它一次吃一点，
10 点吃满就碎。这是全包唯一能"挡住"魔化的东西。

**圣水 —— 名副其实的点火之物。**
给药水云按颜色打上标记，仪式改判这个标记（顺手堵掉"任意滞留药水都能点燃"
那个洞）；云本身每秒洗掉 1 点魔化，并灼烧范围内的空壳——被圣水浇过的壳
裂得更快。

**天启星 —— 指引与审判。**
半径从 7 扩到 32，照的范围从"恶魔标签"扩到空缺者与已经沾染的人；
对空壳直接造成伤害（"审判罪恶"）。仍然是一次性的。
"""

import io
import json
import os
import re
import sys

import add_exorcism as ex

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")

DOLL_R = 12          # 人偶让空壳显形的半径
DOLL_TAKE = 16       # 人偶替谁挡：这个半径内的人
POOL_R = 4           # 圣水池子的半径
POOL_BEAT = 20       # 池子的结算节拍（刻）
STAR_R = 32          # 天启星照多远

# 圣水的 custom_color。两瓶已经合并成一瓶（驱魔圣水，16777200），
# 但旧那瓶的颜色仍然留着 —— 存档里已经有的不该突然失效。
HOLY_COLOURS = (3866074, 16777200)


# ---------------------------------------------------------------------------
# 替死人偶
# ---------------------------------------------------------------------------
DOLL_TICK = """\
# 替死人偶。立着的时候，它替周围把空壳照出来 ——
# Lore 写的「恶魔攻击其会使祂显形」，这里给的是它在驱魔体系里的对应物：
# 不必持圣器，人偶自己就是一盏灯。
execute as @e[type=minecraft:allay,tag=rpg.doll] at @s run function rpg:doll/shine
"""

DOLL_SHINE = """\
# 以人偶为中心照一圈。
particle end_rod ~ ~0.4 ~ 0.25 0.3 0.25 0.01 2
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..%(R)d] at @s run function rpg:vacant/reveal
"""

DOLL_TAKE_F = """\
# 人偶替你脏。这一轮沾上多少，就从你身上还回去多少，转嫁到它身上。
#
# #t1 是上一步算出来的"这一轮的净增量"，所以扣得精确 ——
# 不用去猜玩家手里握着几件魔器。
scoreboard players operation @s rpg_taint -= #t1 rpg_hud
title @s actionbar ["",{"text":"人偶替你受下了","italic":true,"color":"#C9A227"}]
execute as @e[type=minecraft:allay,tag=rpg.doll,distance=..%(TAKE)d,limit=1,sort=nearest] at @s run function rpg:doll/hurt
"""

DOLL_HURT = """\
# 人偶身上多一道裂。10 点生命 = 能替你挡十轮，挡满就碎。
# 先看这一下是不是致命的那一下 —— 放在扣血之后判会早报一拍。
execute if entity @s[nbt={Health:1.0f}] run function rpg:doll/shatter
damage @s 1 minecraft:magic
particle sculk_soul ~ ~0.5 ~ 0.2 0.25 0.2 0.05 14
particle dust{color:[0.32,0.16,0.42],scale:1} ~ ~0.5 ~ 0.2 0.25 0.2 0.02 10
playsound minecraft:block.amethyst_block.break hostile @a[distance=..16] ~ ~ ~ 0.7 0.6
"""

DOLL_SHATTER = """\
# 最后一道裂。人偶碎掉，把吃进去的东西一次吐干净。
particle sculk_charge_pop ~ ~0.6 ~ 0.4 0.4 0.4 0.15 60
particle end_rod ~ ~0.6 ~ 0.4 0.4 0.4 0.08 40
playsound minecraft:entity.allay.death hostile @a[distance=..24] ~ ~ ~ 1 0.7
playsound minecraft:block.amethyst_cluster.break hostile @a[distance=..24] ~ ~ ~ 1 0.5
title @a[distance=..12] actionbar ["",{"text":"人偶碎了","italic":true,"color":"gray"}]
"""


# ---------------------------------------------------------------------------
# 圣水
# ---------------------------------------------------------------------------
AEC_SCAN = """\
# 给新出现的药水云验明正身，只验一次。
#
# 之所以要打标记：仪式那边原本只判"附近有没有 area_effect_cloud"，
# 于是**任何**滞留药水都能点燃图腾 —— 一瓶滞留伤害药水也行。
# 按 custom_color 认水，认过就挂 rpg.aec.seen，不再重复验。
execute as @e[type=minecraft:area_effect_cloud,tag=!rpg.aec.seen] run function rpg:rite/aec
"""

AEC_ONE = """\
tag @s add rpg.aec.seen
%(TESTS)s
"""

POOL_TICK = """\
# 圣水落地之后就是一汪能用的水。
execute as @e[type=minecraft:area_effect_cloud,tag=rpg.holy_water] at @s run function rpg:rite/pool
"""

POOL = """\
# 每 %(BEAT)d 刻结算一次 —— 逐刻洗魔化太快，也白费开销。
scoreboard players add @s rpg_rite 1
execute if entity @s[scores={rpg_rite=%(BEAT)d..}] run function rpg:rite/pool_beat
"""

POOL_BEAT_F = """\
scoreboard players set @s rpg_rite 0
particle end_rod ~ ~0.2 ~ %(R_HALF)s 0.1 %(R_HALF)s 0.02 24
particle dust{color:[1.0,0.98,0.86],scale:1} ~ ~0.2 ~ %(R_HALF)s 0.1 %(R_HALF)s 0.01 16
execute as @a[distance=..%(R)d] run scoreboard players remove @s rpg_taint 1
execute as @a[distance=..%(R)d,scores={rpg_taint=..-1}] run scoreboard players set @s rpg_taint 0
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..%(R)d] at @s run function rpg:vacant/scald
"""

SCALD = """\
# 圣水浇在空壳上。壳撑不了那么久 —— 被浇过的裂得快得多。
effect give @s minecraft:glowing 4 0 true
scoreboard players add @s rpg_vac_x 20
particle sculk_soul ~ ~1.2 ~ 0.3 0.4 0.3 0.04 16
particle smoke ~ ~1 ~ 0.2 0.3 0.2 0.02 10
playsound minecraft:block.lava.extinguish hostile @a[distance=..16] ~ ~ ~ 0.8 1.4
execute if entity @s[scores={rpg_vac_x=%(TEAR)d..},tag=!rpg.vac.torn] run function rpg:vacant/tear
"""


# ---------------------------------------------------------------------------
# 天启星
# ---------------------------------------------------------------------------
STAR_EXTRA = """
# ---- 驱魔适配 ----
# 「能指引恶魔的繁星，审判罪恶」—— 原本这颗星只照 devil 标签、半径 7 格，
# 与魔化值和空缺者毫无交集。既然它是一颗**星**，照的范围理应远得多，
# 也理应照得出披着人皮的那些。
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..%(R)d] at @s run function rpg:item/devil/star/shell
execute as @a[distance=..%(R)d,scores={rpg_taint=31..}] at @s run function rpg:item/devil/star/judge
execute at @s run particle end_rod ~ ~1 ~ 0.6 1.2 0.6 0.4 120
execute at @s run particle flash{color:16777200} ~ ~1.4 ~ 0 0 0 0 1
execute at @s run playsound minecraft:block.beacon.power_select master @a[distance=..%(R)d] ~ ~ ~ 1 1.6
"""

STAR_SHELL = """\
# 照出一个空壳，并且审判它 —— 星光本身就是刑罚。
effect give @s minecraft:glowing 15 0 true
scoreboard players add @s rpg_vac_x 30
damage @s 6 minecraft:magic
particle end_rod ~ ~1.2 ~ 0.3 0.5 0.3 0.06 30
particle sculk_soul ~ ~1.2 ~ 0.3 0.4 0.3 0.03 16
playsound minecraft:block.beacon.activate hostile @a[distance=..24] ~ ~ ~ 0.8 1.5
"""

STAR_JUDGE = """\
# 沾染到一定程度的人，也在星光底下现形。
# 不扣血，只是让所有人看得见你身上带着什么。
effect give @s minecraft:glowing 15 0 true
particle soul_fire_flame ~ ~1 ~ 0.35 0.6 0.35 0.02 20
title @s actionbar ["",{"text":"星光照出了你身上的东西","italic":true,"color":"dark_red"}]
"""


def wf(rel, text):
    ex.wf(rel, text)


# 这几件物品的辨认方式：给予行里出现的名字。它们都是单行的 give。
HOLY_ITEMS = ("驱魔图腾", "驱魔圣水", "圣水", "天启星", "替死人偶")

GIVE_LINE = re.compile(r"^(give @a \w+\[)(.*)(\]\s*\d*)$")


def flag_holy_items():
    """给真正的圣物打上 holy_weapon_tag。

    `rpg.h.holy_weapon_tag1` 是"手里握着圣器"这个前提，而全包唯一写入
    `holy_weapon_tag` 的地方是武器分支的 item_modifier —— 于是在给武器加过
    神圣分支之前，这个前提**永远为假**，空缺者也就永远不显形。

    这里不动判定，而是让本来就是驱魔道具的这几件真的算作圣器。
    """
    n = 0
    for rel in ("command/give/item.mcfunction", "command/give/weapon.mcfunction",
                "command/give/extra.mcfunction"):
        q = os.path.join(FUNC, rel)
        if not os.path.isfile(q):
            continue
        out, touched = [], False
        for line in io.open(q, encoding="utf-8").read().split("\n"):
            m = GIVE_LINE.match(line.strip())
            if not m or "holy_weapon_tag" in line:
                out.append(line)
                continue
            if not any(k in line for k in HOLY_ITEMS):
                out.append(line)
                continue
            head, comps, tail = m.group(1), m.group(2), m.group(3)
            if "custom_data={" in comps:
                comps = comps.replace("custom_data={", "custom_data={holy_weapon_tag:1b,", 1)
            else:
                comps = comps + ",custom_data={holy_weapon_tag:1b}"
            out.append(head + comps + tail)
            touched = True
            n += 1
        if touched:
            io.open(q, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return n


# 归入驱魔一族的旧物品：名字 -> 新的前缀标签
RITE_PREFIX = {"替死人偶": "[驱魔]", "天启星": "[驱魔]"}

# 旧「圣水」的辨认方式：[brave] 前缀 + 名字恰好是「圣水」
OLD_WATER = re.compile(r'"text":"\[brave\]".{0,80}?"text":"圣水"')

TIER_TOKEN = re.compile(r'\{"text":"\[[^"]*\]"[^}]*\}')


def merge_and_prefix():
    """合并两瓶圣水，并把其余驱魔道具改挂 [驱魔] 前缀。

    功能上这四件是同一套东西（显形、净化、仪式），却散在三个稀有度里；
    而两瓶圣水本身就是重复的。归成一族，图鉴那边才好单开一节。
    """
    merged = renamed = 0
    for rel in ("command/give/item.mcfunction", "command/give/weapon.mcfunction",
                "command/give/extra.mcfunction"):
        q = os.path.join(FUNC, rel)
        if not os.path.isfile(q):
            continue
        out, touched = [], False
        for line in io.open(q, encoding="utf-8").read().split("\n"):
            # 旧圣水整行删掉 —— 驱魔圣水已经把它的活全接了
            if OLD_WATER.search(line):
                merged += 1
                touched = True
                continue
            hit = next((k for k in RITE_PREFIX if '"text":"%s"' % k in line), None)
            if hit and "[驱魔]" not in line:
                new = TIER_TOKEN.sub(
                    '{"text":"[驱魔]","italic":false,"color":"#FFD700","bold":true}',
                    line, count=1)
                if new != line:
                    line = new
                    renamed += 1
                    touched = True
            out.append(line)
        if touched:
            io.open(q, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return merged, renamed


# [HOLY] 品质：本来就是圣物，却没有标记
HOLY_QUALITY = re.compile(r'"text":"\[HOLY\]"')

# 圣器可以在这些槽位上生效。护甲拿在手里才算数是荒谬的 —— 它该穿着算。
HOLY_SLOTS = ("weapon.mainhand", "weapon.offhand",
              "armor.head", "armor.chest", "armor.legs", "armor.feet")


def holy_quality_and_worn():
    """给 [HOLY] 品质补标记，并让"圣器在身"包含穿戴。

    另开 `rpg.holy` 而不是扩写 `rpg.h.holy_weapon_tag1`：后者的语义是
    "手里握着"，神圣分支的命中特效读的就是它 —— 混进穿戴的话，
    戴着圣冠打人也会冒圣光。
    """
    marked = 0
    for rel in ("command/give/item.mcfunction", "command/give/weapon.mcfunction",
                "command/give/extra.mcfunction"):
        q = os.path.join(FUNC, rel)
        if not os.path.isfile(q):
            continue
        out, touched = [], False
        for line in io.open(q, encoding="utf-8").read().split("\n"):
            m = GIVE_LINE.match(line.strip())
            if not m or "holy_weapon_tag" in line or not HOLY_QUALITY.search(line):
                out.append(line)
                continue
            head, comps, tail = m.group(1), m.group(2), m.group(3)
            if "custom_data={" in comps:
                comps = comps.replace("custom_data={", "custom_data={holy_weapon_tag:1b,", 1)
            else:
                comps = comps + ",custom_data={holy_weapon_tag:1b}"
            out.append(head + comps + tail)
            touched = True
            marked += 1
        if touched:
            io.open(q, "w", encoding="utf-8", newline="\n").write("\n".join(out))

    # index_player 是 opt_index 那一步才生成的，所以「穿戴也算」那半边
    # 挪去了 opt_holy.py，跑在它后面。

    # ---- 驱魔体系改读 rpg.holy ----
    swapped = 0
    for rel in ("taint/step.mcfunction", "vacant/vacant.mcfunction",
                "exorcism.mcfunction"):
        q = os.path.join(FUNC, rel)
        if not os.path.isfile(q):
            continue
        t = io.open(q, encoding="utf-8").read()
        if "rpg.h.holy_weapon_tag1" not in t:
            continue
        swapped += t.count("rpg.h.holy_weapon_tag1")
        io.open(q, "w", encoding="utf-8", newline="\n").write(
            t.replace("rpg.h.holy_weapon_tag1", "rpg.holy"))
    return marked, swapped


def build_functions():
    # ---- 人偶 ----
    wf("doll/doll.mcfunction", DOLL_TICK)
    wf("doll/shine.mcfunction", DOLL_SHINE % {"R": DOLL_R})
    wf("doll/hurt.mcfunction", DOLL_HURT)
    wf("doll/shatter.mcfunction", DOLL_SHATTER)
    wf("taint/doll.mcfunction", DOLL_TAKE_F % {"TAKE": DOLL_TAKE})

    # ---- 圣水 ----
    tests = "\n".join(
        'execute if data entity @s {potion_contents:{custom_color:%d}} '
        'run tag @s add rpg.holy_water' % c for c in HOLY_COLOURS)
    wf("rite/aec_scan.mcfunction", AEC_SCAN)
    wf("rite/aec.mcfunction", AEC_ONE % {"TESTS": tests})
    wf("rite/pool_tick.mcfunction", POOL_TICK)
    wf("rite/pool.mcfunction", POOL % {"BEAT": POOL_BEAT})
    wf("rite/pool_beat.mcfunction",
       POOL_BEAT_F % {"R": POOL_R, "R_HALF": "%.1f" % (POOL_R * 0.5)})
    wf("vacant/scald.mcfunction", SCALD % {"TEAR": ex.TEAR_AT})

    # ---- 天启星 ----
    wf("item/devil/star/shell.mcfunction", STAR_SHELL)
    wf("item/devil/star/judge.mcfunction", STAR_JUDGE)


def patch_star():
    """把驱魔那几行接到天启星原有的函数上，接在自我消耗之前。"""
    p = os.path.join(FUNC, "item/devil/star/star.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "star/shell" in s:
        return 0
    anchor = "item replace entity @s weapon.mainhand with air"
    assert anchor in s, "天启星的函数不是预期的形状"
    io.open(p, "w", encoding="utf-8", newline="\n").write(
        s.replace(anchor, (STAR_EXTRA % {"R": STAR_R}).strip() + "\n" + anchor))
    return 1


def patch_taint():
    """魔化结算里插入"人偶替死"。

    必须精确知道**这一轮净增了多少**才能原样还回去，所以在增益行前后各取一次
    快照 —— 比去数玩家手里握着几件魔器可靠得多，将来加新的魔化来源也不用改这里。
    """
    p = os.path.join(FUNC, "taint/step.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "taint/doll" in s:
        return 0

    first = "execute if entity @s[tag=rpg.h.devil_tag1] run scoreboard players add @s rpg_taint 2"
    assert first in s, "taint/step 不是预期的形状（增益段）"
    s = s.replace(first,
                  "# 替死人偶要按「这一轮实际沾了多少」来还，所以先记一笔。\n"
                  "scoreboard players operation #t0 rpg_hud = @s rpg_taint\n"
                  + first)

    clamp = "execute if entity @s[scores={rpg_taint=..-1}] run scoreboard players set @s rpg_taint 0"
    assert clamp in s, "taint/step 不是预期的形状（下限钳制）"
    s = s.replace(clamp, clamp + "\n\n"
                  "# 身边立着替死人偶的话，这一轮沾上的由它承受。\n"
                  "scoreboard players operation #t1 rpg_hud = @s rpg_taint\n"
                  "scoreboard players operation #t1 rpg_hud -= #t0 rpg_hud\n"
                  "execute if score #t1 rpg_hud matches 1.. "
                  "if entity @e[type=minecraft:allay,tag=rpg.doll,distance=..%d,limit=1] "
                  "run function rpg:taint/doll" % DOLL_TAKE, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    return 1


def patch_rite_tick():
    """仪式改判「圣水」标记，而不是「随便什么滞留药水」。"""
    p = os.path.join(FUNC, "rite/tick.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg.holy_water" in s:
        return 0
    old = "if entity @e[type=minecraft:area_effect_cloud,distance=..3]"
    assert old in s, "rite/tick 不是预期的形状"
    io.open(p, "w", encoding="utf-8", newline="\n").write(
        s.replace(old,
                  "if entity @e[type=minecraft:area_effect_cloud,"
                  "tag=rpg.holy_water,distance=..3]"))
    return 1


def patch_doll_item():
    """给人偶召出来的悦灵打上标签，否则没有任何东西认得它。"""
    n = 0
    for rel in ("command/give/weapon.mcfunction", "command/give/box.mcfunction"):
        p = os.path.join(FUNC, rel)
        if not os.path.isfile(p):
            continue
        s = io.open(p, encoding="utf-8").read()
        if 'Tags:["rpg.doll"]' in s:
            continue
        new = re.sub(r"(\{id:allay,)", r'\1Tags:["rpg.doll"],', s)
        if new != s:
            io.open(p, "w", encoding="utf-8", newline="\n").write(new)
            n += new.count('Tags:["rpg.doll"]')
    return n


def wire_tick():
    p = os.path.join(FUNC, "exorcism.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg:doll/doll" in s:
        return 0
    s = s.rstrip("\n") + """

# 三件老驱魔道具。每条都带类型且过守卫 —— 场上没有对应的东西就整段跳过。
execute if entity @e[type=minecraft:allay,tag=rpg.doll,limit=1] run function rpg:doll/doll
execute if entity @e[type=minecraft:area_effect_cloud,tag=!rpg.aec.seen,limit=1] run function rpg:rite/aec_scan
execute if entity @e[type=minecraft:area_effect_cloud,tag=rpg.holy_water,limit=1] run function rpg:rite/pool_tick
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    return 3


def main():
    build_functions()
    a = patch_doll_item()
    b = patch_taint()
    c = patch_rite_tick()
    d = patch_star()
    e = wire_tick()
    g, h = merge_and_prefix()
    i, j = holy_quality_and_worn()
    f = flag_holy_items()
    print("holy items: doll tagged x%d, taint hook %d, rite gate %d, "
          "star extended %d, tick +%d, marked as holy x%d" % (a, b, c, d, e, f))
    print("holy items: old 圣水 lines merged away x%d, re-prefixed as 驱魔 x%d"
          % (g, h))
    print("holy items: [HOLY] quality marked x%d, exorcism now reads rpg.holy "
          "(worn counts) x%d" % (i, j))


if __name__ == "__main__":
    main()
