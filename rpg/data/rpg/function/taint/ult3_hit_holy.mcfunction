# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
effect give @s minecraft:wither 4 1 true
damage @s 20 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
particle soul ~ ~1 ~ 0.35 0.5 0.35 0.06 24 force
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
