# 别西卜每刻入口。任何召唤路径落地的第四柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.bz,scores={rpg_dm_lord=4},limit=1] as @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.bz,scores={rpg_dm_lord=4}] at @s run function rpg:beelzebub/dress
execute if entity @e[type=minecraft:vindicator,tag=rpg.bz,limit=1] as @e[type=minecraft:vindicator,tag=rpg.bz] at @s run function rpg:beelzebub/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.bz.part,predicate=!rpg:beelzebub/riding,limit=1] run function rpg:beelzebub/orphans
