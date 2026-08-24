# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
effect give @s minecraft:hunger 7 3 true
effect give @s minecraft:weakness 4 1 true
damage @s 4 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 1 true
