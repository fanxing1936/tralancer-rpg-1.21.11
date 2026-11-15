# 号角（as/at 他）：脚下红十字圣印，金色光浪与图腾光点
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[13111342]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4.5f,1f,4.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 17
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 12
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 18
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~2.6 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#F0CF7A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4.25f,4.25f,4.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~0.40 ~1.60 ~0.00 1.000 0.000 0.000 0.35 0 force
particle minecraft:end_rod ~0.38 ~1.60 ~0.12 0.951 0.000 0.309 0.35 0 force
particle minecraft:end_rod ~0.32 ~1.60 ~0.24 0.809 0.000 0.588 0.35 0 force
particle minecraft:end_rod ~0.24 ~1.60 ~0.32 0.588 0.000 0.809 0.35 0 force
particle minecraft:end_rod ~0.12 ~1.60 ~0.38 0.309 0.000 0.951 0.35 0 force
particle minecraft:end_rod ~0.00 ~1.60 ~0.40 0.000 0.000 1.000 0.35 0 force
particle minecraft:end_rod ~-0.12 ~1.60 ~0.38 -0.309 0.000 0.951 0.35 0 force
particle minecraft:end_rod ~-0.24 ~1.60 ~0.32 -0.588 0.000 0.809 0.35 0 force
particle minecraft:end_rod ~-0.32 ~1.60 ~0.24 -0.809 0.000 0.588 0.35 0 force
particle minecraft:end_rod ~-0.38 ~1.60 ~0.12 -0.951 0.000 0.309 0.35 0 force
particle minecraft:end_rod ~-0.40 ~1.60 ~0.00 -1.000 0.000 0.000 0.35 0 force
particle minecraft:end_rod ~-0.38 ~1.60 ~-0.12 -0.951 0.000 -0.309 0.35 0 force
particle minecraft:end_rod ~-0.32 ~1.60 ~-0.24 -0.809 0.000 -0.588 0.35 0 force
particle minecraft:end_rod ~-0.24 ~1.60 ~-0.32 -0.588 0.000 -0.809 0.35 0 force
particle minecraft:end_rod ~-0.12 ~1.60 ~-0.38 -0.309 0.000 -0.951 0.35 0 force
particle minecraft:end_rod ~-0.00 ~1.60 ~-0.40 -0.000 0.000 -1.000 0.35 0 force
particle minecraft:end_rod ~0.12 ~1.60 ~-0.38 0.309 0.000 -0.951 0.35 0 force
particle minecraft:end_rod ~0.24 ~1.60 ~-0.32 0.588 0.000 -0.809 0.35 0 force
particle minecraft:end_rod ~0.32 ~1.60 ~-0.24 0.809 0.000 -0.588 0.35 0 force
particle minecraft:end_rod ~0.38 ~1.60 ~-0.12 0.951 0.000 -0.309 0.35 0 force
particle minecraft:totem_of_undying ~ ~1.6 ~ 0.4 0.6 0.4 0.5 40 force
particle minecraft:flash{color:15781754} ~ ~2.2 ~ 0 0 0 0 1 force
