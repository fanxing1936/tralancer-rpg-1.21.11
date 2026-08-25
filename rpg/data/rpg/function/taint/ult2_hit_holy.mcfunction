# 对方身上带着圣器：黑暗与失明落不下来，其余 debuff 减半。
execute at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^3
effect give @s minecraft:slowness 4 3 true
effect give @s minecraft:mining_fatigue 4 2 true
damage @s 17 minecraft:drown by @e[tag=rpg.dm.cast,limit=1]
