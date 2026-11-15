# 玛门每刻入口。任何召唤路径落地的第 7 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.mml,scores={rpg_dm_lord=7},limit=1] as @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.mml,scores={rpg_dm_lord=7}] at @s run function rpg:mammon_lord/dress
execute if entity @e[type=minecraft:vindicator,tag=rpg.mml,limit=1] as @e[type=minecraft:vindicator,tag=rpg.mml] at @s run function rpg:mammon_lord/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.mml.part,predicate=!rpg:mammon_lord/riding,limit=1] run function rpg:mammon_lord/orphans
