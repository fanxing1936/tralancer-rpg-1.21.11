# attack：25 刻，播完回到 idle。由 add_lord_servants.py 生成。
execute if score @s rpg_sms_t matches 26.. run return run function rpg:samael_servant/anim/enter/idle
scoreboard players add @s rpg_sms_t 1
function rpg:samael_servant/anim/attack/at
