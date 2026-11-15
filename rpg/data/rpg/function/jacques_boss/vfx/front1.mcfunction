# 坟墓克星下劈（as/at 他）：金色双层弧光、火花
summon minecraft:text_display ^ ^1.2 ^1.6 {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#F0CF7A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 13
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ^ ^1.25 ^1.7 {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF2C8"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.25f,2.25f,2.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 13
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ^ ^1 ^2 {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF2C8"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 10
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:crit ^ ^1 ^1.8 0.6 0.4 0.6 0.3 14
particle minecraft:enchanted_hit ^ ^1.1 ^1.8 0.5 0.4 0.5 0.3 10
particle minecraft:electric_spark ^ ^0.4 ^2 0.4 0.1 0.4 0.3 8
