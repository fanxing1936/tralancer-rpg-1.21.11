# 地面圣印（at 落点）。
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.seal","rpg.pf.big","rpg.pf.cw"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/seal_outer"}},brightness:{sky:15,block:15},view_range:2f,teleport_duration:1,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[0.01f,1f,0.01f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.seal","rpg.pf.big","rpg.pf.ccw"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/seal_inner"}},brightness:{sky:15,block:15},view_range:2f,teleport_duration:1,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 40
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
