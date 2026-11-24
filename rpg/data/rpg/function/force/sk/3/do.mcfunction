playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 1 0.8
playsound minecraft:block.beacon.activate player @a[distance=..16] ~ ~ ~ 0.6 1.8
particle minecraft:flame ~ ~0.3 ~ 2.6 0.2 2.6 0.03 160
particle minecraft:end_rod ~ ~1 ~ 0.4 0.4 0.4 0.25 50
execute if score #lv rpg_fo matches 1 run scoreboard players set #dmg rpg_fo 60
execute if score #lv rpg_fo matches 2 run scoreboard players set #dmg rpg_fo 80
execute if score #lv rpg_fo matches 3 run scoreboard players set #dmg rpg_fo 100
scoreboard players set #hm rpg_fo 10
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..5] at @s run function rpg:force/sk/3/one
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shock_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[11f,1f,11f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 25
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/scorch","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7f,1f,7f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 60
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
summon minecraft:text_display ^ ^0.8 ^2.2 {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 17
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
