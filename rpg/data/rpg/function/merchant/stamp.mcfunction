execute unless score @s rpg_mer_day matches 0.. run return run scoreboard players operation @s rpg_mer_day = #day rpg_ev
execute unless score @s rpg_mer_day = #day rpg_ev at @s run function rpg:merchant/restock
