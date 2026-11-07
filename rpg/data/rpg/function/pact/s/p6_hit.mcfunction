effect give @s minecraft:glowing 6 0 true
effect give @s minecraft:weakness 6 1 true
tag @s add rpg.pact.lured
damage @s 4 minecraft:magic by @e[type=#rpg:seal_hostile,tag=!rpg.pact.lured,distance=..8,sort=nearest,limit=1]
tag @s remove rpg.pact.lured
