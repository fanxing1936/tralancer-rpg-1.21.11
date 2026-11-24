execute as @a[scores={rpg_jr_do=1..}] at @s run function rpg:events/jr/press
scoreboard players add #t rpg_ev 1
execute if score #t rpg_ev matches 20.. run function rpg:events/sec
