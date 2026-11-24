advancement revoke @s only rpg:world/kill_rpg_hg
execute if predicate {condition:"minecraft:random_chance",chance:0.2} run loot give @s loot rpg:world/sp/bronze
function rpg:quest/start_3
function rpg:quest/hook/guard
