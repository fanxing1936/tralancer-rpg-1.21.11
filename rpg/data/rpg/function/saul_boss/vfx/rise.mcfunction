# 他大笑着站起来（as/at 他）：蛛丝炸开、暗红的光
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[13193306]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 16
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 5
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[13193306]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 12
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 16
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.40 ~1.20 ~0.00 1.000 0.000 0.000 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.39 ~1.20 ~0.10 0.966 0.000 0.259 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.35 ~1.20 ~0.20 0.866 0.000 0.500 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.28 ~1.20 ~0.28 0.707 0.000 0.707 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.20 ~1.20 ~0.35 0.500 0.000 0.866 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.10 ~1.20 ~0.39 0.259 0.000 0.966 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.00 ~1.20 ~0.40 0.000 0.000 1.000 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.10 ~1.20 ~0.39 -0.259 0.000 0.966 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.20 ~1.20 ~0.35 -0.500 0.000 0.866 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.28 ~1.20 ~0.28 -0.707 0.000 0.707 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.35 ~1.20 ~0.20 -0.866 0.000 0.500 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.39 ~1.20 ~0.10 -0.966 0.000 0.259 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.40 ~1.20 ~0.00 -1.000 0.000 0.000 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.39 ~1.20 ~-0.10 -0.966 0.000 -0.259 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.35 ~1.20 ~-0.20 -0.866 0.000 -0.500 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.28 ~1.20 ~-0.28 -0.707 0.000 -0.707 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.20 ~1.20 ~-0.35 -0.500 0.000 -0.866 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.10 ~1.20 ~-0.39 -0.259 0.000 -0.966 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~-0.00 ~1.20 ~-0.40 -0.000 0.000 -1.000 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.10 ~1.20 ~-0.39 0.259 0.000 -0.966 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.20 ~1.20 ~-0.35 0.500 0.000 -0.866 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.28 ~1.20 ~-0.28 0.707 0.000 -0.707 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.35 ~1.20 ~-0.20 0.866 0.000 -0.500 0.4 0 force
particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~0.39 ~1.20 ~-0.10 0.966 0.000 -0.259 0.4 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.40 ~0.60 ~0.00 1.000 0.000 0.000 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.37 ~0.60 ~0.15 0.924 0.000 0.383 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.28 ~0.60 ~0.28 0.707 0.000 0.707 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.15 ~0.60 ~0.37 0.383 0.000 0.924 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.00 ~0.60 ~0.40 0.000 0.000 1.000 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.15 ~0.60 ~0.37 -0.383 0.000 0.924 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.28 ~0.60 ~0.28 -0.707 0.000 0.707 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.37 ~0.60 ~0.15 -0.924 0.000 0.383 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.40 ~0.60 ~0.00 -1.000 0.000 0.000 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.37 ~0.60 ~-0.15 -0.924 0.000 -0.383 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.28 ~0.60 ~-0.28 -0.707 0.000 -0.707 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.15 ~0.60 ~-0.37 -0.383 0.000 -0.924 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.00 ~0.60 ~-0.40 -0.000 0.000 -1.000 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.15 ~0.60 ~-0.37 0.383 0.000 -0.924 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.28 ~0.60 ~-0.28 0.707 0.000 -0.707 0.3 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.37 ~0.60 ~-0.15 0.924 0.000 -0.383 0.3 0 force
particle minecraft:item{item:"minecraft:cobweb"} ~ ~1.4 ~ 0.6 0.8 0.6 0.08 24
particle minecraft:flash{color:13193306} ~ ~2 ~ 0 0 0 0 1 force
