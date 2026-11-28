execute unless score #run rpg_te matches 1.. run return 0
execute unless score #kind rpg_te matches 3 run return 0
execute unless score #ph rpg_te matches 3 run return 0
execute as @e[type=minecraft:villager,tag=rpg.te.witch] at @s run function rpg:town/ev/w/follow
