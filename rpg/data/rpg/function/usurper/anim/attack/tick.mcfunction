# attack：21 刻，播完回到 idle。由 add_usurper_model.py 生成。
execute if score @s rpg_usm_t matches 22.. run return run function rpg:usurper/anim/enter/idle
scoreboard players add @s rpg_usm_t 1
function rpg:usurper/anim/attack/at
