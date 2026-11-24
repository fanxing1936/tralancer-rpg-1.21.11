# 以目标村民执行；位置和朝向从载体读取。重复调用会重建本实体的外观。
execute unless entity @s[type=minecraft:villager] run return 0
execute at @s run function rpg:merchant_mystery/dress_at
