# 骨柱放骨刺（at 柱脚，朝目标）：先亮 1 秒裂线
execute positioned ~ ~0.05 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/lane_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,9f],left_rotation:[0f,0f,0f,1f],scale:[1.4400000000000002f,1f,18f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.05 ~ run tp @e[tag=rpg.mkb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 20
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.walker"]}
execute as @e[tag=rpg.mkb.fxnew] run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 37
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,7.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,18f,0.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 30
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 49
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
particle minecraft:end_rod ~ ~2.5 ~ 0.3 1.2 0.3 0.03 16
playsound minecraft:block.bone_block.hit hostile @a[distance=..40] ~ ~ ~ 1.4 0.5
