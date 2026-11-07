# 地面黑色拖痕（at 地面）。
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.puddle"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/puddle"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.03f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 44
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
particle dust{color:[0.835f,0.588f,0.949f],scale:1.0} ~ ~0.2 ~ 1 0 1 0 12 force
