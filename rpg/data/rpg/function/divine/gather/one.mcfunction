scoreboard players add @s rpg_lt_gather 1
execute as @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.prop,distance=..8] at @s facing entity @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.cross,distance=..8,limit=1,sort=nearest] feet run tp @s ^ ^ ^0.22
execute as @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.prop,distance=..8] at @s run particle minecraft:end_rod ~ ~0.08 ~ 0.08 0.03 0.08 0.01 2 force
execute positioned ^0 ^0.12 ^-1.58 run particle dust{color:[0.75,0.90,1.0],scale:1.4} ~ ~ ~ 0.25 0.05 0.25 0.02 8 force
execute if score @s rpg_lt_gather matches 24.. run return run function rpg:divine/gather/finish
