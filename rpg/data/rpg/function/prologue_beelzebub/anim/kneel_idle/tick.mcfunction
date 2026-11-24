# kneel_idle：60 刻循环。由 add_prologue_models.py 生成。
execute if score @s rpg_prbz_t matches 60.. run scoreboard players set @s rpg_prbz_t 0
scoreboard players add @s rpg_prbz_t 1
function rpg:prologue_beelzebub/anim/kneel_idle/at
