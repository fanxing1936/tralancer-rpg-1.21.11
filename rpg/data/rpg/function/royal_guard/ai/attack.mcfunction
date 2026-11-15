scoreboard players add @s rpg_rg_ta 1
execute if score @s rpg_rg_ta matches 12 positioned ^ ^ ^1.6 run function rpg:royal_guard/ai/slam
execute if score @s rpg_rg_ta matches 37.. run function rpg:royal_guard/ai/rest_start
