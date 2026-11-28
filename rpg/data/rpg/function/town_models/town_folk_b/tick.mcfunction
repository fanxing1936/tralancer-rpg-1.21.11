execute as @e[type=minecraft:villager,tag=rpg.tw.model.folk_b] at @s run function rpg:town_models/town_folk_b/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.model.folk_b.part,predicate=!rpg:town_models/town_folk_b/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.tw.model.folk_b.part,predicate=!rpg:town_models/town_folk_b/riding]
