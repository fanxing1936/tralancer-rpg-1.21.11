execute positioned ^ ^ ^1.0 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^2.4 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^3.8 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^5.2 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^6.6 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^8.0 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^9.4 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^10.8 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^12.2 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^13.6 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^15.0 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute positioned ^ ^ ^16.4 run tag @a[distance=..1.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 12
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
execute positioned ^ ^1.2 ^0.8 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[11187395]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,8.0f],left_rotation:[0f,0f,0f,1f],scale:[0.5f,0.5f,16.0f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^ ^1.2 ^0.8 run tp @e[tag=rpg.dt.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 21
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
execute positioned ^ ^1.2 ^0.8 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[723984]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,8.0f],left_rotation:[0f,0f,0f,1f],scale:[0.3f,0.3f,16.0f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^ ^1.2 ^0.8 run tp @e[tag=rpg.dt.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 21
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^1.20 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^2.40 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^3.60 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^4.80 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^6.00 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^7.20 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^8.40 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^9.60 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^10.80 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^12.00 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^13.20 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^14.40 0.2 0.1 0.2 0 2 force
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^ ^1.20 ^15.60 0.2 0.1 0.2 0 2 force
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..48] ~ ~ ~ 0.6 1.4
playsound minecraft:item.trident.thunder hostile @a[distance=..48] ~ ~ ~ 0.4 1.6
