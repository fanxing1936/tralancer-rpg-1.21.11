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
SIGHT = 24               # 指挥旗的射程（格）
RAY_STEP_LEN = 0.5       # 射线的取点间隔。1 格太疏，小生物会从两点之间漏过去

# 命中半径随距离张开 —— 人的瞄准误差是角度上的，不是距离上的。
# 近处收紧（不误抓脚边的东西），远处放宽。24 格处约 1.6 格，合 3.8 度。
RAY_R0 = 0.5             # 起步半径
RAY_RK = 0.045           # 每格张开多少
MARK_R = "2.0"           # 认准那一下用的半径。到得了这里说明锥内已经有东西，
                         # 这里只是从同一个点上挑最近的，宽一点无妨

# 队形。按入队编号分开：停多远，以及从哪个方向靠过来。
# 四个人都 facing 雇主照直走的话，会停在同一个点上挤成一团。
SLOT_DIST = [2.6, 3.4, 4.2, 5.0]
SLOT_YAW = [0, 28, -28, 56]

# 指挥旗能指谁。射线与标记两处共用这一份 —— 分开写迟早改漏一处。
#
# 类型走 rpg:sq_ignore 标签（见 build_ignore_tag）；剩下三条是自己人：
# rpg.merc 在编与待雇都带，rpg.sq.board 是骑在佣兵头上的那块信息板 ——
# 不挡掉的话，往队友那边一指，标中的就是自家名牌。
TARGET = ("type=!#rpg:sq_ignore,"
          "tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll")

# 不该被指挥旗当成敌人的实体类型。一律 required:false ——
# 原版哪天改名或删掉某一个，整张标签也不会因此加载失败。
IGNORE_TYPES = [
    "#minecraft:impact_projectiles", "#minecraft:boat", "#minecraft:chest_boat",
    "minecraft:player",
    "minecraft:item", "minecraft:experience_orb", "minecraft:area_effect_cloud",
    "minecraft:item_display", "minecraft:text_display", "minecraft:block_display",
    "minecraft:marker", "minecraft:interaction", "minecraft:armor_stand",
    "minecraft:painting", "minecraft:item_frame", "minecraft:glow_item_frame",
    "minecraft:leash_knot", "minecraft:lightning_bolt", "minecraft:falling_block",
    "minecraft:tnt", "minecraft:end_crystal", "minecraft:fishing_bobber",
    "minecraft:eye_of_ender", "minecraft:firework_rocket", "minecraft:evoker_fangs",
    "minecraft:ominous_item_spawner", "minecraft:minecart",
    "minecraft:chest_minecart", "minecraft:furnace_minecart",
    "minecraft:hopper_minecart", "minecraft:spawner_minecart",
    "minecraft:tnt_minecart", "minecraft:command_block_minecart",
]

CUR = 'minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}]'

OBJECTIVES = ["rpg_squad", "rpg_sq_mode", "rpg_sq_cd", "rpg_sq_t",
              "rpg_sq_n", "rpg_sq_have", "rpg_sq_aim", "rpg_sq_stance",
              "rpg_sq_tier", "rpg_sq_roll", "rpg_sq_fr", "rpg_sq_slot"]

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
        '{Tags:["rpg.squad","rpg.merc","rpg.sq.new"],'
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


def free_nbt():
    """一名**待雇**佣兵。

    和在编的同一副身板，区别只在标签与名字：他没有 rpg.squad，所以不属于
    任何队伍，也不会被 lead 捞进去 —— 站着等价钱而已。
    rpg.merc 是伞标签，在编与待雇都带，专门给"新生僵尸重新配装"那条流水线
    排除用（尸壳属于 #minecraft:zombies）。
    """
    return member_nbt().replace(
        '{Tags:["rpg.squad","rpg.merc","rpg.sq.new"],',
        '{Tags:["rpg.sq.free","rpg.merc"],').replace(
        '"text":"佣兵"', '"text":"待雇佣兵"')


# ---------------------------------------------------------------------------
# 五等佣兵
# ---------------------------------------------------------------------------
# 名字取自作者指定的序列（HAIKU 即作者写的 hakui，按 Claude 的模型名读）。
#
# atk 是**基础**攻击，不是玩家看到的数字：剑给生物的加成实测为
# 木3 / 石4 / 铁5 / 钻6 / 下界合金7，所以 atk = 目标总攻击 − 起手剑加成。
# 名牌下方显示的是读属性得到的**当前**值，换了武器会跟着变。
# 整套盔甲各自加多少护甲点。原版护甲上限 30，所以图鉴报的是
# min(30, 基础 + 整套) —— 那才是玩家在信息板上看到的数。
SET_ARMOR = {"leather": 7, "chainmail": 12, "iron": 15,
             "diamond": 20, "netherite": 20}

SWORD_BONUS = {"wooden": 3, "stone": 4, "iron": 5, "diamond": 6, "netherite": 7}

TIERS = [
    dict(n=1, key="HAIKU",  colour="gray",    w=40, cut=40,
         hp=30,  armor=1,  tough=0, atk=1, sword="wooden",    mat="leather",
         trim=None,                   gear="皮革",     price=8),
    dict(n=2, key="SONNET", colour="#57C6D6", w=28, cut=68,
         hp=40,  armor=2,  tough=0, atk=2, sword="stone",     mat="chainmail",
         trim=("coast", "copper"),    gear="锁链",     price=20),
    dict(n=3, key="OPUS",   colour="#A275DE", w=18, cut=86,
         hp=55,  armor=5,  tough=2, atk=3, sword="iron",      mat="iron",
         trim=("ward", "iron"),       gear="铁",       price=40),
    dict(n=4, key="FABLE",  colour="#D9A02B", w=10, cut=96,
         hp=75,  armor=5,  tough=5, atk=5, sword="diamond",   mat="diamond",
         trim=("silence", "gold"),    gear="钻石",     price=80),
    dict(n=5, key="MYTHOS", colour="#FFD700", w=4,  cut=100,
         hp=100, armor=10, tough=8, atk=8, sword="netherite", mat="netherite",
         trim=("spire", "netherite"), gear="下界合金", price=160),
]

TRIM_CN = {"coast": "海岸", "ward": "守护", "silence": "沉寂", "spire": "尖塔"}

TAG_Y = "0.7"        # 信息板相对骑乘位的高度（想贴近名牌就调这个）


def _armour(t):
    """一整套甲，带纹饰。盔甲属于等级、不可替换 —— 纹饰就是等级的徽记。"""
    trim = ""
    if t["trim"]:
        trim = (',components:{"minecraft:trim":{pattern:"minecraft:%s",'
                'material:"minecraft:%s"}}' % t["trim"])
    slots = (("head", "helmet"), ("chest", "chestplate"),
             ("legs", "leggings"), ("feet", "boots"))
    return ",".join('%s:{id:"minecraft:%s_%s",count:1%s}'
                    % (slot, t["mat"], piece, trim) for slot, piece in slots)


def upgrade_armour(t):
    """升级时把整套甲换掉。

    `item replace` 一件一件来 —— 升级只动等级的东西，手上那把是玩家
    自己配的武器，一个字都不碰。起手剑同理：升级不退还、也不重发，
    他手上是什么就还是什么。
    """
    trim = ""
    if t["trim"]:
        trim = ('[minecraft:trim={pattern:"minecraft:%s",material:"minecraft:%s"}]'
                % t["trim"])
    slots = (("armor.head", "helmet"), ("armor.chest", "chestplate"),
             ("armor.legs", "leggings"), ("armor.feet", "boots"))
    return "\n".join(
        "item replace entity @s %s with minecraft:%s_%s%s"
        % (slot, t["mat"], piece, trim) for slot, piece in slots)


def gear_text(t):
    return t["gear"] + (("　·　%s纹饰" % TRIM_CN[t["trim"][0]]) if t["trim"] else "")


def plate(t, free):
    """名牌本身：佣兵 · MYTHOS。"""
    return ('[{"text":"%s · ","color":"gray"},'
            '{"text":"%s","color":"%s","bold":true}]'
            % ("待雇" if free else "佣兵", t["key"], t["colour"]))


def tier_nbt(t, free):
    """一名佣兵。

    Silent:1b —— 作者要求佣兵不出声。
    drop_chances：武器掉、盔甲不掉 —— 武器是玩家塞进去的投入，盔甲属于等级。
    """
    return (
        '{Tags:["%s","rpg.merc","rpg.sq.new"],'
        'IsBaby:0b,Silent:1b,PersistenceRequired:1b,CustomNameVisible:1b,'
        'CustomName:%s,Health:%df,'
        'attributes:['
        '{id:"max_health",base:%df},'
        '{id:"attack_damage",base:%df},'
        '{id:"armor",base:%df},'
        '{id:"armor_toughness",base:%df},'
        '{id:"follow_range",base:0f},'
        '{id:"movement_speed",base:0f},'
        '{id:"knockback_resistance",base:0.3f}],'
        'equipment:{mainhand:{id:"minecraft:%s_sword",count:1},%s},'
        'drop_chances:{mainhand:1f,head:0f,chest:0f,legs:0f,feet:0f}}'
        % ("rpg.sq.free" if free else "rpg.squad", plate(t, free),
           t["hp"], t["hp"], t["atk"], t["armor"], t["tough"],
           t["sword"], _armour(t)))


def board_nbt():
    """信息板。文本一律由 rpg:squad/board 现算现写，这里只搭壳子。"""
    return ('{Tags:["rpg.sq.board","rpg.sq.newboard"],'
            'billboard:"center",alignment:"center",see_through:0b,'
            'background:1610612736,'
            'transformation:{translation:[0f,%sf,0f],left_rotation:[0f,0f,0f,1f],'
            'scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]},'
            'text:[{"text":""}]}' % TAG_Y)


# ---------------------------------------------------------------------------
# 每刻
# ---------------------------------------------------------------------------
ROOT = """\
# 佣兵小队每刻入口。
# 只有一条玩家作用域判定；真正的遍历在雇主自己那一段里，而且限距。
execute as @a[tag=rpg.sq.lead] at @s run function rpg:squad/lead
execute as @a[scores={rpg_sq_t=1..}] run scoreboard players remove @s rpg_sq_t 1

# 佣兵没了，骑在他身上的信息板会掉下来 —— 收走。带类型且限距，很便宜。
execute if entity @e[type=minecraft:text_display,tag=rpg.sq.board,limit=1] run function rpg:squad/sweep

# 刚到场的人，等装备的属性生效之后再画一次信息板。
execute if entity @e[type=minecraft:husk,tag=rpg.sq.fresh,limit=1] run function rpg:squad/fresh
"""

FRESH = """# 刚到场那几刻反复补画。
#
# 装备带来的属性修饰符不是在 summon 那一刻就位的 —— 实测刚生出来读 armor
# 得到的是没算装备的基数。到底几刻才稳没有保证，所以干脆连画 %(N)d 刻再收手：
# 这段开销只在有人刚到场时存在，平时那道存在性判定直接落空。
execute as @e[type=minecraft:husk,tag=rpg.sq.fresh] run function rpg:squad/board
execute as @e[type=minecraft:husk,tag=rpg.sq.fresh] run scoreboard players add @s rpg_sq_fr 1
tag @e[type=minecraft:husk,tag=rpg.sq.fresh,scores={rpg_sq_fr=%(N)d..}] remove rpg.sq.fresh
"""

SWEEP = """\
# 收走没主人的信息板。
#
# 原本用 `distance=..1.5` 判断「附近还有没有佣兵」—— 那是错的：
# 板是**骑**在佣兵身上的，骑乘位比脚下高一截，这个距离量出来够不着，
# 结果板刚生出来就被自己人扫掉，五等佣兵的名牌下方一直是空的。
#
# 改成问它「还骑着东西吗」。骑着就有 vehicle；主人一死，乘客当场被甩下来，
# vehicle 就没了。精确，而且与距离无关。
execute as @e[type=minecraft:text_display,tag=rpg.sq.board] run function rpg:squad/sweep_one
"""

SWEEP_ONE = """\
scoreboard players set #ride rpg_squad 0
execute on vehicle run scoreboard players set #ride rpg_squad 1
execute if score #ride rpg_squad matches 0 run kill @s
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
%(SLOTS)s
"""

WALK_BOSS = """\
# 朝雇主走一步 —— 但不是照直走。
#
# 先转向雇主（人一直看着他，这样才像跟班），再把**执行朝向**偏 %(YAW)d 度
# 迈那一步：人就会绕到侧面去，而不是和别人挤在同一条线上。
# 偏航只影响这一步的方向，不动实体自己的朝向 —— 不需要任何三角函数。
tp @s ~ ~ ~ facing entity @a[tag=rpg.sq.boss,limit=1]
execute at @s rotated ~%(YAW)d 0 run function rpg:squad/step
"""

WALK_AIM = """\
# 朝目标走一步，同样按编号错开，免得四个人叠在目标同一侧。
tp @s ~ ~ ~ facing entity @e[tag=rpg.sq.mark,limit=1,sort=nearest,distance=..128]
execute at @s rotated ~%(YAW)d 0 run function rpg:squad/step
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
#
# 两步：身边没有待雇者就先招一个来（不花钱），有待雇者才是真的雇佣。
# 「只有对未雇佣的佣兵才会雇佣」——雇的是**眼前这个人**，不是凭空变一个出来。
advancement revoke @s only rpg:item/squad_hire
execute if entity @s[scores={rpg_sq_t=1..}] run return 0
scoreboard players set @s rpg_sq_t %(LOCK)d

# 头一次募兵先领一个队伍编号。多人下认人全靠它，不靠"最近的玩家"。
execute unless score @s rpg_squad = @s rpg_squad run function rpg:squad/enroll
scoreboard players operation #sq rpg_squad = @s rpg_squad

# 潜行 = 给身边的在编佣兵升一级（原本这个组合是空着的）
execute if predicate rpg:sneaking run return run function rpg:squad/upgrade

execute if entity @e[type=minecraft:husk,tag=rpg.sq.free,distance=..%(NEAR)d,limit=1] run return run function rpg:squad/enlist
function rpg:squad/post
"""

POST = """\
# 招一个待雇者到场，等级当场掷点 —— 甲、纹饰、基础数值与价钱全由这一掷定下。
# 掷完你看着名牌决定雇不雇，这才叫募兵。
execute store result score @s rpg_sq_roll run random value 1..100
%(ROLL)s
playsound minecraft:entity.villager.trade player @s ~ ~ ~ 1 0.9
"""

POST_ONE = """\
# %(KEY)s —— %(GEAR)s甲，❤%(HP)d ⛊%(ARMOR)d，价钱 %(PRICE)d 枚
execute at @s anchored eyes positioned ^ ^ ^2 run function rpg:squad/post%(N)d_at
title @s actionbar ["",{"text":"待雇 · %(KEY)s","color":"%(COLOUR)s","bold":true},{"text":"　%(PRICE)d 枚　再次长按雇下他","color":"gray","italic":true}]
"""

POST_AT = """\
summon minecraft:husk ~ ~ ~ %(NBT)s
summon minecraft:text_display ~ ~ ~ %(BOARD)s
execute as @e[type=minecraft:husk,tag=rpg.sq.new] run scoreboard players set @s rpg_sq_tier %(N)d
# 信息板骑在他身上 —— 跟着走，不必每刻 tp，也就没有一刻的延迟
execute as @e[type=minecraft:text_display,tag=rpg.sq.newboard] run ride @s mount @e[type=minecraft:husk,tag=rpg.sq.new,limit=1,sort=nearest]
tag @e[tag=rpg.sq.newboard] remove rpg.sq.newboard
# 信息板**下一刻**再画。装备是随 summon 一起给的，而它带来的属性修饰符
# 这一刻还没挂上 —— 现在读 armor 会少一截（实测 20，下一刻才是 30）。
tag @e[type=minecraft:husk,tag=rpg.sq.new] add rpg.sq.fresh
tag @e[type=minecraft:husk,tag=rpg.sq.new] remove rpg.sq.new
particle happy_villager ~ ~1 ~ 0.4 0.6 0.4 0.05 24
particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.02 12
"""

BOARD = """\
# 名牌**下方**那块信息板。实体名牌只渲染一行，换行符不生效，
# 所以另挂一个 text_display 骑在身上。
#
# 三个数都是**现读的属性**，不是写死的 —— 换了武器攻击数字跟着变。
%(GEAR)s
execute store result storage rpg:squad hp int 1 run attribute @s minecraft:max_health get
execute store result storage rpg:squad ar int 1 run attribute @s minecraft:armor get
execute store result storage rpg:squad atk int 1 run attribute @s minecraft:attack_damage get
function rpg:squad/board_do with storage rpg:squad
"""

BOARD_DO = """\
# 宏展开的那一行。信息板是骑在佣兵身上的那个 text_display。
$execute on passengers run data modify entity @s text set value ["",{"text":"$(gear)","color":"gray"},{"text":"\\n"},{"text":"❤ $(hp)","color":"red"},{"text":"　⛊ $(ar)","color":"#8FA1B3"},{"text":"　⚔ $(atk)","color":"#D4AF37"}]
"""



ENLIST = """\
# 眼前有一个待雇者。数一数已经有几个人，再看钱够不够。
#
# 每一条都用 `return run`：不用的话，命中 hire0 之后人数变成 1，
# 下一行 `if n=1` 也会成立 —— 一次按下会把四档全跑一遍，只扣第一档的钱。
scoreboard players set #cnt rpg_squad 0
execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players add #cnt rpg_squad 1
scoreboard players operation @s rpg_sq_n = #cnt rpg_squad
execute if entity @s[scores={rpg_sq_n=%(CAP)d..}] run return run function rpg:squad/full

scoreboard players set #tier rpg_squad 0
execute as @e[type=minecraft:husk,tag=rpg.sq.free,distance=..%(NEAR)d,limit=1,sort=nearest] run scoreboard players operation #tier rpg_squad = @s rpg_sq_tier

# 手上有多少钱。`clear ... 0` 是**只数不拿**，原版惯用写法。
execute store result score @s rpg_sq_have run clear @s %(CUR)s 0
%(BRANCH)s
"""

BUY_ONE = """\
# %(KEY)s：%(PRICE)d 枚。
execute if entity @s[scores={rpg_sq_have=..%(SHORT)d}] run return run function rpg:squad/poor
clear @s %(CUR)s %(PRICE)d
function rpg:squad/sign_on
"""

SIGN_ON = """\
# 钱付了，把眼前那个待雇者收编。
execute as @e[type=minecraft:husk,tag=rpg.sq.free,distance=..%(NEAR)d,limit=1,sort=nearest] run function rpg:squad/sign_one
title @s actionbar ["",{"text":"佣兵已入队","color":"%(GOLD)s"}]
playsound minecraft:entity.villager.yes player @s ~ ~ ~ 1 1
playsound minecraft:block.anvil_use player @a[distance=..12] ~ ~ ~ 0.6 1.4
"""

SIGN_ONE = """\
# 待雇 -> 在编。
tag @s remove rpg.sq.free
tag @s add rpg.squad
scoreboard players operation @s rpg_squad = #sq rpg_squad
scoreboard players set @s rpg_sq_mode 0
scoreboard players set @s rpg_sq_cd 0
# 队里的编号。站位按它分开 —— 不然四个人会停在同一个点上。
scoreboard players operation @s rpg_sq_slot = #cnt rpg_squad
%(RENAME)s
function rpg:squad/board
particle happy_villager ~ ~1.6 ~ 0.3 0.3 0.3 0.1 30
particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.03 16
"""

UPGRADE = """\
# 升级。潜行 + 募兵旗，对着身边的在编佣兵。
#
# 和掷点各有各的位置：掷点便宜但看运气，升级**确定**，所以按目标等级的
# **全价**收 —— 你买的是"这一次一定成"。
# 选择器不能直接比较实体与雇主的队伍编号，所以先把这一队的近身候选人挂上
# 只在本次同步调用里存活的 pick，然后再从中取最近的一个。不能先 limit=1
# 再验编号：另一个玩家的佣兵站得更近时，会把自己的人挡掉。
tag @s add rpg.sq.boss
execute as @e[type=minecraft:husk,tag=rpg.squad,distance=..%(NEAR)d] if score @s rpg_squad = #sq rpg_squad run tag @s add rpg.sq.pick
execute unless entity @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..%(NEAR)d] run function rpg:squad/none_near
scoreboard players set #tier rpg_squad 0
execute as @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..%(NEAR)d,limit=1,sort=nearest] run scoreboard players operation #tier rpg_squad = @s rpg_sq_tier
execute if score #tier rpg_squad matches %(TOP)d.. run function rpg:squad/up_max
execute store result score @s rpg_sq_have run clear @s %(CUR)s 0
%(BRANCH)s
tag @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..%(NEAR)d] remove rpg.sq.pick
tag @s remove rpg.sq.boss
"""

UP_ONE = """\
# 升到 %(KEY)s：%(PRICE)d 枚。
execute if entity @s[scores={rpg_sq_have=..%(SHORT)d}] run return run function rpg:squad/poor
clear @s %(CUR)s %(PRICE)d
execute as @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..%(NEAR)d,limit=1,sort=nearest] run function rpg:squad/up_do%(N)d
title @s actionbar ["",{"text":"已晋升 · %(KEY)s","italic":false,"color":"%(COLOUR)s","bold":true}]
"""

UP_DO = """\
# 换一身。等级的东西全部重写：数值、甲、纹饰、名牌，外加一把该等的起手剑。
# 手上那把是玩家自己配的，**不动** —— 武器归玩家，甲归等级。
scoreboard players set @s rpg_sq_tier %(N)d
attribute @s minecraft:max_health base set %(HP)d
attribute @s minecraft:armor base set %(ARMOR)d
attribute @s minecraft:armor_toughness base set %(TOUGH)d
attribute @s minecraft:attack_damage base set %(ATK)d
%(ARMOUR)s
data modify entity @s CustomName set value %(PLATE)s
scoreboard players set @s rpg_sq_fr 0
tag @s add rpg.sq.fresh
execute at @s run particle happy_villager ~ ~1.6 ~ 0.4 0.5 0.4 0.1 40
execute at @s run particle end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 24
execute at @s run playsound minecraft:entity.player.levelup player @a[distance=..16] ~ ~ ~ 1 1.2
"""

UP_MAX = """\
title @s actionbar ["",{"text":"他已经是 MYTHOS 了","italic":true,"color":"%(GOLD)s"}]
playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.7 1.4
"""

ENROLL = """\
scoreboard players add #sq_seq rpg_squad 1
scoreboard players operation @s rpg_squad = #sq_seq rpg_squad
scoreboard players set @s rpg_sq_stance 0
tag @s add rpg.sq.lead
"""


POOR = """\
title @s actionbar ["",{"text":"钱不够","italic":true,"color":"red"}]
playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 0.9
"""

FULL = """\
title @s actionbar ["",{"text":"小队已满员","italic":true,"color":"gray"}]
playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 1.2
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
# 三个动作靠「潜行」与「副手空不空」分开。
#
# 配装原本走 player_interacted_with_entity（右键佣兵），但那个触发器只在
# 交互**被消费**时才响 —— 原版全部七个用例都是真的做成了一件事（刷、喂、
# 拴、修、引诱），而用剑右键一只尸壳在原版里什么都不做。所以那条路不响。
# 改走副手 + using_item，与包里其余主动物品同一条路。
execute if predicate rpg:sneaking if items entity @s weapon.offhand * run return run function rpg:squad/fire_near
execute if predicate rpg:sneaking run return run function rpg:squad/stance
execute if items entity @s weapon.offhand * run return run function rpg:squad/handover
function rpg:squad/aim
"""

HANDOVER = """\
# 把副手那件交给最近的自己人。
tag @s add rpg.sq.boss
execute as @e[type=minecraft:husk,tag=rpg.squad,distance=..8] if score @s rpg_squad = #sq rpg_squad run tag @s add rpg.sq.pick
execute unless entity @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..8] run function rpg:squad/none_near
execute as @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..8,limit=1,sort=nearest] at @s run function rpg:squad/give_weapon
tag @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..8] remove rpg.sq.pick
tag @s remove rpg.sq.boss
"""

GIVE_WEAPON = """\
# @s 是佣兵，rpg.sq.boss 是雇主。他原本拿的掉在地上 —— 那就是取回的方式。
execute if items entity @s weapon.mainhand * run function rpg:squad/drop_weapon
item replace entity @s weapon.mainhand from entity @a[tag=rpg.sq.boss,limit=1] weapon.offhand
item replace entity @a[tag=rpg.sq.boss,limit=1] weapon.offhand with air
particle enchant ~ ~1.4 ~ 0.3 0.4 0.3 0.6 24
playsound minecraft:item.armor.equip_iron player @a[distance=..12] ~ ~ ~ 1 1.1
title @a[tag=rpg.sq.boss,limit=1] actionbar ["",{"text":"已配装","color":"%(GOLD)s"}]
# 攻击数字是现读的属性，换完武器要重画一次信息板
function rpg:squad/board
"""

FIRE_NEAR = """\
# 潜行 + 副手有东西 = 解雇最近的自己人。
tag @s add rpg.sq.boss
tag @s add rpg.sq.firing
execute as @e[type=minecraft:husk,tag=rpg.squad,distance=..8] if score @s rpg_squad = #sq rpg_squad run tag @s add rpg.sq.pick
execute unless entity @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..8] run function rpg:squad/none_near
execute as @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..8,limit=1,sort=nearest] at @s run function rpg:squad/dismiss
tag @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..8] remove rpg.sq.pick
tag @s remove rpg.sq.firing
tag @s remove rpg.sq.boss
"""

NONE_NEAR = """\
title @s actionbar ["",{"text":"身边没有自己的佣兵","italic":true,"color":"gray"}]
playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 1.2
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
# 视线上的 %(SIGHT)d 格，每 %(LEN)s 格取一个点。`positioned ^ ^ ^N` 取点，
# 命中即 return，不用递归。取点间隔比命中半径小 —— 否则小生物会从两点之间漏过去。
%(STEPS)s
function rpg:squad/miss
"""

# 先查实体、再查方块。反过来的话，瞄着站在地上的怪时射线只要蹭到地面
# 就当场判 miss —— 贴着墙、站在坑里、半身没在草里的目标全都指不中。
RAY_STEP = ("execute positioned ^ ^ ^%(D)s if entity @e[distance=..%(R)s,"
            "%(T)s,limit=1] "
            "run return run function rpg:squad/mark\n"
            "execute positioned ^ ^ ^%(D)s unless block ~ ~ ~ #minecraft:replaceable "
            "run return run function rpg:squad/miss")

MARK = """\
# 找到了。标记目标，全队转入交战。
execute as @e[distance=..%(R)s,%(T)s,limit=1,sort=nearest] run function rpg:squad/mark_one
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
%(REFUND)s
title @a[tag=rpg.sq.boss,limit=1] actionbar ["",{"text":"已解雇","italic":true,"color":"gray"}]
kill @s
"""


def build_ignore_tag():
    """指挥旗的类型黑名单。

    写成实体类型标签而不是一长串 `type=!...`：选择器里那串要在两个地方
    各抄一遍，迟早改漏一处；标签只有一份。
    """
    wj(os.path.join(DP, "data/rpg/tags/entity_type/sq_ignore.json"),
       {"values": [{"id": t, "required": False} for t in IGNORE_TYPES]})


def build_functions():
    wf("squad/squad.mcfunction", ROOT)
    wf("squad/lead.mcfunction", LEAD % {"LEASH": LEASH})
    wf("squad/member.mcfunction", MEMBER)
    # 队形：每个编号一条支线，停多远与从哪边靠都不同。
    slots = []
    for i in range(CAP):
        slots.append(
            "execute if entity @s[scores={rpg_sq_slot=%d}] "
            "if entity @a[tag=rpg.sq.boss,distance=%s..] "
            "run return run function rpg:squad/walk_boss%d"
            % (i, SLOT_DIST[i], i))
        wf("squad/walk_boss%d.mcfunction" % i, WALK_BOSS % {"YAW": SLOT_YAW[i]})
        wf("squad/walk_aim%d.mcfunction" % i, WALK_AIM % {"YAW": SLOT_YAW[i]})
    # 没发到编号的（老存档里的人）按 0 号走，不至于站着不动
    slots.append("execute unless score @s rpg_sq_slot = @s rpg_sq_slot "
                 "if entity @a[tag=rpg.sq.boss,distance=%s..] "
                 "run function rpg:squad/walk_boss0" % SLOT_DIST[0])
    wf("squad/follow.mcfunction",
       FOLLOW % {"LEASH": LEASH, "SLOTS": "\n".join(slots)})

    aims = ["execute if entity @s[scores={rpg_sq_slot=%d}] "
            "run return run function rpg:squad/walk_aim%d" % (i, i)
            for i in range(CAP)]
    aims.append("function rpg:squad/walk_aim0")
    wf("squad/walk_aim.mcfunction", "\n".join(
        ["# 按编号错开地压上去。没编号的走 0 号。"] + aims))
    wf("squad/step.mcfunction", STEP % {"STRIDE": STRIDE})
    wf("squad/engage.mcfunction", ENGAGE % {"REACH": REACH})
    wf("squad/strike.mcfunction", STRIKE % {"SWING": SWING})
    wf("squad/strike_do.mcfunction", STRIKE_DO % {"REACH": REACH})
    wf("squad/set_mark.mcfunction", SET_MARK)
    wf("squad/stand_down.mcfunction", STAND_DOWN)

    # ---- 五等：招募掷点、按等级定价、按等级换名牌 ----
    roll, buy, rename, gear = [], [], [], []
    lo = 1
    for t in TIERS:
        roll.append("execute if score @s rpg_sq_roll matches %d..%d "
                    "run return run function rpg:squad/post%d" % (lo, t["cut"], t["n"]))
        lo = t["cut"] + 1
        wf("squad/post%d.mcfunction" % t["n"], POST_ONE % {
            "N": t["n"], "KEY": t["key"], "COLOUR": t["colour"],
            "GEAR": t["gear"], "HP": t["hp"], "ARMOR": t["armor"],
            "PRICE": t["price"]})
        wf("squad/post%d_at.mcfunction" % t["n"], POST_AT % {
            "N": t["n"], "NBT": tier_nbt(t, True), "BOARD": board_nbt()})

        buy.append("execute if score #tier rpg_squad matches %d "
                   "run return run function rpg:squad/buy%d" % (t["n"], t["n"]))
        wf("squad/buy%d.mcfunction" % t["n"], BUY_ONE % {
            "KEY": t["key"], "PRICE": t["price"],
            "SHORT": t["price"] - 1, "CUR": CUR})

        rename.append("execute if entity @s[scores={rpg_sq_tier=%d}] "
                      "run data modify entity @s CustomName set value %s"
                      % (t["n"], plate(t, False)))
        gear.append("execute if entity @s[scores={rpg_sq_tier=%d}] "
                    "run data modify storage rpg:squad gear set value '%s'"
                    % (t["n"], gear_text(t)))

    wf("squad/hire.mcfunction", HIRE % {"LOCK": LOCK, "NEAR": 6})
    wf("squad/post.mcfunction", POST % {"ROLL": "\n".join(roll)})
    wf("squad/enlist.mcfunction",
       ENLIST % {"CAP": CAP, "CUR": CUR, "NEAR": 6, "BRANCH": "\n".join(buy)})
    wf("squad/sign_on.mcfunction", SIGN_ON % {"NEAR": 6, "GOLD": GOLD})
    wf("squad/sign_one.mcfunction", SIGN_ONE % {"RENAME": "\n".join(rename)})
    wf("squad/board.mcfunction", BOARD % {"GEAR": "\n".join(gear)})
    wf("squad/board_do.mcfunction", BOARD_DO)
    wf("squad/enroll.mcfunction", ENROLL)
    wf("squad/poor.mcfunction", POOR)
    wf("squad/full.mcfunction", FULL)

    wf("squad/order.mcfunction", ORDER % {"LOCK": LOCK})
    wf("squad/no_squad.mcfunction", NO_SQUAD)
    wf("squad/sweep.mcfunction", SWEEP)
    wf("squad/sweep_one.mcfunction", SWEEP_ONE)

    # 升级链。升到 N 等付 N 等的全价 —— 确定的东西比碰运气贵。
    ups = []
    for t in TIERS[1:]:
        ups.append("execute if score #tier rpg_squad matches %d "
                   "run function rpg:squad/up%d"
                   % (t["n"] - 1, t["n"]))
        wf("squad/up%d.mcfunction" % t["n"], UP_ONE % {
            "KEY": t["key"], "PRICE": t["price"], "SHORT": t["price"] - 1,
            "CUR": CUR, "NEAR": 6, "N": t["n"], "COLOUR": t["colour"]})
        wf("squad/up_do%d.mcfunction" % t["n"], UP_DO % {
            "N": t["n"], "HP": t["hp"], "ARMOR": t["armor"],
            "TOUGH": t["tough"], "ATK": t["atk"],
            "ARMOUR": upgrade_armour(t), "PLATE": plate(t, False)})
    wf("squad/upgrade.mcfunction", UPGRADE % {
        "NEAR": 6, "CUR": CUR, "TOP": TIERS[-1]["n"],
        "BRANCH": "\n".join(ups)})
    wf("squad/up_max.mcfunction", UP_MAX % {"GOLD": GOLD})
    wf("squad/fresh.mcfunction", FRESH % {"N": 6})
    wf("squad/handover.mcfunction", HANDOVER)
    wf("squad/give_weapon.mcfunction", GIVE_WEAPON % {"GOLD": GOLD})
    wf("squad/fire_near.mcfunction", FIRE_NEAR)
    wf("squad/none_near.mcfunction", NONE_NEAR)
    wf("squad/stance.mcfunction", STANCE)
    wf("squad/say_follow.mcfunction", SAY_FOLLOW % {"GOLD": GOLD})
    wf("squad/say_hold.mcfunction", SAY_HOLD % {"STEEL": STEEL})
    wf("squad/aim.mcfunction", AIM)
    wf("squad/unaim.mcfunction", UNAIM)
    # 步长 0.5：1 格的间隔会让小生物从两个取点之间漏过去。
    # 只在按下指挥旗那一刻跑一次，不是每刻 —— 多一倍的取点不进每刻开销。
    dists = [i * RAY_STEP_LEN for i in range(1, int(SIGHT / RAY_STEP_LEN) + 1)]
    steps = "\n".join(
        RAY_STEP % {"D": ("%g" % d),
                    "R": ("%.2f" % (RAY_R0 + RAY_RK * d)), "T": TARGET}
        for d in dists)
    wf("squad/ray.mcfunction",
       RAY % {"SIGHT": SIGHT, "LEN": ("%g" % RAY_STEP_LEN), "STEPS": steps})
    wf("squad/mark.mcfunction", MARK % {"R": MARK_R, "T": TARGET})
    build_ignore_tag()
    wf("squad/mark_one.mcfunction", MARK_ONE)
    wf("squad/miss.mcfunction", MISS)

    wf("squad/on_member.mcfunction", ON_MEMBER)
    wf("squad/take_weapon.mcfunction", TAKE_WEAPON % {"GOLD": GOLD})
    wf("squad/drop_weapon.mcfunction", DROP_WEAPON)
    refund = "\n".join(
        "execute at @s if entity @s[scores={rpg_sq_tier=%d}] "
        "run loot spawn ~ ~1 ~ loot rpg:squad/refund%d" % (t["n"], t["n"])
        for t in TIERS)
    wf("squad/dismiss.mcfunction", DISMISS % {"REFUND": refund})

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

    # 原本这里有个 squad_equip 进度（右键佣兵配装）。删掉了：
    # player_interacted_with_entity 只在交互**被消费**时才响，而尸壳在原版里
    # 右键没有任何行为 —— 对它永远不响；可对**会被消费**的交互却会响，
    # 比如拿拴绳右键，那会把拴绳"装备"给佣兵。配装改走副手 + 指挥旗。

    # 解雇退款：各退该等雇价的一半。一等一张表 ——
    # 掉落表里的数量只能是字面量，没法读记分板。
    for t in TIERS:
        wj(os.path.join(DP,
                        "data/rpg/loot_table/squad/refund%d.json" % t["n"]), {
            "type": "minecraft:generic",
            "pools": [{"rolls": 1, "entries": [
                {"type": "minecraft:item", "name": "minecraft:raw_gold",
                 "functions": [
                     {"function": "minecraft:set_count",
                      "count": t["price"] // 2},
                     {"function": "minecraft:set_components",
                      "components": {
                          "minecraft:custom_data": {"currency_tag": True}}}]}]}]})

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
    # The legacy zombie variant pipeline is optional and may be retired.  The
    # squad itself does not depend on it; there is simply nothing to exclude
    # mercenary husks from when the batch no longer exists.
    if not os.path.isfile(p):
        return 0
    s = io.open(p, encoding="utf-8").read()
    if "rpg.squad" in s:
        return 0
    old = "tag @e[type=#minecraft:zombies,tag=!zombie,limit=4] add rpg.spawn.new"
    assert old in s, "zombie_batch 不是预期的形状"
    new = ("# tag=!rpg.merc：佣兵也是尸壳，但他们是雇来的（含还没雇的待雇者），\n"
           "# 新出生的野怪重掷装备、更不该被替换成强化变种。\n"
           "tag @e[type=#minecraft:zombies,tag=!zombie,tag=!rpg.merc,limit=4] "
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
                row(seg("长按右键：身边没人时", "gray"),
                    seg("召出一名待雇佣兵", GOLD, True)),
                row(seg("　对着待雇者再长按一次，才是雇下他", "gray")),
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
                 row(seg("⚔配装", "white", True), seg("　副手拿武器 + 长按右键", STEEL)),
                 row(seg("　交给最近的佣兵；他原本拿的掉在地上", "gray")),
                 row(seg("⚔姿态", "white", True), seg("　潜行 + 长按右键", STEEL)),
                 row(seg("　跟随 ⇄ 驻守", "gray")),
                 row(seg("⚔解雇", "white", True), seg("　潜行 + 副手拿物品 + 长按", STEEL)),
                 row(seg("　装备掉地，退回一半雇金", "gray")),
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


def dump_for_guide():
    """把五等交给图鉴，免得两边各写一份、迟早写歪。

    与 add_pact 的 _pact.json 同一套路：数值只在这个文件里有一份。
    """
    wj(os.path.join(DP, "..", "_squad.json"),
       {"cap": CAP, "sight": SIGHT, "leash": LEASH, "cd": 13,
        "tiers": [{"n": t["n"], "key": t["key"], "colour": t["colour"],
                   "w": t["w"], "hp": t["hp"], "armor": t["armor"],
                   "atk": t["atk"], "sword": t["sword"], "gear": gear_text(t),
                   "tough": t["tough"],
                   "armor_real": min(30, t["armor"] + SET_ARMOR[t["mat"]]),
                   "price": t["price"],
                   "total": t["atk"] + SWORD_BONUS[t["sword"]]}
                  for t in TIERS]})


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
    dump_for_guide()
    cur = tag_currency()
    batch = guard_spawn_batch()
    print("squad: cap %d (husk), give +%d, currency tagged %d, spawn-batch guarded %d"
          % (CAP, gave, cur, batch))
    print("squad: objectives %s" % (obj or "-"))


if __name__ == "__main__":
    main()
