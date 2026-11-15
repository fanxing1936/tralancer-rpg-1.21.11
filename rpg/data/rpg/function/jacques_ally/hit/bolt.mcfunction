# 竖琴弩（as/at 他）：一道金色弩光直达目标
execute positioned ~ ~1.45 ~ facing entity @e[tag=rpg.al.aim,limit=1] eyes positioned ^ ^ ^0.9 run function rpg:jacques_ally/hit/fly
scoreboard players set #d rpg_al 0
summon minecraft:text_display ^ ^1.45 ^1.1 {Tags:["rpg.jqa.fx","rpg.jqa.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF2C8"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_life 8
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_kd 10
tag @e[tag=rpg.jqa.fxnew] remove rpg.jqa.fxnew
particle minecraft:electric_spark ^ ^1.45 ^1.2 0.15 0.15 0.15 0.4 8
