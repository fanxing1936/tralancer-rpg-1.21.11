# strong：73 刻，播完回到 idle。由 add_holy_guards.py 生成。
execute if score @s rpg_ei_t matches 74.. run return run function rpg:end_illager/anim/enter/idle
scoreboard players add @s rpg_ei_t 1
function rpg:end_illager/anim/strong/at
