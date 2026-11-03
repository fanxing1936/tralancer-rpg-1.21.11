# walk：20 刻循环。由 add_sunken_skeleton.py 生成。
execute if score @s rpg_sk_t matches 20.. run scoreboard players set @s rpg_sk_t 0
scoreboard players add @s rpg_sk_t 1
function rpg:sunken_skeleton/anim/walk/at
