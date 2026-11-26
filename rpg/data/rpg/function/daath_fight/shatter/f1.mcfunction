tag @a[distance=..2.7,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
summon minecraft:item_display ~ ~0.4 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagon","minecraft:custom_model_data":{colors:[11187395]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.4f,1f,5.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 26
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 25
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:block{block_state:"minecraft:black_stained_glass"} ~ ~0.4 ~ 1.2 0.4 1.2 0.2 20
