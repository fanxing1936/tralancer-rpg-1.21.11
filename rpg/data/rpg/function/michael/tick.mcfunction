# 米迦勒每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.mkwear,tag=!rpg.mkm,limit=1] as @e[tag=rpg.mkwear,tag=!rpg.mkm] at @s run function rpg:michael/dress
execute if entity @e[tag=rpg.mkm,limit=1] as @e[tag=rpg.mkm] at @s run function rpg:michael/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.mkm.part,predicate=!rpg:michael/riding,limit=1] run function rpg:michael/orphans
