# 虚空坍缩（at 地面）。
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.pool"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/puddle"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 108
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.edge"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/mark_ring"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.09f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 108
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.gyre"],text:{text:"",font:"rpg:pope_fx"},background:0,billboard:"vertical",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,7.5f,0f],scale:[0.0833f,6.6667f,1f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 108
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
