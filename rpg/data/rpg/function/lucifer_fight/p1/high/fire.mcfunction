tag @s add rpg.dm.cast
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:taint/sk1c_lift
tag @s remove rpg.dm.cast
execute as @e[tag=rpg.unit.f,distance=..8] at @s run function rpg:lucifer_fight/p1/fx/burst_small
playsound minecraft:entity.illusioner.prepare_blindness hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle end_rod ~ ~1 ~ 3 1 3 0.1 40
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.6} ~ ~1 ~ 3 1 3 0.05 30
