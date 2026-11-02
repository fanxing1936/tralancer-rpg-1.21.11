# attack：16 刻，播完回到 idle。由 add_sunken_skeleton.py 生成。
execute if score @s rpg_sk_t matches 17.. run return run function rpg:sunken_skeleton/anim/enter/idle
scoreboard players add @s rpg_sk_t 1
function rpg:sunken_skeleton/anim/attack/at
