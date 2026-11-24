summon minecraft:marker ~ ~ ~ {Tags:["rpg.fo.zone","rpg.fo.znew"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_k 63
scoreboard players operation @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end = #now rpg_fo
scoreboard players add @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end 120
tag @e[type=minecraft:marker,tag=rpg.fo.znew] remove rpg.fo.znew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.xm","rpg.fo.xmnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/cracks","minecraft:custom_model_data":{colors:[10989513]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[10f,1f,10f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_life 120
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.xmnew] remove rpg.fo.xmnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.fo.xm","rpg.fo.xmnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/swirl","minecraft:custom_model_data":{colors:[2763312]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,1f,8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_life 120
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_kd 1
tag @e[tag=rpg.fo.xmnew] remove rpg.fo.xmnew
