summon minecraft:marker ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.bm"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.bm,distance=..0.5] rpg_dt_life 24
scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.bm,distance=..0.5] rpg_dt_kd 0
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagram","minecraft:custom_model_data":{colors:[8160659]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4.4f,1f,4.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 20
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 15
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
