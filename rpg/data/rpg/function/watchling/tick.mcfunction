# 守望者每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.mkw,tag=!rpg.mkwm,limit=1] as @e[tag=rpg.mkw,tag=!rpg.mkwm] at @s run function rpg:watchling/dress
execute if entity @e[tag=rpg.mkwm,limit=1] as @e[tag=rpg.mkwm] at @s run function rpg:watchling/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.mkwm.part,predicate=!rpg:watchling/riding,limit=1] run function rpg:watchling/orphans
