execute at @s as @a[distance=..18,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m40
particle dust{color:[0.71,0.85,0.34],scale:2.6} ~ ~1 ~ 1.4 1 1.4 0.04 42 force
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..32] ~ ~ ~ 1 0.65
