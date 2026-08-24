# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
effect give @s minecraft:slowness 4 3 true
effect give @s minecraft:mining_fatigue 4 2 true
effect give @s minecraft:weakness 4 1 true
damage @s 2 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
