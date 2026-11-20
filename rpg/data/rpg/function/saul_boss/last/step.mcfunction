# 全速冲两格（as/at 他）
execute if block ^ ^0.5 ^1 #minecraft:replaceable if block ^ ^1.5 ^1 #minecraft:replaceable unless block ^ ^-0.5 ^1 #minecraft:replaceable run tp @s ^ ^ ^1
tag @e[tag=rpg.unit.f,distance=..1.5] add rpg.slb.hit
execute at @s if block ^ ^0.5 ^1 #minecraft:replaceable if block ^ ^1.5 ^1 #minecraft:replaceable unless block ^ ^-0.5 ^1 #minecraft:replaceable run tp @s ^ ^ ^1
execute at @s run tag @e[tag=rpg.unit.f,distance=..1.5] add rpg.slb.hit
execute at @s run particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~ ~1 ~ 0.3 0.5 0.3 0 6 force
execute at @s run particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.3 0.3 0 1
