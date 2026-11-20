# 一道斩痕（at 落点，朝向随机）：亮 0.6 秒后斩下
summon minecraft:marker ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.cut"]}
execute as @e[tag=rpg.slb.fxnew] run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 13
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
execute positioned ~ ~0.05 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[6950936]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5f,0.02f,4.4f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.05 ~ run tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 12
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
playsound minecraft:block.note_block.hat hostile @a[distance=..24] ~ ~ ~ 0.6 1.6
