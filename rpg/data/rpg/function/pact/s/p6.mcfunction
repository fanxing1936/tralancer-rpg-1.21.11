playsound minecraft:entity.illusioner.prepare_blindness player @a[distance=..24] ~ ~ ~ 1 0.7
particle witch ~ ~1 ~ 3 1 3 0.2 56
execute as @e[type=#rpg:seal_hostile,distance=..8] at @s run function rpg:pact/s/p6_hit
particle dust{color:[0.85,0.48,0.85],scale:2} ~ ~1 ~ 3 1 3 0.04 30
