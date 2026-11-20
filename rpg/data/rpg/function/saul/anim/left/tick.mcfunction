# left：5 刻，播完回到 idle。由 add_saul_model.py 生成。
execute if score @s rpg_slm_t matches 6.. run return run function rpg:saul/anim/enter/idle
scoreboard players add @s rpg_slm_t 1
function rpg:saul/anim/left/at
