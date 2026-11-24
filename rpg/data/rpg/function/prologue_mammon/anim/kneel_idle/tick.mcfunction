# kneel_idle：60 刻循环。由 add_prologue_models.py 生成。
execute if score @s rpg_prmm_t matches 60.. run scoreboard players set @s rpg_prmm_t 0
scoreboard players add @s rpg_prmm_t 1
function rpg:prologue_mammon/anim/kneel_idle/at
