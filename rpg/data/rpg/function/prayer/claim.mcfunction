execute unless entity @s[type=minecraft:player,gamemode=!spectator] run return 0
execute if entity @s[nbt={Health:0.0f}] run return 0
execute if score @s rpg_pr_time matches 1.. run return run function rpg:prayer/error/busy
execute unless score @s rpg_pr_pending matches 1.. run return 0
function rpg:prayer/space
execute unless score @s rpg_pr_space matches 1 run return run function rpg:prayer/error/pending
execute if score @s rpg_pr_pending matches 1 run return run function rpg:prayer/reward/gold
execute if score @s rpg_pr_pending matches 2 run return run function rpg:prayer/reward/diamond
execute if score @s rpg_pr_pending matches 3 run return run function rpg:prayer/reward/iron
execute if score @s rpg_pr_pending matches 4 run return run function rpg:prayer/reward/smelting
execute if score @s rpg_pr_pending matches 5 run return run function rpg:prayer/reward/forging
execute if score @s rpg_pr_pending matches 6 run return run function rpg:prayer/reward/holy_water
execute if score @s rpg_pr_pending matches 7 run return run function rpg:prayer/reward/vital_potion
execute if score @s rpg_pr_pending matches 8 run return run function rpg:prayer/reward/shield_potion
execute if score @s rpg_pr_pending matches 9 run return run function rpg:prayer/reward/frost_helm
execute if score @s rpg_pr_pending matches 10 run return run function rpg:prayer/reward/frost_chest
execute if score @s rpg_pr_pending matches 11 run return run function rpg:prayer/reward/frost_legs
execute if score @s rpg_pr_pending matches 12 run return run function rpg:prayer/reward/frost_boots
execute if score @s rpg_pr_pending matches 13 run return run function rpg:prayer/reward/forest_helm
execute if score @s rpg_pr_pending matches 14 run return run function rpg:prayer/reward/forest_boots
execute if score @s rpg_pr_pending matches 15 run return run function rpg:prayer/reward/dogma
execute if score @s rpg_pr_pending matches 16 run return run function rpg:prayer/reward/truth
execute if score @s rpg_pr_pending matches 17 run return run function rpg:prayer/reward/vine
execute if score @s rpg_pr_pending matches 18 run return run function rpg:prayer/reward/chime
execute if score @s rpg_pr_pending matches 19 run return run function rpg:prayer/reward/mischief
execute if score @s rpg_pr_pending matches 20 run return run function rpg:prayer/reward/legend_smelting
execute if score @s rpg_pr_pending matches 21 run return run function rpg:prayer/reward/doll
execute if score @s rpg_pr_pending matches 22 run return run function rpg:prayer/reward/apocalypse
execute if score @s rpg_pr_pending matches 23 run return run function rpg:prayer/reward/faith
execute if score @s rpg_pr_pending matches 24 run return run function rpg:prayer/reward/longinus
execute if score @s rpg_pr_pending matches 25 run return run function rpg:prayer/reward/holy_crown
execute if score @s rpg_pr_pending matches 26 run return run function rpg:prayer/reward/shroud
execute if score @s rpg_pr_pending matches 27 run return run function rpg:prayer/reward/jachin
