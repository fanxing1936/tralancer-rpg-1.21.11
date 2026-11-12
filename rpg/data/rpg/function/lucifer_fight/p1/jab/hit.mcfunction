tag @s add rpg.dm.cast
execute positioned ^ ^ ^1.8 as @a[distance=..1.8,gamemode=!spectator,gamemode=!creative] run function rpg:lucifer_fight/p1/jab/dmg
tag @s remove rpg.dm.cast
execute positioned ^ ^1.2 ^1.8 run particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.6} ~ ~ ~ 0.3 0.3 0.3 0.05 10
execute positioned ^ ^1.2 ^1.8 run particle crit ~ ~ ~ 0.3 0.3 0.3 0.2 8
