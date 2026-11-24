playsound minecraft:item.trident.thunder player @a[distance=..32] ~ ~ ~ 1 1.4
playsound minecraft:block.beacon.power_select player @a[distance=..32] ~ ~ ~ 1 0.8
scoreboard players set #dmg rpg_fo 180
scoreboard players set #hm rpg_fo 15
execute positioned ^ ^ ^3 run tag @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..2.0] add rpg.fo.jd
particle minecraft:end_rod ^ ^1.2 ^3 1.0 0.6 1.0 0.02 18
execute positioned ^ ^ ^6 run tag @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..2.8] add rpg.fo.jd
particle minecraft:end_rod ^ ^1.2 ^6 1.4 0.6 1.4 0.02 24
execute positioned ^ ^ ^9 run tag @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..3.6] add rpg.fo.jd
particle minecraft:end_rod ^ ^1.2 ^9 1.8 0.6 1.8 0.02 30
execute positioned ^ ^ ^12 run tag @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..4.4] add rpg.fo.jd
particle minecraft:end_rod ^ ^1.2 ^12 2.2 0.6 2.2 0.02 36
execute positioned ^ ^ ^15 run tag @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..5.2] add rpg.fo.jd
particle minecraft:end_rod ^ ^1.2 ^15 2.6 0.6 2.6 0.02 42
execute positioned ^ ^ ^18 run tag @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..6.0] add rpg.fo.jd
particle minecraft:end_rod ^ ^1.2 ^18 3.0 0.6 3.0 0.02 48
execute as @e[tag=rpg.fo.jd] at @s run function rpg:force/x/f/hal_one
tag @e[tag=rpg.fo.jd] remove rpg.fo.jd
summon minecraft:item_display ^ ^0.06 ^8 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[16f,1f,16f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 23
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:text_display ^ ^1.8 ^7 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,5f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
