tag @s add rpg.fg.from
execute anchored feet positioned ^ ^ ^2 run particle minecraft:explosion ~ ~0.3 ~ 0.4 0.1 0.4 0 2
execute anchored feet positioned ^ ^ ^4 run particle minecraft:explosion ~ ~0.3 ~ 0.6 0.1 0.6 0 3
execute anchored feet positioned ^ ^ ^3 run particle minecraft:block{block_state:"minecraft:coarse_dirt"} ~ ~0.2 ~ 1.2 0.1 1.2 0 60
playsound minecraft:entity.generic.explode player @a[distance=..24] ~ ~ ~ 0.7 1.3
execute rotated ~ 0 positioned ^ ^ ^3 as @e[type=!#rpg:no_damage_track,type=!minecraft:player,type=!minecraft:armor_stand,tag=!rpg.unit,distance=..3.3,tag=!rpg.ally] run function rpg:forge/stone/rift_hit
tag @s remove rpg.fg.from
