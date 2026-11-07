# 二阶技能：潜行长按。
execute unless score @s rpg_pact_lv matches 2.. run return run function rpg:hud/m81
execute if score @s rpg_pact_cd2 matches 1.. run return run function rpg:hud/m80
execute if score @s rpg_pact matches 5 unless entity @e[type=#rpg:seal_hostile,distance=..14,limit=1] run return run function rpg:pact/say/no_target
scoreboard players set @s rpg_pact_cd2 400
scoreboard players add @s rpg_taint 6
tag @s add rpg.pact.cast
execute if score @s rpg_pact matches 1 run function rpg:pact/s/p1
execute if score @s rpg_pact matches 2 run function rpg:pact/s/p2
execute if score @s rpg_pact matches 3 run function rpg:pact/s/p3
execute if score @s rpg_pact matches 4 run function rpg:pact/s/p4
execute if score @s rpg_pact matches 5 run function rpg:pact/s/p5
execute if score @s rpg_pact matches 6 run function rpg:pact/s/p6
execute if score @s rpg_pact matches 7 run function rpg:pact/s/p7
tag @s remove rpg.pact.cast
