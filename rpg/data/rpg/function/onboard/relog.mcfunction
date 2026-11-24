# 中途退出又回来：回到黑屏，重新弹出当前这一步
scoreboard players set @s rpg_ob_lv 0
# 旁白听到一半退出：回来从头放（配乐也要重新起）
execute if entity @s[tag=rpg.ob.intro] run function rpg:onboard/intro/stop
scoreboard players set @s rpg_ob_mt 0
execute if score @s rpg_ob matches 1 run tag @s remove rpg.ob.queued
execute if score @s rpg_ob matches 1 run return run scoreboard players set @s rpg_ob_t 0
function rpg:onboard/hold/enter
tag @s add rpg.ob.wait
scoreboard players set @s rpg_ob_t 0
