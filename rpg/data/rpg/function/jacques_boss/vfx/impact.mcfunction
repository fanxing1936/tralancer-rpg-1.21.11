# 落刀冲击（at 落点）
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 5
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF2C8"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:crit ~0.40 ~0.30 ~0.00 1.000 0.000 0.000 0.5 0 force
particle minecraft:crit ~0.37 ~0.30 ~0.15 0.924 0.000 0.383 0.5 0 force
particle minecraft:crit ~0.28 ~0.30 ~0.28 0.707 0.000 0.707 0.5 0 force
particle minecraft:crit ~0.15 ~0.30 ~0.37 0.383 0.000 0.924 0.5 0 force
particle minecraft:crit ~0.00 ~0.30 ~0.40 0.000 0.000 1.000 0.5 0 force
particle minecraft:crit ~-0.15 ~0.30 ~0.37 -0.383 0.000 0.924 0.5 0 force
particle minecraft:crit ~-0.28 ~0.30 ~0.28 -0.707 0.000 0.707 0.5 0 force
particle minecraft:crit ~-0.37 ~0.30 ~0.15 -0.924 0.000 0.383 0.5 0 force
particle minecraft:crit ~-0.40 ~0.30 ~0.00 -1.000 0.000 0.000 0.5 0 force
particle minecraft:crit ~-0.37 ~0.30 ~-0.15 -0.924 0.000 -0.383 0.5 0 force
particle minecraft:crit ~-0.28 ~0.30 ~-0.28 -0.707 0.000 -0.707 0.5 0 force
particle minecraft:crit ~-0.15 ~0.30 ~-0.37 -0.383 0.000 -0.924 0.5 0 force
particle minecraft:crit ~-0.00 ~0.30 ~-0.40 -0.000 0.000 -1.000 0.5 0 force
particle minecraft:crit ~0.15 ~0.30 ~-0.37 0.383 0.000 -0.924 0.5 0 force
particle minecraft:crit ~0.28 ~0.30 ~-0.28 0.707 0.000 -0.707 0.5 0 force
particle minecraft:crit ~0.37 ~0.30 ~-0.15 0.924 0.000 -0.383 0.5 0 force
particle minecraft:end_rod ~0.40 ~0.40 ~0.00 1.000 0.000 0.000 0.2 0 force
particle minecraft:end_rod ~0.32 ~0.40 ~0.24 0.809 0.000 0.588 0.2 0 force
particle minecraft:end_rod ~0.12 ~0.40 ~0.38 0.309 0.000 0.951 0.2 0 force
particle minecraft:end_rod ~-0.12 ~0.40 ~0.38 -0.309 0.000 0.951 0.2 0 force
particle minecraft:end_rod ~-0.32 ~0.40 ~0.24 -0.809 0.000 0.588 0.2 0 force
particle minecraft:end_rod ~-0.40 ~0.40 ~0.00 -1.000 0.000 0.000 0.2 0 force
particle minecraft:end_rod ~-0.32 ~0.40 ~-0.24 -0.809 0.000 -0.588 0.2 0 force
particle minecraft:end_rod ~-0.12 ~0.40 ~-0.38 -0.309 0.000 -0.951 0.2 0 force
particle minecraft:end_rod ~0.12 ~0.40 ~-0.38 0.309 0.000 -0.951 0.2 0 force
particle minecraft:end_rod ~0.32 ~0.40 ~-0.24 0.809 0.000 -0.588 0.2 0 force
