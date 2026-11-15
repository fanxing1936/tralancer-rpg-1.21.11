# 七根火刑柱（as/at 圆心，朝他面向的方向）
execute rotated ~0.0 0 positioned ^ ^ ^9 run function rpg:jacques_boss/stakes/one0
execute rotated ~51.429 0 positioned ^ ^ ^9 run function rpg:jacques_boss/stakes/one1
execute rotated ~102.857 0 positioned ^ ^ ^9 run function rpg:jacques_boss/stakes/one2
execute rotated ~154.286 0 positioned ^ ^ ^9 run function rpg:jacques_boss/stakes/one3
execute rotated ~205.714 0 positioned ^ ^ ^9 run function rpg:jacques_boss/stakes/one4
execute rotated ~257.143 0 positioned ^ ^ ^9 run function rpg:jacques_boss/stakes/one5
execute rotated ~308.571 0 positioned ^ ^ ^9 run function rpg:jacques_boss/stakes/one6
summon minecraft:item_display ~ ~0.03 ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew","rpg.jqb.ult"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/glow","minecraft:custom_model_data":{colors:[5902854]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[20f,1f,20f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 125
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 0
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
