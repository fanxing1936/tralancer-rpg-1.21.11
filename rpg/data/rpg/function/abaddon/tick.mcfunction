# 亚巴顿每刻入口。任何召唤路径落地的第三柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.ab,scores={rpg_dm_lord=3},limit=1] as @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.ab,scores={rpg_dm_lord=3}] at @s run function rpg:abaddon/dress
execute if entity @e[type=minecraft:vindicator,tag=rpg.ab,limit=1] as @e[type=minecraft:vindicator,tag=rpg.ab] at @s run function rpg:abaddon/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.ab.part,predicate=!rpg:abaddon/riding,limit=1] run function rpg:abaddon/orphans
