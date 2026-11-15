# 恶魔枷甲：穿齐四件，每秒确认一次
execute if entity @s[tag=!rpg.set.demon] run playsound minecraft:item.armor.equip_netherite player @s ~ ~ ~ 1 0.8
tag @s add rpg.set.demon
execute store result score @s rpg_as_hp run data get entity @s Health 100
execute store result score @s rpg_as_max run attribute @s minecraft:max_health get 50
execute if score @s rpg_as_hp < @s rpg_as_max run effect give @s minecraft:strength 3 1 true
execute if score @s rpg_as_hp < @s rpg_as_max run effect give @s minecraft:resistance 3 0 true
