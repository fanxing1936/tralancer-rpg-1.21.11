execute as @e[type=minecraft:villager,tag=rpg.tw.model.priest] at @s run function rpg:town_models/town_priest/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.model.priest.part,predicate=!rpg:town_models/town_priest/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.tw.model.priest.part,predicate=!rpg:town_models/town_priest/riding]
