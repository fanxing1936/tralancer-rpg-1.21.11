playsound minecraft:block.beacon.power_select player @a[distance=..24] ~ ~ ~ 1 1.8
playsound minecraft:entity.allay.ambient_without_item player @a[distance=..24] ~ ~ ~ 1 0.6
tag @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..16,limit=3,sort=nearest] add rpg.fo.gz
execute as @e[tag=rpg.fo.gz] at @s run function rpg:force/x/l/gaze_one
summon minecraft:text_display ^-1.4 ^2.6 ^2.2 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 40
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 16
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:text_display ^ ^3 ^2.6 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 40
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 16
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
summon minecraft:text_display ^1.4 ^2.6 ^2.2 {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 40
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 16
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
