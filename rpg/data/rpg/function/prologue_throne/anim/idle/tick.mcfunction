# idle：160 刻循环。由 add_prologue_models.py 生成。
execute if score @s rpg_prth_t matches 160.. run scoreboard players set @s rpg_prth_t 0
scoreboard players add @s rpg_prth_t 1
function rpg:prologue_throne/anim/idle/at
