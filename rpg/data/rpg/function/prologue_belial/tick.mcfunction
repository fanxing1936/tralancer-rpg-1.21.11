# 贝利尔（序章）每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.pr.w.belial,tag=!rpg.prbl,limit=1] as @e[tag=rpg.pr.w.belial,tag=!rpg.prbl] at @s run function rpg:prologue_belial/dress
execute if entity @e[tag=rpg.prbl,limit=1] as @e[tag=rpg.prbl] at @s run function rpg:prologue_belial/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.prbl.part,predicate=!rpg:prologue_belial/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.prbl.part,predicate=!rpg:prologue_belial/riding]
