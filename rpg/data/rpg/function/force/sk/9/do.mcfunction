playsound minecraft:block.beacon.power_select player @a[distance=..24] ~ ~ ~ 1 1.6
particle minecraft:end_rod ~ ~1 ~ 8 1.5 8 0 120
execute as @e[type=!player,distance=..16] run effect clear @s minecraft:invisibility
execute if score #lv rpg_fo matches 1 run effect give @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..16] minecraft:glowing 6 0 true
execute if score #lv rpg_fo matches 2 run effect give @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..16] minecraft:glowing 8 0 true
execute if score #lv rpg_fo matches 3 run effect give @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..16] minecraft:glowing 10 0 true
execute if score #lv rpg_fo matches 1 run effect give @e[tag=rpg.vacant,distance=..16] minecraft:glowing 6 0 true
execute if score #lv rpg_fo matches 2 run effect give @e[tag=rpg.vacant,distance=..16] minecraft:glowing 8 0 true
execute if score #lv rpg_fo matches 3 run effect give @e[tag=rpg.vacant,distance=..16] minecraft:glowing 10 0 true
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[30f,1f,30f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 26
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
summon minecraft:text_display ^ ^2.8 ^2.5 {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.75f,2.75f,2.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 14
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 18
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
