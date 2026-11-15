# 被灌注的罪仆身上绕三枚原作符文（骑在它身上）
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.irune","rpg.usb.ifx"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0.7f,-0.5f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.375f,1.375f,1.375f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.irune","rpg.usb.ifx"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[-0.7f,-0.2f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.375f,1.375f,1.375f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.irune","rpg.usb.ifx"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.375f,1.375f,1.375f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.usb.fxnew,tag=rpg.usb.irune] run ride @s mount @e[tag=rpg.usb.infused,limit=1,sort=nearest]
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 140
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
