# 以载体执行，读取它自己的位置和朝向。
execute unless entity @s[type=minecraft:zombie] run return 0
execute at @s run function rpg:town_models/town_hollow_big/dress_at
