# 暴食：击杀回复 2 点生命（美丽阶起 4 点）
execute unless score @s rpg_fo_kl matches 1.. run return 0
scoreboard players set @s rpg_fo_kl 0
execute unless score @s rpg_sef matches 5.. run effect give @s minecraft:regeneration 3 1 true
execute if score @s rpg_sef matches 5.. run effect give @s minecraft:instant_health 1 0 true
