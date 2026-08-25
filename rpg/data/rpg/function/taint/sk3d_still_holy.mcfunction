# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
effect give @s minecraft:slowness 1 255 true
effect give @s minecraft:weakness 3 2 true
damage @s 4 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
