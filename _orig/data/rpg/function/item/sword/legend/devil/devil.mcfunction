execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{devil_weapon_tag:1b}}}}] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{devil_weapon_tag:1b}}}}] run particle soul_fire_flame ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30

execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{devil_weapon_tag:2b}}}}] run particle trial_spawner_detection_ominous ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{devil_weapon_tag:2b}}}}] run particle sonic_boom ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 5


execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{devil_weapon_tag:3b}}}}] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{devil_weapon_tag:3b}}}}] run particle trial_omen ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30


scoreboard players reset * devil_weapon
