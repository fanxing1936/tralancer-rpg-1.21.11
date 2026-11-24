summon minecraft:marker ~ ~ ~ {Tags:["rpg.fo.zone","rpg.fo.znew"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_k 6
scoreboard players operation @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_lv = #lv rpg_fo
scoreboard players operation @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end = #now rpg_fo
scoreboard players add @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end 160
tag @e[type=minecraft:marker,tag=rpg.fo.znew] remove rpg.fo.znew
playsound minecraft:block.beacon.activate player @a[distance=..16] ~ ~ ~ 1 1.5
particle minecraft:end_rod ~ ~1 ~ 1.5 1 1.5 0.02 60
execute align y run summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/seal_seraph","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,1f,8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 160
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 1
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.6f,1f,8.6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 160
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
