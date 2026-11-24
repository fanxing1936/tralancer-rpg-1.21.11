tag @s add rpg.q.gate
scoreboard players add @s rpg_q_eg 1
particle minecraft:end_rod ~1.2 ~ ~ 0 3 0 0 12
particle minecraft:end_rod ~-1.2 ~ ~ 0 3 0 0 12
execute if score @s rpg_q_eg matches 10 run function rpg:quest/title/get_gate
