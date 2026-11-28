# 一片落羽（at 落点）
summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.rainf"]}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 22
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_f","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 21
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.07 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/firering","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.6f,1f,2.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 21
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~9 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.rainfeather"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_boss/feather"}},item_display:"none",brightness:{sky:15,block:15},teleport_duration:0,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0.9238795f,0.3826834f],scale:[1.6f,1.6f,1.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 24
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
