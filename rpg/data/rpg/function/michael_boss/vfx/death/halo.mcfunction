# 光环降下（at 他）：头顶的光环长出来，脚下的炽天使圣印慢慢转，一圈白光向外推
summon minecraft:text_display ~ ~3.3 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.625f,0.625f,0.625f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 120
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 50
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/seal_seraph","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7f,1f,7f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 124
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 16
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/glow_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 124
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_h","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 19
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
particle minecraft:end_rod ~0.40 ~0.30 ~0.00 1.000 0.000 0.000 0.12 0 force
particle minecraft:end_rod ~0.37 ~0.30 ~0.15 0.924 0.000 0.383 0.12 0 force
particle minecraft:end_rod ~0.28 ~0.30 ~0.28 0.707 0.000 0.707 0.12 0 force
particle minecraft:end_rod ~0.15 ~0.30 ~0.37 0.383 0.000 0.924 0.12 0 force
particle minecraft:end_rod ~0.00 ~0.30 ~0.40 0.000 0.000 1.000 0.12 0 force
particle minecraft:end_rod ~-0.15 ~0.30 ~0.37 -0.383 0.000 0.924 0.12 0 force
particle minecraft:end_rod ~-0.28 ~0.30 ~0.28 -0.707 0.000 0.707 0.12 0 force
particle minecraft:end_rod ~-0.37 ~0.30 ~0.15 -0.924 0.000 0.383 0.12 0 force
particle minecraft:end_rod ~-0.40 ~0.30 ~0.00 -1.000 0.000 0.000 0.12 0 force
particle minecraft:end_rod ~-0.37 ~0.30 ~-0.15 -0.924 0.000 -0.383 0.12 0 force
particle minecraft:end_rod ~-0.28 ~0.30 ~-0.28 -0.707 0.000 -0.707 0.12 0 force
particle minecraft:end_rod ~-0.15 ~0.30 ~-0.37 -0.383 0.000 -0.924 0.12 0 force
particle minecraft:end_rod ~-0.00 ~0.30 ~-0.40 -0.000 0.000 -1.000 0.12 0 force
particle minecraft:end_rod ~0.15 ~0.30 ~-0.37 0.383 0.000 -0.924 0.12 0 force
particle minecraft:end_rod ~0.28 ~0.30 ~-0.28 0.707 0.000 -0.707 0.12 0 force
particle minecraft:end_rod ~0.37 ~0.30 ~-0.15 0.924 0.000 -0.383 0.12 0 force
playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 1.2 0.6
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..48] ~ ~ ~ 1 0.5
