execute in rpg:armageddon_3 positioned 0 35.6 0 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.5f,7.5f,7.5f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_3 positioned 0 35.6 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
execute in rpg:armageddon_3 positioned 0 35.6 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 32
execute in rpg:armageddon_3 positioned 0 35.6 0 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute in rpg:armageddon_3 positioned 0 35.6 0 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_3 positioned 0 35.6 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
execute in rpg:armageddon_3 positioned 0 35.6 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 7
execute in rpg:armageddon_3 positioned 0 35.6 0 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute as @a[tag=rpg.pri3] at @s run playsound minecraft:entity.generic.explode master @s ~ ~ ~ 0.8 0.4
