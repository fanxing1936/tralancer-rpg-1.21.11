execute if block ^ ^0.5 ^0.9 #minecraft:replaceable if block ^ ^1.5 ^0.9 #minecraft:replaceable run tp @s ^ ^ ^0.8
particle minecraft:flame ~ ~0.2 ~ 0.3 0.1 0.3 0.02 4
particle minecraft:flame ~ ~1 ~ 0.3 0.6 0.3 0.04 6
particle minecraft:dust_color_transition{from_color:[1.0,0.62,0.2],to_color:[0.35,0.04,0.0],scale:1.4} ~ ~1 ~ 0.35 0.6 0.35 0 4
particle minecraft:large_smoke ~ ~0.4 ~ 0.2 0.2 0.2 0.01 1
tag @e[tag=rpg.unit.f,distance=..1.6,tag=!rpg.jqb.rolled] add rpg.jqb.hit
tag @e[tag=rpg.unit,tag=rpg.jqb.hit] add rpg.jqb.rolled
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit] run damage @s 10 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1]
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit,tag=rpg.jqb.cursed] at @s run function rpg:jacques_boss/curse/pop
tag @e[tag=rpg.unit] remove rpg.jqb.hit
