execute if score @s rpg_force matches 2 run scoreboard players add @s rpg_mana 50
execute if score @s rpg_force matches 2 if score @s rpg_mana > @s rpg_mana_max run scoreboard players operation @s rpg_mana = @s rpg_mana_max
execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana2 50
execute if score @s rpg_force matches 3 if score @s rpg_mana2 > @s rpg_mana_max run scoreboard players operation @s rpg_mana2 = @s rpg_mana_max
scoreboard players add @s rpg_taint 8
execute if score @s rpg_taint matches 101.. run scoreboard players set @s rpg_taint 100
