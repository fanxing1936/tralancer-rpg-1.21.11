execute as @e at @s on attacker if entity @s[scores={holy=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{holy_weapon_tag:1b}}}}] run particle dust{color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={holy=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{holy_weapon_tag:1b}}}}] run particle end_rod ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30

execute as @e at @s on attacker if entity @s[scores={holy=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{holy_weapon_tag:2b}}}}] run particle firework ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={holy=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{holy_weapon_tag:2b}}}}] run particle end_rod ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30

execute as @e at @s on attacker if entity @s[scores={holy=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{holy_weapon_tag:3b}}}}] run particle totem_of_undying ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={holy=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{holy_weapon_tag:3b}}}}] run particle dust{color:[1.0,0.78,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30


scoreboard players reset * holy
