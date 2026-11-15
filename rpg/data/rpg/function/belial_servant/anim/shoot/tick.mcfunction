# shoot：19 刻，播完回到 idle。由 add_lord_servants.py 生成。
execute if score @s rpg_bls_t matches 20.. run return run function rpg:belial_servant/anim/enter/idle
scoreboard players add @s rpg_bls_t 1
function rpg:belial_servant/anim/shoot/at
