# 登场（as/at 战场中心）：天光、灵光环
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/core","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 24
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 22
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,7.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,18f,0.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 30
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 49
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 18
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/seal_seraph","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[9f,1f,9f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 40
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 15
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[11.25f,11.25f,11.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 33
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ^2.0 ^1.5 ^0.0 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 50
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ^0.0 ^1.5 ^2.0 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 50
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ^-2.0 ^1.5 ^0.0 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 50
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ^-0.0 ^1.5 ^-2.0 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 50
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
particle minecraft:end_rod ~0.40 ~1.20 ~0.00 1.000 0.000 0.000 0.3 0 force
particle minecraft:end_rod ~0.38 ~1.20 ~0.12 0.951 0.000 0.309 0.3 0 force
particle minecraft:end_rod ~0.32 ~1.20 ~0.24 0.809 0.000 0.588 0.3 0 force
particle minecraft:end_rod ~0.24 ~1.20 ~0.32 0.588 0.000 0.809 0.3 0 force
particle minecraft:end_rod ~0.12 ~1.20 ~0.38 0.309 0.000 0.951 0.3 0 force
particle minecraft:end_rod ~0.00 ~1.20 ~0.40 0.000 0.000 1.000 0.3 0 force
particle minecraft:end_rod ~-0.12 ~1.20 ~0.38 -0.309 0.000 0.951 0.3 0 force
particle minecraft:end_rod ~-0.24 ~1.20 ~0.32 -0.588 0.000 0.809 0.3 0 force
particle minecraft:end_rod ~-0.32 ~1.20 ~0.24 -0.809 0.000 0.588 0.3 0 force
particle minecraft:end_rod ~-0.38 ~1.20 ~0.12 -0.951 0.000 0.309 0.3 0 force
particle minecraft:end_rod ~-0.40 ~1.20 ~0.00 -1.000 0.000 0.000 0.3 0 force
particle minecraft:end_rod ~-0.38 ~1.20 ~-0.12 -0.951 0.000 -0.309 0.3 0 force
particle minecraft:end_rod ~-0.32 ~1.20 ~-0.24 -0.809 0.000 -0.588 0.3 0 force
particle minecraft:end_rod ~-0.24 ~1.20 ~-0.32 -0.588 0.000 -0.809 0.3 0 force
particle minecraft:end_rod ~-0.12 ~1.20 ~-0.38 -0.309 0.000 -0.951 0.3 0 force
particle minecraft:end_rod ~-0.00 ~1.20 ~-0.40 -0.000 0.000 -1.000 0.3 0 force
particle minecraft:end_rod ~0.12 ~1.20 ~-0.38 0.309 0.000 -0.951 0.3 0 force
particle minecraft:end_rod ~0.24 ~1.20 ~-0.32 0.588 0.000 -0.809 0.3 0 force
particle minecraft:end_rod ~0.32 ~1.20 ~-0.24 0.809 0.000 -0.588 0.3 0 force
particle minecraft:end_rod ~0.38 ~1.20 ~-0.12 0.951 0.000 -0.309 0.3 0 force
particle minecraft:flash{color:16765117} ~ ~1.5 ~ 0 0 0 0 1 force
