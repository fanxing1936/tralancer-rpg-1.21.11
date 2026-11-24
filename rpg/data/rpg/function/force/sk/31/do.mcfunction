playsound minecraft:block.bell.use player @a[distance=..24] ~ ~ ~ 1 0.8
playsound minecraft:block.beacon.power_select player @a[distance=..24] ~ ~ ~ 0.8 1.2
effect give @a[distance=..8,gamemode=!spectator] minecraft:resistance 10 0 true
execute as @a[distance=..8,gamemode=!spectator] run scoreboard players operation @s rpg_fo_cr = #now rpg_fo
scoreboard players add @a[distance=..8,gamemode=!spectator] rpg_fo_cr 200
execute as @a[distance=..8,gamemode=!spectator] at @s run function rpg:force/x/f/hal_ally
particle minecraft:end_rod ~ ~0.2 ~ 4 0.1 4 0 60
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[16f,1f,16f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 40
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 0
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/seal_seraph","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 40
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 1
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
