execute as @e[tag=rpg.unit,tag=rpg.mkb.hit,distance=0..] run damage @s 10 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
execute if score #stage rpg_mk_i3 matches 2 as @e[tag=rpg.unit,tag=rpg.mkb.hit,distance=0..] run function rpg:michael_boss_i3/flame/add
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.hit
summon minecraft:text_display ^ ^1.2 ^1 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 30
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ^ ^1.2 ^1 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 32
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ^ ^1.2 ^1 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 7
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
