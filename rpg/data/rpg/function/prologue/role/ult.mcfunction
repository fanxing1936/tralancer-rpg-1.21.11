execute if score @s rpg_pr_cd2 matches 1.. run return run playsound minecraft:block.note_block.bass master @s ~ ~ ~ 1 0.5
scoreboard players set @s rpg_pr_cd2 1200
scoreboard players set @s rpg_pr_av 400
tag @s add rpg.pact.cast
execute if score @s rpg_pr_role matches 1 run function rpg:prologue/role/morning_star
execute if score @s rpg_pr_role matches 2 run function rpg:pact/s/a4
execute if score @s rpg_pr_role matches 3 run function rpg:pact/s/a6
execute if score @s rpg_pr_role matches 4 run function rpg:pact/s/a7
tag @s remove rpg.pact.cast
