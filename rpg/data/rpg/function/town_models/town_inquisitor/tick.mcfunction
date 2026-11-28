execute as @e[type=minecraft:vindicator,tag=rpg.tw.model.inquisitor] at @s run function rpg:town_models/town_inquisitor/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.model.inquisitor.part,predicate=!rpg:town_models/town_inquisitor/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.tw.model.inquisitor.part,predicate=!rpg:town_models/town_inquisitor/riding]
