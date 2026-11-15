summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#C04A3C"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.25f,2.25f,2.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 16
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 5
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
particle minecraft:enchant ~ ~1 ~ 0.4 0.6 0.4 1.5 30
playsound minecraft:block.enchantment_table.use hostile @s ~ ~ ~ 1 1.6
