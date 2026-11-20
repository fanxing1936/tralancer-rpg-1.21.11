# roll_r：15 刻，播完回到 idle。由 add_michael_spirit_model.py 生成。
execute if score @s rpg_mis_t matches 16.. run return run function rpg:michael_spirit/anim/enter/idle
scoreboard players add @s rpg_mis_t 1
function rpg:michael_spirit/anim/roll_r/at
