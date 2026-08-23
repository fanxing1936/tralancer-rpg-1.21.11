# 驱魔体系每刻入口。
# 魔化与 HUD 是玩家侧的，走 @a 一次；空缺者那一支带类型且过守卫。
execute as @a at @s run function rpg:taint/taint
execute as @a run function rpg:hud/hud
execute if entity @e[type=minecraft:villager,tag=!rpg.vac.seen,limit=1] run function rpg:vacant/mark
execute if entity @a[tag=rpg.h.holy_weapon_tag1] run function rpg:vacant/vacant
execute unless entity @a[tag=rpg.h.holy_weapon_tag1] if entity @e[type=minecraft:villager,tag=rpg.vacant,tag=rpg.hurt,limit=1] run function rpg:vacant/vacant
execute if entity @e[type=minecraft:item_display,tag=rpg.totem,limit=1] run function rpg:rite/tick
execute as @a[scores={rpg_rite=1..}] run scoreboard players remove @s rpg_rite 1

# 蔓延的节拍器。没有比一次记分板比较更便宜的守卫 ——
# 先数够 400 刻，再去找村民。
scoreboard players add #spread rpg_vac 1
execute if score #spread rpg_vac matches 400.. run function rpg:vacant/spread

# 七十二柱契约。三条全是玩家作用域（玩家表很短），
# 而且各自带着柱位判定 —— 没签那一柱的人连函数都不会进。
execute as @a[scores={rpg_pact_cd=1..}] run function rpg:pact/cd
execute if entity @a[tag=rpg.pact,scores={rpg_pact=5},limit=1] run function rpg:pact/samael
execute as @a[tag=rpg.pact,scores={rpg_pact=7}] at @s run function rpg:pact/mammon
execute as @a[scores={rpg_pact_t=1..}] run scoreboard players remove @s rpg_pact_t 1

# 三件老驱魔道具。每条都带类型且过守卫 —— 场上没有对应的东西就整段跳过。
execute if entity @e[type=minecraft:allay,tag=rpg.doll,limit=1] run function rpg:doll/doll
execute if entity @e[type=minecraft:area_effect_cloud,tag=!rpg.aec.seen,limit=1] run function rpg:rite/aec_scan
execute if entity @e[type=minecraft:area_effect_cloud,tag=rpg.holy_water,limit=1] run function rpg:rite/pool_tick

# 逆圣化受术者标签的寿命。两条都是玩家作用域，没在做仪式的人一条也进不去。
execute as @a[scores={rpg_inv=1..}] run scoreboard players remove @s rpg_inv 1
execute as @a[tag=rpg.inv.subject,scores={rpg_inv=..0}] run function rpg:rite/inv_abort
