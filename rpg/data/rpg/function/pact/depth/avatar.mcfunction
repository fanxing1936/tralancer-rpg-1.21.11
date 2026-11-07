# 化身：潜行抬头长按。大招加 20 秒附身。
execute unless score @s rpg_pact_lv matches 3.. run return run function rpg:hud/m81
execute if score @s rpg_pact_cd3 matches 1.. run return run function rpg:hud/m80
scoreboard players set @s rpg_pact_cd3 3600
scoreboard players add @s rpg_taint 15
scoreboard players set @s rpg_pact_av 400
tag @s add rpg.pact.cast
execute if score @s rpg_pact matches 1 run function rpg:pact/s/a1
execute if score @s rpg_pact matches 2 run function rpg:pact/s/a2
execute if score @s rpg_pact matches 3 run function rpg:pact/s/a3
execute if score @s rpg_pact matches 4 run function rpg:pact/s/a4
execute if score @s rpg_pact matches 5 run function rpg:pact/s/a5
execute if score @s rpg_pact matches 6 run function rpg:pact/s/a6
execute if score @s rpg_pact matches 7 run function rpg:pact/s/a7
tag @s remove rpg.pact.cast
