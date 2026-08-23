particle end_rod ~ ~0.6 ~ 0.4 0.5 0.4 0.05 60
particle dust{color:[1.0,0.98,0.86],scale:2} ~ ~0.8 ~ 0.5 0.6 0.5 0.04 80
particle minecraft:flash{color:16777200} ~ ~0.8 ~ 0 0 0 0 1
playsound minecraft:block.beacon.activate player @a[distance=..24] ~ ~ ~ 1 1.2
execute as @a[distance=..8] run function rpg:hud/m14
