# 信条：力的回复翻倍（圣力每秒再 +2，魔力每秒再 +3）
execute if score @s rpg_force matches 1 run scoreboard players add @s rpg_mana 2
execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana 2
execute if score @s rpg_force matches 2 run scoreboard players add @s rpg_mana 3
execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana2 3
particle minecraft:wax_on ~ ~2.2 ~ 0.2 0.1 0.2 0 2
