# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
effect give @s minecraft:mining_fatigue 4 3 true
effect give @s minecraft:wither 2 0 true
damage @s 5 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
