# down：8 刻循环。由 add_michael_model.py 生成。
execute if score @s rpg_mkm_t matches 8.. run scoreboard players set @s rpg_mkm_t 0
scoreboard players add @s rpg_mkm_t 1
function rpg:michael/anim/down/at
