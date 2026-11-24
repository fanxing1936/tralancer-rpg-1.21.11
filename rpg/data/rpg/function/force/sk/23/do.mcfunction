execute if score #lv rpg_fo matches 1 run summon minecraft:iron_golem ^ ^ ^2 {Tags:["rpg.fo.pup","rpg.fo.timed","rpg.fo.pnew","rpg.ally"],CustomName:{text:"傀儡",color:"#A276BE",italic:false},CustomNameVisible:1b,PlayerCreated:1b,DeathLootTable:"minecraft:empty",Health:40f,attributes:[{id:"minecraft:max_health",base:40d}]}
execute if score #lv rpg_fo matches 2 run summon minecraft:iron_golem ^ ^ ^2 {Tags:["rpg.fo.pup","rpg.fo.timed","rpg.fo.pnew","rpg.ally"],CustomName:{text:"傀儡",color:"#A276BE",italic:false},CustomNameVisible:1b,PlayerCreated:1b,DeathLootTable:"minecraft:empty",Health:60f,attributes:[{id:"minecraft:max_health",base:60d}]}
execute if score #lv rpg_fo matches 3 run summon minecraft:iron_golem ^ ^ ^2 {Tags:["rpg.fo.pup","rpg.fo.timed","rpg.fo.pnew","rpg.ally"],CustomName:{text:"傀儡",color:"#A276BE",italic:false},CustomNameVisible:1b,PlayerCreated:1b,DeathLootTable:"minecraft:empty",Health:80f,attributes:[{id:"minecraft:max_health",base:80d}]}
scoreboard players operation @e[tag=rpg.fo.pnew] rpg_fo_end = #now rpg_fo
scoreboard players add @e[tag=rpg.fo.pnew] rpg_fo_end 400
execute as @e[tag=rpg.fo.pnew] at @s run particle minecraft:soul ~ ~1 ~ 0.5 1 0.5 0.03 40
tag @e[tag=rpg.fo.pnew] remove rpg.fo.pnew
playsound minecraft:entity.zombie_villager.cure player @a[distance=..16] ~ ~ ~ 0.6 0.6
execute positioned ^ ^ ^2 run summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagon","minecraft:custom_model_data":{colors:[10647230]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 40
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
execute positioned ^ ^ ^2 run summon minecraft:text_display ~ ~ ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#A276BE"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,2.1f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,0.01f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 8
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
