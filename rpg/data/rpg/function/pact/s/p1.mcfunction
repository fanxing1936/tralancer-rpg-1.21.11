playsound minecraft:entity.phantom.flap player @a[distance=..24] ~ ~ ~ 1 0.55
playsound minecraft:entity.ender_dragon.flap player @a[distance=..24] ~ ~ ~ 0.7 1.45
particle dragon_breath ~ ~1.5 ~ 3 1.2 3 0.08 48
execute as @e[type=#rpg:seal_hostile,distance=..8] at @s run function rpg:pact/s/p1_hit
particle dust{color:[0.37,0.84,0.55],scale:2} ~ ~1 ~ 3 1 3 0.04 30
