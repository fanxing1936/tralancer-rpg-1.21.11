# 扑击落点（at 瞄准点）
kill @e[tag=rpg.mkb.burnto,predicate=!rpg:in_prologue]
summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.burnto"]}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 20
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 17
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/glow_f","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 17
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.07 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/seal_seraph","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5.5f,1f,5.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 17
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 15
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
playsound minecraft:block.note_block.bell hostile @a[distance=..48] ~ ~ ~ 1.2 1.8
