summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/lane_r","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,9.2f],left_rotation:[0f,0f,0f,1f],scale:[1.1199999999999999f,1f,18.4f],right_rotation:[0f,0f,0f,1f]}}
tp @e[tag=rpg.mkb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 8
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
