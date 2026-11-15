scoreboard players add @s rpg_ei_ta 1
execute if score @s rpg_ei_ta matches 30 positioned ^ ^1.7 ^0.8 run function rpg:end_illager/ai/fire
execute if score @s rpg_ei_ta matches 62.. run function rpg:end_illager/ai/free
