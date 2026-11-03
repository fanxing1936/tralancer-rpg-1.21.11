# spread：24 刻，播完回到 idle。由 add_abaddon_model.py 生成。
execute if score @s rpg_ab_t matches 25.. run return run function rpg:abaddon/anim/enter/idle
scoreboard players add @s rpg_ab_t 1
function rpg:abaddon/anim/spread/at
