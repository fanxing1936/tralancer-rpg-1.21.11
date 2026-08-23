# -*- coding: utf-8 -*-
"""佣兵小队：花钱雇人，给他们配刀，指着谁打谁。

一个独立分支，不与罪器／契约／驱魔任何一条耦合。

## 为什么是"手动驾驶"的尸壳

要用尸壳的模型就得用尸壳这个实体，而尸壳是**敌对生物** —— 它自带
`NearestAttackableTargetGoal`，会主动打玩家和村民。原版命令**没有任何办法
清除一个生物的当前目标**（`Target` 不在可写 NBT 里，`AngryAt` 只对中立生物
有效），所以"让它别打老板"这件事没法在事后补救。

唯一能从根上断掉的地方是**索敌半径**：

    attributes:[{id:"follow_range",base:0}]

实测（无头 1.21.11）：对照组普通生物当场砍死了村民，而 `follow_range: 0`
的那只放着不管，村民满血 20.0f。它永远不会自己选中任何东西 ——
**因此也永远不可能误伤雇主**，这条安全性是结构性的，不靠判定去兜。

代价是它也不会自己打该打的人。于是移动与攻击全部由数据包驱动：

* `movement_speed: 0` —— 让它自己的 AI 推不动它，省得和我们的位移打架
  （`NoAI` 不行：那样连重力都没了，人会浮在空中）
* 位移用 `tp`，客户端的走路动画是按位置变化算的，所以看起来仍然在走
* 攻击用 `damage ... by @s`，伤害值从它**自己的 attack_damage 属性**读，
  而这个属性是含手持武器的（实测：空手 5.0，拿下界合金剑 12.0，
  换装后一两刻生效）—— 所以"给佣兵配武器"不需要任何武器数值表，
  你塞什么进去它就按什么打，包括本包所有自定义武器

尸壳比卫道士省一件事：它**不怕阳光**，白天不会自燃。但也多带来两件：

* 它属于 `#minecraft:zombies`，会被本包的"新生僵尸重新配装"流水线抓走 ——
  已在 `zombie_batch` 里按标签排除
* 它泡在水里会转化成普通僵尸，而转化是**换一个实体**，标签与记分板一起没了 ——
  所以佣兵不下水，踩到水就召回

## 多人

从第一行就按多人写：

* 每个雇主有一个 `rpg_squad` 编号，队员携带同一个编号。认人靠编号比对，
  不靠"最近的玩家"
* 每刻只有一条玩家作用域判定（`@a[tag=rpg.sq.lead]`）；真正的遍历发生在
  雇主自己的函数里，且限距
* 雇主在自己那一段里临时挂 `rpg.sq.boss`，队员据此找人 —— 命令执行是
  单线程的，同一刻只可能有一个玩家挂着它，所以 `limit=1` 是精确的
  （与罪器、契约用的是同一条不变量）
"""

import io
import json
import os
import sys

import add_exorcism as ex

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement/item")
PRED = os.path.join(DP, "data/rpg/predicate")
GIVE = os.path.join(FUNC, "command/give/extra.mcfunction")
ITEM = os.path.join(FUNC, "command/give/item.mcfunction")

CAP = 4                  # 小队上限
COST = 8                 # 第 n 名的价钱 = COST * n
LOCK = 10                # 触发去抖（刻）
SWING = 13               # 攻击间隔（刻）—— 生物受伤后约 10 刻无敌帧
REACH = "3.4"            # 够得着的距离
STRIDE = "0.22"          # 每刻迈出多远（别叫 STEP：下面有个同名模板）
LEASH = 34               # 掉队多远直接归队
SIGHT = 24               # 指挥旗的射线长度

CUR = 'minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}]'

OBJECTIVES = ["rpg_squad", "rpg_sq_mode", "rpg_sq_cd", "rpg_sq_t",
              "rpg_sq_n", "rpg_sq_have", "rpg_sq_aim", "rpg_sq_stance"]

RULE = ex.RULE
seg, row, wf, wj = ex.seg, ex.row, ex.wf, ex.wj

GOLD = "#D4AF37"
STEEL = "#8FA1B3"


# ---------------------------------------------------------------------------
# 队员本体
# ---------------------------------------------------------------------------
def member_nbt():
    """一名佣兵。

    follow_range 0 是这套体系的安全底座 —— 它永远不会自己选中任何目标，
    所以永远不可能误伤雇主。movement_speed 0 让它自己的 AI 推不动它。
    drop_chances.mainhand 拉满：人没了，武器还你。
    """
    return (
        '{Tags:["rpg.squad","rpg.sq.new"],'
        'IsBaby:0b,'
        'PersistenceRequired:1b,'
        'CustomNameVisible:1b,'
        'CustomName:[{"text":"佣兵","color":"%s"}],'
        'Health:40f,'
        'attributes:['
        '{id:"max_health",base:40f},'
        # 写死攻击力：僵尸类的基础攻击随难度浮动（简单 2.5 / 普通 3 /
        # 困难 4.5），佣兵的强度不该跟着世界难度飘。武器加成照常叠在上面。
        '{id:"attack_damage",base:4f},'
        '{id:"armor",base:4f},'
        '{id:"follow_range",base:0f},'
        '{id:"movement_speed",base:0f},'
        '{id:"knockback_resistance",base:0.3f}],'
        'drop_chances:{mainhand:1f}}' % STEEL)


# ---------------------------------------------------------------------------
# 每刻
# ---------------------------------------------------------------------------
ROOT = """\
# 佣兵小队每刻入口。
# 只有一条玩家作用域判定；真正的遍历在雇主自己那一段里，而且限距。
execute as @a[tag=rpg.sq.lead] at @s run function rpg:squad/lead
execute as @a[scores={rpg_sq_t=1..}] run scoreboard players remove @s rpg_sq_t 1
"""

LEAD = """\
# 以雇主的身份跑一遍自己的队伍。
#
# 临时挂 rpg.sq.boss：命令执行是单线程的，同一刻只可能有一个玩家挂着它，
# 所以队员那边的 @a[tag=rpg.sq.boss,limit=1] 是**精确的**，
# 而不是"碰巧最近的那个玩家"。多人下这一点是全部归属逻辑的地基。
tag @s add rpg.sq.boss
scoreboard players operation #sq rpg_squad = @s rpg_squad

# 本队当前的攻击目标，标出来给队员用（同样只在这一段里存活）
scoreboard players set #mark rpg_squad 0
execute as @e[tag=rpg.sq.aim,distance=..64] if score @s rpg_sq_aim = #sq rpg_squad run function rpg:squad/set_mark

# 搜索半径必须**大于**归队距离：否则掉出 LEASH 的人连这一层都进不来，
# 那条"太远就拉回来"永远轮不到他 —— 人就永久丢了。
execute as @e[type=minecraft:husk,tag=rpg.squad,distance=..128] if score @s rpg_squad = #sq rpg_squad at @s run function rpg:squad/member

tag @e[tag=rpg.sq.mark] remove rpg.sq.mark
tag @s remove rpg.sq.boss
"""

MEMBER = """\
# 一名队员的一刻。@s 是队员，执行位置在它自己脚下。
execute if entity @s[scores={rpg_sq_cd=1..}] run scoreboard players remove @s rpg_sq_cd 1
execute if entity @s[scores={rpg_sq_mode=2}] run function rpg:squad/engage
execute if entity @s[scores={rpg_sq_mode=0}] run function rpg:squad/follow
# 姿态 1 是驻守：站着不动，什么都不做
"""

FOLLOW = """\
# 跟随。近了就站着，远了就走过去，掉队太远直接归队。
# 踩进水里也直接召回：尸壳泡水会转化成普通僵尸，而转化是**换一个实体** ——
# 标签和记分板一起没了，队员就这么凭空消失。所以佣兵不下水。
execute if block ~ ~ ~ water unless entity @a[tag=rpg.sq.boss,distance=..3] run tp @s @a[tag=rpg.sq.boss,limit=1]
execute if entity @a[tag=rpg.sq.boss,distance=%(LEASH)d..] run tp @s @a[tag=rpg.sq.boss,limit=1]
execute if entity @a[tag=rpg.sq.boss,distance=3..] run function rpg:squad/walk_boss
"""

WALK_BOSS = """\
# 朝雇主走一步。
tp @s ~ ~ ~ facing entity @a[tag=rpg.sq.boss,limit=1]
execute at @s run function rpg:squad/step
"""

WALK_AIM = """\
# 朝目标走一步。
tp @s ~ ~ ~ facing entity @e[tag=rpg.sq.mark,limit=1,sort=nearest,distance=..128]
execute at @s run function rpg:squad/step
"""

STEP = """\
# 迈一步。`rotated ~ 0` 把俯仰归零 —— 不然朝着高处的目标会走上天。
#
# 位移用 tp 而不是 Motion：Motion 要先把朝向换算成 xz 分量，而 tp 沿
# `^ ^ ^` 走一步不需要任何三角函数。客户端的走路动画是按位置变化算的，
# 所以 tp 出来的佣兵看起来仍然在走路。
execute rotated ~ 0 positioned ^ ^ ^%(STRIDE)s unless block ~ ~ ~ #minecraft:replaceable if block ~ ~1 ~ #minecraft:replaceable positioned ~ ~1 ~ run tp @s ~ ~ ~
execute rotated ~ 0 positioned ^ ^ ^%(STRIDE)s if block ~ ~ ~ #minecraft:replaceable run tp @s ~ ~ ~
"""

ENGAGE = """\
# 交战。目标没了就归队，够得着就砍，够不着就压上去。
execute unless score #mark rpg_squad matches 1 run function rpg:squad/stand_down
execute if entity @e[tag=rpg.sq.mark,distance=%(REACH)s..128] run function rpg:squad/walk_aim
execute if entity @e[tag=rpg.sq.mark,distance=..%(REACH)s] if entity @s[scores={rpg_sq_cd=..0}] run function rpg:squad/strike
"""

STRIKE = """\
# 一次挥砍。伤害读的是队员**自己的 attack_damage 属性** ——
# 那个值天然含手持武器（空手 5，拿下界合金剑 12），所以配什么武器就按什么打，
# 不需要任何武器数值表，本包所有自定义武器也一并适用。
#
# damage 的数值不能直接吃记分板，所以走宏：把属性存进 storage 再展开。
scoreboard players set @s rpg_sq_cd %(SWING)d
tag @s add rpg.sq.striker
execute store result storage rpg:squad atk int 1 run attribute @s minecraft:attack_damage get
function rpg:squad/strike_do with storage rpg:squad
tag @s remove rpg.sq.striker
particle sweep_attack ~ ~1 ~ 0.2 0.2 0.2 0 1
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..16] ~ ~ ~ 0.7 1.1
playsound minecraft:entity.husk.ambient hostile @a[distance=..16] ~ ~ ~ 0.5 0.8
"""

STRIKE_DO = """\
# 宏展开的那一行。$(atk) 是上一步读到的攻击力。
$execute as @e[tag=rpg.sq.mark,limit=1,sort=nearest,distance=..%(REACH)s] run damage @s $(atk) minecraft:mob_attack by @e[tag=rpg.sq.striker,limit=1]
"""

SET_MARK = """\
# 本队的攻击目标。旗子给队员用 —— 一支队伍最多只有一个目标，
# 所以这件事在雇主这一层问一次就够，不必每个队员各开一次全表走查。
tag @s add rpg.sq.mark
scoreboard players set #mark rpg_squad 1
"""


STAND_DOWN = """\
# 目标没了。回到跟随。
scoreboard players set @s rpg_sq_mode 0
particle happy_villager ~ ~1.6 ~ 0.2 0.2 0.2 0 4
"""


# ---------------------------------------------------------------------------
# 募兵
# ---------------------------------------------------------------------------
HIRE = """\
# 募兵旗 —— 由 rpg:item/squad_hire 在长按右键时触发。
advancement revoke @s only rpg:item/squad_hire
execute if entity @s[scores={rpg_sq_t=1..}] run return 0
scoreboard players set @s rpg_sq_t %(LOCK)d

# 头一次募兵先领一个队伍编号。多人下认人全靠它，不靠"最近的玩家"。
execute unless score @s rpg_squad = @s rpg_squad run function rpg:squad/enroll

# 数一数现有几个人
scoreboard players operation #sq rpg_squad = @s rpg_squad
scoreboard players set #cnt rpg_squad 0
execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players add #cnt rpg_squad 1
scoreboard players operation @s rpg_sq_n = #cnt rpg_squad
execute if entity @s[scores={rpg_sq_n=%(CAP)d..}] run return run function rpg:squad/full

# 手上有多少钱。`clear ... 0` 是**只数不拿**，原版惯用写法。
execute store result score @s rpg_sq_have run clear @s %(CUR)s 0
%(BRANCH)s
"""

ENROLL = """\
scoreboard players add #sq_seq rpg_squad 1
scoreboard players operation @s rpg_squad = #sq_seq rpg_squad
scoreboard players set @s rpg_sq_stance 0
tag @s add rpg.sq.lead
"""

HIRE_N = """\
# 第 %(N)d 名，价钱 %(PRICE)d 枚。
execute if entity @s[scores={rpg_sq_have=..%(SHORT)d}] run return run function rpg:squad/poor
clear @s %(CUR)s %(PRICE)d
function rpg:squad/spawn
"""

POOR = """\
title @s actionbar ["",{"text":"钱不够","italic":true,"color":"red"}]
playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 0.9
"""

FULL = """\
title @s actionbar ["",{"text":"小队已满员","italic":true,"color":"gray"}]
playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 1.2
"""

SPAWN = """\
# 在雇主身前两格把人召出来。
execute at @s anchored eyes positioned ^ ^ ^2 run function rpg:squad/spawn_at
scoreboard players add @s rpg_sq_n 1
title @s actionbar ["",{"text":"佣兵已入队","color":"%(GOLD)s"}]
playsound minecraft:entity.villager.yes player @s ~ ~ ~ 1 1
playsound minecraft:block.anvil_use player @a[distance=..12] ~ ~ ~ 0.6 1.4
"""

SPAWN_AT = """\
summon minecraft:husk ~ ~ ~ %(NBT)s
execute as @e[type=minecraft:husk,tag=rpg.sq.new] run scoreboard players operation @s rpg_squad = #sq rpg_squad
execute as @e[type=minecraft:husk,tag=rpg.sq.new] run scoreboard players set @s rpg_sq_mode 0
execute as @e[type=minecraft:husk,tag=rpg.sq.new] run scoreboard players set @s rpg_sq_cd 0
tag @e[type=minecraft:husk,tag=rpg.sq.new] remove rpg.sq.new
particle happy_villager ~ ~1 ~ 0.4 0.6 0.4 0.05 30
particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.02 16
"""


# ---------------------------------------------------------------------------
# 指挥
# ---------------------------------------------------------------------------
ORDER = """\
# 指挥旗 —— 由 rpg:item/squad_order 在长按右键时触发。
# 不潜行：指着谁打谁。潜行：切换 跟随／驻守。
advancement revoke @s only rpg:item/squad_order
execute if entity @s[scores={rpg_sq_t=1..}] run return 0
scoreboard players set @s rpg_sq_t %(LOCK)d
execute unless score @s rpg_squad = @s rpg_squad run return run function rpg:squad/no_squad
scoreboard players operation #sq rpg_squad = @s rpg_squad
execute if predicate rpg:sneaking run return run function rpg:squad/stance
function rpg:squad/aim
"""

NO_SQUAD = """\
title @s actionbar ["",{"text":"你还没有小队","italic":true,"color":"gray"}]
playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 1.2
"""

STANCE = """\
# 跟随 ⇄ 驻守。
#
# 注意中间那个 9：直接写"0 改 1、1 改 0"两行，第一行改完第二行立刻看到 1
# 又给改回 0 —— 翻不过来。先把 1 挪到一个两条判定都碰不到的值上。
execute if entity @s[scores={rpg_sq_stance=1}] run scoreboard players set @s rpg_sq_stance 9
execute if entity @s[scores={rpg_sq_stance=0}] run scoreboard players set @s rpg_sq_stance 1
execute if entity @s[scores={rpg_sq_stance=9}] run scoreboard players set @s rpg_sq_stance 0

execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players operation @s rpg_sq_mode = #sq_stance rpg_squad
execute if entity @s[scores={rpg_sq_stance=0}] run function rpg:squad/say_follow
execute if entity @s[scores={rpg_sq_stance=1}] run function rpg:squad/say_hold
"""

SAY_FOLLOW = """\
scoreboard players set #sq_stance rpg_squad 0
execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players set @s rpg_sq_mode 0
title @s actionbar ["",{"text":"跟　随","color":"%(GOLD)s","bold":true}]
playsound minecraft:entity.villager.yes player @s ~ ~ ~ 1 1.3
"""

SAY_HOLD = """\
scoreboard players set #sq_stance rpg_squad 1
execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players set @s rpg_sq_mode 1
title @s actionbar ["",{"text":"驻　守","color":"%(STEEL)s","bold":true}]
playsound minecraft:block.anvil_land player @s ~ ~ ~ 0.5 1.6
"""

AIM = """\
# 指着谁打谁。先把上一个目标摘掉，再沿视线找第一个挡路的东西。
execute as @e[tag=rpg.sq.aim] if score @s rpg_sq_aim = #sq rpg_squad run function rpg:squad/unaim
execute at @s anchored eyes run function rpg:squad/ray
"""

UNAIM = """\
tag @s remove rpg.sq.aim
scoreboard players reset @s rpg_sq_aim
"""

RAY = """\
# 视线上的 %(SIGHT)d 段。`positioned ^ ^ ^N` 取点，命中即 return，不用递归。
%(STEPS)s
function rpg:squad/miss
"""

RAY_STEP = ("execute positioned ^ ^ ^%(D)d unless block ~ ~ ~ #minecraft:replaceable "
            "run return run function rpg:squad/miss\n"
            "execute positioned ^ ^ ^%(D)d if entity @e[distance=..1.3,"
            "type=!player,type=!minecraft:item,type=!minecraft:experience_orb,"
            "type=!minecraft:item_display,tag=!rpg.squad,limit=1] "
            "run return run function rpg:squad/mark")

MARK = """\
# 找到了。标记目标，全队转入交战。
execute as @e[distance=..1.3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display,tag=!rpg.squad,limit=1,sort=nearest] run function rpg:squad/mark_one
execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players set @s rpg_sq_mode 2
particle crit ~ ~ ~ 0.3 0.3 0.3 0.2 20
playsound minecraft:entity.husk.ambient hostile @a[distance=..20] ~ ~ ~ 1 0.7
"""

MARK_ONE = """\
tag @s add rpg.sq.aim
scoreboard players operation @s rpg_sq_aim = #sq rpg_squad
effect give @s minecraft:glowing 15 0 true
particle angry_villager ~ ~1.4 ~ 0.3 0.3 0.3 0 8
"""

MISS = """\
title @s actionbar ["",{"text":"视线里没有目标","italic":true,"color":"gray"}]
playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.7 1.4
"""


# ---------------------------------------------------------------------------
# 配装与解雇
# ---------------------------------------------------------------------------
EQUIP = """\
# 右键佣兵 —— 由 rpg:item/squad_equip 触发。
# 空手：把他手里那件收回来。拿着东西：换上去。潜行：解雇。
#
# 进度触发器不会告诉我们点的是哪一个，所以取身边最近的自己人 ——
# 你得贴着他才点得到，这个近似是安全的。
advancement revoke @s only rpg:item/squad_equip
execute if entity @s[scores={rpg_sq_t=1..}] run return 0
scoreboard players set @s rpg_sq_t %(LOCK)d
scoreboard players operation #sq rpg_squad = @s rpg_squad
tag @s add rpg.sq.boss
execute as @e[type=minecraft:husk,tag=rpg.squad,distance=..6,limit=1,sort=nearest] if score @s rpg_squad = #sq rpg_squad run function rpg:squad/on_member
tag @s remove rpg.sq.boss
"""

ON_MEMBER = """\
# @s 是被点的佣兵，rpg.sq.boss 是点他的人。
execute if predicate rpg:sneaking_boss run return run function rpg:squad/dismiss
# 先把他原本拿的东西掉出来（有的话），再换上雇主手里那件
execute unless items entity @s weapon.mainhand *[] run return run function rpg:squad/take_weapon
function rpg:squad/drop_weapon
function rpg:squad/take_weapon
"""

TAKE_WEAPON = """\
# 把雇主手里那件塞给他，然后清空雇主的手。
execute unless items entity @a[tag=rpg.sq.boss,limit=1] weapon.mainhand *[] run return 0
item replace entity @s weapon.mainhand from entity @a[tag=rpg.sq.boss,limit=1] weapon.mainhand
item replace entity @a[tag=rpg.sq.boss,limit=1] weapon.mainhand with air
particle enchant ~ ~1.4 ~ 0.3 0.4 0.3 0.6 24
playsound minecraft:item.armor.equip_iron player @a[distance=..12] ~ ~ ~ 1 1.1
title @a[tag=rpg.sq.boss,limit=1] actionbar ["",{"text":"已配装","color":"%(GOLD)s"}]
"""

DROP_WEAPON = """\
# 原版没有"让实体丢下手里那件"的命令，所以先召一个占位掉落物，
# 再把他的装备整份写进去。
execute at @s run summon minecraft:item ~ ~1 ~ {Tags:["rpg.sq.drop"],Item:{id:"minecraft:stone",count:1}}
data modify entity @e[type=minecraft:item,tag=rpg.sq.drop,limit=1,sort=nearest] Item set from entity @s equipment.mainhand
tag @e[type=minecraft:item,tag=rpg.sq.drop] remove rpg.sq.drop
item replace entity @s weapon.mainhand with air
"""

DISMISS = """\
# 解雇。装备掉在地上，人散了，退回一半雇金。
execute if items entity @s weapon.mainhand *[] run function rpg:squad/drop_weapon
execute at @s run particle poof ~ ~1 ~ 0.4 0.6 0.4 0.05 40
execute at @s run playsound minecraft:entity.husk.death hostile @a[distance=..16] ~ ~ ~ 0.7 1.2
execute at @s run loot spawn ~ ~1 ~ loot rpg:squad/refund
title @a[tag=rpg.sq.boss,limit=1] actionbar ["",{"text":"已解雇","italic":true,"color":"gray"}]
kill @s
"""


def build_functions():
    wf("squad/squad.mcfunction", ROOT)
    wf("squad/lead.mcfunction", LEAD % {"LEASH": LEASH})
    wf("squad/member.mcfunction", MEMBER)
    wf("squad/follow.mcfunction", FOLLOW % {"LEASH": LEASH})
    wf("squad/walk_boss.mcfunction", WALK_BOSS)
    wf("squad/walk_aim.mcfunction", WALK_AIM)
    wf("squad/step.mcfunction", STEP % {"STRIDE": STRIDE})
    wf("squad/engage.mcfunction", ENGAGE % {"REACH": REACH})
    wf("squad/strike.mcfunction", STRIKE % {"SWING": SWING})
    wf("squad/strike_do.mcfunction", STRIKE_DO % {"REACH": REACH})
    wf("squad/set_mark.mcfunction", SET_MARK)
    wf("squad/stand_down.mcfunction", STAND_DOWN)

    branch = []
    for n in range(CAP):
        price = COST * (n + 1)
        branch.append("execute if entity @s[scores={rpg_sq_n=%d}] "
                      "run function rpg:squad/hire%d" % (n, n))
        wf("squad/hire%d.mcfunction" % n,
           HIRE_N % {"N": n + 1, "PRICE": price, "SHORT": price - 1, "CUR": CUR})
    wf("squad/hire.mcfunction",
       HIRE % {"LOCK": LOCK, "CAP": CAP, "CUR": CUR, "BRANCH": "\n".join(branch)})
    wf("squad/enroll.mcfunction", ENROLL)
    wf("squad/poor.mcfunction", POOR)
    wf("squad/full.mcfunction", FULL)
    wf("squad/spawn.mcfunction", SPAWN % {"GOLD": GOLD})
    wf("squad/spawn_at.mcfunction", SPAWN_AT % {"NBT": member_nbt()})

    wf("squad/order.mcfunction", ORDER % {"LOCK": LOCK})
    wf("squad/no_squad.mcfunction", NO_SQUAD)
    wf("squad/stance.mcfunction", STANCE)
    wf("squad/say_follow.mcfunction", SAY_FOLLOW % {"GOLD": GOLD})
    wf("squad/say_hold.mcfunction", SAY_HOLD % {"STEEL": STEEL})
    wf("squad/aim.mcfunction", AIM)
    wf("squad/unaim.mcfunction", UNAIM)
    steps = "\n".join(RAY_STEP % {"D": d} for d in range(1, SIGHT + 1))
    wf("squad/ray.mcfunction", RAY % {"SIGHT": SIGHT, "STEPS": steps})
    wf("squad/mark.mcfunction", MARK)
    wf("squad/mark_one.mcfunction", MARK_ONE)
    wf("squad/miss.mcfunction", MISS)

    wf("squad/equip.mcfunction", EQUIP % {"LOCK": LOCK})
    wf("squad/on_member.mcfunction", ON_MEMBER)
    wf("squad/take_weapon.mcfunction", TAKE_WEAPON % {"GOLD": GOLD})
    wf("squad/drop_weapon.mcfunction", DROP_WEAPON)
    wf("squad/dismiss.mcfunction", DISMISS)

    # 潜行判定。指挥旗那次问的是玩家自己，配装那次问的是身上挂着 boss 标签的人。
    wj(os.path.join(PRED, "sneaking.json"),
       {"condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"flags": {"is_sneaking": True}}})
    wj(os.path.join(PRED, "sneaking_boss.json"),
       {"condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"type": "minecraft:player", "flags": {"is_sneaking": True}}})

    for name, data, fn in (
            ("squad_hire", "{squad_hire:1b}", "rpg:squad/hire"),
            ("squad_order", "{squad_order:1b}", "rpg:squad/order")):
        wj(os.path.join(ADV, name + ".json"), {
            "criteria": {"requirement": {
                "trigger": "minecraft:using_item",
                "conditions": {"item": {"predicates": {
                    "minecraft:custom_data": data}}}}},
            "rewards": {"function": fn}})

    wj(os.path.join(ADV, "squad_equip.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:player_interacted_with_entity",
            "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this",
                 "predicate": {"type": "minecraft:husk",
                               "nbt": "{Tags:[\"rpg.squad\"]}"}}]}}},
        "rewards": {"function": "rpg:squad/equip"}})

    # 解雇退款：一半雇金，按最便宜的一档算
    wj(os.path.join(DP, "data/rpg/loot_table/squad/refund.json"), {
        "type": "minecraft:generic",
        "pools": [{"rolls": 1, "entries": [
            {"type": "minecraft:item", "name": "minecraft:raw_gold",
             "functions": [
                 {"function": "minecraft:set_count",
                  "count": COST // 2},
                 {"function": "minecraft:set_components",
                  "components": {"minecraft:custom_data": {"currency_tag": True}}}]}]}]})

    tick = os.path.join(FUNC, "command/tick.mcfunction")
    s = io.open(tick, encoding="utf-8").read()
    if "rpg:squad/squad" not in s:
        s = s.replace("function rpg:exorcism",
                      "function rpg:exorcism\nfunction rpg:squad/squad")
        io.open(tick, "w", encoding="utf-8", newline="\n").write(s)


def guard_spawn_batch():
    """把佣兵从"新生僵尸重新配装"那条流水线上摘出去。

    尸壳属于 `#minecraft:zombies`，而 `command/spawn/zombie_batch` 每刻会给
    新出生的僵尸类重掷全套战利品装备，还有几率直接替换成强化变种。
    不排除的话，刚雇来的人转头就被系统当野怪处理掉了。
    """
    p = os.path.join(FUNC, "command/spawn/zombie_batch.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg.squad" in s:
        return 0
    old = "tag @e[type=#minecraft:zombies,tag=!zombie,limit=4] add rpg.spawn.new"
    assert old in s, "zombie_batch 不是预期的形状"
    new = ("# tag=!rpg.squad：佣兵也是尸壳，但他们是雇来的，不该被当作\n"
           "# 新出生的野怪重掷装备、更不该被替换成强化变种。\n"
           "tag @e[type=#minecraft:zombies,tag=!zombie,tag=!rpg.squad,limit=4] "
           "add rpg.spawn.new")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
    return 1


def consumable(seconds):
    return ("food={nutrition:0,saturation:0f,can_always_eat:1b},"
            "consumable={consume_seconds:%df,animation:\"block\","
            "sound:\"minecraft:item.armor.equip_chain\","
            "has_consume_particles:false,on_consume_effects:[]}," % seconds)


def build_give():
    """两面旗：一面招人，一面指挥。"""
    s = io.open(GIVE, encoding="utf-8").read()
    if "募兵旗" in s:
        return 0
    hire = ("give @a white_banner["
            "custom_name=" + row(seg("[佣兵]", GOLD, True), seg("募兵旗", "white")) + ","
            "lore=[" + ",".join([
                RULE,
                row(seg("插在哪里，", "gray"), seg("哪里就是营地", GOLD)),
                row(seg("长按右键雇一名佣兵", "gray")),
                RULE,
                row(seg("⚔募兵", "white", True), seg("　上限 %d 人" % CAP, STEEL)),
                row(seg("　价钱逐人递增：%s 枚货币"
                        % " / ".join(str(COST * (i + 1)) for i in range(CAP)), "gray")),
                row(seg("　佣兵永不主动出手，也永远不会误伤你", "gray")),
                RULE]) + "],"
            "banner_patterns=[{pattern:\"minecraft:border\",color:\"gray\"},"
            "{pattern:\"minecraft:cross\",color:\"red\"}],"
            + consumable(100130) +
            "max_stack_size=1,custom_data={squad_hire:1b}]")
    order = ("give @a red_banner["
             "custom_name=" + row(seg("[佣兵]", GOLD, True), seg("指挥旗", "white")) + ","
             "lore=[" + ",".join([
                 RULE,
                 row(seg("举起它，队伍就看你的手势", "gray")),
                 RULE,
                 row(seg("⚔指挥", "white", True), seg("　长按右键", STEEL)),
                 row(seg("　指着谁打谁：全队压上，目标倒下即归队", "gray")),
                 row(seg("⚔姿态", "white", True), seg("　潜行 + 长按右键", STEEL)),
                 row(seg("　跟随 ⇄ 驻守", "gray")),
                 RULE,
                 row(seg("右键佣兵可为其配装；空手右键取回武器", "gray")),
                 row(seg("潜行右键佣兵可将其解雇", "gray")),
                 RULE]) + "],"
             "banner_patterns=[{pattern:\"minecraft:border\",color:\"black\"},"
             "{pattern:\"minecraft:straight_cross\",color:\"white\"}],"
             + consumable(100131) +
             "max_stack_size=1,custom_data={squad_order:1b}]")
    io.open(GIVE, "w", encoding="utf-8", newline="\n").write(
        s.rstrip("\n") + "\n\n##佣兵小队\n" + hire + "\n" + order + "\n")
    return 2


def tag_currency():
    """给既有的［货币］补一个 custom_data 标记。

    雇佣要精确扣费，而这件物品原本只靠名字区分 —— 名字匹配既脆又慢。
    """
    s = io.open(ITEM, encoding="utf-8").read()
    if "currency_tag" in s:
        return 0
    out = []
    n = 0
    for line in s.split("\n"):
        if '"[currency]"' in line and "raw_gold" in line and "custom_data" not in line:
            line = line.rstrip()
            assert line.endswith("]"), "货币那一行的结尾不是预期的形状"
            line = line[:-1] + ",custom_data={currency_tag:1b}]"
            n += 1
        out.append(line)
    io.open(ITEM, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return n


def add_objectives():
    p = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    add = [o for o in OBJECTIVES if o not in s]
    if add:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n"
            + "\n".join("scoreboard objectives add %s dummy" % o for o in add) + "\n")
    return add


def main():
    obj = add_objectives()
    build_functions()
    gave = build_give()
    cur = tag_currency()
    batch = guard_spawn_batch()
    print("squad: cap %d (husk), give +%d, currency tagged %d, spawn-batch guarded %d"
          % (CAP, gave, cur, batch))
    print("squad: objectives %s" % (obj or "-"))


if __name__ == "__main__":
    main()
