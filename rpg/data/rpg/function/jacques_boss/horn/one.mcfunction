# 一名圣卫（as 载体，at 落点）：塔卫、重盾、术士随机
function rpg:holy_guard/summon
tag @e[type=minecraft:vindicator,tag=rpg.hg,tag=!rpg.jqb.guard,distance=..2,limit=1,sort=nearest] add rpg.jqb.guard
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[13111342]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.6f,1f,2.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 30
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 1
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sq_0","minecraft:custom_model_data":{colors:[15921906]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 6
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#F2F2F2"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,2.1f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,0.01f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 8
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 21
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 22
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
particle minecraft:end_rod ~ ~1 ~ 0.4 1 0.4 0.05 16
particle minecraft:totem_of_undying ~ ~1 ~ 0.3 0.8 0.3 0.3 20
particle minecraft:end_rod ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.25 0 force
particle minecraft:end_rod ~0.37 ~0.20 ~0.15 0.924 0.000 0.383 0.25 0 force
particle minecraft:end_rod ~0.28 ~0.20 ~0.28 0.707 0.000 0.707 0.25 0 force
particle minecraft:end_rod ~0.15 ~0.20 ~0.37 0.383 0.000 0.924 0.25 0 force
particle minecraft:end_rod ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.25 0 force
particle minecraft:end_rod ~-0.15 ~0.20 ~0.37 -0.383 0.000 0.924 0.25 0 force
particle minecraft:end_rod ~-0.28 ~0.20 ~0.28 -0.707 0.000 0.707 0.25 0 force
particle minecraft:end_rod ~-0.37 ~0.20 ~0.15 -0.924 0.000 0.383 0.25 0 force
particle minecraft:end_rod ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.25 0 force
particle minecraft:end_rod ~-0.37 ~0.20 ~-0.15 -0.924 0.000 -0.383 0.25 0 force
particle minecraft:end_rod ~-0.28 ~0.20 ~-0.28 -0.707 0.000 -0.707 0.25 0 force
particle minecraft:end_rod ~-0.15 ~0.20 ~-0.37 -0.383 0.000 -0.924 0.25 0 force
particle minecraft:end_rod ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.25 0 force
particle minecraft:end_rod ~0.15 ~0.20 ~-0.37 0.383 0.000 -0.924 0.25 0 force
particle minecraft:end_rod ~0.28 ~0.20 ~-0.28 0.707 0.000 -0.707 0.25 0 force
particle minecraft:end_rod ~0.37 ~0.20 ~-0.15 0.924 0.000 -0.383 0.25 0 force
