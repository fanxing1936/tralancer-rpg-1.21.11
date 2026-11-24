playsound minecraft:block.bell.resonate player @a[distance=..24] ~ ~ ~ 1 1.3
particle minecraft:end_rod ~ ~1 ~ 4 0.6 4 0.02 80
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..8] at @s run function rpg:force/sk/11/one
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[16f,1f,16f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 26
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
summon minecraft:text_display ^ ^1.2 ^2 {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.25f,3.25f,3.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
