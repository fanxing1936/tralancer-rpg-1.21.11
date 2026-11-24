playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 1 0.8
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 30
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.75f,2.75f,2.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 12
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 22
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
execute if score #lv rpg_fo matches 1 run scoreboard players set #r rpg_fo 16
execute if score #lv rpg_fo matches 2 run scoreboard players set #r rpg_fo 20
execute if score #lv rpg_fo matches 3 run scoreboard players set #r rpg_fo 24
execute rotated ~ 0 run function rpg:force/blink/step_m
effect give @s minecraft:invisibility 1 0 true
execute at @s run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 30
execute at @s run summon minecraft:text_display ^ ^1 ^-1 {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.75f,2.75f,2.75f],right_rotation:[0f,0f,0f,1f]}}
execute at @s run scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 12
execute at @s run scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 22
execute at @s run tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
