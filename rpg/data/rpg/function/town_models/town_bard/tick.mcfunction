execute as @e[type=minecraft:villager,tag=rpg.tw.model.bard] at @s run function rpg:town_models/town_bard/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.model.bard.part,predicate=!rpg:town_models/town_bard/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.tw.model.bard.part,predicate=!rpg:town_models/town_bard/riding]
