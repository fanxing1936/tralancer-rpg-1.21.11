execute store result score @s player_attack_damage run attribute @s minecraft:attack_damage get 100
execute store result score @s player_attack_speed run attribute @s minecraft:attack_speed get 100
execute store result score @s player_armor run attribute @s minecraft:armor get 100
execute store result score @s player_armor_toughness run attribute @s minecraft:armor_toughness get 100
execute store result score @s player_attack_damage_ run attribute @s minecraft:attack_damage get
execute store result score @s player_attack_speed_ run attribute @s minecraft:attack_speed get
execute store result score @s player_armor_ run attribute @s minecraft:armor get
execute store result score @s player_armor_toughness_ run attribute @s minecraft:armor_toughness get
scoreboard players operation @s player_attack_speed %= 100 player_attack_speed
scoreboard players operation @s player_attack_damage %= 100 player_attack_damage
scoreboard players operation @s player_armor %= 100 player_armor
scoreboard players operation @s player_armor_toughness %= 100 player_armor_toughness
execute if entity @s[tag=rpg.h.sword_tag1] run item modify entity @s weapon.mainhand rpg:command/sword_value
execute if entity @s[tag=rpg.e.head_chestplate_tag1] run item modify entity @s armor.head rpg:command/chestplate_value
execute if entity @s[tag=rpg.e.chest_chestplate_tag1] run item modify entity @s armor.chest rpg:command/chestplate_value
execute if entity @s[tag=rpg.e.legs_chestplate_tag1] run item modify entity @s armor.legs rpg:command/chestplate_value
execute if entity @s[tag=rpg.e.feet_chestplate_tag1] run item modify entity @s armor.feet rpg:command/chestplate_value
execute if entity @s[tag=rpg.h.player_tag1] run item modify entity @s weapon.mainhand rpg:command/player_value
