# 利维坦每刻入口。任何召唤路径落地的第二柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.lv,scores={rpg_dm_lord=2},limit=1] as @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.lv,scores={rpg_dm_lord=2}] at @s run function rpg:leviathan/dress
execute if entity @e[type=minecraft:vindicator,tag=rpg.lv,limit=1] as @e[type=minecraft:vindicator,tag=rpg.lv] at @s run function rpg:leviathan/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.lv.part,predicate=!rpg:leviathan/riding,limit=1] run function rpg:leviathan/orphans
