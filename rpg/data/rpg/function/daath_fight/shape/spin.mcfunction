execute positioned ~ ~ ~ run tag @a[distance=..3.7,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
summon minecraft:text_display ^ ^1.1 ^ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.75f,5.75f,5.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 28
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:text_display ^ ^1.1 ^1.0 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.925f,2.925f,2.925f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 27
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[8160659]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.0f,1f,1.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 16
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
particle minecraft:cloud ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.22 0 force
particle minecraft:cloud ~0.37 ~0.20 ~0.15 0.924 0.000 0.383 0.22 0 force
particle minecraft:cloud ~0.28 ~0.20 ~0.28 0.707 0.000 0.707 0.22 0 force
particle minecraft:cloud ~0.15 ~0.20 ~0.37 0.383 0.000 0.924 0.22 0 force
particle minecraft:cloud ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.22 0 force
particle minecraft:cloud ~-0.15 ~0.20 ~0.37 -0.383 0.000 0.924 0.22 0 force
particle minecraft:cloud ~-0.28 ~0.20 ~0.28 -0.707 0.000 0.707 0.22 0 force
particle minecraft:cloud ~-0.37 ~0.20 ~0.15 -0.924 0.000 0.383 0.22 0 force
particle minecraft:cloud ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.22 0 force
particle minecraft:cloud ~-0.37 ~0.20 ~-0.15 -0.924 0.000 -0.383 0.22 0 force
particle minecraft:cloud ~-0.28 ~0.20 ~-0.28 -0.707 0.000 -0.707 0.22 0 force
particle minecraft:cloud ~-0.15 ~0.20 ~-0.37 -0.383 0.000 -0.924 0.22 0 force
particle minecraft:cloud ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.22 0 force
particle minecraft:cloud ~0.15 ~0.20 ~-0.37 0.383 0.000 -0.924 0.22 0 force
particle minecraft:cloud ~0.28 ~0.20 ~-0.28 0.707 0.000 -0.707 0.22 0 force
particle minecraft:cloud ~0.37 ~0.20 ~-0.15 0.924 0.000 -0.383 0.22 0 force
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..32] ~ ~ ~ 1.2 0.7
playsound minecraft:item.trident.throw hostile @a[distance=..32] ~ ~ ~ 0.7 0.7
