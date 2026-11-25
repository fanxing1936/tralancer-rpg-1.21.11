# 随机一首，和上一首不同（最近一首记在 l，从 1 数）
execute store result score #r rpg_bgm run random value 1..3
execute if score #r rpg_bgm = @s rpg_bgm_l run scoreboard players add #r rpg_bgm 1
execute if score #r rpg_bgm matches 4.. run scoreboard players set #r rpg_bgm 1
scoreboard players operation @s rpg_bgm_l = #r rpg_bgm
execute if score #r rpg_bgm matches 1 run return run function rpg:bgm/play/ow_day1
execute if score #r rpg_bgm matches 2 run return run function rpg:bgm/play/ow_day2
execute if score #r rpg_bgm matches 3 run return run function rpg:bgm/play/ow_day3
