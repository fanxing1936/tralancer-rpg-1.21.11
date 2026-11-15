# 每次翻滚冲锋起步（as/at 他）
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[16747069]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 5
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:flame ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.35 0 force
particle minecraft:flame ~0.36 ~0.20 ~0.17 0.901 0.000 0.434 0.35 0 force
particle minecraft:flame ~0.25 ~0.20 ~0.31 0.623 0.000 0.782 0.35 0 force
particle minecraft:flame ~0.09 ~0.20 ~0.39 0.223 0.000 0.975 0.35 0 force
particle minecraft:flame ~-0.09 ~0.20 ~0.39 -0.223 0.000 0.975 0.35 0 force
particle minecraft:flame ~-0.25 ~0.20 ~0.31 -0.623 0.000 0.782 0.35 0 force
particle minecraft:flame ~-0.36 ~0.20 ~0.17 -0.901 0.000 0.434 0.35 0 force
particle minecraft:flame ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.35 0 force
particle minecraft:flame ~-0.36 ~0.20 ~-0.17 -0.901 0.000 -0.434 0.35 0 force
particle minecraft:flame ~-0.25 ~0.20 ~-0.31 -0.623 0.000 -0.782 0.35 0 force
particle minecraft:flame ~-0.09 ~0.20 ~-0.39 -0.223 0.000 -0.975 0.35 0 force
particle minecraft:flame ~0.09 ~0.20 ~-0.39 0.223 0.000 -0.975 0.35 0 force
particle minecraft:flame ~0.25 ~0.20 ~-0.31 0.623 0.000 -0.782 0.35 0 force
particle minecraft:flame ~0.36 ~0.20 ~-0.17 0.901 0.000 -0.434 0.35 0 force
particle minecraft:lava ~ ~0.4 ~ 0.3 0.1 0.3 0 3
