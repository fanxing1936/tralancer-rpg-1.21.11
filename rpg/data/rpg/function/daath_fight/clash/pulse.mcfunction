execute positioned ~ ~0.07 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,3.5f],left_rotation:[0f,0f,0f,1f],scale:[0.3f,0.02f,7.0f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.07 ~ run tp @e[tag=rpg.dt.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 10
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 0
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ^-0.4 ^1.8 ^0.4 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 10
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 7
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
playsound minecraft:block.note_block.bell hostile @a[distance=..48] ~ ~ ~ 1 0.6
