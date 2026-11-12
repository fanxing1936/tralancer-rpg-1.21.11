execute store result score #s rpg_l2_v run random value 1..5
execute if score #s rpg_l2_v matches 1 run function rpg:minion/summon/lucifer/bael
execute if score #s rpg_l2_v matches 2 run function rpg:minion/summon/lucifer/agares
execute if score #s rpg_l2_v matches 3 run function rpg:minion/summon/lucifer/vassago
execute if score #s rpg_l2_v matches 4 run function rpg:minion/summon/lucifer/samigina
execute if score #s rpg_l2_v matches 5 run function rpg:minion/summon/lucifer/marbas
tag @e[tag=rpg.demon.minion,tag=!rpg.lu2f.minion,distance=..2,limit=1,sort=nearest] add rpg.lu2f.new_minion
scoreboard players operation @e[tag=rpg.lu2f.new_minion] rpg_l2_id = #id rpg_l2_id
tag @e[tag=rpg.lu2f.new_minion] add rpg.lu2f.minion
tag @e[tag=rpg.lu2f.new_minion] remove rpg.lu2f.new_minion
particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.4 ~ 0.6 0.3 0.6 0.1 30
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/vine_mark"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 4
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 20
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
