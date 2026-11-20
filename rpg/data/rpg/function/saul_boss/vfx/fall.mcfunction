# 倒下（as/at 他）：蛛丝散开、白灰飘起
summon minecraft:item_display ~ ~0.04 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/glow","minecraft:custom_model_data":{colors:[6974064]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 60
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.40 ~0.60 ~0.00 1.000 0.000 0.000 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.38 ~0.60 ~0.12 0.951 0.000 0.309 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.32 ~0.60 ~0.24 0.809 0.000 0.588 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.24 ~0.60 ~0.32 0.588 0.000 0.809 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.12 ~0.60 ~0.38 0.309 0.000 0.951 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.00 ~0.60 ~0.40 0.000 0.000 1.000 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.12 ~0.60 ~0.38 -0.309 0.000 0.951 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.24 ~0.60 ~0.32 -0.588 0.000 0.809 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.32 ~0.60 ~0.24 -0.809 0.000 0.588 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.38 ~0.60 ~0.12 -0.951 0.000 0.309 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.40 ~0.60 ~0.00 -1.000 0.000 0.000 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.38 ~0.60 ~-0.12 -0.951 0.000 -0.309 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.32 ~0.60 ~-0.24 -0.809 0.000 -0.588 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.24 ~0.60 ~-0.32 -0.588 0.000 -0.809 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.12 ~0.60 ~-0.38 -0.309 0.000 -0.951 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.00 ~0.60 ~-0.40 -0.000 0.000 -1.000 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.12 ~0.60 ~-0.38 0.309 0.000 -0.951 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.24 ~0.60 ~-0.32 0.588 0.000 -0.809 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.32 ~0.60 ~-0.24 0.809 0.000 -0.588 0.15 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.38 ~0.60 ~-0.12 0.951 0.000 -0.309 0.15 0 force
particle minecraft:white_ash ~ ~1.5 ~ 1 1 1 0.01 30
