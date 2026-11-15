# stun：26 刻循环。由 add_holy_guards.py 生成。
execute if score @s rpg_ei_t matches 26.. run scoreboard players set @s rpg_ei_t 0
scoreboard players add @s rpg_ei_t 1
function rpg:end_illager/anim/stun/at
