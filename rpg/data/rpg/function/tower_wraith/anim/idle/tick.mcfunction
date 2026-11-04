# idle：80 刻循环。由 add_tower_wraith.py 生成。
execute if score @s rpg_tw_t matches 80.. run scoreboard players set @s rpg_tw_t 0
scoreboard players add @s rpg_tw_t 1
function rpg:tower_wraith/anim/idle/at
