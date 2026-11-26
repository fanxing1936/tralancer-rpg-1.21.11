execute positioned ~ ~ ~ run tag @a[distance=..5.1,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 14
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.1875f,7.1875f,7.1875f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 30
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[11187395]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[11f,1f,11f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 16
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 5
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 16
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 17
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:squid_ink ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.5 0 force
particle minecraft:squid_ink ~0.39 ~0.20 ~0.10 0.966 0.000 0.259 0.5 0 force
particle minecraft:squid_ink ~0.35 ~0.20 ~0.20 0.866 0.000 0.500 0.5 0 force
particle minecraft:squid_ink ~0.28 ~0.20 ~0.28 0.707 0.000 0.707 0.5 0 force
particle minecraft:squid_ink ~0.20 ~0.20 ~0.35 0.500 0.000 0.866 0.5 0 force
particle minecraft:squid_ink ~0.10 ~0.20 ~0.39 0.259 0.000 0.966 0.5 0 force
particle minecraft:squid_ink ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.5 0 force
particle minecraft:squid_ink ~-0.10 ~0.20 ~0.39 -0.259 0.000 0.966 0.5 0 force
particle minecraft:squid_ink ~-0.20 ~0.20 ~0.35 -0.500 0.000 0.866 0.5 0 force
particle minecraft:squid_ink ~-0.28 ~0.20 ~0.28 -0.707 0.000 0.707 0.5 0 force
particle minecraft:squid_ink ~-0.35 ~0.20 ~0.20 -0.866 0.000 0.500 0.5 0 force
particle minecraft:squid_ink ~-0.39 ~0.20 ~0.10 -0.966 0.000 0.259 0.5 0 force
particle minecraft:squid_ink ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.5 0 force
particle minecraft:squid_ink ~-0.39 ~0.20 ~-0.10 -0.966 0.000 -0.259 0.5 0 force
particle minecraft:squid_ink ~-0.35 ~0.20 ~-0.20 -0.866 0.000 -0.500 0.5 0 force
particle minecraft:squid_ink ~-0.28 ~0.20 ~-0.28 -0.707 0.000 -0.707 0.5 0 force
particle minecraft:squid_ink ~-0.20 ~0.20 ~-0.35 -0.500 0.000 -0.866 0.5 0 force
particle minecraft:squid_ink ~-0.10 ~0.20 ~-0.39 -0.259 0.000 -0.966 0.5 0 force
particle minecraft:squid_ink ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.5 0 force
particle minecraft:squid_ink ~0.10 ~0.20 ~-0.39 0.259 0.000 -0.966 0.5 0 force
particle minecraft:squid_ink ~0.20 ~0.20 ~-0.35 0.500 0.000 -0.866 0.5 0 force
particle minecraft:squid_ink ~0.28 ~0.20 ~-0.28 0.707 0.000 -0.707 0.5 0 force
particle minecraft:squid_ink ~0.35 ~0.20 ~-0.20 0.866 0.000 -0.500 0.5 0 force
particle minecraft:squid_ink ~0.39 ~0.20 ~-0.10 0.966 0.000 -0.259 0.5 0 force
summon minecraft:text_display ~ ~0.80 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 31
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~1.60 ~0.80 ~0.00 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5625f,0.5625f,0.5625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~1.29 ~1.05 ~0.94 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~0.49 ~1.30 ~1.52 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.9375f,0.9375f,0.9375f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-0.49 ~0.80 ~1.52 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5625f,0.5625f,0.5625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-1.29 ~1.05 ~0.94 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-1.60 ~1.30 ~0.00 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.9375f,0.9375f,0.9375f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-1.29 ~0.80 ~-0.94 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5625f,0.5625f,0.5625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-0.49 ~1.05 ~-1.52 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~0.49 ~1.30 ~-1.52 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.9375f,0.9375f,0.9375f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~1.29 ~0.80 ~-0.94 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5625f,0.5625f,0.5625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:flash{color:11187395} ~ ~1 ~ 0 0 0 0 1 force
playsound rpg:daath.flash3 hostile @a[distance=..48] ~ ~ ~ 1.4 0.9
playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 1.2 0.8
