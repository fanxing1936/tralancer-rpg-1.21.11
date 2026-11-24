function rpg:force/hit
particle minecraft:end_rod ~ ~1 ~ 0.2 0.8 0.2 0.1 12
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 16
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
