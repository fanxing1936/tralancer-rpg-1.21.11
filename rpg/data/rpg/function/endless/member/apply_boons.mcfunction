function rpg:endless/member/clear_boons
execute if score @s rpg_end_vital matches 1..2 run attribute @s minecraft:max_health modifier add rpg:endless/vital_health 4 add_value
execute if score @s rpg_end_vital matches 3..4 run attribute @s minecraft:max_health modifier add rpg:endless/vital_health 8 add_value
execute if score @s rpg_end_vital matches 3..4 run attribute @s minecraft:armor modifier add rpg:endless/vital_armor 2 add_value
execute if score @s rpg_end_vital matches 5..6 run attribute @s minecraft:max_health modifier add rpg:endless/vital_health 12 add_value
execute if score @s rpg_end_vital matches 5..6 run attribute @s minecraft:armor modifier add rpg:endless/vital_armor 4 add_value
execute if score @s rpg_end_vital matches 7.. run attribute @s minecraft:max_health modifier add rpg:endless/vital_health 16 add_value
execute if score @s rpg_end_vital matches 7.. run attribute @s minecraft:armor modifier add rpg:endless/vital_armor 6 add_value
execute if score @s rpg_end_vital matches 7.. run attribute @s minecraft:knockback_resistance modifier add rpg:endless/vital_anchor 0.1 add_value
execute if score @s rpg_end_power matches 1..2 run attribute @s minecraft:attack_damage modifier add rpg:endless/power_damage 1 add_value
execute if score @s rpg_end_power matches 3..4 run attribute @s minecraft:attack_damage modifier add rpg:endless/power_damage 2 add_value
execute if score @s rpg_end_power matches 3..4 run attribute @s minecraft:movement_speed modifier add rpg:endless/power_speed 0.02 add_value
execute if score @s rpg_end_power matches 5..6 run attribute @s minecraft:attack_damage modifier add rpg:endless/power_damage 4 add_value
execute if score @s rpg_end_power matches 5..6 run attribute @s minecraft:movement_speed modifier add rpg:endless/power_speed 0.04 add_value
execute if score @s rpg_end_power matches 7.. run attribute @s minecraft:attack_damage modifier add rpg:endless/power_damage 6 add_value
execute if score @s rpg_end_power matches 7.. run attribute @s minecraft:movement_speed modifier add rpg:endless/power_speed 0.06 add_value
