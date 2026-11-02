# summon：32 刻，播完回到 idle。由 add_leviathan_model.py 生成。
execute if score @s rpg_lv_t matches 33.. run return run function rpg:leviathan/anim/enter/idle
scoreboard players add @s rpg_lv_t 1
function rpg:leviathan/anim/summon/at
