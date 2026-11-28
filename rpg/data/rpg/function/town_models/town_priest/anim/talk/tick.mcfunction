# talk：30 刻，播完回到 idle。由 add_town_models.py 生成。
execute if score @s rpg_tw_m0_t matches 31.. run return run function rpg:town_models/town_priest/anim/enter/idle
scoreboard players add @s rpg_tw_m0_t 1
function rpg:town_models/town_priest/anim/talk/at
