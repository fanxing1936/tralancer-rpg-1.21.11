scoreboard players operation @s player_level_ = @s player_level
attribute @s minecraft:max_health modifier remove 64
attribute @s minecraft:max_health modifier remove 32
attribute @s minecraft:max_health modifier remove 16
attribute @s minecraft:max_health modifier remove 8
attribute @s minecraft:max_health modifier remove 4
attribute @s minecraft:max_health modifier remove 2
attribute @s minecraft:max_health modifier remove 1
attribute @s minecraft:max_health modifier remove 0
execute if score @s player_level_ > 64 player_level_ run attribute @s minecraft:max_health modifier add 64 64 add_value
execute if score @s player_level_ > 64 player_level_ run scoreboard players operation @s player_level_ -= 64 player_level_
execute if score @s player_level_ <= 64 player_level_ if score @s player_level_ > 32 player_level_ run attribute @s minecraft:max_health modifier add 32 32 add_value
execute if score @s player_level_ <= 64 player_level_ if score @s player_level_ > 32 player_level_ run scoreboard players operation @s player_level_ -= 32 player_level_
execute if score @s player_level_ <= 32 player_level_ if score @s player_level_ > 16 player_level_ run attribute @s minecraft:max_health modifier add 16 16 add_value
execute if score @s player_level_ <= 32 player_level_ if score @s player_level_ > 16 player_level_ run scoreboard players operation @s player_level_ -= 16 player_level_
execute if score @s player_level_ <= 16 player_level_ if score @s player_level_ > 8 player_level_ run attribute @s minecraft:max_health modifier add 8 8 add_value
execute if score @s player_level_ <= 16 player_level_ if score @s player_level_ > 8 player_level_ run scoreboard players operation @s player_level_ -= 8 player_level_
execute if score @s player_level_ <= 8 player_level_ if score @s player_level_ > 4 player_level_ run attribute @s minecraft:max_health modifier add 4 4 add_value
execute if score @s player_level_ <= 8 player_level_ if score @s player_level_ > 4 player_level_ run scoreboard players operation @s player_level_ -= 4 player_level_
execute if score @s player_level_ <= 4 player_level_ if score @s player_level_ > 2 player_level_ run attribute @s minecraft:max_health modifier add 2 2 add_value
execute if score @s player_level_ <= 4 player_level_ if score @s player_level_ > 2 player_level_ run scoreboard players operation @s player_level_ -= 2 player_level_
execute if score @s player_level_ <= 2 player_level_ if score @s player_level_ > 1 player_level_ run attribute @s minecraft:max_health modifier add 1 1 add_value
execute if score @s player_level_ <= 2 player_level_ if score @s player_level_ > 1 player_level_ run scoreboard players operation @s player_level_ -= 1 player_level_
execute if score @s player_level_ = 1 player_level_ run attribute @s minecraft:max_health modifier add 0 0.5 add_value
execute if score @s player_level_ = 1 player_level_ run scoreboard players operation @s player_level_ -= 1 player_level_
scoreboard players operation @s rpg_hp_level = @s player_level
