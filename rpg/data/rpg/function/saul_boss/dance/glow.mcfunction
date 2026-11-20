# 剑痕发亮（as 他）：快斩开了
execute as @e[tag=rpg.slb.dancebeam] run data modify entity @s item.components."minecraft:custom_model_data".colors[0] set value 15660282
execute as @e[tag=rpg.slb.danceseg] at @s run particle minecraft:end_rod ~ ~0.4 ~ 0.3 0.1 0.3 0.01 2
playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 1 1.6
