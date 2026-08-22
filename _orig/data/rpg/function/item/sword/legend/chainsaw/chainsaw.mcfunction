execute as @e at @s on attacker if entity @s[scores={chainsaw=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{chainsaw_tag:1b}}}}] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={chainsaw=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{chainsaw_tag:1b}}}}] run summon evoker_fangs ~ ~ ~ {Motion:[0d,0.2d],Health:10,Glowing:1b,attributes:[{id:"generic.scale",base:3f},{id:"generic.max_health",base:10f}]}
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{chainsaw_tag:1b}}}}] run particle trial_spawner_detection ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 5
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{chainsaw_tag:1b}}}}] run damage @e[limit=1,sort=nearest] 1 minecraft:player_attack
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{chainsaw_tag:1b}}}}] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
scoreboard players reset * random
scoreboard players reset * chainsaw