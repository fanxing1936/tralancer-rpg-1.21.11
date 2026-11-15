# 萨麦尔每刻入口。任何召唤路径落地的第 5 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.sml,scores={rpg_dm_lord=5},limit=1] as @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.sml,scores={rpg_dm_lord=5}] at @s run function rpg:samael_lord/dress
execute if entity @e[type=minecraft:vindicator,tag=rpg.sml,limit=1] as @e[type=minecraft:vindicator,tag=rpg.sml] at @s run function rpg:samael_lord/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.sml.part,predicate=!rpg:samael_lord/riding,limit=1] run function rpg:samael_lord/orphans
