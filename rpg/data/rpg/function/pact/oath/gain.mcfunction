# 涨契合，封顶 100。#gain 由调用方给。
scoreboard players operation @s rpg_pact_bond += #gain rpg_pact
execute if score @s rpg_pact_bond matches 101.. run scoreboard players set @s rpg_pact_bond 100
