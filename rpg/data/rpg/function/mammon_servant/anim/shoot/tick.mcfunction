# shoot：49 刻，播完回到 idle。由 add_lord_servants.py 生成。
execute if score @s rpg_mms_t matches 50.. run return run function rpg:mammon_servant/anim/enter/idle
scoreboard players add @s rpg_mms_t 1
function rpg:mammon_servant/anim/shoot/at
