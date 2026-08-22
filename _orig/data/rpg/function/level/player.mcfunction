execute as @a at @s if score @s level > @s player_level run particle minecraft:totem_of_undying ~-0.5 ~ ~-0.5 1 1 1 0.5 100
execute as @a at @s if score @s level > @s player_level run title @s title ["",{"text":"†","bold":true,"color":"white"},{"text":"LEVEL","bold":true,"color":"yellow"}," ",{"text":"UP","color":"gold","bold":true},{"text":"†","color":"white","bold":true}]
execute as @a at @s if score @s level > @s player_level run title @s subtitle ["♣当前",{"text":"等级","color":"gold","bold":true},"：",{"score":{"objective":"level","name":"@s"}}]
execute as @a at @s if score @s level > @s player_level run effect give @s minecraft:instant_health 1 10 true
execute as @a at @s if score @s level > @s player_level run scoreboard players operation @s player_level = @s level

execute as @a at @s run scoreboard players operation @s player_level_ = @s player_level
execute as @a at @s run attribute @s minecraft:generic.max_health modifier remove 64
execute as @a at @s run attribute @s minecraft:generic.max_health modifier remove 32
execute as @a at @s run attribute @s minecraft:generic.max_health modifier remove 16
execute as @a at @s run attribute @s minecraft:generic.max_health modifier remove 8
execute as @a at @s run attribute @s minecraft:generic.max_health modifier remove 4
execute as @a at @s run attribute @s minecraft:generic.max_health modifier remove 2
execute as @a at @s run attribute @s minecraft:generic.max_health modifier remove 1
execute as @a at @s run attribute @s minecraft:generic.max_health modifier remove 0
execute as @a at @s if score @s player_level_ > 64 player_level_ run attribute @s minecraft:generic.max_health modifier add 64 64 add_value
execute as @a at @s if score @s player_level_ > 64 player_level_ run scoreboard players operation @s player_level_ -= 64 player_level_
execute as @a at @s if score @s player_level_ <= 64 player_level_ if score @s player_level_ > 32 player_level_ run attribute @s minecraft:generic.max_health modifier add 32 32 add_value
execute as @a at @s if score @s player_level_ <= 64 player_level_ if score @s player_level_ > 32 player_level_ run scoreboard players operation @s player_level_ -= 32 player_level_
execute as @a at @s if score @s player_level_ <= 32 player_level_ if score @s player_level_ > 16 player_level_ run attribute @s minecraft:generic.max_health modifier add 16 16 add_value
execute as @a at @s if score @s player_level_ <= 32 player_level_ if score @s player_level_ > 16 player_level_ run scoreboard players operation @s player_level_ -= 16 player_level_
execute as @a at @s if score @s player_level_ <= 16 player_level_ if score @s player_level_ > 8 player_level_ run attribute @s minecraft:generic.max_health modifier add 8 8 add_value
execute as @a at @s if score @s player_level_ <= 16 player_level_ if score @s player_level_ > 8 player_level_ run scoreboard players operation @s player_level_ -= 8 player_level_
execute as @a at @s if score @s player_level_ <= 8 player_level_ if score @s player_level_ > 4 player_level_ run attribute @s minecraft:generic.max_health modifier add 4 4 add_value
execute as @a at @s if score @s player_level_ <= 8 player_level_ if score @s player_level_ > 4 player_level_ run scoreboard players operation @s player_level_ -= 4 player_level_
execute as @a at @s if score @s player_level_ <= 4 player_level_ if score @s player_level_ > 2 player_level_ run attribute @s minecraft:generic.max_health modifier add 2 2 add_value
execute as @a at @s if score @s player_level_ <= 4 player_level_ if score @s player_level_ > 2 player_level_ run scoreboard players operation @s player_level_ -= 2 player_level_
execute as @a at @s if score @s player_level_ <= 2 player_level_ if score @s player_level_ > 1 player_level_ run attribute @s minecraft:generic.max_health modifier add 1 1 add_value
execute as @a at @s if score @s player_level_ <= 2 player_level_ if score @s player_level_ > 1 player_level_ run scoreboard players operation @s player_level_ -= 1 player_level_
execute as @a at @s if score @s player_level_ = 1 player_level_ run attribute @s minecraft:generic.max_health modifier add 0 0.5 add_value
execute as @a at @s if score @s player_level_ = 1 player_level_ run scoreboard players operation @s player_level_ -= 1 player_level_
