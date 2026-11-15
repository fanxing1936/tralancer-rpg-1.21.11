summon minecraft:marker ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.stake","rpg.jqb.ult"]}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_id 3
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 127
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.stakev","rpg.jqb.ult"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/pillar","minecraft:custom_model_data":{colors:[3811872]}}},brightness:{sky:15,block:15},teleport_duration:15,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,-2.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,7.4f,8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 150
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 14
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:flame ~ ~1 ~ 0.3 1 0.3 0.02 12
particle minecraft:large_smoke ~ ~0.3 ~ 0.6 0.1 0.6 0.03 8
playsound minecraft:block.stone.place hostile @a[distance=..32] ~ ~ ~ 1 0.6
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.ult"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/glow","minecraft:custom_model_data":{colors:[12727834]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 125
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
