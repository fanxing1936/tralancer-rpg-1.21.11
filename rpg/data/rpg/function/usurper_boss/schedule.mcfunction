execute unless entity @e[tag=rpg.unit.f,distance=..25] run return 0
scoreboard players remove @s rpg_ub_b 1
execute if score @s rpg_ub_b matches 1.. run return 0
scoreboard players set @s rpg_ub_b 8
execute if score @s rpg_ub_n matches 3.. run return run function rpg:usurper_boss/pick
scoreboard players add @s rpg_ub_n 1
execute if score @s rpg_ub matches 1 run function rpg:usurper_boss/basic/1
execute if score @s rpg_ub matches 2 run function rpg:usurper_boss/basic/2
