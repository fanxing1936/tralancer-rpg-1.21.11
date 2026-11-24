execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.michael] run function rpg:prologue_michael/anim/enter/dive_cry
execute in rpg:armageddon positioned 4 120.5 0 run summon minecraft:text_display ~ ~1.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.75f,8.75f,8.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned 4 120.5 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 14
execute in rpg:armageddon positioned 4 120.5 0 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 33
execute in rpg:armageddon positioned 4 120.5 0 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
execute in rpg:armageddon run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.michael] 4 119 0 90 0
