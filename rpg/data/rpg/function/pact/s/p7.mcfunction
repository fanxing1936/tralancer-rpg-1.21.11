playsound minecraft:block.chain.break player @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:block.amethyst_block.chime player @a[distance=..24] ~ ~ ~ 1 0.7
particle wax_on ~ ~1 ~ 3 1 3 0.1 56
execute as @e[type=#rpg:seal_hostile,distance=..8] at @s run function rpg:pact/s/p7_hit
particle dust{color:[0.9,0.64,0.24],scale:2} ~ ~1 ~ 3 1 3 0.04 30
