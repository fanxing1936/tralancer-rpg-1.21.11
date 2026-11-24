playsound minecraft:entity.skeleton.hurt player @a[distance=..16] ~ ~ ~ 1 0.5
playsound minecraft:block.sculk.spread player @a[distance=..16] ~ ~ ~ 1 0.8
particle minecraft:dust{color:[0.55,0.5,0.38],scale:1.4} ^ ^1 ^3 1.6 0.6 1.6 0 50
particle minecraft:squid_ink ^ ^1 ^3 1.2 0.4 1.2 0.02 4
execute positioned ^ ^ ^2 as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..2,tag=!rpg.fo.hit] at @s run function rpg:force/sk/15/one
execute positioned ^ ^ ^4.5 as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..2.5,tag=!rpg.fo.hit] at @s run function rpg:force/sk/15/one
tag @e[tag=rpg.fo.hit] remove rpg.fo.hit
summon minecraft:text_display ^ ^1.2 ^3 {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#B8A88A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 8
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 13
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
summon minecraft:item_display ^ ^0.06 ^3 {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/cracks","minecraft:custom_model_data":{colors:[4865834]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 60
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
