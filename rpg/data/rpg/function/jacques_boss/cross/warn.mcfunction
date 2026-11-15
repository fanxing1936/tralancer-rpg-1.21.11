# 十字预警（as/at 十字中心）：四条暗金臂，各宽 3 长 20
execute rotated ~0 0 positioned ~ ~0.05 ~ run function rpg:jacques_boss/cross/arm_warn
execute rotated ~90 0 positioned ~ ~0.05 ~ run function rpg:jacques_boss/cross/arm_warn
execute rotated ~180 0 positioned ~ ~0.05 ~ run function rpg:jacques_boss/cross/arm_warn
execute rotated ~270 0 positioned ~ ~0.05 ~ run function rpg:jacques_boss/cross/arm_warn
summon minecraft:item_display ~ ~0.03 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/glow","minecraft:custom_model_data":{colors:[9401392]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,1f,6f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 30
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 30
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 1
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/hexagram","minecraft:custom_model_data":{colors:[13213770]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7f,1f,7f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 30
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 2
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
execute rotated ~0 0 positioned ^ ^ ^20 run function rpg:jacques_boss/cross/tip
execute rotated ~90 0 positioned ^ ^ ^20 run function rpg:jacques_boss/cross/tip
execute rotated ~180 0 positioned ^ ^ ^20 run function rpg:jacques_boss/cross/tip
execute rotated ~270 0 positioned ^ ^ ^20 run function rpg:jacques_boss/cross/tip
