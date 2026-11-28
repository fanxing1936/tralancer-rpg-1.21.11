# idle：100 刻循环。由 add_town_models.py 生成。
execute if score @s rpg_tw_m7_t matches 100.. run scoreboard players set @s rpg_tw_m7_t 0
scoreboard players add @s rpg_tw_m7_t 1
function rpg:town_models/town_folk_a/anim/idle/at
