tag @e[tag=rpg.legacy.target] remove rpg.legacy.target
tag @e[distance=..1.2,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows,limit=1,sort=nearest] add rpg.legacy.target
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:levitation 2 2 true
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:glowing 2 0 true
particle minecraft:bubble_pop ~ ~ ~ 0.6 0.6 0.6 0.08 28 force
playsound minecraft:entity.generic.splash player @a[distance=..16] ~ ~ ~ 0.7 1.4
tag @e[tag=rpg.legacy.target,limit=1] remove rpg.legacy.target
kill @s
