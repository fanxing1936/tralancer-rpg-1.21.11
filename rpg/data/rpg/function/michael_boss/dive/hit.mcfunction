# 砸下（as/at 他）：3 格内 14，3～6 格冲击波 6
kill @e[tag=rpg.mkb.diveto]
kill @e[tag=rpg.mkb.divering]
tag @e[tag=rpg.unit.f,distance=..3] add rpg.mkb.hit
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit] run damage @s 14 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1]
tag @e[tag=rpg.unit] remove rpg.mkb.hit
tag @e[tag=rpg.unit.f,distance=3..6] add rpg.mkb.hit
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit] run damage @s 6 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1]
tag @e[tag=rpg.unit] remove rpg.mkb.hit
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[12f,1f,12f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 40
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.04 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/scorch","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 80
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.5f,7.5f,7.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 4
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 7
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,7.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,18f,0.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 30
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 50
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 51
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 52
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 53
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 54
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 55
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 56
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 57
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
particle minecraft:flame ~0.40 ~0.30 ~0.00 1.000 0.000 0.000 0.4 0 force
particle minecraft:flame ~0.39 ~0.30 ~0.10 0.966 0.000 0.259 0.4 0 force
particle minecraft:flame ~0.35 ~0.30 ~0.20 0.866 0.000 0.500 0.4 0 force
particle minecraft:flame ~0.28 ~0.30 ~0.28 0.707 0.000 0.707 0.4 0 force
particle minecraft:flame ~0.20 ~0.30 ~0.35 0.500 0.000 0.866 0.4 0 force
particle minecraft:flame ~0.10 ~0.30 ~0.39 0.259 0.000 0.966 0.4 0 force
particle minecraft:flame ~0.00 ~0.30 ~0.40 0.000 0.000 1.000 0.4 0 force
particle minecraft:flame ~-0.10 ~0.30 ~0.39 -0.259 0.000 0.966 0.4 0 force
particle minecraft:flame ~-0.20 ~0.30 ~0.35 -0.500 0.000 0.866 0.4 0 force
particle minecraft:flame ~-0.28 ~0.30 ~0.28 -0.707 0.000 0.707 0.4 0 force
particle minecraft:flame ~-0.35 ~0.30 ~0.20 -0.866 0.000 0.500 0.4 0 force
particle minecraft:flame ~-0.39 ~0.30 ~0.10 -0.966 0.000 0.259 0.4 0 force
particle minecraft:flame ~-0.40 ~0.30 ~0.00 -1.000 0.000 0.000 0.4 0 force
particle minecraft:flame ~-0.39 ~0.30 ~-0.10 -0.966 0.000 -0.259 0.4 0 force
particle minecraft:flame ~-0.35 ~0.30 ~-0.20 -0.866 0.000 -0.500 0.4 0 force
particle minecraft:flame ~-0.28 ~0.30 ~-0.28 -0.707 0.000 -0.707 0.4 0 force
particle minecraft:flame ~-0.20 ~0.30 ~-0.35 -0.500 0.000 -0.866 0.4 0 force
particle minecraft:flame ~-0.10 ~0.30 ~-0.39 -0.259 0.000 -0.966 0.4 0 force
particle minecraft:flame ~-0.00 ~0.30 ~-0.40 -0.000 0.000 -1.000 0.4 0 force
particle minecraft:flame ~0.10 ~0.30 ~-0.39 0.259 0.000 -0.966 0.4 0 force
particle minecraft:flame ~0.20 ~0.30 ~-0.35 0.500 0.000 -0.866 0.4 0 force
particle minecraft:flame ~0.28 ~0.30 ~-0.28 0.707 0.000 -0.707 0.4 0 force
particle minecraft:flame ~0.35 ~0.30 ~-0.20 0.866 0.000 -0.500 0.4 0 force
particle minecraft:flame ~0.39 ~0.30 ~-0.10 0.966 0.000 -0.259 0.4 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~0.40 ~0.80 ~0.00 1.000 0.000 0.000 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~0.37 ~0.80 ~0.15 0.924 0.000 0.383 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~0.28 ~0.80 ~0.28 0.707 0.000 0.707 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~0.15 ~0.80 ~0.37 0.383 0.000 0.924 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~0.00 ~0.80 ~0.40 0.000 0.000 1.000 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~-0.15 ~0.80 ~0.37 -0.383 0.000 0.924 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~-0.28 ~0.80 ~0.28 -0.707 0.000 0.707 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~-0.37 ~0.80 ~0.15 -0.924 0.000 0.383 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~-0.40 ~0.80 ~0.00 -1.000 0.000 0.000 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~-0.37 ~0.80 ~-0.15 -0.924 0.000 -0.383 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~-0.28 ~0.80 ~-0.28 -0.707 0.000 -0.707 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~-0.15 ~0.80 ~-0.37 -0.383 0.000 -0.924 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~-0.00 ~0.80 ~-0.40 -0.000 0.000 -1.000 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~0.15 ~0.80 ~-0.37 0.383 0.000 -0.924 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~0.28 ~0.80 ~-0.28 0.707 0.000 -0.707 0.3 0 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~0.37 ~0.80 ~-0.15 0.924 0.000 -0.383 0.3 0 force
particle minecraft:flash{color:16765117} ~ ~1 ~ 0 0 0 0 1 force
playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1 0.8
playsound minecraft:entity.phantom.flap hostile @a[distance=..40] ~ ~ ~ 1.4 0.5
