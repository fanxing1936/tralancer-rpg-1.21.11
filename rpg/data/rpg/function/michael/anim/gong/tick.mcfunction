# gong：12 刻，播完回到 idle。由 add_michael_model.py 生成。
execute if score @s rpg_mkm_t matches 13.. run return run function rpg:michael/anim/enter/idle
scoreboard players add @s rpg_mkm_t 1
function rpg:michael/anim/gong/at
