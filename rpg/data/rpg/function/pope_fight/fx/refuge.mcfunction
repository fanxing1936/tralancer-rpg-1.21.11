# 圣所（at 地面）：一根细光柱标出位置，老远就能看见。
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.refuge"],text:{text:"",font:"rpg:pope_fx"},background:0,billboard:"vertical",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,18f,0f],scale:[0.125f,11.25f,1f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 110
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.refdisc"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:pope_fx/seal_inner"}},brightness:{sky:15,block:15},view_range:2f,teleport_duration:1,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.1f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 110
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
