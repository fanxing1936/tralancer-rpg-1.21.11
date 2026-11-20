# roll_f：12 刻，播完回到 idle。由 add_saul_model.py 生成。
execute if score @s rpg_slgm_t matches 13.. run return run function rpg:saul_ghost/anim/enter/idle
scoreboard players add @s rpg_slgm_t 1
function rpg:saul_ghost/anim/roll_f/at
