tag @s add rpg.el.boss
execute store result score @s rpg_el_a2 run random value 1..9
execute if score @s rpg_el_a2 >= @s rpg_el_a1 run scoreboard players add @s rpg_el_a2 1
