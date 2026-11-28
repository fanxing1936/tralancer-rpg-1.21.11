# 肋骨一斩（as/at 他）
execute positioned ^ ^ ^1.9 run tag @e[tag=rpg.unit.f,distance=..1.9] add rpg.mkb.hit
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit,distance=0..] run damage @s 5 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
execute if score #stage rpg_mk_i3 matches 2 as @e[tag=rpg.unit,tag=rpg.mkb.hit,distance=0..] run function rpg:michael_boss_i3/flame/add
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.hit
execute if score #r rpg_mk_i3 matches 1..3 run summon minecraft:text_display ^ ^1.3 ^1.5 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,-0.30071f,0.95372f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 30
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute if score #r rpg_mk_i3 matches 4..6 run summon minecraft:text_display ^ ^1.3 ^1.5 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0.95372f,0.30071f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 30
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
particle minecraft:flame ^ ^1.2 ^1.6 0.3 0.2 0.3 0.02 4
