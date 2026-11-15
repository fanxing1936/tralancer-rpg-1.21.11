# 登场（at 落点）：金光柱从天而降，脚下转动的红十字圣印与金色六芒星，光浪扫开
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 21
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 22
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[13111342]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 44
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 1
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.04 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagram","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 44
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 2
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 14
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 19
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~2 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#F0CF7A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6.25f,6.25f,6.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.45 0 force
particle minecraft:end_rod ~0.39 ~0.20 ~0.09 0.975 0.000 0.223 0.45 0 force
particle minecraft:end_rod ~0.36 ~0.20 ~0.17 0.901 0.000 0.434 0.45 0 force
particle minecraft:end_rod ~0.31 ~0.20 ~0.25 0.782 0.000 0.623 0.45 0 force
particle minecraft:end_rod ~0.25 ~0.20 ~0.31 0.623 0.000 0.782 0.45 0 force
particle minecraft:end_rod ~0.17 ~0.20 ~0.36 0.434 0.000 0.901 0.45 0 force
particle minecraft:end_rod ~0.09 ~0.20 ~0.39 0.223 0.000 0.975 0.45 0 force
particle minecraft:end_rod ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.45 0 force
particle minecraft:end_rod ~-0.09 ~0.20 ~0.39 -0.223 0.000 0.975 0.45 0 force
particle minecraft:end_rod ~-0.17 ~0.20 ~0.36 -0.434 0.000 0.901 0.45 0 force
particle minecraft:end_rod ~-0.25 ~0.20 ~0.31 -0.623 0.000 0.782 0.45 0 force
particle minecraft:end_rod ~-0.31 ~0.20 ~0.25 -0.782 0.000 0.623 0.45 0 force
particle minecraft:end_rod ~-0.36 ~0.20 ~0.17 -0.901 0.000 0.434 0.45 0 force
particle minecraft:end_rod ~-0.39 ~0.20 ~0.09 -0.975 0.000 0.223 0.45 0 force
particle minecraft:end_rod ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.45 0 force
particle minecraft:end_rod ~-0.39 ~0.20 ~-0.09 -0.975 0.000 -0.223 0.45 0 force
particle minecraft:end_rod ~-0.36 ~0.20 ~-0.17 -0.901 0.000 -0.434 0.45 0 force
particle minecraft:end_rod ~-0.31 ~0.20 ~-0.25 -0.782 0.000 -0.623 0.45 0 force
particle minecraft:end_rod ~-0.25 ~0.20 ~-0.31 -0.623 0.000 -0.782 0.45 0 force
particle minecraft:end_rod ~-0.17 ~0.20 ~-0.36 -0.434 0.000 -0.901 0.45 0 force
particle minecraft:end_rod ~-0.09 ~0.20 ~-0.39 -0.223 0.000 -0.975 0.45 0 force
particle minecraft:end_rod ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.45 0 force
particle minecraft:end_rod ~0.09 ~0.20 ~-0.39 0.223 0.000 -0.975 0.45 0 force
particle minecraft:end_rod ~0.17 ~0.20 ~-0.36 0.434 0.000 -0.901 0.45 0 force
particle minecraft:end_rod ~0.25 ~0.20 ~-0.31 0.623 0.000 -0.782 0.45 0 force
particle minecraft:end_rod ~0.31 ~0.20 ~-0.25 0.782 0.000 -0.623 0.45 0 force
particle minecraft:end_rod ~0.36 ~0.20 ~-0.17 0.901 0.000 -0.434 0.45 0 force
particle minecraft:end_rod ~0.39 ~0.20 ~-0.09 0.975 0.000 -0.223 0.45 0 force
particle minecraft:firework ~0.40 ~1.20 ~0.00 1.000 0.200 0.000 0.3 0 force
particle minecraft:firework ~0.37 ~1.20 ~0.15 0.924 0.200 0.383 0.3 0 force
particle minecraft:firework ~0.28 ~1.20 ~0.28 0.707 0.200 0.707 0.3 0 force
particle minecraft:firework ~0.15 ~1.20 ~0.37 0.383 0.200 0.924 0.3 0 force
particle minecraft:firework ~0.00 ~1.20 ~0.40 0.000 0.200 1.000 0.3 0 force
particle minecraft:firework ~-0.15 ~1.20 ~0.37 -0.383 0.200 0.924 0.3 0 force
particle minecraft:firework ~-0.28 ~1.20 ~0.28 -0.707 0.200 0.707 0.3 0 force
particle minecraft:firework ~-0.37 ~1.20 ~0.15 -0.924 0.200 0.383 0.3 0 force
particle minecraft:firework ~-0.40 ~1.20 ~0.00 -1.000 0.200 0.000 0.3 0 force
particle minecraft:firework ~-0.37 ~1.20 ~-0.15 -0.924 0.200 -0.383 0.3 0 force
particle minecraft:firework ~-0.28 ~1.20 ~-0.28 -0.707 0.200 -0.707 0.3 0 force
particle minecraft:firework ~-0.15 ~1.20 ~-0.37 -0.383 0.200 -0.924 0.3 0 force
particle minecraft:firework ~-0.00 ~1.20 ~-0.40 -0.000 0.200 -1.000 0.3 0 force
particle minecraft:firework ~0.15 ~1.20 ~-0.37 0.383 0.200 -0.924 0.3 0 force
particle minecraft:firework ~0.28 ~1.20 ~-0.28 0.707 0.200 -0.707 0.3 0 force
particle minecraft:firework ~0.37 ~1.20 ~-0.15 0.924 0.200 -0.383 0.3 0 force
particle minecraft:flash{color:16773832} ~ ~2 ~ 0 0 0 0 1 force
particle minecraft:totem_of_undying ~ ~1.2 ~ 0.6 1 0.6 0.5 60 force
