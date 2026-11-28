# 散开（as/at 他）：一闪，光柱、白鸽升起、羽毛四散，冲击环推开
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/core","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 24
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 22
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,7.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,18f,0.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 30
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 49
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,7.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,18f,0.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 30
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 49
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 18
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[9f,1f,9f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 41
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.8 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[13.75f,13.75f,13.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 33
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.75f,8.75f,8.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 4
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 7
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 52
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 53
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 54
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 55
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 56
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 57
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 58
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 59
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ^1.6 ^0.8 ^0.0 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ^1.1 ^1.1 ^1.1 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ^0.0 ^1.3 ^1.6 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ^-1.1 ^1.6 ^1.1 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ^-1.6 ^1.8 ^0.0 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ^-1.1 ^2.0 ^-1.1 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ^-0.0 ^2.3 ^-1.6 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:text_display ^1.1 ^2.5 ^-1.1 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 48
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
particle minecraft:end_rod ~0.40 ~1.00 ~0.00 1.000 0.000 0.000 0.32 0 force
particle minecraft:end_rod ~0.39 ~1.00 ~0.08 0.981 0.000 0.195 0.32 0 force
particle minecraft:end_rod ~0.37 ~1.00 ~0.15 0.924 0.000 0.383 0.32 0 force
particle minecraft:end_rod ~0.33 ~1.00 ~0.22 0.831 0.000 0.556 0.32 0 force
particle minecraft:end_rod ~0.28 ~1.00 ~0.28 0.707 0.000 0.707 0.32 0 force
particle minecraft:end_rod ~0.22 ~1.00 ~0.33 0.556 0.000 0.831 0.32 0 force
particle minecraft:end_rod ~0.15 ~1.00 ~0.37 0.383 0.000 0.924 0.32 0 force
particle minecraft:end_rod ~0.08 ~1.00 ~0.39 0.195 0.000 0.981 0.32 0 force
particle minecraft:end_rod ~0.00 ~1.00 ~0.40 0.000 0.000 1.000 0.32 0 force
particle minecraft:end_rod ~-0.08 ~1.00 ~0.39 -0.195 0.000 0.981 0.32 0 force
particle minecraft:end_rod ~-0.15 ~1.00 ~0.37 -0.383 0.000 0.924 0.32 0 force
particle minecraft:end_rod ~-0.22 ~1.00 ~0.33 -0.556 0.000 0.831 0.32 0 force
particle minecraft:end_rod ~-0.28 ~1.00 ~0.28 -0.707 0.000 0.707 0.32 0 force
particle minecraft:end_rod ~-0.33 ~1.00 ~0.22 -0.831 0.000 0.556 0.32 0 force
particle minecraft:end_rod ~-0.37 ~1.00 ~0.15 -0.924 0.000 0.383 0.32 0 force
particle minecraft:end_rod ~-0.39 ~1.00 ~0.08 -0.981 0.000 0.195 0.32 0 force
particle minecraft:end_rod ~-0.40 ~1.00 ~0.00 -1.000 0.000 0.000 0.32 0 force
particle minecraft:end_rod ~-0.39 ~1.00 ~-0.08 -0.981 0.000 -0.195 0.32 0 force
particle minecraft:end_rod ~-0.37 ~1.00 ~-0.15 -0.924 0.000 -0.383 0.32 0 force
particle minecraft:end_rod ~-0.33 ~1.00 ~-0.22 -0.831 0.000 -0.556 0.32 0 force
particle minecraft:end_rod ~-0.28 ~1.00 ~-0.28 -0.707 0.000 -0.707 0.32 0 force
particle minecraft:end_rod ~-0.22 ~1.00 ~-0.33 -0.556 0.000 -0.831 0.32 0 force
particle minecraft:end_rod ~-0.15 ~1.00 ~-0.37 -0.383 0.000 -0.924 0.32 0 force
particle minecraft:end_rod ~-0.08 ~1.00 ~-0.39 -0.195 0.000 -0.981 0.32 0 force
particle minecraft:end_rod ~-0.00 ~1.00 ~-0.40 -0.000 0.000 -1.000 0.32 0 force
particle minecraft:end_rod ~0.08 ~1.00 ~-0.39 0.195 0.000 -0.981 0.32 0 force
particle minecraft:end_rod ~0.15 ~1.00 ~-0.37 0.383 0.000 -0.924 0.32 0 force
particle minecraft:end_rod ~0.22 ~1.00 ~-0.33 0.556 0.000 -0.831 0.32 0 force
particle minecraft:end_rod ~0.28 ~1.00 ~-0.28 0.707 0.000 -0.707 0.32 0 force
particle minecraft:end_rod ~0.33 ~1.00 ~-0.22 0.831 0.000 -0.556 0.32 0 force
particle minecraft:end_rod ~0.37 ~1.00 ~-0.15 0.924 0.000 -0.383 0.32 0 force
particle minecraft:end_rod ~0.39 ~1.00 ~-0.08 0.981 0.000 -0.195 0.32 0 force
particle minecraft:white_ash ~0.40 ~0.40 ~0.00 1.000 0.000 0.000 0.2 0 force
particle minecraft:white_ash ~0.39 ~0.40 ~0.10 0.966 0.000 0.259 0.2 0 force
particle minecraft:white_ash ~0.35 ~0.40 ~0.20 0.866 0.000 0.500 0.2 0 force
particle minecraft:white_ash ~0.28 ~0.40 ~0.28 0.707 0.000 0.707 0.2 0 force
particle minecraft:white_ash ~0.20 ~0.40 ~0.35 0.500 0.000 0.866 0.2 0 force
particle minecraft:white_ash ~0.10 ~0.40 ~0.39 0.259 0.000 0.966 0.2 0 force
particle minecraft:white_ash ~0.00 ~0.40 ~0.40 0.000 0.000 1.000 0.2 0 force
particle minecraft:white_ash ~-0.10 ~0.40 ~0.39 -0.259 0.000 0.966 0.2 0 force
particle minecraft:white_ash ~-0.20 ~0.40 ~0.35 -0.500 0.000 0.866 0.2 0 force
particle minecraft:white_ash ~-0.28 ~0.40 ~0.28 -0.707 0.000 0.707 0.2 0 force
particle minecraft:white_ash ~-0.35 ~0.40 ~0.20 -0.866 0.000 0.500 0.2 0 force
particle minecraft:white_ash ~-0.39 ~0.40 ~0.10 -0.966 0.000 0.259 0.2 0 force
particle minecraft:white_ash ~-0.40 ~0.40 ~0.00 -1.000 0.000 0.000 0.2 0 force
particle minecraft:white_ash ~-0.39 ~0.40 ~-0.10 -0.966 0.000 -0.259 0.2 0 force
particle minecraft:white_ash ~-0.35 ~0.40 ~-0.20 -0.866 0.000 -0.500 0.2 0 force
particle minecraft:white_ash ~-0.28 ~0.40 ~-0.28 -0.707 0.000 -0.707 0.2 0 force
particle minecraft:white_ash ~-0.20 ~0.40 ~-0.35 -0.500 0.000 -0.866 0.2 0 force
particle minecraft:white_ash ~-0.10 ~0.40 ~-0.39 -0.259 0.000 -0.966 0.2 0 force
particle minecraft:white_ash ~-0.00 ~0.40 ~-0.40 -0.000 0.000 -1.000 0.2 0 force
particle minecraft:white_ash ~0.10 ~0.40 ~-0.39 0.259 0.000 -0.966 0.2 0 force
particle minecraft:white_ash ~0.20 ~0.40 ~-0.35 0.500 0.000 -0.866 0.2 0 force
particle minecraft:white_ash ~0.28 ~0.40 ~-0.28 0.707 0.000 -0.707 0.2 0 force
particle minecraft:white_ash ~0.35 ~0.40 ~-0.20 0.866 0.000 -0.500 0.2 0 force
particle minecraft:white_ash ~0.39 ~0.40 ~-0.10 0.966 0.000 -0.259 0.2 0 force
particle minecraft:flash{color:16774638} ~ ~1.2 ~ 0 0 0 0 1 force
particle minecraft:end_rod ~ ~1.4 ~ 0.4 0.8 0.4 0.25 60 force
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..48] ~ ~ ~ 1.6 0.6
playsound minecraft:block.beacon.deactivate hostile @a[distance=..48] ~ ~ ~ 1.4 0.8
playsound minecraft:entity.phantom.flap hostile @a[distance=..48] ~ ~ ~ 1.6 0.6
