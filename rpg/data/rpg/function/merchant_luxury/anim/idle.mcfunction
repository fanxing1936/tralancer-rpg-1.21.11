# 以这位奢侈品商人为执行者播放 idle。
execute unless entity @s[type=minecraft:villager,tag=rpg.mer.model.luxury] run return 0
execute at @s run function rpg:merchant_luxury/anim/enter/idle
