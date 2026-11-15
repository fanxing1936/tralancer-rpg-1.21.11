# 竖琴之弦（as/at 他）：朝天一箭化作金光柱，天上爆开
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16771496]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 21
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 22
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
summon minecraft:text_display ~ ~9 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#F0CF7A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.5f,7.5f,7.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~9 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF2C8"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagram","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 72
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 17
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:firework ~0.40 ~9.00 ~0.00 1.000 0.000 0.000 0.4 0 force
particle minecraft:firework ~0.39 ~9.00 ~0.10 0.966 0.000 0.259 0.4 0 force
particle minecraft:firework ~0.35 ~9.00 ~0.20 0.866 0.000 0.500 0.4 0 force
particle minecraft:firework ~0.28 ~9.00 ~0.28 0.707 0.000 0.707 0.4 0 force
particle minecraft:firework ~0.20 ~9.00 ~0.35 0.500 0.000 0.866 0.4 0 force
particle minecraft:firework ~0.10 ~9.00 ~0.39 0.259 0.000 0.966 0.4 0 force
particle minecraft:firework ~0.00 ~9.00 ~0.40 0.000 0.000 1.000 0.4 0 force
particle minecraft:firework ~-0.10 ~9.00 ~0.39 -0.259 0.000 0.966 0.4 0 force
particle minecraft:firework ~-0.20 ~9.00 ~0.35 -0.500 0.000 0.866 0.4 0 force
particle minecraft:firework ~-0.28 ~9.00 ~0.28 -0.707 0.000 0.707 0.4 0 force
particle minecraft:firework ~-0.35 ~9.00 ~0.20 -0.866 0.000 0.500 0.4 0 force
particle minecraft:firework ~-0.39 ~9.00 ~0.10 -0.966 0.000 0.259 0.4 0 force
particle minecraft:firework ~-0.40 ~9.00 ~0.00 -1.000 0.000 0.000 0.4 0 force
particle minecraft:firework ~-0.39 ~9.00 ~-0.10 -0.966 0.000 -0.259 0.4 0 force
particle minecraft:firework ~-0.35 ~9.00 ~-0.20 -0.866 0.000 -0.500 0.4 0 force
particle minecraft:firework ~-0.28 ~9.00 ~-0.28 -0.707 0.000 -0.707 0.4 0 force
particle minecraft:firework ~-0.20 ~9.00 ~-0.35 -0.500 0.000 -0.866 0.4 0 force
particle minecraft:firework ~-0.10 ~9.00 ~-0.39 -0.259 0.000 -0.966 0.4 0 force
particle minecraft:firework ~-0.00 ~9.00 ~-0.40 -0.000 0.000 -1.000 0.4 0 force
particle minecraft:firework ~0.10 ~9.00 ~-0.39 0.259 0.000 -0.966 0.4 0 force
particle minecraft:firework ~0.20 ~9.00 ~-0.35 0.500 0.000 -0.866 0.4 0 force
particle minecraft:firework ~0.28 ~9.00 ~-0.28 0.707 0.000 -0.707 0.4 0 force
particle minecraft:firework ~0.35 ~9.00 ~-0.20 0.866 0.000 -0.500 0.4 0 force
particle minecraft:firework ~0.39 ~9.00 ~-0.10 0.966 0.000 -0.259 0.4 0 force
particle minecraft:end_rod ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.3 0 force
particle minecraft:end_rod ~0.37 ~0.20 ~0.15 0.924 0.000 0.383 0.3 0 force
particle minecraft:end_rod ~0.28 ~0.20 ~0.28 0.707 0.000 0.707 0.3 0 force
particle minecraft:end_rod ~0.15 ~0.20 ~0.37 0.383 0.000 0.924 0.3 0 force
particle minecraft:end_rod ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.3 0 force
particle minecraft:end_rod ~-0.15 ~0.20 ~0.37 -0.383 0.000 0.924 0.3 0 force
particle minecraft:end_rod ~-0.28 ~0.20 ~0.28 -0.707 0.000 0.707 0.3 0 force
particle minecraft:end_rod ~-0.37 ~0.20 ~0.15 -0.924 0.000 0.383 0.3 0 force
particle minecraft:end_rod ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.3 0 force
particle minecraft:end_rod ~-0.37 ~0.20 ~-0.15 -0.924 0.000 -0.383 0.3 0 force
particle minecraft:end_rod ~-0.28 ~0.20 ~-0.28 -0.707 0.000 -0.707 0.3 0 force
particle minecraft:end_rod ~-0.15 ~0.20 ~-0.37 -0.383 0.000 -0.924 0.3 0 force
particle minecraft:end_rod ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.3 0 force
particle minecraft:end_rod ~0.15 ~0.20 ~-0.37 0.383 0.000 -0.924 0.3 0 force
particle minecraft:end_rod ~0.28 ~0.20 ~-0.28 0.707 0.000 -0.707 0.3 0 force
particle minecraft:end_rod ~0.37 ~0.20 ~-0.15 0.924 0.000 -0.383 0.3 0 force
particle minecraft:flash{color:16771496} ~ ~9 ~ 0 0 0 0 1 force
