# 招架起手（as/at 他）：剑身一道银光
summon minecraft:text_display ^0.2 ^1.5 ^0.7 {Tags:["rpg.slb.fx","rpg.slb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#EEF4FA"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 16
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 4
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:text_display ^0.3 ^1.9 ^0.6 {Tags:["rpg.slb.fx","rpg.slb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#EEF4FA"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 10
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 7
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:end_rod ^ ^1.5 ^0.7 0.1 0.3 0.1 0.02 6
