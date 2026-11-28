# 开局里（as 玩家，还没有故乡）：一抽到国家就定下故乡、先排队去建，开局走完时多半已经建好
function rpg:town/home/pick
execute if score #nat rpg_tw matches -1 run return run scoreboard players reset @s rpg_tw_home
execute store result storage rpg:town h.i int 1 run scoreboard players get @s rpg_tw_home
function rpg:town/req with storage rpg:town h
