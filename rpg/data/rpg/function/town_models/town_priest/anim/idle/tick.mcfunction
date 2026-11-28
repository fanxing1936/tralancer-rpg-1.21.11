# idle：67 刻循环。由 add_town_models.py 生成。
execute if score @s rpg_tw_m0_t matches 67.. run scoreboard players set @s rpg_tw_m0_t 0
scoreboard players add @s rpg_tw_m0_t 1
function rpg:town_models/town_priest/anim/idle/at
