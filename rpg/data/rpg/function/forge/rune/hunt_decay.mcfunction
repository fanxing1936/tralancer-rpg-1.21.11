scoreboard players remove @s rpg_fg_mt 1
execute if score @s rpg_fg_mt matches 0 run scoreboard players reset @s rpg_fg_mark
execute if score @s rpg_fg_mt matches 1.. if score #c10 rpg_fg matches 0 run particle minecraft:crit ~ ~2.1 ~ 0.1 0.1 0.1 0 2
