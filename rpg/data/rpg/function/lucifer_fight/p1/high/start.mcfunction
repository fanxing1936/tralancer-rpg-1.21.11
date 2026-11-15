execute if entity @s[tag=rpg.advent] at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/1_3
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m3
execute positioned ~ ~3.1 ~ run function rpg:lucifer_fight/p1/fx/crown
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/crown_ring"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 15
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 26
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
