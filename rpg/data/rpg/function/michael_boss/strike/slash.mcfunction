# 脊骨一挥（as/at 他）：身前 2.6 格那一点 2.4 格内
execute positioned ^ ^ ^2.6 run tag @e[tag=rpg.unit.f,distance=..2.4] add rpg.mkb.hit
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit] run damage @s 7 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1]
tag @e[tag=rpg.unit] remove rpg.mkb.hit
summon minecraft:text_display ^ ^1.4 ^2 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,-0.24192f,0.97030f],scale:[4.25f,4.25f,4.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 28
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ^0.6 ^1.9 ^2.4 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 7
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
particle minecraft:sweep_attack ^ ^1.2 ^2.2 0.5 0.2 0.5 0 2
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ^ ^1.3 ^2.4 0.6 0.3 0.6 0 6
