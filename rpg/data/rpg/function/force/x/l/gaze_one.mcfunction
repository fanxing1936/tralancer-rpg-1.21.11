tag @s remove rpg.fo.gz
tag @s add rpg.fo.mk
scoreboard players operation @s rpg_fo_end = #now rpg_fo
scoreboard players add @s rpg_fo_end 160
scoreboard players set @s rpg_fo_mk 20
execute store result score @s rpg_fo_hp run data get entity @s Health 10
effect give @s minecraft:glowing 8 0 true
particle minecraft:end_rod ~ ~1.5 ~ 0.2 0.4 0.2 0.05 10
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0.5f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.125f,1.125f,1.125f],right_rotation:[0f,0f,0f,1f]}}
ride @e[tag=rpg.fo.xhnew,limit=1] mount @s
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 160
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
