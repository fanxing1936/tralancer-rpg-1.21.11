execute as @e at @s on attacker if entity @s[scores={potion=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{potion_tag:1b}}}}] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={potion=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{potion_tag:1b}}}}] run summon llama_spit ~ ~5 ~ {Motion:[0d,-1d]}
execute as @e at @s on attacker if entity @s[scores={potion=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{potion_tag:1b}}}}] run particle crit ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.5 30
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{potion_tag:1b}}}}] run particle dust_color_transition{from_color:[0.52,0.8,0.0],to_color:[0.98,0.98,0.98],scale:2} ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 3
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{potion_tag:1b}}}}] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
scoreboard players reset * random
scoreboard players reset * potion

