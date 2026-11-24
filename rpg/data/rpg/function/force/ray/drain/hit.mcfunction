tag @s add rpg.fo.hit
scoreboard players set #stop rpg_fo 1
execute if score #lv rpg_fo matches 1 run scoreboard players set #dmg rpg_fo 40
execute if score #lv rpg_fo matches 2 run scoreboard players set #dmg rpg_fo 60
execute if score #lv rpg_fo matches 3 run scoreboard players set #dmg rpg_fo 80
scoreboard players set #hm rpg_fo 10
function rpg:force/hit
particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.3} ~ ~1 ~ 0.3 0.5 0.3 0 20
execute as @a[tag=rpg.fo.me,limit=1] at @s run function rpg:force/sk/18/heal
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#8B0A1E"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
