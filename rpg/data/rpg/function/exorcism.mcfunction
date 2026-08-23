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
