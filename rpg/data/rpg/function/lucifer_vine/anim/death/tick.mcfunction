# death：35 刻，播完回到 idle。由 add_lucifer_vine_model.py 生成。
execute if score @s rpg_luv_t matches 36.. run return run function rpg:lucifer_vine/anim/enter/idle
scoreboard players add @s rpg_luv_t 1
function rpg:lucifer_vine/anim/death/at
