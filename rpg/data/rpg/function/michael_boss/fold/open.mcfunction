# 六翼展开（as/at 他）：6 格内羽刃，击退；然后显形
tag @s remove rpg.mkb.fold
function rpg:michael/anim/enter/hero
tag @e[tag=rpg.unit.f,distance=..6] add rpg.mkb.hit
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit] run damage @s 8 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1]
tag @e[tag=rpg.unit] remove rpg.mkb.hit
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 18
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
particle minecraft:end_rod ~0.40 ~1.20 ~0.00 1.000 0.000 0.000 0.5 0 force
particle minecraft:end_rod ~0.39 ~1.20 ~0.10 0.966 0.000 0.259 0.5 0 force
particle minecraft:end_rod ~0.35 ~1.20 ~0.20 0.866 0.000 0.500 0.5 0 force
particle minecraft:end_rod ~0.28 ~1.20 ~0.28 0.707 0.000 0.707 0.5 0 force
particle minecraft:end_rod ~0.20 ~1.20 ~0.35 0.500 0.000 0.866 0.5 0 force
particle minecraft:end_rod ~0.10 ~1.20 ~0.39 0.259 0.000 0.966 0.5 0 force
particle minecraft:end_rod ~0.00 ~1.20 ~0.40 0.000 0.000 1.000 0.5 0 force
particle minecraft:end_rod ~-0.10 ~1.20 ~0.39 -0.259 0.000 0.966 0.5 0 force
particle minecraft:end_rod ~-0.20 ~1.20 ~0.35 -0.500 0.000 0.866 0.5 0 force
particle minecraft:end_rod ~-0.28 ~1.20 ~0.28 -0.707 0.000 0.707 0.5 0 force
particle minecraft:end_rod ~-0.35 ~1.20 ~0.20 -0.866 0.000 0.500 0.5 0 force
particle minecraft:end_rod ~-0.39 ~1.20 ~0.10 -0.966 0.000 0.259 0.5 0 force
particle minecraft:end_rod ~-0.40 ~1.20 ~0.00 -1.000 0.000 0.000 0.5 0 force
particle minecraft:end_rod ~-0.39 ~1.20 ~-0.10 -0.966 0.000 -0.259 0.5 0 force
particle minecraft:end_rod ~-0.35 ~1.20 ~-0.20 -0.866 0.000 -0.500 0.5 0 force
particle minecraft:end_rod ~-0.28 ~1.20 ~-0.28 -0.707 0.000 -0.707 0.5 0 force
particle minecraft:end_rod ~-0.20 ~1.20 ~-0.35 -0.500 0.000 -0.866 0.5 0 force
particle minecraft:end_rod ~-0.10 ~1.20 ~-0.39 -0.259 0.000 -0.966 0.5 0 force
particle minecraft:end_rod ~-0.00 ~1.20 ~-0.40 -0.000 0.000 -1.000 0.5 0 force
particle minecraft:end_rod ~0.10 ~1.20 ~-0.39 0.259 0.000 -0.966 0.5 0 force
particle minecraft:end_rod ~0.20 ~1.20 ~-0.35 0.500 0.000 -0.866 0.5 0 force
particle minecraft:end_rod ~0.28 ~1.20 ~-0.28 0.707 0.000 -0.707 0.5 0 force
particle minecraft:end_rod ~0.35 ~1.20 ~-0.20 0.866 0.000 -0.500 0.5 0 force
particle minecraft:end_rod ~0.39 ~1.20 ~-0.10 0.966 0.000 -0.259 0.5 0 force
summon minecraft:text_display ~ ~1.7 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[11.25f,11.25f,11.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 32
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 50
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 51
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 52
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 53
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 54
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 55
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 56
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.5 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 57
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6.25f,6.25f,6.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 4
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 7
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
particle minecraft:flame ~0.40 ~1.60 ~0.00 1.000 0.000 0.000 0.35 0 force
particle minecraft:flame ~0.37 ~1.60 ~0.15 0.924 0.000 0.383 0.35 0 force
particle minecraft:flame ~0.28 ~1.60 ~0.28 0.707 0.000 0.707 0.35 0 force
particle minecraft:flame ~0.15 ~1.60 ~0.37 0.383 0.000 0.924 0.35 0 force
particle minecraft:flame ~0.00 ~1.60 ~0.40 0.000 0.000 1.000 0.35 0 force
particle minecraft:flame ~-0.15 ~1.60 ~0.37 -0.383 0.000 0.924 0.35 0 force
particle minecraft:flame ~-0.28 ~1.60 ~0.28 -0.707 0.000 0.707 0.35 0 force
particle minecraft:flame ~-0.37 ~1.60 ~0.15 -0.924 0.000 0.383 0.35 0 force
particle minecraft:flame ~-0.40 ~1.60 ~0.00 -1.000 0.000 0.000 0.35 0 force
particle minecraft:flame ~-0.37 ~1.60 ~-0.15 -0.924 0.000 -0.383 0.35 0 force
particle minecraft:flame ~-0.28 ~1.60 ~-0.28 -0.707 0.000 -0.707 0.35 0 force
particle minecraft:flame ~-0.15 ~1.60 ~-0.37 -0.383 0.000 -0.924 0.35 0 force
particle minecraft:flame ~-0.00 ~1.60 ~-0.40 -0.000 0.000 -1.000 0.35 0 force
particle minecraft:flame ~0.15 ~1.60 ~-0.37 0.383 0.000 -0.924 0.35 0 force
particle minecraft:flame ~0.28 ~1.60 ~-0.28 0.707 0.000 -0.707 0.35 0 force
particle minecraft:flame ~0.37 ~1.60 ~-0.15 0.924 0.000 -0.383 0.35 0 force
scoreboard players set @s rpg_mk_so 30
function rpg:michael_boss/solid/on
playsound minecraft:entity.phantom.flap hostile @a[distance=..40] ~ ~ ~ 2 0.5
playsound minecraft:item.trident.riptide_3 hostile @a[distance=..40] ~ ~ ~ 1 1.2
