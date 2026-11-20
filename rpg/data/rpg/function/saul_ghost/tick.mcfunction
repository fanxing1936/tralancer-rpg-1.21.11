# 老战友的幻影每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[type=minecraft:vindicator,tag=rpg.slg,tag=!rpg.slgm,limit=1] as @e[type=minecraft:vindicator,tag=rpg.slg,tag=!rpg.slgm] at @s run function rpg:saul_ghost/dress
execute if entity @e[type=minecraft:vindicator,tag=rpg.slgm,limit=1] as @e[type=minecraft:vindicator,tag=rpg.slgm] at @s run function rpg:saul_ghost/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.slgm.part,predicate=!rpg:saul_ghost/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.slgm.part,predicate=!rpg:saul_ghost/riding]
