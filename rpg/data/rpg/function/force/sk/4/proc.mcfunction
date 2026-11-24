execute if score #lv rpg_fo matches 1 run scoreboard players set #dmg rpg_fo 20
execute if score #lv rpg_fo matches 2 run scoreboard players set #dmg rpg_fo 30
execute if score #lv rpg_fo matches 3 run scoreboard players set #dmg rpg_fo 40
scoreboard players set #hm rpg_fo 20
function rpg:force/hit
data merge entity @s {Fire:60s}
particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.04 14
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 12
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 20
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
