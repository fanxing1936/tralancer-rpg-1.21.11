# 周围的掉落物直接被吞掉，连带给他补一口。
particle wax_on ~ ~0.3 ~ 0.2 0.2 0.2 0.05 8
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 0 true
kill @s
