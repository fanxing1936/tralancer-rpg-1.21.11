execute as @e[type=!#rpg:no_damage_track,type=!minecraft:player,type=!minecraft:armor_stand,tag=!rpg.unit,distance=..5,tag=!rpg.ally] run function rpg:forge/stone/frost_hit
particle minecraft:snowflake ~ ~1 ~ 2.5 0.3 2.5 0.02 120
particle minecraft:item_snowball ~ ~0.5 ~ 2.5 0.2 2.5 0.1 40
playsound minecraft:block.powder_snow.break player @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:block.glass.break player @a[distance=..24] ~ ~ ~ 0.6 1.6
