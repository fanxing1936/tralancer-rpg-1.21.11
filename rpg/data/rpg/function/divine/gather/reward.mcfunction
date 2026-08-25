clear @s minecraft:enchanted_book[minecraft:custom_data~{rpg_divine_old:1b}]
execute if score @s rpg_lt_divine matches 1 run scoreboard players set @s rpg_lt_divine 0
tag @s remove rpg.divine.old
loot give @s loot rpg:ritual/life_tree/new_covenant
