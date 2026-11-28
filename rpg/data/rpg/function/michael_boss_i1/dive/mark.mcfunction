# 落点（at 瞄准点）：一圈圣焰，先跟着走
summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.diveto"]}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 40
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.divering"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_f","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 36
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.divering"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/glow_f","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 36
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.07 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.divering"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/seal_seraph","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 36
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 15
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
