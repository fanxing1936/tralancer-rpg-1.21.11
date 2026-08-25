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
    # 有些 new 会完整包含 old（例如在原命令后追加寿命结算），
    # 不能用 `old not in s` 判幂等；否则第二次跑会把 new 里的 old
    # 再替换一遍，每次都多长一层。每个 sub 都是单点手术，new 存在就是已完成。
    if new in s:
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
execute as @e[tag=rpg.hurt] at @s run function rpg:pact/samael_victim
"""

SAMAEL_VICTIM = """\
# on attacker 会把 @s 换成攻击者；先给真正的受击者挂一个同步标签，
# 否则用 distance=..1,limit=1 会在拥挤的战团里毒到旁边那个实体。
tag @s add rpg.samael.victim
execute on attacker if entity @s[tag=rpg.pact,scores={rpg_pact=5}] run function rpg:pact/samael_hit
tag @s remove rpg.samael.victim
"""

SAMAEL_HIT = """\
# 此刻 @s 是攻击者，受击者由上一层的同步标签精确锁定。
effect give @e[tag=rpg.samael.victim,distance=..1,limit=1] minecraft:poison 6 1 true
particle dust{color:[0.69,0.0,0.34],scale:1} ~ ~1 ~ 0.3 0.4 0.3 0.02 8
"""


def fix_samael():
    if "samael_hit" in read("pact/samael.mcfunction"):
        return
    write("pact/samael.mcfunction", SAMAEL)
    write("pact/samael_victim.mcfunction", SAMAEL_VICTIM)
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
    # 第二阶段 fix_inversion_owned 会把这个距离版再升级成唯一 id 版；
    # 整个脚本重跑时若已看到最终形态，就不能退回去寻找最初那一行。
    if "if score @s rpg_inv_id = #inv_id rpg_inv_id" not in \
            read("rite/inv_fail.mcfunction"):
        sub("rite/inv_fail.mcfunction",
            "execute as @a[tag=rpg.inv.subject] run function rpg:rite/inv_abort",
            "# 只掐这一场。不带距离的话，甲这边失败会把地图另一头乙的仪式一起判掉。\n"
            "execute as @a[tag=rpg.inv.subject,distance=..48] run function rpg:rite/inv_abort",
            "仪式失败不再波及全世界的受术者")

    # 受术者的标签配一份寿命：图腾总长 200 刻，多给 20 刻宽限
    if "scoreboard players add #inv_seq rpg_inv_id 1" not in \
            read("rite/light_inv.mcfunction"):
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


def fix_inversion_owned():
    """在寿命修复之上，用唯一 id 隔离同时进行的逆圣化。

    只限距离不够：两支图腾靠近时，失败、节拍伤害和授痕都会串场。
    每支图腾与它的受术者共享 rpg_inv_id；图腾逐刻将它拷入同步
    临时格 #inv_id，所有后续操作同时验标签与 id。
    """
    sub("rite/inv_fail.mcfunction",
        "execute as @a[tag=rpg.inv.subject,distance=..48] run function rpg:rite/inv_abort",
        "execute as @a[tag=rpg.inv.subject] if score @s rpg_inv_id = #inv_id rpg_inv_id "
        "run function rpg:rite/inv_abort",
        "仪式失败按唯一 id 收尾，不再串场")

    for old, new in (
            ("@a[distance=..7,scores={rpg_taint=100}] run function rpg:rite/light_inv",
             "@a[tag=!rpg.inv.subject,distance=..7,scores={rpg_taint=100}] run return run function rpg:rite/light_inv"),
            ("@a[distance=..7,scores={rpg_taint=100}] run function rpg:rite/light_pure",
             "@a[tag=!rpg.inv.subject,distance=..7,scores={rpg_taint=100}] run function rpg:rite/light_pure")):
        sub("rite/light.mcfunction", old, new,
            "已在另一场逆圣化中的玩家不会被新图腾抢走")

    sub("rite/light_inv.mcfunction",
        "tag @a[distance=..7,scores={rpg_taint=100}] add rpg.inv.subject\n"
        "# 配一份寿命。受术者若死在圈外，没人来摘这个标签 ——\n"
        "# 留着它会干扰下一场仪式的判定。\n"
        "scoreboard players set @a[tag=rpg.inv.subject,distance=..7] rpg_inv 220",
        "scoreboard players add #inv_seq rpg_inv_id 1\n"
        "scoreboard players operation @s rpg_inv_id = #inv_seq rpg_inv_id\n"
        "tag @a[tag=!rpg.inv.subject,distance=..7,scores={rpg_taint=100}] add rpg.inv.new\n"
        "execute as @a[tag=rpg.inv.new,distance=..7] run scoreboard players operation @s rpg_inv_id = #inv_seq rpg_inv_id\n"
        "tag @a[tag=rpg.inv.new,distance=..7] add rpg.inv.subject\n"
        "# 寿命比图腾的 200 刻多给 20 刻，防止死在圈外留下幽灵标签。\n"
        "scoreboard players set @a[tag=rpg.inv.new,distance=..7] rpg_inv 220",
        "图腾与本批受术者写入同一个唯一仪式 id")

    for cmd in ("times 10 50 20",
                'title ["",{"text":"逆 圣 化","italic":false,"color":"dark_red","bold":true}]',
                'subtitle ["",{"text":"负与负相乘，站住别走","italic":false,"color":"gold"}]'):
        sub("rite/light_inv.mcfunction",
            "title @a[tag=rpg.inv.subject] " + cmd,
            "title @a[tag=rpg.inv.new,distance=..7] " + cmd,
            "逆圣化开场提示只发给本场新受术者")
    s = read("rite/light_inv.mcfunction")
    if "remove rpg.inv.new" not in s:
        write("rite/light_inv.mcfunction",
              s.rstrip("\n") + "\ntag @a[tag=rpg.inv.new,distance=..7] remove rpg.inv.new\n")
        fixes.append(("rite/light_inv", "本场临时受术者标签当场回收"))

    sub("rite/beat_inv.mcfunction",
        "execute unless entity @a[tag=rpg.inv.subject,distance=..7] run return run function rpg:rite/inv_fail",
        "scoreboard players operation #inv_id rpg_inv_id = @s rpg_inv_id\n"
        "scoreboard players set #inv_alive rpg_inv_id 0\n"
        "execute as @a[tag=rpg.inv.subject,distance=..7] if score @s rpg_inv_id = #inv_id rpg_inv_id "
        "run scoreboard players set #inv_alive rpg_inv_id 1\n"
        "execute unless score #inv_alive rpg_inv_id matches 1 run return run function rpg:rite/inv_fail",
        "图腾只承认与自己 id 相同的受术者")
    sub("rite/beat_inv.mcfunction",
        "execute as @a[tag=rpg.inv.subject,distance=..7] run function rpg:rite/inv_hud",
        "execute as @a[tag=rpg.inv.subject,distance=..7] if score @s rpg_inv_id = #inv_id rpg_inv_id "
        "run function rpg:rite/inv_hud",
        "逆圣化 HUD 按仪式 id 隔离")

    for rel in ("rite/v1.mcfunction", "rite/v2.mcfunction", "rite/v3.mcfunction",
                "rite/v4.mcfunction", "rite/v5.mcfunction"):
        s = read(rel)
        old = "execute as @a[tag=rpg.inv.subject,distance=..7] "
        new = ("execute as @a[tag=rpg.inv.subject,distance=..7] "
               "if score @s rpg_inv_id = #inv_id rpg_inv_id ")
        out, changed, already = [], 0, 0
        for line in s.split("\n"):
            if line.startswith(new):
                already += 1
            elif line.startswith(old):
                line = line.replace(old, new, 1)
                changed += 1
            out.append(line)
        assert not (changed and already), "%s: 同时存在已改与未改的节拍行" % rel
        assert changed or already, "%s: 找不到逆圣化受术者选择器" % rel
        if changed:
            write(rel, "\n".join(out))
            fixes.append((rel[:-len(".mcfunction")], "节拍伤害按仪式 id 隔离"))

    sub("rite/inv_burst.mcfunction",
        "execute as @a[tag=rpg.inv.subject,distance=..7] run function rpg:rite/inv_grant",
        "execute as @a[tag=rpg.inv.subject,distance=..7] "
        "if score @s rpg_inv_id = #inv_id rpg_inv_id run function rpg:rite/inv_grant",
        "圣痕只授予完成本场仪式的玩家")

    for rel in ("rite/inv_grant.mcfunction", "rite/inv_abort.mcfunction"):
        sub(rel,
            "tag @s remove rpg.inv.subject\nscoreboard players set @s rpg_inv 0",
            "tag @s remove rpg.inv.subject\n"
            "scoreboard players set @s rpg_inv 0\n"
            "scoreboard players reset @s rpg_inv_id",
            "仪式收场时把寿命与归属 id 一并清掉")

    p = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg_inv_id " not in s:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\nscoreboard objectives add rpg_inv_id dummy\n")


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
# 一次性把名单设成整组只能修一半：多个 Boss 并存时，单条
# bossbar 的 value / players / name 仍会被最后遍历的实体轮流覆盖。原版又不支持
# 动态的“一实体一栏” id，所以预分配四个固定槽。每个 Boss 第一次被加载时拿到
# 稳定槽位，并骑一只 marker 作为死亡探针：区块卸载时槽位保持，死亡才释放。
# 四槽都满时新 Boss 暂时记为 0（无栏），每刻按实体遍历顺序重试空槽；这是确定的
# 溢出策略，不会让某一条栏的名称、数值和观众来自不同 Boss。
BOSSBAR_IDS = ("devil", "devil2", "devil3", "devil4")

BOSSBAR_ASSIGN = """\
# @s 是刚拿到第 %(N)d 槽的 Boss。骑乘 marker 是它的死亡探针：
# 区块卸载时两者一起卸载，槽位保留；Boss 死亡时 marker 被甩下，释放槽位。
scoreboard players set @s rpg_boss_slot %(N)d
summon minecraft:marker ~ ~ ~ {Tags:["rpg.bossbar.probe","rpg.bossbar.new"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.bossbar.new,distance=..1,limit=1,sort=nearest] rpg_boss_slot %(N)d
ride @e[type=minecraft:marker,tag=rpg.bossbar.new,distance=..1,limit=1,sort=nearest] mount @s
tag @e[type=minecraft:marker,tag=rpg.bossbar.new,distance=..1] remove rpg.bossbar.new
scoreboard players set #boss_slot%(N)d rpg_boss_slot 1
"""

BOSSBAR_SHOW = """\
# @s 是稳定占有第 %(N)d 槽的 Boss：名称、值与观众来自同一实体。
execute store result bossbar minecraft:%(ID)s value run data get entity @s Health
bossbar set minecraft:%(ID)s players @a[distance=..20]
execute if entity @s[type=minecraft:evoker] run bossbar set minecraft:%(ID)s name {"text":"\\ue301\\ue302\\ue303"}
execute if entity @s[type=minecraft:vindicator,tag=devil2] run bossbar set minecraft:%(ID)s name {"text":"\\ue201\\ue202\\ue203"}
"""

BOSSBAR_PROBE = """\
# 还骑着就说明 Boss 只是活着或连同区块一起回来了；什么都不做。
execute on vehicle run return 0
%(RELEASE)s
kill @s
"""


def bossbar_allocate_text():
    out = ["# 取第一个空槽；四槽满时稳定落到 0，并在后续 tick 重试。"]
    for n in range(1, 5):
        out.append(
            "execute if score #boss_slot%d rpg_boss_slot matches 0 "
            "run return run function rpg:entities/warden/bossbar_assign%d" % (n, n))
    out.append("scoreboard players set @s rpg_boss_slot 0")
    return "\n".join(out) + "\n"


def bossbar_probe_text():
    release = []
    for n in range(1, 5):
        release.append(
            "execute if score @s rpg_boss_slot matches %d "
            "run scoreboard players set #boss_slot%d rpg_boss_slot 0" % (n, n))
    return BOSSBAR_PROBE % {"RELEASE": "\n".join(release)}


def bossbar_tick_text():
    out = [
        "# 先让已脱离死亡 Boss 的探针释放槽位；随区块卸载的探针不会误释放。",
        "execute as @e[type=minecraft:marker,tag=rpg.bossbar.probe] run function rpg:entities/warden/bossbar_probe",
        "",
        "# fake player 在目标未加载时仍保留占用；add 0 只负责首次初始化。",
    ]
    for n in range(1, 5):
        out.append("scoreboard players add #boss_slot%d rpg_boss_slot 0" % n)

    out.extend((
        "",
        "# 没有槽位分数的是新 Boss；0 是四槽已满的溢出 Boss，空槽出现后重试。",
    ))
    selectors = (
        "@e[type=minecraft:evoker,tag=boss]",
        "@e[type=minecraft:vindicator,tag=devil2,tag=boss]",
    )
    for selector in selectors:
        out.append(
            "execute as %s at @s unless score @s rpg_boss_slot = @s rpg_boss_slot "
            "run function rpg:entities/warden/bossbar_allocate" % selector)
    for selector in selectors:
        out.append(
            "execute as %s at @s if score @s rpg_boss_slot matches 0 "
            "run function rpg:entities/warden/bossbar_allocate" % selector)

    out.extend(("", "# 每个槽只由自己的 Boss 写值、名称和附近观众。"))
    for n, bossbar_id in enumerate(BOSSBAR_IDS, 1):
        for selector in selectors:
            out.append(
                "execute as %s,scores={rpg_boss_slot=%d},limit=1] at @s "
                "run function rpg:entities/warden/bossbar_show%d" % (selector[:-1], n, n))
        # 两种实际 Boss 实体都不存在时隐藏该槽；空选择器是赋值为空名单。
        out.append(
            "execute unless entity @e[type=minecraft:evoker,tag=boss,scores={rpg_boss_slot=%d}] "
            "unless entity @e[type=minecraft:vindicator,tag=devil2,tag=boss,scores={rpg_boss_slot=%d}] "
            "run bossbar set minecraft:%s players @a[tag=rpg.bossbar.none]" %
            (n, n, bossbar_id))
    return "\n".join(out) + "\n"


def bossbar_load_text():
    out = ["# 固定四槽：同类 Boss 可在相距很远的四场战斗中各自显示。"]
    for bossbar_id in BOSSBAR_IDS:
        out.extend((
            'bossbar add minecraft:%s {"text":"devil","bold":true}' % bossbar_id,
            "bossbar set minecraft:%s color blue" % bossbar_id,
            "bossbar set minecraft:%s max 1000" % bossbar_id,
            "bossbar set minecraft:%s style notched_6" % bossbar_id,
        ))
    return "\n".join(out) + "\n"


def fix_bossbar():
    for rel in ("entities/warden/action.mcfunction",
                "entities/warden/action2.mcfunction"):
        s = read(rel)
        marker = "# 名称、血量和观众由 warden/bossbar_tick 统一写入，避免多 Boss 互盖。"
        if marker not in s:
            candidates = (
                "execute as @a[distance=..20] at @s run bossbar set minecraft:devil players @s",
                "bossbar set minecraft:devil players @a[distance=..20]",
            )
            found = [old for old in candidates if old in s]
            assert len(found) == 1, "%s: Bossbar 出生写入不是预期形状" % rel
            s = s.replace(found[0], marker)
            fixes.append((rel, "Boss 出生函数不再直接覆盖全局血条观众"))
        out = []
        for line in s.split("\n"):
            if line.startswith("bossbar set minecraft:devil color ") or \
                    line.startswith("bossbar set minecraft:devil name "):
                continue
            out.append(line)
        write(rel, "\n".join(out))

    sub("entities/warden/warden.mcfunction",
        "execute as @e[tag=boss] at @s store result bossbar minecraft:devil value run data get entity @s Health",
        "function rpg:entities/warden/bossbar_tick",
        "四个稳定槽并行追踪 Boss，远处分场玩家也能看到各自血条")
    for n, bossbar_id in enumerate(BOSSBAR_IDS, 1):
        write("entities/warden/bossbar_assign%d.mcfunction" % n,
              BOSSBAR_ASSIGN % {"N": n})
        write("entities/warden/bossbar_show%d.mcfunction" % n,
              BOSSBAR_SHOW % {"N": n, "ID": bossbar_id})
    write("entities/warden/bossbar_allocate.mcfunction", bossbar_allocate_text())
    write("entities/warden/bossbar_probe.mcfunction", bossbar_probe_text())
    write("entities/warden/bossbar_tick.mcfunction", bossbar_tick_text())
    write("command/bossbar.mcfunction", bossbar_load_text())

    p = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg_boss_slot " not in s:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\nscoreboard objectives add rpg_boss_slot dummy\n")


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


# ---------------------------------------------------------------------------
# 9. 玛门的掉落物吸附：不能吸向最近的路人
# ---------------------------------------------------------------------------
# 这个函数是 `execute as @a[pact=7] at @s` 调的，进来时 @s 就是
# 真正的契约者。可一旦 `as @e[type=item] at @s` 之后，@s 换成了
# 掉落物；原来用 `facing entity @p` 把它吸向最近的**任意**玩家。
# 两人靠近时，契约者反而会把东西送到旁观者手里。
#
# 用一个同步调用内生死的施法者标签锁住真正的人；与链锯、
# 路西法和佣兵的归属策略是同一种形状。
def fix_mammon_pull():
    sub("pact/mammon.mcfunction",
        "execute as @e[type=minecraft:item,distance=0.6..6,nbt={PickupDelay:0s}] "
        "at @s facing entity @p feet run tp @s ^ ^ ^0.45",
        "tag @s add rpg.mam.pull\n"
        "execute as @e[type=minecraft:item,distance=0.6..6,nbt={PickupDelay:0s}] "
        "at @s facing entity @a[tag=rpg.mam.pull,limit=1] feet run tp @s ^ ^ ^0.45\n"
        "tag @s remove rpg.mam.pull",
        "玛门吸附锁定真正的契约者，不再吸向最近路人")


# ---------------------------------------------------------------------------
# 10. 主动符石与熔炉热浪：伤害/击退归属不能用 @p 猜
# ---------------------------------------------------------------------------
def lock_sync_caster(rel, held_tag, cast_tag):
    """把进函数时的真实 @s 带过内层 victim 执行上下文。"""
    s = read(rel)
    if ("tag @s add " + cast_tag) in s:
        return
    old = "@p[tag=%s]" % held_tag
    assert old in s, "%s: 找不到要替换的最近持有者 %s" % (rel, old)
    head = ("# 施法者标签只在本次同步调用内存活；内层把 @s 换成受击者后，\n"
            "# 仍能精确找回真正施法者，不会把伤害记给站得更近的同款持有者。\n"
            "tag @s add %s\n" % cast_tag)
    s = head + s.replace(old, "@a[tag=%s,limit=1]" % cast_tag)
    s = s.rstrip("\n") + "\ntag @s remove %s\n" % cast_tag
    write(rel, s)
    fixes.append((rel[:-len(".mcfunction")], "伤害/击退锁定同步调用的真实施法者"))


def fix_active_item_owners():
    # 熔火之锤的三重热浪每一圈都是独立同步调用。
    for n in (1, 2, 3):
        lock_sync_caster("item/epic/forge_ring%d.mcfunction" % n,
                         "rpg.h.forge_tag1", "rpg.forge.cast")
    sub("item/epic/forge_push.mcfunction",
        "@p[tag=rpg.h.forge_tag1]",
        "@a[tag=rpg.forge.cast,limit=1]",
        "热浪击退朝远离真正施法者的方向，不再朝最近持锤者")
    lock_sync_caster("item/rune/quake_burst.mcfunction",
                     "rpg.h.quake_tag1", "rpg.quake.cast")
    lock_sync_caster("item/rune/shade_burst.mcfunction",
                     "rpg.h.shade_tag1", "rpg.shade.cast")
    lock_sync_caster("item/rune/tide_burst.mcfunction",
                     "rpg.h.tide_tag1", "rpg.tide.cast")
    sub("item/rune/tide_burst.mcfunction",
        "damage @s 5 minecraft:freeze",
        "damage @s 5 minecraft:freeze by @a[tag=rpg.tide.cast,limit=1]",
        "潮汐爆发伤害归属真正施法者，不再成为无来源环境伤害")


# ---------------------------------------------------------------------------
# 11. 战利品触发：随机数不借最近玩家的记分板
# ---------------------------------------------------------------------------
# 两类触发都从掉落物实体的上下文同步调用。原实现先把随机数写到 @p，随后每个
# 分支再用 @p 取回；多人挤在一起时这不是“主人”，也没有必要把临时状态寄存在
# 玩家身上。fake player 在一次函数链内写后即读，不跨刻，因此不会串线。
def fix_loot_scratch():
    for rel in ("loot/trigger.mcfunction", "loot/trigger_ominous.mcfunction"):
        s = read(rel)
        old = "execute as @p at @s store result score @s loot run random value 1..100"
        new = "execute store result score #loot loot run random value 1..100"
        if new not in s:
            assert old in s, "%s: 战利品随机入口不是预期形状" % rel
            s = s.replace(old, new, 1)
        s = s.replace("if score @p loot", "if score #loot loot")
        assert not re.search(r"@p(?:\[|\b)", s), \
            "%s: 战利品触发不得借最近玩家保存随机数" % rel
        write(rel, s)


def assert_new_system_guards():
    """新系统的多人不变量。

    这些内容由各自的生成器写出，opt_mp 不负责重写；但既然它是
    构建链里的多人关口，就应该在这里把会导致跨玩家串线的回归拦下。
    """
    arrow = read("mammon/arrow.mcfunction")
    guarded_seen = ("execute if score #mine rpg_mam matches 1 run tag @s add "
                    "rpg.mam.seen")
    assert guarded_seen in arrow, \
        "mammon/arrow: 必须验过 on origin 才能打 seen，否则会吞掉别人的箭"
    assert "\ntag @s add rpg.mam.seen\n" not in arrow, \
        "mammon/arrow: 发现未守卫的 seen，多人射箭会互相抢标记"

    for rel in ("squad/upgrade.mcfunction",
                "squad/handover.mcfunction",
                "squad/fire_near.mcfunction"):
        src = read(rel)
        assert "if score @s rpg_squad = #sq rpg_squad run tag @s add rpg.sq.pick" in src, \
            "%s: 必须先按队伍编号挑候选人，不能先 limit=1 再验归属" % rel
        assert "tag=rpg.sq.pick" in src, \
            "%s: 最终目标必须从本队候选人中取" % rel

    # HEAD 后的系统都有真实的执行者、origin 或队伍编号，不应再用
    # “最近玩家”猜归属。世界事件里有意图的 @p 留给 mp_audit 人工复核；
    # 这些新系统则一处都不应该有。
    roots = ("pact", "mammon", "squad", "taint", "vacant", "hud", "rite", "doll")
    bad = []
    for root in roots:
        base = os.path.join(FUNC, root)
        if not os.path.isdir(base):
            continue
        for dirpath, _dirs, names in os.walk(base):
            for fn in names:
                if not fn.endswith(".mcfunction"):
                    continue
                path = os.path.join(dirpath, fn)
                for i, line in enumerate(io.open(path, encoding="utf-8"), 1):
                    if not line.lstrip().startswith("#") and re.search(r"@p(?:\[|\b)", line):
                        bad.append((os.path.relpath(path, FUNC), i, line.strip()))
    assert not bad, "新系统不得用 @p 猜玩家归属: %r" % (bad[:8],)

    for rel in tuple("item/epic/forge_ring%d.mcfunction" % n for n in (1, 2, 3)) + (
            "item/epic/forge_push.mcfunction",
            "item/rune/quake_burst.mcfunction",
            "item/rune/shade_burst.mcfunction",
            "item/rune/tide_burst.mcfunction"):
        assert not re.search(r"@p(?:\[|\b)", read(rel)), \
            "%s: 主动物品内层不得用 @p 猜施法者" % rel
    assert "damage @s 5 minecraft:freeze by @a[tag=rpg.tide.cast,limit=1]" in \
           read("item/rune/tide_burst.mcfunction"), \
        "潮汐爆发必须把伤害归属同步调用内的真实施法者"

    assert "rpg_inv_id = #inv_id rpg_inv_id" in read("rite/beat_inv.mcfunction"), \
        "逆圣化逐刻结算必须同时验仪式 id"
    assert "tag=rpg.inv.subject,distance=..48" not in read("rite/inv_fail.mcfunction"), \
        "逆圣化不得再用大半径猜仪式归属"

    warden = read("entities/warden/warden.mcfunction")
    assert "function rpg:entities/warden/bossbar_tick" in warden, \
        "Bossbar 必须由四槽跟踪器统一写入"
    tick = read("entities/warden/bossbar_tick.mcfunction")
    assert "rpg:entities/warden/bossbar_probe" in tick and \
           "rpg:entities/warden/bossbar_allocate" in tick, \
        "Bossbar 四槽必须逐刻释放死亡槽并给新/溢出 Boss 分配空槽"
    for n, bossbar_id in enumerate(BOSSBAR_IDS, 1):
        show = read("entities/warden/bossbar_show%d.mcfunction" % n)
        assert "bossbar minecraft:%s value" % bossbar_id in show and \
               "bossbar set minecraft:%s players @a[distance=..20]" % bossbar_id in show, \
            "Bossbar 槽 %d 的值与观众必须在同一 Boss 上写入" % n
        assert "#boss_slot%d rpg_boss_slot" % n in tick, \
            "Bossbar tick 必须维护第 %d 槽的持久占用" % n
    load = read("command/bossbar.mcfunction")
    for bossbar_id in BOSSBAR_IDS:
        assert "bossbar add minecraft:%s " % bossbar_id in load, \
            "全新存档必须创建 Bossbar minecraft:%s" % bossbar_id

    for rel in ("loot/trigger.mcfunction", "loot/trigger_ominous.mcfunction"):
        src = read(rel)
        assert "score #loot loot" in src and not re.search(r"@p(?:\[|\b)", src), \
            "%s: 同步随机 scratch 必须用 #loot，不能借最近玩家" % rel


def main():
    fix_damage_scan()
    fix_samael()
    fix_inversion()
    fix_inversion_owned()
    fix_saw()
    fix_chime()
    fix_bossbar()
    fix_bossbar_load()
    fix_bare_walks()
    fix_mammon_pull()
    fix_active_item_owners()
    fix_loot_scratch()
    assert_new_system_guards()
    print("multiplayer: %d fixes" % len(fixes))
    for rel, why in fixes:
        print("  %-30s %s" % (rel, why))


if __name__ == "__main__":
    main()
