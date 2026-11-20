summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.aim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[9213602]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,10f],left_rotation:[0f,0f,0f,1f],scale:[0.8f,0.02f,20f],right_rotation:[0f,0f,0f,1f]}}
tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 42
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
