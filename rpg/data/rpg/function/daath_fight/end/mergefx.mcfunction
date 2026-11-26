summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16773800]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 24
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 19
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:end_rod ~ ~5 ~ 0.15 5 0.15 0.01 30 force
summon minecraft:text_display ~ ~1.1 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6.325f,6.325f,6.325f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 30
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.15 80 force
playsound minecraft:block.beacon.activate hostile @a[distance=..48] ~ ~ ~ 1.4 1.2
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..48] ~ ~ ~ 1.4 0.8
