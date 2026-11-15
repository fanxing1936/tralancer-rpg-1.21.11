# 大卫的幽灵摆出英雄姿势（as/at 它）：天光落在他身上
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[14216447]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 21
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 22
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[14216447]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 12
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 18
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~0.40 ~1.00 ~0.00 1.000 0.000 0.000 0.3 0 force
particle minecraft:end_rod ~0.38 ~1.00 ~0.12 0.951 0.000 0.309 0.3 0 force
particle minecraft:end_rod ~0.32 ~1.00 ~0.24 0.809 0.000 0.588 0.3 0 force
particle minecraft:end_rod ~0.24 ~1.00 ~0.32 0.588 0.000 0.809 0.3 0 force
particle minecraft:end_rod ~0.12 ~1.00 ~0.38 0.309 0.000 0.951 0.3 0 force
particle minecraft:end_rod ~0.00 ~1.00 ~0.40 0.000 0.000 1.000 0.3 0 force
particle minecraft:end_rod ~-0.12 ~1.00 ~0.38 -0.309 0.000 0.951 0.3 0 force
particle minecraft:end_rod ~-0.24 ~1.00 ~0.32 -0.588 0.000 0.809 0.3 0 force
particle minecraft:end_rod ~-0.32 ~1.00 ~0.24 -0.809 0.000 0.588 0.3 0 force
particle minecraft:end_rod ~-0.38 ~1.00 ~0.12 -0.951 0.000 0.309 0.3 0 force
particle minecraft:end_rod ~-0.40 ~1.00 ~0.00 -1.000 0.000 0.000 0.3 0 force
particle minecraft:end_rod ~-0.38 ~1.00 ~-0.12 -0.951 0.000 -0.309 0.3 0 force
particle minecraft:end_rod ~-0.32 ~1.00 ~-0.24 -0.809 0.000 -0.588 0.3 0 force
particle minecraft:end_rod ~-0.24 ~1.00 ~-0.32 -0.588 0.000 -0.809 0.3 0 force
particle minecraft:end_rod ~-0.12 ~1.00 ~-0.38 -0.309 0.000 -0.951 0.3 0 force
particle minecraft:end_rod ~-0.00 ~1.00 ~-0.40 -0.000 0.000 -1.000 0.3 0 force
particle minecraft:end_rod ~0.12 ~1.00 ~-0.38 0.309 0.000 -0.951 0.3 0 force
particle minecraft:end_rod ~0.24 ~1.00 ~-0.32 0.588 0.000 -0.809 0.3 0 force
particle minecraft:end_rod ~0.32 ~1.00 ~-0.24 0.809 0.000 -0.588 0.3 0 force
particle minecraft:end_rod ~0.38 ~1.00 ~-0.12 0.951 0.000 -0.309 0.3 0 force
particle minecraft:totem_of_undying ~ ~1.2 ~ 0.4 1 0.4 0.3 30 force
