execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.michael,distance=0..] run function rpg:prologue_michael/anim/enter/stomp
execute in rpg:armageddon_2 positioned 8 95.6 0 run summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.75f,8.75f,8.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_2 positioned 8 95.6 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 14
execute in rpg:armageddon_2 positioned 8 95.6 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 33
execute in rpg:armageddon_2 positioned 8 95.6 0 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute as @a[tag=rpg.pri2] at @s run playsound minecraft:entity.phantom.swoop master @s ~ ~ ~ 1.4 0.6
execute in rpg:armageddon_2 run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.michael,distance=0..] 8 94 0 90 0
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_2 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] -5.5 82.0 5.0 -117.8 -25.0
