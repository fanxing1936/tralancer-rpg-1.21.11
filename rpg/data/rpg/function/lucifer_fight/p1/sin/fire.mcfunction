data modify storage rpg:demon uuid set from entity @s UUID
function rpg:taint/sk1_line with storage rpg:demon
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.6} ~ ~1 ~ 0.6 0.8 0.6 0.05 30
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/crack"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.04f,0f],scale:[2.4f,1f,2.4f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 6
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 40
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
