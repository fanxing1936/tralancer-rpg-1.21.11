# 圣血祭的光线（at 杖头）。
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.line"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/line"}},brightness:{sky:15,block:15},view_range:2f,teleport_duration:2,interpolation_duration:5,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.07f,0.07f,0.01f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 34
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
