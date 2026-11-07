# idle：80 刻循环。由 add_pope_model.py 生成。
execute if score @s rpg_pp_t matches 80.. run scoreboard players set @s rpg_pp_t 0
scoreboard players add @s rpg_pp_t 1
function rpg:pope/anim/idle/at
