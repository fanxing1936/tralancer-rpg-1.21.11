# 全睁（as/at 他）：全屏一闪，黑暗，场上所有人挨一下；背对他的减半；每只活着的守望者 +6
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.away
execute as @e[tag=rpg.unit.f,distance=..44] at @s rotated ~ 0 positioned ^ ^ ^100 unless entity @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,distance=..100] run tag @s add rpg.mkb.away
execute store result score #w rpg_mk_i2 if entity @e[type=minecraft:vindicator,tag=rpg.mkb.w,distance=0..]
execute if score #w rpg_mk_i2 matches 0 as @e[tag=rpg.unit.f,distance=..44,tag=!rpg.mkb.away] run damage @s 12 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
execute if score #w rpg_mk_i2 matches 0 as @e[tag=rpg.unit.f,distance=..44,tag=rpg.mkb.away] run damage @s 6 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
execute if score #w rpg_mk_i2 matches 1 as @e[tag=rpg.unit.f,distance=..44,tag=!rpg.mkb.away] run damage @s 18 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
execute if score #w rpg_mk_i2 matches 1 as @e[tag=rpg.unit.f,distance=..44,tag=rpg.mkb.away] run damage @s 9 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
execute if score #w rpg_mk_i2 matches 2 as @e[tag=rpg.unit.f,distance=..44,tag=!rpg.mkb.away] run damage @s 24 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
execute if score #w rpg_mk_i2 matches 2 as @e[tag=rpg.unit.f,distance=..44,tag=rpg.mkb.away] run damage @s 12 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
execute if score #w rpg_mk_i2 matches 3.. as @e[tag=rpg.unit.f,distance=..44,tag=!rpg.mkb.away] run damage @s 30 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
execute if score #w rpg_mk_i2 matches 3.. as @e[tag=rpg.unit.f,distance=..44,tag=rpg.mkb.away] run damage @s 15 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
title @a[distance=..48] times 0 3 0
title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
summon minecraft:text_display ~ ~1.8 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[12.5f,12.5f,12.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 33
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,7.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,18f,0.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 30
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 49
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.75f,8.75f,8.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 32
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
summon minecraft:text_display ~ ~2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 7
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute as @e[tag=rpg.mkb.eye,distance=0..] at @s run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.04 4
effect give @a[distance=..44,gamemode=!spectator,gamemode=!creative] minecraft:darkness 2 0 true
execute as @e[tag=rpg.mkb.eye,distance=0..] at @s run particle minecraft:flash{color:16724736} ~ ~ ~ 0 0 0 0 1 force
particle minecraft:flash{color:16765117} ~ ~2 ~ 0 0 0 0 1 force
playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..48] ~ ~ ~ 2 0.6
playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 2 0.5
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.away
