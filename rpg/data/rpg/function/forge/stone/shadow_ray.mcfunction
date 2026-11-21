execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[type=!#rpg:no_damage_track,type=!minecraft:player,type=!minecraft:armor_stand,tag=!rpg.unit,dx=0,dy=0,dz=0,limit=1,tag=!rpg.ally] run tag @s add rpg.fg.tgt
execute if entity @e[tag=rpg.fg.tgt] run return 0
execute unless block ~ ~ ~ #minecraft:replaceable run return 0
scoreboard players remove #i rpg_fg 1
execute if score #i rpg_fg matches 1.. positioned ^ ^ ^0.5 run function rpg:forge/stone/shadow_ray
