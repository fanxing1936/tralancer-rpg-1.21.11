# 泥沼
execute if entity @s[type=minecraft:wither_skeleton] run return run tp @s ~ -200 ~
execute if entity @s[type=minecraft:blaze] run return run tp @s ~ -200 ~
execute if entity @s[type=minecraft:enderman] run return run tp @s ~ -200 ~
execute if entity @s[type=minecraft:vindicator] run return run tp @s ~ -200 ~
tag @s add rpg.pl.z1
attribute @s minecraft:max_health modifier add rpg:pl 0.5 add_multiplied_base
attribute @s minecraft:attack_damage modifier add rpg:pl 0.25 add_multiplied_base
attribute @s minecraft:movement_speed modifier add rpg:pl 0.08 add_multiplied_base
data modify entity @s Health set value 1024f
