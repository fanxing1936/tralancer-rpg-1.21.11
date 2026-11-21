summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.trail"]}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/embers","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:block_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],block_state:{Name:"minecraft:fire"},brightness:{sky:15,block:15},view_range:2f,transformation:{translation:[-0.05f,0f,-0.05f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,0.1f,0.1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.mkb.fxnew,limit=1] store result entity @s Rotation[0] float 1 run random value 0..359
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 28
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
