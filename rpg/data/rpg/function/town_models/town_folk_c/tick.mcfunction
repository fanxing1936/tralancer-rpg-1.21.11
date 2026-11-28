execute as @e[type=minecraft:villager,tag=rpg.tw.model.folk_c] at @s run function rpg:town_models/town_folk_c/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.model.folk_c.part,predicate=!rpg:town_models/town_folk_c/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.tw.model.folk_c.part,predicate=!rpg:town_models/town_folk_c/riding]
