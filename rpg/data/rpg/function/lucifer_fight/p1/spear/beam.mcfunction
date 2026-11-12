summon minecraft:text_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim","rpg.lu1f.orient"],text:{text:"",font:"rpg:lucifer_fx"},background:0,billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,-0.707107f,0f,0.707107f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[11.25f,1.4f,1f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 29
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 12
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim","rpg.lu1f.orient"],text:{text:"",font:"rpg:lucifer_fx"},background:0,billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0.707107f,0f,0.707107f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[11.25f,1.4f,1f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 29
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 12
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim","rpg.lu1f.orient"],text:{text:"",font:"rpg:lucifer_fx"},background:0,billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[-0.5f,-0.5f,-0.5f,0.5f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[11.25f,1.4f,1f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 29
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 12
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
execute as @e[tag=rpg.lu1f.orient] run tp @s ~ ~ ~ ~ 0
tag @e[tag=rpg.lu1f.orient] remove rpg.lu1f.orient
