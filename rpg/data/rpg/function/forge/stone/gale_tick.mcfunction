particle minecraft:cloud ^-1.5 ^0.5 ^ 0 0.6 0 0.01 2
particle minecraft:cloud ^ ^0.5 ^ 0 0.6 0 0.01 2
particle minecraft:cloud ^1.5 ^0.5 ^ 0 0.6 0 0.01 2
particle minecraft:gust ^ ^1 ^ 1 0.6 0.2 0 1
tag @s add rpg.fg.from
execute as @e[type=!#rpg:no_damage_track,type=!minecraft:player,type=!minecraft:armor_stand,tag=!rpg.unit,distance=..2.6,tag=!rpg.ally] run function rpg:forge/fx/push
tag @s remove rpg.fg.from
kill @e[type=#rpg:forge/projectiles,distance=..2.6,tag=!rpg.fg.a]
