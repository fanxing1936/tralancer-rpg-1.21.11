# idle：64 刻循环。由 add_beelzebub.py 生成。
execute if score @s rpg_bz_t matches 64.. run scoreboard players set @s rpg_bz_t 0
scoreboard players add @s rpg_bz_t 1
function rpg:beelzebub/anim/idle/at
