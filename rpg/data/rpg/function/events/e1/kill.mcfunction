advancement revoke @s only rpg:events/tide_kill
execute unless score #tide rpg_ev matches 1 run return 0
execute if predicate {condition:"minecraft:random_chance",chance:0.06} run loot give @s loot rpg:forge/item/soul
