scoreboard players set #rift rpg_pr_i2 2
scoreboard players set #smoke rpg_pr_i2 0
execute in rpg:armageddon_2 run particle minecraft:flash{color:[0.5,0.3,0.8,1.0]} 0 87.5 -9 0 0 0 0 1 force
execute in rpg:armageddon_2 positioned 0 87.5 -9 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[10f,10f,10f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_2 positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
execute in rpg:armageddon_2 positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 4
execute in rpg:armageddon_2 positioned 0 87.5 -9 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute in rpg:armageddon_2 positioned 0 87.5 -9 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_2 positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
execute in rpg:armageddon_2 positioned 0 87.5 -9 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 7
execute in rpg:armageddon_2 positioned 0 87.5 -9 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute as @a[tag=rpg.pri2] at @s run playsound minecraft:block.end_portal_frame.fill master @s ~ ~ ~ 1 0.5
