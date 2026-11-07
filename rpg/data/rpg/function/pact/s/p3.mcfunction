playsound minecraft:block.amethyst_block.resonate player @a[distance=..24] ~ ~ ~ 1 0.35
playsound minecraft:entity.warden.heartbeat player @a[distance=..24] ~ ~ ~ 1 0.42
particle sculk_soul ~ ~1 ~ 4 1 4 0.04 56
execute as @e[type=#rpg:seal_hostile,distance=..10] at @s run function rpg:pact/s/p3_hit
particle dust{color:[0.65,0.69,0.79],scale:2} ~ ~1 ~ 3 1 3 0.04 30
