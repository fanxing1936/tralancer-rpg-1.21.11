# 重算两个槽的效果。
attribute @s minecraft:armor modifier remove rpg:pact/seal/1
attribute @s minecraft:armor modifier remove rpg:pact/seal/2
attribute @s minecraft:attack_damage modifier remove rpg:pact/seal/1
attribute @s minecraft:attack_damage modifier remove rpg:pact/seal/2
attribute @s minecraft:entity_interaction_range modifier remove rpg:pact/seal/1
attribute @s minecraft:entity_interaction_range modifier remove rpg:pact/seal/2
attribute @s minecraft:knockback_resistance modifier remove rpg:pact/seal/1
attribute @s minecraft:knockback_resistance modifier remove rpg:pact/seal/2
attribute @s minecraft:max_health modifier remove rpg:pact/seal/1
attribute @s minecraft:max_health modifier remove rpg:pact/seal/2
attribute @s minecraft:movement_speed modifier remove rpg:pact/seal/1
attribute @s minecraft:movement_speed modifier remove rpg:pact/seal/2
tag @s remove rpg.pact.s3
tag @s remove rpg.pact.s4
tag @s remove rpg.pact.s5
tag @s remove rpg.pact.onhit
execute unless score @s rpg_pact_s1 matches 1.. run scoreboard players set @s rpg_pact_s1 0
execute if score @s rpg_pact_s1 matches 1.. run function rpg:pact/seal/slot1
execute unless score @s rpg_pact_s2 matches 1.. run scoreboard players set @s rpg_pact_s2 0
execute if score @s rpg_pact_s2 matches 1.. run function rpg:pact/seal/slot2
