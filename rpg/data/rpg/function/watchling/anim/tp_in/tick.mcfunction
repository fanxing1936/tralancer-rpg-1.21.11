# tp_in：11 刻，播完回到 idle。由 add_michael_model.py 生成。
execute if score @s rpg_mkwm_t matches 12.. run return run function rpg:watchling/anim/enter/idle
scoreboard players add @s rpg_mkwm_t 1
function rpg:watchling/anim/tp_in/at
