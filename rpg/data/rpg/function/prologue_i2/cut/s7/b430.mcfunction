function rpg:prologue_i2/sub/n09
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.michael,distance=0..] run function rpg:prologue_michael/anim/enter/rise
execute as @a[tag=rpg.pri2] at @s run playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 1 1.2
execute in rpg:armageddon_2 positioned 0 81 -2 run summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,7.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,18f,0.6f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_2 positioned 0 81 -2 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 30
execute in rpg:armageddon_2 positioned 0 81 -2 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 49
execute in rpg:armageddon_2 positioned 0 81 -2 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_2 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] 0.0 82.0 8.0 -180.0 -31.0
