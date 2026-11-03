# collide_stop：32 刻，播完回到 idle。由 add_tower_guard.py 生成。
execute if score @s rpg_tg_t matches 33.. run return run function rpg:tower_guard/anim/enter/idle
scoreboard players add @s rpg_tg_t 1
function rpg:tower_guard/anim/collide_stop/at
