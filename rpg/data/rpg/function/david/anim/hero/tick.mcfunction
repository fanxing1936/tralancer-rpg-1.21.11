# hero：40 刻，播完回到 idle。由 add_jacques_model.py 生成。
execute if score @s rpg_jqdm_t matches 41.. run return run function rpg:david/anim/enter/idle
scoreboard players add @s rpg_jqdm_t 1
function rpg:david/anim/hero/at
