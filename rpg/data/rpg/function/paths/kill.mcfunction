# 路径试炼与赐福的击杀钩子（as 击杀者；rpg:sephira/kill 末尾）
execute if score @s rpg_ps_30 matches 1 if predicate rpg:paths/day run scoreboard players add @s rpg_pa_30 1
execute if score @s rpg_ps_29 matches 1 if score @s rpg_fg_kx matches 5.. unless predicate rpg:paths/day run scoreboard players add @s rpg_pa_29 1
execute if score @s rpg_ps_28 matches 1 if entity @s[tag=rpg.pl.in] if score #moon rpg_pl matches 1.. run scoreboard players add @s rpg_pa_28 1
execute if score @s rpg_ps_28 matches 1 if entity @s[tag=rpg.pl.in] unless score #moon rpg_pl matches 1.. if score #rain rpg_pl matches 1.. run scoreboard players add @s rpg_pa_28 1
execute if score @s rpg_ps_23 matches 1 run function rpg:paths/low
execute if score @s rpg_ps_24 matches 2 run effect give @s minecraft:regeneration 2 1 true
