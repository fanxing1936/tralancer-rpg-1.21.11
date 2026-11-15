# rise：99 刻，播完回到 idle。由 add_mammon_model.py 生成。
execute if score @s rpg_mml_t matches 100.. run return run function rpg:mammon_lord/anim/enter/idle
scoreboard players add @s rpg_mml_t 1
function rpg:mammon_lord/anim/rise/at
