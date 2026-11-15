summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.crossv","rpg.jqb.ult"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[9401392]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,10.0f],left_rotation:[0f,0f,0f,1f],scale:[3f,0.02f,20f],right_rotation:[0f,0f,0f,1f]}}
tp @e[tag=rpg.jqb.fxnew,limit=1] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 30
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
