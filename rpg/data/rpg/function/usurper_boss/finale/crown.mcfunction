# 王冠碎裂（as/at 载体）：头部换成不带王冠的那份，碎片四散
execute on passengers if entity @s[tag=rpg.prime_enchanter.p.head] run data modify entity @s item.components."minecraft:item_model" set value "rpg:usurper_fx/pe_head_bare"
summon minecraft:text_display ~ ~2.5 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF6DC"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.125f,3.125f,3.125f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 16
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 5
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~ ~2.5 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#F0CF7A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 4
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~2.5 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.shard0"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/crown","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:20,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 30
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~2.5 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.shard1"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/crown","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:20,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 30
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~2.5 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.shard2"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/crown","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:20,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 30
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~2.5 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.shard3"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/crown","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:20,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 30
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~2.5 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.shard4"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/crown","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:20,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 30
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~2.5 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.shard5"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/crown","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:20,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 30
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
particle minecraft:end_rod ~ ~2.5 ~ 0.3 0.3 0.3 0.15 30
playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 1.4 0.6
playsound minecraft:block.beacon.deactivate hostile @a[distance=..48] ~ ~ ~ 1.2 0.8
