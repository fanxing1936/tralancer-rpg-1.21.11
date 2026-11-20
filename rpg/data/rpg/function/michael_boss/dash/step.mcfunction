# 冲两格（as/at 他）：沿途碰到的记下，身后留火
execute positioned ^ ^ ^1 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ^ ^ ^1
execute at @s run function rpg:michael_boss/dash/fire
execute at @s run tag @e[tag=rpg.unit.f,distance=..1.5] add rpg.mkb.hit
execute at @s run execute positioned ^ ^ ^1 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ^ ^ ^1
execute at @s run function rpg:michael_boss/dash/fire
execute at @s run tag @e[tag=rpg.unit.f,distance=..1.5] add rpg.mkb.hit
execute at @s run particle minecraft:flame ~ ~1 ~ 0.4 0.6 0.4 0.03 6
