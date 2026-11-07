playsound minecraft:entity.generic.splash player @a[distance=..24] ~ ~ ~ 1.2 0.65
playsound minecraft:block.conduit.attack.target player @a[distance=..24] ~ ~ ~ 0.8 0.7
particle nautilus ~ ~1 ~ 4 1.2 4 0.12 60
particle bubble_column_up ~ ~0.4 ~ 4 0.5 4 0.35 70
execute as @e[type=#rpg:seal_hostile,distance=..4] at @s run function rpg:pact/s/p2_out
execute as @e[type=#rpg:seal_hostile,distance=4.01..10] at @s run function rpg:pact/s/p2_in
particle dust{color:[0.31,0.62,0.94],scale:2} ~ ~1 ~ 3 1 3 0.04 30
