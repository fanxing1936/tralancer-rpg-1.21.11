summon minecraft:text_display ~ ~0.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 32
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
