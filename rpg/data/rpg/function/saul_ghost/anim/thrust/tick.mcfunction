# thrust：7 刻，播完回到 idle。由 add_saul_model.py 生成。
execute if score @s rpg_slgm_t matches 8.. run return run function rpg:saul_ghost/anim/enter/idle
scoreboard players add @s rpg_slgm_t 1
function rpg:saul_ghost/anim/thrust/at
