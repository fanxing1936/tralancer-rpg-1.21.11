# 一把落剑（at 落点）：地上一圈预警，剑从 10 格高处插下来
summon minecraft:marker ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.rain"]}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 15
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[13193306]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.2f,1f,3.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 14
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~10 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.rainsword"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:saul/rapier"}},item_display:"none",brightness:{sky:15,block:15},teleport_duration:0,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[1f,0f,0f,0f],scale:[1.6f,1.6f,1.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 24
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:end_rod ~ ~10 ~ 0.2 0.3 0.2 0.02 6
