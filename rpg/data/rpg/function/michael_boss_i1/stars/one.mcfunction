summon minecraft:text_display ~ ~14 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.meteor"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:0,interpolation_duration:3,view_range:4f,transformation:{translation:[0f,1.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 14
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 47
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
