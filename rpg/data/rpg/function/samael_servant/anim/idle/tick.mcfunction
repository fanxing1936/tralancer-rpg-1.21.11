# idle：99 刻循环。由 add_lord_servants.py 生成。
execute if score @s rpg_sms_t matches 99.. run scoreboard players set @s rpg_sms_t 0
scoreboard players add @s rpg_sms_t 1
function rpg:samael_servant/anim/idle/at
