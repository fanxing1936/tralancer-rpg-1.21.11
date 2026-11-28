# 这座镇建不起来：换同国的另一座；两座都不行就往后换
execute if score @s rpg_tw_home matches 11.. run return run scoreboard players remove @s rpg_tw_home 10
scoreboard players add @s rpg_tw_home 10
execute store result storage rpg:town h.i int 1 run scoreboard players get @s rpg_tw_home
function rpg:town/home/other_m with storage rpg:town h
