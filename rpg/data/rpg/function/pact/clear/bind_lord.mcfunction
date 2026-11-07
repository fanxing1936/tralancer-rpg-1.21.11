scoreboard players operation @s rpg_pact_bid = #bid rpg_pact_bid
execute on passengers run scoreboard players operation @s rpg_pact_bid = #bid rpg_pact_bid
execute if score #lv rpg_pact matches 2 run attribute @s minecraft:armor modifier add rpg:pact/lord 6 add_value
execute if score #lv rpg_pact matches 2 run attribute @s minecraft:attack_damage modifier add rpg:pact/lord 4 add_value
execute if score #lv rpg_pact matches 3 run attribute @s minecraft:armor modifier add rpg:pact/lord 12 add_value
execute if score #lv rpg_pact matches 3 run attribute @s minecraft:attack_damage modifier add rpg:pact/lord 8 add_value
