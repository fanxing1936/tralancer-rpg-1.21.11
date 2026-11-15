# 一阶段普攻（as/at 载体）：远处射书页弹，贴身就横扫
function rpg:usurper/anim/enter/attack
scoreboard players set @s rpg_ub_busy 21
execute if entity @e[tag=rpg.unit.f,distance=..3.5] run return run function rpg:usurper_boss/basic/sweep
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] eyes positioned ^ ^1.6 ^0.8 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew","rpg.usb.bolt"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper/paper1","minecraft:custom_model_data":{colors:[16050687]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0.70710677f,0f,0.70710677f],scale:[8f,8f,8f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.usb.fxnew] at @s run tp @s ~ ~ ~ facing entity @e[tag=rpg.unit.f,distance=..27,sort=nearest,limit=1] eyes
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 30
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 0
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] eyes positioned ^ ^1.6 ^0.8 run function rpg:usurper_boss/basic/flash
