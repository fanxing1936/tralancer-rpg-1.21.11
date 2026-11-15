# idle：20 刻循环。由 add_prime_enchanter_model.py 生成。
execute if score @s rpg_pe_t matches 20.. run scoreboard players set @s rpg_pe_t 0
scoreboard players add @s rpg_pe_t 1
function rpg:prime_enchanter/anim/idle/at
