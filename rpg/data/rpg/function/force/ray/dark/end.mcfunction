particle minecraft:soul_fire_flame ~ ~0.5 ~ 1.2 0.6 1.2 0.05 60
particle minecraft:large_smoke ~ ~0.5 ~ 1 0.4 1 0.02 20
playsound minecraft:entity.blaze.shoot hostile @a[distance=..16] ~ ~ ~ 1 0.6
execute if score #lv rpg_fo matches 1 run scoreboard players set #dmg rpg_fo 50
execute if score #lv rpg_fo matches 2 run scoreboard players set #dmg rpg_fo 70
execute if score #lv rpg_fo matches 3 run scoreboard players set #dmg rpg_fo 90
scoreboard players set #hm rpg_fo 10
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..2.5] at @s run function rpg:force/sk/3/one
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#5B2A86"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
function rpg:force/ground/dark/go
