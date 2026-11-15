# as 预警标记 at 标记：原作藤蔓破土（add_lucifer_vine_model.py），并结算附近的人（领主此刻挂着 rpg.dm.cast）。
# 藤蔓自带寿命：到点播消亡动作再清掉，领主没了也照样收场。
function rpg:lucifer_vine/spawn
scoreboard players set @e[type=minecraft:armor_stand,tag=rpg.luv.new,distance=..1] rpg_luv_l 34
tag @e[type=minecraft:armor_stand,tag=rpg.luv.new,distance=..1] remove rpg.luv.new
particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.3 ~ 0.6 0.2 0.6 0.12 24
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.6} ~ ~1 ~ 0.4 1 0.4 0.03 10
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/crack"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.04f,0f],scale:[2.4f,1f,2.4f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 6
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 40
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
execute positioned ~ ~1 ~ as @e[tag=rpg.unit.f,distance=..1.6,tag=!rpg.lu2f.hit] run function rpg:lucifer_fight/vine/hit_once
kill @s
