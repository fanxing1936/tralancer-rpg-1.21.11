execute as @e[type=minecraft:villager,tag=rpg.tw.model.watchman] at @s run function rpg:town_models/town_watchman/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.model.watchman.part,predicate=!rpg:town_models/town_watchman/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.tw.model.watchman.part,predicate=!rpg:town_models/town_watchman/riding]
