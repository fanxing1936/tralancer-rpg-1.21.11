# 下劈（as/at 他）
summon minecraft:text_display ^ ^0.5 ^2 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 4
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ^ ^0.5 ^2 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 7
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:item_display ^ ^0.1 ^2 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 40
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
