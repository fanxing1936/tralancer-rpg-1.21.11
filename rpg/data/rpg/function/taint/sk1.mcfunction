# 五招掷一招，并记住上一招；若撞号则顺延一格，避免连续重复。
execute store result score #pick rpg_fall run random value 1..5
execute if score #pick rpg_fall = @s rpg_dm_last run scoreboard players add #pick rpg_fall 1
execute if score #pick rpg_fall matches 6.. run scoreboard players set #pick rpg_fall 1
scoreboard players operation @s rpg_dm_last = #pick rpg_fall
execute if score #pick rpg_fall matches 1 run return run function rpg:taint/sk1_1
execute if score #pick rpg_fall matches 2 run return run function rpg:taint/sk1_2
execute if score #pick rpg_fall matches 3 run return run function rpg:taint/sk1_3
execute if score #pick rpg_fall matches 4 run return run function rpg:taint/sk1_4
execute if score #pick rpg_fall matches 5 run return run function rpg:taint/sk1_5
