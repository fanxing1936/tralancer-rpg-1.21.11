# 为既有和新放置的神秘商人补齐外观。
execute as @e[type=minecraft:villager,tag=rpg.mer.mystery,tag=!rpg.mer.model.mystery] at @s run function rpg:merchant_mystery/dress
execute as @e[type=minecraft:villager,tag=rpg.mer.model.mystery] at @s run function rpg:merchant_mystery/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.mer.model.mystery.part,predicate=!rpg:merchant_mystery/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.mer.model.mystery.part,predicate=!rpg:merchant_mystery/riding]
