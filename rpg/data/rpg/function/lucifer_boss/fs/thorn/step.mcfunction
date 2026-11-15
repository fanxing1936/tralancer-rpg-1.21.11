# 荆棘线前进一步（as/at 标记）：落在地面上，钻出一根原作的藤刺；碰到的人挨一下
execute positioned ^ ^ ^1.2 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~ ~ 0
execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_props/spike"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,-3.9f,0f],scale:[3.95721f,3.95721f,3.95721f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 10
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 34
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
execute at @s run particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.2 ~ 0.4 0.1 0.4 0.1 8
tag @e[type=minecraft:vindicator,tag=rpg.lub,limit=1,sort=nearest] add rpg.dm.cast
execute at @s as @e[tag=rpg.unit.f,distance=..1.4,tag=!rpg.lub.thit] run function rpg:lucifer_boss/fs/thorn/dmg
tag @e[type=minecraft:vindicator,tag=rpg.lub] remove rpg.dm.cast
execute at @s run playsound minecraft:block.big_dripleaf.break hostile @a[distance=..20] ~ ~ ~ 0.5 0.6
