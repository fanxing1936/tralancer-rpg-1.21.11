playsound minecraft:entity.elder_guardian.curse player @a[distance=..24] ~ ~ ~ 0.6 1.2
playsound minecraft:ambient.underwater.enter player @a[distance=..24] ~ ~ ~ 1 0.6
particle minecraft:nautilus ~ ~1 ~ 5 1 5 0.5 160
particle minecraft:bubble_pop ~ ~0.5 ~ 5 0.3 5 0.05 80
scoreboard players set #dmg rpg_fo 60
scoreboard players set #hm rpg_fo 10
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,tag=!rpg.pope,tag=!rpg.mkb,tag=!rpg.jqb,tag=!rpg.lub,tag=!rpg.slb,tag=!rpg.usb,distance=1.8..10] at @s run function rpg:force/x/f/lord2_pull
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..10] at @s run function rpg:force/hit
effect give @e[type=#rpg:seal_hostile,tag=!rpg.ally,tag=!rpg.pope,tag=!rpg.mkb,tag=!rpg.jqb,tag=!rpg.lub,tag=!rpg.slb,tag=!rpg.usb,distance=..10] minecraft:slowness 3 9 true
effect give @e[type=#rpg:seal_hostile,tag=!rpg.ally,tag=!rpg.pope,tag=!rpg.mkb,tag=!rpg.jqb,tag=!rpg.lub,tag=!rpg.slb,tag=!rpg.usb,distance=..10] minecraft:jump_boost 3 250 true
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.xm","rpg.fo.xmnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/swirl","minecraft:custom_model_data":{colors:[5218032]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[14f,1f,14f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_life 40
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_kd 2
tag @e[tag=rpg.fo.xmnew] remove rpg.fo.xmnew
