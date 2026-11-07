# 每 30 次结算渗一次，每升一阶多 1 点。贪婪那一柱翻倍。
scoreboard players add @s rpg_pact_seep 1
execute if score @s rpg_pact_seep matches ..29 run return 0
scoreboard players set @s rpg_pact_seep 0
scoreboard players operation @s rpg_taint += @s rpg_pact_lv
execute if entity @s[scores={rpg_pact=7}] run scoreboard players operation @s rpg_taint += @s rpg_pact_lv
