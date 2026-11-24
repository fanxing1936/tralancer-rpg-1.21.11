tag @s add rpg.fo.hit
execute if score #lv rpg_fo matches 1 run scoreboard players set #dmg rpg_fo 60
execute if score #lv rpg_fo matches 2 run scoreboard players set #dmg rpg_fo 90
execute if score #lv rpg_fo matches 3 run scoreboard players set #dmg rpg_fo 120
scoreboard players set #hm rpg_fo 15
function rpg:force/hit
particle minecraft:end_rod ~ ~1.2 ~ 0.15 0.3 0.15 0.12 8
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.25f,2.25f,2.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
