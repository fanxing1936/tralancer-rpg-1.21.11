# 落点（at 目标脚下）：一圈火光，1 秒后他砸下来
summon minecraft:marker ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.land"]}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 26
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.03 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.landv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/glow","minecraft:custom_model_data":{colors:[12727834]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[9f,1f,9f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 22
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.landv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16747069]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,1f,8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 22
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.12 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.landv"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[16756832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6.4f,1f,6.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 22
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 17
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:flame ~4.00 ~0.20 ~0.00 0 0 0 0 1 force
particle minecraft:flame ~3.76 ~0.20 ~1.37 0 0 0 0 1 force
particle minecraft:flame ~3.06 ~0.20 ~2.57 0 0 0 0 1 force
particle minecraft:flame ~2.00 ~0.20 ~3.46 0 0 0 0 1 force
particle minecraft:flame ~0.69 ~0.20 ~3.94 0 0 0 0 1 force
particle minecraft:flame ~-0.69 ~0.20 ~3.94 0 0 0 0 1 force
particle minecraft:flame ~-2.00 ~0.20 ~3.46 0 0 0 0 1 force
particle minecraft:flame ~-3.06 ~0.20 ~2.57 0 0 0 0 1 force
particle minecraft:flame ~-3.76 ~0.20 ~1.37 0 0 0 0 1 force
particle minecraft:flame ~-4.00 ~0.20 ~0.00 0 0 0 0 1 force
particle minecraft:flame ~-3.76 ~0.20 ~-1.37 0 0 0 0 1 force
particle minecraft:flame ~-3.06 ~0.20 ~-2.57 0 0 0 0 1 force
particle minecraft:flame ~-2.00 ~0.20 ~-3.46 0 0 0 0 1 force
particle minecraft:flame ~-0.69 ~0.20 ~-3.94 0 0 0 0 1 force
particle minecraft:flame ~0.69 ~0.20 ~-3.94 0 0 0 0 1 force
particle minecraft:flame ~2.00 ~0.20 ~-3.46 0 0 0 0 1 force
particle minecraft:flame ~3.06 ~0.20 ~-2.57 0 0 0 0 1 force
particle minecraft:flame ~3.76 ~0.20 ~-1.37 0 0 0 0 1 force
particle minecraft:flame ~ ~0.2 ~ 3 0.1 3 0.02 30
playsound minecraft:block.fire.ambient hostile @a[distance=..32] ~ ~ ~ 2 1.2
