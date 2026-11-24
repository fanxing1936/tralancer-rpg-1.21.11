# 以这位奢侈品商人为执行者播放 examine。
execute unless entity @s[type=minecraft:villager,tag=rpg.mer.model.luxury] run return 0
execute at @s run function rpg:merchant_luxury/anim/enter/examine
execute at @s run playsound minecraft:entity.villager.ambient neutral @a[distance=..16] ~ ~ ~ 1 1
