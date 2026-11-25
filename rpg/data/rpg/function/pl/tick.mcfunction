scoreboard players add #t rpg_pl 1
execute if score #t rpg_pl matches 20.. run function rpg:pl/sec
execute as @e[type=minecraft:interaction,tag=rpg.pl.tree] if data entity @s interaction on target run function rpg:pl/tree/use
execute as @e[type=minecraft:interaction,tag=rpg.pl.tree] run data remove entity @s interaction
execute if score #rain rpg_pl matches 1.. run function rpg:pl/rain/tick
execute if score #t rpg_pl matches 10 run scoreboard players remove @a[scores={rpg_pl_tb=1..}] rpg_pl_tb 1
execute if score #t rpg_pl matches 11 as @a[scores={rpg_pl_tb=0}] run function rpg:pl/tree/off
