# 砸地（at 落点）：火的冲击波、岩浆溅起、裂地
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FF8A3D"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6.25f,6.25f,6.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFD08A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.16 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16765066]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 12
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 18
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.04 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/cracks","minecraft:custom_model_data":{colors:[2755076]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7f,1f,7f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 80
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:flame ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.55 0 force
particle minecraft:flame ~0.39 ~0.20 ~0.09 0.975 0.000 0.223 0.55 0 force
particle minecraft:flame ~0.36 ~0.20 ~0.17 0.901 0.000 0.434 0.55 0 force
particle minecraft:flame ~0.31 ~0.20 ~0.25 0.782 0.000 0.623 0.55 0 force
particle minecraft:flame ~0.25 ~0.20 ~0.31 0.623 0.000 0.782 0.55 0 force
particle minecraft:flame ~0.17 ~0.20 ~0.36 0.434 0.000 0.901 0.55 0 force
particle minecraft:flame ~0.09 ~0.20 ~0.39 0.223 0.000 0.975 0.55 0 force
particle minecraft:flame ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.55 0 force
particle minecraft:flame ~-0.09 ~0.20 ~0.39 -0.223 0.000 0.975 0.55 0 force
particle minecraft:flame ~-0.17 ~0.20 ~0.36 -0.434 0.000 0.901 0.55 0 force
particle minecraft:flame ~-0.25 ~0.20 ~0.31 -0.623 0.000 0.782 0.55 0 force
particle minecraft:flame ~-0.31 ~0.20 ~0.25 -0.782 0.000 0.623 0.55 0 force
particle minecraft:flame ~-0.36 ~0.20 ~0.17 -0.901 0.000 0.434 0.55 0 force
particle minecraft:flame ~-0.39 ~0.20 ~0.09 -0.975 0.000 0.223 0.55 0 force
particle minecraft:flame ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.55 0 force
particle minecraft:flame ~-0.39 ~0.20 ~-0.09 -0.975 0.000 -0.223 0.55 0 force
particle minecraft:flame ~-0.36 ~0.20 ~-0.17 -0.901 0.000 -0.434 0.55 0 force
particle minecraft:flame ~-0.31 ~0.20 ~-0.25 -0.782 0.000 -0.623 0.55 0 force
particle minecraft:flame ~-0.25 ~0.20 ~-0.31 -0.623 0.000 -0.782 0.55 0 force
particle minecraft:flame ~-0.17 ~0.20 ~-0.36 -0.434 0.000 -0.901 0.55 0 force
particle minecraft:flame ~-0.09 ~0.20 ~-0.39 -0.223 0.000 -0.975 0.55 0 force
particle minecraft:flame ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.55 0 force
particle minecraft:flame ~0.09 ~0.20 ~-0.39 0.223 0.000 -0.975 0.55 0 force
particle minecraft:flame ~0.17 ~0.20 ~-0.36 0.434 0.000 -0.901 0.55 0 force
particle minecraft:flame ~0.25 ~0.20 ~-0.31 0.623 0.000 -0.782 0.55 0 force
particle minecraft:flame ~0.31 ~0.20 ~-0.25 0.782 0.000 -0.623 0.55 0 force
particle minecraft:flame ~0.36 ~0.20 ~-0.17 0.901 0.000 -0.434 0.55 0 force
particle minecraft:flame ~0.39 ~0.20 ~-0.09 0.975 0.000 -0.223 0.55 0 force
particle minecraft:large_smoke ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.3 0 force
particle minecraft:large_smoke ~0.36 ~0.20 ~0.17 0.901 0.000 0.434 0.3 0 force
particle minecraft:large_smoke ~0.25 ~0.20 ~0.31 0.623 0.000 0.782 0.3 0 force
particle minecraft:large_smoke ~0.09 ~0.20 ~0.39 0.223 0.000 0.975 0.3 0 force
particle minecraft:large_smoke ~-0.09 ~0.20 ~0.39 -0.223 0.000 0.975 0.3 0 force
particle minecraft:large_smoke ~-0.25 ~0.20 ~0.31 -0.623 0.000 0.782 0.3 0 force
particle minecraft:large_smoke ~-0.36 ~0.20 ~0.17 -0.901 0.000 0.434 0.3 0 force
particle minecraft:large_smoke ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.3 0 force
particle minecraft:large_smoke ~-0.36 ~0.20 ~-0.17 -0.901 0.000 -0.434 0.3 0 force
particle minecraft:large_smoke ~-0.25 ~0.20 ~-0.31 -0.623 0.000 -0.782 0.3 0 force
particle minecraft:large_smoke ~-0.09 ~0.20 ~-0.39 -0.223 0.000 -0.975 0.3 0 force
particle minecraft:large_smoke ~0.09 ~0.20 ~-0.39 0.223 0.000 -0.975 0.3 0 force
particle minecraft:large_smoke ~0.25 ~0.20 ~-0.31 0.623 0.000 -0.782 0.3 0 force
particle minecraft:large_smoke ~0.36 ~0.20 ~-0.17 0.901 0.000 -0.434 0.3 0 force
particle minecraft:lava ~ ~0.60 ~ 0.500 0.900 0.000 0.6 0 force
particle minecraft:lava ~ ~0.60 ~ 1.000 0.600 0.000 0.6 0 force
particle minecraft:lava ~ ~0.60 ~ 0.250 0.900 0.433 0.6 0 force
particle minecraft:lava ~ ~0.60 ~ 0.500 0.600 0.866 0.6 0 force
particle minecraft:lava ~ ~0.60 ~ -0.250 0.900 0.433 0.6 0 force
particle minecraft:lava ~ ~0.60 ~ -0.500 0.600 0.866 0.6 0 force
particle minecraft:lava ~ ~0.60 ~ -0.500 0.900 0.000 0.6 0 force
particle minecraft:lava ~ ~0.60 ~ -1.000 0.600 0.000 0.6 0 force
particle minecraft:lava ~ ~0.60 ~ -0.250 0.900 -0.433 0.6 0 force
particle minecraft:lava ~ ~0.60 ~ -0.500 0.600 -0.866 0.6 0 force
particle minecraft:lava ~ ~0.60 ~ 0.250 0.900 -0.433 0.6 0 force
particle minecraft:lava ~ ~0.60 ~ 0.500 0.600 -0.866 0.6 0 force
particle minecraft:flash{color:16747069} ~ ~1 ~ 0 0 0 0 1 force
