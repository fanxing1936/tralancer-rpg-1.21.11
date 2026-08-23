particle sculk_soul ~ ~1.2 ~ 0.3 0.4 0.3 0.03 12
execute as @e[type=minecraft:villager,tag=!rpg.vacant,distance=..8,limit=1,sort=nearest] at @s run function rpg:vacant/take
