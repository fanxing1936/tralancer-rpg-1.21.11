# 路西法（序章）每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.pr.w.lucifer,tag=!rpg.prlu,limit=1] as @e[tag=rpg.pr.w.lucifer,tag=!rpg.prlu] at @s run function rpg:prologue_lucifer/dress
execute if entity @e[tag=rpg.prlu,limit=1] as @e[tag=rpg.prlu] at @s run function rpg:prologue_lucifer/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.prlu.part,predicate=!rpg:prologue_lucifer/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.prlu.part,predicate=!rpg:prologue_lucifer/riding]
