loot give @s loot rpg:world/sp/star
loot give @s loot rpg:world/raw/diamond
execute if predicate {condition:"minecraft:random_chance",chance:0.5} run loot give @s loot rpg:world/sp/star
function rpg:quest/start_5
function rpg:quest/hook/star
