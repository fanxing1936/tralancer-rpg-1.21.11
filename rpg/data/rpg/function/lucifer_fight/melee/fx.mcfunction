summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/crack"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.04f,0f],scale:[3.5f,1f,3.5f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 6
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 40
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/shock_ring"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.06f,0f],scale:[0.5f,1f,0.5f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 7
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 9
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
