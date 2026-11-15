# 20 秒到了：光柱里离开（as/at 他）。
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqa.fx","rpg.jqa.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_life 24
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_kd 16
tag @e[tag=rpg.jqa.fxnew] remove rpg.jqa.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqa.fx","rpg.jqa.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_life 24
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_kd 17
tag @e[tag=rpg.jqa.fxnew] remove rpg.jqa.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqa.fx","rpg.jqa.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_life 12
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_kd 18
tag @e[tag=rpg.jqa.fxnew] remove rpg.jqa.fxnew
particle minecraft:end_rod ~0.40 ~0.20 ~0.00 1.000 0 0.000 0.25 0
particle minecraft:end_rod ~0.37 ~0.20 ~0.15 0.924 0 0.383 0.25 0
particle minecraft:end_rod ~0.28 ~0.20 ~0.28 0.707 0 0.707 0.25 0
particle minecraft:end_rod ~0.15 ~0.20 ~0.37 0.383 0 0.924 0.25 0
particle minecraft:end_rod ~0.00 ~0.20 ~0.40 0.000 0 1.000 0.25 0
particle minecraft:end_rod ~-0.15 ~0.20 ~0.37 -0.383 0 0.924 0.25 0
particle minecraft:end_rod ~-0.28 ~0.20 ~0.28 -0.707 0 0.707 0.25 0
particle minecraft:end_rod ~-0.37 ~0.20 ~0.15 -0.924 0 0.383 0.25 0
particle minecraft:end_rod ~-0.40 ~0.20 ~0.00 -1.000 0 0.000 0.25 0
particle minecraft:end_rod ~-0.37 ~0.20 ~-0.15 -0.924 0 -0.383 0.25 0
particle minecraft:end_rod ~-0.28 ~0.20 ~-0.28 -0.707 0 -0.707 0.25 0
particle minecraft:end_rod ~-0.15 ~0.20 ~-0.37 -0.383 0 -0.924 0.25 0
particle minecraft:end_rod ~-0.00 ~0.20 ~-0.40 -0.000 0 -1.000 0.25 0
particle minecraft:end_rod ~0.15 ~0.20 ~-0.37 0.383 0 -0.924 0.25 0
particle minecraft:end_rod ~0.28 ~0.20 ~-0.28 0.707 0 -0.707 0.25 0
particle minecraft:end_rod ~0.37 ~0.20 ~-0.15 0.924 0 -0.383 0.25 0
particle minecraft:totem_of_undying ~ ~1.2 ~ 0.4 0.8 0.4 0.3 24
playsound minecraft:block.beacon.deactivate player @a[distance=..32] ~ ~ ~ 1 1.2
function rpg:jacques_ally/remove
