execute as @e[scores={absorption=0..},tag=rpg.e.chest_absorption_tag1] at @s store result score @s random run random value 1..5
execute as @e[scores={absorption=0..,random=1},tag=rpg.e.chest_absorption_tag1] at @s run effect give @s absorption 5 1 true
execute as @e[scores={absorption=0..,random=1},tag=rpg.e.chest_absorption_tag1] at @s run particle dust_color_transition{from_color:[1.0,0.92,0.0],to_color:[0.5,1.0,0.0],scale:1} ~0.25 ~1.5 ~0.25 -0.5 -0.5 -0.5 1 100
scoreboard players reset * random
scoreboard players reset * absorption

execute as @e[scores={boom=1..3},tag=rpg.e.chest_boom_tag1] at @s run execute positioned ~ ~ ~ run function rpg:effect/pseudo_explosion/owned_p5
execute as @e[scores={boom=1..3},tag=rpg.e.chest_boom_tag1] at @s run particle explosion ~1 ~1.5 ~1 -2 -2 -2 1 50 force
execute as @e[scores={boom=1..3},tag=rpg.e.chest_boom_tag1] at @s run kill

execute as @e[scores={health=0..3},tag=rpg.e.chest_health_tag1] at @s run effect give @s strength 5 2 true
execute as @e[scores={health=0..3},tag=rpg.e.chest_health_tag1] at @s run particle dust_color_transition{from_color:[0.9,0.66,0.0],to_color:[1.0,0.58,0.0],scale:1} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 10
