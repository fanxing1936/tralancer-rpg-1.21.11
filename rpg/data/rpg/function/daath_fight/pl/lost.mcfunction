# 判负：它按住你的额头
execute if score @s rpg_dt_pt matches 1 run effect give @s minecraft:blindness 4 0 true
execute if score @s rpg_dt_pt matches 1 run effect give @s minecraft:resistance 6 4 true
execute if score @s rpg_dt_pt matches 1 run effect give @s minecraft:slowness 4 6 true
execute if score @s rpg_dt_pt matches 50.. run function rpg:daath_fight/pl/lost_go
