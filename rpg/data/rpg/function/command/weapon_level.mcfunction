execute as @s[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s store result score @s weapon_level run data get entity @s Item.components.minecraft:custom_data.level
execute as @s[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run scoreboard players add @s weapon_level 1
execute as @s[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount double 0.01 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount 102
execute as @s[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount double 0.0097 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount 100
execute as @s[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s store result entity @s Item.components.minecraft:custom_data.level int 1 run scoreboard players get @s weapon_level
