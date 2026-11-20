# 冲刺一格（as/at 他）：沿途碰到的人记下
execute if block ^ ^0.5 ^1.2 #minecraft:replaceable if block ^ ^1.5 ^1.2 #minecraft:replaceable unless block ^ ^-0.5 ^1.2 #minecraft:replaceable run tp @s ^ ^ ^1.2
tag @e[tag=rpg.unit.f,distance=..1.4] add rpg.slb.hit
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~ ~1 ~ 0.25 0.5 0.25 0 3
particle minecraft:cloud ~ ~0.1 ~ 0.2 0 0.2 0.01 1
