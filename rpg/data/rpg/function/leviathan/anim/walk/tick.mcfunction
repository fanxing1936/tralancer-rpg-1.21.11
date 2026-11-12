# walk：16 刻循环。由 add_leviathan_model.py 生成。
execute if score @s rpg_lv_t matches 16.. run scoreboard players set @s rpg_lv_t 0
scoreboard players add @s rpg_lv_t 1
function rpg:leviathan/anim/walk/at
