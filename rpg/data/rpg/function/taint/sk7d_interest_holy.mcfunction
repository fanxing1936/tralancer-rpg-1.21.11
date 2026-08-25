# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
xp add @s -15 points
effect give @s minecraft:weakness 3 1 true
damage @s 6 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
