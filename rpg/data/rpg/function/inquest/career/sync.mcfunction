scoreboard players operation @s rpg_ex_prev = @s rpg_ex_lvl
scoreboard players set @s rpg_ex_lvl 1
execute if score @s rpg_ex_xp matches 40.. run scoreboard players set @s rpg_ex_lvl 2
execute if score @s rpg_ex_xp matches 100.. run scoreboard players set @s rpg_ex_lvl 3
execute if score @s rpg_ex_xp matches 180.. run scoreboard players set @s rpg_ex_lvl 4
execute if score @s rpg_ex_xp matches 280.. run scoreboard players set @s rpg_ex_lvl 5
execute if score @s rpg_ex_lvl > @s rpg_ex_prev run function rpg:inquest/career/level_up
scoreboard players operation @s rpg_ex_seen = @s rpg_ex_xp
