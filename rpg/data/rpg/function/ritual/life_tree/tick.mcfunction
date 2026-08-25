scoreboard players add #life_tree rpg_lt_tick 1
execute if score #life_tree rpg_lt_tick matches 10.. run scoreboard players set #life_tree rpg_lt_tick 0
execute if score #life_tree rpg_lt_tick matches 0 run execute as @e[type=minecraft:marker,tag=rpg.ritual.life_tree] at @s run function rpg:ritual/life_tree/draw
