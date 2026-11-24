tag @s add rpg.fo.hit
scoreboard players set #stop rpg_fo 1
execute if score #lv rpg_fo matches 1 run effect give @s minecraft:slowness 2 9 true
execute if score #lv rpg_fo matches 2 run effect give @s minecraft:slowness 3 9 true
execute if score #lv rpg_fo matches 3 run effect give @s minecraft:slowness 4 9 true
execute if score #lv rpg_fo matches 1 run effect give @s minecraft:jump_boost 2 250 true
execute if score #lv rpg_fo matches 2 run effect give @s minecraft:jump_boost 3 250 true
execute if score #lv rpg_fo matches 3 run effect give @s minecraft:jump_boost 4 250 true
execute if score #lv rpg_fo matches 1 run effect give @s minecraft:weakness 2 1 true
execute if score #lv rpg_fo matches 2 run effect give @s minecraft:weakness 3 1 true
execute if score #lv rpg_fo matches 3 run effect give @s minecraft:weakness 4 1 true
particle minecraft:dust{color:[1.0,0.85,0.35],scale:1.2} ~ ~1 ~ 0.4 0.7 0.4 0 40
playsound minecraft:block.chain.place hostile @a[distance=..16] ~ ~ ~ 1 0.6
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/xmark","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,1f,2.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 60
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.6f,1f,2.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 60
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
summon minecraft:item_display ~ ~1 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:force_vfx/chain","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.0f,0.01f,1.0f],right_rotation:[0f,0f,0f,1f]},Rotation:[0f,0f]}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 60
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 24
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:item_display ~ ~1 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:force_vfx/chain","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.0f,0.01f,1.0f],right_rotation:[0f,0f,0f,1f]},Rotation:[60f,0f]}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 60
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 24
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:item_display ~ ~1 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:force_vfx/chain","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.0f,0.01f,1.0f],right_rotation:[0f,0f,0f,1f]},Rotation:[120f,0f]}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 60
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 24
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
