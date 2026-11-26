# 倒影举剑：记住这一刻你站的地方（慢 0.7 秒）；站在灯下没有倒影
execute if entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..6] run return 0
summon minecraft:marker ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.rm"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.rm,distance=..0.5] rpg_dt_life 30
scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.rm,distance=..0.5] rpg_dt_kd 0
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.2f,1f,3.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 15
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 0
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:daath_fx/crack_mirror","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.0f,1f,3.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 15
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 0
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
playsound minecraft:block.sculk_sensor.clicking hostile @a[distance=..32] ~ ~ ~ 1 0.5
