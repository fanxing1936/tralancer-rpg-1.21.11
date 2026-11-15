execute positioned ~ ~ ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.mpil"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,20f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,40f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.usb.fxnew] run tp @s ~ ~ ~ ~ -90
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 125
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 19
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.03 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/glow","minecraft:custom_model_data":{colors:[12095535]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[10f,1f,10f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 120
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,1f,8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 120
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.09 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/storm","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7f,1f,7f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 120
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 1.4 0.6
playsound minecraft:block.beacon.activate hostile @a[distance=..48] ~ ~ ~ 1.2 0.8
