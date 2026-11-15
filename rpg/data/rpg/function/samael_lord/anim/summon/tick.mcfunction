# summon：42 刻，播完回到 idle。由 add_samael_model.py 生成。
execute if score @s rpg_sml_t matches 43.. run return run function rpg:samael_lord/anim/enter/idle
scoreboard players add @s rpg_sml_t 1
function rpg:samael_lord/anim/summon/at
