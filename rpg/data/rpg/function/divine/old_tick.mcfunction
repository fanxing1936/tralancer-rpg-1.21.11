scoreboard players add @s rpg_lt_regen 1
execute if score @s rpg_lt_regen matches 400.. run effect give @s minecraft:regeneration 1 0 true
execute if score @s rpg_lt_regen matches 400.. run scoreboard players set @s rpg_lt_regen 0
