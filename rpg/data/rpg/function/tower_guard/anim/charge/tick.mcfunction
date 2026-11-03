# charge：12 刻循环。由 add_tower_guard.py 生成。
execute if score @s rpg_tg_t matches 12.. run scoreboard players set @s rpg_tg_t 0
scoreboard players add @s rpg_tg_t 1
function rpg:tower_guard/anim/charge/at
