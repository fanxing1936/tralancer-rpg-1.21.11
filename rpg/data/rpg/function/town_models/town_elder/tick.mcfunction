execute as @e[type=minecraft:villager,tag=rpg.tw.model.elder] at @s run function rpg:town_models/town_elder/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.model.elder.part,predicate=!rpg:town_models/town_elder/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.tw.model.elder.part,predicate=!rpg:town_models/town_elder/riding]
