# -*- coding: utf-8 -*-
"""友军雅克（docs/JACQUES-ALLY.md）：击败圣殿大团长雅克后得到「圣殿誓约」，右键召他来并肩作战 20 秒。

    python add_jacques_ally.py ../rpg ../resourcepack

- 道具：圣殿誓约，右键使用。贴图是原作《地下城》风之号角（SM_WindHorn + T_Windhorn）换成圣殿配色后渲染的
  32×32 像素图（jacques_ally_ref/make_oath_icon.py 一次性生成 oath.png），，冷却 3 分钟（自己的冷却分数 + 原版 use_cooldown 的冷却遮罩）。
  雅克战胜利时发给战场里每个还没有的人（rpg:jacques_ally/reward）。
- 载体：铁傀儡（NoAI，缩到卫道士的高度 0.7407），穿雅克的外观（rpg.jqwear）。铁傀儡是原版敌怪会主动
  去打的东西：僵尸、骷髅、蜘蛛、掠夺者、劫掠兽、史莱姆……都会锁定他。数据包里的 Boss 与怪物技能由
  add_ally_units.py 在构建末尾统一改写，把他当成玩家一样选为目标、算进范围伤害。
- 他：生命 100，副手藏一件死亡保护；被打到致命时死亡保护被吃掉 → 他倒下离场。玩家误伤会被补回。
  行动全由函数驱动：找最近的敌怪（含隐身的 Boss 载体），走过去；贴身坟墓克星三连，远处竖琴弩单发；
  没有敌人时跟着召唤他的人。20 秒到时，光柱里离开。
"""

import json
import math
import os
import sys

import rpg_ui_style as ui
from boss_fx import Fx, flat_sc, sc
from display_mob import hook_tag, wf, wj

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
RP = sys.argv[2] if len(sys.argv) > 2 else None
HERE = os.path.dirname(os.path.abspath(__file__))
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "jacques_ally")
B = "rpg:jacques_ally"
LOOK = "rpg:jacques"
O = "rpg_al"
ALLY = "type=minecraft:iron_golem,tag=rpg.jqa"
# 敌人：封印用的敌怪表（含卫道士载体的 Boss 与领主），不打苦力怕；不打无敌的（预览、大卫的幽灵、阶段无敌）
FOE = ("type=#rpg:seal_hostile,type=!minecraft:creeper,tag=!rpg.ally,tag=!rpg.jqd,tag=!rpg.jqb.preview,"
       "nbt=!{Invulnerable:1b}")
UNIT_TAGS = ("rpg.unit", "rpg.unit.ns", "rpg.unit.nc", "rpg.unit.f")

LIFE = 400                 # 20 秒
HP = 100
COOLDOWN = 3600            # 3 分钟
SCALE = 0.7407             # 铁傀儡 2.7 高 × 0.7407 = 2.0，和卫道士的乘客挂点一样，外观部件不用另调
SLASH_DMG, SWEEP_DMG, SHOT_DMG = 9, 12, 8
MELEE_R, SHOT_MIN, SHOT_MAX, SEEK_R = 3.2, 6, 22, 20
STEP = 0.3
GUARD = 'minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]'

GOLD = "#F0CF7A"
GOLD_I = 0xF0CF7A
PALE = "#FFF2C8"
PALE_I = 0xFFF2C8
TEMPLAR_RED = "#C8102E"
TEMPLAR_WHITE = "#F2F2F2"
GOLD_DUST = "minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.2}"


def w(path, lines):
    wf(os.path.join(OUT, *path.split("/")) + ".mcfunction", lines)


fx = Fx(fn=B, tag="rpg.jqa.fx", life="rpg_al_life", kind="rpg_al_kd", writer=w, kinds={
    "sweep": dict(life=8, steps=[(7, 3, flat_sc(4.5)), (3, 3, flat_sc(5.5))]),
    "pillarfade": dict(life=24, steps=[(23, 3, sc((0.75, 28, 0.75))), (12, 12, sc((0.02, 28, 0.02)))]),
    "pillarcore": dict(life=24, steps=[(23, 3, sc((0.3, 28, 0.3))), (14, 10, sc((0.01, 28, 0.01)))]),
    "ringm": dict(life=12, steps=[(11, 10, flat_sc(6))]),
})
NEW = "rpg.jqa.fxnew"


def say(text, gloss=None, who="@s"):
    parts = [ui.comp("〖", TEMPLAR_RED, True), ui.comp("雅克", TEMPLAR_WHITE, True), ui.comp("〗", TEMPLAR_RED, True)]
    if gloss:
        parts.append(ui.comp(" " + ui.fraktur(gloss), ui.BROADCAST_GLOSS))
    parts += [ui.comp(ui.GAP, ui.BROADCAST_BODY), ui.comp(text, ui.BROADCAST_BODY)]
    return "tellraw %s %s" % (who, ui.row(*parts))


def anim(clip):
    return "function %s/anim/enter/%s" % (LOOK, clip)


def weapon(name):
    return "function %s/weapon/%s" % (LOOK, name)


def light_pillar(color):
    return ([fx.disp("beam", scale=(0.2, 28, 0.2), color=color, trans=(0, 14, 0))] + fx.born(kind="pillarfade")
            + [fx.disp("beam", scale=(0.1, 28, 0.1), color=0xFFFFFF, trans=(0, 14, 0))] + fx.born(kind="pillarcore")
            + ["particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30"])


def wave(p, n, speed, y=0.2, r0=0.4):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        out.append("particle %s ~%.2f ~%.2f ~%.2f %.3f 0 %.3f %g 0" % (p, r0 * c, y, r0 * s, c, s, speed))
    return out


# =====================================================================================
# 道具：圣殿誓约
# =====================================================================================
OATH_NAME = ui.tier_name("legend", "圣殿誓约")
OATH_LORE = [
    [ui.comp("雅克的号角。他倒在火里时，把它留给了你。", ui.GRAY)],
    [ui.comp("")],
    [ui.comp("右键：", ui.GRAY), ui.comp("召唤圣殿大团长雅克并肩作战 20 秒", PALE)],
    [ui.comp("· 生命 100，敌人会像对待玩家一样攻击他", ui.GRAY)],
    [ui.comp("· 坟墓克星三连 / 竖琴弩", ui.GRAY)],
    [ui.comp("冷却 3 分钟", ui.GRAY)],
]


def oath_item():
    return ("minecraft:paper[item_model=\"rpg:jacques_oath\",custom_name=" + OATH_NAME
            + ",lore=" + ui.lore(OATH_LORE)
            + ",rarity=\"epic\",enchantment_glint_override=true,max_stack_size=1,"
            "consumable={consume_seconds:100180f,animation:\"toot_horn\",sound:\"minecraft:intentionally_empty\","
            "has_consume_particles:false,on_consume_effects:[]},"
            "use_cooldown={seconds:%df,cooldown_group:\"rpg:jacques_oath\"},"
            "custom_data={rpg_jq_oath:1b}]" % (COOLDOWN // 20))


def items():
    w("give", ["# 给执行者一件圣殿誓约（调试 / 发放入口）。", "give @s " + oath_item()])
    w("reward", [
        "# 雅克战胜利（at 战场中心）：战场里还没有圣殿誓约的人各得一件。",
        "execute as @a[distance=..48,gamemode=!spectator] unless items entity @s container.* *[minecraft:custom_data~{rpg_jq_oath:1b}] "
        "unless items entity @s weapon.offhand *[minecraft:custom_data~{rpg_jq_oath:1b}] run function %s/reward_one" % B,
    ])
    w("reward_one", [
        "give @s " + oath_item(),
        say("……拿着它。下次，我站在你这边。", gloss="The Grand Master"),
        "playsound minecraft:event.raid.horn master @s ~ ~ ~ 0.8 1.4",
    ])
    adv = os.path.join(DP, "data", "rpg", "advancement", "jacques_ally")
    wj(os.path.join(adv, "use.json"), {
        "criteria": {"use": {"trigger": "minecraft:using_item", "conditions": {
            "item": {"predicates": {"minecraft:custom_data": "{rpg_jq_oath:1b}"}}}}},
        "rewards": {"function": "%s/use" % B}})
    wj(os.path.join(adv, "friendly.json"), {
        "criteria": {"hit": {"trigger": "minecraft:player_hurt_entity", "conditions": {
            "entity": [{"condition": "minecraft:entity_properties", "entity": "this",
                        "predicate": {"type": "minecraft:iron_golem", "nbt": "{Tags:[\"rpg.ally\"]}"}}]}}},
        "rewards": {"function": "%s/friendly" % B}})

    cd_msg = ui.row(ui.comp("〖圣殿誓约〗", GOLD, True), ui.comp(ui.GAP, ui.BROADCAST_BODY),
                    ui.comp("号角还在回响。还需 ", ui.BROADCAST_BODY), {"score": {"name": "#left", "objective": O}, "color": PALE},
                    ui.comp(" 秒。", ui.BROADCAST_BODY))
    w("use", [
        "# 右键圣殿誓约（as 玩家）。按住会每刻触发一次：只认按下的第一刻。",
        "advancement revoke @s only rpg:jacques_ally/use",
        "execute store result score #now %s run time query gametime" % O,
        "scoreboard players operation #gap %s = #now %s" % (O, O),
        "scoreboard players operation #gap %s -= @s rpg_al_lu" % O,
        "scoreboard players operation @s rpg_al_lu = #now %s" % O,
        "execute if score #gap %s matches ..2 run return 0" % O,
        "execute if score @s rpg_al_cd > #now %s run return run function %s/use_wait" % (O, B),
        "function %s/summon" % B,
    ])
    w("use_wait", [
        "scoreboard players operation #left %s = @s rpg_al_cd" % O,
        "scoreboard players operation #left %s -= #now %s" % (O, O),
        "scoreboard players add #left %s 19" % O,
        "scoreboard players set #k %s 20" % O,
        "scoreboard players operation #left %s /= #k %s" % (O, O),
        "tellraw @s " + cd_msg,
    ])
    w("friendly", [
        "# 玩家误伤了友军雅克：把他的生命补回这一刻之前（as 玩家）。",
        "advancement revoke @s only rpg:jacques_ally/friendly",
        "execute as @e[%s,distance=..48] store result entity @s Health float 1 run scoreboard players get @s rpg_al_hp" % ALLY,
    ])


# =====================================================================================
# 召唤、每刻、离场
# =====================================================================================
def life():
    w("load", [
        "scoreboard objectives add %s dummy" % O,
        "scoreboard objectives add rpg_al_id dummy",     # 玩家编号 / 友军的主人编号
        "scoreboard objectives add rpg_al_own dummy",
        "scoreboard objectives add rpg_al_cd dummy",     # 玩家：冷却到哪一刻（游戏刻）
        "scoreboard objectives add rpg_al_lu dummy",     # 玩家：上一次触发的游戏刻
        "scoreboard objectives add rpg_al_t dummy",      # 友军：已存在刻数
        "scoreboard objectives add rpg_al_hp dummy",     # 友军：上一刻的生命
        "scoreboard objectives add rpg_al_b dummy",      # 友军：出手冷却
        "scoreboard objectives add rpg_al_cb dummy",     # 友军：三连走到第几下
        "scoreboard objectives add rpg_al_sk dummy",     # 友军：正在出的招（1 下劈 2 再劈 3 横扫 4 弩）
        "scoreboard objectives add rpg_al_mt dummy",     # 友军：招式时间线
        "scoreboard objectives add rpg_al_life dummy",
        "scoreboard objectives add rpg_al_kd dummy",
    ])
    w("units", [
        "# 「像玩家一样的单位」的标签（每刻最先刷新；add_ally_units.py 把敌方技能里的 @a 改写成按这些标签选）：",
        "#   rpg.unit 全部玩家 + 友军；.ns 去掉旁观；.nc 去掉创造；.f 去掉旁观与创造（能挨打的人）。友军自己一直带着四个。",
    ] + ["tag @a remove %s" % t for t in UNIT_TAGS] + [
        "tag @a add rpg.unit",
        "tag @a[gamemode=!spectator] add rpg.unit.ns",
        "tag @a[gamemode=!creative] add rpg.unit.nc",
        "tag @a[gamemode=!spectator,gamemode=!creative] add rpg.unit.f",
    ])
    name = [ui.comp("[圣殿誓约]", GOLD, True), ui.comp("雅克", TEMPLAR_WHITE)]
    w("summon", [
        "# 召唤友军雅克（as/at 玩家）：在身前 1.5 格落下。",
        "execute unless score @s rpg_al_id matches 1.. run function %s/new_id" % B,
        "scoreboard players operation @s rpg_al_cd = #now %s" % O,
        "scoreboard players add @s rpg_al_cd %d" % COOLDOWN,
        "scoreboard players operation #own %s = @s rpg_al_id" % O,
        "execute rotated ~ 0 positioned ^ ^ ^1.5 run function %s/spawn" % B,
        "playsound minecraft:event.raid.horn player @a[distance=..48] ~ ~ ~ 1.2 1.3",
        say("圣殿骑士团，听候差遣。", gloss="The Grand Master"),
    ])
    w("new_id", ["scoreboard players add #next rpg_al_id 1", "scoreboard players operation @s rpg_al_id = #next rpg_al_id"])
    w("spawn", [
        "summon minecraft:iron_golem ~ ~ ~ {Tags:[\"rpg.ally\",\"rpg.jqa\",\"rpg.jqwear\",%s,\"rpg.jqa.new\"],NoAI:1b,PlayerCreated:1b,"
        "Silent:1b,PersistenceRequired:1b,DeathLootTable:\"minecraft:empty\",CustomNameVisible:1b,CustomName:%s,"
        "Health:%df,active_effects:[{id:\"invisibility\",duration:-1,amplifier:0,show_particles:0b}],"
        "attributes:[{id:\"scale\",base:%sf},{id:\"max_health\",base:%df},{id:\"armor\",base:8f},{id:\"knockback_resistance\",base:0.6f}]}"
        % (",".join('"%s"' % t for t in UNIT_TAGS), json.dumps(ui.row_value(*name), ensure_ascii=False, separators=(",", ":")),
           HP, SCALE, HP),
        "execute as @e[%s,tag=rpg.jqa.new] run function %s/init" % (ALLY, B),
    ] + light_pillar(PALE_I) + fx.decal("sigil", 3.5, TEMPLAR_RED, pos="~ ~0.06 ~", kind="spin", life=30)
      + fx.decal("ring", 2, PALE_I, pos="~ ~0.1 ~", kind="ringm") + wave("minecraft:end_rod", 20, 0.3) + [
        "particle minecraft:totem_of_undying ~ ~1.2 ~ 0.4 0.8 0.4 0.4 30",
    ])
    w("init", [
        "tag @s remove rpg.jqa.new",
        "tp @s ~ ~ ~ ~ 0",
        "scoreboard players operation @s rpg_al_own = #own %s" % O,
        "scoreboard players set @s rpg_al_t 0",
        "scoreboard players set @s rpg_al_hp %d" % HP,
        "scoreboard players set @s rpg_al_b 30",
        "scoreboard players set @s rpg_al_cb 0",
        "scoreboard players set @s rpg_al_sk 0",
        "item replace entity @s weapon.offhand with %s" % GUARD,
        "scoreboard players set #fxt %s 60" % O,
    ])

    w("tick", [
        "# 每刻：有友军或残留特效时才做事。",
        "execute if entity @e[%s,limit=1] run scoreboard players set #fxt %s 40" % (ALLY, O),
        "execute unless score #fxt %s matches 1.. run return 0" % O,
        "scoreboard players remove #fxt %s 1" % O,
        "execute as @e[%s] at @s run function %s/unit" % (ALLY, B),
        "execute as @e[tag=rpg.jqa.fx] at @s run function %s/fx/tick" % B,
    ])
    w("unit", [
        "# 友军雅克每刻（as/at 他）。",
        "execute if entity @s[tag=rpg.jqa.down] run return run function %s/down_tick" % B,
        "scoreboard players add @s rpg_al_t 1",
        "execute unless items entity @s weapon.offhand minecraft:paper run return run function %s/fall" % B,
        "execute if score @s rpg_al_t matches %d.. run return run function %s/leave" % (LIFE, B),
        "execute if score @s rpg_al_t matches %d run %s" % (LIFE - 40, say("时候到了。愿主与你同在。", gloss="The Grand Master", who="@a[distance=..32]")),
        "execute store result score @s rpg_al_hp run data get entity @s Health 1",
        "# 重力（NoAI 的载体自己不会落下）",
        "execute if block ~ ~-0.05 ~ #minecraft:replaceable run tp @s ~ ~-0.5 ~",
        "tag @s add rpg.al.cur",
        "function %s/think" % B,
        "tag @s remove rpg.al.cur",
        "particle %s ~ ~1.2 ~ 0.3 0.6 0.3 0 1" % GOLD_DUST,
    ])
    w("think", [
        "# 正在出招：走时间线，不动。",
        "execute if score @s rpg_al_sk matches 1.. run return run function %s/move" % B,
        "scoreboard players remove @s rpg_al_b 1",
        "# 目标：最近的敌人（%d 格内，含隐身的 Boss 载体）" % SEEK_R,
        "tag @e[tag=rpg.al.aim] remove rpg.al.aim",
        "execute as @e[%s,distance=..%d,sort=nearest,limit=1] run tag @s add rpg.al.aim" % (FOE, SEEK_R),
        "execute unless entity @e[tag=rpg.al.aim,limit=1] run return run function %s/follow" % B,
        "execute if score @s rpg_al_b matches ..0 if entity @e[tag=rpg.al.aim,distance=..%s] run return run function %s/melee" % (MELEE_R, B),
        "execute if score @s rpg_al_b matches ..0 if entity @e[tag=rpg.al.aim,distance=%d..%d] if predicate %s/shoot_roll run return run function %s/shot" % (SHOT_MIN, SHOT_MAX, B, B),
        "execute unless entity @e[tag=rpg.al.aim,distance=..%s] facing entity @e[tag=rpg.al.aim,limit=1] feet rotated ~ 0 run function %s/step" % (MELEE_R - 0.6, B),
        "execute if entity @e[tag=rpg.al.aim,distance=..%s] facing entity @e[tag=rpg.al.aim,limit=1] feet run tp @s ~ ~ ~ ~ 0" % (MELEE_R - 0.6),
    ])
    wj(os.path.join(DP, "data", "rpg", "predicate", "jacques_ally", "shoot_roll.json"),
       {"condition": "minecraft:random_chance", "chance": 0.06})
    w("follow", [
        "# 没有敌人：跟着召唤他的人（离开 4 格以上就走过去，远过 24 格直接跟上）。",
        "scoreboard players operation #own %s = @s rpg_al_own" % O,
        "execute as @a if score @s rpg_al_id = #own %s run tag @s add rpg.al.me" % O,
        "execute if entity @a[tag=rpg.al.me,distance=24..] at @a[tag=rpg.al.me,limit=1] run tp @s ~ ~ ~",
        "execute unless entity @a[tag=rpg.al.me,distance=..4] facing entity @a[tag=rpg.al.me,limit=1] feet rotated ~ 0 run function %s/step" % B,
        "tag @a remove rpg.al.me",
    ])
    w("step", [
        "# 朝当前朝向走一步（as 他，rotated 走向）：前面空就走，前面一格高的台阶就上去。",
        "execute if block ^ ^0.3 ^0.6 #minecraft:replaceable if block ^ ^1.5 ^0.6 #minecraft:replaceable run return run tp @s ^ ^ ^%s ~ 0" % STEP,
        "execute if block ^ ^1.3 ^0.6 #minecraft:replaceable if block ^ ^2.3 ^0.6 #minecraft:replaceable run tp @s ^ ^1 ^%s ~ 0" % STEP,
    ])
    w("leave", [
        "# 20 秒到了：光柱里离开（as/at 他）。",
    ] + light_pillar(PALE_I) + fx.decal("ring", 2, PALE_I, pos="~ ~0.1 ~", kind="ringm") + wave("minecraft:end_rod", 16, 0.25) + [
        "particle minecraft:totem_of_undying ~ ~1.2 ~ 0.4 0.8 0.4 0.3 24",
        "playsound minecraft:block.beacon.deactivate player @a[distance=..32] ~ ~ ~ 1 1.2",
        "function %s/remove" % B,
    ])
    w("fall", [
        "# 死亡保护被吃掉：他倒下，1.5 秒后消失（敌人不再把他当目标）。",
        "tag @s add rpg.jqa.down",
    ] + ["tag @s remove %s" % t for t in UNIT_TAGS] + [
        "data merge entity @s {Invulnerable:1b}",
        "scoreboard players set @s rpg_al_mt 0",
        weapon("glaive"),
        anim("fall"),
        say("……抱歉，只能到这里了。", who="@a[distance=..32]"),
        "playsound minecraft:entity.player.death player @a[distance=..32] ~ ~ ~ 1 0.8",
    ])
    w("down_tick", [
        "scoreboard players add @s rpg_al_mt 1",
        "execute if score @s rpg_al_mt matches 24 run " + anim("down"),
        "execute if score @s rpg_al_mt matches 30.. run return run function %s/leave" % B,
    ])
    w("remove", ["execute on passengers run kill @s", "tp @s ~ -256 ~", "kill @s"])
    w("clear", ["# 清掉所有友军雅克与他们的特效。",
                "execute as @e[%s] at @s run function %s/remove" % (ALLY, B), "kill @e[tag=rpg.jqa.fx]"])


# =====================================================================================
# 招式：坟墓克星三连、竖琴弩
# =====================================================================================
def combat():
    w("melee", [
        "execute facing entity @e[tag=rpg.al.aim,limit=1] feet run tp @s ~ ~ ~ ~ 0",
        "scoreboard players set @s rpg_al_mt 0",
        "execute if score @s rpg_al_cb matches 0 run scoreboard players set @s rpg_al_sk 1",
        "execute if score @s rpg_al_cb matches 1 run scoreboard players set @s rpg_al_sk 2",
        "execute if score @s rpg_al_cb matches 2 run scoreboard players set @s rpg_al_sk 3",
        "execute if score @s rpg_al_cb matches 0 run " + anim("slash1"),
        "execute if score @s rpg_al_cb matches 1 run " + anim("slash2"),
        "execute if score @s rpg_al_cb matches 2 run " + anim("sweep"),
        "scoreboard players add @s rpg_al_cb 1",
        "execute if score @s rpg_al_cb matches 3.. run scoreboard players set @s rpg_al_cb 0",
    ])
    w("shot", [
        "execute facing entity @e[tag=rpg.al.aim,limit=1] feet run tp @s ~ ~ ~ ~ 0",
        "scoreboard players set @s rpg_al_mt 0",
        "scoreboard players set @s rpg_al_sk 4",
        weapon("harp1"), anim("load"),
    ])
    # 时间线：(招, 命中刻, 收招刻)；命中时刻同 Boss 战（原作事件）
    w("move", [
        "scoreboard players add @s rpg_al_mt 1",
        "execute if score @s rpg_al_sk matches 1 if score @s rpg_al_mt matches 7 run function %s/hit/front" % B,
        "execute if score @s rpg_al_sk matches 2 if score @s rpg_al_mt matches 9 run function %s/hit/front" % B,
        "execute if score @s rpg_al_sk matches 3 if score @s rpg_al_mt matches 3 run function %s/hit/sweep" % B,
        "execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 4 run " + weapon("harp2"),
        "execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 8 run " + weapon("harp3"),
        "execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 12 run " + weapon("harp4"),
        "execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 14 if entity @e[tag=rpg.al.aim] facing entity @e[tag=rpg.al.aim,limit=1] feet run tp @s ~ ~ ~ ~ 0",
        "execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 16 run " + anim("shoot"),
        "execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 16 run function %s/hit/bolt" % B,
        "execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 18 run " + weapon("harp1"),
        "execute if score @s rpg_al_sk matches 1 if score @s rpg_al_mt matches 14.. run function %s/move_end" % B,
        "execute if score @s rpg_al_sk matches 2 if score @s rpg_al_mt matches 18.. run function %s/move_end" % B,
        "execute if score @s rpg_al_sk matches 3 if score @s rpg_al_mt matches 16.. run function %s/move_end" % B,
        "execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 24.. run function %s/move_end" % B,
    ])
    w("move_end", ["scoreboard players set @s rpg_al_sk 0", "scoreboard players set @s rpg_al_b 3", weapon("glaive")])

    w("hit/front", [
        "# 下劈（as/at 他）：身前 2.3 格内的敌人",
        "execute positioned ^ ^ ^1.8 as @e[%s,distance=..2.3] run damage @s %d minecraft:mob_attack by @e[tag=rpg.al.cur,limit=1]" % (FOE, SLASH_DMG),
    ] + fx.slash("^ ^1.2 ^1.6", GOLD) + fx.slash("^ ^1.25 ^1.7", PALE, size=1.8, frame=1) + [
        "particle minecraft:crit ^ ^1 ^1.8 0.6 0.4 0.6 0.3 12",
        "particle minecraft:enchanted_hit ^ ^1.1 ^1.8 0.5 0.4 0.5 0.3 8",
    ])
    arc = []
    for deg in range(-60, 61, 20):
        a = math.radians(deg)
        arc.append((round(3.0 * math.sin(a), 2), round(3.0 * math.cos(a), 2)))
    w("hit/sweep", [
        "# 横扫（as/at 他）：身前约 80°、4.5 格内的敌人",
        "execute positioned ^ ^ ^1.4 as @e[%s,distance=..3.2] run damage @s %d minecraft:mob_attack by @e[tag=rpg.al.cur,limit=1]" % (FOE, SWEEP_DMG),
        "execute positioned ^ ^1.1 ^1.2 run %s" % fx.disp("crescent", color=GOLD_I),
        "execute as @e[tag=%s] positioned as @s run tp @s ~ ~ ~ ~ 0" % NEW,
    ] + fx.born(kind="sweep") + [
        "particle minecraft:sweep_attack ^ ^1 ^1.8 0.8 0.2 0.8 0 4",
    ] + ["particle minecraft:end_rod ^%s ^1.1 ^%s 0.15 0.15 0.15 0.05 2" % (x, z) for x, z in arc])
    w("hit/bolt", [
        "# 竖琴弩（as/at 他）：一道金色弩光直达目标",
        "execute positioned ~ ~1.45 ~ facing entity @e[tag=rpg.al.aim,limit=1] eyes positioned ^ ^ ^0.9 run function %s/hit/fly" % B,
        "scoreboard players set #d %s 0" % O,
    ] + fx.spark("^ ^1.45 ^1.1", PALE, size=1.3) + [
        "particle minecraft:electric_spark ^ ^1.45 ^1.2 0.15 0.15 0.15 0.4 8",
    ])
    w("hit/fly", [
        "# 弩光往前走（每 1 格一步，最多 %d 步），碰到目标就结算" % (SHOT_MAX + 2),
        "scoreboard players add #d %s 1" % O,
        "particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1 force",
        "particle %s ~ ~ ~ 0.02 0.02 0.02 0 1" % GOLD_DUST,
        "# 弩光朝目标的眼睛飞，目标的位置在脚底：在弩光下方 1.2 格处量",
        "execute positioned ~ ~-1.2 ~ if entity @e[tag=rpg.al.aim,distance=..1.5] run return run function %s/hit/bolt_hit" % B,
        "execute if entity @e[tag=rpg.al.aim,distance=..1.2] run return run function %s/hit/bolt_hit" % B,
        "execute unless block ~ ~ ~ #minecraft:replaceable run return 0",
        "execute if score #d %s matches ..%d positioned ^ ^ ^1 run function %s/hit/fly" % (O, SHOT_MAX + 2, B),
    ])
    w("hit/bolt_hit", [
        "execute as @e[tag=rpg.al.aim,limit=1] run damage @s %d minecraft:mob_projectile by @e[tag=rpg.al.cur,limit=1]" % SHOT_DMG,
    ] + fx.glyph("pop", 1.0, PALE, kind="pop") + [
        "particle minecraft:crit ~ ~ ~ 0.2 0.2 0.2 0.4 8",
        "playsound rpg:jacques.arrow player @a[distance=..16] ~ ~ ~ 0.6 1.2",
    ])


def debug():
    w("debug/summon", ["# 调试：在自己身前召一个友军雅克（不走冷却）。必须由玩家执行。",
                       "execute store result score #now %s run time query gametime" % O,
                       "execute unless score @s rpg_al_id matches 1.. run function %s/new_id" % B,
                       "scoreboard players operation #own %s = @s rpg_al_id" % O,
                       "execute rotated ~ 0 positioned ^ ^ ^1.5 run function %s/spawn" % B])
    w("debug/hand", ["# 调试：把一件圣殿誓约放到主手（替换主手原有物品）。", "item replace entity @s weapon.mainhand with " + oath_item()])
    w("debug/reset_cd", ["# 调试：清掉自己的圣殿誓约冷却。", "scoreboard players reset @s rpg_al_cd"])


def hook_first(name, entry):
    """Put entry first in #minecraft:<name> (the unit tags must be fresh before any fight reads them)."""
    tag = os.path.join(DP, "data", "minecraft", "tags", "function", name + ".json")
    with open(tag, encoding="utf-8") as fh:
        doc = json.load(fh)
    vals = [v for v in doc["values"] if v != entry]
    doc["values"] = [entry] + vals
    wj(tag, doc)


def resources():
    """The oath's sprite, model and item definition (assets/rpg/…/jacques_oath)."""
    import shutil
    a = os.path.join(RP, "assets", "rpg")
    os.makedirs(os.path.join(a, "textures", "item"), exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "jacques_ally_ref", "oath.png"), os.path.join(a, "textures", "item", "jacques_oath.png"))
    wj(os.path.join(a, "models", "item", "jacques_oath.json"),
       {"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/jacques_oath"}})
    wj(os.path.join(a, "items", "jacques_oath.json"), {"model": {"type": "minecraft:model", "model": "rpg:item/jacques_oath"}})


def main():
    if RP:
        resources()
    items()
    life()
    combat()
    debug()
    fx.build()
    hook_tag(DP, "load", "%s/load" % B, False)
    hook_first("tick", "%s/units" % B)
    hook_tag(DP, "tick", "%s/tick" % B, True)
    count = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("jacques_ally: %d functions" % count)


if __name__ == "__main__":
    main()
