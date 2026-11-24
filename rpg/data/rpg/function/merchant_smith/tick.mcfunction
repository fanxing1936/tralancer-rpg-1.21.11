# 为既有和新放置的铁匠补齐外观。
execute as @e[type=minecraft:villager,tag=rpg.mer.smith,tag=!rpg.mer.model.smith] at @s run function rpg:merchant_smith/dress
execute as @e[type=minecraft:villager,tag=rpg.mer.model.smith] at @s run function rpg:merchant_smith/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.mer.model.smith.part,predicate=!rpg:merchant_smith/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.mer.model.smith.part,predicate=!rpg:merchant_smith/riding]
