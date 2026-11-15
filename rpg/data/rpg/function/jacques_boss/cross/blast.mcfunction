# 十字炸开（as/at 十字中心）：四臂同时判定 18；四道光、冲击环
execute rotated ~0 0 positioned ~ ~0.6 ~ run function rpg:jacques_boss/cross/arm
execute rotated ~90 0 positioned ~ ~0.6 ~ run function rpg:jacques_boss/cross/arm
execute rotated ~180 0 positioned ~ ~0.6 ~ run function rpg:jacques_boss/cross/arm
execute rotated ~270 0 positioned ~ ~0.6 ~ run function rpg:jacques_boss/cross/arm
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit] run damage @s 18 minecraft:magic by @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1]
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit,tag=rpg.jqb.cursed] at @s run function rpg:jacques_boss/curse/pop
tag @e[tag=rpg.unit] remove rpg.jqb.hit
summon minecraft:item_display ~ ~0.12 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[10f,1f,10f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 5
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#FFF2C8"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,5f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:text_display ~ ~2.4 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#F0CF7A"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.75f,8.75f,8.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 4
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.15 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 14
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 19
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagram","minecraft:custom_model_data":{colors:[16771496]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[9f,1f,9f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 17
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 21
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 24
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 22
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30 force
particle minecraft:flash{color:16773832} ~ ~1.5 ~ 0 0 0 0 1 force
particle minecraft:totem_of_undying ~ ~1 ~ 1 1.5 1 0.6 80 force
particle minecraft:end_rod ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.7 0 force
particle minecraft:end_rod ~0.39 ~0.20 ~0.08 0.981 0.000 0.195 0.7 0 force
particle minecraft:end_rod ~0.37 ~0.20 ~0.15 0.924 0.000 0.383 0.7 0 force
particle minecraft:end_rod ~0.33 ~0.20 ~0.22 0.831 0.000 0.556 0.7 0 force
particle minecraft:end_rod ~0.28 ~0.20 ~0.28 0.707 0.000 0.707 0.7 0 force
particle minecraft:end_rod ~0.22 ~0.20 ~0.33 0.556 0.000 0.831 0.7 0 force
particle minecraft:end_rod ~0.15 ~0.20 ~0.37 0.383 0.000 0.924 0.7 0 force
particle minecraft:end_rod ~0.08 ~0.20 ~0.39 0.195 0.000 0.981 0.7 0 force
particle minecraft:end_rod ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.7 0 force
particle minecraft:end_rod ~-0.08 ~0.20 ~0.39 -0.195 0.000 0.981 0.7 0 force
particle minecraft:end_rod ~-0.15 ~0.20 ~0.37 -0.383 0.000 0.924 0.7 0 force
particle minecraft:end_rod ~-0.22 ~0.20 ~0.33 -0.556 0.000 0.831 0.7 0 force
particle minecraft:end_rod ~-0.28 ~0.20 ~0.28 -0.707 0.000 0.707 0.7 0 force
particle minecraft:end_rod ~-0.33 ~0.20 ~0.22 -0.831 0.000 0.556 0.7 0 force
particle minecraft:end_rod ~-0.37 ~0.20 ~0.15 -0.924 0.000 0.383 0.7 0 force
particle minecraft:end_rod ~-0.39 ~0.20 ~0.08 -0.981 0.000 0.195 0.7 0 force
particle minecraft:end_rod ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.7 0 force
particle minecraft:end_rod ~-0.39 ~0.20 ~-0.08 -0.981 0.000 -0.195 0.7 0 force
particle minecraft:end_rod ~-0.37 ~0.20 ~-0.15 -0.924 0.000 -0.383 0.7 0 force
particle minecraft:end_rod ~-0.33 ~0.20 ~-0.22 -0.831 0.000 -0.556 0.7 0 force
particle minecraft:end_rod ~-0.28 ~0.20 ~-0.28 -0.707 0.000 -0.707 0.7 0 force
particle minecraft:end_rod ~-0.22 ~0.20 ~-0.33 -0.556 0.000 -0.831 0.7 0 force
particle minecraft:end_rod ~-0.15 ~0.20 ~-0.37 -0.383 0.000 -0.924 0.7 0 force
particle minecraft:end_rod ~-0.08 ~0.20 ~-0.39 -0.195 0.000 -0.981 0.7 0 force
particle minecraft:end_rod ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.7 0 force
particle minecraft:end_rod ~0.08 ~0.20 ~-0.39 0.195 0.000 -0.981 0.7 0 force
particle minecraft:end_rod ~0.15 ~0.20 ~-0.37 0.383 0.000 -0.924 0.7 0 force
particle minecraft:end_rod ~0.22 ~0.20 ~-0.33 0.556 0.000 -0.831 0.7 0 force
particle minecraft:end_rod ~0.28 ~0.20 ~-0.28 0.707 0.000 -0.707 0.7 0 force
particle minecraft:end_rod ~0.33 ~0.20 ~-0.22 0.831 0.000 -0.556 0.7 0 force
particle minecraft:end_rod ~0.37 ~0.20 ~-0.15 0.924 0.000 -0.383 0.7 0 force
particle minecraft:end_rod ~0.39 ~0.20 ~-0.08 0.981 0.000 -0.195 0.7 0 force
particle minecraft:firework ~0.40 ~0.60 ~0.00 1.000 0.000 0.000 0.5 0 force
particle minecraft:firework ~0.39 ~0.60 ~0.10 0.966 0.000 0.259 0.5 0 force
particle minecraft:firework ~0.35 ~0.60 ~0.20 0.866 0.000 0.500 0.5 0 force
particle minecraft:firework ~0.28 ~0.60 ~0.28 0.707 0.000 0.707 0.5 0 force
particle minecraft:firework ~0.20 ~0.60 ~0.35 0.500 0.000 0.866 0.5 0 force
particle minecraft:firework ~0.10 ~0.60 ~0.39 0.259 0.000 0.966 0.5 0 force
particle minecraft:firework ~0.00 ~0.60 ~0.40 0.000 0.000 1.000 0.5 0 force
particle minecraft:firework ~-0.10 ~0.60 ~0.39 -0.259 0.000 0.966 0.5 0 force
particle minecraft:firework ~-0.20 ~0.60 ~0.35 -0.500 0.000 0.866 0.5 0 force
particle minecraft:firework ~-0.28 ~0.60 ~0.28 -0.707 0.000 0.707 0.5 0 force
particle minecraft:firework ~-0.35 ~0.60 ~0.20 -0.866 0.000 0.500 0.5 0 force
particle minecraft:firework ~-0.39 ~0.60 ~0.10 -0.966 0.000 0.259 0.5 0 force
particle minecraft:firework ~-0.40 ~0.60 ~0.00 -1.000 0.000 0.000 0.5 0 force
particle minecraft:firework ~-0.39 ~0.60 ~-0.10 -0.966 0.000 -0.259 0.5 0 force
particle minecraft:firework ~-0.35 ~0.60 ~-0.20 -0.866 0.000 -0.500 0.5 0 force
particle minecraft:firework ~-0.28 ~0.60 ~-0.28 -0.707 0.000 -0.707 0.5 0 force
particle minecraft:firework ~-0.20 ~0.60 ~-0.35 -0.500 0.000 -0.866 0.5 0 force
particle minecraft:firework ~-0.10 ~0.60 ~-0.39 -0.259 0.000 -0.966 0.5 0 force
particle minecraft:firework ~-0.00 ~0.60 ~-0.40 -0.000 0.000 -1.000 0.5 0 force
particle minecraft:firework ~0.10 ~0.60 ~-0.39 0.259 0.000 -0.966 0.5 0 force
particle minecraft:firework ~0.20 ~0.60 ~-0.35 0.500 0.000 -0.866 0.5 0 force
particle minecraft:firework ~0.28 ~0.60 ~-0.28 0.707 0.000 -0.707 0.5 0 force
particle minecraft:firework ~0.35 ~0.60 ~-0.20 0.866 0.000 -0.500 0.5 0 force
particle minecraft:firework ~0.39 ~0.60 ~-0.10 0.966 0.000 -0.259 0.5 0 force
playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..40] ~ ~ ~ 1.4 0.8
playsound minecraft:block.bell.use hostile @a[distance=..40] ~ ~ ~ 1.4 0.6
kill @s
