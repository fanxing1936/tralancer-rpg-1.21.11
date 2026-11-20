summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#EEF4FA"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.75f,2.75f,2.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 8
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 13
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:sweep_attack ~ ~1 ~ 0.2 0.2 0.2 0 1
particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.4 6
