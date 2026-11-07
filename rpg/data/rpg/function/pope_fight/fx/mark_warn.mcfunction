# 落点预警（at 地面）：外圈先亮，内盘长满时弹体落地。
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.mark"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/mark_ring"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 30
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.fill"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/mark_fill"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.04f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 30
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
particle dust{color:[0.835f,0.588f,0.949f],scale:1.0} ~ ~0.2 ~ 0.6 0 0.6 0 6 force
