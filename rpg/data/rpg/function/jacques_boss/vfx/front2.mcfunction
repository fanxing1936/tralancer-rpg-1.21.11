# 燃刃下劈（as/at 他）：火色双层弧光、火星迸溅
summon minecraft:text_display ^ ^1.2 ^1.6 {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FF8A3D"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 13
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ^ ^1.25 ^1.7 {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFD08A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.25f,2.25f,2.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 13
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ^ ^1 ^2 {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFD08A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 10
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:crit ^ ^1 ^1.8 0.6 0.4 0.6 0.3 10
particle minecraft:flame ^ ^1 ^1.8 0.5 0.4 0.5 0.06 16
particle minecraft:lava ^ ^0.6 ^2 0.3 0.1 0.3 0 3
particle minecraft:dust_color_transition{from_color:[1.0,0.62,0.2],to_color:[0.35,0.04,0.0],scale:1.4} ^ ^1 ^1.8 0.6 0.4 0.6 0 6
