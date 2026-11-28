kill @e[type=minecraft:item_display,tag=rpg.pr.wisp,distance=0..]
execute in rpg:armageddon positioned 0 87.5 -9 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
execute in rpg:armageddon positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 4
execute in rpg:armageddon positioned 0 87.5 -9 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 0 87.5 -9 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
execute in rpg:armageddon positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 7
execute in rpg:armageddon positioned 0 87.5 -9 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
particle minecraft:reverse_portal 0 87.5 -9 1.5 2 0.3 0.3 120
particle minecraft:witch 0 87.5 -9 1 1.5 0.3 0 40
execute as @a[tag=rpg.pri1] at @s run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1.2 0.6
