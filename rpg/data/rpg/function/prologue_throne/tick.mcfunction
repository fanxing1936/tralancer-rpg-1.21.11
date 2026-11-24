# 座天使每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.pr.w.throne,tag=!rpg.prth,limit=1] as @e[tag=rpg.pr.w.throne,tag=!rpg.prth] at @s run function rpg:prologue_throne/dress
execute if entity @e[tag=rpg.prth,limit=1] as @e[tag=rpg.prth] at @s run function rpg:prologue_throne/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.prth.part,predicate=!rpg:prologue_throne/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.prth.part,predicate=!rpg:prologue_throne/riding]
