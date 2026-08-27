execute if entity @s[nbt={Health:0.0f}] run return 0
execute if entity @s[gamemode=spectator] run return 0
scoreboard players remove @s rpg_pr_time 1
execute if score @s rpg_pr_time matches 35 run function rpg:prayer/fx/35
execute if score @s rpg_pr_time matches 25 run function rpg:prayer/fx/25
execute if score @s rpg_pr_time matches 15 run function rpg:prayer/fx/15
execute if score @s rpg_pr_time matches 5 run function rpg:prayer/fx/5
execute if score @s rpg_pr_time matches 0 run function rpg:prayer/claim
