tag @e[tag=rpg.legacy.target] remove rpg.legacy.target
tag @e[distance=..1.2,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows,limit=1,sort=nearest] add rpg.legacy.target
execute as @e[tag=rpg.legacy.target,limit=1] run data merge entity @s {Fire:100s}
execute on origin run damage @e[tag=rpg.legacy.target,limit=1] 5 minecraft:on_fire by @s
particle minecraft:flame ~ ~ ~ 0.7 0.7 0.7 0.08 35 force
playsound minecraft:entity.blaze.shoot player @a[distance=..16] ~ ~ ~ 0.8 0.8
tag @e[tag=rpg.legacy.target,limit=1] remove rpg.legacy.target
kill @s
