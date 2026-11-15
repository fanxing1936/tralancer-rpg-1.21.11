# 书页横扫：身前一道原作的弧光（贴在胸口高度，朝他面向的方向）
execute positioned ^ ^ ^1.5 run execute as @e[tag=rpg.unit.f,distance=..2.4] run damage @s 8 minecraft:magic by @e[type=minecraft:vindicator,tag=rpg.usb,limit=1]
execute positioned ^ ^1.1 ^1.2 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/crescent","minecraft:custom_model_data":{colors:[15259135]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.usb.fxnew] positioned as @s run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 8
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 10
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
particle minecraft:enchant ^ ^1 ^1.5 1 0.3 1 1 24
playsound minecraft:item.book.page_turn hostile @a[distance=..16] ~ ~ ~ 1 0.8
