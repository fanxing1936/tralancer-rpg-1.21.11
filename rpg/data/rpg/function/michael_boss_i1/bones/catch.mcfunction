# 接回肋骨（as/at 他）
kill @e[tag=rpg.mkb.rib,distance=0..]
kill @e[tag=rpg.mkb.orb,distance=0..]
function rpg:michael/weapon/rib
function rpg:michael/anim/enter/rib_slash5
particle minecraft:flame ~ ~1.2 ~ 0.5 0.6 0.5 0.05 16
summon minecraft:text_display ~ ~1.7 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.5f,7.5f,7.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 33
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.3 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,5f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 32
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.3 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 7
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
playsound minecraft:item.trident.return hostile @a[distance=..48] ~ ~ ~ 1.4 0.8
