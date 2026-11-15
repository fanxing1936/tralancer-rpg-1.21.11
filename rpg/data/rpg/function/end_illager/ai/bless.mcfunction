execute as @e[type=minecraft:vindicator,tag=rpg.hg,distance=..12] run effect give @s minecraft:regeneration 5 1 true
execute as @e[type=minecraft:vindicator,tag=rpg.hg,distance=..12] at @s run particle minecraft:happy_villager ~ ~1.4 ~ 0.4 0.6 0.4 0 10 normal
particle minecraft:end_rod ~ ~2.4 ~ 0.6 0.4 0.6 0.05 24 normal
playsound rpg:end_illager.heal hostile @a[distance=..24] ~ ~ ~ 1 1.4
