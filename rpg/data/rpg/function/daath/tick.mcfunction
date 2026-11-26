# 影每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.dtwear,tag=!rpg.dtm,limit=1] as @e[tag=rpg.dtwear,tag=!rpg.dtm] at @s run function rpg:daath/dress
execute if entity @e[tag=rpg.dtm,limit=1] as @e[tag=rpg.dtm] at @s run function rpg:daath/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.dtm.part,predicate=!rpg:daath/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.dtm.part,predicate=!rpg:daath/riding]
