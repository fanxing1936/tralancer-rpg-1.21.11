execute if score @s rpg_fo_end > #now rpg_fo run return run particle minecraft:wax_on ~ ~1 ~ 0.4 0.7 0.4 0 2
tag @s remove rpg.fo.gd
execute if score @s rpg_fo_ai matches 0 run data merge entity @s {NoAI:0b}
particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~1 ~ 1.2 0.8 1.2 0 80
playsound minecraft:block.glass.break hostile @a[distance=..16] ~ ~ ~ 1 0.6
playsound minecraft:block.chain.break hostile @a[distance=..16] ~ ~ ~ 1 0.6
scoreboard players set #dmg rpg_fo 100
scoreboard players set #hm rpg_fo 10
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..3] at @s run function rpg:force/hit
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.xm","rpg.fo.xmnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagon","minecraft:custom_model_data":{colors:[15114812]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_life 20
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.xmnew] remove rpg.fo.xmnew
