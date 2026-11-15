# 落点（at 玩家脚下）：淡绿的预警圈，半径 3 格
summon minecraft:marker ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lub.star"]}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 11
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 32
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/fall_mark"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[6f,1f,6f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 11
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 32
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/crown_ring"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.08f,0f],scale:[6.6f,1f,6.6f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 11
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 32
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.6} ~ ~0.2 ~ 2 0.05 2 0 20
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..24] ~ ~ ~ 1.2 1.4
