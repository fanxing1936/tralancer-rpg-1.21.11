particle end_rod ~ ~0.6 ~ 0.4 0.5 0.4 0.05 60
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:2} ~ ~0.8 ~ 0.5 0.6 0.5 0.04 80
particle minecraft:flash{color:16773800} ~ ~0.8 ~ 0 0 0 0 1
playsound minecraft:block.beacon.activate player @a[distance=..24] ~ ~ ~ 1 1.2
execute as @a[distance=..8] run function rpg:hud/m33
