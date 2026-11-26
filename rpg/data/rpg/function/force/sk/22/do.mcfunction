playsound minecraft:entity.ravager.roar player @a[distance=..24] ~ ~ ~ 0.7 0.6
particle minecraft:sculk_soul ~ ~1 ~ 3 0.5 3 0.02 50
particle minecraft:squid_ink ~ ~0.3 ~ 2.5 0.1 2.5 0.02 6
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,tag=!rpg.pope,tag=!rpg.mkb,tag=!rpg.jqb,tag=!rpg.lub,tag=!rpg.slb,tag=!rpg.usb,tag=!rpg.dtb,distance=..6] at @s run function rpg:force/sk/22/one
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[5974662]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[12f,1f,12f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 5
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
summon minecraft:text_display ^ ^1.2 ^2 {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#5B2A86"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
