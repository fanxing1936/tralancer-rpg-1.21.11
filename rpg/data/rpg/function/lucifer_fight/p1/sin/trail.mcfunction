summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu1f.orient"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/serpent_trail"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[1.6f,1f,9f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 13
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 18
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
execute as @e[tag=rpg.lu1f.orient] run tp @s ~ ~ ~ ~ 0
tag @e[tag=rpg.lu1f.orient] remove rpg.lu1f.orient
