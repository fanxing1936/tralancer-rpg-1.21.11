# walk：16 刻循环。由 add_vanguard.py 生成。
execute if score @s rpg_vg_t matches 16.. run scoreboard players set @s rpg_vg_t 0
scoreboard players add @s rpg_vg_t 1
function rpg:vanguard/anim/walk/at
