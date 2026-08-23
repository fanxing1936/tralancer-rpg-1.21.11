# 以人偶为中心照一圈。
particle end_rod ~ ~0.4 ~ 0.25 0.3 0.25 0.01 2
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..12] at @s run function rpg:vacant/reveal
