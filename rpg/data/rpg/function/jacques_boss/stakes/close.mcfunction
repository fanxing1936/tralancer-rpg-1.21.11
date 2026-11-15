# 收拢（at 圆心）：圈里所有人 16
execute positioned ~ ~ ~ run tag @e[tag=rpg.unit.f,distance=..9.5] add rpg.jqb.hit
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit] run damage @s 16 minecraft:magic by @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1]
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit,tag=rpg.jqb.cursed] at @s run function rpg:jacques_boss/curse/pop
tag @e[tag=rpg.unit] remove rpg.jqb.hit
kill @e[tag=rpg.jqb.stakev]
kill @e[type=minecraft:marker,tag=rpg.jqb.stake]
summon minecraft:item_display ~ ~0.12 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[16747069]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[22f,1f,22f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 5
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~1.4 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FF8A3D"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6.25f,6.25f,6.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~3 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFD08A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[11.25f,11.25f,11.25f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.15 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16765066]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 14
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 19
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagram","minecraft:custom_model_data":{colors:[12727834]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[12f,1f,12f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 30
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 17
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/cracks","minecraft:custom_model_data":{colors:[2755076]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[10f,1f,10f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 80
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16747069]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 21
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 22
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
particle minecraft:flame ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.8 0 force
particle minecraft:flame ~0.39 ~0.20 ~0.07 0.985 0.000 0.174 0.8 0 force
particle minecraft:flame ~0.38 ~0.20 ~0.14 0.940 0.000 0.342 0.8 0 force
particle minecraft:flame ~0.35 ~0.20 ~0.20 0.866 0.000 0.500 0.8 0 force
particle minecraft:flame ~0.31 ~0.20 ~0.26 0.766 0.000 0.643 0.8 0 force
particle minecraft:flame ~0.26 ~0.20 ~0.31 0.643 0.000 0.766 0.8 0 force
particle minecraft:flame ~0.20 ~0.20 ~0.35 0.500 0.000 0.866 0.8 0 force
particle minecraft:flame ~0.14 ~0.20 ~0.38 0.342 0.000 0.940 0.8 0 force
particle minecraft:flame ~0.07 ~0.20 ~0.39 0.174 0.000 0.985 0.8 0 force
particle minecraft:flame ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.8 0 force
particle minecraft:flame ~-0.07 ~0.20 ~0.39 -0.174 0.000 0.985 0.8 0 force
particle minecraft:flame ~-0.14 ~0.20 ~0.38 -0.342 0.000 0.940 0.8 0 force
particle minecraft:flame ~-0.20 ~0.20 ~0.35 -0.500 0.000 0.866 0.8 0 force
particle minecraft:flame ~-0.26 ~0.20 ~0.31 -0.643 0.000 0.766 0.8 0 force
particle minecraft:flame ~-0.31 ~0.20 ~0.26 -0.766 0.000 0.643 0.8 0 force
particle minecraft:flame ~-0.35 ~0.20 ~0.20 -0.866 0.000 0.500 0.8 0 force
particle minecraft:flame ~-0.38 ~0.20 ~0.14 -0.940 0.000 0.342 0.8 0 force
particle minecraft:flame ~-0.39 ~0.20 ~0.07 -0.985 0.000 0.174 0.8 0 force
particle minecraft:flame ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.8 0 force
particle minecraft:flame ~-0.39 ~0.20 ~-0.07 -0.985 0.000 -0.174 0.8 0 force
particle minecraft:flame ~-0.38 ~0.20 ~-0.14 -0.940 0.000 -0.342 0.8 0 force
particle minecraft:flame ~-0.35 ~0.20 ~-0.20 -0.866 0.000 -0.500 0.8 0 force
particle minecraft:flame ~-0.31 ~0.20 ~-0.26 -0.766 0.000 -0.643 0.8 0 force
particle minecraft:flame ~-0.26 ~0.20 ~-0.31 -0.643 0.000 -0.766 0.8 0 force
particle minecraft:flame ~-0.20 ~0.20 ~-0.35 -0.500 0.000 -0.866 0.8 0 force
particle minecraft:flame ~-0.14 ~0.20 ~-0.38 -0.342 0.000 -0.940 0.8 0 force
particle minecraft:flame ~-0.07 ~0.20 ~-0.39 -0.174 0.000 -0.985 0.8 0 force
particle minecraft:flame ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.8 0 force
particle minecraft:flame ~0.07 ~0.20 ~-0.39 0.174 0.000 -0.985 0.8 0 force
particle minecraft:flame ~0.14 ~0.20 ~-0.38 0.342 0.000 -0.940 0.8 0 force
particle minecraft:flame ~0.20 ~0.20 ~-0.35 0.500 0.000 -0.866 0.8 0 force
particle minecraft:flame ~0.26 ~0.20 ~-0.31 0.643 0.000 -0.766 0.8 0 force
particle minecraft:flame ~0.31 ~0.20 ~-0.26 0.766 0.000 -0.643 0.8 0 force
particle minecraft:flame ~0.35 ~0.20 ~-0.20 0.866 0.000 -0.500 0.8 0 force
particle minecraft:flame ~0.38 ~0.20 ~-0.14 0.940 0.000 -0.342 0.8 0 force
particle minecraft:flame ~0.39 ~0.20 ~-0.07 0.985 0.000 -0.174 0.8 0 force
particle minecraft:flame ~0.40 ~1.20 ~0.00 1.000 0.250 0.000 0.5 0 force
particle minecraft:flame ~0.39 ~1.20 ~0.10 0.966 0.250 0.259 0.5 0 force
particle minecraft:flame ~0.35 ~1.20 ~0.20 0.866 0.250 0.500 0.5 0 force
particle minecraft:flame ~0.28 ~1.20 ~0.28 0.707 0.250 0.707 0.5 0 force
particle minecraft:flame ~0.20 ~1.20 ~0.35 0.500 0.250 0.866 0.5 0 force
particle minecraft:flame ~0.10 ~1.20 ~0.39 0.259 0.250 0.966 0.5 0 force
particle minecraft:flame ~0.00 ~1.20 ~0.40 0.000 0.250 1.000 0.5 0 force
particle minecraft:flame ~-0.10 ~1.20 ~0.39 -0.259 0.250 0.966 0.5 0 force
particle minecraft:flame ~-0.20 ~1.20 ~0.35 -0.500 0.250 0.866 0.5 0 force
particle minecraft:flame ~-0.28 ~1.20 ~0.28 -0.707 0.250 0.707 0.5 0 force
particle minecraft:flame ~-0.35 ~1.20 ~0.20 -0.866 0.250 0.500 0.5 0 force
particle minecraft:flame ~-0.39 ~1.20 ~0.10 -0.966 0.250 0.259 0.5 0 force
particle minecraft:flame ~-0.40 ~1.20 ~0.00 -1.000 0.250 0.000 0.5 0 force
particle minecraft:flame ~-0.39 ~1.20 ~-0.10 -0.966 0.250 -0.259 0.5 0 force
particle minecraft:flame ~-0.35 ~1.20 ~-0.20 -0.866 0.250 -0.500 0.5 0 force
particle minecraft:flame ~-0.28 ~1.20 ~-0.28 -0.707 0.250 -0.707 0.5 0 force
particle minecraft:flame ~-0.20 ~1.20 ~-0.35 -0.500 0.250 -0.866 0.5 0 force
particle minecraft:flame ~-0.10 ~1.20 ~-0.39 -0.259 0.250 -0.966 0.5 0 force
particle minecraft:flame ~-0.00 ~1.20 ~-0.40 -0.000 0.250 -1.000 0.5 0 force
particle minecraft:flame ~0.10 ~1.20 ~-0.39 0.259 0.250 -0.966 0.5 0 force
particle minecraft:flame ~0.20 ~1.20 ~-0.35 0.500 0.250 -0.866 0.5 0 force
particle minecraft:flame ~0.28 ~1.20 ~-0.28 0.707 0.250 -0.707 0.5 0 force
particle minecraft:flame ~0.35 ~1.20 ~-0.20 0.866 0.250 -0.500 0.5 0 force
particle minecraft:flame ~0.39 ~1.20 ~-0.10 0.966 0.250 -0.259 0.5 0 force
particle minecraft:lava ~ ~0.60 ~ 0.500 0.900 0.000 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ 1.000 0.600 0.000 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ 0.354 0.900 0.354 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ 0.707 0.600 0.707 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ 0.000 0.900 0.500 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ 0.000 0.600 1.000 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ -0.354 0.900 0.354 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ -0.707 0.600 0.707 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ -0.500 0.900 0.000 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ -1.000 0.600 0.000 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ -0.354 0.900 -0.354 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ -0.707 0.600 -0.707 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ -0.000 0.900 -0.500 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ -0.000 0.600 -1.000 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ 0.354 0.900 -0.354 0.8 0 force
particle minecraft:lava ~ ~0.60 ~ 0.707 0.600 -0.707 0.8 0 force
particle minecraft:flash{color:16747069} ~ ~1.5 ~ 0 0 0 0 1 force
particle minecraft:large_smoke ~ ~1 ~ 2 0.6 2 0.05 40 force
particle minecraft:flame ~ ~0.5 ~ 7 0.4 7 0.2 120
playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1.4 0.6
