# 他沉入地面之前（as/at 他）：一道天光落下
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[14212838]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 24
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 18
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 24
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 19
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[15660282]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 12
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 16
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:end_rod ~0.40 ~0.80 ~0.00 1.000 0.000 0.000 0.15 0 force
particle minecraft:end_rod ~0.38 ~0.80 ~0.12 0.951 0.000 0.309 0.15 0 force
particle minecraft:end_rod ~0.32 ~0.80 ~0.24 0.809 0.000 0.588 0.15 0 force
particle minecraft:end_rod ~0.24 ~0.80 ~0.32 0.588 0.000 0.809 0.15 0 force
particle minecraft:end_rod ~0.12 ~0.80 ~0.38 0.309 0.000 0.951 0.15 0 force
particle minecraft:end_rod ~0.00 ~0.80 ~0.40 0.000 0.000 1.000 0.15 0 force
particle minecraft:end_rod ~-0.12 ~0.80 ~0.38 -0.309 0.000 0.951 0.15 0 force
particle minecraft:end_rod ~-0.24 ~0.80 ~0.32 -0.588 0.000 0.809 0.15 0 force
particle minecraft:end_rod ~-0.32 ~0.80 ~0.24 -0.809 0.000 0.588 0.15 0 force
particle minecraft:end_rod ~-0.38 ~0.80 ~0.12 -0.951 0.000 0.309 0.15 0 force
particle minecraft:end_rod ~-0.40 ~0.80 ~0.00 -1.000 0.000 0.000 0.15 0 force
particle minecraft:end_rod ~-0.38 ~0.80 ~-0.12 -0.951 0.000 -0.309 0.15 0 force
particle minecraft:end_rod ~-0.32 ~0.80 ~-0.24 -0.809 0.000 -0.588 0.15 0 force
particle minecraft:end_rod ~-0.24 ~0.80 ~-0.32 -0.588 0.000 -0.809 0.15 0 force
particle minecraft:end_rod ~-0.12 ~0.80 ~-0.38 -0.309 0.000 -0.951 0.15 0 force
particle minecraft:end_rod ~-0.00 ~0.80 ~-0.40 -0.000 0.000 -1.000 0.15 0 force
particle minecraft:end_rod ~0.12 ~0.80 ~-0.38 0.309 0.000 -0.951 0.15 0 force
particle minecraft:end_rod ~0.24 ~0.80 ~-0.32 0.588 0.000 -0.809 0.15 0 force
particle minecraft:end_rod ~0.32 ~0.80 ~-0.24 0.809 0.000 -0.588 0.15 0 force
particle minecraft:end_rod ~0.38 ~0.80 ~-0.12 0.951 0.000 -0.309 0.15 0 force
particle minecraft:totem_of_undying ~ ~1 ~ 0.5 0.6 0.5 0.2 20
