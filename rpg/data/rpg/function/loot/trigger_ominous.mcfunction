# 开箱：落哪一档
execute store result score #loot loot run random value 1..100
execute if score #loot loot matches 1..1 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:1b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 2..7 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:2b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 8..27 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:3b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 28..67 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:4b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 68..97 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:5b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 98..100 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:6b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
scoreboard players reset * loot
