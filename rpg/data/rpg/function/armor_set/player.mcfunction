# 穿齐四件同一 armor_set 才算成套；脱下任一件，下一秒撤掉加成。

# 圣卫残甲
execute if items entity @s armor.head *[minecraft:custom_data~{armor_set:"sentinel"}] if items entity @s armor.chest *[minecraft:custom_data~{armor_set:"sentinel"}] if items entity @s armor.legs *[minecraft:custom_data~{armor_set:"sentinel"}] if items entity @s armor.feet *[minecraft:custom_data~{armor_set:"sentinel"}] run tag @s add rpg.set.sentinel.now
execute if entity @s[tag=rpg.set.sentinel.now] run function rpg:armor_set/sentinel_on
execute if entity @s[tag=rpg.set.sentinel,tag=!rpg.set.sentinel.now] run function rpg:armor_set/sentinel_off
tag @s remove rpg.set.sentinel.now

# 驱魔人法衣
execute if items entity @s armor.head *[minecraft:custom_data~{armor_set:"exorcist"}] if items entity @s armor.chest *[minecraft:custom_data~{armor_set:"exorcist"}] if items entity @s armor.legs *[minecraft:custom_data~{armor_set:"exorcist"}] if items entity @s armor.feet *[minecraft:custom_data~{armor_set:"exorcist"}] run tag @s add rpg.set.exorcist.now
execute if entity @s[tag=rpg.set.exorcist.now] run function rpg:armor_set/exorcist_on
execute if entity @s[tag=rpg.set.exorcist,tag=!rpg.set.exorcist.now] run function rpg:armor_set/exorcist_off
tag @s remove rpg.set.exorcist.now

# 渊海套
execute if items entity @s armor.head *[minecraft:custom_data~{armor_set:"abyss"}] if items entity @s armor.chest *[minecraft:custom_data~{armor_set:"abyss"}] if items entity @s armor.legs *[minecraft:custom_data~{armor_set:"abyss"}] if items entity @s armor.feet *[minecraft:custom_data~{armor_set:"abyss"}] run tag @s add rpg.set.abyss.now
execute if entity @s[tag=rpg.set.abyss.now] run function rpg:armor_set/abyss_on
execute if entity @s[tag=rpg.set.abyss,tag=!rpg.set.abyss.now] run function rpg:armor_set/abyss_off
tag @s remove rpg.set.abyss.now

# 恶魔枷甲
execute if items entity @s armor.head *[minecraft:custom_data~{armor_set:"demon"}] if items entity @s armor.chest *[minecraft:custom_data~{armor_set:"demon"}] if items entity @s armor.legs *[minecraft:custom_data~{armor_set:"demon"}] if items entity @s armor.feet *[minecraft:custom_data~{armor_set:"demon"}] run tag @s add rpg.set.demon.now
execute if entity @s[tag=rpg.set.demon.now] run function rpg:armor_set/demon_on
execute if entity @s[tag=rpg.set.demon,tag=!rpg.set.demon.now] run function rpg:armor_set/demon_off
tag @s remove rpg.set.demon.now

# 神圣套
execute if items entity @s armor.head *[minecraft:custom_data~{armor_set:"holy"}] if items entity @s armor.chest *[minecraft:custom_data~{armor_set:"holy"}] if items entity @s armor.legs *[minecraft:custom_data~{armor_set:"holy"}] if items entity @s armor.feet *[minecraft:custom_data~{armor_set:"holy"}] run tag @s add rpg.set.holy.now
execute if entity @s[tag=rpg.set.holy.now] run function rpg:armor_set/holy_on
execute if entity @s[tag=rpg.set.holy,tag=!rpg.set.holy.now] run function rpg:armor_set/holy_off
tag @s remove rpg.set.holy.now
