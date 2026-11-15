# 一颗晨星从 7 格高处落下（feather 的下落插值：20 刻落 6 格）
execute positioned ~ ~7 ~ run summon minecraft:text_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],text:{text:"",font:"rpg:lucifer_fx"},background:0,billboard:"center",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[6.5f,6.5f,6.5f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 19
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 22
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
particle minecraft:end_rod ~ ~7 ~ 0.2 0.2 0.2 0.05 12 force
playsound minecraft:entity.firework_rocket.launch hostile @a[distance=..32] ~ ~ ~ 1 0.6
