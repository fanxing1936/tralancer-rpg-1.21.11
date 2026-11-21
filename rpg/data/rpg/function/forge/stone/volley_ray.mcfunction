scoreboard players remove #i rpg_fg 1
execute if score #i rpg_fg matches ..0 run return run summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fx","rpg.fg.volley","rpg.fg.new"]}
execute unless block ~ ~ ~ #minecraft:replaceable run return run summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fx","rpg.fg.volley","rpg.fg.new"]}
execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[type=!#rpg:no_damage_track,type=!minecraft:player,type=!minecraft:armor_stand,tag=!rpg.unit,dx=0,dy=0,dz=0,tag=!rpg.ally] positioned ~0.5 ~0.5 ~0.5 run return run summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fx","rpg.fg.volley","rpg.fg.new"]}
execute positioned ^ ^ ^0.5 run function rpg:forge/stone/volley_ray
