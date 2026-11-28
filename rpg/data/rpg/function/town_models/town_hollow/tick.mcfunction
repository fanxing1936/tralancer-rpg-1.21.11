execute as @e[type=minecraft:zombie,tag=rpg.tw.model.hollow] at @s run function rpg:town_models/town_hollow/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.model.hollow.part,predicate=!rpg:town_models/town_hollow/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.tw.model.hollow.part,predicate=!rpg:town_models/town_hollow/riding]
