execute in rpg:armageddon run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.michael] 4 81 0 90 0
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.michael] run function rpg:prologue_michael/anim/enter/land
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer] run function rpg:prologue_lucifer/anim/enter/look_up
execute in rpg:armageddon run particle minecraft:explosion_emitter 4 81.5 0 0 0 0 0 1 force
execute in rpg:armageddon run particle minecraft:end_rod 4 81.5 0 2.5 0.3 2.5 0.25 160 force
execute as @a[tag=rpg.pr] at @s run playsound minecraft:entity.generic.explode master @s ~ ~ ~ 0.8 0.7
execute as @a[tag=rpg.pr] at @s run playsound minecraft:entity.phantom.flap master @s ~ ~ ~ 1.2 0.5
execute in rpg:armageddon positioned 4 81 0 run summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,7.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,18f,0.6f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 81 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 30
execute in rpg:armageddon positioned 4 81 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 49
execute in rpg:armageddon positioned 4 81 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 4 82 0 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.5f,7.5f,7.5f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 82 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 16
execute in rpg:armageddon positioned 4 82 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 4
execute in rpg:armageddon positioned 4 82 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 4 82 0 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 82 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 10
execute in rpg:armageddon positioned 4 82 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 7
execute in rpg:armageddon positioned 4 82 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 4 81.06 0 run summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 81.06 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 16
execute in rpg:armageddon positioned 4 81.06 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 41
execute in rpg:armageddon positioned 4 81.06 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 4 83 0 run summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 52
execute in rpg:armageddon positioned 4 83 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 4 83 0 run summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 53
execute in rpg:armageddon positioned 4 83 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 4 83 0 run summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 54
execute in rpg:armageddon positioned 4 83 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 4 83 0 run summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 55
execute in rpg:armageddon positioned 4 83 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 4 83 0 run summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 56
execute in rpg:armageddon positioned 4 83 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 4 83 0 run summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 57
execute in rpg:armageddon positioned 4 83 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 4 83 0 run summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 58
execute in rpg:armageddon positioned 4 83 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 4 83 0 run summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
execute in rpg:armageddon positioned 4 83 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 59
execute in rpg:armageddon positioned 4 83 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] -5.0 82.6 3.4 -110.0 0.0
