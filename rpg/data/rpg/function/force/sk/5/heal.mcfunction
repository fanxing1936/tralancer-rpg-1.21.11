execute if score #lv rpg_fo matches 1 run effect give @s minecraft:instant_health 1 0 true
execute if score #lv rpg_fo matches 2 run effect give @s minecraft:instant_health 1 0 true
execute if score #lv rpg_fo matches 3 run effect give @s minecraft:instant_health 1 1 true
execute if score #lv rpg_fo matches 2 run effect give @s minecraft:regeneration 3 1 true
particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 6
particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.04 20
summon minecraft:text_display ~ ~2.3 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.375f,1.375f,1.375f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 24
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 23
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
summon minecraft:text_display ~0.4 ~1.6 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 16
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
