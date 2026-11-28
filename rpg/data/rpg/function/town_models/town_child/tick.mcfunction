execute as @e[type=minecraft:villager,tag=rpg.tw.model.child] at @s run function rpg:town_models/town_child/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.model.child.part,predicate=!rpg:town_models/town_child/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.tw.model.child.part,predicate=!rpg:town_models/town_child/riding]
