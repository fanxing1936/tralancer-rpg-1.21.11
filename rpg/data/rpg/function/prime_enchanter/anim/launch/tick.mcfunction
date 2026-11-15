# launch：79 刻，播完回到 idle。由 add_prime_enchanter_model.py 生成。
execute if score @s rpg_pe_t matches 80.. run return run function rpg:prime_enchanter/anim/enter/idle
scoreboard players add @s rpg_pe_t 1
function rpg:prime_enchanter/anim/launch/at
