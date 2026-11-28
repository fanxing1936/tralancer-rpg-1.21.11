function rpg:town/job/fl_rem with storage rpg:town m
scoreboard players set #cool rpg_tw 3
scoreboard players add #c rpg_tw 1
scoreboard players set #ph rpg_tw 0
execute if score #c rpg_tw matches 97.. run function rpg:town/job/give_up
