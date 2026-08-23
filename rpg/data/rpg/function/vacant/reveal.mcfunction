# 被圣器照住。平时它和普通村民毫无分别，此刻藏不住了 ——
# 而照得越久，壳越撑不住。
effect give @s minecraft:glowing 2 0 true
particle sculk_soul ~ ~1.4 ~ 0.2 0.3 0.2 0.01 2
scoreboard players add @s rpg_vac_x 1
execute if entity @s[scores={rpg_vac_x=60..},tag=!rpg.vac.torn] run function rpg:vacant/tear
