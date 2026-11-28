# 土径的一格（positioned 地表上一格）：只换地表那一层；#var 0 普通、1 雪原、2 沙漠
execute unless block ~ ~-1 ~ #rpg:town_pathable run return 0
execute if block ~ ~ ~ #rpg:town_plant run setblock ~ ~ ~ minecraft:air
execute if score #var rpg_tw matches 1 run return run setblock ~ ~-1 ~ minecraft:gravel
execute if score #var rpg_tw matches 2 run return run setblock ~ ~-1 ~ minecraft:smooth_sandstone
setblock ~ ~-1 ~ minecraft:gravel
