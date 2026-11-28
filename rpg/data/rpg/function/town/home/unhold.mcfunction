tag @s remove rpg.tw.wait
effect clear @s minecraft:blindness
gamemode survival @s
execute if score @s rpg_tw_gm matches 1 run gamemode creative @s
execute if score @s rpg_tw_gm matches 2 run gamemode adventure @s
