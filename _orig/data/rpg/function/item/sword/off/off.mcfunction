execute as @e at @s on attacker if entity @s[scores={deep=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{deep_tag:1b}}}}] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={deep=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{deep_tag:1b}}}}] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 50
execute as @e at @s on attacker if entity @s[scores={deep=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{deep_tag:1b}}}}] run effect give @e[limit=1,sort=nearest] minecraft:darkness 3 1 true
scoreboard players reset * random
scoreboard players reset * deep

execute as @e at @s on attacker if entity @s[scores={ink=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{ink_tag:1b}}}}] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={ink=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{ink_tag:1b}}}}] run particle glow_squid_ink ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute as @e at @s on attacker if entity @s[scores={ink=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{ink_tag:1b}}}}] run particle glow ~0.5 ~1.5 ~0.5 -1 -1 -1 1 50
scoreboard players reset * ink

execute as @e at @s on attacker if entity @s[scores={damage=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{damage_tag:1b}}}}] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={damage=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{damage_tag:1b}}}}] run particle dust_pillar{block_state:{Name:redstone_block}} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 100
execute as @e at @s on attacker if entity @s[scores={damage=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{damage_tag:1b}}}}] run effect give @s minecraft:instant_health 1 0 true
scoreboard players reset * random
scoreboard players reset * damage


execute as @e at @s on attacker if entity @s[scores={blow=0..},nbt={SelectedItem:{components:{"minecraft:custom_data":{blow_tag:1b}}}}] store result score @s random run random value 1..3
execute as @e at @s on attacker if entity @s[scores={blow=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{blow_tag:1b}}}}] run effect give @e[limit=1,sort=nearest] wither 5 10 true
execute as @e at @s on attacker if entity @s[scores={blow=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{blow_tag:1b}}}}] run particle end_rod ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 100
execute as @e at @s on attacker if entity @s[scores={blow=0..,random=1},nbt={SelectedItem:{components:{"minecraft:custom_data":{blow_tag:1b}}}}] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 1 100
scoreboard players reset * random
scoreboard players reset * blow