# 刺出一道直线（as/at 他，朝这个方向）：沿线判定 14
execute positioned ~ ~0.6 ~ run function rpg:saul_boss/line/hits
execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 14 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
tag @e[tag=rpg.unit,tag=rpg.slb.hit] add rpg.slb.failed
tag @e[tag=rpg.unit] remove rpg.slb.hit
execute positioned ~ ~0.06 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[15660282]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,15.0f],left_rotation:[0f,0f,0f,1f],scale:[1.4f,0.03f,30f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.06 ~ run tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 16
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 21
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
execute positioned ~ ~1.3 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,15.0f],left_rotation:[0f,0f,0f,1f],scale:[0.18f,0.18f,30f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~1.3 ~ run tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 16
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 21
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:crit ^ ^0.60 ^2.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^4.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^6.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^8.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^10.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^12.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^14.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^16.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^18.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^20.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^22.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^24.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^26.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^28.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:crit ^ ^0.60 ^30.00 0.3 0.15 0.3 0.2 2 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.20 ^3.00 0.2 0.1 0.2 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.20 ^6.00 0.2 0.1 0.2 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.20 ^9.00 0.2 0.1 0.2 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.20 ^12.00 0.2 0.1 0.2 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.20 ^15.00 0.2 0.1 0.2 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.20 ^18.00 0.2 0.1 0.2 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.20 ^21.00 0.2 0.1 0.2 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.20 ^24.00 0.2 0.1 0.2 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.20 ^27.00 0.2 0.1 0.2 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.20 ^30.00 0.2 0.1 0.2 0 1 force
playsound minecraft:item.trident.throw hostile @a[distance=..40] ~ ~ ~ 1.3 1.2
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1 1.5
