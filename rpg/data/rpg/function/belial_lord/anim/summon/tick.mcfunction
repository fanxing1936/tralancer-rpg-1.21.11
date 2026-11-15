# summon：82 刻，播完回到 idle。由 add_belial_model.py 生成。
execute if score @s rpg_bll_t matches 83.. run return run function rpg:belial_lord/anim/enter/idle
scoreboard players add @s rpg_bll_t 1
function rpg:belial_lord/anim/summon/at
