# 一座圣坛（at 2×2 的方块角）：原作地卜师石柱，白金，从地下升起；16 刻后铺屏障方块，人能站上去
summon minecraft:marker ~ ~ ~ {Tags:["rpg.usb.altar"]}
execute positioned ~1 ~ ~1 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/pillar","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,-2.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[26.7f,7.4f,26.7f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 136
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 17
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~1 ~0.05 ~1 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.2f,1f,3.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 120
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~1 ~2 ~1 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF6DC"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,2.1f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,0.01f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 92
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 9
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
particle minecraft:end_rod ~1 ~1 ~1 0.5 1 0.5 0.05 20
playsound minecraft:block.stone.place hostile @a[distance=..32] ~ ~ ~ 1 0.5
