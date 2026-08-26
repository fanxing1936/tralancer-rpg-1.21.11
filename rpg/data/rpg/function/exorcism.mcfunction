# 驱魔体系每刻入口。
# 魔化与 HUD 是玩家侧的，走 @a 一次；空缺者那一支带类型且过守卫。
# 上位契约玩家状态先于魔化与 HUD 结算。
execute as @a at @s run function rpg:divine/player_tick
# 终末圣裁只读取本刻已经存在的受击标记，不新增伤害扫描。
execute if entity @a[scores={rpg_lt_judge=1..},limit=1] run function rpg:divine/judgment/scan
execute as @a at @s run function rpg:taint/taint
execute as @a run function rpg:hud/hud
execute if entity @e[type=minecraft:villager,tag=!rpg.vac.seen,limit=1] run function rpg:vacant/mark
execute if entity @a[tag=rpg.holy] run function rpg:vacant/vacant
execute unless entity @a[tag=rpg.holy] if entity @e[type=minecraft:villager,tag=rpg.vacant,tag=rpg.hurt,limit=1] run function rpg:vacant/vacant
execute if entity @e[type=minecraft:item_display,tag=rpg.totem,limit=1] run function rpg:rite/tick
execute as @a[scores={rpg_rite=1..}] run scoreboard players remove @s rpg_rite 1

# 蔓延的节拍器。没有比一次记分板比较更便宜的守卫 ——
# 先数够 400 刻，再去找村民。
scoreboard players add #spread rpg_vac 1
execute if score #spread rpg_vac matches 400.. run function rpg:vacant/spread

# 死亡探针。场上没有标记就整段跳过。
execute if entity @e[type=minecraft:marker,tag=rpg.demon.soul,limit=1] run execute as @e[type=minecraft:marker,tag=rpg.demon.soul] run function rpg:taint/demon_soul

# 降临者的十分钟寿命。带类型且过守卫 —— 场上没有就整段跳过。
execute if entity @e[type=minecraft:vindicator,tag=rpg.advent,limit=1] run execute as @e[type=minecraft:vindicator,tag=rpg.advent] at @s run function rpg:taint/advent_tick

# 七十二柱契约。三条全是玩家作用域（玩家表很短），
# 而且各自带着柱位判定 —— 没签那一柱的人连函数都不会进。
execute as @a[scores={rpg_pact_cd=1..}] run function rpg:pact/cd
execute if entity @a[tag=rpg.pact,scores={rpg_pact=5},limit=1] run function rpg:pact/samael
execute as @a[tag=rpg.pact,scores={rpg_pact=7}] at @s run function rpg:pact/mammon
execute as @a[scores={rpg_pact_t=1..}] run scoreboard players remove @s rpg_pact_t 1

# 玛门的弓。弓没有「射出去了」这个触发器，只能在拉弓之后开一个几刻的
# 窗口，反过来从箭那头认。窗口分数不为零的人才进 —— 没碰过这把弓的
# 人一条也不欠。
execute as @a[scores={rpg_mam_win=1..}] at @s run function rpg:mammon/watch

# 三件老驱魔道具。每条都带类型且过守卫 —— 场上没有对应的东西就整段跳过。
execute if entity @e[type=minecraft:allay,tag=rpg.doll,limit=1] run function rpg:doll/doll
execute if entity @e[type=minecraft:area_effect_cloud,tag=!rpg.aec.seen,limit=1] run function rpg:rite/aec_scan
execute if entity @e[type=minecraft:area_effect_cloud,tag=rpg.holy_water,limit=1] run function rpg:rite/pool_tick

# 逆圣化受术者标签的寿命。两条都是玩家作用域，没在做仪式的人一条也进不去。
execute as @a[scores={rpg_inv=1..}] run scoreboard players remove @s rpg_inv 1
execute as @a[tag=rpg.inv.subject,scores={rpg_inv=..0}] run function rpg:rite/inv_abort
# 反仪式临时实体均有显式类型、标签与存在性守卫。
execute if entity @e[type=minecraft:armor_stand,tag=rpg.counter.name,limit=1] run execute as @e[type=minecraft:armor_stand,tag=rpg.counter.name] at @s run function rpg:inquest/counter/name_tick
execute if entity @e[type=minecraft:item_display,tag=rpg.rite.prop,limit=1] run execute as @e[type=minecraft:item_display,tag=rpg.rite.prop] run function rpg:inquest/tool/prop_tick

# 罪仆生态：仅场上确有罪仆时推进十刻节拍。
execute if entity @e[tag=rpg.demon.minion,limit=1] run function rpg:minion/tick

# 生命之树粒子阵：有锚点时才推进十刻刷新。
execute if entity @e[type=minecraft:marker,tag=rpg.ritual.life_tree,limit=1] run function rpg:ritual/life_tree/tick

# 卡巴拉血契输入冷却；仅处理实际使用过仪式物品的玩家。
execute as @a[scores={rpg_lt_usecd=1..}] run scoreboard players remove @s rpg_lt_usecd 1

# Daath 汇聚动画：只有正在转化的生命之树才进入。
execute if entity @e[type=minecraft:marker,tag=rpg.lt.gathering,limit=1] run function rpg:divine/gather/step


# 第一章：仅在控制器存在时进入一次有界状态机。
execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] at @s run function rpg:campaign/beelzebub/tick

execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] at @s run function rpg:campaign/beelzebub/ui/tick


# 无尽驱魔控制器：公共 Bossbar 只允许一个活动实例。
execute as @a[tag=rpg.end.member] unless entity @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] run function rpg:endless/member/stale_cleanup
execute if entity @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] run execute as @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] at @s run function rpg:endless/tick
