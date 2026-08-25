scoreboard players set @s rpg_lt_migrate 1
scoreboard players set @s rpg_lt_covenant 0
clear @s minecraft:enchanted_book[minecraft:custom_data~{rpg_new_covenant:1b}]
loot give @s loot rpg:ritual/life_tree/old_covenant
scoreboard players set @s rpg_lt_claim 1
tellraw @s ["",{"text":"[秘仪] ","color":"#D596F2","bold":true,"italic":false},{"text":"先前的生命之树见证已重铸为","color":"gray","bold":false,"italic":false},{"text":"『旧约』","color":"#D4AF37","bold":true,"italic":false},{"text":"。","color":"gray","bold":false,"italic":false}]
