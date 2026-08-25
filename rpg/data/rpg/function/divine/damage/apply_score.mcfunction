scoreboard players operation @s rpg_lt_max /= #hundred rpg_lt_max
execute store result storage rpg:divine damage.amount int 1 run scoreboard players get @s rpg_lt_max
execute if score @s rpg_lt_max matches 1.. run function rpg:divine/damage/macro with storage rpg:divine damage
