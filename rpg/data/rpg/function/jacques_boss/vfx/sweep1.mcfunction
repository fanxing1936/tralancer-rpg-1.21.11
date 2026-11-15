# 横扫（as/at 他）：弧线上的金光向外甩出
particle minecraft:end_rod ^-2.6 ^1.1 ^1.5 0.15 0.15 0.15 0.06 3 force
particle minecraft:end_rod ^-2.12 ^1.1 ^2.12 0.15 0.15 0.15 0.06 3 force
particle minecraft:end_rod ^-1.5 ^1.1 ^2.6 0.15 0.15 0.15 0.06 3 force
particle minecraft:end_rod ^-0.78 ^1.1 ^2.9 0.15 0.15 0.15 0.06 3 force
particle minecraft:end_rod ^0.0 ^1.1 ^3.0 0.15 0.15 0.15 0.06 3 force
particle minecraft:end_rod ^0.78 ^1.1 ^2.9 0.15 0.15 0.15 0.06 3 force
particle minecraft:end_rod ^1.5 ^1.1 ^2.6 0.15 0.15 0.15 0.06 3 force
particle minecraft:end_rod ^2.12 ^1.1 ^2.12 0.15 0.15 0.15 0.06 3 force
particle minecraft:end_rod ^2.6 ^1.1 ^1.5 0.15 0.15 0.15 0.06 3 force
particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3} ^-2.6 ^1.1 ^1.5 0.1 0.1 0.1 0 2 force
particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3} ^-2.12 ^1.1 ^2.12 0.1 0.1 0.1 0 2 force
particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3} ^-1.5 ^1.1 ^2.6 0.1 0.1 0.1 0 2 force
particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3} ^-0.78 ^1.1 ^2.9 0.1 0.1 0.1 0 2 force
particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3} ^0.0 ^1.1 ^3.0 0.1 0.1 0.1 0 2 force
particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3} ^0.78 ^1.1 ^2.9 0.1 0.1 0.1 0 2 force
particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3} ^1.5 ^1.1 ^2.6 0.1 0.1 0.1 0 2 force
particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3} ^2.12 ^1.1 ^2.12 0.1 0.1 0.1 0 2 force
particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3} ^2.6 ^1.1 ^1.5 0.1 0.1 0.1 0 2 force
summon minecraft:item_display ^ ^0.1 ^1.5 {Tags:["rpg.jqb.fx","rpg.jqb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,1f,5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_life 16
scoreboard players set @e[tag=rpg.jqb.fxnew] rpg_jq_kd 5
tag @e[tag=rpg.jqb.fxnew] remove rpg.jqb.fxnew
