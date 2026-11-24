playsound minecraft:block.beacon.activate player @a[distance=..32] ~ ~ ~ 1.5 1.3
playsound minecraft:block.bell.resonate player @a[distance=..32] ~ ~ ~ 1 1.6
playsound minecraft:ui.toast.challenge_complete player @a[distance=..32] ~ ~ ~ 0.6 1.6
particle minecraft:end_rod ~ ~1 ~ 6 1.5 6 0.05 200
scoreboard players set #dmg rpg_fo 160
scoreboard players set #hm rpg_fo 15
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..12] at @s run function rpg:force/x/f/hal_one
effect give @a[distance=..12,gamemode=!spectator] minecraft:instant_health 1 3 true
effect give @a[distance=..12,gamemode=!spectator] minecraft:regeneration 6 1 true
execute as @a[distance=..12,gamemode=!spectator] at @s run function rpg:force/x/f/hal_ally
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[26f,1f,26f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 23
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:text_display ^ ^1.6 ^-1.8 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 14
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 19
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:text_display ^ ^2.4 ^4.5 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
