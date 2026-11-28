# 两道斩痕斩下（as/at 十字）
execute positioned ^ ^0.6 ^-4.5 run function rpg:michael_boss_i4/cross/line
execute rotated ~90 0 positioned ^ ^0.6 ^-4.5 run function rpg:michael_boss_i4/cross/line
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit,distance=0..] run damage @s 11 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
execute if score #stage rpg_mk_i4 matches 2 as @e[tag=rpg.unit,tag=rpg.mkb.hit,distance=0..] run function rpg:michael_boss_i4/flame/add
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.hit
execute positioned ^ ^0.08 ^-4.5 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/lane_f","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,4.5f],left_rotation:[0f,0f,0f,1f],scale:[0.8f,1f,9f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^ ^0.08 ^-4.5 run tp @e[tag=rpg.mkb.fxnew,limit=1,distance=0..] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 26
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute rotated ~90 0 positioned ^ ^0.08 ^-4.5 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/lane_f","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,4.5f],left_rotation:[0f,0f,0f,1f],scale:[0.8f,1f,9f],right_rotation:[0f,0f,0f,1f]}}
execute rotated ~90 0 positioned ^ ^0.08 ^-4.5 run tp @e[tag=rpg.mkb.fxnew,limit=1,distance=0..] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 26
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.75f,8.75f,8.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 35
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,5f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 32
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 7
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/scorch","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
particle minecraft:flame ~ ~0.5 ~ 2 0.2 2 0.03 20
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..24] ~ ~ ~ 1.2 1.4
kill @s
