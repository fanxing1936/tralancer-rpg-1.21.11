scoreboard players add @s rpg_end_time 1
execute if score @s rpg_end_time matches 120.. run function rpg:endless/floor/begin
