summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.spoke"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:4f,transformation:{translation:[0f,1.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.mkb.fxnew] run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 42
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
