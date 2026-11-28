# attack：16 刻，播完回到 idle。由 add_town_models.py 生成。
execute if score @s rpg_tw_m6_t matches 17.. run return run function rpg:town_models/town_inquisitor/anim/enter/idle
scoreboard players add @s rpg_tw_m6_t 1
function rpg:town_models/town_inquisitor/anim/attack/at
