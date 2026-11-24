particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:flame ~ ~0.5 ~ 2.5 0.5 2.5 0.1 120 force
particle minecraft:lava ~ ~0.5 ~ 2 0.2 2 0 30
playsound minecraft:entity.generic.explode player @a[distance=..48] ~ ~ ~ 2 0.7
scoreboard players set #dmg rpg_fo 140
scoreboard players set #hm rpg_fo 10
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..5] at @s run function rpg:force/x/l/star_one
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shock_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[12f,1f,12f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 22
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/scorch","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,1f,8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 100
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
