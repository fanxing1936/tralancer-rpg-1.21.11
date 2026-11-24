execute if score #r rpg_fo matches ..29 run particle minecraft:dust{color:[0.65,0.05,0.12],scale:1.1} ~ ~ ~ 0.02 0.02 0.02 0 1 force
execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[type=#rpg:seal_hostile,tag=!rpg.ally,dx=0,dy=0,dz=0,tag=!rpg.fo.hit,limit=1,sort=nearest] at @s run function rpg:force/ray/drain/hit
execute if score #stop rpg_fo matches 1 run return run scoreboard players set #stop rpg_fo 1
scoreboard players remove #r rpg_fo 1
execute unless block ~ ~ ~ #rpg:force/pass run return run scoreboard players set #stop rpg_fo 1
execute if score #r rpg_fo matches ..0 run return run scoreboard players set #stop rpg_fo 1
scoreboard players operation #rm rpg_fo = #r rpg_fo
scoreboard players operation #rm rpg_fo %= #4 rpg_fo
execute if score #rm rpg_fo matches 0 if score #r rpg_fo matches ..28 run summon minecraft:text_display ~ ~ ~ {Tags:["rpg.fo.mfx","rpg.fo.mfxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#C0303C"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.25f,2.25f,2.25f],right_rotation:[0f,0f,0f,1f]}}
execute if score #rm rpg_fo matches 0 if score #r rpg_fo matches ..28 run scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_life 8
execute if score #rm rpg_fo matches 0 if score #r rpg_fo matches ..28 run scoreboard players set @e[tag=rpg.fo.mfxnew] rpg_fo_kd 10
execute if score #rm rpg_fo matches 0 if score #r rpg_fo matches ..28 run tag @e[tag=rpg.fo.mfxnew] remove rpg.fo.mfxnew
execute positioned ^ ^ ^0.5 run function rpg:force/ray/drain/step
