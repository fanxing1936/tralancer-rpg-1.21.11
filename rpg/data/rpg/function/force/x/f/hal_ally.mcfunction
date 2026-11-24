summon minecraft:text_display ~ ~2.3 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.375f,1.375f,1.375f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 24
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 20
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
