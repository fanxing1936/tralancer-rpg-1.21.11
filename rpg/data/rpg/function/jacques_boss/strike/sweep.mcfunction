# 横扫（as/at 载体）：身前约 80°、4.5 格；原作弧光横贴在胸口高度
execute positioned ^ ^ ^1.4 run tag @e[tag=rpg.unit.f,distance=..3.2] add rpg.jqb.hit
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit] run damage @s 11 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1]
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit,tag=rpg.jqb.cursed] at @s run function rpg:jacques_boss/curse/pop
tag @e[tag=rpg.unit] remove rpg.jqb.hit
execute positioned ^ ^1.1 ^1.2 run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/crescent","minecraft:custom_model_data":{colors:[15781754]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rpg.jqb.fxnew] positioned as @s run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 8
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 15
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
particle minecraft:sweep_attack ^ ^1 ^1.8 0.8 0.2 0.8 0 4
execute if score @s rpg_jq matches 1 run function rpg:jacques_boss/vfx/sweep1
execute if score @s rpg_jq matches 2 run function rpg:jacques_boss/vfx/sweep2
execute if score @s rpg_jq matches 2 run function rpg:jacques_boss/strike/fireline
