# 一名罪仆从根须里爬出来（at 落点）：路西法柱下五名随机一名，穿苔藓骷髅（add_lord_servants.py）
execute store result score #n rpg_lub if entity @e[tag=rpg.lub.unit]
execute if score #n rpg_lub matches 4.. run return 0
execute store result score #s rpg_lub run random value 1..5
execute if score #s rpg_lub matches 1 run function rpg:minion/summon/lucifer/bael
execute if score #s rpg_lub matches 2 run function rpg:minion/summon/lucifer/agares
execute if score #s rpg_lub matches 3 run function rpg:minion/summon/lucifer/vassago
execute if score #s rpg_lub matches 4 run function rpg:minion/summon/lucifer/samigina
execute if score #s rpg_lub matches 5 run function rpg:minion/summon/lucifer/marbas
tag @e[tag=rpg.demon.minion,tag=!rpg.lub.unit,distance=..2,limit=1,sort=nearest] add rpg.lub.unit
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/vine_mark"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 3
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 24
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],text:{text:"",font:"rpg:lucifer_fx"},background:0,billboard:"center",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.5f,2.5f,2.5f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 23
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 16
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.4 ~ 0.6 0.3 0.6 0.1 30
particle block{block_state:{Name:"minecraft:moss_block"}} ~ ~0.6 ~ 0.4 0.4 0.4 0.1 20
playsound minecraft:entity.skeleton.ambient hostile @a[distance=..24] ~ ~ ~ 1 0.6
