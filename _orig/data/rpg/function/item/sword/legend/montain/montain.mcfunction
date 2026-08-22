execute as @e at @s on attacker if entity @s[scores={montain=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{montain_tag:1b}}}}] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={montain=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{montain_tag:1b}}}}] run summon llama_spit ~ ~5 ~ {Motion:[0d,-1d]}
execute as @e at @s on attacker if entity @s[scores={montain=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{montain_tag:1b}}}}] run particle gust ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 5
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{montain_tag:1b}}}}] run particle dust_color_transition{from_color:[0.15,0.91,0.76],to_color:[0.9,0.63,0.0],scale:1} ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 3
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{montain_tag:1b}}}}] run particle dust_color_transition{from_color:[0.15,0.91,0.76],to_color:[0.9,0.63,0.0],scale:2} ~0.1 ~0.7 ~0.1 -0.2 -0.5 -0.2 0.1 5
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{montain_tag:1b}}}}] run particle dust_color_transition{from_color:[0.9,0.63,0.0],to_color:[0.15,0.91,0.76],scale:1} ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 2
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{montain_tag:1b}}}}] run damage @e[limit=1,sort=nearest] 1 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{montain_tag:1b}}}}] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
scoreboard players reset * random
scoreboard players reset * montain

execute as @a[nbt={SelectedItem:{components:{"minecraft:custom_data":{montain_tag:1b}}}}] at @s run particle dust_color_transition{from_color:[0.15,0.91,0.76],to_color:[0.9,0.63,0.0],scale:2} ~0.1 ~0.3 ~0.1 -0.2 -0.2 -0.2 0.1 2