# 全场圣印（at 地面）：半透明，要看得见脚下和圣所。
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.dooms","rpg.pf.cw"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/doom_outer"}},brightness:{sky:15,block:15},view_range:2f,teleport_duration:1,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.07f,0f],scale:[0.01f,1f,0.01f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.dooms","rpg.pf.ccw"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/doom_inner"}},brightness:{sky:15,block:15},view_range:2f,teleport_duration:1,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.07f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 122
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
