execute positioned ^ ^ ^1.8 run tag @a[distance=..2.6,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 12
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
summon minecraft:text_display ^ ^1.2 ^0.9 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.315f,3.315f,3.315f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 27
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ^ ^1.3 ^1 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.1625f,3.1625f,3.1625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 30
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~ ~1.20 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 31
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~0.60 ~1.20 ~0.00 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5625f,0.5625f,0.5625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~0.42 ~1.45 ~0.42 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~0.00 ~1.70 ~0.60 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.9375f,0.9375f,0.9375f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-0.42 ~1.20 ~0.42 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5625f,0.5625f,0.5625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-0.60 ~1.45 ~0.00 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-0.42 ~1.70 ~-0.42 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.9375f,0.9375f,0.9375f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~-0.00 ~1.20 ~-0.60 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5625f,0.5625f,0.5625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ~0.42 ~1.45 ~-0.42 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 32
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 39
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
playsound minecraft:item.shield.block hostile @a[distance=..48] ~ ~ ~ 1.2 1.4
playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 1 1
