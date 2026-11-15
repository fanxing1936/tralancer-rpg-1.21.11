execute as @e[tag=rpg.al.aim,limit=1] run damage @s 8 minecraft:mob_projectile by @e[tag=rpg.al.cur,limit=1]
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.jqa.fx","rpg.jqa.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF2C8"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.5f,2.5f,2.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_life 10
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_kd 3
tag @e[tag=rpg.jqa.fxnew] remove rpg.jqa.fxnew
particle minecraft:crit ~ ~ ~ 0.2 0.2 0.2 0.4 8
playsound rpg:jacques.arrow player @a[distance=..16] ~ ~ ~ 0.6 1.2
