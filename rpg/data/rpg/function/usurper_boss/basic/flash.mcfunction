summon minecraft:text_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#B784D6"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.25f,2.25f,2.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 4
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
