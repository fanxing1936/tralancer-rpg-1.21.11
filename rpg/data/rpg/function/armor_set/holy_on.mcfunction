# 神圣套：穿齐四件，每秒确认一次
execute if entity @s[tag=!rpg.set.holy] run playsound minecraft:item.armor.equip_netherite player @s ~ ~ ~ 1 0.8
tag @s add rpg.set.holy
execute unless predicate rpg:armor_set/regen run effect give @s minecraft:regeneration infinite 0 true
