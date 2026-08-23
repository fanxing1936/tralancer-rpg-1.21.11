# -*- coding: utf-8 -*-
"""多人适配：把单人下看不出来的三类错和一类卡顿改掉。

单人把这几件事混成了同一件事，所以它们全都藏得很好：

* **`@a` 就是"我"。** 只有一个玩家在线时，`@a[tag=...,limit=1,sort=nearest]`
  读起来就是"施法者"。两个人在线，它可能解析成**另一个人** —— 伤害记到
  旁观者头上，獠牙认错主人。
* **一个标签就是一个开关。** 在同一次函数调用里生死的标签没问题；
  一旦跨刻存活，两个玩家就可能同时挂着它，此时任何**不带距离**的
  `@a[tag=...]` 都会一起打到。
* **`bossbar set <id> players @s`** 是**赋值**，不是追加。写在
  `execute as @a[distance=..20]` 后面，等于每个玩家轮流把列表覆盖成自己 ——
  三个人在场，只有最后一个看得见血条。
* 而 `execute as @a ... run` 后面挂的一切，在 N 人服上就要付 N 遍。
  一次记分板比较无所谓，一次全表遍历就是灾难。

这一趟只做**多人正确性与伸缩性**，不碰任何数值与手感。
每处改动都带断言：改不到就报错，绝不静默跳过。
"""

import io
import os
import re
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")

fixes = []


def read(rel):
    with io.open(os.path.join(FUNC, rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel, text):
    p = os.path.join(FUNC, rel)
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text.rstrip("\n") + "\n")


def sub(rel, old, new, why):
    """一处替换，改不到就炸。"""
    s = read(rel)
    if new in s and old not in s:
        return                               # 幂等：已经改过
    assert old in s, "%s: 找不到要改的那一行\n%s" % (rel, old)
    write(rel, s.replace(old, new))
    fixes.append((rel, why))


# ---------------------------------------------------------------------------
# 1. damage_scan：每个玩家三次全表遍历 → 一次
# ---------------------------------------------------------------------------
# 这是全包最贵的一条按人数放大的路径。它挂在 `execute as @a at @s` 后面，
# 而三行各自开一次 `@e[type=!#rpg:no_damage_track,distance=..64]` ——
# 注意那是**否定**类型过滤，用不上实体类型索引，等于三次真正的全表走查。
# 五个人在线就是每刻十五次。
#
# 三行的先后依赖全在**同一个实体身上**（先记血量、再对齐基准、再比对），
# 所以把循环翻过来 —— 一次遍历，进函数把三件事一次做完 —— 结果逐字相同。
# opt_invert 当初因为"有回写又有回读"保守地放过了它，但那个依赖是实体内的，
# 翻转恰好保留。
DAMAGE_ONE = """\
# 一个实体的份。原本这三行各自开一次 @e[type=!#rpg:no_damage_track,distance=..64]，
# 而那是否定类型过滤 —— 用不上类型索引，三行就是三次真正的全表走查，
# 再乘以在线人数。依赖全在同一个实体身上，所以把循环翻过来结果逐字相同。
execute store result score @s damage_action run data get entity @s Health
# 第一次见到的实体先把基准对齐：否则它会被当成"刚受伤"，
# 读档时区块一批批加载，每批新实体都会误触发一次全部武器判定。
# `unless score X = X` 在分数不存在时成立，是判断"这个分数有没有值"的惯用写法。
execute unless score @s damage_timing = @s damage_timing run scoreboard players operation @s damage_timing = @s damage_action
execute unless score @s damage_action = @s damage_timing run tag @s add rpg.hurt
"""

DAMAGE_SCAN = """\
# Snapshot health for entities a player could plausibly have hit, and flag the
# ones whose health moved since last tick.  Run once per player from
# rpg:command/index instead of once per weapon-effect line for every entity.
#
# 一次遍历，逐实体进 damage_one 把三件事做完 —— 详见那边的注释。
execute as @e[type=!#rpg:no_damage_track,distance=..64] run function rpg:command/damage_one
"""


def fix_damage_scan():
    s = read("command/damage_scan.mcfunction")
    if "damage_one" in s:
        return
    assert s.count("@e[type=!#rpg:no_damage_track,distance=..64]") == 3, \
        "damage_scan 不是预期的三行形状，先看看它变成什么样了"
    write("command/damage_one.mcfunction", DAMAGE_ONE)
    write("command/damage_scan.mcfunction", DAMAGE_SCAN)
    fixes.append(("command/damage_scan", "每人 3 次全表遍历 → 全场 1 次/人"))


# ---------------------------------------------------------------------------
# 2. 萨麦尔的攻击附毒：从按人数放大的路径上挪下来
# ---------------------------------------------------------------------------
# 原来挂在 `execute as @a[tag=rpg.pact,scores={rpg_pact=5}] at @s` 后面，
# 两行各开一次不带类型的 `@e[tag=rpg.hurt]` —— 每个签了第五柱的玩家付两次。
# 但这条判定本身与"哪个玩家在跑"无关：它问的是**受伤实体的攻击者**是不是
# 第五柱。所以只需要全场跑一次，和 rpg:item/rune/wilt 一个形状。
SAMAEL = """\
# 暴怒的毒。走 rpg.hurt + on attacker，与包里其余被动同一形状。
#
# 这一趟**不按人数放大**：它问的是受伤实体的攻击者是不是第五柱，
# 与"哪个玩家在跑这条命令"无关，所以全场一次遍历就够。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.pact,scores={rpg_pact=5}] run function rpg:pact/samael_hit
"""

SAMAEL_HIT = """\
# 此刻 @s 是攻击者，执行位置仍在受伤者脚下 —— 所以毒要发给位置上的那一个。
effect give @e[distance=..1,limit=1] minecraft:poison 6 1 true
particle dust{color:[0.69,0.0,0.34],scale:1} ~ ~1 ~ 0.3 0.4 0.3 0.02 8
"""


def fix_samael():
    if "samael_hit" in read("pact/samael.mcfunction"):
        return
    write("pact/samael.mcfunction", SAMAEL)
    write("pact/samael_hit.mcfunction", SAMAEL_HIT)
    sub("exorcism.mcfunction",
        "execute as @a[tag=rpg.pact,scores={rpg_pact=5}] at @s run function rpg:pact/samael",
        "execute if entity @a[tag=rpg.pact,scores={rpg_pact=5},limit=1] "
        "run function rpg:pact/samael",
        "萨麦尔附毒不再按人数放大（2N 次遍历 → 1 次）")


# ---------------------------------------------------------------------------
# 3. 逆圣化：一处仪式失败，不该掐掉全世界的仪式
# ---------------------------------------------------------------------------
# `rpg.inv.subject` 跨刻存活，所以两个玩家可以同时挂着它。
# 而 inv_fail 里写的是**不带距离**的 `@a[tag=rpg.inv.subject]` ——
# 甲的图腾失败，会把地图另一头乙的仪式一起判失败。
#
# 同一个标签还有第二个毛病：受术者若死在圈外，标签留在身上没人来摘，
# 下一次仪式的判定就会被这个幽灵干扰。所以再给它配一个寿命。
def fix_inversion():
    sub("rite/inv_fail.mcfunction",
        "execute as @a[tag=rpg.inv.subject] run function rpg:rite/inv_abort",
        "# 只掐这一场。不带距离的话，甲这边失败会把地图另一头乙的仪式一起判掉。\n"
        "execute as @a[tag=rpg.inv.subject,distance=..48] run function rpg:rite/inv_abort",
        "仪式失败不再波及全世界的受术者")

    # 受术者的标签配一份寿命：图腾总长 200 刻，多给 20 刻宽限
    sub("rite/light_inv.mcfunction",
        "tag @a[distance=..7,scores={rpg_taint=100}] add rpg.inv.subject",
        "tag @a[distance=..7,scores={rpg_taint=100}] add rpg.inv.subject\n"
        "# 配一份寿命。受术者若死在圈外，没人来摘这个标签 ——\n"
        "# 留着它会干扰下一场仪式的判定。\n"
        "scoreboard players set @a[tag=rpg.inv.subject,distance=..7] rpg_inv 220",
        "受术者标签带上寿命，死在圈外不再留下幽灵")

    for rel in ("rite/inv_grant.mcfunction", "rite/inv_abort.mcfunction"):
        sub(rel, "tag @s remove rpg.inv.subject",
            "tag @s remove rpg.inv.subject\nscoreboard players set @s rpg_inv 0",
            "仪式收场时把寿命一并清零")

    s = read("exorcism.mcfunction")
    if "rpg_inv=1.." not in s:
        write("exorcism.mcfunction", s.rstrip("\n") + """

# 逆圣化受术者标签的寿命。两条都是玩家作用域，没在做仪式的人一条也进不去。
execute as @a[scores={rpg_inv=1..}] run scoreboard players remove @s rpg_inv 1
execute as @a[tag=rpg.inv.subject,scores={rpg_inv=..0}] run function rpg:rite/inv_abort
""")
        fixes.append(("exorcism", "受术者标签过期自动收场"))

    p = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg_inv " not in s:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\nscoreboard objectives add rpg_inv dummy\n")


# ---------------------------------------------------------------------------
# 4. 熔岩链锯：獠牙认错主人
# ---------------------------------------------------------------------------
# 两处都是单人下看不出来的：
#   `@e[tag=rpg.saw.fang]` 不带距离也不带类型 —— 会把**另一个玩家**刚召出来的
#   獠牙一起改主人，然后连标签一起摘掉，对方那一轮就断了；
#   `@p[tag=rpg.h.dawn_tag1]` 取的是"离目标最近的持锯者"，两个人都拿着锯时，
#   伤害会记到站得更近的那一个头上。
#
# 施法者本来就是 @s（saw 是 `as @a[...] at @s` 调进来的），只是进了
# `execute as @e[...]` 之后 @s 被改绑成了目标。所以挂一个只在本次调用里
# 存活的标签 —— 同一刻只可能有一个玩家挂着它，limit=1 就是精确的。
def fix_saw():
    s = read("item/epic/saw_cut.mcfunction")
    if "rpg.saw.cast" in s:
        return
    s = ("# 施法者只在本次调用里挂这个标签 —— 同一刻只可能有一个玩家挂着，\n"
         "# 所以下面的 limit=1 是精确的，而不是\"离目标最近的持锯者\"。\n"
         "tag @s add rpg.saw.cast\n" + s)
    s = s.replace("@p[tag=rpg.h.dawn_tag1]", "@a[tag=rpg.saw.cast,limit=1]")
    # 獠牙只认自己这一轮召出来的：带类型（走索引）且带距离
    s = s.replace("@e[tag=rpg.saw.fang]",
                  "@e[type=minecraft:evoker_fangs,tag=rpg.saw.fang,distance=..6]")
    s = s.rstrip("\n") + "\ntag @s remove rpg.saw.cast\n"
    write("item/epic/saw_cut.mcfunction", s)
    fixes.append(("item/epic/saw_cut", "獠牙与伤害归属锁定到真正的施法者"))


# ---------------------------------------------------------------------------
# 5. 晶啸：震荡的伤害归属
# ---------------------------------------------------------------------------
# 调用处已经确认攻击者在 8 格内（`if entity @a[tag=rpg.epic.chime,distance=..8]`），
# 但归属那一行没跟着限距，于是两个持晶啸的人同刻命中时可能记错人。
def fix_chime():
    sub("item/epic/chime_wave.mcfunction",
        "by @a[tag=rpg.epic.chime,limit=1,sort=nearest]",
        "by @a[tag=rpg.epic.chime,limit=1,sort=nearest,distance=..8]",
        "震荡伤害归属跟随调用处的 8 格判定")


# ---------------------------------------------------------------------------
# 6. Boss 血条：三个人在场只有一个看得见
# ---------------------------------------------------------------------------
# `bossbar set <id> players @s` 是**赋值**。写在 `execute as @a[distance=..20]`
# 后面，每个玩家轮流把整份名单覆盖成自己 —— 最后一个执行的人独占血条。
# 一次性把名单设成整组即可，顺带少跑 N-1 条命令。
def fix_bossbar():
    for rel in ("entities/warden/action.mcfunction",
                "entities/warden/action2.mcfunction"):
        sub(rel,
            "execute as @a[distance=..20] at @s run bossbar set minecraft:devil players @s",
            "# `bossbar ... players` 是赋值不是追加 —— 逐个玩家写，等于每人\n"
            "# 轮流把名单覆盖成自己，最后只有一个人看得见血条。一次设整组。\n"
            "bossbar set minecraft:devil players @a[distance=..20]",
            "Boss 血条对在场所有人可见")


# ---------------------------------------------------------------------------
# 7. Boss 血条在全新服务器上根本不存在
# ---------------------------------------------------------------------------
# `command/bossbar.mcfunction` 建了 minecraft:devil 这条血条，但**没有任何地方
# 调用它** —— 作者本机的存档里它之所以在，是因为当年手敲过一次，而 bossbar
# 存在 level.dat 里。换一个全新的服务器存档，Boss 一出场，
# `bossbar set minecraft:devil ...` 每一条都会报"没有这个 bossbar"。
# 挂进 load 标签即可（与 soreboard 每次加载重建记分项同一形状）。
def fix_bossbar_load():
    import json
    p = os.path.join(DP, "data/minecraft/tags/function/load.json")
    doc = json.load(io.open(p, encoding="utf-8"))
    if "rpg:command/bossbar" in doc["values"]:
        return
    doc["values"].append("rpg:command/bossbar")
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    fixes.append(("minecraft/load", "Boss 血条在全新存档上也会被建出来"))


# ---------------------------------------------------------------------------
# 8. `as @e ... if entity @s[...]` —— 先把全世界绑一遍，再逐个问要不要
# ---------------------------------------------------------------------------
# `item/chestplate/off` 是 command/tick 调的**第一个**函数，里面八行长这样：
#
#     execute as @e at @s if entity @s[scores={absorption=0..},tag=X] run ...
#
# `@e` 不带任何过滤 = 世界上每一个已加载实体。对每一个都要 `as` 绑定、
# `at` 重定位，然后再跑一次嵌套 execute 去问"你是不是我要找的"。
# 把条件折回选择器里，筛选发生在遍历本身，八分之七的实体连上下文都不用建：
#
#     execute as @e[scores={absorption=0..},tag=X] at @s run ...
#
# 语义完全相同 —— 两种写法筛的是同一批实体。折完之后相邻几行开的是同一个
# 选择器，opt_invert 还能把它们再并成一次遍历。
#
# 这不算多人专属问题，但多人直接把它放大：人越多，已加载区块越多，
# 世界上的实体也就越多，而这八行的代价正比于那个数字。
FOLD = re.compile(r"^execute as @e (at @s )?if entity @s\[([^\]]*)\] (.*)$")


def fix_bare_walks():
    changed = 0
    for rel in ("item/chestplate/off.mcfunction",):
        out = []
        for line in read(rel).split("\n"):
            m = FOLD.match(line.strip())
            if not m:
                out.append(line)
                continue
            at, filt, rest = m.group(1) or "", m.group(2), m.group(3)
            line = "execute as @e[%s] %s%s" % (filt, at, rest)
            out.append(line.replace("at @s at @s ", "at @s "))
            changed += 1
        if changed:
            write(rel, "\n".join(out))
    if changed:
        fixes.append(("item/chestplate/off",
                      "%d 行全世界绑定 → 折进选择器，交给 opt_invert 再并" % changed))


def main():
    fix_damage_scan()
    fix_samael()
    fix_inversion()
    fix_saw()
    fix_chime()
    fix_bossbar()
    fix_bossbar_load()
    fix_bare_walks()
    print("multiplayer: %d fixes" % len(fixes))
    for rel, why in fixes:
        print("  %-30s %s" % (rel, why))


if __name__ == "__main__":
    main()
