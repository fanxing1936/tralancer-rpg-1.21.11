tag @s add rpg.dm.cast
execute as @e[tag=rpg.unit.f,distance=..6] at @s run function rpg:taint/sk1e_reject
tag @s remove rpg.dm.cast
playsound minecraft:block.beacon.deactivate hostile @a[distance=..32] ~ ~ ~ 1 0.55
particle end_rod ~ ~1.5 ~ 2.5 1 2.5 0.08 30
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.6} ~ ~1 ~ 2.5 0.6 2.5 0.05 30
execute positioned ^ ^1.4 ^1.5 run function rpg:lucifer_fight/p1/fx/slash
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/shock_ring"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.06f,0f],scale:[0.5f,1f,0.5f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 20
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 9
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
