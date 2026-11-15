# 第 5 道光束：先是一条细线（as 方向标记，at 起点，朝光束方向）
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.jb4"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,10.0f],left_rotation:[0f,0f,0f,1f],scale:[0.06f,0.06f,20f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.usb.fxnew] run tp @s ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 28
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ^ ^ ^20 {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF6DC"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 7
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
playsound minecraft:block.beacon.ambient hostile @a[distance=..40] ~ ~ ~ 1 2
