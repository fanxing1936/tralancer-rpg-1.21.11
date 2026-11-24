# 米迦勒（序章）每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.pr.w.michael,tag=!rpg.prmi,limit=1] as @e[tag=rpg.pr.w.michael,tag=!rpg.prmi] at @s run function rpg:prologue_michael/dress
execute if entity @e[tag=rpg.prmi,limit=1] as @e[tag=rpg.prmi] at @s run function rpg:prologue_michael/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.prmi.part,predicate=!rpg:prologue_michael/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.prmi.part,predicate=!rpg:prologue_michael/riding]
