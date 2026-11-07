playsound minecraft:entity.ravager.roar player @a[distance=..24] ~ ~ ~ 0.8 1.3
execute as @e[type=#rpg:seal_hostile,distance=..14,sort=nearest,limit=1] at @s run function rpg:pact/s/p5_hit
particle dust{color:[1.0,0.36,0.32],scale:2} ~ ~1 ~ 3 1 3 0.04 30
