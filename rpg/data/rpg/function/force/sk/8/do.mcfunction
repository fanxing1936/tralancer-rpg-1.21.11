scoreboard players operation @s rpg_fo_mt = #now rpg_fo
scoreboard players add @s rpg_fo_mt 200
scoreboard players operation @s rpg_fo_mlv = #lv rpg_fo
scoreboard players set @a[distance=..8] rpg_fo_dr 0
playsound minecraft:block.bell.use player @a[distance=..16] ~ ~ ~ 1 0.7
particle minecraft:end_rod ~ ~1 ~ 4 0.5 4 0 60
summon minecraft:text_display ^ ^1.5 ^-0.7 {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 14
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 19
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[16f,1f,16f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 200
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
