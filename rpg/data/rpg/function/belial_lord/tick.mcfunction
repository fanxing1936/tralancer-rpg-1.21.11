# 贝利尔每刻入口。任何召唤路径落地的第 6 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.bll,scores={rpg_dm_lord=6},limit=1] as @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.bll,scores={rpg_dm_lord=6}] at @s run function rpg:belial_lord/dress
execute if entity @e[type=minecraft:vindicator,tag=rpg.bll,limit=1] as @e[type=minecraft:vindicator,tag=rpg.bll] at @s run function rpg:belial_lord/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.bll.part,predicate=!rpg:belial_lord/riding,limit=1] run function rpg:belial_lord/orphans
