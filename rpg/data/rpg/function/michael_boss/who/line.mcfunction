# 一条骨刺线（as/at 他，朝这条线）：沿线判定、几节骨刺、一路碎骨
scoreboard players set #d rpg_mk 20
function rpg:michael_boss/line/thin
execute positioned ^ ^ ^5 run particle minecraft:block{block_state:"minecraft:bone_block"} ~ ~0.5 ~ 0.2 0.4 0.2 0 6
execute positioned ^ ^ ^5 run particle minecraft:dust_color_transition{from_color:[1.0,0.5,0.32],to_color:[1.0,0.2,0.0],scale:1.1} ~ ~0.7 ~ 0.15 0.5 0.15 0 3
execute positioned ^ ^ ^5 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[15918808]}}},brightness:{sky:15,block:15},teleport_duration:0,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.05f,0.2f,0.05f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^ ^ ^5 run scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 12
execute positioned ^ ^ ^5 run scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 23
execute positioned ^ ^ ^5 run tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
execute positioned ^ ^ ^11 run particle minecraft:block{block_state:"minecraft:bone_block"} ~ ~0.5 ~ 0.2 0.4 0.2 0 6
execute positioned ^ ^ ^11 run particle minecraft:dust_color_transition{from_color:[1.0,0.5,0.32],to_color:[1.0,0.2,0.0],scale:1.1} ~ ~0.7 ~ 0.15 0.5 0.15 0 3
execute positioned ^ ^ ^11 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[15918808]}}},brightness:{sky:15,block:15},teleport_duration:0,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.05f,0.2f,0.05f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^ ^ ^11 run scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 12
execute positioned ^ ^ ^11 run scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 23
execute positioned ^ ^ ^11 run tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
execute positioned ^ ^ ^17 run particle minecraft:block{block_state:"minecraft:bone_block"} ~ ~0.5 ~ 0.2 0.4 0.2 0 6
execute positioned ^ ^ ^17 run particle minecraft:dust_color_transition{from_color:[1.0,0.5,0.32],to_color:[1.0,0.2,0.0],scale:1.1} ~ ~0.7 ~ 0.15 0.5 0.15 0 3
execute positioned ^ ^ ^17 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[15918808]}}},brightness:{sky:15,block:15},teleport_duration:0,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.05f,0.2f,0.05f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^ ^ ^17 run scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 12
execute positioned ^ ^ ^17 run scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 23
execute positioned ^ ^ ^17 run tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
execute positioned ^ ^ ^24 run particle minecraft:block{block_state:"minecraft:bone_block"} ~ ~0.5 ~ 0.2 0.4 0.2 0 6
execute positioned ^ ^ ^24 run particle minecraft:dust_color_transition{from_color:[1.0,0.5,0.32],to_color:[1.0,0.2,0.0],scale:1.1} ~ ~0.7 ~ 0.15 0.5 0.15 0 3
execute positioned ^ ^ ^24 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[15918808]}}},brightness:{sky:15,block:15},teleport_duration:0,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.05f,0.2f,0.05f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ^ ^ ^24 run scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 12
execute positioned ^ ^ ^24 run scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 23
execute positioned ^ ^ ^24 run tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
particle minecraft:block{block_state:"minecraft:bone_block"} ^ ^0.4 ^3 0.3 0.3 0.3 0 4
particle minecraft:block{block_state:"minecraft:bone_block"} ^ ^0.4 ^6 0.3 0.3 0.3 0 4
particle minecraft:block{block_state:"minecraft:bone_block"} ^ ^0.4 ^9 0.3 0.3 0.3 0 4
particle minecraft:block{block_state:"minecraft:bone_block"} ^ ^0.4 ^12 0.3 0.3 0.3 0 4
particle minecraft:block{block_state:"minecraft:bone_block"} ^ ^0.4 ^15 0.3 0.3 0.3 0 4
particle minecraft:block{block_state:"minecraft:bone_block"} ^ ^0.4 ^18 0.3 0.3 0.3 0 4
particle minecraft:block{block_state:"minecraft:bone_block"} ^ ^0.4 ^21 0.3 0.3 0.3 0 4
particle minecraft:block{block_state:"minecraft:bone_block"} ^ ^0.4 ^24 0.3 0.3 0.3 0 4
particle minecraft:block{block_state:"minecraft:bone_block"} ^ ^0.4 ^27 0.3 0.3 0.3 0 4
