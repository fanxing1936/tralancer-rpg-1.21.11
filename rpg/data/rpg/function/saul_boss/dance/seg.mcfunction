summon minecraft:marker ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.danceseg"]}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 400
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
execute positioned ~ ~0.08 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.dancebeam"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[6950936]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,-1.0f],left_rotation:[0f,0f,0f,1f],scale:[0.35f,0.03f,2.2f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.08 ~ run tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 400
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
