# stun：31 刻循环。由 add_holy_guards.py 生成。
execute if score @s rpg_rg_t matches 31.. run scoreboard players set @s rpg_rg_t 0
scoreboard players add @s rpg_rg_t 1
function rpg:royal_guard/anim/stun/at
