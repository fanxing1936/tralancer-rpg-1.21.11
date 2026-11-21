# 火灭（as/at 他）
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6.25f,6.25f,6.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 36
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
particle minecraft:large_smoke ~ ~0.5 ~ 14 0.3 14 0.02 60
playsound minecraft:block.fire.extinguish hostile @a[distance=..48] ~ ~ ~ 1.4 0.6
