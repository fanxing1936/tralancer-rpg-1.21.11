# 巨剑砸地（at 中心）：5 格内 18
execute as @e[tag=rpg.unit.f,distance=..5] run damage @s 18 minecraft:mob_attack
tag @e[tag=rpg.unit.f,distance=..5] add rpg.slb.failed
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[15660282]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[14f,1f,14f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 16
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 5
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~0.04 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/cracks","minecraft:custom_model_data":{colors:[1710624]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[9f,1f,9f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 100
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[13193306]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 14
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 17
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#EEF4FA"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.5f,7.5f,7.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 16
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 4
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:crit ~0.40 ~0.40 ~0.00 1.000 0.000 0.000 0.8 0 force
particle minecraft:crit ~0.39 ~0.40 ~0.08 0.981 0.000 0.195 0.8 0 force
particle minecraft:crit ~0.37 ~0.40 ~0.15 0.924 0.000 0.383 0.8 0 force
particle minecraft:crit ~0.33 ~0.40 ~0.22 0.831 0.000 0.556 0.8 0 force
particle minecraft:crit ~0.28 ~0.40 ~0.28 0.707 0.000 0.707 0.8 0 force
particle minecraft:crit ~0.22 ~0.40 ~0.33 0.556 0.000 0.831 0.8 0 force
particle minecraft:crit ~0.15 ~0.40 ~0.37 0.383 0.000 0.924 0.8 0 force
particle minecraft:crit ~0.08 ~0.40 ~0.39 0.195 0.000 0.981 0.8 0 force
particle minecraft:crit ~0.00 ~0.40 ~0.40 0.000 0.000 1.000 0.8 0 force
particle minecraft:crit ~-0.08 ~0.40 ~0.39 -0.195 0.000 0.981 0.8 0 force
particle minecraft:crit ~-0.15 ~0.40 ~0.37 -0.383 0.000 0.924 0.8 0 force
particle minecraft:crit ~-0.22 ~0.40 ~0.33 -0.556 0.000 0.831 0.8 0 force
particle minecraft:crit ~-0.28 ~0.40 ~0.28 -0.707 0.000 0.707 0.8 0 force
particle minecraft:crit ~-0.33 ~0.40 ~0.22 -0.831 0.000 0.556 0.8 0 force
particle minecraft:crit ~-0.37 ~0.40 ~0.15 -0.924 0.000 0.383 0.8 0 force
particle minecraft:crit ~-0.39 ~0.40 ~0.08 -0.981 0.000 0.195 0.8 0 force
particle minecraft:crit ~-0.40 ~0.40 ~0.00 -1.000 0.000 0.000 0.8 0 force
particle minecraft:crit ~-0.39 ~0.40 ~-0.08 -0.981 0.000 -0.195 0.8 0 force
particle minecraft:crit ~-0.37 ~0.40 ~-0.15 -0.924 0.000 -0.383 0.8 0 force
particle minecraft:crit ~-0.33 ~0.40 ~-0.22 -0.831 0.000 -0.556 0.8 0 force
particle minecraft:crit ~-0.28 ~0.40 ~-0.28 -0.707 0.000 -0.707 0.8 0 force
particle minecraft:crit ~-0.22 ~0.40 ~-0.33 -0.556 0.000 -0.831 0.8 0 force
particle minecraft:crit ~-0.15 ~0.40 ~-0.37 -0.383 0.000 -0.924 0.8 0 force
particle minecraft:crit ~-0.08 ~0.40 ~-0.39 -0.195 0.000 -0.981 0.8 0 force
particle minecraft:crit ~-0.00 ~0.40 ~-0.40 -0.000 0.000 -1.000 0.8 0 force
particle minecraft:crit ~0.08 ~0.40 ~-0.39 0.195 0.000 -0.981 0.8 0 force
particle minecraft:crit ~0.15 ~0.40 ~-0.37 0.383 0.000 -0.924 0.8 0 force
particle minecraft:crit ~0.22 ~0.40 ~-0.33 0.556 0.000 -0.831 0.8 0 force
particle minecraft:crit ~0.28 ~0.40 ~-0.28 0.707 0.000 -0.707 0.8 0 force
particle minecraft:crit ~0.33 ~0.40 ~-0.22 0.831 0.000 -0.556 0.8 0 force
particle minecraft:crit ~0.37 ~0.40 ~-0.15 0.924 0.000 -0.383 0.8 0 force
particle minecraft:crit ~0.39 ~0.40 ~-0.08 0.981 0.000 -0.195 0.8 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.40 ~0.60 ~0.00 1.000 0.000 0.000 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.39 ~0.60 ~0.10 0.966 0.000 0.259 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.35 ~0.60 ~0.20 0.866 0.000 0.500 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.28 ~0.60 ~0.28 0.707 0.000 0.707 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.20 ~0.60 ~0.35 0.500 0.000 0.866 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.10 ~0.60 ~0.39 0.259 0.000 0.966 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.00 ~0.60 ~0.40 0.000 0.000 1.000 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.10 ~0.60 ~0.39 -0.259 0.000 0.966 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.20 ~0.60 ~0.35 -0.500 0.000 0.866 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.28 ~0.60 ~0.28 -0.707 0.000 0.707 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.35 ~0.60 ~0.20 -0.866 0.000 0.500 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.39 ~0.60 ~0.10 -0.966 0.000 0.259 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.40 ~0.60 ~0.00 -1.000 0.000 0.000 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.39 ~0.60 ~-0.10 -0.966 0.000 -0.259 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.35 ~0.60 ~-0.20 -0.866 0.000 -0.500 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.28 ~0.60 ~-0.28 -0.707 0.000 -0.707 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.20 ~0.60 ~-0.35 -0.500 0.000 -0.866 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.10 ~0.60 ~-0.39 -0.259 0.000 -0.966 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~-0.00 ~0.60 ~-0.40 -0.000 0.000 -1.000 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.10 ~0.60 ~-0.39 0.259 0.000 -0.966 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.20 ~0.60 ~-0.35 0.500 0.000 -0.866 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.28 ~0.60 ~-0.28 0.707 0.000 -0.707 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.35 ~0.60 ~-0.20 0.866 0.000 -0.500 0.5 0 force
particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~0.39 ~0.60 ~-0.10 0.966 0.000 -0.259 0.5 0 force
particle minecraft:flash{color:15660282} ~ ~1 ~ 0 0 0 0 1 force
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1.2 0.6
playsound minecraft:block.anvil.land hostile @a[distance=..48] ~ ~ ~ 1.4 0.5
