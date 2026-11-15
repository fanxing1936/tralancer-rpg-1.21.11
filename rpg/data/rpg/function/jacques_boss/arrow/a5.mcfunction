# 一支弩箭（at 弩口，朝飞行方向）：原作光束拉成细箭，每刻前进 1 格
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.arrow","rpg.jqb.a5"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.07f,0.07f,1.3f],right_rotation:[0f,0f,0f,1f]}}
tp @e[tag=rpg.jqb.fxnew,limit=1] ~ ~ ~ ~ ~
execute if score #stage rpg_jq matches 2 run tag @e[tag=rpg.jqb.fxnew] add rpg.jqb.af
execute if score #stage rpg_jq matches 2 as @e[tag=rpg.jqb.fxnew] run data modify entity @s item.components."minecraft:custom_model_data".colors[0] set value 16747069
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 30
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
