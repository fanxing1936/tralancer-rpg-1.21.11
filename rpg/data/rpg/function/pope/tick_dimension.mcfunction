# 当前维度：载体跟随、动画与音效；共用管线在末尾清理孤儿部件。
execute if entity @e[distance=0..,type=minecraft:vindicator,tag=rpg.pope,limit=1] as @e[distance=0..,type=minecraft:vindicator,tag=rpg.pope] at @s run function rpg:pope/follow
execute if entity @e[distance=0..,type=minecraft:item_display,tag=rpg.pope.part,predicate=!rpg:pope/riding,limit=1] run kill @e[distance=0..,type=minecraft:item_display,tag=rpg.pope.part,predicate=!rpg:pope/riding]
