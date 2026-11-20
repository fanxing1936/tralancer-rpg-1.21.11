# 扫罗每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.slwear,tag=!rpg.slm,limit=1] as @e[tag=rpg.slwear,tag=!rpg.slm] at @s run function rpg:saul/dress
execute if entity @e[tag=rpg.slm,limit=1] as @e[tag=rpg.slm] at @s run function rpg:saul/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.slm.part,predicate=!rpg:saul/riding,limit=1] run function rpg:saul/orphans
