# 赢了：上浮
execute if score @s rpg_dt_pt matches 1 run effect give @s minecraft:levitation 4 1 true
particle minecraft:end_rod ~ ~0.6 ~ 0.6 0.8 0.6 0.02 4
execute if score @s rpg_dt_pt matches 50 run effect give @s minecraft:blindness 2 0 true
execute if score @s rpg_dt_pt matches 70.. run function rpg:daath_fight/pl/won
