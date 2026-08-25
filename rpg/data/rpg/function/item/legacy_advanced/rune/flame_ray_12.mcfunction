particle flame ~ ~ ~ 0.12 0.12 0.12 0.02 3 force
execute if entity @e[distance=..0.75,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker,type=!minecraft:armor_stand,limit=1,sort=nearest] run damage @e[distance=..0.75,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker,type=!minecraft:armor_stand,limit=1,sort=nearest] 17 minecraft:in_fire by @s
