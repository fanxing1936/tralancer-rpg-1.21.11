execute as @e at @s if entity @s[scores={absorption=0..},nbt={Inventory:[{components:{"minecraft:custom_data":{absorption_tag:1b}},Slot:102b}]}] store result score @s random run random value 1..5
execute as @e at @s if entity @s[scores={absorption=0..,random=1},nbt={Inventory:[{components:{"minecraft:custom_data":{absorption_tag:1b}},Slot:102b}]}] run effect give @s absorption 5 1 true
execute as @e at @s if entity @s[scores={absorption=0..,random=1},nbt={Inventory:[{components:{"minecraft:custom_data":{absorption_tag:1b}},Slot:102b}]}] at @s run particle dust_color_transition{from_color:[1.0,0.92,0.0],to_color:[0.5,1.0,0.0],scale:1} ~0.25 ~1.5 ~0.25 -0.5 -0.5 -0.5 1 100
scoreboard players reset * random
scoreboard players reset * absorption

execute as @e at @s if entity @s[scores={boom=1..3},nbt={Inventory:[{components:{"minecraft:custom_data":{boom_tag:1b}},Slot:102b}]}] run summon minecraft:creeper ~ ~ ~ {"ExplosionRadius":5,"Fuse":0}
execute as @e at @s if entity @s[scores={boom=1..3},nbt={Inventory:[{components:{"minecraft:custom_data":{boom_tag:1b}},Slot:102b}]}] at @s run particle explosion ~1 ~1.5 ~1 -2 -2 -2 1 50 force
execute as @e at @s if entity @s[scores={boom=1..3},nbt={Inventory:[{components:{"minecraft:custom_data":{boom_tag:1b}},Slot:102b}]}] at @s run kill 

execute as @e at @s if entity @s[scores={health=0..3},nbt={Inventory:[{components:{"minecraft:custom_data":{health_tag:1b}},Slot:102b}]}] run effect give @s strength 5 2 true
execute as @e at @s if entity @s[scores={health=0..3},nbt={Inventory:[{components:{"minecraft:custom_data":{health_tag:1b}},Slot:102b}]}] at @s run particle dust_color_transition{from_color:[0.9,0.66,0.0],to_color:[1.0,0.58,0.0],scale:1} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 10

