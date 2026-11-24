scoreboard players operation @s rpg_fz_b = #b rpg_sef
attribute @s minecraft:max_health modifier remove rpg:vital
execute if score #b rpg_sef matches 1 run attribute @s minecraft:max_health modifier add rpg:vital -4 add_value
execute if score #b rpg_sef matches 2 run attribute @s minecraft:max_health modifier add rpg:vital -8 add_value
execute if score #b rpg_sef matches 3 run attribute @s minecraft:max_health modifier add rpg:vital -12 add_value
