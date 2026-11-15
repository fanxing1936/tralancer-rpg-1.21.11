# walk：16 刻循环。由 add_lord_servants.py 生成。
execute if score @s rpg_lcs_t matches 16.. run scoreboard players set @s rpg_lcs_t 0
scoreboard players add @s rpg_lcs_t 1
function rpg:lucifer_servant/anim/walk/at
