# 天使士兵每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.pr.w.angel,tag=!rpg.pran,limit=1] as @e[tag=rpg.pr.w.angel,tag=!rpg.pran] at @s run function rpg:prologue_angel/dress
execute if entity @e[tag=rpg.pran,limit=1] as @e[tag=rpg.pran] at @s run function rpg:prologue_angel/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.pran.part,predicate=!rpg:prologue_angel/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.pran.part,predicate=!rpg:prologue_angel/riding]
