# 倒下（as/at 他）：火从身上散去
summon minecraft:item_display ~ ~0.04 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/glow","minecraft:custom_model_data":{colors:[12727834]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 60
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:flame ~0.40 ~0.60 ~0.00 1.000 0.000 0.000 0.2 0 force
particle minecraft:flame ~0.38 ~0.60 ~0.12 0.951 0.000 0.309 0.2 0 force
particle minecraft:flame ~0.32 ~0.60 ~0.24 0.809 0.000 0.588 0.2 0 force
particle minecraft:flame ~0.24 ~0.60 ~0.32 0.588 0.000 0.809 0.2 0 force
particle minecraft:flame ~0.12 ~0.60 ~0.38 0.309 0.000 0.951 0.2 0 force
particle minecraft:flame ~0.00 ~0.60 ~0.40 0.000 0.000 1.000 0.2 0 force
particle minecraft:flame ~-0.12 ~0.60 ~0.38 -0.309 0.000 0.951 0.2 0 force
particle minecraft:flame ~-0.24 ~0.60 ~0.32 -0.588 0.000 0.809 0.2 0 force
particle minecraft:flame ~-0.32 ~0.60 ~0.24 -0.809 0.000 0.588 0.2 0 force
particle minecraft:flame ~-0.38 ~0.60 ~0.12 -0.951 0.000 0.309 0.2 0 force
particle minecraft:flame ~-0.40 ~0.60 ~0.00 -1.000 0.000 0.000 0.2 0 force
particle minecraft:flame ~-0.38 ~0.60 ~-0.12 -0.951 0.000 -0.309 0.2 0 force
particle minecraft:flame ~-0.32 ~0.60 ~-0.24 -0.809 0.000 -0.588 0.2 0 force
particle minecraft:flame ~-0.24 ~0.60 ~-0.32 -0.588 0.000 -0.809 0.2 0 force
particle minecraft:flame ~-0.12 ~0.60 ~-0.38 -0.309 0.000 -0.951 0.2 0 force
particle minecraft:flame ~-0.00 ~0.60 ~-0.40 -0.000 0.000 -1.000 0.2 0 force
particle minecraft:flame ~0.12 ~0.60 ~-0.38 0.309 0.000 -0.951 0.2 0 force
particle minecraft:flame ~0.24 ~0.60 ~-0.32 0.588 0.000 -0.809 0.2 0 force
particle minecraft:flame ~0.32 ~0.60 ~-0.24 0.809 0.000 -0.588 0.2 0 force
particle minecraft:flame ~0.38 ~0.60 ~-0.12 0.951 0.000 -0.309 0.2 0 force
particle minecraft:large_smoke ~0.40 ~1.00 ~0.00 1.000 0.000 0.000 0.15 0 force
particle minecraft:large_smoke ~0.37 ~1.00 ~0.15 0.924 0.000 0.383 0.15 0 force
particle minecraft:large_smoke ~0.28 ~1.00 ~0.28 0.707 0.000 0.707 0.15 0 force
particle minecraft:large_smoke ~0.15 ~1.00 ~0.37 0.383 0.000 0.924 0.15 0 force
particle minecraft:large_smoke ~0.00 ~1.00 ~0.40 0.000 0.000 1.000 0.15 0 force
particle minecraft:large_smoke ~-0.15 ~1.00 ~0.37 -0.383 0.000 0.924 0.15 0 force
particle minecraft:large_smoke ~-0.28 ~1.00 ~0.28 -0.707 0.000 0.707 0.15 0 force
particle minecraft:large_smoke ~-0.37 ~1.00 ~0.15 -0.924 0.000 0.383 0.15 0 force
particle minecraft:large_smoke ~-0.40 ~1.00 ~0.00 -1.000 0.000 0.000 0.15 0 force
particle minecraft:large_smoke ~-0.37 ~1.00 ~-0.15 -0.924 0.000 -0.383 0.15 0 force
particle minecraft:large_smoke ~-0.28 ~1.00 ~-0.28 -0.707 0.000 -0.707 0.15 0 force
particle minecraft:large_smoke ~-0.15 ~1.00 ~-0.37 -0.383 0.000 -0.924 0.15 0 force
particle minecraft:large_smoke ~-0.00 ~1.00 ~-0.40 -0.000 0.000 -1.000 0.15 0 force
particle minecraft:large_smoke ~0.15 ~1.00 ~-0.37 0.383 0.000 -0.924 0.15 0 force
particle minecraft:large_smoke ~0.28 ~1.00 ~-0.28 0.707 0.000 -0.707 0.15 0 force
particle minecraft:large_smoke ~0.37 ~1.00 ~-0.15 0.924 0.000 -0.383 0.15 0 force
particle minecraft:campfire_cosy_smoke ~ ~1 ~ 0.4 0.4 0.4 0.01 8
