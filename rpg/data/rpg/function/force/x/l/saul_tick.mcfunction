scoreboard players operation #q rpg_fo = #now rpg_fo
scoreboard players operation #q rpg_fo %= #5 rpg_fo
execute unless score #q rpg_fo matches 0 run return 0
scoreboard players remove @s rpg_fo_tk 1
playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.3
particle minecraft:sweep_attack ^ ^1.1 ^1.8 0.6 0.3 0.6 0 3
scoreboard players set #dmg rpg_fo 30
scoreboard players set #hm rpg_fo 10
tag @s add rpg.fo.me
execute positioned ^ ^ ^2 as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..2.8] at @s run function rpg:force/hit
tag @s remove rpg.fo.me
execute if score @s rpg_fo_tk matches 0..1 run playsound minecraft:item.trident.return player @a[distance=..16] ~ ~ ~ 1 1.6
execute if score @s rpg_fo_tk matches 0 run summon minecraft:text_display ^-0.5 ^1.1 ^3.4 {Tags:["rpg.fo.xm","rpg.fo.xmnew"],text:{text:"",font:"rpg:usurper_fx",color:"#C0303C"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rpg_fo_tk matches 1 run summon minecraft:text_display ^0.5 ^1.1 ^3.4 {Tags:["rpg.fo.xm","rpg.fo.xmnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E6DFCF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rpg_fo_tk matches 2 run summon minecraft:text_display ^-0.5 ^1.1 ^3.4 {Tags:["rpg.fo.xm","rpg.fo.xmnew"],text:{text:"",font:"rpg:usurper_fx",color:"#C0303C"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rpg_fo_tk matches 3 run summon minecraft:text_display ^0.5 ^1.1 ^3.4 {Tags:["rpg.fo.xm","rpg.fo.xmnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E6DFCF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rpg_fo_tk matches 4 run summon minecraft:text_display ^-0.5 ^1.1 ^3.4 {Tags:["rpg.fo.xm","rpg.fo.xmnew"],text:{text:"",font:"rpg:usurper_fx",color:"#C0303C"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rpg_fo_tk matches 5 run summon minecraft:text_display ^0.5 ^1.1 ^3.4 {Tags:["rpg.fo.xm","rpg.fo.xmnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E6DFCF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rpg_fo_tk matches 6 run summon minecraft:text_display ^-0.5 ^1.1 ^3.4 {Tags:["rpg.fo.xm","rpg.fo.xmnew"],text:{text:"",font:"rpg:usurper_fx",color:"#C0303C"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rpg_fo_tk matches 7 run summon minecraft:text_display ^0.5 ^1.1 ^3.4 {Tags:["rpg.fo.xm","rpg.fo.xmnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E6DFCF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_life 8
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_kd 13
tag @e[tag=rpg.fo.xmnew] remove rpg.fo.xmnew
