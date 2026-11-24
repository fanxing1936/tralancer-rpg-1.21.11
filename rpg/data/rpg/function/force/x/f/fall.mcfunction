scoreboard players operation @s rpg_fo_fl = #now rpg_fo
scoreboard players add @s rpg_fo_fl 200
playsound minecraft:entity.wither.spawn player @a[distance=..32] ~ ~ ~ 0.5 1.6
playsound minecraft:entity.phantom.flap player @a[distance=..16] ~ ~ ~ 1 0.6
particle minecraft:smoke ^ ^1 ^-1.6 0.5 0.8 0.5 0.03 30
title @s actionbar {"text":"堕天：10 秒内魔力技能不耗力、不涨魔化","color":"#A276BE","bold":true,"italic":false}
summon minecraft:text_display ^ ^1.6 ^-1.8 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"#8A5AB0"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 14
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 19
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.xm","rpg.fo.xmnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[5974662]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_life 40
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.xmnew] remove rpg.fo.xmnew
