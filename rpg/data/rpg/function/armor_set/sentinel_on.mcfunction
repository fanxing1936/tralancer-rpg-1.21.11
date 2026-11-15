# 圣卫残甲：穿齐四件，每秒确认一次
execute if entity @s[tag=!rpg.set.sentinel] run playsound minecraft:item.armor.equip_netherite player @s ~ ~ ~ 1 0.8
tag @s add rpg.set.sentinel
attribute @s minecraft:armor_toughness modifier remove rpg:armor_set/sentinel
attribute @s minecraft:armor_toughness modifier add rpg:armor_set/sentinel 4 add_value
attribute @s minecraft:knockback_resistance modifier remove rpg:armor_set/sentinel
attribute @s minecraft:knockback_resistance modifier add rpg:armor_set/sentinel 0.2 add_value
