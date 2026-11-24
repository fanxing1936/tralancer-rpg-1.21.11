summon minecraft:marker ~ ~ ~ {Tags:["rpg.fo.zone","rpg.fo.znew"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_k 16
scoreboard players operation @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_lv = #lv rpg_fo
scoreboard players operation @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end = #now rpg_fo
scoreboard players add @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end 80
tag @e[type=minecraft:marker,tag=rpg.fo.znew] remove rpg.fo.znew
playsound minecraft:block.end_portal.spawn hostile @a[distance=..24] ~ ~ ~ 0.4 1.6
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/swirl","minecraft:custom_model_data":{colors:[3871832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 80
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 1
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagram","minecraft:custom_model_data":{colors:[10647230]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.5f,1f,7.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 80
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 2
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:force_vfx/maw_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 80
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 25
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:item_display ~ ~0.12 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:force_vfx/spiral","minecraft:custom_model_data":{colors:[10647230]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.6f,1f,3.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 80
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 1
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
