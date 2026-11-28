execute if score @s rpg_pr_cd1 matches 1.. run return run playsound minecraft:block.note_block.bass master @s ~ ~ ~ 1 0.6
scoreboard players set @s rpg_pr_cd1 240
tag @s add rpg.pact.cast
execute if score @s rpg_pr_role matches 1 run function rpg:pact/s/p1
execute if score @s rpg_pr_role matches 2 run function rpg:pact/s/p4
execute if score @s rpg_pr_role matches 3 run function rpg:pact/s/p6
execute if score @s rpg_pr_role matches 4 run function rpg:pact/s/p7
tag @s remove rpg.pact.cast
