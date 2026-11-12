summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/feather"}},brightness:{sky:15,block:15},view_range:2f,Rotation:[30f,0f],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.2f,1.2f,1.2f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 19
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 22
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
