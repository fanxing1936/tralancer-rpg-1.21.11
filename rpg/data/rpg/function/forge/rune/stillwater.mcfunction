scoreboard players add @s rpg_fg_calm 1
execute if score @s rpg_fg_calm matches 60 run function rpg:forge/rune/stillwater_give
execute if score @s rpg_fg_calm matches 120.. run scoreboard players set @s rpg_fg_calm 60
