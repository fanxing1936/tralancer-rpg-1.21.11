# 按身份分配力（as 玩家）。无知者先没有，美丽阶觉醒时自选。
execute if score @s rpg_ident matches 1 run scoreboard players set @s rpg_force 0
execute if score @s rpg_ident matches 2 run scoreboard players set @s rpg_force 2
execute if score @s rpg_ident matches 3 run scoreboard players set @s rpg_force 1
execute if score @s rpg_ident matches 4 run scoreboard players set @s rpg_force 2
execute if score @s rpg_ident matches 5 run scoreboard players set @s rpg_force 1
execute if score @s rpg_ident matches 6 run scoreboard players set @s rpg_force 1
execute if score @s rpg_ident matches 7 run scoreboard players set @s rpg_force 3
scoreboard players set @s rpg_vital 100
scoreboard players set @s rpg_assim 0
scoreboard players set @s rpg_mana 0
scoreboard players set @s rpg_mana2 0
scoreboard players operation @s rpg_fz_tp = @s rpg_taint
execute unless score @s rpg_mana_max matches 1.. run scoreboard players set @s rpg_mana_max 100
