# 横扫（as/at 他）：身前约 80°、4.5 格内的敌人
execute positioned ^ ^ ^1.4 as @e[type=#rpg:seal_hostile,type=!minecraft:creeper,tag=!rpg.ally,tag=!rpg.jqd,tag=!rpg.jqb.preview,nbt=!{Invulnerable:1b},distance=..3.2] run damage @s 12 minecraft:mob_attack by @e[tag=rpg.al.cur,limit=1]
execute positioned ^ ^1.1 ^1.2 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqa.fx","rpg.jqa.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/crescent","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.jqa.fxnew] positioned as @s run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_life 8
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_kd 15
tag @e[tag=rpg.jqa.fxnew] remove rpg.jqa.fxnew
particle minecraft:sweep_attack ^ ^1 ^1.8 0.8 0.2 0.8 0 4
particle minecraft:end_rod ^-2.6 ^1.1 ^1.5 0.15 0.15 0.15 0.05 2
particle minecraft:end_rod ^-1.93 ^1.1 ^2.3 0.15 0.15 0.15 0.05 2
particle minecraft:end_rod ^-1.03 ^1.1 ^2.82 0.15 0.15 0.15 0.05 2
particle minecraft:end_rod ^0.0 ^1.1 ^3.0 0.15 0.15 0.15 0.05 2
particle minecraft:end_rod ^1.03 ^1.1 ^2.82 0.15 0.15 0.15 0.05 2
particle minecraft:end_rod ^1.93 ^1.1 ^2.3 0.15 0.15 0.15 0.05 2
particle minecraft:end_rod ^2.6 ^1.1 ^1.5 0.15 0.15 0.15 0.05 2
