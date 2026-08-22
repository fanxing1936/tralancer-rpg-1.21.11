execute as @e at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] store result score @e[limit=1,sort=nearest] random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run damage @e[limit=1,sort=nearest] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run effect give @e[distance=0..2] wither 5 1 true
execute as @e at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run particle sculk_soul ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50
execute as @e at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run particle trial_spawner_detection_ominous ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50
execute as @e[scores={random=1}] at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run data merge entity @e[limit=1,sort=nearest] {Motion:[0.8d,0.8d,0.8d]}
execute as @e[scores={random=2}] at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run data merge entity @e[limit=1,sort=nearest] {Motion:[-0.8d,0.8d,0.8d]}
execute as @e[scores={random=3}] at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run data merge entity @e[limit=1,sort=nearest] {Motion:[0.8d,0.8d,-0.8d]}
execute as @e[scores={random=4}] at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run data merge entity @e[limit=1,sort=nearest] {Motion:[-0.8d,0.8d,-0.8d]}
execute as @e[scores={random=5}] at @s on attacker if entity @s[scores={soul=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{soul_tag:1b}}}}] run data merge entity @e[limit=1,sort=nearest] {Motion:[0d,0.8d,0d]}
scoreboard players reset * soul

