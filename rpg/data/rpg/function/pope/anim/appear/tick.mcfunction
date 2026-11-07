# appear：36 刻，播完回到 idle。由 add_pope_model.py 生成。
execute if score @s rpg_pp_t matches 37.. run return run function rpg:pope/anim/enter/idle
scoreboard players add @s rpg_pp_t 1
function rpg:pope/anim/appear/at
