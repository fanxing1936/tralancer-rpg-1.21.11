scoreboard players add @s rpg_mana 3
execute if score @s rpg_mana > @s rpg_mana_max run scoreboard players operation @s rpg_mana = @s rpg_mana_max
