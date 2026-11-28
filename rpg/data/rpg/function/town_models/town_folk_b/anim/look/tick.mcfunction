# look：46 刻，播完回到 idle。由 add_town_models.py 生成。
execute if score @s rpg_tw_m8_t matches 47.. run return run function rpg:town_models/town_folk_b/anim/enter/idle
scoreboard players add @s rpg_tw_m8_t 1
function rpg:town_models/town_folk_b/anim/look/at
