execute positioned ~ ~0.06 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[8160659]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,8.0f],left_rotation:[0f,0f,0f,1f],scale:[1.4f,0.02f,16.0f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.06 ~ run tp @e[tag=rpg.dt.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 0
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
playsound minecraft:block.beacon.ambient hostile @a[distance=..48] ~ ~ ~ 1 1.6
