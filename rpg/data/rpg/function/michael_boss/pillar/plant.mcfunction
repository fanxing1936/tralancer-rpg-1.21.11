# 脊骨插进场地中心（at 中心）：一根比人高的骨柱，立到战斗结束
summon minecraft:item_display ~ ~2.3 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.pillar"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_boss/spine"}},item_display:"none",brightness:{sky:15,block:13},view_range:4f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,-0.9238795f,0.3826834f],scale:[4.5f,4.5f,4.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 30000
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/core","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 24
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 22
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,7.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,18f,0.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 30
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 49
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
summon minecraft:item_display ~ ~0.04 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/scorch","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 30000
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,1f,8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 41
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.75f,8.75f,8.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 4
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 7
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/seal_seraph","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7f,1f,7f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 30000
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 16
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
particle minecraft:block{block_state:"minecraft:bone_block"} ~ ~0.5 ~ 0.8 0.3 0.8 0 40
particle minecraft:flash{color:16765117} ~ ~2 ~ 0 0 0 0 1 force
playsound minecraft:block.bone_block.break hostile @a[distance=..48] ~ ~ ~ 2 0.5
playsound minecraft:item.trident.hit_ground hostile @a[distance=..48] ~ ~ ~ 1.5 0.6
