# 甩出石子（as 雅克）：没有幽灵（调试）就不打断
execute unless entity @e[type=minecraft:vindicator,tag=rpg.jqd] run return 0
execute as @e[type=minecraft:vindicator,tag=rpg.jqd,limit=1] at @s run function rpg:jacques_boss/david/sling
