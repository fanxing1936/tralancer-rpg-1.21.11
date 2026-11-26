execute positioned ^ ^ ^1.3 run tag @a[distance=..3.2,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
summon minecraft:text_display ^ ^1.2 ^0.9 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.51f,3.51f,3.51f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 27
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ^0.8 ^1.0 ^1.2 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.535f,2.535f,2.535f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 27
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.1 ^1.8 1.2 0.1 1.2 0 10
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..32] ~ ~ ~ 1 0.8
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[8160659]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.0f,1f,1.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 16
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
