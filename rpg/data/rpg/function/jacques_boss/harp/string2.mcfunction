summon minecraft:marker ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.str","rpg.jqb.ult"]}
tp @e[tag=rpg.jqb.fxnew,limit=1] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_id 2
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 46
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.strv","rpg.jqb.ult"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0.05f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.12f,0.02f,30f],right_rotation:[0f,0f,0f,1f]}}
tp @e[tag=rpg.jqb.fxnew,limit=1] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_id 2
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 46
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
