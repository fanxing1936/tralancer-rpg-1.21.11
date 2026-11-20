# 举脊骨蓄力（as/at 他）：身后一圈光环，脚下圣印
summon minecraft:text_display ~ ~2.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 22
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 44
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.07 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/seal_seraph","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 24
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 15
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
