# 原作藤臂（add_lucifer_props.py 的 spike）从地下升起，约 3.7 格。
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_props/spike"}},brightness:{sky:15,block:15},view_range:2f,Rotation:[37f,0f],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,-3.9f,0f],scale:[7.19492f,7.19492f,7.19492f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 10
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 34
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.3 ~ 0.6 0.2 0.6 0.12 16
execute positioned ~ ~1 ~ as @a[distance=..1.8,tag=!rpg.lu2f.hit,gamemode=!spectator,gamemode=!creative] run function rpg:lucifer_fight/ult/hit_once
kill @s
