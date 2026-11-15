# attack：37 刻，播完回到 idle。由 add_holy_guards.py 生成。
execute if score @s rpg_rg_t matches 38.. run return run function rpg:royal_guard/anim/enter/idle
scoreboard players add @s rpg_rg_t 1
function rpg:royal_guard/anim/attack/at
