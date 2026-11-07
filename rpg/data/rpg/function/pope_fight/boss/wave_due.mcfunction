scoreboard players set #wave rpg_pf 1
execute if score #next rpg_pf matches 750 run return run scoreboard players set #next rpg_pf 500
execute if score #next rpg_pf matches 500 run return run scoreboard players set #next rpg_pf 250
execute if score #next rpg_pf matches 250 run return run scoreboard players set #next rpg_pf 0
