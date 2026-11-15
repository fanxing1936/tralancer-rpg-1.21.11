# 大卫的幽灵每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[type=minecraft:vindicator,tag=rpg.jqd,tag=!rpg.jqdm,limit=1] as @e[type=minecraft:vindicator,tag=rpg.jqd,tag=!rpg.jqdm] at @s run function rpg:david/dress
execute if entity @e[type=minecraft:vindicator,tag=rpg.jqdm,limit=1] as @e[type=minecraft:vindicator,tag=rpg.jqdm] at @s run function rpg:david/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.jqdm.part,predicate=!rpg:david/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.jqdm.part,predicate=!rpg:david/riding]
