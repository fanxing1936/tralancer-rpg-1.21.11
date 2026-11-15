execute as @e[tag=rpg.unit.f,distance=..40] at @s run function rpg:usurper_boss/over/warn_at
execute at @s positioned ^0.11 ^2.44 ^0.22 run function rpg:usurper_boss/slam/charge
playsound minecraft:block.beacon.ambient hostile @a[distance=..48] ~ ~ ~ 1.4 1.8
