data modify storage rpg:demon uuid set from entity @s UUID
function rpg:taint/ult1_fangs with storage rpg:demon
tag @s add rpg.dm.cast
execute as @e[tag=rpg.unit.f,distance=..10] run function rpg:taint/ult1_hit
tag @s remove rpg.dm.cast
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:3} ~ ~1 ~ 5 1 5 0.04 72
particle end_rod ~ ~2 ~ 2.5 1.5 2.5 0.05 60
playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..32] ~ ~ ~ 1.2 0.55
playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..40] ~ ~ ~ 0.8 0.7
execute positioned ~ ~2 ~ run function rpg:lucifer_fight/p1/ult/burst
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/shock_ring"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.06f,0f],scale:[0.5f,1f,0.5f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 22
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 10
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
