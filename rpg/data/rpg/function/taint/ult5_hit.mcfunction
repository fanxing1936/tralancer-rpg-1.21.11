# 身上带着圣器的人走另一条 —— 见 ult5_hit_holy。
execute if entity @s[tag=rpg.holy] run return run function rpg:taint/ult5_hit_holy
effect give @s minecraft:poison 10 2 true
effect give @s minecraft:wither 7 1 true
damage @s 22 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
