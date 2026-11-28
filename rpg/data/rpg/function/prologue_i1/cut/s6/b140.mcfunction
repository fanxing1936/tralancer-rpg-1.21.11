execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.beelzebub,distance=0..] run function rpg:prologue_beelzebub/anim/enter/shield
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer,distance=0..] run function rpg:prologue_lucifer/anim/enter/tear
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer,distance=0..] run function rpg:prologue_lucifer/look/possessed
scoreboard players set #rift rpg_pr_i1 1
execute in rpg:armageddon positioned 0 87.5 -9 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[10f,10f,10f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
execute in rpg:armageddon positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 4
execute in rpg:armageddon positioned 0 87.5 -9 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute in rpg:armageddon positioned 0 87.5 -9 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
execute in rpg:armageddon positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 7
execute in rpg:armageddon positioned 0 87.5 -9 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
particle minecraft:reverse_portal 0 87.5 -9 3 4 0.3 0.6 400
execute as @a[tag=rpg.pri1] at @s run playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.9 0.6
execute as @a[tag=rpg.pri1] at @s run playsound minecraft:entity.wither.spawn master @s ~ ~ ~ 0.5 1.6
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] 5.0 82.5 6.0 160.3 -9.5
