execute store result score #loot loot run random value 1..100
execute if score #loot loot matches 1 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:1b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 2..3 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:2b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 4..5 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:8b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 6..12 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:3b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 13..19 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:4b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 20..25 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:7b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 26..100 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:5b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
scoreboard players reset * loot
