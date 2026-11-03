# cast：36 刻，播完回到 idle。由 add_tower_wraith.py 生成。
execute if score @s rpg_tw_t matches 37.. run return run function rpg:tower_wraith/anim/enter/idle
scoreboard players add @s rpg_tw_t 1
function rpg:tower_wraith/anim/cast/at
