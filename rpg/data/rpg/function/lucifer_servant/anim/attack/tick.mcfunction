# attack：14 刻，播完回到 idle。由 add_lord_servants.py 生成。
execute if score @s rpg_lcs_t matches 15.. run return run function rpg:lucifer_servant/anim/enter/idle
scoreboard players add @s rpg_lcs_t 1
function rpg:lucifer_servant/anim/attack/at
