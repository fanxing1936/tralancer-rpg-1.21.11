# 开箱：落哪一档
execute store result score #loot loot run random value 1..100
execute if score #loot loot matches 1..1 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:1b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 2..5 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:2b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 6..20 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:3b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 21..50 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:4b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
execute if score #loot loot matches 51..100 run summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:5b}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}
scoreboard players reset * loot
