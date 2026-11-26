execute positioned ^ ^ ^1.0 run tag @a[distance=..1.25,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^2.1 run tag @a[distance=..1.25,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^3.2 run tag @a[distance=..1.25,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^1.25 ^0.8 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[11187395]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,2.0f],left_rotation:[0f,0f,0f,1f],scale:[0.14f,0.14f,4.0f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^ ^1.25 ^0.8 run tp @e[tag=rpg.dt.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 8
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 20
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ^ ^1.25 ^2.0 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 29
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^0.80 0.08 0.04 0.08 0 1 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^1.60 0.08 0.04 0.08 0 1 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^2.40 0.08 0.04 0.08 0 1 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^3.20 0.08 0.04 0.08 0 1 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^4.00 0.08 0.04 0.08 0 1 force
playsound minecraft:item.trident.throw hostile @a[distance=..28] ~ ~ ~ 0.8 1.4
