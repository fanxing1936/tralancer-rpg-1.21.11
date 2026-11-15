# 驱魔人法衣：穿齐四件，每秒确认一次
execute if entity @s[tag=!rpg.set.exorcist] run playsound minecraft:item.armor.equip_netherite player @s ~ ~ ~ 1 0.8
tag @s add rpg.set.exorcist
