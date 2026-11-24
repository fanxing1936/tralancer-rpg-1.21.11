# 放完自己循环（as 玩家）
scoreboard players remove @s rpg_ob_mt 1
execute if score @s rpg_ob_mt matches 1.. run return 0
execute if score @s rpg_ob_mi matches 1 run return run function rpg:onboard/music/intro
execute if score @s rpg_ob_mi matches 2 run return run function rpg:onboard/music/flow
