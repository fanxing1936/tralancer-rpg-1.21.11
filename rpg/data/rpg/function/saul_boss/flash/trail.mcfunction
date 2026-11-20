# 剑痕的一节（at 这一节，朝落点）
summon minecraft:marker ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.flashseg"]}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 12
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
execute positioned ~ ~1 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[15660282]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0.75f],left_rotation:[0f,0f,0f,1f],scale:[0.16f,0.16f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~1 ~ run tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 12
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:end_rod ~ ~1 ~ 0.2 0.2 0.2 0.02 2
scoreboard players remove #d rpg_sl 1
execute if score #d rpg_sl matches 1.. unless entity @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,distance=..1.6] positioned ^ ^ ^1.5 run function rpg:saul_boss/flash/trail
