# 第 2 名圣卫（as 载体，at 落点）
function rpg:holy_guard/summon
tag @e[type=minecraft:vindicator,tag=rpg.hg,tag=!rpg.usb.guard,distance=..2,limit=1,sort=nearest] add rpg.usb.gnew
tag @e[tag=rpg.usb.gnew] add rpg.usb.unit
tag @e[tag=rpg.usb.gnew] add rpg.usb.guard
scoreboard players set @e[tag=rpg.usb.gnew] rpg_ub_id 2
tag @e[tag=rpg.usb.gnew] remove rpg.usb.gnew
tag @s add rpg.usb.guarded
execute at @s positioned ~ ~1.6 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.abeam"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/bolt_beam","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:2,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew,tag=rpg.usb.abeam] rpg_ub_id 2
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 24000
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sq_0","minecraft:custom_model_data":{colors:[16774876]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 8
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 16
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.6f,1f,2.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 30
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 1
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF6DC"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,2.1f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,0.01f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 16
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 8
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
particle minecraft:end_rod ~ ~1 ~ 0.4 1 0.4 0.05 20
playsound minecraft:block.beacon.activate hostile @a[distance=..32] ~ ~ ~ 1 1.4
