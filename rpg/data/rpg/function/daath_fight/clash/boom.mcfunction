summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.1875f,7.1875f,7.1875f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 30
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[11187395]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[12f,1f,12f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 16
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 5
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:daath_fx/crack_mirror","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,1f,8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 60
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 0
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 0.8
playsound minecraft:item.mace.smash_ground_heavy hostile @a[distance=..48] ~ ~ ~ 1.4 0.6
