tag @s add rpg.dm.cast
execute positioned ^ ^ ^3 as @a[distance=..3.2,gamemode=!spectator,gamemode=!creative] run function rpg:lucifer_fight/melee/hit
tag @s remove rpg.dm.cast
execute positioned ^ ^ ^3 run particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.3 ~ 1.6 0.2 1.6 0.15 60
execute positioned ^ ^ ^3 run particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.6} ~ ~0.5 ~ 1.2 0.3 1.2 0.05 30
execute positioned ^ ^ ^3 run particle explosion ~ ~0.5 ~ 0.6 0.2 0.6 0 2
execute positioned ^ ^ ^3 run function rpg:lucifer_fight/melee/fx
