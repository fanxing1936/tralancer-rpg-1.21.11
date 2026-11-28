execute as @e[type=minecraft:villager,tag=rpg.tw.model.witch] at @s run function rpg:town_models/town_witch/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.model.witch.part,predicate=!rpg:town_models/town_witch/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.tw.model.witch.part,predicate=!rpg:town_models/town_witch/riding]
