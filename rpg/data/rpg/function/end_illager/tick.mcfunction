# 术士每刻入口；圣光弹不跟载体走，单独推进。
execute if entity @e[type=minecraft:vindicator,tag=rpg.ei,limit=1] as @e[type=minecraft:vindicator,tag=rpg.ei] at @s run function rpg:end_illager/follow
execute if entity @e[type=minecraft:text_display,tag=rpg.ei.bolt,limit=1] as @e[type=minecraft:text_display,tag=rpg.ei.bolt] at @s run function rpg:end_illager/ai/bolt
execute if entity @e[type=minecraft:item_display,tag=rpg.ei.part,predicate=!rpg:end_illager/riding,limit=1] run function rpg:end_illager/orphans
