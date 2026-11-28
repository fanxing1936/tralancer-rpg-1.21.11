# attack：37 刻，播完回到 idle。由 add_town_models.py 生成。
execute if score @s rpg_tw_m11_t matches 38.. run return run function rpg:town_models/town_hollow_big/anim/enter/idle
scoreboard players add @s rpg_tw_m11_t 1
function rpg:town_models/town_hollow_big/anim/attack/at
