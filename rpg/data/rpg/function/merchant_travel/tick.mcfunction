# 为既有和新放置的迷途商人补齐外观。
execute as @e[type=minecraft:villager,tag=rpg.mer.travel,tag=!rpg.mer.model.travel] at @s run function rpg:merchant_travel/dress
execute as @e[type=minecraft:villager,tag=rpg.mer.model.travel] at @s run function rpg:merchant_travel/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.mer.model.travel.part,predicate=!rpg:merchant_travel/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.mer.model.travel.part,predicate=!rpg:merchant_travel/riding]
