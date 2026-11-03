# attack：20 刻，播完回到 idle。由 add_vanguard.py 生成。
execute if score @s rpg_vg_t matches 21.. run return run function rpg:vanguard/anim/enter/idle
scoreboard players add @s rpg_vg_t 1
function rpg:vanguard/anim/attack/at
