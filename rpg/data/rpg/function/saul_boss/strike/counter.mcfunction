execute positioned ^ ^ ^2.2 run tag @e[tag=rpg.unit.f,distance=..1.8] add rpg.slb.hit
execute if score @s rpg_sl matches 1 as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 6 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
execute if score @s rpg_sl matches 2 as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 5 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
tag @e[tag=rpg.unit,tag=rpg.slb.hit] add rpg.slb.failed
tag @e[tag=rpg.unit] remove rpg.slb.hit
execute positioned ^ ^1.35 ^0.9 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,1.6f],left_rotation:[0f,0f,0f,1f],scale:[0.12f,0.12f,3.2f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^ ^1.35 ^0.9 run tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 8
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 20
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:crit ^ ^1.35 ^3.8 0.15 0.15 0.15 0.3 4
particle minecraft:crit ^ ^1.3 ^2 0.3 0.3 0.3 0.5 10
