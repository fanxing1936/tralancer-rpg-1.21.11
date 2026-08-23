# -*- coding: utf-8 -*-
"""玛门 —— 七宗罪的最后一件罪器，一把弓。

卷五的七宗罪表里，贪婪那一格一直是空的：六位领主各有一件罪遗武器，
玛门只有第七柱的契约。这个文件把那一格填上。

弓的三件事，全都围着「贪婪从不白给」转：

* **三箭齐发** —— 一次射出三根。多出来的两根是凭空造的，不吃箭袋。
* **什一税** —— 每射一次，玛门就随机从你身上取走点什么：经验、钱、血、
  或者干脆让你饿着。掷点决定收哪一样。
* **买断** —— 满弓之后继续持弓，攒够就能射出一击金箭。它**必定**收费，
  五级经验，付不起就拿命抵。贪婪不赊账。

和第七柱的契约是绑在一起的（作者要求）：

* 签了玛门之柱，弓**不再从身上取东西** —— 它改从魂上收，每箭多沾两点魔化。
  柱位的枷锁本来就是「魔化沾染速度翻倍」，这一条正好接在同一根线上。
* 签了第七柱之后射出的买断金箭，落地时顺带把周围的掉落物翻一倍 ——
  直接复用柱位自己的［点金］，和包里其余「契约借同一位魔神的力」同一形状。

技术上有两处值得记：

1. **弓没有「射出去了」这个触发器**。`using_item` 只告诉你「正在拉」，
   而拉到一半松手是不出箭的 —— 照着「停止拉弓」判定会凭空多出两支箭。
   所以这里认的是**箭本身**：拉弓时开一个几刻的窗口，窗口里扫身边的新箭，
   用 `execute on origin` 回头确认射手是不是自己。没拉过这把弓的人，
   连那次扫描都不欠。
2. **散布不用三角函数**。命令里算 sin/cos 太贵，而定速矢量上的小扰动
   本来就等价于一个小角度的偏转 —— 直接把 Motion 的三个分量各抖一下，
   出来就是个漂亮的锥形散布。
"""
import io
import json
import os
import sys

import add_exorcism as ex

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
RP = sys.argv[2] if len(sys.argv) > 2 else "../resourcepack"
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement/item")
# 放进 extra —— 那就是「新锻装备」那个盒子，利维坦与路西法也在里面。
GIVE = os.path.join(FUNC, "command/give/extra.mcfunction")

# ---------------------------------------------------------------------------
# 常数
# ---------------------------------------------------------------------------
CMD = 1110003            # 弓的第三个模型位（1110001 泡泡弓 / 1110002 疾风弓）
ACCENT = "#B7950B"       # 与第七柱同色 —— 作者要的就是契约与罪器认得出是一家
LIT = "#FFD700"

FULL = 40                # 攒到多少刻算买断（原版满弓 20 刻，即再持满弓一秒）
WIN = 8                  # 拉弓之后留几刻去认那支箭
CATCH_R = 10             # 认箭的半径。满弓箭每刻飞 3 格，6 格只够容一刻延迟
BUY_LV = 5               # 买断的价：五级经验
BUY_HP = 6               # 付不起就拿命抵（三颗心）
FORKS = 2                # 附赠几根箭（连原箭共三根）
JIT_XZ = 250             # Motion 的横向抖动（千分之一格/刻）
JIT_Y = 110

# 佣兵那边的同一种钱。什一税优先收它。
CUR = "minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}]"

OBJECTIVES = ["rpg_mam", "rpg_mam_c", "rpg_mam_win", "rpg_mam_dw"]

seg, row, wj = ex.seg, ex.row, ex.wj
RULE = ex.RULE


def wf(rel, text):
    ex.wf(rel, text)


# ---------------------------------------------------------------------------
# 物品
# ---------------------------------------------------------------------------
def item_snbt():
    """罪器的名牌一律同一张脸：[DEVIL] 前缀 + 领主本色 + 三段式 Lore。"""
    lore = [
        RULE,
        row(seg("堕落的"), seg("财富之主", ACCENT, True)),
        row(seg("称量众生的秤，"), seg("玛门", ACCENT, True)),
        RULE,
        row(seg("🏹被动技能"), seg("[三箭齐发]", ACCENT, True)),
        row(seg("一次射出三根，多出的两根凭空而来")),
        RULE,
        row(seg("🏹被动技能"), seg("[什一税]", ACCENT, True)),
        row(seg("每射一箭，玛门都要从你身上取走一样")),
        RULE,
        row(seg("🏹主动技能"), seg("[买断]", ACCENT, True)),
        row(seg("满弓后继续持弓，射出一击金箭")),
        row(seg("必定收费 —— 贪婪不赊账")),
        RULE,
    ]
    return (
        "bow["
        "custom_name=" + row(seg("[DEVIL]", ACCENT, True), seg("玛门")) + ","
        "lore=[" + ",".join(lore) + "],"
        "enchantments={power:5,punch:2,flame:1,unbreaking:3},"
        'attribute_modifiers=[{type:"luck",amount:1,slot:mainhand,'
        'operation:add_value,id:"rpg:mammon/greed"}],'
        "custom_model_data={floats:[%d.0f]}," % CMD +
        "unbreakable={},"
        # 只留 devil_tag（魔化按罪器计数）与 mammon_tag（这把弓自己的触发）。
        #
        # bow_tag 在这个包里身兼两职：它既是「武器注册」的开关
        # （com/weapon 靠它把武器接进符文／磨刀石／分支那一套），
        # 又是**爆裂弓玩法**的开关（item/bow/speed：给箭加速、命中召苦力怕）。
        #
        # 两件事挤在一个标记上，所以不能简单地取舍：去掉它，玛门就不算武器；
        # 留着它，每支箭都召一只苦力怕。解法是把玩法那一半单独摘出来 ——
        # 见 carve_out()：让 speed.mcfunction 跳过玛门。
        #
        # hunter_tag 则是纯玩法（猎手弓那一套），玛门不需要，已经去掉。
        "custom_data={bow_tag:1b,devil_tag:1b,mammon_tag:1b},"
        'tooltip_display={hidden_components:["minecraft:unbreakable"]}]')


# ---------------------------------------------------------------------------
# 拉弓
# ---------------------------------------------------------------------------
DRAW = """\
# 正在拉弓。`using_item` 在按住期间每刻都响，所以这里就是逐刻的蓄力。
advancement revoke @s only rpg:item/mammon

# 这是新的一次拉弓吗？rpg_mam_dw 只活 2 刻，所以「上一刻还在拉」等价于它 >=1。
# 是新的一次就先清零 —— 蓄力**不跨箭累积**。
#
# 清零必须放在开始，不能放在结束：松手之后要 8 刻才关窗，
# 而连射的再次拉弓比这快得多，永远等不到那次清零。
execute if entity @s[scores={rpg_mam_dw=..0}] run scoreboard players set @s rpg_mam_c 0
scoreboard players set @s rpg_mam_dw 2
scoreboard players add @s rpg_mam_c 1

# 开一个窗口。松手之后的几刻里，rpg:mammon/watch 会去认那支离弦的箭 ——
# 弓没有「射出去了」这个触发器，只能反过来从箭那头认。
scoreboard players set @s rpg_mam_win %(WIN)d

# 攒满的那一刻响一声，告诉你买断已经可以出手了
execute if entity @s[scores={rpg_mam_c=%(FULL)d}] run playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.6
execute if entity @s[scores={rpg_mam_c=%(FULL)d}] at @s run particle wax_on ~ ~1.2 ~ 0.3 0.3 0.3 0.05 20

# 交给统一 HUD 渲染：声明占用，并把进度换算成格数
scoreboard players set @s rpg_hud %(HID)d
scoreboard players set @s rpg_hud_t %(TTL)d
scoreboard players operation @s rpg_hud_p = @s rpg_mam_c
scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud
scoreboard players operation @s rpg_hud_p /= #mam_full rpg_hud
execute if entity @s[scores={rpg_hud_p=%(SEG)d..}] run scoreboard players set @s rpg_hud_p %(SEG)d
"""

WATCH = """\
# 认箭。只有窗口没走完的人才会进到这里 —— 没碰过这把弓的人一条不欠。
scoreboard players remove @s rpg_mam_win 1
execute if entity @s[scores={rpg_mam_dw=1..}] run scoreboard players remove @s rpg_mam_dw 1

# 身边六格内的新箭。带类型、带半径，比一次全表遍历便宜得多。
# 标记自己是当前射手：箭那头要用 `on origin` 回头核对。
tag @s add rpg.mam.shooter
execute as @e[type=minecraft:arrow,tag=!rpg.mam.seen,distance=..%(R)d] run function rpg:mammon/arrow
tag @s remove rpg.mam.shooter

# 窗口走完还没等到箭 —— 那是拉到一半松了手，没出箭。蓄力作废。
execute if entity @s[scores={rpg_mam_win=..0}] run scoreboard players set @s rpg_mam_c 0
"""

ARROW = """\
# 一支还没认过的箭。是不是我射的？`on origin` 会把 @s 换成射手。
tag @s add rpg.mam.seen
scoreboard players set #mine rpg_mam 0
execute on origin if entity @s[tag=rpg.mam.shooter] run scoreboard players set #mine rpg_mam 1
execute if score #mine rpg_mam matches 1 run function rpg:mammon/shot
"""

# ---------------------------------------------------------------------------
# 三箭齐发
# ---------------------------------------------------------------------------
SHOT = """\
# 这一箭是玛门的。@s 是那支原箭。
#
# 买断与否，先在这里定下来：射手攒够了刻数，这一发就是买来的。
scoreboard players set #gold rpg_mam 0
execute on origin if entity @s[scores={rpg_mam_c=%(FULL)d..}] run scoreboard players set #gold rpg_mam 1

# 三根箭共用的底子：归属、伤害、以及**发射它的那把弓**都跟着原箭走。
#
# 伤害不写死：箭的 damage 是基数，命中伤害是它乘以飞行速度、再叠附魔。
# 照抄原箭，附赠的两根才和真箭一模一样 —— 这才叫「一次射出三根」。
# weapon 是 1.21.5 之后箭身上记的那把弓，力量／冲击／火矢都由它生效；
# 先 remove 再 set from：万一原箭没有这一项，storage 里不该留着上一发的。
data modify storage rpg:mam owner set from entity @s Owner
data modify storage rpg:mam dmg set from entity @s damage
data remove storage rpg:mam weapon
data modify storage rpg:mam weapon set from entity @s weapon
data modify storage rpg:mam pierce set value 0b
execute if score #gold rpg_mam matches 1 run data modify storage rpg:mam dmg set value %(GDMG)sd
execute if score #gold rpg_mam matches 1 run data modify storage rpg:mam pierce set value 5b
execute if score #gold rpg_mam matches 1 run function rpg:mammon/gild

# 原箭的速度。附赠的两根在这个基础上各抖一下 —— 三角函数在命令里太贵，
# 而定速矢量上的小扰动本来就等价于一个小角度的偏转。
execute store result score #mx rpg_mam run data get entity @s Motion[0] 1000
execute store result score #my rpg_mam run data get entity @s Motion[1] 1000
execute store result score #mz rpg_mam run data get entity @s Motion[2] 1000
%(FORKS)s

# 结算记在射手头上
execute on origin run function rpg:mammon/settle
"""

GILD = """\
# 买断的那一箭。@s 还是原箭 —— 附赠的两根在 aim 里照抄同一份伤害。
data modify entity @s PierceLevel set value 5b
data modify entity @s crit set value 1b
data modify entity @s Glowing set value 1b
data modify entity @s damage set from storage rpg:mam dmg
"""

FORK = """\
# 一根附赠的箭。pickup:0b —— 凭空造的东西捡不回来，
# 否则这把弓就成了无限箭袋。
summon minecraft:arrow ~ ~ ~ {Tags:["rpg.mam.seen","rpg.mam.new"],pickup:0b,Fire:200s}
execute as @e[type=minecraft:arrow,tag=rpg.mam.new,limit=1] run function rpg:mammon/aim
"""

AIM = """\
# 抖一下方向，接上归属与伤害。
#
# crit 与 PierceLevel 不能写在 summon 的 NBT 里：箭在构造时会自己重算这两项，
# 写进去的值当场就没了（实测 summon 给 5b，读回来是 0b）。落地之后再 data modify
# 就留得住 —— 所以这两行必须在这里，不能挪回上面那条 summon。
tag @s remove rpg.mam.new
data modify entity @s Owner set from storage rpg:mam owner
data modify entity @s damage set from storage rpg:mam dmg
data modify entity @s weapon set from storage rpg:mam weapon
data modify entity @s crit set value 1b
data modify entity @s PierceLevel set from storage rpg:mam pierce

execute store result score #jx rpg_mam run random value -%(XZ)d..%(XZ)d
execute store result score #jy rpg_mam run random value -%(Y)d..%(Y)d
execute store result score #jz rpg_mam run random value -%(XZ)d..%(XZ)d
scoreboard players operation #jx rpg_mam += #mx rpg_mam
scoreboard players operation #jy rpg_mam += #my rpg_mam
scoreboard players operation #jz rpg_mam += #mz rpg_mam
execute store result entity @s Motion[0] double 0.001 run scoreboard players get #jx rpg_mam
execute store result entity @s Motion[1] double 0.001 run scoreboard players get #jy rpg_mam
execute store result entity @s Motion[2] double 0.001 run scoreboard players get #jz rpg_mam
"""

# ---------------------------------------------------------------------------
# 结算
# ---------------------------------------------------------------------------
SETTLE = """\
# @s 是射手。蓄力无论如何都清零 —— 下一箭重新攒。
scoreboard players set @s rpg_mam_c 0
execute if score #gold rpg_mam matches 1 run return run function rpg:mammon/buyout
function rpg:mammon/toll
"""

TOLL = """\
# 什一税。玛门从不白干活，每一箭都要拿走点什么 —— 掷点决定拿哪一样。
#
# 签了第七柱的人例外：他欠的不是钱，是魂。
execute if entity @s[tag=rpg.pact,scores={rpg_pact=7}] run return run function rpg:mammon/toll_pact

execute store result score #t rpg_mam run random value 1..100
execute if score #t rpg_mam matches 1..34 run return run function rpg:mammon/toll1
execute if score #t rpg_mam matches 35..58 run return run function rpg:mammon/toll2
execute if score #t rpg_mam matches 59..78 run return run function rpg:mammon/toll3
execute if score #t rpg_mam matches 79..92 run return run function rpg:mammon/toll4
function rpg:mammon/toll5
"""

TOLL_PACT = """\
# 第七柱的人：贪婪不从他口袋里掏，它从魂上收。
# 柱位的枷锁本来就是「魔化沾染速度翻倍」，这一条接在同一根线上。
scoreboard players add @s rpg_taint %(TAINT)d
title @s actionbar ["",{"text":"[什一税]","italic":false,"color":"%(A)s","bold":true},{"text":"　柱中的东西替你付了账","italic":false,"color":"dark_red"}]
playsound minecraft:block.sculk.charge player @s ~ ~ ~ 0.8 0.6
execute at @s run particle sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.02 8
"""

TOLL_XP = """\
# 通行费：一箭一段路，路是要买的。
xp add @s -%(N)d points
title @s actionbar ["",{"text":"[通行费]","italic":false,"color":"%(A)s","bold":true},{"text":"　玛门收走了 %(N)d 点经验","italic":false,"color":"gray"}]
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.8 0.5
"""

TOLL_COIN = """\
# 什一税：先看口袋里有没有钱。`clear ... 0` 是只数不拿，原版惯用写法。
execute store result score #have rpg_mam run clear @s %(CUR)s 0
execute if score #have rpg_mam matches 1.. run return run function rpg:mammon/toll2_coin
# 一个子儿也没有 —— 那就折成经验。
function rpg:mammon/toll1
"""

TOLL_COIN_DO = """\
clear @s %(CUR)s 1
title @s actionbar ["",{"text":"[什一税]","italic":false,"color":"%(A)s","bold":true},{"text":"　玛门收走了 1 枚","italic":false,"color":"gray"}]
playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 0.6
execute at @s run particle wax_on ~ ~1 ~ 0.3 0.4 0.3 0.05 10
"""

TOLL_BLOOD = """\
# 血税。口袋空了，秤上还有别的东西。
damage @s %(N)d minecraft:magic
title @s actionbar ["",{"text":"[血税]","italic":false,"color":"%(A)s","bold":true},{"text":"　玛门称走了你的一份血","italic":false,"color":"dark_red"}]
playsound minecraft:entity.player.hurt player @s ~ ~ ~ 0.7 0.6
"""

TOLL_HUNGER = """\
# 饥荒。贪婪拿走的不一定是你身上的东西 —— 也可以是你下一顿。
effect give @s minecraft:hunger 8 1 true
title @s actionbar ["",{"text":"[饥荒]","italic":false,"color":"%(A)s","bold":true},{"text":"　你的下一顿也被算进账里","italic":false,"color":"gray"}]
playsound minecraft:entity.generic.eat player @s ~ ~ ~ 0.8 0.5
"""

TOLL_GREED = """\
# 贪得无厌。偶尔它一次收两样。
xp add @s -%(N)d points
damage @s %(D)d minecraft:magic
title @s actionbar ["",{"text":"[贪得无厌]","italic":false,"color":"%(A)s","bold":true},{"text":"　这一箭，玛门收了两样","italic":false,"color":"dark_red"}]
playsound minecraft:entity.wither.ambient player @s ~ ~ ~ 0.6 1.4
"""

# ---------------------------------------------------------------------------
# 买断
# ---------------------------------------------------------------------------
BUYOUT = """\
# 买断。它不掷点 —— 贪婪不赊账，这一箭的价钱是写死的。
title @s actionbar ["",{"text":"[买断]","italic":false,"color":"%(A)s","bold":true},{"text":"　金箭离弦","italic":false,"color":"%(L)s"}]
playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 0.8
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 0.6
execute at @s anchored eyes run particle wax_on ^ ^ ^1 0.3 0.3 0.3 0.1 40
execute at @s anchored eyes run particle end_rod ^ ^ ^1 0.2 0.2 0.2 0.05 25

# 签了第七柱的人，这一箭顺带把周围的掉落物点成两份 ——
# 借的是柱位自己的［点金］，不另写一份同味道的东西。
execute if entity @s[tag=rpg.pact,scores={rpg_pact=7}] at @s as @e[type=minecraft:item,distance=..8] at @s run function rpg:pact/p7_gild

# 付账。先看经验够不够，不够就拿命抵。
execute store result score #lv rpg_mam run xp query @s levels
execute if score #lv rpg_mam matches %(LV)d.. run return run function rpg:mammon/pay_xp
function rpg:mammon/pay_hp
"""

PAY_XP = """\
xp add @s -%(LV)d levels
title @s actionbar ["",{"text":"[买断]","italic":false,"color":"%(A)s","bold":true},{"text":"　付讫：%(LV)d 级","italic":false,"color":"gray"}]
"""

PAY_HP = """\
# 付不起。玛门不会因此收手 —— 它只是换个东西收。
damage @s %(HP)d minecraft:magic
effect give @s minecraft:weakness 6 0 true
title @s actionbar ["",{"text":"[买断]","italic":false,"color":"%(A)s","bold":true},{"text":"　付不起 —— 于是拿命抵了","italic":false,"color":"dark_red"}]
playsound minecraft:entity.wither.hurt player @s ~ ~ ~ 0.8 0.6
"""


# ---------------------------------------------------------------------------
# 生成
# ---------------------------------------------------------------------------
def build_functions():
    forks = "\n".join(["function rpg:mammon/fork"] * FORKS)

    wf("mammon/draw.mcfunction", DRAW % {
        "WIN": WIN, "FULL": FULL, "HID": ex.HUD_MAMMON,
        "TTL": ex.HUD_TTL, "SEG": ex.SEGMENTS})
    wf("mammon/watch.mcfunction", WATCH % {"R": CATCH_R})
    wf("mammon/arrow.mcfunction", ARROW)
    wf("mammon/shot.mcfunction", SHOT % {
        "FULL": FULL, "GDMG": "4.0", "FORKS": forks})
    wf("mammon/gild.mcfunction", GILD)
    wf("mammon/fork.mcfunction", FORK)
    wf("mammon/aim.mcfunction", AIM % {"XZ": JIT_XZ, "Y": JIT_Y})
    wf("mammon/settle.mcfunction", SETTLE)

    wf("mammon/toll.mcfunction", TOLL)
    wf("mammon/toll_pact.mcfunction", TOLL_PACT % {"TAINT": 2, "A": ACCENT})
    wf("mammon/toll1.mcfunction", TOLL_XP % {"N": 6, "A": ACCENT})
    wf("mammon/toll2.mcfunction", TOLL_COIN % {"CUR": CUR})
    wf("mammon/toll2_coin.mcfunction", TOLL_COIN_DO % {"CUR": CUR, "A": ACCENT})
    wf("mammon/toll3.mcfunction", TOLL_BLOOD % {"N": 2, "A": ACCENT})
    wf("mammon/toll4.mcfunction", TOLL_HUNGER % {"A": ACCENT})
    wf("mammon/toll5.mcfunction", TOLL_GREED % {"N": 12, "D": 2, "A": ACCENT})

    wf("mammon/buyout.mcfunction", BUYOUT % {"A": ACCENT, "L": LIT, "LV": BUY_LV})
    wf("mammon/pay_xp.mcfunction", PAY_XP % {"LV": BUY_LV, "A": ACCENT})
    wf("mammon/pay_hp.mcfunction", PAY_HP % {"HP": BUY_HP, "A": ACCENT})
    return 18


def build_advancement():
    wj(os.path.join(ADV, "mammon.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {
                "items": "minecraft:bow",
                "predicates": {"minecraft:custom_data": "{mammon_tag:1b}"}}}}},
        "rewards": {"function": "rpg:mammon/draw"}})


def carve_out():
    """把玛门从「爆裂弓」那套玩法里摘出来。

    bow_tag 身兼武器注册与爆裂弓两职。玛门需要前者（否则它不算武器，
    符文与磨刀石都认不了它），但绝不要后者 —— 那会让每支箭都召一只苦力怕，
    顺带把箭速翻倍、跑出认箭半径，买断也跟着失灵。

    所以不动 bow_tag 本身，只在爆裂弓那条路上加一道「除了玛门」。
    判定用手上那件东西而不是索引标签：mammon_tag 没有进 index_player，
    而这几行只在有箭在飞时才走，多一次物品判定不值一提。
    """
    p = os.path.join(FUNC, "item/bow/speed.mcfunction")
    if not os.path.isfile(p):
        return 0
    s = io.open(p, encoding="utf-8").read()
    if "mammon_tag" in s:
        return 0
    guard = ("if entity @s[tag=rpg.h.bow_tag1] "
             "unless items entity @s weapon.mainhand "
             "*[minecraft:custom_data~{mammon_tag:1b}]")
    out = s.replace("if entity @s[tag=rpg.h.bow_tag1]", guard)
    n = out.count("mammon_tag")
    io.open(p, "w", encoding="utf-8", newline="\n").write(out)
    return n


def wire_tick():
    p = os.path.join(FUNC, "exorcism.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg:mammon/watch" in s:
        return 0
    io.open(p, "w", encoding="utf-8", newline="\n").write(
        s.rstrip("\n") + "\n\n"
        "# 玛门的弓。弓没有「射出去了」这个触发器，只能在拉弓之后开一个几刻的\n"
        "# 窗口，反过来从箭那头认。窗口分数不为零的人才进 —— 没碰过这把弓的\n"
        "# 人一条也不欠。\n"
        "execute as @a[scores={rpg_mam_win=1..}] at @s run function rpg:mammon/watch\n")
    return 1


def build_give():
    s = io.open(GIVE, encoding="utf-8").read()
    if "mammon_tag" in s:
        return 0
    io.open(GIVE, "w", encoding="utf-8", newline="\n").write(
        s.rstrip("\n") + "\n\n##玛门（贪婪·第七件罪器）\ngive @a " + item_snbt() + "\n")
    return 1


def add_objectives():
    p = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    add = [o for o in OBJECTIVES if o not in s]
    tail = ["scoreboard objectives add %s dummy" % o for o in add]
    if "#mam_full" not in s:
        tail.append("scoreboard players set #mam_full rpg_hud %d" % FULL)
    if tail:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n" + "\n".join(tail) + "\n")
    return add


# ---------------------------------------------------------------------------
# 资源包
# ---------------------------------------------------------------------------
def build_models():
    """把 1110003 接进 bow 的模型分派，并补上四个 pulling 阶段的模型。

    贴图由作者提供，路径就是下面这四个 —— 模型先摆好，图一放进去就生效。
    """
    base = "mammon_bow"
    md = os.path.join(RP, "assets/rpg/models/item")
    if not os.path.isdir(md):
        os.makedirs(md)
    for suffix in ("", "_pulling_0", "_pulling_1", "_pulling_2"):
        wj(os.path.join(md, base + suffix + ".json"),
           {"parent": "item/bow",
            "textures": {"layer0": "rpg:item/" + base + suffix}})

    p = os.path.join(RP, "assets/minecraft/items/bow.json")
    doc = json.load(io.open(p, encoding="utf-8"))
    entries = doc["model"]["entries"]
    if any(e["threshold"] == CMD for e in entries):
        return 0
    entries.append({
        "threshold": CMD,
        "model": {
            "type": "minecraft:condition",
            "property": "minecraft:using_item",
            "on_false": {"type": "minecraft:model", "model": "rpg:item/" + base},
            "on_true": {
                "type": "minecraft:range_dispatch",
                "property": "minecraft:use_duration",
                "scale": 0.05,
                "fallback": {"type": "minecraft:model",
                             "model": "rpg:item/%s_pulling_0" % base},
                "entries": [
                    {"threshold": 0.65,
                     "model": {"type": "minecraft:model",
                               "model": "rpg:item/%s_pulling_1" % base}},
                    {"threshold": 0.9,
                     "model": {"type": "minecraft:model",
                               "model": "rpg:item/%s_pulling_2" % base}},
                ]}}})
    entries.sort(key=lambda e: e["threshold"])
    wj(p, doc)
    return 1


def main():
    obj = add_objectives()
    n = build_functions()
    build_advancement()
    ticked = wire_tick()
    carved = carve_out()
    gave = build_give()
    models = build_models()
    print("mammon: %d functions, give +%d, tick +%d, models +%d, "
          "爆裂弓避让 %d 处" % (n, gave, ticked, models, carved))
    print("mammon: objectives %s" % (obj or "-"))


if __name__ == "__main__":
    main()
