scoreboard players add @s rpg_pl_er 1
execute unless score @s rpg_pl_er matches 60.. run return 0
scoreboard players set @s rpg_pl_er 0
execute if score @s rpg_force matches 1 if score @s rpg_vital matches 1.. run scoreboard players remove @s rpg_vital 1
execute unless score @s rpg_force matches 1 if score @s rpg_taint matches ..89 run scoreboard players add @s rpg_taint 1
