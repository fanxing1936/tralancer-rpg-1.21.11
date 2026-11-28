# 里程：各种移动的厘米数加起来，每满 1000 格给一份
scoreboard players operation @s rpg_xd += @s rpg_xs_0
scoreboard players set @s rpg_xs_0 0
scoreboard players operation @s rpg_xd += @s rpg_xs_1
scoreboard players set @s rpg_xs_1 0
scoreboard players operation @s rpg_xd += @s rpg_xs_2
scoreboard players set @s rpg_xs_2 0
scoreboard players operation @s rpg_xd += @s rpg_xs_3
scoreboard players set @s rpg_xs_3 0
scoreboard players operation @s rpg_xd += @s rpg_xs_4
scoreboard players set @s rpg_xs_4 0
scoreboard players operation @s rpg_xd += @s rpg_xs_5
scoreboard players set @s rpg_xs_5 0
scoreboard players operation @s rpg_xd += @s rpg_xs_6
scoreboard players set @s rpg_xs_6 0
scoreboard players operation @s rpg_xd += @s rpg_xs_7
scoreboard players set @s rpg_xs_7 0
execute if score @s rpg_xd matches 100000.. run function rpg:explore/km
