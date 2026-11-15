# 雅克每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.jqwear,tag=!rpg.jqm,limit=1] as @e[tag=rpg.jqwear,tag=!rpg.jqm] at @s run function rpg:jacques/dress
execute if entity @e[tag=rpg.jqm,limit=1] as @e[tag=rpg.jqm] at @s run function rpg:jacques/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.jqm.part,predicate=!rpg:jacques/riding,limit=1] run function rpg:jacques/orphans
