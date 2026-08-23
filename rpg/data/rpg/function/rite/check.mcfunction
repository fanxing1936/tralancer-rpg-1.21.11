# 验阵。四盏都在才算数，缺一不成。
scoreboard players set @s rpg_rite 60
execute unless block ~3 ~ ~ minecraft:soul_lantern run function rpg:rite/fail
execute unless block ~-3 ~ ~ minecraft:soul_lantern run function rpg:rite/fail
execute unless block ~ ~ ~3 minecraft:soul_lantern run function rpg:rite/fail
execute unless block ~ ~ ~-3 minecraft:soul_lantern run function rpg:rite/fail
execute if block ~3 ~ ~ minecraft:soul_lantern if block ~-3 ~ ~ minecraft:soul_lantern if block ~ ~ ~3 minecraft:soul_lantern if block ~ ~ ~-3 minecraft:soul_lantern run function rpg:rite/purge
