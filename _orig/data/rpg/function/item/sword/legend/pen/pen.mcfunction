execute as @e at @s on attacker if entity @s[scores={pen=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{pen_tag:1b}}}}] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={pen=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{pen_tag:1b}}}}] run particle squid_ink ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.2 30
execute as @a[scores={pen_=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{pen_tag:1b}}}}] at @s on attacker at @s run particle cloud ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 30
execute as @a[scores={pen_=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{pen_tag:1b}}}}] at @s on attacker at @s run damage @s 3 minecraft:out_of_world
execute as @a[scores={pen_=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{pen_tag:1b}}}}] at @s run effect give @s instant_health 1 0 true
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{pen_tag:1b}}}}] run particle enchant ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 1 3
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{pen_tag:1b}}}}] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
scoreboard players reset * random
scoreboard players reset * pen
scoreboard players reset * pen_

