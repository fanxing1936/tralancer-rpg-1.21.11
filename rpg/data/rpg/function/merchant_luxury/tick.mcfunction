# 为既有和新放置的奢侈品商人补齐外观。
execute as @e[type=minecraft:villager,tag=rpg.mer.luxury,tag=!rpg.mer.model.luxury] at @s run function rpg:merchant_luxury/dress
execute as @e[type=minecraft:villager,tag=rpg.mer.model.luxury] at @s run function rpg:merchant_luxury/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.mer.model.luxury.part,predicate=!rpg:merchant_luxury/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.mer.model.luxury.part,predicate=!rpg:merchant_luxury/riding]
