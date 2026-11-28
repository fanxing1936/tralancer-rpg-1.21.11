data merge entity @s {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b}
execute store result entity @s Rotation[0] float 1 run random value -180..179
tag @s add rpg.tw.guard
tag @s add rpg.ally
scoreboard players operation @s rpg_tw_id = #built rpg_tw
