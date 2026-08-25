# -*- coding: utf-8 -*-
"""七十二柱契约：一本书，签下去就借到魔神的力，也把柱中的东西请进心里。

卷五写着「每一个正式边缘者都被分配一根柱位和一位魔神：边缘者借用魔神的力，
魔神借契约进入边缘者的心」。此前这句话在包里没有任何对应物 —— 魔化值只会
被动沾染，游戏从没有哪一刻**邀请你选择堕落**。契约补的就是这一步。

一本书两种行为，都走长按右键：

* 未立约　→ 签下契约。绑定柱位，恩赐与枷锁即刻生效，书变成已立约的样子
* 已立约　→ 动用柱中之力。冷却 15 秒，每次再添 3 点魔化

七位领主的「力量」尽量**直接复用罪器自己的施法路径**（路西法的蛇矛与尖牙、
利维坦的落锚），而不是另写一套相似的东西 —— 契约借的就是同一位魔神的力，
表现理应一模一样。只有那些和武器状态机缠死、无法独立调用的（亚巴顿的收割、
别西卜的余烬、萨麦尔的毒），才在这里另写一份同味道的。

恩赐与枷锁一律做成**属性修饰符**：`attribute ... modifier add` 写一次就长期
留在玩家身上，每刻零开销。只有萨麦尔的攻击附毒和玛门的拾取吸附必须逐刻看，
这两条各自挂在自己柱位的分数判定后面，没签那一柱就完全不进去。

七本契约书各有一张风格化纹理；原图保存在 `_tools/pact_art`，构建时复制到
材质包。custom_model_data 按柱位排为 1110031–1110037，并由同一份柱位表生成
range_dispatch，避免重建材质包后只剩占位图。
"""

import io
import json
import os
import shutil
import sys

import add_exorcism as ex          # 复用 HUD 的段落拼装与写文件

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
RP = sys.argv[2] if len(sys.argv) > 2 else "../resourcepack"
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pact_art")
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement/item")
GIVE = os.path.join(FUNC, "command/give/extra.mcfunction")

CMD0 = 1110031           # 柱位 N 的 custom_model_data = CMD0 + N - 1
CD = 300                 # 力量冷却（刻）
USE_TAINT = 3            # 每次动用柱中之力添的魔化
LOCK = 8                 # 触发去抖（刻）—— using_item 按住期间每刻都响
HUD_PACT = 5             # HUD 占用编号，接在驱魔那四个后面

OBJECTIVES = ["rpg_pact", "rpg_pact_cd", "rpg_pact_t",
              "rpg_hud_dm", "rpg_hud_dmt"]

RULE = ex.RULE
seg, row = ex.seg, ex.row


def wf(rel, text):
    ex.wf(rel, text)


# ---------------------------------------------------------------------------
# 七柱
# ---------------------------------------------------------------------------
# name / 罪 / 主色 / 恩赐文案 / 力量名 / 力量文案 / 枷锁文案
# boon / bane 是 (属性, 数值, 运算) 列表，签约时写进去，毁约时原样撤掉
PILLARS = [
    dict(n=1, who="路西法", sin="傲慢", colour="#00491C", lit="green",
         boon="攻击伤害 +2.5",
         power="原罪", power_text="沿视线刺出蛇矛，幻魔者尖牙同路破土；贯穿者受伤加重并向近旁蔓延",
         bane="击退抗性 −0.25（更容易被打飞）",
         boons=[("attack_damage", 2.5, "add_value")],
         banes=[("knockback_resistance", -0.25, "add_value")]),
    dict(n=2, who="利维坦", sin="嫉妒", colour="#1B4F72", lit="aqua",
         boon="移动速度 +8%",
         power="沉锚", power_text="向前方抛出巨锚，锚落处涌起漩涡，将敌人拖向锚心并持续碾压",
         bane="最大生命 −4",
         boons=[("movement_speed", 0.008, "add_value")],
         banes=[("max_health", -4, "add_value")]),
    dict(n=3, who="亚巴顿", sin="怠惰", colour="#6A6A70", lit="gray",
         boon="最大生命 +6",
         power="收割", power_text="周身 6 格爆发灵魂收割，每收割一个目标回复 1 颗心",
         bane="移动速度 −12%",
         boons=[("max_health", 6, "add_value")],
         banes=[("movement_speed", -0.012, "add_value")]),
    dict(n=4, who="别西卜", sin="暴食", colour="#5A6B1E", lit="yellow",
         boon="攻击速度 +12%",
         power="余烬", power_text="向前方喷出灰烬，追加三段刀罡",
         bane="护甲 −3",
         boons=[("attack_speed", 0.5, "add_value")],
         banes=[("armor", -3, "add_value")]),
    dict(n=5, who="萨麦尔", sin="暴怒", colour="#7B241C", lit="red",
         boon="攻击伤害 +1.5，且攻击附带剧毒",
         power="毒雾", power_text="前方 7 格喷出毒雾，中者剧毒与凋零并存",
         bane="最大生命 −2",
         boons=[("attack_damage", 1.5, "add_value")],
         banes=[("max_health", -2, "add_value")]),
    dict(n=6, who="贝利尔", sin="色欲", colour="#5B2C6F", lit="light_purple",
         boon="护甲 +2",
         power="朝拜", power_text="7 格内所有生物停止活动，并受一次冲击",
         bane="攻击伤害 −1",
         boons=[("armor", 2, "add_value")],
         banes=[("attack_damage", -1, "add_value")]),
    dict(n=7, who="玛门", sin="贪婪", colour="#B7950B", lit="gold",
         boon="6 格内的掉落物自动吸附到身边",
         power="点金", power_text="8 格内的掉落物尽数翻倍，并吐出经验",
         bane="魔化沾染速度翻倍",
         boons=[], banes=[]),
]


# ---------------------------------------------------------------------------
# 力量：七道
# ---------------------------------------------------------------------------
# 1 路西法［原罪］—— 直接借罪器自己的施法路径。
#   lucifer_lance / lucifer_fangs 的伤害归属读的是 @a[tag=rpg.luci.cast]，
#   所以只要把这个标签临时挂上，它们就能脱离武器独立跑。
P1 = """\
# 借的就是同一位魔神的力，表现与［原罪］一模一样 —— 蛇矛与尖牙都是罪器原件。
particle dust_color_transition{from_color:9882230,to_color:4895350,scale:1} ~ ~1.1 ~ 0.3 0.3 0.3 0.02 20
playsound minecraft:entity.ender_dragon.flap player @a[distance=..24] ~ ~ ~ 0.7 1.7
playsound minecraft:block.sculk_catalyst.bloom player @a[distance=..24] ~ ~ ~ 1 0.6
tag @s add rpg.luci.cast
execute at @s anchored eyes run function rpg:item/extra/lucifer_lance
execute at @s rotated ~ 0 run function rpg:item/extra/lucifer_fangs
tag @s remove rpg.luci.cast
"""

# 2 利维坦［沉锚］—— 同样借原件。血税不收：契约的代价是魔化，不是生命。
P2 = """\
# 落锚走罪器原件 leviathan_drop。`rotated ~ 0` 把俯仰归零 —— 锚是往下沉的东西。
tag @s add rpg.levi.cast
execute at @s if block ~ ~-1 ~ air run tag @s add rpg.levi.airborne
particle dust_color_transition{from_color:16559622,to_color:1195644,scale:1} ~ ~1.1 ~ 0.3 0.4 0.3 0.02 16
playsound minecraft:block.chain.break player @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:item.mace.smash_air player @a[distance=..24] ~ ~ ~ 1 0.7
execute at @s rotated ~ 0 positioned ^ ^ ^8 run function rpg:item/extra/leviathan_drop
tag @s remove rpg.levi.airborne
tag @s remove rpg.levi.cast
"""

# 3 亚巴顿［收割］—— 罪器那份和武器状态机缠死，这里另写一份同味道的。
P3 = """\
# 收割：周身一圈灵魂被抽走，抽一个回一颗心。
particle sculk_soul ~ ~1 ~ 3 1 3 0.02 120
particle soul ~ ~0.5 ~ 3 0.6 3 0.04 80
particle sculk_charge_pop ~ ~1 ~ 2.5 1 2.5 0.06 40
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..28] ~ ~ ~ 0.8 0.7
playsound minecraft:block.sculk_shrieker.shriek hostile @a[distance=..28] ~ ~ ~ 1 0.6
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run function rpg:pact/p3_reap
"""

P3_REAP = """\
# 一个目标的份。回血落在施术者身上 —— 收割是拿命换命。
damage @s 8 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
effect give @s minecraft:wither 4 0 true
particle soul ~ ~1 ~ 0.2 0.4 0.2 0.06 12
execute as @a[tag=rpg.pact.cast,limit=1,sort=nearest] run effect give @s minecraft:instant_health 1 0 true
"""

# 4 别西卜［余烬］
P4 = """\
# 余烬：灰扑出去，三段刀罡跟着切进去。
particle campfire_cosy_smoke ~ ~1 ~ 0.4 0.4 0.4 0.02 30
playsound minecraft:item.mace.smash_air player @a[distance=..24] ~ ~ ~ 1 0.8
playsound minecraft:entity.blaze.shoot hostile @a[distance=..24] ~ ~ ~ 1 0.6
execute at @s anchored eyes run function rpg:pact/p4_ash
"""

P4_ASH = """\
# 沿视线三段。`positioned ^ ^ ^N` 取点，整条线不需要递归。
%(STEPS)s
"""

P4_STEP = """\
execute positioned ^ ^ ^%(D)d run particle ash ~ ~ ~ 1 1 1 0.05 40
execute positioned ^ ^ ^%(D)d run particle sweep_attack ~ ~ ~ 0.8 0.8 0.8 0 4
execute positioned ^ ^ ^%(D)d run particle lava ~ ~ ~ 0.6 0.6 0.6 0 6
execute positioned ^ ^ ^%(D)d as @e[distance=..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run damage @s 7 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
execute positioned ^ ^ ^%(D)d as @e[distance=..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run effect give @s minecraft:hunger 8 2 true"""

# 5 萨麦尔［毒雾］
P5 = """\
# 毒雾：有毒的光辉使者，吐出来的东西也带光。
particle dust{color:[0.69,0.0,0.34],scale:2} ~ ~1 ~ 0.4 0.4 0.4 0.02 30
playsound minecraft:entity.witch.throw hostile @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:entity.spider.hurt hostile @a[distance=..24] ~ ~ ~ 0.8 0.5
execute at @s anchored eyes run function rpg:pact/p5_fog
"""

P5_FOG = """\
%(STEPS)s
"""

P5_STEP = """\
execute positioned ^ ^ ^%(D)d run particle dust_color_transition{from_color:[0.69,0.0,0.34],to_color:[0.24,0.0,0.12],scale:2} ~ ~ ~ 0.9 0.9 0.9 0.03 26
execute positioned ^ ^ ^%(D)d run particle sneeze ~ ~ ~ 0.7 0.7 0.7 0.02 10
execute positioned ^ ^ ^%(D)d as @e[distance=..2.6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run effect give @s minecraft:poison 10 2 true
execute positioned ^ ^ ^%(D)d as @e[distance=..2.6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run effect give @s minecraft:wither 6 1 true
execute positioned ^ ^ ^%(D)d as @e[distance=..2.6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run damage @s 3 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]"""

# 6 贝利尔［朝拜］—— 与罪器那一版同形：7 格内全部定住。
P6 = """\
# 朝拜：叛天的首谋一开口，方圆七格都得低头。
particle enchant ~ ~1.2 ~ 3 1.5 3 1 150
particle dust_color_transition{from_color:[0.4,0.0,0.6],to_color:[0.0,0.0,0.0],scale:2} ~ ~1 ~ 3 1.2 3 0.06 90
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..28] ~ ~ ~ 1 0.6
playsound minecraft:block.beacon.power_select master @a[distance=..28] ~ ~ ~ 0.8 0.5
execute as @e[distance=0.1..7,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run function rpg:pact/p6_kneel
"""

P6_KNEEL = """\
effect give @s minecraft:slowness 5 255 true
effect give @s minecraft:weakness 5 2 true
effect give @s minecraft:glowing 5 0 true
particle dust_color_transition{from_color:[0.4,0.0,0.6],to_color:[0.0,0.0,0.0],scale:2} ~ ~1 ~ 0.3 0.6 0.3 0.05 16
damage @s 4 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
"""

# 7 玛门［点金］
P7 = """\
# 点金：贪婪不制造东西，它只让已有的东西变多。
particle happy_villager ~ ~1 ~ 3 1 3 0.2 80
particle wax_on ~ ~1 ~ 3 1 3 0.1 60
particle end_rod ~ ~1 ~ 2.5 1 2.5 0.05 40
playsound minecraft:block.amethyst_block.chime player @a[distance=..24] ~ ~ ~ 1 1.4
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.8 1.6
execute as @e[type=minecraft:item,distance=..8] at @s run function rpg:pact/p7_gild
summon minecraft:experience_orb ~ ~1 ~ {Value:60}
"""

P7_GILD = """# 一堆掉落物翻一倍。读出这堆的数量、翻倍、写回去 —— 比逐件复制便宜得多。
# 只处理 32 及以下的堆：再多翻倍就越过 64 的堆叠上限了。
particle wax_on ~ ~0.4 ~ 0.2 0.2 0.2 0.05 8
execute store result score #gild rpg_pact run data get entity @s Item.count
execute if score #gild rpg_pact matches 1..32 run function rpg:pact/p7_double
"""

P7_DOUBLE = """scoreboard players operation #gild rpg_pact *= #two rpg_pact
execute store result entity @s Item.count byte 1 run scoreboard players get #gild rpg_pact
"""

# ---- 玛门的常驻：拾取吸附 ----
MAMMON_TICK = """\
# 贪婪不用弯腰 —— 6 格内的掉落物自己飘过来。
# 只有签了第七柱的人才会进到这里，其余柱位连一次走查都不欠。
execute as @e[type=minecraft:item,distance=0.6..6,nbt={PickupDelay:0s}] at @s facing entity @p feet run tp @s ^ ^ ^0.45
"""

# ---- 萨麦尔的常驻：攻击附毒 ----
SAMAEL_TICK = """\
# 暴怒的毒。走 rpg.hurt + on attacker，与包里其余被动同一形状。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.pact,scores={rpg_pact=5}] run effect give @e[distance=..1,limit=1] minecraft:poison 6 1 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.pact,scores={rpg_pact=5}] run particle dust{color:[0.69,0.0,0.34],scale:1} ~ ~1 ~ 0.3 0.4 0.3 0.02 8
"""


# ---------------------------------------------------------------------------
# 触发与分流
# ---------------------------------------------------------------------------
TRIGGER = """\
# 契约之书 —— 由 rpg:item/pact 在长按右键时触发。
#
# `minecraft:using_item` 在按住期间**每刻都会响**，而签约与动用都该是一次性的，
# 所以先用一个短锁去抖：锁没退干净就直接返回。
advancement revoke @s only rpg:item/pact
execute if entity @s[scores={rpg_pact_t=1..}] run return 0
scoreboard players set @s rpg_pact_t %(LOCK)d

execute unless entity @s[tag=rpg.pact] run function rpg:pact/sign
execute if entity @s[tag=rpg.pact] run function rpg:pact/invoke
"""

SIGN = """\
# 还没有柱位。看手里这本是哪一柱，就签哪一柱。
# `if items` 读的是手上那一件，不需要翻整个背包。
%(BRANCH)s
"""

SIGN_ONE = """\
# 第 %(N)d 柱 · %(WHO)s（%(SIN)s）
scoreboard players set @s rpg_pact %(N)d
scoreboard players set @s rpg_pact_cd %(CD)d
tag @s add rpg.pact
%(ATTR)s
item replace entity @s weapon.mainhand with %(ITEM)s
title @s times 10 70 20
title @s title ["",{"text":"契 约 已 立","italic":false,"color":"%(COLOUR)s","bold":true}]
title @s subtitle ["",{"text":"%(WHO)s之柱 · %(SIN)s","italic":false,"color":"%(LIT)s"}]
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.8 0.6
playsound minecraft:entity.wither.spawn master @a[distance=..32] ~ ~ ~ 0.5 1.4
execute at @s run particle sculk_charge_pop ~ ~1 ~ 0.5 0.8 0.5 0.1 60
execute at @s run particle minecraft:flash{color:%(FLASH)d} ~ ~1 ~ 0 0 0 0 1
tellraw @s ["",{"text":"◆ ","color":"%(COLOUR)s"},{"text":"魔神借契约进入你的心。","color":"gray","italic":true}]
"""

INVOKE = """\
# 已有柱位。手里必须是**自己那一本已立约的书** —— 攥着别柱的书没有用。
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{pact_signed:1b}] run return run function rpg:pact/reissue

# 站在一支**燃着的**驱魔图腾旁边举起这本书，不是动用力量，而是毁约。
# 这是逆圣化之外的第二条解约途径 —— 详见 rpg:pact/renounce。
execute if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,distance=..%(R)d] run return run function rpg:pact/renounce

execute if entity @s[scores={rpg_pact_cd=1..}] run return run function rpg:pact/cooling

scoreboard players set @s rpg_pact_cd %(CD)d
scoreboard players add @s rpg_taint %(TAINT)d
tag @s add rpg.pact.cast
%(BRANCH)s
tag @s remove rpg.pact.cast
"""

REISSUE = """# 手里这本没盖过印。死一次把书掉了是常事 —— 柱位还在身上，
# 只要新捡的这本正是同一柱，就地重新盖印，而不是把人卡死。
# 柱位对不上才是真的攥错了书。
%(BRANCH)s
function rpg:pact/wrong_book
"""

BURN = """\
# 退书 + 解约。逆圣化与毁约两条路共用这一段。
#
# 顺序要紧：先把书退回未立约，再 break —— break 会清掉柱位编号，
# 清掉之后就认不出该退成哪一本了。
%(UNSIGN)s
function rpg:pact/break
"""

RENOUNCE = """\
# 毁约。
#
# 契约本来只有逆圣化一条出路，而逆圣化要求魔化先推到 100 ——
# 对签错柱位的人那不是出路，是死胡同。所以给它第二条：
# 借驱魔仪式的火烧断它。仪式本来就是烧污染的，成本也实打实
# （一支图腾加一瓶圣水）。
#
function rpg:pact/burn

# 柱中的东西不会白白松手。
scoreboard players add @s rpg_taint %(BACKLASH)d
execute if entity @s[scores={rpg_taint=%(MAXP)d..}] run scoreboard players set @s rpg_taint %(MAX)d
effect give @s minecraft:wither 10 1
effect give @s minecraft:blindness 4 0

particle minecraft:flash{color:16777200} ~ ~1 ~ 0 0 0 0 1
particle end_rod ~ ~1 ~ 0.6 0.8 0.6 0.25 120
particle sculk_charge_pop ~ ~1 ~ 0.5 0.7 0.5 0.12 80
playsound minecraft:block.beacon.deactivate master @a[distance=..32] ~ ~ ~ 1 0.6
playsound minecraft:entity.wither.hurt master @s ~ ~ ~ 1 0.7
title @s times 10 60 20
title @s title ["",{"text":"契 约 已 断","italic":false,"color":"gold","bold":true}]
title @s subtitle ["",{"text":"柱位空了出来，代价留在你身上","italic":false,"color":"gray"}]

# 图腾把自己烧尽了
kill @e[type=minecraft:item_display,tag=rpg.totem.lit,distance=..%(R)d,limit=1,sort=nearest]
"""

UNSIGN_ONE = """\
# 从背包里把已立约的那本收走，发回一本未立约的。
#
# 不用 `item replace weapon.mainhand`：毁约是举着书触发的，书确实在手里；
# 但逆圣化那条路玩家多半**没拿着书**，照抄过去会把手里那件东西顶掉。
clear @s minecraft:enchanted_book[minecraft:custom_data~{pact_signed:1b,pact:%(N)d}]
give @s %(ITEM)s
"""


WRONG_BOOK = """\
# 攥着另一柱的书。柱位是排他的 —— 一个人只能挂在一根柱子上。
title @s actionbar ["",{"text":"你已与另一柱立约","italic":true,"color":"dark_red"}]
playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 0.8
"""

COOLING = """\
# 柱中之力还没回气。把剩余时间交给统一 HUD 渲染，别再多写一条 actionbar。
playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.6 0.5
"""

CD_TICK = """\
# 冷却递减，仅此而已。
#
# 原本这里还会把 rpg_hud 占成蓄力档 —— 那意味着每用一次柱中之力，
# 魔化条就被顶掉整整 15 秒。契约冷却和魔化一样是**持续状态**，
# 现在两者由 rpg:hud/status 并排画在同一行里，谁也不顶谁。
scoreboard players remove @s rpg_pact_cd 1
"""

# 逆圣化会把契约一并烧断 —— 反转烧掉的是污染的一切，柱位也在其中。
BREAK = """\
# 毁约。恩赐与枷锁一同撤走，柱位清空。
%(ATTR)s
scoreboard players set @s rpg_pact 0
scoreboard players set @s rpg_pact_cd 0
tag @s remove rpg.pact
playsound minecraft:block.glass.break master @s ~ ~ ~ 1 0.5
"""


def item_snbt(p, signed):
    """一本书的完整 SNBT。签约前后只差名字、Lore 和两个 custom_data 位。"""
    tag = "[已立约]" if signed else "[契约]"
    lore = [RULE,
            row(seg("七十二柱之一，", "gray"), seg("所罗门", p["colour"], True),
                seg("封入柱中的名", "gray"))]
    if signed:
        lore.append(row(seg("长按右键动用柱中之力（冷却 %d 秒）" % (CD // 20), "gray")))
        lore.append(row(seg("在燃着的驱魔图腾旁长按则", "gray"),
                        seg("毁约", "#FF3300", True)))
    else:
        lore.append(row(seg("长按右键签下契约", "gray")))
    lore += [RULE,
             row(seg("🜏恩赐", "white", True), seg("　" + p["boon"], p["lit"])),
             row(seg("🜏力量", "white", True), seg("[" + p["power"] + "]", p["colour"], True)),
             row(seg("　" + p["power_text"], "gray")),
             row(seg("🜏枷锁", "white", True), seg("　" + p["bane"], "dark_red")),
             RULE,
             row(seg("契约期间持续沾染", "gray"), seg("魔化", "dark_red", True)),
             RULE]
    data = "{pact_tag:1b,pact:%d%s}" % (p["n"], ",pact_signed:1b" if signed else "")
    return ("enchanted_book["
            "custom_name=" + row(seg(tag, p["colour"], True),
                                 seg(p["who"] + "之柱", "white")) + ","
            "lore=[" + ",".join(lore) + "],"
            "custom_model_data={floats:[%d.0f]}," % (CMD0 + p["n"] - 1) +
            "enchantment_glint_override=true,"
            "max_stack_size=1,"
            "food={nutrition:0,saturation:0f,can_always_eat:1b},"
            'consumable={consume_seconds:100120f,animation:"block",'
            'sound:"minecraft:block.enchantment_table.use",'
            "has_consume_particles:false,on_consume_effects:[]},"
            "custom_data=" + data + "]")


def attr_lines(p, add):
    """恩赐与枷锁的属性修饰符。id 用 rpg:pact/N/... ，毁约时按同一个 id 撤。"""
    out = []
    for kind, mods in (("boon", p["boons"]), ("bane", p["banes"])):
        for i, (attr, amount, op) in enumerate(mods):
            mid = "rpg:pact/%d/%s%d" % (p["n"], kind, i)
            if add:
                # 先撤再加：同名修饰符重复添加会被服务器拒绝
                out.append("attribute @s minecraft:%s modifier remove %s" % (attr, mid))
                out.append("attribute @s minecraft:%s modifier add %s %s %s"
                           % (attr, mid, amount, op))
            else:
                out.append("attribute @s minecraft:%s modifier remove %s" % (attr, mid))
    return "\n".join(out) if out else "# 这一柱不靠属性修饰符 —— 它的恩赐与枷锁都是逐刻的"


def build_functions():
    n = 0

    # ---- 七道力量 ----
    wf("pact/p1.mcfunction", P1)
    wf("pact/p2.mcfunction", P2)
    wf("pact/p3.mcfunction", P3)
    wf("pact/p3_reap.mcfunction", P3_REAP)
    wf("pact/p4.mcfunction", P4)
    wf("pact/p4_ash.mcfunction",
       P4_ASH % {"STEPS": "\n".join(P4_STEP % {"D": d} for d in (2, 4, 6))})
    wf("pact/p5.mcfunction", P5)
    wf("pact/p5_fog.mcfunction",
       P5_FOG % {"STEPS": "\n".join(P5_STEP % {"D": d} for d in (2, 4, 6))})
    wf("pact/p6.mcfunction", P6)
    wf("pact/p6_kneel.mcfunction", P6_KNEEL)
    wf("pact/p7.mcfunction", P7)
    wf("pact/p7_gild.mcfunction", P7_GILD)
    wf("pact/p7_double.mcfunction", P7_DOUBLE)
    n += 13

    # ---- 签约 ----
    branch = []
    for p in PILLARS:
        branch.append("execute if items entity @s weapon.mainhand "
                      "*[minecraft:custom_data~{pact:%d}] run function rpg:pact/sign%d"
                      % (p["n"], p["n"]))
        wf("pact/sign%d.mcfunction" % p["n"], SIGN_ONE % {
            "N": p["n"], "CD": CD, "WHO": p["who"], "SIN": p["sin"],
            "COLOUR": p["colour"], "LIT": p["lit"],
            "FLASH": int(p["colour"].lstrip("#"), 16),
            "ATTR": attr_lines(p, True),
            "ITEM": item_snbt(p, True)})
        wf("pact/break%d.mcfunction" % p["n"],
           BREAK % {"ATTR": attr_lines(p, False)})
        n += 2
    wf("pact/sign.mcfunction", SIGN % {"BRANCH": "\n".join(branch)})

    # ---- 动用 ----
    inv = ["execute if entity @s[scores={rpg_pact=%d}] run function rpg:pact/p%d"
           % (p["n"], p["n"]) for p in PILLARS]
    wf("pact/invoke.mcfunction",
       INVOKE % {"CD": CD, "TAINT": USE_TAINT, "R": ex.RITE_R,
                 "BRANCH": "\n".join(inv)})

    # 毁约：先把书退回未立约（break 会清掉柱位编号，之后就认不出该退成哪本），
    # 再撤掉恩赐与枷锁。
    unsign = []
    for q in PILLARS:
        unsign.append("execute if entity @s[scores={rpg_pact=%d}] "
                      "run function rpg:pact/unsign%d" % (q["n"], q["n"]))
        wf("pact/unsign%d.mcfunction" % q["n"],
           UNSIGN_ONE % {"N": q["n"], "ITEM": item_snbt(q, False)})
    wf("pact/burn.mcfunction", BURN % {"UNSIGN": "\n".join(unsign)})
    wf("pact/renounce.mcfunction",
       RENOUNCE % {"BACKLASH": 20,
                   "MAX": ex.TAINT_MAX, "MAXP": ex.TAINT_MAX + 1,
                   "R": ex.RITE_R})
    wf("pact/trigger.mcfunction", TRIGGER % {"LOCK": LOCK})
    reissue = ["execute if entity @s[scores={rpg_pact=%d}] "
               "if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:%d}] "
               "run return run function rpg:pact/sign%d" % (q["n"], q["n"], q["n"])
               for q in PILLARS]
    wf("pact/reissue.mcfunction", REISSUE % {"BRANCH": "\n".join(reissue)})
    wf("pact/wrong_book.mcfunction", WRONG_BOOK)
    wf("pact/cooling.mcfunction", COOLING)
    wf("pact/cd.mcfunction", CD_TICK)
    wf("pact/mammon.mcfunction", MAMMON_TICK)
    wf("pact/samael.mcfunction", SAMAEL_TICK)

    # 毁约总入口：逆圣化烧断契约时走这里，按柱位撤掉对应的修饰符
    brk = ["execute if entity @s[scores={rpg_pact=%d}] run function rpg:pact/break%d"
           % (p["n"], p["n"]) for p in PILLARS]
    wf("pact/break.mcfunction",
       "# 毁约总入口。柱位不同，要撤的修饰符也不同。\n" + "\n".join(brk))

    wj = ex.wj
    wj(os.path.join(ADV, "pact.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:using_item",
            "conditions": {
                "item": {"predicates": {
                    "minecraft:custom_data": "{pact_tag:1b}"}}}}},
        "rewards": {"function": "rpg:pact/trigger"}})
    return n


def build_hud_bar():
    """（已废弃）契约冷却现在与魔化并排画在状态行里，不再占蓄力档。"""
    return


def build_hud_identity():
    """从 PILLARS 生成 actionbar 的契约对象段。

    七柱的名字、罪与颜色只在这里有一个事实来源。驱魔 HUD 只预留第二段并
    调用 `rpg:hud/pact`，不复制这张表；以后改柱名或代表色会自动同步。
    """
    status_p = os.path.join(FUNC, "hud/status.mcfunction")
    render_p = os.path.join(FUNC, "hud/render.mcfunction")
    status = io.open(status_p, encoding="utf-8").read()
    render = io.open(render_p, encoding="utf-8").read()
    assert "function rpg:hud/pact" in status, "统一 HUD 没有预留契约对象段"
    assert "storage rpg:hud b" in status and "$(b)" in render, \
        "统一 HUD 的契约对象 storage 段不完整"

    dispatch = [
        "# 当前契约对象。身份是持续状态，即使力量已经冷却也一直显示。",
        "scoreboard players set @s rpg_hud_on 1",
    ]
    for p in PILLARS:
        dispatch.append(
            "execute if entity @s[scores={rpg_pact=%d}] run function rpg:hud/pact%d"
            % (p["n"], p["n"]))
        comp = row(seg("　│　契约 ", "dark_gray"),
                   seg(p["who"], p["lit"], True),
                   seg(" · " + p["sin"], p["lit"]))
        wf("hud/pact%d.mcfunction" % p["n"],
           "data modify storage rpg:hud b set value '%s'" % comp)
    wf("hud/pact.mcfunction", "\n".join(dispatch))
    return len(PILLARS) + len(dispatch)


def _build_hud_bar_unused():
    """给契约冷却加一条 HUD，编号接在驱魔那四个后面。

    条的拼装直接借 add_exorcism 的 helper —— 同一套字符、同一套配色，
    再抄一份只会让两处慢慢长歪。
    """
    body = ["# 契约冷却条。回满即可再次动用柱中之力。"]
    for k in range(ex.SEGMENTS + 1):
        comp = ex.row(ex.seg("契约 ", "dark_gray"),
                      *ex.bar(k, ex.SEGMENTS, "dark_red"),
                      ex.seg("  %d%%" % (k * 100 // ex.SEGMENTS), "gray"))
        body.append("execute if entity @s[scores={rpg_hud_p=%d}] run title @s actionbar %s"
                    % (k, comp))
    wf("hud/s%d.mcfunction" % HUD_PACT, "\n".join(body))

    # 挂进调度层，紧跟其余技能条
    p = os.path.join(FUNC, "hud/hud.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg:hud/s%d" % HUD_PACT in s:
        return
    hook = ("execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=%d}] "
            "run function rpg:hud/s%d" % (ex.HUD_INVERT, ex.HUD_INVERT))
    s = s.replace(hook, hook + "\n" +
                  "execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=%d}] "
                  "run function rpg:hud/s%d" % (HUD_PACT, HUD_PACT))
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def wire_tick():
    """三条挂在驱魔入口上 —— 都是玩家作用域，没签约的人一条也进不去。"""
    p = os.path.join(FUNC, "exorcism.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg:pact/cd" in s:
        return 0
    s = s.rstrip("\n") + """

# 七十二柱契约。三条全是玩家作用域（玩家表很短），
# 而且各自带着柱位判定 —— 没签那一柱的人连函数都不会进。
execute as @a[scores={rpg_pact_cd=1..}] run function rpg:pact/cd
execute as @a[tag=rpg.pact,scores={rpg_pact=5}] at @s run function rpg:pact/samael
execute as @a[tag=rpg.pact,scores={rpg_pact=7}] at @s run function rpg:pact/mammon
execute as @a[scores={rpg_pact_t=1..}] run scoreboard players remove @s rpg_pact_t 1
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    return 4


def wire_taint():
    """契约的常驻代价：每次结算多沾 1 点，玛门翻倍。"""
    p = os.path.join(FUNC, "taint/step.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg.pact" in s:
        return 0
    anchor = "execute if entity @s[tag=rpg.h.devil_weapon_tag1] run scoreboard players add @s rpg_taint 1"
    add = (anchor + "\n"
           "# 立约本身就是代价 —— 柱中的东西一直在往里渗。贪婪那一柱渗得更快。\n"
           "execute if entity @s[tag=rpg.pact] run scoreboard players add @s rpg_taint 1\n"
           "execute if entity @s[tag=rpg.pact,scores={rpg_pact=7}] run scoreboard players add @s rpg_taint 1")
    assert anchor in s
    io.open(p, "w", encoding="utf-8", newline="\n").write(s.replace(anchor, add))

    # 逆圣化把污染整个烧穿，柱位也在其中
    q = os.path.join(FUNC, "rite/inv_grant.mcfunction")
    t = io.open(q, encoding="utf-8").read()
    if "rpg:pact/burn" not in t:
        t = t.replace("scoreboard players set @s rpg_taint 0",
                      "scoreboard players set @s rpg_taint 0\n"
                      "# 反转烧掉的是污染的一切 —— 柱位也在其中。\n"
                      "# 走 burn 而不是 break：光清标记的话，玩家手里会留着一本\n"
                      "# 「已立约」的空壳 —— 看着还在契约中，实际什么也没有。\n"
                      "execute if entity @s[tag=rpg.pact] run function rpg:pact/burn")
        io.open(q, "w", encoding="utf-8", newline="\n").write(t)
    return 1


LORD = """\
# 从这个人身上挣出来的是谁 —— 看他签的是哪一柱。
# 没签过的人交给最后那一行的无名者。
%(BRANCH)s
%(NONE)s
"""

LORD_ONE = """\
# %(WHO)s。契约不是租约：借过的力，最后会自己来取回去。
#
# 底子与无名者那只一样：卫道士 + devil 标签（隐身与烟雾由包里
# 已有的恶魔 boss 那一套负责），最多十分钟后自己散掉。
summon minecraft:vindicator ~ ~1 ~ %(NBT)s
# 记下他是哪一位 —— 出手时按这个分流。要在 advent_life 之前，
# 那一步会把 rpg.advent.new 摘掉。
scoreboard players set @e[tag=rpg.advent.new] rpg_dm_lord %(N)d
function rpg:taint/advent_life
particle dust{color:[%(RGB)s],scale:3} ~ ~1.2 ~ 0.8 1 0.8 0.05 70
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..48] ~ ~ ~ 1 0.5
"""


# ---------------------------------------------------------------------------
# 降临者那一手
# ---------------------------------------------------------------------------
# 取自各自的罪器与柱中之力 —— 借的是同一位魔神的力，挣出来之后
# 表现理应还是那一套。归属统一读 @e[tag=rpg.dm.cast]。
BY = 'by @e[tag=rpg.dm.cast,limit=1]'
PLAYERS = '@a[distance=..%d,gamemode=!spectator,gamemode=!creative]'

SKILLS = {
    # ---------------- 路西法 · 傲慢 ----------------
    1: [
        ("""\
# 原罪 —— 蛇矛沿视线破土，尖牙同路。
data modify storage rpg:demon uuid set from entity @s UUID
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle dust{color:[0.0,0.29,0.11],scale:2} ~ ~1 ~ 0.6 0.8 0.6 0.05 40
execute at @s anchored eyes facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run function rpg:taint/sk1_line with storage rpg:demon
""", {"sk1_line": "$" + "\n$".join(
            "execute positioned ^ ^ ^%d run summon minecraft:evoker_fangs "
            "~ ~ ~ {Warmup:%d,Owner:$(uuid)}" % (d, d * 2)
            for d in range(1, 9))}),

        ("""\
# 蛇矛 —— 一记贯穿，连着把人钉退。
playsound minecraft:entity.breeze.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.6
execute at @s anchored eyes facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run function rpg:taint/sk1b_thrust
""", {"sk1b_thrust": "\n".join(
            "execute positioned ^ ^ ^%d run particle dust{color:[0.0,0.29,0.11],scale:2} ~ ~ ~ 0.2 0.2 0.2 0 6\n"
            "execute positioned ^ ^ ^%d run particle crit ~ ~ ~ 0.2 0.2 0.2 0.1 8\n"
            "execute positioned ^ ^ ^%d as @a[distance=..2,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk1b_hit"
            % (d, d, d) for d in range(1, 10))}),

        ("""\
# 高踞 —— 傲慢把人举起来，再让他自己摔下去。
playsound minecraft:entity.illusioner.prepare_blindness hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle end_rod ~ ~1 ~ 3 1 3 0.1 60
execute as %(P8)s run function rpg:taint/sk1c_lift
""", {"sk1c_lift": """\
effect give @s minecraft:levitation 3 1 true
damage @s 3 minecraft:magic %(BY)s
"""}),

        ("""\
# 失坠 —— 王冠之下不许任何人保有自己的高度。
playsound minecraft:entity.phantom.flap hostile @a[distance=..32] ~ ~ ~ 1 0.55
playsound minecraft:entity.ender_dragon.flap hostile @a[distance=..32] ~ ~ ~ 0.7 1.45
particle dragon_breath ~ ~1.5 ~ 3 1.2 3 0.08 72
particle dust_color_transition{from_color:[0.19,0.85,0.49],to_color:[0.0,0.18,0.07],scale:2.2} ~ ~1 ~ 3 1 3 0.04 54
execute as %(P8)s run function rpg:taint/sk1d_fall
""", {"sk1d_fall": """\
effect give @s minecraft:levitation 2 1 true
effect give @s minecraft:weakness 5 1 true
damage @s 5 minecraft:magic %(BY)s
"""}),

        ("""\
# 王座回绝 —— 靠得太近的人会被王座本身拒斥。
playsound minecraft:block.beacon.deactivate hostile @a[distance=..32] ~ ~ ~ 1 0.55
particle end_rod ~ ~1.5 ~ 2.5 1.2 2.5 0.08 72
particle enchanted_hit ~ ~1 ~ 3 1 3 0.15 64
execute as %(P6)s at @s run function rpg:taint/sk1e_reject
""", {"sk1e_reject": """\
execute facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^-3
damage @s 6 minecraft:magic %(BY)s
effect give @s minecraft:slowness 4 1 true
"""}),
    ],

    # ---------------- 利维坦 · 嫉妒 ----------------
    2: [
        ("""\
# 沉锚 —— 锚落处涌起漩涡，把人拖向锚心。
playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle bubble_column_up ~ ~0.5 ~ 2 0.5 2 0.4 80
particle dust{color:[0.11,0.31,0.45],scale:3} ~ ~1 ~ 2 1 2 0.05 60
execute as %(P8)s at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^1.2
execute as %(P8)s run damage @s 5 minecraft:magic %(BY)s
""", {}),

        ("""\
# 溺没 —— 深海的规矩：在这儿，你不会呼吸。
playsound minecraft:entity.drowned.ambient_water hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle bubble ~ ~1 ~ 3 1.2 3 0.2 120
execute as %(P8)s run function rpg:taint/sk2b_drown
""", {"sk2b_drown": """\
effect give @s minecraft:slowness 6 2 true
effect give @s minecraft:mining_fatigue 6 2 true
damage @s 4 minecraft:drown %(BY)s
"""}),

        ("""\
# 嫉羡 —— 你身上那些好东西，他也想要。
playsound minecraft:entity.elder_guardian.hurt hostile @a[distance=..32] ~ ~ ~ 1 1.2
particle witch ~ ~1 ~ 3 1 3 0.3 80
execute as %(P8)s run function rpg:taint/sk2c_envy
""", {"sk2c_envy": """\
# 把你身上的增益全部抹掉 —— 他见不得你比他好。
effect clear @s minecraft:strength
effect clear @s minecraft:speed
effect clear @s minecraft:resistance
effect clear @s minecraft:regeneration
effect clear @s minecraft:absorption
effect clear @s minecraft:fire_resistance
damage @s 3 minecraft:magic %(BY)s
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:speed 6 1 true
"""}),

        ("""\
# 逆潮 —— 近者被推离，远者被卷近，所有距离都由他重写。
playsound minecraft:entity.generic.splash hostile @a[distance=..32] ~ ~ ~ 1.2 0.65
playsound minecraft:block.conduit.attack.target hostile @a[distance=..32] ~ ~ ~ 0.8 0.7
particle nautilus ~ ~1 ~ 4 1.2 4 0.12 96
particle bubble_column_up ~ ~0.4 ~ 4 0.5 4 0.35 110
execute as @a[distance=..4,gamemode=!spectator,gamemode=!creative] at @s run function rpg:taint/sk2d_out
execute as @a[distance=4.01..10,gamemode=!spectator,gamemode=!creative] at @s run function rpg:taint/sk2d_in
""", {"sk2d_out": """\
execute facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^-2.4
damage @s 4 minecraft:drown %(BY)s
""", "sk2d_in": """\
execute facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^2.4
damage @s 4 minecraft:drown %(BY)s
"""}),

        ("""\
# 海渊重压 —— 不需要海水，深度本身压在骨头上。
playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..32] ~ ~ ~ 1 0.42
particle bubble_pop ~ ~1 ~ 4 1.4 4 0.18 120
particle dust_color_transition{from_color:[0.24,0.66,0.91],to_color:[0.02,0.09,0.18],scale:2.5} ~ ~1 ~ 4 1 4 0.04 72
execute as %(P10)s run function rpg:taint/sk2e_pressure
""", {"sk2e_pressure": """\
effect give @s minecraft:slowness 6 3 true
effect give @s minecraft:mining_fatigue 6 2 true
damage @s 7 minecraft:drown %(BY)s
"""}),
    ],

    # ---------------- 亚巴顿 · 怠惰 ----------------
    3: [
        ("""\
# 收割 —— 周身爆发，每收一个回一颗心。
playsound minecraft:entity.wither.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle sculk_charge_pop ~ ~1 ~ 3 1 3 0.1 90
execute as %(P6)s run function rpg:taint/sk3_reap
""", {"sk3_reap": """\
damage @s 7 minecraft:magic %(BY)s
particle soul ~ ~1 ~ 0.3 0.5 0.3 0.05 20
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
"""}),

        ("""\
# 沉眠 —— 怠惰不杀你，它只让你抬不起手。
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle sculk_soul ~ ~1 ~ 3 1 3 0.05 70
execute as %(P7)s run function rpg:taint/sk3b_sleep
""", {"sk3b_sleep": """\
effect give @s minecraft:slowness 8 3 true
effect give @s minecraft:mining_fatigue 8 2 true
effect give @s minecraft:weakness 8 1 true
damage @s 2 minecraft:magic %(BY)s
"""}),

        ("""\
# 深渊之口 —— 地底下那张嘴张开了。
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..32] ~ ~ ~ 1 0.8
particle sonic_boom ~ ~1 ~ 0 0 0 0 3
particle sculk_charge_pop ~ ~0.2 ~ 4 0.3 4 0.2 120
execute as %(P8)s at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^2
execute as %(P8)s run function rpg:taint/sk3c_maw
""", {"sk3c_maw": """\
effect give @s minecraft:wither 6 1 true
damage @s 6 minecraft:magic %(BY)s
"""}),

        ("""\
# 停摆 —— 不眠之钟的反面，连一刻都不再向前。
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..32] ~ ~ ~ 1 0.35
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..32] ~ ~ ~ 1 0.42
particle sculk_soul ~ ~1 ~ 4 1 4 0.04 82
particle dust{color:[0.58,0.58,0.61],scale:2.2} ~ ~1 ~ 4 1 4 0.04 64
execute as %(P10)s run function rpg:taint/sk3d_still
""", {"sk3d_still": """\
effect give @s minecraft:slowness 3 255 true
effect give @s minecraft:weakness 6 2 true
damage @s 4 minecraft:magic %(BY)s
"""}),

        ("""\
# 死寂 —— 无底坑吞掉声音，也吞掉继续抵抗的力气。
playsound minecraft:entity.warden.roar hostile @a[distance=..32] ~ ~ ~ 0.7 0.45
particle soul ~ ~1 ~ 4 1.4 4 0.06 92
particle reverse_portal ~ ~1 ~ 4 1 4 0.18 78
execute as %(P8)s run function rpg:taint/sk3e_silence
""", {"sk3e_silence": """\
effect give @s minecraft:darkness 6 0 true
effect give @s minecraft:mining_fatigue 8 3 true
effect give @s minecraft:wither 5 0 true
damage @s 5 minecraft:magic %(BY)s
"""}),
    ],

    # ---------------- 别西卜 · 暴食 ----------------
    4: [
        ("""\
# 余烬 —— 前方喷灰，吸进去的人饿得站不住。
playsound minecraft:entity.blaze.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.5
execute at @s anchored eyes facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run function rpg:taint/sk4_cone
""", {"sk4_cone": "\n".join(
            "execute positioned ^ ^ ^%d run particle ash ~ ~ ~ 1 1 1 0.1 40\n"
            "execute positioned ^ ^ ^%d run particle lava ~ ~ ~ 0.6 0.6 0.6 0 6\n"
            "execute positioned ^ ^ ^%d as @a[distance=..3,gamemode=!spectator,"
            "gamemode=!creative] run function rpg:taint/sk4_hit" % (d, d, d)
            for d in range(1, 7))}),

        ("""\
# 吞噬 —— 他吃的是你那一顿。
playsound minecraft:entity.generic.eat hostile @a[distance=..32] ~ ~ ~ 1 0.6
playsound minecraft:entity.player.burp hostile @a[distance=..24] ~ ~ ~ 1 0.7
particle item_slime ~ ~1 ~ 2 1 2 0.2 60
execute as %(P7)s run function rpg:taint/sk4b_devour
""", {"sk4b_devour": """\
effect give @s minecraft:hunger 14 3 true
effect give @s minecraft:weakness 8 1 true
damage @s 4 minecraft:magic %(BY)s
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 1 true
"""}),

        ("""\
# 蝇群 —— 苍蝇王名副其实。
playsound minecraft:entity.bee.loop_aggressive hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle mycelium ~ ~1 ~ 2 1 2 0.3 80
execute at @s run function rpg:taint/sk4c_swarm
""", {"sk4c_swarm": "\n".join(
            ['summon minecraft:vex ~ ~1 ~ {life_ticks:400,Tags:["rpg.demon.fly"],'
             'CustomName:[{"text":"蝇","color":"#5A6B1E"}],Health:10f,'
              'attributes:[{id:"max_health",base:10f},{id:"attack_damage",base:4f}]}'] * 3)}),

        ("""\
# 腐宴 —— 宴席先腐烂，宾客才知道自己已经坐在盘中。
playsound minecraft:entity.generic.eat hostile @a[distance=..32] ~ ~ ~ 1 0.45
playsound minecraft:block.composter.fill_success hostile @a[distance=..28] ~ ~ ~ 1 0.55
particle spore_blossom_air ~ ~1.4 ~ 4 1.5 4 0.08 105
particle mycelium ~ ~0.8 ~ 4 1 4 0.16 92
execute as %(P8)s run function rpg:taint/sk4d_feast
""", {"sk4d_feast": """\
effect give @s minecraft:hunger 12 4 true
effect give @s minecraft:nausea 7 0 true
effect give @s minecraft:poison 6 1 true
damage @s 4 minecraft:magic %(BY)s
"""}),

        ("""\
# 饥啮 —— 万千张口只追最近的一份血肉。
playsound minecraft:entity.fox.bite hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle ash ~ ~1 ~ 2.5 1 2.5 0.14 84
particle damage_indicator ~ ~1 ~ 2 0.8 2 0.08 36
execute as @a[distance=..10,limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk4e_bite
""", {"sk4e_bite": """\
effect give @s minecraft:hunger 10 3 true
damage @s 11 minecraft:magic %(BY)s
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 1 true
"""}),
    ],

    # ---------------- 萨麦尔 · 暴怒 ----------------
    5: [
        ("""\
# 毒雾 —— 剧毒与凋零并存。
playsound minecraft:entity.witch.throw hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle dust_color_transition{from_color:[0.69,0.0,0.34],to_color:[0.24,0.0,0.12],scale:3} ~ ~1 ~ 3 1.2 3 0.06 100
execute as %(P7)s run function rpg:taint/sk5_hit
""", {"sk5_hit": """\
effect give @s minecraft:poison 10 1 true
effect give @s minecraft:wither 6 0 true
damage @s 3 minecraft:magic %(BY)s
"""}),

        ("""\
# 怒斩 —— 暴怒不讲章法，它只是冲上来。
playsound minecraft:entity.ravager.roar hostile @a[distance=..32] ~ ~ ~ 1 1.2
particle crit ~ ~1 ~ 1 1 1 0.4 60
execute at @s facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run tp @s ^ ^ ^4
execute as %(P6)s run function rpg:taint/sk5b_slash
""", {"sk5b_slash": """\
damage @s 9 minecraft:magic %(BY)s
effect give @s minecraft:poison 8 1 true
particle sweep_attack ~ ~1 ~ 0.4 0.4 0.4 0 4
"""}),

        ("""\
# 死亡低语 —— 死亡天使开口，不必碰到你。
playsound minecraft:entity.wither.spawn hostile @a[distance=..32] ~ ~ ~ 0.8 1.6
particle soul_fire_flame ~ ~1 ~ 3 1 3 0.05 80
execute as %(P8)s run function rpg:taint/sk5c_whisper
""", {"sk5c_whisper": """\
damage @s 5 minecraft:magic %(BY)s
effect give @s minecraft:wither 10 2 true
"""}),

        ("""\
# 血猎 —— 他循着最近的血气突入，不给伤者喘息。
playsound minecraft:entity.vex.charge hostile @a[distance=..32] ~ ~ ~ 1 0.55
playsound minecraft:entity.ravager.roar hostile @a[distance=..32] ~ ~ ~ 0.8 1.15
particle dust_color_transition{from_color:[0.89,0.30,0.30],to_color:[0.24,0.0,0.04],scale:2.6} ~ ~1 ~ 3 1 3 0.06 92
execute at @s facing entity @a[distance=..12,limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run tp @s ^ ^ ^5
execute as %(P5)s run function rpg:taint/sk5d_hunt
""", {"sk5d_hunt": """\
effect give @s minecraft:glowing 6 0 true
effect give @s minecraft:poison 7 1 true
damage @s 8 minecraft:magic %(BY)s
"""}),

        ("""\
# 怒潮 —— 暴怒从中心炸开，把所有人赶出他的呼吸。
playsound minecraft:item.mace.smash_ground_heavy hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle sweep_attack ~ ~1 ~ 3 1 3 0 26
particle crit ~ ~1 ~ 4 1 4 0.22 96
particle dust{color:[0.89,0.30,0.30],scale:2.4} ~ ~1 ~ 4 1 4 0.05 72
execute as %(P8)s at @s run function rpg:taint/sk5e_surge
""", {"sk5e_surge": """\
execute facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^-2.8
effect give @s minecraft:poison 6 1 true
damage @s 7 minecraft:magic %(BY)s
"""}),
    ],

    # ---------------- 贝利尔 · 色欲 ----------------
    6: [
        ("""\
# 朝拜 —— 七格之内，全都得低头。
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle dust_color_transition{from_color:[0.4,0.0,0.6],to_color:[0.0,0.0,0.0],scale:2} ~ ~1 ~ 3 1.2 3 0.06 90
execute as %(P7)s run function rpg:taint/sk6_kneel
""", {"sk6_kneel": """\
effect give @s minecraft:slowness 3 3 true
effect give @s minecraft:weakness 3 1 true
effect give @s minecraft:mining_fatigue 3 1 true
damage @s 4 minecraft:magic %(BY)s
"""}),

        ("""\
# 迷乱 —— 你分不清哪边是他。
playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle portal ~ ~1 ~ 3 1 3 0.6 120
execute as %(P8)s run function rpg:taint/sk6b_daze
""", {"sk6b_daze": """\
effect give @s minecraft:nausea 8 0 true
effect give @s minecraft:levitation 1 0 true
damage @s 3 minecraft:magic %(BY)s
"""}),

        ("""\
# 献身 —— 他要的从来不是你的命，是你的血。
playsound minecraft:entity.vex.charge hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle dust{color:[0.36,0.17,0.44],scale:2} ~ ~1 ~ 3 1 3 0.1 90
execute as %(P7)s run function rpg:taint/sk6c_drain
""", {"sk6c_drain": """\
damage @s 6 minecraft:magic %(BY)s
particle damage_indicator ~ ~1 ~ 0.3 0.3 0.3 0.1 10
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 1 true
"""}),

        ("""\
# 顾盼 —— 一个眼神就把所有人的视线强行转向王座。
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..32] ~ ~ ~ 1 0.65
particle witch ~ ~1.4 ~ 4 1.4 4 0.18 105
particle dust_color_transition{from_color:[0.75,0.42,0.91],to_color:[0.12,0.0,0.18],scale:2.4} ~ ~1 ~ 4 1 4 0.05 72
execute as %(P8)s run function rpg:taint/sk6d_gaze
""", {"sk6d_gaze": """\
tp @s ~ ~ ~ facing entity @e[tag=rpg.dm.cast,limit=1] eyes
effect give @s minecraft:nausea 6 0 true
effect give @s minecraft:weakness 5 1 true
damage @s 3 minecraft:magic %(BY)s
"""}),

        ("""\
# 欲障 —— 紫幕落下，真实与渴望只剩一层薄纱。
playsound minecraft:block.respawn_anchor.ambient hostile @a[distance=..32] ~ ~ ~ 1 0.55
particle portal ~ ~1 ~ 4 1.5 4 0.55 120
particle reverse_portal ~ ~1 ~ 3.5 1.2 3.5 0.25 84
execute as %(P10)s run function rpg:taint/sk6e_veil
""", {"sk6e_veil": """\
effect give @s minecraft:darkness 6 0 true
effect give @s minecraft:slowness 6 2 true
effect give @s minecraft:glowing 6 0 true
damage @s 5 minecraft:magic %(BY)s
"""}),
    ],

    # ---------------- 玛门 · 贪婪 ----------------
    7: [
        ("""\
# 点金 —— 他不打你，他从你身上抽。
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..32] ~ ~ ~ 1 1.4
particle wax_on ~ ~1 ~ 3 1 3 0.1 80
particle end_rod ~ ~1 ~ 2 1 2 0.05 40
execute as %(P8)s run function rpg:taint/sk7_take
""", {"sk7_take": """\
xp add @s -20 points
damage @s 3 minecraft:magic %(BY)s
particle wax_on ~ ~1 ~ 0.3 0.5 0.3 0.05 16
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
"""}),

        ("""\
# 夺财 —— 掉在地上的也是他的。
playsound minecraft:entity.item.pickup hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle wax_off ~ ~1 ~ 4 1 4 0.2 100
execute at @s as @e[type=minecraft:item,distance=..10] run function rpg:taint/sk7b_seize
execute as %(P8)s run damage @s 3 minecraft:magic %(BY)s
""", {"sk7b_seize": """\
# 周围的掉落物直接被吞掉，连带给他补一口。
particle wax_on ~ ~0.3 ~ 0.2 0.2 0.2 0.05 8
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
kill @s
"""}),

        ("""\
# 重金一击 —— 一次结清。
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..32] ~ ~ ~ 1 0.7
playsound minecraft:entity.player.levelup hostile @a[distance=..24] ~ ~ ~ 0.8 0.6
particle flash{color:16777200} ~ ~1 ~ 0 0 0 0 1
particle end_rod ~ ~1 ~ 1 1 1 0.4 60
execute as @a[distance=..5,limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk7c_settle
""", {"sk7c_settle": """\
damage @s 12 minecraft:magic %(BY)s
xp add @s -40 points
"""}),

        ("""\
# 复利 —— 每一息都在增长的账，最后从经验与血里一起扣。
playsound minecraft:block.vault.reject_rewarded_player hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle wax_on ~ ~1 ~ 4 1 4 0.12 92
particle trial_omen ~ ~1 ~ 3 1 3 0.08 64
execute as %(P10)s run function rpg:taint/sk7d_interest
""", {"sk7d_interest": """\
xp add @s -15 points
effect give @s minecraft:weakness 6 1 true
damage @s 6 minecraft:magic %(BY)s
"""}),

        ("""\
# 金牢 —— 黄金不是奖赏，是把脚钉在账本上的铆钉。
playsound minecraft:block.anvil.land hostile @a[distance=..32] ~ ~ ~ 0.8 1.35
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..32] ~ ~ ~ 1 0.75
particle end_rod ~ ~1 ~ 3 1 3 0.08 72
particle wax_on ~ ~0.5 ~ 3 0.5 3 0.12 88
execute as %(P7)s run function rpg:taint/sk7e_prison
""", {"sk7e_prison": """\
effect give @s minecraft:slowness 3 255 true
effect give @s minecraft:glowing 6 0 true
damage @s 5 minecraft:magic %(BY)s
"""}),
    ],
}


# 恶魔战斗提示不借用 Minecraft 的 16 色名：七柱本色有些很暗，直接拿来
# 写聊天提示也不能直接用近黑本色，所以这里保留相同色相，单独给出可读的
# 亮色、柔色和高光。提示走双层 Actionbar 的上层，下层战斗状态仍可同时显示。
DEMON_UI = {
    1: dict(who="路西法", main="#31D97C", soft="#A9F5CE", glint="#E8FFF3",
            skills=[("原罪", "蛇矛破土"), ("蛇矛", "贯穿罪痕"), ("高踞", "众生俯首"),
                    ("失坠", "荣耀折翼"), ("王座回绝", "近身者皆退")],
            ultimate="万蛇加冕", ult_text="傲慢者立于万蛇之上"),
    2: dict(who="利维坦", main="#3DA9E8", soft="#A9DDF5", glint="#E8F8FF",
            skills=[("沉锚", "深潮回卷"), ("溺没", "剥夺呼吸"), ("嫉羡", "恩赐尽褫"),
                    ("逆潮", "远近皆失其位"), ("海渊重压", "深度压骨")],
            ultimate="妒海沉城", ult_text="深海正拖拽整片陆地"),
    3: dict(who="亚巴顿", main="#92929B", soft="#D1D1D8", glint="#F0F0F4",
            skills=[("收割", "灵魂归仓"), ("沉眠", "四肢封缄"), ("深渊之口", "地脉噬人"),
                    ("停摆", "此刻不再前行"), ("死寂", "无底坑吞声")],
            ultimate="终末收割", ult_text="所有灵魂都将归于静止"),
    4: dict(who="别西卜", main="#B7C84B", soft="#E4EA9B", glint="#FFF6C7",
            skills=[("余烬", "灰烬噬肺"), ("吞噬", "血肉为宴"), ("蝇群", "饥群出巢"),
                    ("腐宴", "宾客皆在盘中"), ("饥啮", "万口追血肉")],
            ultimate="万蝇饕宴", ult_text="饥饿张开了千万张口"),
    5: dict(who="萨麦尔", main="#E44D4D", soft="#FF9B83", glint="#FFE0D5",
            skills=[("毒雾", "腐血漫延"), ("怒斩", "暴怒近身"), ("死亡低语", "终声索命"),
                    ("血猎", "循伤者而至"), ("怒潮", "赤环逐众")],
            ultimate="血怒天罚", ult_text="死亡天使循血而至"),
    6: dict(who="贝利尔", main="#C06BE8", soft="#E0A9F5", glint="#FFE8FA",
            skills=[("朝拜", "众生低首"), ("迷乱", "感官倒悬"), ("献身", "献血予王"),
                    ("顾盼", "万目归于王座"), ("欲障", "紫幕覆真形")],
            ultimate="紫宴朝圣", ult_text="你的意志正在向他跪下"),
    7: dict(who="玛门", main="#E2B93B", soft="#FFE08A", glint="#FFF5C7",
            skills=[("点金", "性命折价"), ("夺财", "万物归库"), ("重金一击", "一次结清"),
                    ("复利", "血与经验同偿"), ("金牢", "黄金钉足")],
            ultimate="黄金终审", ult_text="灵魂与财富一并结算"),
}

NONE_UI = dict(who="无名者", main="#D23B47", soft="#AAA5AE", glint="#ECE9EF",
               skills=[("蚀界", "名字也会被黑暗吞掉")],
               ultimate="无名蚀界", ult_text="黑暗正抹去一切称谓")


def combat_notices():
    """固定顺序的恶魔提示；数据包编号与资源包私用字符共用这一份。"""
    out = []
    for n in range(1, 8):
        ui = DEMON_UI[n]
        for name, phrase in ui["skills"]:
            out.append({"key": (ui["who"], name, phrase, False),
                        "ui": ui, "name": name, "phrase": phrase,
                        "ultimate": False})
    name, phrase = NONE_UI["skills"][0]
    out.append({"key": (NONE_UI["who"], name, phrase, False),
                "ui": NONE_UI, "name": name, "phrase": phrase,
                "ultimate": False})
    for n in range(1, 8):
        ui = DEMON_UI[n]
        out.append({"key": (ui["who"], ui["ultimate"], ui["ult_text"], True),
                    "ui": ui, "name": ui["ultimate"],
                    "phrase": ui["ult_text"], "ultimate": True})
    out.append({"key": (NONE_UI["who"], NONE_UI["ultimate"],
                         NONE_UI["ult_text"], True),
                "ui": NONE_UI, "name": NONE_UI["ultimate"],
                "phrase": NONE_UI["ult_text"], "ultimate": True})
    assert len(out) == 44
    return out


def notice_text(q):
    """资源包烘字用的三段纯文本；颜色仍读同一份 ui 三色。"""
    head = "[%s%s]" % (q["ui"]["who"], " · 罪约" if q["ultimate"] else "")
    return (head, "　%s · %s" % (q["name"], q["phrase"]),
            " ◆" if q["ultimate"] else " ✦")


def _notice(ui, name, phrase, ultimate=False, radius=14):
    """把提示号写进独立上层槽；中央 HUD 把它叠在 Actionbar 状态行上方。"""
    key = (ui["who"], name, phrase, bool(ultimate))
    keys = [q["key"] for q in combat_notices()]
    if key not in keys:
        raise AssertionError("unregistered demon notice: %r" % (key,))
    number = keys.index(key) + 1
    return ("execute at @s as @a[distance=..%d,gamemode=!spectator,gamemode=!creative] "
            "run function rpg:hud/demon/m%d" % (radius, number))


def build_demon_hud():
    """生成双层 Actionbar 的消息槽、合成分流与固定提示渲染器。"""
    notices = combat_notices()
    render = ["# 上层恶魔提示 + 下层持久状态，同一 Actionbar 合成。"]
    solo = ["# 没有下层状态时，上层提示自己居中。"]
    for i, _q in enumerate(notices, 1):
        wf("hud/demon/m%d.mcfunction" % i,
           "scoreboard players set @s rpg_hud_dm %d\n"
           "scoreboard players set @s rpg_hud_dmt 50" % i)
        render.append("execute if entity @s[scores={rpg_hud_dm=%d}] "
                      "run return run function rpg:hud/demon/r%d with storage rpg:hud" %
                      (i, i))
        solo.append("execute if entity @s[scores={rpg_hud_dm=%d}] "
                    "run return run function rpg:hud/demon/s%d" % (i, i))

        # F000/F1xx/F2xx are outside vanilla 1.21.11 Unifont PUA's occupied
        # glyphs; E4xx/E5xx/E6xx otherwise render vanilla symbols/tofu first.
        top = chr(0xF000 + i - 1) + chr(0xF040 + i - 1)
        back = chr(0xF100 + i - 1)
        forward = chr(0xF200 + i - 1)
        top_comp = json.dumps({"text": top, "font": "rpg:combat_prompt",
                               "italic": False, "color": "white"},
                              ensure_ascii=True, separators=(",", ":"))
        back_comp = json.dumps({"text": back, "font": "rpg:combat_prompt"},
                               ensure_ascii=True, separators=(",", ":"))
        fwd_comp = json.dumps({"text": forward, "font": "rpg:combat_prompt"},
                              ensure_ascii=True, separators=(",", ":"))
        wf("hud/demon/r%d.mcfunction" % i,
           "$title @s actionbar [\"\",%s,%s,$(a),$(b),$(c)]" %
           (top_comp, back_comp))
        wf("hud/demon/s%d.mcfunction" % i,
           "title @s actionbar [\"\",%s,%s,%s]" %
           (top_comp, back_comp, fwd_comp))
    wf("hud/demon/render.mcfunction", "\n".join(render))
    wf("hud/demon/solo.mcfunction", "\n".join(solo))
    return len(notices)


# 每位恶魔的罪约只做实体伤害、状态、传送与表现，不召唤爆炸物、不修改地形。
# hit 段走 wf_holy，持圣器者会继承现有的缩短/削弱规则。
ULTIMATES = {
    1: ("""# 万蛇加冕 —— 三圈蛇牙从王冠下同时破土。
data modify storage rpg:demon uuid set from entity @s UUID
function rpg:taint/ult1_fangs with storage rpg:demon
particle dust_color_transition{from_color:[0.19,0.85,0.49],to_color:[0.0,0.18,0.07],scale:3} ~ ~1 ~ 5 1 5 0.04 150 force
particle end_rod ~ ~2 ~ 2.5 1.5 2.5 0.05 75 force
particle flash{color:3266940} ~ ~2 ~ 0 0 0 0 1 force
particle dragon_breath ~ ~1 ~ 4 1 4 0.08 110 force
particle enchanted_hit ~ ~1 ~ 4 1 4 0.12 90 force
playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..32] ~ ~ ~ 1.2 0.55
playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..40] ~ ~ ~ 0.8 0.7
execute as %(P10)s run function rpg:taint/ult1_hit
""", """effect give @s minecraft:levitation 2 1 true
damage @s 18 minecraft:magic %(BY)s
"""),
    2: ("""# 妒海沉城 —— 深潮将十二格内的一切拖向海眼。
particle bubble_column_up ~ ~0.5 ~ 5 1 5 0.55 220 force
particle dust_color_transition{from_color:[0.24,0.66,0.91],to_color:[0.02,0.09,0.18],scale:3} ~ ~1 ~ 5 1 5 0.05 150 force
particle flash{color:4041192} ~ ~1 ~ 0 0 0 0 1 force
particle nautilus ~ ~1 ~ 5 1.5 5 0.14 120 force
particle splash ~ ~0.7 ~ 5 1 5 0.25 160 force
playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..36] ~ ~ ~ 1.25 0.45
playsound minecraft:entity.generic.splash hostile @a[distance=..36] ~ ~ ~ 1.4 0.55
execute as %(P12)s run function rpg:taint/ult2_hit
""", """execute at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^3
effect give @s minecraft:slowness 8 3 true
effect give @s minecraft:mining_fatigue 8 2 true
damage @s 17 minecraft:drown %(BY)s
"""),
    3: ("""# 终末收割 —— 灵魂被一并割下，每一枚都反哺收割者。
particle sculk_charge_pop ~ ~1 ~ 5 1 5 0.14 180 force
particle soul ~ ~1 ~ 4 1.5 4 0.08 130 force
particle sonic_boom ~ ~1 ~ 0 0 0 0 4 force
particle flash{color:9605787} ~ ~1 ~ 0 0 0 0 1 force
particle reverse_portal ~ ~1 ~ 4 1.5 4 0.3 130 force
particle soul_fire_flame ~ ~1 ~ 4 1 4 0.08 95 force
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..36] ~ ~ ~ 1.1 0.65
playsound minecraft:entity.wither.spawn hostile @a[distance=..40] ~ ~ ~ 0.7 0.55
execute as %(P10)s run function rpg:taint/ult3_hit
""", """effect give @s minecraft:wither 8 1 true
damage @s 20 minecraft:magic %(BY)s
particle soul ~ ~1 ~ 0.35 0.5 0.35 0.06 24 force
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
"""),
    4: ("""# 万蝇饕宴 —— 灰烬遮天，饥群从宴席中孵化。
particle ash ~ ~1 ~ 5 2 5 0.15 240 force
particle mycelium ~ ~1 ~ 4 1.5 4 0.18 170 force
particle dust_color_transition{from_color:[0.72,0.78,0.29],to_color:[0.14,0.17,0.03],scale:2.6} ~ ~1 ~ 4 1 4 0.05 130 force
particle flash{color:12044363} ~ ~1 ~ 0 0 0 0 1 force
particle large_smoke ~ ~1 ~ 5 1.5 5 0.14 150 force
particle spore_blossom_air ~ ~2 ~ 5 2 5 0.08 120 force
playsound minecraft:entity.bee.loop_aggressive hostile @a[distance=..36] ~ ~ ~ 1.25 0.45
playsound minecraft:entity.ravager.roar hostile @a[distance=..40] ~ ~ ~ 0.65 0.55
function rpg:taint/ult4_swarm
execute as %(P10)s run function rpg:taint/ult4_hit
""", """effect give @s minecraft:hunger 14 4 true
effect give @s minecraft:weakness 8 1 true
damage @s 18 minecraft:magic %(BY)s
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
"""),
    5: ("""# 血怒天罚 —— 死亡天使沿最近的血气突入人群。
execute at @s facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run tp @s ^ ^ ^5
particle flash{color:15158613} ~ ~1 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.89,0.30,0.30],to_color:[0.24,0.0,0.04],scale:3} ~ ~1 ~ 4 1.2 4 0.06 180 force
particle sweep_attack ~ ~1 ~ 3 0.8 3 0 34 force
particle trial_omen ~ ~1 ~ 4 1 4 0.1 110 force
particle crit ~ ~1 ~ 4 1 4 0.22 130 force
playsound minecraft:entity.ravager.roar hostile @a[distance=..36] ~ ~ ~ 1.2 0.8
playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..40] ~ ~ ~ 0.8 1.15
execute as %(P8)s run function rpg:taint/ult5_hit
""", """effect give @s minecraft:poison 10 2 true
effect give @s minecraft:wither 7 1 true
damage @s 22 minecraft:magic %(BY)s
"""),
    6: ("""# 紫宴朝圣 —— 意志被拖向宴席中央，再献出自己的血。
particle portal ~ ~1 ~ 5 1.5 5 0.65 240 force
particle dust_color_transition{from_color:[0.75,0.42,0.91],to_color:[0.12,0.0,0.18],scale:3} ~ ~1 ~ 4 1 4 0.06 150 force
particle flash{color:12610536} ~ ~1 ~ 0 0 0 0 1 force
particle witch ~ ~1 ~ 5 1.5 5 0.18 150 force
particle reverse_portal ~ ~1 ~ 4 1 4 0.28 120 force
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..36] ~ ~ ~ 1.2 0.5
playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..36] ~ ~ ~ 1.1 0.55
execute as %(P10)s run function rpg:taint/ult6_hit
""", """execute at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^2.5
effect give @s minecraft:slowness 7 4 true
effect give @s minecraft:weakness 7 2 true
effect give @s minecraft:nausea 8 0 true
damage @s 17 minecraft:magic %(BY)s
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
"""),
    7: ("""# 黄金终审 —— 场上的财富、经验与性命在同一刻结算。
particle wax_on ~ ~1 ~ 5 1.5 5 0.16 210 force
particle end_rod ~ ~1 ~ 4 1 4 0.08 130 force
particle flash{color:16765754} ~ ~1 ~ 0 0 0 0 1 force
particle firework ~ ~1 ~ 5 1.5 5 0.18 160 force
particle totem_of_undying ~ ~1 ~ 4 1 4 0.16 120 force
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..36] ~ ~ ~ 1.2 0.55
playsound minecraft:entity.player.levelup hostile @a[distance=..36] ~ ~ ~ 1.1 0.45
execute at @s as @e[type=minecraft:item,distance=..12] at @s run function rpg:taint/ult7_seize
execute as %(P10)s run function rpg:taint/ult7_hit
""", """xp add @s -80 points
effect give @s minecraft:slowness 5 2 true
damage @s 24 minecraft:magic %(BY)s
"""),
}

ULT_NONE = ("""# 无名蚀界 —— 无名者没有柱位，只把周围的一切称谓抹黑。
particle squid_ink ~ ~1 ~ 5 1.5 5 0.18 210 force
particle sculk_soul ~ ~1 ~ 4 1 4 0.09 120 force
particle dust_color_transition{from_color:[0.82,0.23,0.28],to_color:[0.0,0.0,0.0],scale:3} ~ ~1 ~ 4 1 4 0.05 130 force
particle flash{color:13777735} ~ ~1 ~ 0 0 0 0 1 force
particle trial_omen ~ ~1 ~ 4 1 4 0.1 100 force
particle reverse_portal ~ ~1 ~ 4 1.5 4 0.3 130 force
playsound minecraft:entity.warden.roar hostile @a[distance=..36] ~ ~ ~ 1.1 0.55
playsound minecraft:entity.wither.spawn hostile @a[distance=..40] ~ ~ ~ 0.7 0.45
execute as %(P10)s run function rpg:taint/ult0_hit
""", """effect give @s minecraft:darkness 8 0 true
effect give @s minecraft:blindness 4 0 true
effect give @s minecraft:wither 7 1 true
damage @s 18 minecraft:magic %(BY)s
""")


def _rgb(hex_colour):
    h = hex_colour.lstrip("#")
    return ",".join("%.2f" % (int(h[i:i + 2], 16) / 255.0) for i in (0, 2, 4))


def wire_lords():
    """降临的分流。add_exorcism 只写得出无名者 —— 它不认识柱位。"""
    # fallback 必须从固定模板重建。若读取上一次生成的 lord/skill 再把非注释行
    # 当 fallback，单独重跑 add_pact 会把七条分流吞进去并再追加一遍，文件每次
    # 增长七条；完整 build 因 add_exorcism 先覆盖而碰巧藏住了这个幂等缺陷。
    none_src = ex.LORD_NONE % {
        "NBT": ex.demon_nbt("无名者", "#3D0000", "dark_gray")}
    branch = []
    none = "\n".join(l for l in none_src.split("\n")
                     if l and not l.startswith("#"))
    sk = []
    ult_warn, ult_charge, ult_cast = [], [], []
    subs = {"BY": BY, "P5": PLAYERS % 5, "P6": PLAYERS % 6, "P7": PLAYERS % 7,
            "P8": PLAYERS % 8, "P10": PLAYERS % 10, "P12": PLAYERS % 12}
    charge_fx = {
        1: "particle end_rod ~ ~2 ~ 0.45 0.7 0.45 0.02 3 force",
        2: "particle bubble_column_up ~ ~0.4 ~ 0.6 0.2 0.6 0.16 5 force",
        3: "particle soul ~ ~1 ~ 0.55 0.7 0.55 0.03 4 force",
        4: "particle mycelium ~ ~1 ~ 0.65 0.65 0.65 0.08 5 force",
        5: "particle damage_indicator ~ ~1 ~ 0.55 0.65 0.55 0.04 4 force",
        6: "particle portal ~ ~1 ~ 0.65 0.7 0.65 0.18 5 force",
        7: "particle wax_on ~ ~1 ~ 0.6 0.7 0.6 0.04 4 force",
    }
    for p in PILLARS:
        ui = DEMON_UI[p["n"]]
        branch.append("execute if score #lord rpg_fall matches %d "
                      "run return run function rpg:taint/lord%d" % (p["n"], p["n"]))
        wf("taint/lord%d.mcfunction" % p["n"], LORD_ONE % {
            "WHO": p["who"], "RGB": _rgb(p["colour"]), "N": p["n"],
            "NBT": ex.demon_nbt(p["who"], p["colour"], p["lit"])})

        # 他那五招。skN 只负责掷点，真正的招式在 skN_1..5。
        sk.append("execute if entity @s[scores={rpg_dm_lord=%d}] "
                  "run return run function rpg:taint/sk%d" % (p["n"], p["n"]))
        pick = ["# 五招掷一招，并记住上一招；若撞号则顺延一格，避免连续重复。",
                "execute store result score #pick rpg_fall run random value 1..%d"
                % len(SKILLS[p["n"]]),
                "execute if score #pick rpg_fall = @s rpg_dm_last run scoreboard players add #pick rpg_fall 1",
                "execute if score #pick rpg_fall matches %d.. run scoreboard players set #pick rpg_fall 1"
                % (len(SKILLS[p["n"]]) + 1),
                "scoreboard players operation @s rpg_dm_last = #pick rpg_fall"]
        for i, (body, extra) in enumerate(SKILLS[p["n"]], 1):
            pick.append("execute if score #pick rpg_fall matches %d "
                        "run return run function rpg:taint/sk%d_%d"
                        % (i, p["n"], i))
            skill_name, skill_text = ui["skills"][i - 1]
            wf("taint/sk%d_%d.mcfunction" % (p["n"], i),
               _notice(ui, skill_name, skill_text) + "\n" + body % subs)
            for name, text in extra.items():
                # 走 wf_holy：带 debuff 的会自动派生"对方有圣器"的那一版
                ex.wf_holy("taint/%s.mcfunction" % name, text % subs)
        wf("taint/sk%d.mcfunction" % p["n"], "\n".join(pick))

        # 罪约三路分流：warn 只出现一次，charge 每刻只画少量聚拢粒子，
        # ultimate 才结算伤害。全部按实体自己的 lord 分数判断。
        ult_warn.append("execute if entity @s[scores={rpg_dm_lord=%d}] "
                        "run return run function rpg:taint/ult%d_warn" %
                        (p["n"], p["n"]))
        ult_charge.append("execute if entity @s[scores={rpg_dm_lord=%d}] "
                          "run return run function rpg:taint/ult%d_charge" %
                          (p["n"], p["n"]))
        ult_cast.append("execute if entity @s[scores={rpg_dm_lord=%d}] "
                        "run return run function rpg:taint/ult%d" %
                        (p["n"], p["n"]))
        rgb = _rgb(ui["main"])
        flash = int(ui["main"].lstrip("#"), 16)
        wf("taint/ult%d_warn.mcfunction" % p["n"],
           _notice(ui, ui["ultimate"], ui["ult_text"], True, 18) + "\n" +
           "particle dust{color:[%s],scale:2.6} ~ ~1 ~ 1.4 1 1.4 0.04 42 force\n" % rgb +
           "playsound minecraft:block.trial_spawner.ominous_activate hostile "
           "@a[distance=..32] ~ ~ ~ 1 0.65")
        wf("taint/ult%d_charge.mcfunction" % p["n"],
           "particle dust{color:[%s],scale:1.7} ~ ~1 ~ 0.55 0.75 0.55 0.02 3 force\n%s\n"
           "execute if score @s rpg_dm_ult matches 20 run particle flash{color:%d} ~ ~1 ~ 0 0 0 0 1 force\n"
           "execute if score @s rpg_dm_ult matches 20 run playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 0.9 0.65\n"
           "execute if score @s rpg_dm_ult matches 10 run particle dust{color:[%s],scale:3.2} ~ ~1 ~ 2.2 1.2 2.2 0.08 85 force\n"
           "execute if score @s rpg_dm_ult matches 10 run playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 1.1 1.1" %
           (rgb, charge_fx[p["n"]], flash, rgb))
        ult_body, ult_hit = ULTIMATES[p["n"]]
        wf("taint/ult%d.mcfunction" % p["n"], ult_body % subs)
        ex.wf_holy("taint/ult%d_hit.mcfunction" % p["n"], ult_hit % subs)

    # 别西卜那道锥形的命中段，六个取点共用一份
    ex.wf_holy("taint/sk4_hit.mcfunction",
       "damage @s 5 minecraft:magic %(BY)s\n"
       "effect give @s minecraft:hunger 8 1 true\n"
       "effect give @s minecraft:slowness 2 0 true\n" % subs)

    # 路西法贯穿那一路的命中段，九个取点共用一份
    ex.wf_holy("taint/sk1b_hit.mcfunction",
       "damage @s 8 minecraft:magic %(BY)s\n"
       "effect give @s minecraft:slowness 3 1 true\n" % subs)

    wf("taint/lord.mcfunction",
       LORD % {"BRANCH": "\n".join(branch), "NONE": none})
    # add_exorcism 只写得出无名者那一手；这里改写成七柱分流，
    # 最后一行仍然落回无名者（没签过约的人招出来的就是他）。
    old_none = "\n".join(l for l in ex.SKILL_NONE.split("\n")
                          if l and not l.startswith("#"))
    wf("taint/skill.mcfunction",
       "# 谁在出手 —— 看他是哪一柱挣出来的。没有柱位的落到最后一行。\n"
       + "\n".join(sk) + "\n" +
       _notice(NONE_UI, NONE_UI["skills"][0][0], NONE_UI["skills"][0][1]) +
       "\n" + old_none)

    # 无名者的提示、蓄势与结算是七柱分流的 fallback。
    none_rgb = _rgb(NONE_UI["main"])
    wf("taint/ult0_warn.mcfunction",
       _notice(NONE_UI, NONE_UI["ultimate"], NONE_UI["ult_text"], True, 18) + "\n" +
       "particle dust{color:[%s],scale:2.6} ~ ~1 ~ 1.4 1 1.4 0.04 42 force\n" % none_rgb +
       "playsound minecraft:block.trial_spawner.ominous_activate hostile "
       "@a[distance=..32] ~ ~ ~ 1 0.45")
    wf("taint/ult0_charge.mcfunction",
       "particle dust{color:[%s],scale:1.7} ~ ~1 ~ 0.55 0.75 0.55 0.02 3 force\n"
       "particle squid_ink ~ ~1 ~ 0.55 0.65 0.55 0.04 4 force\n"
       "execute if score @s rpg_dm_ult matches 20 run particle flash{color:13777735} ~ ~1 ~ 0 0 0 0 1 force\n"
       "execute if score @s rpg_dm_ult matches 20 run playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 0.9 0.55\n"
       "execute if score @s rpg_dm_ult matches 10 run particle dust{color:[%s],scale:3.2} ~ ~1 ~ 2.2 1.2 2.2 0.08 85 force\n"
       "execute if score @s rpg_dm_ult matches 10 run playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 1.1 0.9" %
       (none_rgb, none_rgb))
    none_body, none_hit = ULT_NONE
    wf("taint/ult0.mcfunction", none_body % subs)
    ex.wf_holy("taint/ult0_hit.mcfunction", none_hit % subs)

    wf("taint/ult_start.mcfunction", """# 每第四次出手进入三十刻罪约蓄势。
scoreboard players set @s rpg_dm_casts 0
scoreboard players set @s rpg_dm_ult 30
function rpg:taint/ult_warn
""")
    wf("taint/ult_tick.mcfunction", """# 罪约蓄势期间由恶魔自己的计时器推进，多只同时存在也互不覆盖。
function rpg:taint/ult_charge
scoreboard players remove @s rpg_dm_ult 1
execute if entity @s[scores={rpg_dm_ult=..0}] run function rpg:taint/ult_resolve
""")
    wf("taint/ult_resolve.mcfunction", """# 结算期间临时挂归属标签，复用普通招式的精确伤害来源。
tag @s add rpg.dm.cast
function rpg:taint/ultimate
tag @s remove rpg.dm.cast
""")
    wf("taint/ult_warn.mcfunction",
       "# 罪约预警。没有柱位即无名者。\n" + "\n".join(ult_warn) +
       "\nfunction rpg:taint/ult0_warn")
    wf("taint/ult_charge.mcfunction",
       "# 罪约蓄势表现。没有柱位即无名者。\n" + "\n".join(ult_charge) +
       "\nfunction rpg:taint/ult0_charge")
    wf("taint/ultimate.mcfunction",
       "# 罪约结算。没有柱位即无名者。\n" + "\n".join(ult_cast) +
       "\nfunction rpg:taint/ult0")

    # 路西法的三圈蛇牙使用本体 UUID；不会误伤自己的主人归属。
    fang_pos = []
    for r in (2, 4, 6):
        for x, z in ((r, 0), (-r, 0), (0, r), (0, -r),
                     (r, r), (r, -r), (-r, r), (-r, -r)):
            fang_pos.append("$summon minecraft:evoker_fangs ~%d ~ ~%d "
                            "{Warmup:%d,Owner:$(uuid)}" % (x, z, r * 2))
    wf("taint/ult1_fangs.mcfunction", "\n".join(fang_pos))
    wf("taint/ult4_swarm.mcfunction", "\n".join(
       ['summon minecraft:vex ~ ~1 ~ {life_ticks:300,Tags:["rpg.demon.fly"],'
        'CustomName:[{"text":"饥蝇","color":"#B7C84B"}],Health:10f,'
        'attributes:[{id:"max_health",base:10f},{id:"attack_damage",base:4f}]}'] * 4))
    wf("taint/ult7_seize.mcfunction", """particle wax_on ~ ~0.3 ~ 0.25 0.25 0.25 0.04 10 force
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
kill @s
""")
    return len(PILLARS)


# 七位领主的贴图文件名。按柱位顺序 —— 作者的图放进对应文件即可生效。
SLUG = {1: "lucifer", 2: "leviathan", 3: "abaddon", 4: "beelzebub",
        5: "samael", 6: "belial", 7: "mammon"}


def build_art(rp):
    """恢复七张原图，并把七本书接进 enchanted_book 的模型分派。

    书的 custom_model_data 早就按柱位排好了（CMD0 + N - 1），缺的只是
    材质包这一头。这里补上：七张由项目保管的风格化纹理、一个
    range_dispatch、七个门槛，以及七个模型文件。
    """
    td = os.path.join(rp, "assets/rpg/textures/item")
    md = os.path.join(rp, "assets/rpg/models/item")
    for d in (td, md):
        if not os.path.isdir(d):
            os.makedirs(d)
    for q in PILLARS:
        slug = SLUG[q["n"]]
        art = os.path.join(ART, "pact_%s.png" % slug)
        if not os.path.isfile(art):
            raise RuntimeError("missing authored pact texture: %s" % art)
        shutil.copyfile(art, os.path.join(td, "pact_%s.png" % slug))
        ex.wj(os.path.join(md, "pact_%s.json" % slug),
              {"parent": "item/generated",
               "textures": {"layer0": "rpg:item/pact_%s" % slug}})

    p = os.path.join(rp, "assets/minecraft/items/enchanted_book.json")
    entries = [{"threshold": CMD0 + q["n"] - 1,
                "model": {"type": "minecraft:model",
                          "model": "rpg:item/pact_%s" % SLUG[q["n"]]}}
               for q in PILLARS]
    ex.wj(p, {"model": {
        "type": "minecraft:range_dispatch",
        "property": "minecraft:custom_model_data",
        "index": 0,
        "fallback": {"type": "minecraft:model",
                     "model": "minecraft:item/enchanted_book"},
        "entries": entries}})
    return len(entries)


SUMMON_HEAD = """\
# 八位恶魔的召唤入口，手动招唤用。
#
# **整份跑下去会把八位一起招出来** —— 通常你只想要其中一行，
# 把那一行复制到聊天栏（记得带 /）即可。
#
# 为什么不是裸的 summon：恶魔的寿命是由 rpg:taint/advent_life 给的，
# 只 summon 不走那一步，rpg_fall 停在 0，下一刻就被判过期清掉 ——
# 手动招出来的会瞬间消失。lordN 这一条是完整入口：
# 召唤 + 记下他是谁（技能按这个分流）+ 给寿命。
#
# 每条前面把 #boss 拨上；完整真名调查版本统一按**十分钟**算，
# 而不是旧版降临那只短暂的"来收账者"。
#
# 他们都挂着 devil 标签，于是自动继承包里恶魔 boss 那一套：
# 常驻隐身、周身黑烟与墨。
"""


def build_summon_list():
    """八位的召唤入口写成一份，作者手动招唤用。"""
    lines = [SUMMON_HEAD]
    for q in PILLARS:
        lines.append("# %s · %s　　［%s］" % (q["who"], q["sin"], q["power"]))
        lines.append("scoreboard players set #boss rpg_fall 1")
        lines.append("function rpg:taint/lord%d" % q["n"])
        lines.append("")
    lines.append("# 无名者（没签过契约的人招出来的那一位）")
    lines.append("scoreboard players set #boss rpg_fall 1")
    lines.append("function rpg:taint/lord")
    return wf("command/summon_devil.mcfunction", "\n".join(lines)) \
        or len(PILLARS) + 1


def build_give():
    s = io.open(GIVE, encoding="utf-8").read()
    if "之柱" in s:
        return 0
    lines = ["give @a " + item_snbt(p, False) + " 1" for p in PILLARS]
    io.open(GIVE, "w", encoding="utf-8", newline="\n").write(
        s.rstrip("\n") + "\n\n##七十二柱契约\n" + "\n".join(lines) + "\n")
    return len(lines)


def add_objectives():
    p = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    add = [o for o in OBJECTIVES if o not in s]
    tail = ""
    if add:
        tail += "\n".join("scoreboard objectives add %s dummy" % o for o in add)
    if "#pact_full" not in s:
        tail += ("\nscoreboard players set #pact_full rpg_hud %d" % CD +
                 "\nscoreboard players set #two rpg_pact 2")
    if tail:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n" + tail.strip("\n") + "\n")
    return add


def dump_for_guide():
    """把七柱交给图鉴，免得两边各写一份、迟早写歪。"""
    doc = {"cd_seconds": CD // 20, "use_taint": USE_TAINT, "cmd0": CMD0,
           "pillars": [{k: v for k, v in p.items() if k not in ("boons", "banes")}
                       for p in PILLARS]}
    ex.wj(os.path.join(DP, "..", "_pact.json"), doc)


def main():
    obj = add_objectives()
    n = build_functions()
    build_hud_bar()
    hud = build_hud_identity()
    ticked = wire_tick()
    wire_taint()
    lords = wire_lords()
    demon_hud = build_demon_hud()
    listed = build_summon_list()
    gave = build_give()
    art = build_art(RP)
    dump_for_guide()
    print("pact: %d pillars, %d functions, give +%d, tick +%d, lords %d, "
          "召唤清单 %d 位" % (len(PILLARS), n, gave, ticked, lords, listed))
    print("pact: objectives %s, 书的模型分派 %d 档" % (obj or "-", art))
    print("pact: actionbar 契约对象 %d 位，%d 行" % (len(PILLARS), hud))
    print("pact: 双层 actionbar 恶魔提示 %d 条" % demon_hud)


if __name__ == "__main__":
    main()
