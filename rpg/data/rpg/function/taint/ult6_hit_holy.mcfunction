# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
execute at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^2.5
effect give @s minecraft:slowness 3 4 true
effect give @s minecraft:weakness 3 2 true
effect give @s minecraft:nausea 4 0 true
damage @s 17 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
