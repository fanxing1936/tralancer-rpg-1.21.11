# idle：42 刻循环。由 add_usurper_model.py 生成。
execute if score @s rpg_usm_t matches 42.. run scoreboard players set @s rpg_usm_t 0
scoreboard players add @s rpg_usm_t 1
function rpg:usurper/anim/idle/at
