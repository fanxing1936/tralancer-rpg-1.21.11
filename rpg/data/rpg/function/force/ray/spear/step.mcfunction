execute if score #r rpg_fo matches ..37 run particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1 force
execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[type=#rpg:seal_hostile,tag=!rpg.ally,dx=0,dy=0,dz=0,tag=!rpg.fo.hit] at @s run function rpg:force/ray/spear/hit
execute if score #stop rpg_fo matches 1 run return run scoreboard players set #stop rpg_fo 1
scoreboard players remove #r rpg_fo 1
execute unless block ~ ~ ~ #rpg:force/pass run return run scoreboard players set #stop rpg_fo 1
execute if score #r rpg_fo matches ..0 run return run scoreboard players set #stop rpg_fo 1
scoreboard players operation #rm rpg_fo = #r rpg_fo
scoreboard players operation #rm rpg_fo %= #4 rpg_fo
execute if score #rm rpg_fo matches 0 if score #r rpg_fo matches ..36 run summon minecraft:text_display ~ ~ ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
execute if score #rm rpg_fo matches 0 if score #r rpg_fo matches ..36 run scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 8
execute if score #rm rpg_fo matches 0 if score #r rpg_fo matches ..36 run scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 15
execute if score #rm rpg_fo matches 0 if score #r rpg_fo matches ..36 run tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
execute positioned ^ ^ ^0.5 run function rpg:force/ray/spear/step
