execute if score @s rpg_force matches 1 run scoreboard players remove @s rpg_assim 5
execute if score @s rpg_assim matches ..-1 run scoreboard players set @s rpg_assim 0
execute unless score @s rpg_force matches 1 run scoreboard players remove @s rpg_taint 15
execute if score @s rpg_taint matches ..-1 run scoreboard players set @s rpg_taint 0
particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.02 30
