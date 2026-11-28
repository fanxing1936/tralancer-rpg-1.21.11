# 扇区 1 亮红（at 中心）
execute rotated 120 0 positioned ~ ~0.05 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/lane_f","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,15f],left_rotation:[0f,0f,0f,1f],scale:[0.6400000000000001f,1f,30f],right_rotation:[0f,0f,0f,1f]}}
execute rotated 120 0 positioned ~ ~0.05 ~ run tp @e[tag=rpg.mkb.fxnew,limit=1,distance=0..] ~ ~ ~ ~ ~
execute rotated 240 0 positioned ~ ~0.05 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/lane_f","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,15f],left_rotation:[0f,0f,0f,1f],scale:[0.6400000000000001f,1f,30f],right_rotation:[0f,0f,0f,1f]}}
execute rotated 240 0 positioned ~ ~0.05 ~ run tp @e[tag=rpg.mkb.fxnew,limit=1,distance=0..] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 30
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/wedge","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:6f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[62f,1f,62f],right_rotation:[0f,0f,0f,1f]}}
tp @e[tag=rpg.mkb.fxnew,limit=1,distance=0..] ~ ~0.06 ~ 360 0
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 30
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
playsound minecraft:block.note_block.bass hostile @a[distance=..48] ~ ~ ~ 1.4 0.5
