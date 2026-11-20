# 二阶段大招起手（as/at 他）：暗红剑印与蛛丝
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagram","minecraft:custom_model_data":{colors:[6950936]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 40
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 15
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[13193306]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.4f,1f,3.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 40
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 2
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.38 ~0.20 ~0.12 0.951 0.000 0.309 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.32 ~0.20 ~0.24 0.809 0.000 0.588 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.24 ~0.20 ~0.32 0.588 0.000 0.809 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.12 ~0.20 ~0.38 0.309 0.000 0.951 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.12 ~0.20 ~0.38 -0.309 0.000 0.951 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.24 ~0.20 ~0.32 -0.588 0.000 0.809 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.32 ~0.20 ~0.24 -0.809 0.000 0.588 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.38 ~0.20 ~0.12 -0.951 0.000 0.309 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.38 ~0.20 ~-0.12 -0.951 0.000 -0.309 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.32 ~0.20 ~-0.24 -0.809 0.000 -0.588 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.24 ~0.20 ~-0.32 -0.588 0.000 -0.809 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.12 ~0.20 ~-0.38 -0.309 0.000 -0.951 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.12 ~0.20 ~-0.38 0.309 0.000 -0.951 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.24 ~0.20 ~-0.32 0.588 0.000 -0.809 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.32 ~0.20 ~-0.24 0.809 0.000 -0.588 0.35 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.38 ~0.20 ~-0.12 0.951 0.000 -0.309 0.35 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.40 ~1.20 ~0.00 1.000 0.000 0.000 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.35 ~1.20 ~0.20 0.866 0.000 0.500 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.20 ~1.20 ~0.35 0.500 0.000 0.866 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.00 ~1.20 ~0.40 0.000 0.000 1.000 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.20 ~1.20 ~0.35 -0.500 0.000 0.866 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.35 ~1.20 ~0.20 -0.866 0.000 0.500 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.40 ~1.20 ~0.00 -1.000 0.000 0.000 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.35 ~1.20 ~-0.20 -0.866 0.000 -0.500 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.20 ~1.20 ~-0.35 -0.500 0.000 -0.866 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.00 ~1.20 ~-0.40 -0.000 0.000 -1.000 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.20 ~1.20 ~-0.35 0.500 0.000 -0.866 0.25 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.35 ~1.20 ~-0.20 0.866 0.000 -0.500 0.25 0 force
particle minecraft:flash{color:13193306} ~ ~2 ~ 0 0 0 0 1 force
