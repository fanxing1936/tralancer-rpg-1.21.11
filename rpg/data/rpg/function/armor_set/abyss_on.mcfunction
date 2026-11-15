# 渊海套：穿齐四件，每秒确认一次
execute if entity @s[tag=!rpg.set.abyss] run playsound minecraft:item.armor.equip_netherite player @s ~ ~ ~ 1 0.8
tag @s add rpg.set.abyss
execute if block ~ ~ ~ minecraft:water run tag @s add rpg.set.abyss.wet
execute if block ~ ~1 ~ minecraft:water run tag @s add rpg.set.abyss.wet
execute if entity @s[tag=rpg.set.abyss.wet] run effect give @s minecraft:conduit_power 3 0 true
execute if entity @s[tag=rpg.set.abyss.wet] run effect give @s minecraft:dolphins_grace 3 0 true
tag @s remove rpg.set.abyss.wet
