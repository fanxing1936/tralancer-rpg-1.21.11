tag @s add rpg.fo.hit
scoreboard players set #stop rpg_fo 1
tag @s add rpg.fo.mk
scoreboard players operation @s rpg_fo_end = #now rpg_fo
scoreboard players add @s rpg_fo_end 160
execute if score #lv rpg_fo matches 1 run scoreboard players set @s rpg_fo_mk 15
execute if score #lv rpg_fo matches 2 run scoreboard players set @s rpg_fo_mk 25
execute if score #lv rpg_fo matches 3 run scoreboard players set @s rpg_fo_mk 35
execute store result score @s rpg_fo_hp run data get entity @s Health 10
effect give @s minecraft:glowing 8 0 true
playsound minecraft:block.anvil.land hostile @a[distance=..16] ~ ~ ~ 0.4 1.8
particle minecraft:enchanted_hit ~ ~1.2 ~ 0.3 0.5 0.3 0.2 20
summon minecraft:text_display ~ ~2.7 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 14
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 18
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:force_vfx/brand","minecraft:custom_model_data":{colors:[16767066]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,-0.95f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.7f,1.7f,1.7f],right_rotation:[0f,0f,0f,1f]},billboard:"center"}
ride @e[tag=rpg.fo.xhnew,limit=1] mount @s
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 160
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
