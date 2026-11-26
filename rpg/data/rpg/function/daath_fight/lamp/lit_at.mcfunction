# positioned 光圈圆心
summon minecraft:marker ~ ~ ~ {Tags:["rpg.dt.pool"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..0.5] rpg_dt_lt 160
setblock ~ ~3 ~ minecraft:light[level=15]
summon minecraft:item_display ~ ~0.04 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew","rpg.dt.poolfx"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/glow","minecraft:custom_model_data":{colors:[16773800]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[13.200000000000001f,1f,13.200000000000001f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 160
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 0
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:item_display ~ ~0.07 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew","rpg.dt.poolfx"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[12f,1f,12f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 160
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 0
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16773800]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 24
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 19
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:end_rod ~ ~5 ~ 0.15 5 0.15 0.01 30 force
