summon minecraft:text_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.ult"],text:{text:"",font:"rpg:usurper_fx",color:"#FF8A3D"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,2.1f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,0.01f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 60
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 9
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~2 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FF8A3D"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.ult"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16747069]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 12
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 18
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:flame ~0.40 ~0.30 ~0.00 1.000 0.000 0.000 0.3 0 force
particle minecraft:flame ~0.36 ~0.30 ~0.17 0.901 0.000 0.434 0.3 0 force
particle minecraft:flame ~0.25 ~0.30 ~0.31 0.623 0.000 0.782 0.3 0 force
particle minecraft:flame ~0.09 ~0.30 ~0.39 0.223 0.000 0.975 0.3 0 force
particle minecraft:flame ~-0.09 ~0.30 ~0.39 -0.223 0.000 0.975 0.3 0 force
particle minecraft:flame ~-0.25 ~0.30 ~0.31 -0.623 0.000 0.782 0.3 0 force
particle minecraft:flame ~-0.36 ~0.30 ~0.17 -0.901 0.000 0.434 0.3 0 force
particle minecraft:flame ~-0.40 ~0.30 ~0.00 -1.000 0.000 0.000 0.3 0 force
particle minecraft:flame ~-0.36 ~0.30 ~-0.17 -0.901 0.000 -0.434 0.3 0 force
particle minecraft:flame ~-0.25 ~0.30 ~-0.31 -0.623 0.000 -0.782 0.3 0 force
particle minecraft:flame ~-0.09 ~0.30 ~-0.39 -0.223 0.000 -0.975 0.3 0 force
particle minecraft:flame ~0.09 ~0.30 ~-0.39 0.223 0.000 -0.975 0.3 0 force
particle minecraft:flame ~0.25 ~0.30 ~-0.31 0.623 0.000 -0.782 0.3 0 force
particle minecraft:flame ~0.36 ~0.30 ~-0.17 0.901 0.000 -0.434 0.3 0 force
particle minecraft:lava ~ ~2.20 ~ 0.500 0.900 0.000 0.5 0 force
particle minecraft:lava ~ ~2.20 ~ 1.000 0.600 0.000 0.5 0 force
particle minecraft:lava ~ ~2.20 ~ 0.000 0.900 0.500 0.5 0 force
particle minecraft:lava ~ ~2.20 ~ 0.000 0.600 1.000 0.5 0 force
particle minecraft:lava ~ ~2.20 ~ -0.500 0.900 0.000 0.5 0 force
particle minecraft:lava ~ ~2.20 ~ -1.000 0.600 0.000 0.5 0 force
particle minecraft:lava ~ ~2.20 ~ -0.000 0.900 -0.500 0.5 0 force
particle minecraft:lava ~ ~2.20 ~ -0.000 0.600 -1.000 0.5 0 force
