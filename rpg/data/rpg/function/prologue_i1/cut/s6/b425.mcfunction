function rpg:prologue_i1/cut/shatter
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer,distance=0..] run function rpg:prologue_lucifer/anim/enter/stomped
execute in rpg:armageddon positioned 1.5 81 0 run summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,7.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,18f,0.6f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 1.5 81 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 30
execute in rpg:armageddon positioned 1.5 81 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 49
execute in rpg:armageddon positioned 1.5 81 0 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 1.5 82 0 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[10f,10f,10f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 1.5 82 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
execute in rpg:armageddon positioned 1.5 82 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 32
execute in rpg:armageddon positioned 1.5 82 0 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 1.5 82 0 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 1.5 82 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
execute in rpg:armageddon positioned 1.5 82 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 7
execute in rpg:armageddon positioned 1.5 82 0 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 0 80.1 0 run summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[9f,1f,9f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 0 80.1 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
execute in rpg:armageddon positioned 0 80.1 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 40
execute in rpg:armageddon positioned 0 80.1 0 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute as @a[tag=rpg.pri1] at @s run playsound minecraft:entity.generic.explode master @s ~ ~ ~ 1.4 0.6
execute as @a[tag=rpg.pri1] at @s run playsound minecraft:entity.warden.sonic_boom master @s ~ ~ ~ 0.8 0.7
