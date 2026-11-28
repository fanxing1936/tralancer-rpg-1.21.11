# 两根肋骨从手里落下，插在他身前（as/at 他）；手里的换成空模型
execute on passengers if entity @s[tag=rpg.mkm.p.rib] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute on passengers if entity @s[tag=rpg.mkm.p.rib_attack] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute positioned ^0.5 ^ ^1 run summon minecraft:item_display ~ ~0.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.bones"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_boss/rib"}},item_display:"none",brightness:{sky:15,block:12},view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0.9238795f,0.3826834f],scale:[1.4f,1.4f,1.4f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^-0.5 ^ ^1.2 run summon minecraft:item_display ~ ~0.6 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.bones"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_boss/rib"}},item_display:"none",brightness:{sky:15,block:12},view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0.9238795f,0.3826834f],scale:[1.4f,1.4f,1.4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 30000
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
playsound minecraft:block.bone_block.place hostile @a[distance=..24] ~ ~ ~ 1 0.8
particle minecraft:block{block_state:"minecraft:bone_block"} ^ ^0.3 ^1 0.3 0.1 0.3 0 10
