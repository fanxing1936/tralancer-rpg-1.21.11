# walk：40 刻循环。由 add_abaddon_model.py 生成。
execute if score @s rpg_ab_t matches 40.. run scoreboard players set @s rpg_ab_t 0
scoreboard players add @s rpg_ab_t 1
function rpg:abaddon/anim/walk/at
