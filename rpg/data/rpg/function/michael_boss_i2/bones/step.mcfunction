execute positioned ^ ^ ^1.84 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ^ ^ ^1.84
execute at @s run tag @e[tag=rpg.unit.f,distance=..1.5] add rpg.mkb.hit
execute at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.02 4
