effect give @s minecraft:wither 3 1 true
particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.2} ~ ~1 ~ 0.3 0.5 0.3 0 12
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#8B0A1E"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 8
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 13
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
