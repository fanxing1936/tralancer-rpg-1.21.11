execute as @e[type=minecraft:zombie,tag=rpg.tw.model.hollow_big] at @s run function rpg:town_models/town_hollow_big/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.model.hollow_big.part,predicate=!rpg:town_models/town_hollow_big/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.tw.model.hollow_big.part,predicate=!rpg:town_models/town_hollow_big/riding]
