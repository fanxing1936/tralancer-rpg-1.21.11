$summon minecraft:text_display ~ ~2.6 ~ {Tags:["rpg.dt.fx","rpg.dt.card","rpg.dt.cnew"],text:{"text":"$(x)","color":"#FFFFFF","bold":true},background:-1441722342,billboard:"center",brightness:{sky:15,block:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
$summon minecraft:marker ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.card","rpg.dt.cnew","rpg.dt.k$(k)","rpg.dt.km"]}
scoreboard players set @e[tag=rpg.dt.cnew,distance=..4] rpg_dt_life 170
scoreboard players set @e[tag=rpg.dt.cnew,distance=..4] rpg_dt_kd 0
tag @e[tag=rpg.dt.cnew,distance=..4] remove rpg.dt.cnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew","rpg.dt.card"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:daath_fx/seal_question","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 130
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 15
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
summon minecraft:item_display ~ ~0.07 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew","rpg.dt.card"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 130
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 0
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..48] ~ ~ ~ 1 0.8
