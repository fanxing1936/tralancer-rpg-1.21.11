scoreboard players add @s rpg_tg_ta 1
execute if score @s rpg_tg_ta matches 32 run function rpg:tower_guard/anim/enter/stun
execute if score @s rpg_tg_ta matches 62.. run function rpg:tower_guard/ai/stun_end
