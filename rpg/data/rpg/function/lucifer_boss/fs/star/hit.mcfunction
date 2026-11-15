# 落地（as/at 落点标记）：圈内 14
tag @e[type=minecraft:vindicator,tag=rpg.lub,limit=1,sort=nearest] add rpg.dm.cast
execute as @e[tag=rpg.unit.f,distance=..3] run function rpg:lucifer_boss/fs/star/dmg
tag @e[type=minecraft:vindicator,tag=rpg.lub] remove rpg.dm.cast
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],text:{text:"",font:"rpg:lucifer_fx"},background:0,billboard:"center",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[5f,5f,5f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 23
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 16
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/shock_ring"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.06f,0f],scale:[0.5f,1f,0.5f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 7
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 9
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/crack"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.04f,0f],scale:[3.5f,1f,3.5f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 6
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 40
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
particle minecraft:flash{color:6280844} ~ ~1 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:2.4} ~ ~0.5 ~ 1.5 0.5 1.5 0.1 40
particle minecraft:end_rod ~ ~0.5 ~ 0.5 0.5 0.5 0.15 20
playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 0.9 1.2
playsound minecraft:block.amethyst_block.break hostile @a[distance=..40] ~ ~ ~ 1.2 0.6
kill @s
