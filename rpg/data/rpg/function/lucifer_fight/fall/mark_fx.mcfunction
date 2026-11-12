summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim","rpg.lu2f.fm"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/fall_mark"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 5
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 70
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
