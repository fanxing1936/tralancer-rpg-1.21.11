# 登场（as/at 战场中心）：天光、银色剑环
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[14212838]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 24
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 18
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 24
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 19
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[15660282]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 14
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 17
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[14212838]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.6f,1f,3.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 40
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 15
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:sweep_attack ~2.40 ~1.00 ~0.00 0 0 0 0 1 force
particle minecraft:sweep_attack ~1.70 ~1.00 ~1.70 0 0 0 0 1 force
particle minecraft:sweep_attack ~0.00 ~1.00 ~2.40 0 0 0 0 1 force
particle minecraft:sweep_attack ~-1.70 ~1.00 ~1.70 0 0 0 0 1 force
particle minecraft:sweep_attack ~-2.40 ~1.00 ~0.00 0 0 0 0 1 force
particle minecraft:sweep_attack ~-1.70 ~1.00 ~-1.70 0 0 0 0 1 force
particle minecraft:sweep_attack ~-0.00 ~1.00 ~-2.40 0 0 0 0 1 force
particle minecraft:sweep_attack ~1.70 ~1.00 ~-1.70 0 0 0 0 1 force
particle minecraft:end_rod ~0.40 ~1.00 ~0.00 1.000 0.000 0.000 0.3 0 force
particle minecraft:end_rod ~0.37 ~1.00 ~0.15 0.924 0.000 0.383 0.3 0 force
particle minecraft:end_rod ~0.28 ~1.00 ~0.28 0.707 0.000 0.707 0.3 0 force
particle minecraft:end_rod ~0.15 ~1.00 ~0.37 0.383 0.000 0.924 0.3 0 force
particle minecraft:end_rod ~0.00 ~1.00 ~0.40 0.000 0.000 1.000 0.3 0 force
particle minecraft:end_rod ~-0.15 ~1.00 ~0.37 -0.383 0.000 0.924 0.3 0 force
particle minecraft:end_rod ~-0.28 ~1.00 ~0.28 -0.707 0.000 0.707 0.3 0 force
particle minecraft:end_rod ~-0.37 ~1.00 ~0.15 -0.924 0.000 0.383 0.3 0 force
particle minecraft:end_rod ~-0.40 ~1.00 ~0.00 -1.000 0.000 0.000 0.3 0 force
particle minecraft:end_rod ~-0.37 ~1.00 ~-0.15 -0.924 0.000 -0.383 0.3 0 force
particle minecraft:end_rod ~-0.28 ~1.00 ~-0.28 -0.707 0.000 -0.707 0.3 0 force
particle minecraft:end_rod ~-0.15 ~1.00 ~-0.37 -0.383 0.000 -0.924 0.3 0 force
particle minecraft:end_rod ~-0.00 ~1.00 ~-0.40 -0.000 0.000 -1.000 0.3 0 force
particle minecraft:end_rod ~0.15 ~1.00 ~-0.37 0.383 0.000 -0.924 0.3 0 force
particle minecraft:end_rod ~0.28 ~1.00 ~-0.28 0.707 0.000 -0.707 0.3 0 force
particle minecraft:end_rod ~0.37 ~1.00 ~-0.15 0.924 0.000 -0.383 0.3 0 force
particle minecraft:flash{color:14212838} ~ ~1.5 ~ 0 0 0 0 1 force
