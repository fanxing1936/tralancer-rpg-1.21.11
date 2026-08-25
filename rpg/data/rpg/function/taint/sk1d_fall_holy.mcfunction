# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
effect give @s minecraft:levitation 1 1 true
effect give @s minecraft:weakness 2 1 true
damage @s 5 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
