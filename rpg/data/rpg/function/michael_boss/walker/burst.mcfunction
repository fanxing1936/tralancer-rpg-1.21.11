particle minecraft:block{block_state:"minecraft:bone_block"} ~ ~0.5 ~ 0.2 0.4 0.2 0 6
particle minecraft:dust_color_transition{from_color:[1.0,0.5,0.32],to_color:[1.0,0.2,0.0],scale:1.1} ~ ~0.7 ~ 0.15 0.5 0.15 0 3
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[15918808]}}},brightness:{sky:15,block:15},teleport_duration:0,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.05f,0.2f,0.05f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 23
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
tag @e[tag=rpg.unit.f,distance=..1.3] add rpg.mkb.hit
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit] run damage @s 12 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1]
tag @e[tag=rpg.unit] remove rpg.mkb.hit
