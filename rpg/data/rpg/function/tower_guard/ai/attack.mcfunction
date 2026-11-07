scoreboard players add @s rpg_tg_ta 1
execute if score @s rpg_tg_ta matches 16 positioned ^ ^ ^1.6 run function rpg:tower_guard/ai/attack_hit
execute if score @s rpg_tg_ta matches 32.. run function rpg:tower_guard/ai/attack_end
