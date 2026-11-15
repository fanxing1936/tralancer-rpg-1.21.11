# 二阶段大招起手（as/at 他）：火光冲天，脚下转动的火印
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16747069]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 21
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 22
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagram","minecraft:custom_model_data":{colors:[12727834]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 40
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 17
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[16747069]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 40
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 2
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~2.4 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FF8A3D"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6.25f,6.25f,6.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:flame ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.45 0 force
particle minecraft:flame ~0.39 ~0.20 ~0.10 0.966 0.000 0.259 0.45 0 force
particle minecraft:flame ~0.35 ~0.20 ~0.20 0.866 0.000 0.500 0.45 0 force
particle minecraft:flame ~0.28 ~0.20 ~0.28 0.707 0.000 0.707 0.45 0 force
particle minecraft:flame ~0.20 ~0.20 ~0.35 0.500 0.000 0.866 0.45 0 force
particle minecraft:flame ~0.10 ~0.20 ~0.39 0.259 0.000 0.966 0.45 0 force
particle minecraft:flame ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.45 0 force
particle minecraft:flame ~-0.10 ~0.20 ~0.39 -0.259 0.000 0.966 0.45 0 force
particle minecraft:flame ~-0.20 ~0.20 ~0.35 -0.500 0.000 0.866 0.45 0 force
particle minecraft:flame ~-0.28 ~0.20 ~0.28 -0.707 0.000 0.707 0.45 0 force
particle minecraft:flame ~-0.35 ~0.20 ~0.20 -0.866 0.000 0.500 0.45 0 force
particle minecraft:flame ~-0.39 ~0.20 ~0.10 -0.966 0.000 0.259 0.45 0 force
particle minecraft:flame ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.45 0 force
particle minecraft:flame ~-0.39 ~0.20 ~-0.10 -0.966 0.000 -0.259 0.45 0 force
particle minecraft:flame ~-0.35 ~0.20 ~-0.20 -0.866 0.000 -0.500 0.45 0 force
particle minecraft:flame ~-0.28 ~0.20 ~-0.28 -0.707 0.000 -0.707 0.45 0 force
particle minecraft:flame ~-0.20 ~0.20 ~-0.35 -0.500 0.000 -0.866 0.45 0 force
particle minecraft:flame ~-0.10 ~0.20 ~-0.39 -0.259 0.000 -0.966 0.45 0 force
particle minecraft:flame ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.45 0 force
particle minecraft:flame ~0.10 ~0.20 ~-0.39 0.259 0.000 -0.966 0.45 0 force
particle minecraft:flame ~0.20 ~0.20 ~-0.35 0.500 0.000 -0.866 0.45 0 force
particle minecraft:flame ~0.28 ~0.20 ~-0.28 0.707 0.000 -0.707 0.45 0 force
particle minecraft:flame ~0.35 ~0.20 ~-0.20 0.866 0.000 -0.500 0.45 0 force
particle minecraft:flame ~0.39 ~0.20 ~-0.10 0.966 0.000 -0.259 0.45 0 force
particle minecraft:flash{color:16747069} ~ ~2 ~ 0 0 0 0 1 force
