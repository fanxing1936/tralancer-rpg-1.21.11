scoreboard players operation @s rpg_fo_fe = #now rpg_fo
scoreboard players add @s rpg_fo_fe 100
playsound minecraft:entity.bee.loop_aggressive player @a[distance=..24] ~ ~ ~ 1 0.5
particle minecraft:dust{color:[0.35,0.42,0.12],scale:0.6} ~ ~1.2 ~ 4 1 4 0 200
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.xm","rpg.fo.xmnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagram","minecraft:custom_model_data":{colors:[11917655]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[16f,1f,16f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_life 100
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_kd 1
tag @e[tag=rpg.fo.xmnew] remove rpg.fo.xmnew
